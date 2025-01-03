
from magelang.lang.mage.ast import *

def mage_add_prefix(grammar: MageGrammar, prefix: str) -> MageGrammar:

    def rename(name: str) -> str:
        return prefix + name

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageRefExpr):
            return expr.derive(name=rename(expr.name))
        return rewrite_each_child_expr(expr, rewrite_expr)

    def rewrite_rule(rule: MageRule) -> MageRule:
        expr = rewrite_expr(rule.expr) if rule.expr is not None else None
        return rule.derive(name=rename(rule.name), expr=expr)

    return rewrite_each_rule(grammar, rewrite_rule)
