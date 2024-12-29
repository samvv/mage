
from magelang.logging import error
from magelang.lang.mage.ast import MageCharSetExpr, MageExpr, MageGrammar, MageRule, for_each_expr, for_each_rule
from magelang.lang.mage.emitter import escape

def mage_check_neg_charset_intervals(grammar: MageGrammar) -> MageGrammar:

    def visit_expr(expr: MageExpr) -> None:
        if isinstance(expr, MageCharSetExpr):
            for element in expr.elements:
                if isinstance(element, tuple):
                    low, high = element
                    if ord(low) > ord(high):
                        error(f"invalid character range: character '{escape(low)}' (0x{ord(low):04X}) is lower than '{escape(high)}' (0x{ord(high):04X})")
            return
        for_each_expr(expr, visit_expr)

    def visit_rule(rule: MageRule) -> None:
        if rule.expr is not None:
            visit_expr(rule.expr)

    for_each_rule(grammar, visit_rule)

    return grammar
