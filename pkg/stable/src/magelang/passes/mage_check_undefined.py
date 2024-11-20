
from magelang.logging import error
from magelang.lang.mage.ast import MageGrammar, MageRefExpr, MageExpr, for_each_expr

def mage_check_undefined(grammar: MageGrammar) -> MageGrammar:

    def traverse(expr: MageExpr) -> None:
        if isinstance(expr, MageRefExpr):
            if grammar.lookup(expr.name) is None:
                error(f"undefined rule referenced: {expr.name}")
            return
        for_each_expr(expr, traverse)

    for rule in grammar.rules:
        if rule.expr is not None:
            traverse(rule.expr)

    return grammar
