
from intervaltree import Interval, IntervalTree

from magelang.lang.mage.ast import *
from magelang.logging import warn
from magelang.lang.mage.emitter import escape
from magelang.manager import declare_pass

def _pretty(low, high) -> str:
    return escape(low) if low == high else f'{escape(low)}-{escape(high)}'

@declare_pass()
def mage_check_overlapping_charset_intervals(grammar: MageGrammar) -> MageGrammar:

    def visit_expr(expr: MageExpr) -> None:

        if isinstance(expr, MageCharSetExpr):
            tree = IntervalTree()
            for element in expr.elements:
                if isinstance(element, tuple):
                    low, high = element
                else:
                    low = element
                    high = element
                # This check exists because invalid edges may be present in the CharSetExpr
                if low <= high:
                    i = Interval(ord(low), ord(high)+1)
                    other = tree[i.begin:i.end]
                    for i in other:
                        warn(f'interval {_pretty(low, high)} overlaps with {_pretty(chr(i.begin), chr(i.end-1))}')
                    tree.add(i)
            return

        for_each_direct_child_expr(expr, visit_expr)

    def visit_rule(element: MageRule) -> None:
        if element.expr is not None:
            visit_expr(element.expr)

    for_each_rule(grammar, visit_rule)

    return grammar
