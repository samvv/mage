
from collections.abc import Iterator

from sortedcontainers.sorteddict import KeysView
from magelang.graph import Graph, dump_graph, strongconnect
from magelang.util import unreachable
from magelang.lang.mage.ast import *

# FIXME needs to be extensively tested
def is_empty(expr: MageExpr) -> bool:
    if isinstance(expr, MageLitExpr):
        return len(expr.text) == 0
    if isinstance(expr, MageCharSetExpr):
        return len(expr) == 0
    if isinstance(expr, MageLookaheadExpr):
        return True
    if isinstance(expr, MageRepeatExpr):
        return is_empty(expr) or expr.max == 0
    if isinstance(expr, MageSeqExpr):
        return len(expr.elements) == 0 or all(is_empty(el) for el in expr.elements)
    if isinstance(expr, MageChoiceExpr):
        return len(expr.elements) == 0 or all(is_empty(el) for el in expr.elements)
    unreachable()

# FIXME needs to be extensively tested
def can_be_empty(expr: MageExpr, *, grammar: MageGrammar) -> bool:
    visited = set()
    def visit(expr: MageExpr) -> bool:
        if isinstance(expr, MageLitExpr):
            return len(expr.text) == 0
        if isinstance(expr, MageHideExpr):
            return visit(expr.expr)
        if isinstance(expr, MageRefExpr):
            if expr.name in visited:
                return False
            visited.add(expr.name)
            rule = grammar.lookup(expr.name)
            # If a rule is not defined, it CAN be empty if defined; we just don't know for sure.
            # Likewise if we are dealing with an external rule, chances are it might be empty.
            return rule is None or rule.expr is None or visit(rule.expr)
        if isinstance(expr, MageCharSetExpr):
            return len(expr) == 0
        if isinstance(expr, MageLookaheadExpr):
            return True
        if isinstance(expr, MageListExpr):
            return expr.min_count == 0 or visit(expr.element)
        if isinstance(expr, MageRepeatExpr):
            return expr.min == 0 or visit(expr.expr)
        if isinstance(expr, MageSeqExpr):
            return len(expr.elements) == 0 or all(visit(el) for el in expr.elements)
        if isinstance(expr, MageChoiceExpr):
            return len(expr.elements) == 0 or any(visit(el) for el in expr.elements)
        assert_never(expr)
    return visit(expr)

def is_eof(expr: MageExpr) -> bool:
    # FIXME What about !any_char?
    # FIXME Why is this equivalent to MageLitExpr('') but the latter is not EOF?
    return isinstance(expr, MageCharSetExpr) and len(expr) == 0


Edge = tuple[str, str]

class Prefix:

    def __init__(self, rules: list[MageRule] | None = None) -> None:
        self.rules = rules if rules is not None else []
        self._tree = IntervalTree()

    def add_rule(self, rule: MageRule) -> None:
        self.rules.append(rule)

    def __contains__(self, key: Edge | str) -> bool:
        interval = Interval(ord(key), ord(key)+1) if isinstance(key, str) else key
        return any(other.contains_interval(interval) for other in self._tree.overlap(interval))

    def __getitem__(self, ch: str | slice) -> 'Prefix':
        if isinstance(ch, str):
            interval = Interval(ord(ch), ord(ch)+1)
        elif isinstance(ch, slice):
            interval = Interval(ord(ch.start), ord(ch.stop)+1)
        else:
            raise KeyError(f'{edge} is not a valid prefix key')
        result = self._tree.overlap(interval)
        assert(len(result) == 1)
        return next(iter(result)).data

    def __setitem__(self, edge: str | slice, value: 'Prefix') -> None:
        if isinstance(edge, str):
            interval = Interval(ord(edge), ord(edge)+1, value)
        elif isinstance(edge, slice):
            interval = Interval(ord(edge.start), ord(edge.stop)+1, value)
        else:
            raise KeyError(f'{edge} is not a valid prefix key')
        self._tree.add(interval)

    def __iter__(self) -> Iterator[tuple[Edge, 'Prefix']]:
        for interval in self._tree:
            yield ((chr(interval.begin), chr(interval.end-1)), interval.data)


