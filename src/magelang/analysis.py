
from magelang.util import nonnull, unreachable
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
    return isinstance(expr, MageCharSetExpr) and len(expr) == 0


Edge = str

class Prefix:

    def __init__(self, rules: list[MageRule] = []) -> None:
        self.rules = rules
        self._mapping = dict[Edge, Prefix]()

    def add_rule(self, rule: MageRule) -> None:
        self.rules.append(rule)

    def __contains__(self, edge: Edge) -> bool:
        return edge in self._mapping

    def __getitem__(self, edge: Edge) -> 'Prefix':
        return self._mapping[edge]

    def __setitem__(self, edge: Edge, value: 'Prefix') -> None:
        self._mapping[edge] = value

def first_tokens(grammar: MageGrammar) -> list[MageRule]:

    out = set()

    def visit(expr: MageExpr):
        assert(not isinstance(expr, MageLitExpr))
        assert(not isinstance(expr, MageCharSetExpr))
        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None or rule.expr is None:
                return
            if not rule.is_public:
                visit(rule.expr)
                return
            if grammar.is_token_rule(rule):
                out.add(rule.name)
            return
        if isinstance(expr, MageSeqExpr):
            visit(expr.elements[0])
            return
        if isinstance(expr, MageChoiceExpr):
            for element in expr.elements:
                visit(element)
            return
        if isinstance(expr, MageRepeatExpr):
            visit(expr.expr)
            return
        if isinstance(expr, MageListExpr):
            visit(expr.element)
            return
        if isinstance(expr, MageHideExpr):
            visit(expr.expr)
            return
        assert_never(expr)

    for rule in grammar.rules:
        if grammar.is_parse_rule(rule) and rule.expr is not None:
            visit(rule.expr)

    return list(nonnull(grammar.lookup(name)) for name in out)

def overlapping_tokens(grammar: MageGrammar) -> list[list[MageRule]]:

    main = set(rule.name for rule in grammar.rules if rule.is_token and not rule.is_keyword and rule.expr is not None)
    print(main)
    out = [ main ]

    root_prefix = Prefix()

    def split(rule: MageRule) -> None:
        print('remove')
        main.remove(rule.name)
        out.append(set([ rule.name ]))

    def populate(expr: MageExpr, owner: MageRule) -> None:
        prefix = root_prefix
        def visit(expr: MageExpr, last: bool) -> None:
            nonlocal prefix
            if isinstance(expr, MageRefExpr):
                rule = grammar.lookup(expr.name)
                if rule is not None and rule.expr is not None:
                    visit(rule.expr, last)
                return
            if isinstance(expr, MageLitExpr):
                for ch in expr.text:
                    if ch in prefix:
                        prefix = prefix[ch]
                    else:
                        new_prefix = Prefix()
                        prefix[ch] = new_prefix
                        prefix = new_prefix
                if last:
                    if prefix.rules:
                        split(owner)
                    prefix.add_rule(owner)
                return
        return visit(expr, True)

    for rule in grammar.rules:
        if rule.is_token and not rule.is_keyword and rule.expr is not None:
            populate(rule.expr, rule)

    print(out)
    return list(list(nonnull(grammar.lookup(name)) for name in rules) for rules in out)

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


