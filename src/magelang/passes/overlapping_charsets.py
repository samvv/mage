
from ..ast import *
from ..logging import warn
from intervaltree import Interval, IntervalTree

def _pretty(low, high) -> str:
    return low if low == high else f'{low}-{high}'

def overlapping_charsets(grammar: Grammar) -> Grammar:

    def visit(expr: Expr) -> None:

        if isinstance(expr, CharSetExpr):
            tree = IntervalTree()
            for element in expr.elements:
                if isinstance(element, tuple):
                    low, high = element
                else:
                    low = element
                    high = element
                i = Interval(ord(low), ord(high)+1)
                other = tree[i.begin:i.end]
                for i in other:
                    warn(f'interval {_pretty(low, high)} overlaps with {_pretty(chr(i.begin), chr(i.end-1))}')
                tree.add(i)
            return

        for_each_expr(expr, visit)

    for rule in grammar.rules:
        if rule.expr is not None:
            visit(rule.expr)

    return grammar
