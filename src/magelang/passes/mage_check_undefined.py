
from magelang.logging import error
from magelang.lang.mage.ast import MageGrammar, MageRefExpr, MageExpr, MageRule, for_each_direct_child_expr, for_each_rule, lookup_ref

def mage_check_undefined(grammar: MageGrammar) -> MageGrammar:

    def visit_expr(expr: MageExpr) -> None:
        if isinstance(expr, MageRefExpr):
            if lookup_ref(expr) is None:
                error(f"undefined rule referenced: {expr.name}")
            return
        for_each_direct_child_expr(expr, visit_expr)

    def visit_rule(rule: MageRule) -> None:
        if rule.expr is not None:
            visit_expr(rule.expr)

    for_each_rule(grammar, visit_rule)

    return grammar
