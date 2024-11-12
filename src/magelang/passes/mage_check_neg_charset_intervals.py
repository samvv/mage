
from magelang.logging import error
from magelang.lang.mage.ast import MageCharSetExpr, MageExpr, MageGrammar, for_each_expr
from magelang.lang.mage.emitter import escape

def mage_check_neg_charset_intervals(grammar: MageGrammar) -> MageGrammar:

    def check(expr: MageExpr) -> None:
        if isinstance(expr, MageCharSetExpr):
            for element in expr.elements:
                if isinstance(element, tuple):
                    low, high = element
                    if ord(low) > ord(high):
                        error(f"invalid character range: character '{escape(low)}' (0x{ord(low):04X}) is lower than '{escape(high)}' (0x{ord(high):04X})")
            return
        for_each_expr(expr, check)

    for rule in grammar.rules:
        if rule.expr is not None:
            check(rule.expr)

    return grammar
