
from io import StringIO
from typing import NewType, assert_never
from sweetener import IndentWriter, warn

from .cst import *

_Assoc = NewType('_Assoc', int)

_RIGHT = _Assoc(1)
_LEFT = _Assoc(2)

_infix_operator_table = {
    '**': (4, _RIGHT),
    '*': (5, _LEFT),
    '@': (5, _LEFT),
    '/': (5, _LEFT),
    '//': (5, _LEFT),
    '%': (5, _LEFT),
    '+': (6, _LEFT),
    '-': (6, _LEFT),
    '<<': (7, _LEFT),
    '>>': (7, _LEFT),
    '&': (8, _LEFT),
    '^': (9, _LEFT),
    '|': (10, _LEFT),
    'in': (11, _LEFT),
    'not in': (11, _LEFT),
    'is': (11, _LEFT),
    'is not': (11, _LEFT),
    '<': (11, _LEFT),
    '<=': (11, _LEFT),
    '>': (11, _LEFT),
    '>=': (11, _LEFT),
    '!=': (11, _LEFT),
    '==': (11, _LEFT),
    'and': (12, _LEFT),
    'or': (13, _LEFT),
    ':=': (14, _RIGHT),
}

def _describe_infix_operator(op: PyInfixOp) -> tuple[int, _Assoc]:
    text = emit_token(op)
    return _infix_operator_table[text]

def emit_token(node: PyToken) -> str:

    if isinstance(node, PyIdent):
        return node.value

    if isinstance(node, PyString):
        return repr(node.value)

    if isinstance(node, PyInteger):
        return str(node.value)

    if isinstance(node, PyFloat):
        return str(node.value)

    if isinstance(node, PyOpenBracket):
        return '['

    if isinstance(node, PyCloseBracket):
        return ']'

    if isinstance(node, PyOpenParen):
        return '('

    if isinstance(node, PyCloseParen):
        return ')'

    if isinstance(node, PyColon):
        return ':'

    if isinstance(node, PyHyphenGreaterThan):
        return '->'

    if isinstance(node, PyComma):
        return ','

    if isinstance(node, PyAsterisk):
        return '*'

    if isinstance(node, PyDot):
        return '.'

    if isinstance(node, PyEquals):
        return '='

    if isinstance(node, PyBreakKeyword):
        return 'break'

    if isinstance(node, PyContinueKeyword):
        return 'continue'

    if isinstance(node, PyIfKeyword):
        return 'if'

    if isinstance(node, PyElifKeyword):
        return 'elif'

    if isinstance(node, PyElseKeyword):
        return 'else'

    if isinstance(node, PyWhileKeyword):
        return 'while'

    if isinstance(node, PyDefKeyword):
        return 'def'

    if isinstance(node, PyTryKeyword):
        return 'try'

    if isinstance(node, PyAsyncKeyword):
        return 'async'

    if isinstance(node, PyClassKeyword):
        return 'class'

    if isinstance(node, PyReturnKeyword):
        return 'return'

    if isinstance(node, PyFinallyKeyword):
        return 'finally'

    if isinstance(node, PyPassKeyword):
        return 'pass'

    if isinstance(node, PyForKeyword):
        return 'for'

    if isinstance(node, PyInKeyword):
        return 'in'

    if isinstance(node, PyExceptKeyword):
        return 'except'

    if isinstance(node, PyRaiseKeyword):
        return 'raise'

    if isinstance(node, PyHashtag):
        return '#'

    if isinstance(node, PyPrefixOp):
        return node.value

    if isinstance(node, PyInfixOp):
        return node.value

    assert_never(node)

