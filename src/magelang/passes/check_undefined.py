
from ..logging import error
from ..ast import Grammar, RefExpr, Expr, for_each_expr

def check_undefined(grammar: Grammar) -> Grammar:

    def traverse(expr: Expr) -> None:
        if isinstance(expr, RefExpr):
            if grammar.lookup(expr.name) is None:
                error(f"Undefined rule referenced: {expr.name}")
            return
        for_each_expr(expr, traverse)

    for rule in grammar.rules:
        if rule.expr is not None:
            traverse(rule.expr)

    return grammar
