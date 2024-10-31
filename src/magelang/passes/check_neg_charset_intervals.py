
from magelang.logging import error, warn
from magelang.ast import CharSetExpr, Expr, Grammar, for_each_expr
from magelang.emitter import escape

def check_neg_charset_intervals(grammar: Grammar) -> Grammar:

    def check(expr: Expr) -> None:
        if isinstance(expr, CharSetExpr):
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
