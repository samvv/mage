
from dataclasses import dataclass
import math

from magelang.util import SeqSet, nonnull, unreachable
from magelang.graph import DGraph, toposort
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
    # FIXME What about !any_char? We might want to enumerate all possible characters
    return isinstance(expr, MageCharSetExpr) and len(expr) == 0


def is_tokenizable(grammar: MageGrammar) -> bool:
    """
    Check whether a grammar can be correctly tokenized.

    When a rule is undefined, we assume the worst and this function will return `False`.
    """

    def has_nontoken(expr: MageExpr) -> bool:
        if isinstance(expr, MageCharSetExpr) or isinstance(expr, MageLitExpr):
            return False
        if isinstance(expr, MageSeqExpr) or isinstance(expr, MageChoiceExpr):
            return any(has_nontoken(element) for element in expr.elements)
        if isinstance(expr, MageRepeatExpr) or isinstance(expr, MageHideExpr) or isinstance(expr, MageLookaheadExpr):
            return has_nontoken(expr.expr)
        if isinstance(expr, MageListExpr):
            return has_nontoken(expr.element) or has_nontoken(expr.separator)
        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None or rule.expr is None:
                # We assume the worst and will report this as a nontoken
                return True
            if not rule.is_public:
                return has_nontoken(rule.expr)
            # Rule must be another token or a parse rule, which is invalid
            return True
        assert_never(expr)

    return not any(has_nontoken(nonnull(rule.expr)) for rule in grammar.rules if grammar.is_parse_rule(rule))