def overlapping_tokens(grammar: MageGrammar) -> Generator[list[MageRule]]:

    root_prefix = Prefix()

    def populate(expr: MageExpr, owner: MageRule) -> None:
        def visit(prefix: Prefix, expr: MageExpr, last: bool) -> list[Prefix]:
            new_prefixes = []
            if isinstance(expr, MageRefExpr):
                rule = grammar.lookup(expr.name)
                if rule is not None and rule.expr is not None:
                    new_prefixes.extend(visit(prefix, rule.expr, last))
            elif isinstance(expr, MageLitExpr):
                for ch in expr.text:
                    if ch in prefix:
                        prefix = prefix[ch]
                    else:
                        new_prefix = Prefix()
                        prefix[ch] = new_prefix
                        prefix = new_prefix
            elif isinstance(expr, MageCharSetExpr):
                for element in expr.canonical_elements:
                    if isinstance(element, tuple):
                        low, high = element
                    else:
                        low = element
                        high = element
                    new_prefix = Prefix()
                    prefix[low:high] = new_prefix
            elif isinstance(expr, MageRepeatExpr):
                if expr.min == 0:
                    new_prefixes.append(prefix)
                new_prefixes.extend(visit(prefix, expr.expr, last))
            else:
                assert_never(expr)
            new_prefixes.append(prefix)
            if last:
                for prefix in new_prefixes:
                    prefix.add_rule(owner)
            return new_prefixes
        visit(root_prefix, expr, True)

    for rule in grammar.rules:
        if rule.is_token and not rule.is_keyword and rule.expr is not None:
            populate(rule.expr, rule)

    def visit(prefix: Prefix) -> Generator[list[MageRule]]:
        if prefix.rules:
            yield prefix.rules
        for _, child in prefix:
            yield from visit(child)

    return visit(root_prefix)

    # # TODO It might be possible to cleverly optimise this
    # graph = Graph[str]()
    # rules = list(rule for rule in grammar.rules if grammar.is_token_rule(rule) and not rule.is_keyword)
    # for src, dst in permutations(rules, 2):
    #     graph.add_edge(src.name, dst.name)
    # def visit(prefix: Prefix) -> None:
    #     for src, dst in permutations(prefix.rules, 2):
    #         graph.remove_edge(src.name, dst.name)
    #     for _, child in prefix:
    #         visit(child)
    # visit(root_prefix)

    # return list(list(nonnull(grammar.lookup(name)) for name in scc) for scc in strongconnect(graph))

def issub(left: IntervalTree, right: IntervalTree) -> bool:
    return all(right.contains_interval(interval) for interval in left)

@lru_cache
def do_match(pattern: MageExpr, expr: MageExpr, *, grammar: MageGrammar) -> bool:

    def empty(): return MageLitExpr('')

    def consume(pattern: MageExpr, expr: MageExpr) -> MageExpr | None:
        if isinstance(pattern, MageLitExpr) and isinstance(expr, MageLitExpr):
            n = len(pattern.text)
            m = len(expr.text)
            for i in range(0, min(n, m)):
                ch_0 = pattern.text[i]
                ch_1 = expr.text[i]
                if ch_0 != ch_1:
                    return None
            return expr.derive(text=expr.text[n:]) if n < m else empty()
        if isinstance(pattern, MageCharSetExpr) and isinstance(expr, MageCharSetExpr):
            print('----')
            print(expr.tree)
            print(pattern.tree)
            print(expr.tree - pattern.tree)
            print(pattern.tree - expr.tree)
            return empty() if issub else None
        if isinstance(pattern, MageCharSetExpr) and isinstance(expr, MageLitExpr):
            if len(expr.text) == 0:
                return None
            if not pattern.contains_char(expr.text[0]):
                return empty()
            return expr.derive(text=expr.text[1:])
        if isinstance(pattern, MageSeqExpr):
            result = expr
            for element in pattern.elements:
                result = consume(element, expr)
                if result is None:
                    return None
            return result
        assert_never(pattern)
        assert_never(expr)

    return bool(consume(pattern, expr))