def emit(node: PyNode) -> str:

    string = StringIO()
    out = IndentWriter(string, indentation='    ')

    def visit_body(body: 'PyStmt | list[PyStmt]') -> None:
        if is_py_stmt(body):
            out.write(' ')
            visit(body)
        else:
            assert(isinstance(body, list))
            out.write('\n')
            out.indent()
            for stmt in body:
                visit(stmt)
            out.dedent()

    def visit_expr(node: PyExpr, info: tuple[int, _Assoc] | None = None) -> None:

        if isinstance(node, PyNamedExpr):
            visit_token(node.name)
            return

        if isinstance(node, PyInfixExpr):
            new_prec, new_assoc = _describe_infix_operator(node.op)
            should_nest = info is not None and (new_prec < info[0] or (new_prec == info[0] and new_assoc != info[1]))
            if should_nest:
                out.write('(')
            visit_expr(node.left, (new_prec, new_assoc))
            out.write(' ')
            visit_token(node.op)
            out.write(' ')
            visit_expr(node.right, (new_prec, new_assoc))
            if should_nest:
                out.write(')')
            return

        if isinstance(node, PyNestExpr):
            visit_token(node.open_paren)
            visit_expr(node.expr)
            visit_token(node.close_paren)
            return

        if isinstance(node, PyCallExpr):
            visit_expr(node.operator, info)
            visit_token(node.open_paren)
            for arg, comma in node.args:
                if isinstance(arg, PyKeywordArg):
                    visit_token(arg.name)
                    visit_token(arg.equals)
                    visit_expr(arg.expr)
                else:
                    visit_expr(arg)
                if comma is not None:
                    visit_token(comma)
            visit_token(node.close_paren)
            return

        if isinstance(node, PySubscriptExpr):
            visit_expr(node.expr, info)
            visit_token(node.open_bracket)
            for s, comma in node.slices:
                visit(s)
                if comma is not None:
                    visit_token(comma)
            visit_token(node.close_bracket)
            return

        if isinstance(node, PyListExpr):
            visit_token(node.open_bracket)
            for element in node.elements:
                expr, comma = element
                visit_expr(expr)
                if comma is not None:
                    visit_token(comma)
            visit_token(node.close_bracket)
            return

        if isinstance(node, PyConstExpr):
            visit_token(node.literal)
            return

        if isinstance(node, PyTupleExpr):
            visit_token(node.open_paren)
            for element, comma in node.elements:
                visit_expr(element)
                if comma is not None:
                    visit_token(comma)
            visit_token(node.close_paren)
            return

        if isinstance(node, PyAttrExpr):
            visit_expr(node.expr, info)
            visit_token(node.dot)
            visit_token(node.name)
            return

        if isinstance(node, PyPrefixExpr):
            visit_token(node.prefix_op)
            visit_expr(node.expr, info)
            return

        if isinstance(node, PyStarredExpr):
            visit_token(node.asterisk)
            visit_expr(node.expr, info)
            return

        assert_never(node)

    def visit_pattern(node: PyPattern) -> None:

        if isinstance(node, PyNamedPattern):
            visit_token(node.name)
            return

        if isinstance(node, PyAttrPattern):
            visit_pattern(node.pattern)
            visit_token(node.dot)
            visit_token(node.name)
            return

        if isinstance(node, PyTuplePattern):
            visit_token(node.open_paren)
            for element, comma in node.elements:
                visit_pattern(element)
                if comma is not None:
                    visit_token(comma)
            visit_token(node.close_paren)
            return

        assert_never(node)

    def visit_token(node: PyToken) -> None:
        out.write(emit_token(node))
        if isinstance(node, PyComma):
            out.write(' ')

    def visit(node: PyNode) -> None:

        if is_py_pattern(node):
            visit_pattern(node)
            return

        if is_py_expr(node):
            visit_expr(node)
            return

        if isinstance(node, PyInfixOp):
            out.write(node.value)
            return

        if isinstance(node, PyNamedParam):
            visit_pattern(node.pattern)
            if node.annotation is not None:
                colon, expr = node.annotation
                visit_token(colon)
                out.write(' ')
                visit_expr(expr)
            if node.default is not None:
                equals, expr = node.default
                out.write(' ')
                visit_token(equals)
                out.write(' ')
                visit_expr(expr)
            return

        if isinstance(node, PySepParam):
            visit_token(node.asterisk)
            return

        if isinstance(node, PySlice):
            visit_expr(node.lower)
            visit_token(node.colon)
            visit_expr(node.upper)
            return

        if isinstance(node, PyBreakStmt):
            visit_token(node.break_keyword)
            out.write('\n')
            return

        if isinstance(node, PyContinueStmt):
            visit_token(node.continue_keyword)
            out.write('\n')
            return

        if isinstance(node, PyRaiseStmt):
            visit_token(node.raise_keyword)
            out.write(' ')
            visit_expr(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyExprStmt):
            visit_expr(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyRetStmt):
            visit_token(node.return_keyword)
            if node.expr is not None:
                out.write(' ')
                visit_expr(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyIfCase):
            visit_token(node.if_keyword)
            out.write(' ')
            visit_expr(node.test)
            visit_token(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyElifCase):
            visit_token(node.elif_keyword)
            out.write(' ')
            visit_expr(node.test)
            visit_token(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyElseCase):
            visit_token(node.else_keyword)
            visit_token(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyForStmt):
            visit_token(node.for_keyword)
            out.write(' ')
            visit_pattern(node.pattern)
            out.write(' ')
            visit_token(node.in_keyword)
            out.write(' ')
            visit_expr(node.expr)
            visit_token(node.colon)
            visit_body(node.body)
            out.write('\n')
            return

        if isinstance(node, PyWhileStmt):
            visit_token(node.while_keyword)
            out.write(' ')
            visit_expr(node.expr)
            visit_token(node.colon)
            visit_body(node.body)
            if node.else_clause is not None:
                else_keyword, colon, body = node.else_clause
                visit_token(else_keyword)
                visit_token(colon)
                visit_body(body)
            out.write('\n')
            return

        if isinstance(node, PyTryStmt):
            visit_token(node.try_keyword)
            visit_token(node.colon)
            visit_body(node.body)
            for handler in node.handlers:
                visit_token(handler.except_keyword)
                out.write(' ')
                visit_expr(handler.expr)
                visit_token(handler.colon)
                visit_body(handler.body)
            if node.else_clause is not None:
                else_keyword, colon, body = node.else_clause
                visit_token(else_keyword)
                visit_token(colon)
                visit_body(body)
            if node.finally_clause is not None:
                finally_keyword, colon, body = node.finally_clause
                visit_token(finally_keyword)
                visit_token(colon)
                visit_body(body)
            return

        if isinstance(node, PyIfStmt):
            visit(node.first)
            for alt in node.alternatives:
                visit(alt)
            if node.last is not None:
                visit(node.last)
            return

        if isinstance(node, PyAssignStmt):
            visit_pattern(node.pattern)
            if node.annotation is not None:
                colon, expr = node.annotation
                visit_token(colon)
                out.write(' ')
                visit_expr(expr)
            out.write(' ')
            visit_token(node.equals)
            out.write(' ')
            visit_expr(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyPassStmt):
            visit_token(node.pass_keyword)
            out.write('\n')
            return

        if isinstance(node, PyRaiseStmt):
            visit_token(node.raise_keyword)
            out.write(' ')
            visit_expr(node.expr)
            if node.cause is not None:
                from_keyword, expr = node.cause
                out.write(' ')
                visit_token(from_keyword)
                out.write(' ')
                visit_expr(expr)
            out.write('\n')
            return

        if isinstance(node, PyFuncDef):
            if node.async_keyword is not None:
                visit_token(node.async_keyword)
            visit_token(node.def_keyword)
            out.write(' ')
            visit_token(node.name)
            visit_token(node.open_paren)
            for param, comma in node.params:
                visit(param)
                if comma is not None:
                    visit_token(comma)
            visit_token(node.close_paren)
            if node.return_type is not None:
                rarrow, expr = node.return_type
                out.write(' ')
                visit_token(rarrow)
                out.write(' ')
                visit_expr(expr)
            visit_token(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyClassDef):
            visit_token(node.class_keyword)
            out.write(' ')
            visit_token(node.name)
            if node.bases:
                open_paren, elements, close_paren = node.bases
                visit_token(open_paren)
                for name, comma in elements:
                    visit_token(name)
                    if comma is not None:
                        visit_token(comma)
                visit_token(close_paren)
            visit_token(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyModule):
            for stmt in node.stmts:
                visit(stmt)
                out.write('\n\n')
            return

        assert_never(node)

    visit(node)

    return string.getvalue()

