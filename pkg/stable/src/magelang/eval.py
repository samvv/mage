
from typing import assert_never

from magelang.lang.mage.ast import *

EOF = '\uFFFF'

def accepts(expr: MageExpr, text: str, grammar: MageGrammar) -> bool:

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
            if expr.invert:
                for element in expr.elements:
                    if isinstance(element, str):
                        low = element
                        high = element
                    else:
                        low, high = element
                    if expr.ci:
                        ch = ch.lower()
                        low = low.lower()
                        high = high.lower()
                    if ord(ch) >= ord(low) and ord(ch) <= ord(high):
                        return False
                offset += 1
                return True
            else:
                for element in expr.elements:
                    if isinstance(element, str):
                        low = element
                        high = element
                    else:
                        low, high = element
                    if expr.ci:
                        ch = ch.lower()
                        low = low.lower()
                        high = high.lower()
                    if ord(ch) >= ord(low) and ord(ch) <= ord(high):
                        offset += 1
                        return True
                return False

        if isinstance(expr, MageSeqExpr):
            keep = offset
            for element in expr.elements:
                if not visit(element):
                    offset = keep
                    return False
            return True

        if isinstance(expr, MageChoiceExpr):
            for element in expr.elements:
                if visit(element):
                    return True
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
            return result

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

    return visit(expr)
