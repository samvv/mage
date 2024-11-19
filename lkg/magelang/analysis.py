
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
    return isinstance(expr, MageCharSetExpr) and len(expr) == 0

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

    FALSE = 0 # Must be equal to int(False)
    TRUE = 1 # Must be equal to int(True)
    UNDEFINED = 2 # Returned when the algorithm couldn't calculate the requested property
    SKIP_LEFT = 3 # Returned when the LHS does not parse/emit any characters
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
            return right.contains(left.text[-1])
        if isinstance(left, MageCharSetExpr) and isinstance(right, MageLitExpr):
            return left.contains(right.text[0])
        if isinstance(left, MageCharSetExpr) and isinstance(right, MageCharSetExpr):
            return MageCharSetExpr.overlaps(left, right)
        print(left)
        print(right)
        unreachable()

    result = visit(left, right)
    # assert(result != SKIP_LEFT and result != SKIP_RIGHT)
    return result != FALSE


