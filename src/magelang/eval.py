
from typing import NewType, assert_never

from magelang.analysis import is_eof
from magelang.constants import DEFAULT_MAX_REPEATS
from magelang.helpers import get_field_name, get_fields
from magelang.lang.mage.ast import *
from magelang.runtime import Punctuated
from magelang.util import NameGenerator

EOF = '\uFFFF'

class Error:

    def __init__(self, code: int) -> None:
        self.code = code

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Error) and self.code == value.code

    def __hash__(self) -> int:
        return hash(self.code)

SUCCESS   = Error(0)
NO_MATCH  = Error(1)
RECMAX    = Error(2)

class DynamicNode:

    def __init__(self, name: str, fields: 'dict[str, Any]') -> None:
        self.name = name
        self.fields = fields

def evaluate(
    rule: MageRule,
    text: str,
    max_repeats: int = DEFAULT_MAX_REPEATS
) -> DynamicNode | Error:

    offset = 0
    grammar = rule.grammar

    def peek(i: int = 0) -> str:
        k = offset + i
        return text[k] if k < len(text) else EOF

    def visit_backtrack(expr: MageExpr) -> tuple | DynamicNode | str | None:
        nonlocal offset
        keep = offset
        result = visit(expr)
        if result is not None:
            return result
        offset = keep

    def visit(expr: MageExpr) -> Any:

        nonlocal offset

        if is_eof(expr):
            if offset < len(text):
                return
            return ''

        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            assert(rule is not None)
            assert(rule.expr is not None)
            return visit(rule.expr)

        if isinstance(expr, MageLitExpr):
            for i, ch in enumerate(expr.text):
                if peek(i) != ch:
                    return
            offset += len(expr.text)
            return expr.text

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
                    return ch
            return

        if isinstance(expr, MageSeqExpr):
            elements = []
            for element in expr.elements:
                result = visit(element)
                if result is None:
                    return
                elements.append(element)
            return tuple(elements)

        if isinstance(expr, MageChoiceExpr):
            keep = offset
            for element in expr.elements:
                result = visit_backtrack(element)
                if result is not None:
                    return result
                offset = keep
            return

        if isinstance(expr, MageRepeatExpr):
            elements = []
            for _ in range(0, expr.min):
                result = visit(expr.expr)
                if result is None:
                    return
                elements.append(result)
            if expr.max == POSINF:
                i = 0
                while True:
                    if i == max_repeats:
                        raise RecursionError()
                    result = visit_backtrack(expr.expr)
                    if result is None:
                        break
                    elements.append(result)
                    i += 1
            else:
                if expr.max - expr.min < max_repeats:
                    for _ in range(expr.max - expr.min):
                        result = visit_backtrack(expr.expr)
                        if result is None:
                            break
                        elements.append(result)
                else:
                    i = 0
                    while True:
                        if i == max_repeats:
                            raise RecursionError()
                        result = visit_backtrack(expr.expr)
                        if result is None:
                            break
                        elements.append(result)
                        i += 1
            return elements

        if isinstance(expr, MageLookaheadExpr):
            keep = offset
            result = visit_backtrack(expr.expr)
            offset = keep
            if (result is None) == expr.is_negated:
                return ''
            return

        # if isinstance(expr, MageListExpr):
        #     elements = Punctuated()
        #     count = 0
        #     prev_element = visit_backtrack(expr.element)
        #     if prev_element is not None:
        #         count += 1
        #         while True:
        #             result = visit_backtrack(MageSeqExpr([
        #                 expr.separator,
        #                 expr.element,
        #             ]))
        #             if result is None:
        #                 break
        #             elements.append(prev_element, result[0])
        #             prev_element = result[1]
        #         elements.append_final(prev_element)
        #     if count < expr.min_count:
        #         return
        #     return elements

        if isinstance(expr, MageHideExpr):
            return visit(expr.expr)

        assert_never(expr)

    if rule.expr is None:
        return NO_MATCH

    fields = dict[str, Any]()
    for expr, field in get_fields(rule.expr, grammar=grammar):
        try:
            result = visit(expr)
        except RecursionError:
            return RECMAX
        if result is None:
            return NO_MATCH
        if field is not None:
            fields[field.name] = result

    if offset < len(text):
        return NO_MATCH

    return DynamicNode(rule.name, fields)

def accepts(
    rule: MageRule,
    text: str,
    max_repeats: int = DEFAULT_MAX_REPEATS,
) -> Error:
    """
    Check whether the given expression accepts the given text.

    Returns `None` when the maximum recursion depth was reached. This usually means that the grammar has an infinite loop.

    This function might get optimised in the future.
    """
    result = evaluate(rule, text, max_repeats=max_repeats)
    return result if isinstance(result, Error) else SUCCESS
