
from magelang.util import unreachable
from .ast import *

# FIXME needs to be extensively tested
def is_empty(expr: Expr) -> bool:
    if isinstance(expr, LitExpr):
        return len(expr.text) == 0
    if isinstance(expr, CharSetExpr):
        return len(expr) == 0
    if isinstance(expr, LookaheadExpr):
        return True
    if isinstance(expr, RepeatExpr):
        return is_empty(expr) or expr.max == 0
    if isinstance(expr, SeqExpr):
        return len(expr.elements) == 0 or all(is_empty(el) for el in expr.elements)
    if isinstance(expr, ChoiceExpr):
        return len(expr.elements) == 0 or all(is_empty(el) for el in expr.elements)
    unreachable()

# FIXME needs to be extensively tested
def can_be_empty(expr: Expr, *, grammar: Grammar) -> bool:
    if isinstance(expr, LitExpr):
        return len(expr.text) == 0
    if isinstance(expr, RefExpr):
        rule = grammar.lookup(expr.name)
        assert(rule is not None and rule.expr is not None)
        return can_be_empty(rule.expr, grammar=grammar)
    if isinstance(expr, CharSetExpr):
        return len(expr) == 0
    if isinstance(expr, LookaheadExpr):
        return True
    if isinstance(expr, ListExpr):
        return expr.min_count == 0
    if isinstance(expr, RepeatExpr):
        return expr.min == 0 or can_be_empty(expr.expr, grammar=grammar)
    if isinstance(expr, SeqExpr):
        return len(expr.elements) == 0 or all(can_be_empty(el, grammar=grammar) for el in expr.elements)
    if isinstance(expr, ChoiceExpr):
        return len(expr.elements) == 0 or any(can_be_empty(el, grammar=grammar) for el in expr.elements)
    unreachable()

def is_eof(expr: Expr) -> bool:
    if isinstance(expr, CharSetExpr):
        return len(expr) == 0
    return False

def intersects(left: Expr, right: Expr, *, grammar: Grammar, default: bool = False) -> bool:
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

    def visit(left: Expr, right: Expr) -> int:
        key = (left, right)
        if key in visited:
            return UNDEFINED
        visited.add(key)
        if isinstance(left, SeqExpr):
            for element in reversed(left.elements):
                result = visit(element, right)
                if result != SKIP_LEFT:
                    return result
            return FALSE
        if isinstance(right, SeqExpr):
            for element in right.elements:
                result = visit(left, element)
                if result != SKIP_RIGHT:
                    return result
            return FALSE
        if isinstance(left, LookaheadExpr):
            return SKIP_LEFT
        if isinstance(right, LookaheadExpr):
            return SKIP_RIGHT
        if isinstance(left, RefExpr):
            rule = grammar.lookup(left.name)
            if rule is None or rule.expr is None:
                return default
            return visit(rule.expr, right)
        if isinstance(right, RefExpr):
            rule = grammar.lookup(right.name)
            if rule is None or rule.expr is None:
                return default
            return visit(left, rule.expr)
        if isinstance(left, RepeatExpr):
            result = visit(left.expr, right)
            if result != FALSE:
                return result
            if left.min == 0:
                return SKIP_LEFT
            return FALSE
        if isinstance(right, RepeatExpr):
            result = visit(left, right.expr)
            if result != FALSE:
                return result
            if right.min == 0:
                return SKIP_RIGHT
            return FALSE
        if isinstance(left, HideExpr):
            return visit(left.expr, right)
        if isinstance(right, HideExpr):
            return visit(left, right.expr)
        if isinstance(left, ListExpr):
            return visit(left.element, right)
        if isinstance(right, ListExpr):
            return visit(left, right.element)
        if isinstance(left, ChoiceExpr):
            return any(visit(el, right) for el in left.elements)
        if isinstance(right, ChoiceExpr):
            return any(visit(left, el) for el in right.elements)
        if isinstance(left, LitExpr) and isinstance(right, LitExpr):
            return left.text[-1] == right.text[0]
        if isinstance(left, LitExpr) and isinstance(right, CharSetExpr):
            return right.contains(left.text[-1])
        if isinstance(left, CharSetExpr) and isinstance(right, LitExpr):
            return left.contains(right.text[0])
        if isinstance(left, CharSetExpr) and isinstance(right, CharSetExpr):
            return CharSetExpr.overlaps(left, right)
        print(left)
        print(right)
        unreachable()

    result = visit(left, right)
    # assert(result != SKIP_LEFT and result != SKIP_RIGHT)
    return result != FALSE


