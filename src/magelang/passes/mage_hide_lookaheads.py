
from magelang.lang.mage.ast import MageExpr, MageGrammar, MageHideExpr, MageLookaheadExpr, MageRule, rewrite_each_child_expr, rewrite_each_rule
from magelang.manager import declare_pass

@declare_pass()
def mage_hide_lookaheads(grammar: MageGrammar) -> MageGrammar:

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageHideExpr):
            return expr
        if isinstance(expr, MageLookaheadExpr):
            return MageHideExpr(expr)
        return rewrite_each_child_expr(expr, rewrite_expr)

    def rewrite_rule(rule: MageRule) -> MageRule:
        if rule.expr is None or grammar.is_token_rule(rule):
            return rule
        return rule.derive(expr=rewrite_expr(rule.expr))

    return rewrite_each_rule(grammar, rewrite_rule)
