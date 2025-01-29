

from magelang.lang.mage.ast import MageExpr, MageGrammar, MageHideExpr, rewrite_each_child_expr, rewrite_each_expr
from magelang.manager import declare_pass

@declare_pass()
def mage_unhide(grammar: MageGrammar) -> MageGrammar:
    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageHideExpr):
            return expr.expr
        return rewrite_each_child_expr(expr, rewrite_expr)
    return rewrite_each_expr(grammar, rewrite_expr)
