
from .ast import *

FAIL = 1
EMPTY = 2

def transform(grammar: Grammar) -> Grammar:

    def visit(expr: Expr) -> Expr | int:
        if isinstance(expr, LitExpr):
            if not expr.text:
                return EMPTY
            return expr
        if isinstance(expr, ChoiceExpr):
            new_elements = []
            has_empty = False
            for element in expr.elements:
                new_element = visit(element)
                if new_element == FAIL:
                    continue
                if new_element == EMPTY:
                    has_empty = True
                    continue
                new_elements.append(new_element)
            if has_empty:
                new_elements.append(EMPTY)
            if not new_elements:
                return FAIL
            if len(new_elements) == 1:
                return new_elements[0]
            return ChoiceExpr(new_elements)
        if isinstance(expr, SeqExpr):
            new_elements = []
            has_fail = False
            for element in expr.elements:
                new_element = visit(element)
                if new_element == EMPTY:
                    continue
                if new_element == FAIL:
                    has_fail = True
                    continue
                new_elements.append(new_element)
            if has_fail:
                new_elements.append(FAIL)
            if not new_elements:
                return EMPTY
            if len(new_elements) == 1:
                return new_elements[0]
            return SeqExpr(new_elements)
        if isinstance(expr, CharSetExpr):
            # TODO remove overlapping ranges
            return expr
        if isinstance(expr, RefExpr):
            return expr
        raise RuntimeError(f'unexpected node {expr}')

    new_rules = []
    for rule in grammar.rules:
        new_expr = visit(rule.expr)
        if new_expr == FAIL:
            continue
        if new_expr == EMPTY:
            new_expr = LitExpr('')
        new_rules.append(Rule(rule.is_public, rule.is_token, rule.name, new_expr))

    return Grammar(rules=new_rules)