@lru_cache
def intersects(left: MageExpr, right: MageExpr, *, grammar: MageGrammar, default: bool = False) -> bool:
    """
    Check whether the suffix of the first expression, when randomly generated,
    can ever be equal to a prefix of the second expression.
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


type _Primitive = IntervalTree | str


class _CursorBase:
    pass


@dataclass
class _LitCursor(_CursorBase):
    expr: MageLitExpr
    index: int = 0

    def deref(self) -> _Primitive:
        return self.expr.text[self.index]

    def after_min(self) -> bool:
        return True

    def reset(self) -> None:
        self.index = 0

    def at_end(self) -> bool:
        return self.index == len(self.expr.text)

    def increment(self) -> None:
        self.index += 1


@dataclass
class _SeqCursor(_CursorBase):
    elements: list['Cursor']
    index: int = 0

    def deref(self) -> _Primitive:
        return self.elements[self.index].deref()

    def after_min(self) -> bool:
        return self.at_end() or self.elements[self.index].after_min()

    def at_end(self) -> bool:
        return self.index == len(self.elements)

    def reset(self) -> None:
        self.indexx = 0

    def increment(self) -> None:
        while self.index < len(self.elements):
            cursor = self.elements[self.index]
            if cursor.increment():
                break
            self.index += 1


@dataclass
class _RepeatCursor(_CursorBase):
    cursor: 'Cursor'
    min: int
    max: int
    count: int = 0

    def deref(self) -> _Primitive:
        return self.cursor.deref()

    def after_min(self) -> bool:
        return self.count >= self.min and self.cursor.after_min()

    def at_end(self) -> bool:
        return self.count == self.max

    def reset(self) -> None:
        self.count = 0
        self.cursor.reset()

    def increment(self) -> None:
        if not self.cursor.increment():
            self.cursor.reset()
            self.count += 1


@dataclass
class _CharSetCursor(_CursorBase):
    expr: MageCharSetExpr
    yielded: bool = False

    def deref(self) -> _Primitive:
        assert(not self.yielded)
        return self.expr.tree

    def after_min(self) -> bool:
        return True

    def at_end(self) -> bool:
        return self.yielded

    def reset(self) -> None:
        self.yielded = False

    def increment(self) -> None:
        self.yielded = True


type Cursor = _LitCursor | _SeqCursor | _RepeatCursor | _CharSetCursor


def _to_cursor(expr: MageExpr) -> Cursor:
    if isinstance(expr, MageLitExpr):
        return _LitCursor(expr)
    if isinstance(expr, MageCharSetExpr):
        return _CharSetCursor(expr)
    if isinstance(expr, MageRepeatExpr):
        return _RepeatCursor(_to_cursor(expr.expr), expr.min, expr.max)
    if isinstance(expr, MageSeqExpr):
        elements = list(_to_cursor(element) for element in expr.elements)
        return _SeqCursor(elements)
    assert_never(expr)


def is_subset(left: IntervalTree, right: IntervalTree) -> bool:
    for i in left:
        k = i.begin
        for j in sorted(right.overlap(i)):
            if j.begin > k:
                return False
            k = j.end
        if k < i.end:
            return False
    return True


def envelops(left: MageExpr, right: MageExpr, *, grammar: MageGrammar | None = None) -> bool:
    """
    Check that whatever token `right` accepts is also always accepted by `left`.

    Mathematically, this could somewhat be written as `left >= right`.

    `grammar` is only needed when other rules are being referenced.
    """

    c_left = _to_cursor(left)
    c_right = _to_cursor(right)

    def envelops_primitive(a: _Primitive, b: _Primitive) -> bool:
        if isinstance(a, str) and isinstance(b, str):
            return a == b
        if isinstance(a, IntervalTree) and isinstance(b, IntervalTree):
            return is_subset(b, a)
        if isinstance(a, IntervalTree) and isinstance(b, str):
            return a.overlaps_point(ord(b))
        if isinstance(a, str) and isinstance(b, IntervalTree):
            if len(b) != 1:
                return False
            i = next(iter(b))
            code = ord(a)
            return i.begin == code and i.end == code+1
        unreachable()

    while not c_right.at_end():
        if c_left.at_end():
            return False
        a = c_left.deref()
        b = c_right.deref()
        if not envelops_primitive(a, b):
            return False
        c_left.increment()
        c_right.increment()

    return c_left.after_min()


def get_lexer_modes(grammar: MageGrammar) -> dict[str, int]:

    modes = dict[str, int]()

    token_rules = SeqSet[MageRule]()
    for rule in grammar.elements:
        if grammar.is_token_rule(rule):
            token_rules.append(rule)
            modes[rule.name] = 0

    next_token_rules = SeqSet[MageRule]()
    while True:
        n = len(token_rules)
        for i in range(0, n):
            rule_a = token_rules[i]
            match = False
            for k in range(i+1, n):
                rule_b = token_rules[k]
                if envelops(nonnull(rule_a.expr), nonnull(rule_b.expr), grammar=grammar):
                    match = True
            if match:
                next_token_rules.append(rule_a)
                modes[rule_a.name] += 1
        if not next_token_rules:
            break
        token_rules = next_token_rules
        next_token_rules = SeqSet[MageRule]()

    return modes


@lru_cache
def reference_graph(grammar: MageGrammar) -> DGraph[MageRule, None]:

    graph = DGraph[MageRule, None]()

    def visit_rule(src: MageRule) -> None:
        def visit(expr: MageExpr) -> None:
            if isinstance(expr, MageRefExpr):
                dst = lookup_ref(expr)
                if dst is not None:
                    graph.add_edge(src, dst, None)
            else:
                for_each_direct_child_expr(expr, visit)
        if src.expr is not None:
            visit(src.expr)

    for rule in grammar.get_parse_rules():
        visit_rule(rule)

    return graph


def get_recursive(grammar: MageGrammar) -> list[list[MageRule]]:
    """
    Get all the recursive rules in the grammar.

    Rules that reference each other form a cycle. This function will return a
    list of rules for each isolated cycle.
    """
    graph = reference_graph(grammar)
    sccs = toposort(graph)
    return [ scc for scc in sccs if len(scc) > 1 ]


def get_roots(rules: list[MageRule], grammar: MageGrammar) -> Iterable[MageRule]:
    """
    Get the root recursive rules for the given set of rules, if any.

    A root recursive rule is a rule that is referenced more than once by other
    rules that form part of the same cycle.
    """
    # FIXME is the definition of a root correct?
    graph = reference_graph(grammar)
    for rule in rules:
        n = sum(1 for v, _ in graph.incoming_edges(rule) if v in rules)
        if n > 1:
            yield rule


NONE   = 0
PREFIX = 1
INFIXL = 2
INFIXR = 4
INFIX  = 6
POSTFIX = 8


def fixity(rule: MageRule, roots: list[MageRule], grammar: MageGrammar) -> int:
    """
    Get the fixity of a Mage expression.

    The fixity is either:
    - Prefix for rules that start with an operator (e.g. ++1, await foo)
    - Infix for rules that have the first operator in the middle (e.g. 1 + 2, 5 << 2)
    - Suffix for rules that have the first operator at the end (e.g. result?, k--)
    """

    if rule.expr is None:
        return NONE

    k = 0
    indices = []
    visited = set[MageRule]()

    def visit(expr: MageExpr) -> None:
        nonlocal k
        if isinstance(expr, MageLitExpr) or isinstance(expr, MageCharSetExpr):
            k += 1
        elif isinstance(expr, MageRefExpr):
            rule = lookup_ref(expr)
            if rule in roots:
                indices.append(k)
                return
            if rule is None or rule in visited or rule.expr is None:
                # We assume the rule is not part of this cycle
                return
            visited.add(rule)
            visit(rule.expr)
        elif isinstance(expr, MageSeqExpr):
            for child in expr.elements:
                visit(child)
        elif isinstance(expr, MageChoiceExpr):
            start = k
            end = math.inf
            for child in expr.elements:
                visit(child)
                end = min(end, k)
                k = start
            k = end
        elif isinstance(expr, MageLookaheadExpr):
            pass
        elif isinstance(expr, MageHideExpr):
            visit(expr.expr)
        elif isinstance(expr, MageRepeatExpr):
            # FIXME presumably we could get the result of visit() and multiply with expr.min
            for _ in range(expr.min):
                visit(expr.expr)
        else:
            assert_never(expr)

    visit(rule.expr)

    n = len(indices)
    if n == 0:
        return NONE
    if n == 1:
        i = indices[0]
        return POSTFIX if i == 0 else PREFIX
    if n == 2:
        i = indices[0]
        j = indices[1]
        return NONE if i == j else INFIX
    # FIXME This mode (e.g. ternary operators) should also be supported
    #       See for example Agda, which can have very complex operators
    return NONE


@dataclass
class Grouping:
    prefix: list[MageRule]
    infix: list[MageRule]
    postfix: list[MageRule]


def group_by_fixity(
    nonroots: list[MageRule],
    roots: list[MageRule],
    grammar: MageGrammar
) -> Grouping:
    """
    Groups given rules by their fixity.

    We assume the root recursive rules have already been filtered out of the input.
    """
    prefix = list[MageRule]()
    infix = list[MageRule]()
    postfix = list[MageRule]()
    for rule in nonroots:
        x = fixity(rule, roots, grammar)
        if x == PREFIX:
            prefix.append(rule)
        elif x == INFIX:
            infix.append(rule)
        elif x == POSTFIX:
            postfix.append(rule)
        elif x != NONE:
            unreachable()
    return Grouping(prefix, infix, postfix)
