

from magelang.lang.mage.ast import MageExpr, MageGrammar, MageListExpr, make_list_expr, rewrite_each_child_expr, rewrite_each_expr
from magelang.manager import declare_pass


@declare_pass()
def mage_to_core(grammar: MageGrammar) -> MageGrammar:
    """
    Compress the grammar to contain fewer types of expressions.

    This is useful when you need to switch over the different types and can
    cope with a little loss of information.
    """
    def proc(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageListExpr):
            return make_list_expr(expr.element, expr.separator, expr.min_count)
        return rewrite_each_child_expr(expr, proc)
    return rewrite_each_expr(grammar, proc)