@lru_cache
def intersects(left: MageExpr, right: MageExpr, *, grammar: MageGrammar, default: bool = False) -> bool:
    """
    Check whether the suffix of the first expression, when randomly generated,
    can ever be equal to the prefix of the second expression.
    """

    # Holds which pairs of expressions have already been visited.
    # When two expressions A and B have already been visited, it is guaranteed
    # that we will visit them again in the future in exactly the same way as
    # before due to the deterministic, side-effect-free nature of the grammar.
    visited = set()

    FALSE = 0      # Must be equal to int(False)
    TRUE = 1       # Must be equal to int(True)
    UNDEFINED = 2  # Returned when the algorithm couldn't calculate the requested property
    SKIP_LEFT = 3  # Returned when the LHS does not parse/emit any characters
    SKIP_RIGHT = 4 # Reurned when the RHS does not parse/emit any characters

    def visit(left: MageExpr, right: MageExpr) -> int:
        key = (left, right)
        if key in visited:
            return UNDEFINED
        visited.add(key)
        if isinstance(left, MageSeqExpr):
            for element in reversed(left.elements):
                result = visit(element, right)
                if result != SKIP_LEFT:
                    return result
            return FALSE
        if isinstance(right, MageSeqExpr):
            for element in right.elements:
                result = visit(left, element)
                if result != SKIP_RIGHT:
                    return result
            return FALSE
        if isinstance(left, MageLookaheadExpr):
            return SKIP_LEFT
        if isinstance(right, MageLookaheadExpr):
            return SKIP_RIGHT
        if isinstance(left, MageRefExpr):
            rule = grammar.lookup(left.name)
            if rule is None or rule.expr is None:
                return default
            return visit(rule.expr, right)
        if isinstance(right, MageRefExpr):
            rule = grammar.lookup(right.name)
            if rule is None or rule.expr is None:
                return default
            return visit(left, rule.expr)
        if isinstance(left, MageRepeatExpr):
            result = visit(left.expr, right)
            if result != FALSE:
                return result
            if left.min == 0:
                return SKIP_LEFT
            return FALSE
        if isinstance(right, MageRepeatExpr):
            result = visit(left, right.expr)
            if result != FALSE:
                return result
            if right.min == 0:
                return SKIP_RIGHT
            return FALSE
        if isinstance(left, MageHideExpr):
            return visit(left.expr, right)
        if isinstance(right, MageHideExpr):
            return visit(left, right.expr)
        if isinstance(left, MageListExpr):
            return visit(left.element, right)
        if isinstance(right, MageListExpr):
            return visit(left, right.element)
        if isinstance(left, MageChoiceExpr):
            return any(visit(el, right) for el in left.elements)
        if isinstance(right, MageChoiceExpr):
            return any(visit(left, el) for el in right.elements)
        if isinstance(left, MageLitExpr) and isinstance(right, MageLitExpr):
            return left.text[-1] == right.text[0]
        if isinstance(left, MageLitExpr) and isinstance(right, MageCharSetExpr):
            return right.contains_char(left.text[-1])
        if isinstance(left, MageCharSetExpr) and isinstance(right, MageLitExpr):
            return left.contains_char(right.text[0])
        if isinstance(left, MageCharSetExpr) and isinstance(right, MageCharSetExpr):
            return MageCharSetExpr.overlaps(left, right)
        print(left)
        print(right)
        unreachable()

    result = visit(left, right)
    # assert(result != SKIP_LEFT and result != SKIP_RIGHT)
    return result != FALSE


