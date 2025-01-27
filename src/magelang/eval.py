
from typing import assert_never

from magelang.analysis import is_eof
from magelang.lang.mage.ast import *

EOF = '\uFFFF'

def accepts(expr: MageExpr, text: str, grammar: MageGrammar) -> bool | None:
    """
    Check whether the given expression accepts the given text.

    Returns `None` when the maximum recursion depth was reached. This usually means that the grammar has an infinite loop.
    """

    offset = 0

    def peek(i: int = 0) -> str:
        k = offset + i
        return text[k] if k < len(text) else EOF

    def get_char() -> str:
        nonlocal offset
        ch = text[offset]
        offset += 1
        return ch

    def visit(expr: MageExpr) -> bool:

        nonlocal offset

        if is_eof(expr):
            return offset >= len(text)

        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            assert(rule is not None)
            assert(rule.expr is not None)
            return visit(rule.expr)

        if isinstance(expr, MageLitExpr):
            for i, ch in enumerate(expr.text):
                if peek(i) != ch:
                    return False
            offset += len(expr.text)
            return True

        if isinstance(expr, MageCharSetExpr):
            ch = peek()
            for element in expr.canonical_elements:
                if isinstance(element, str):
                    low = element
                    high = element
                else:
                    low, high = element
                if ord(ch) >= ord(low) and ord(ch) <= ord(high):
                    offset += 1
                    return True
            return False

        if isinstance(expr, MageSeqExpr):
            for element in expr.elements:
                if not visit(element):
                    return False
            return True

        if isinstance(expr, MageChoiceExpr):
            keep = offset
            for element in expr.elements:
                if visit(element):
                    return True
                offset = keep
            return False

        if isinstance(expr, MageRepeatExpr):
            keep = offset
            for _ in range(0, expr.min):
                if not visit(expr.expr):
                    offset = keep
                    return False
            if expr.max == POSINF:
                while True:
                    if not visit(expr.expr):
                        break
            else:
                assert(isinstance(expr.max, int))
                for _ in range(expr.min, expr.max):
                    if not visit(expr.expr):
                        break
            return True

        if isinstance(expr, MageLookaheadExpr):
            keep = offset
            result = visit(expr.expr)
            offset = keep
            return not result if expr.is_negated else result

        if isinstance(expr, MageListExpr):
            if not visit(expr.element):
                return True
            while True:
                keep = offset
                if not visit(expr.separator):
                    return True
                if not visit(expr.element):
                    offset = keep
                    return True

        if isinstance(expr, MageHideExpr):
            return visit(expr.expr)

        assert_never(expr)

    try:
        result = visit(expr)
    except RecursionError:
        return
    if not result:
        return result
    return offset == len(text)
