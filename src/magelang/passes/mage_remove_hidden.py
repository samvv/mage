
from magelang.lang.mage.ast import *
from magelang.manager import declare_pass

@declare_pass()
def mage_remove_hidden(grammar: MageGrammar) -> MageGrammar:
    """
    Remove hide expressions from the grammar and replace them with the empty string.

    Use simplify() to actually eliminate these empty sequences.
    """

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageHideExpr):
            return MageSeqExpr([])
        return rewrite_each_child_expr(expr, rewrite_expr)

    def rewrite_rule(rule: MageRule) -> MageRule:
        if rule.expr is None:
            return rule
        return rule.derive(expr=rewrite_expr(rule.expr))

    return rewrite_each_rule(grammar, rewrite_rule)
