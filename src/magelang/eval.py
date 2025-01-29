
from typing import NewType, assert_never

from magelang.analysis import is_eof
from magelang.constants import DEFAULT_MAX_REPEATS
from magelang.helpers import get_field_name
from magelang.lang.mage.ast import *
from magelang.runtime import Punctuated
from magelang.util import NameGenerator

EOF = '\uFFFF'

Error = NewType('Error', int)

SUCCESS   = Error(0)
NO_MATCH  = Error(1)
RECMAX    = Error(2)

class DynamicNode:

    def __init__(self, name: str, fields: 'dict[str, DynamicNode | str]') -> None:
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

    def visit(expr: MageExpr) -> tuple | DynamicNode | str | None:

        nonlocal offset

        if is_eof(expr):
            if offset < len(text):
                return
            return ''

        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            assert(rule is not None)
            assert(rule.expr is not None)
            debug(f"enterig {expr.name}")
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
                for _ in range(0, max_repeats):
                    result = visit_backtrack(expr.expr)
                    if result is None:
                        break
                    elements.append(result)
                raise RecursionError()
            else:
                n = min(max_repeats, expr.max - expr.min)
                for _ in range(n):
                    result = visit_backtrack(expr.expr)
                    if result is None:
                        break
                    elements.append(result)
                if n == max_repeats:
                    raise RecursionError()
            return elements

        if isinstance(expr, MageLookaheadExpr):
            keep = offset
            result = visit(expr.expr)
            offset = keep
            if result != expr.is_negated:
                return ''
            return

        if isinstance(expr, MageListExpr):
            elements = Punctuated()
            count = 0
            prev_element = visit_backtrack(expr.element)
            if prev_element is not None:
                count += 1
                while True:
                    result = visit_backtrack(MageSeqExpr([
                        expr.separator,
                        expr.element,
                    ]))
                    if result is None:
                        break
                    elements.append(prev_element, result[0])
                    prev_element = result[1]
                elements.append_final(prev_element)
            if count < expr.min_count:
                return
            return elements

        if isinstance(expr, MageHideExpr):
            return visit(expr.expr)

        assert_never(expr)

    if rule.expr is None:
        return NO_MATCH

    generate_name = NameGenerator()
    fields = dict[str, DynamicNode]()
    for expr in flatten_sequence(rule.expr):
        name = get_field_name(expr) or generate_name('field')
        try:
            result = visit(expr)
        except RecursionError:
            return RECMAX
        if result is None:
            return NO_MATCH
        fields[name] = result

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
    return SUCCESS if isinstance(result, DynamicNode) else result
