
from io import StringIO
from typing import NewType, Sequence, assert_never
from magelang.util import IndentWriter

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
    names = []
    if isinstance(op, tuple):
        for element in op:
            names.append(emit_token(element))
    else:
        names.append(emit_token(op))
    text = ' '.join(names)
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

    if isinstance(node, PyRArrow):
        return '->'

    if isinstance(node, PyComma):
        return ','

    if isinstance(node, PyAsterisk):
        return '*'

    if isinstance(node, PyDot):
        return '.'

    if isinstance(node, PyDotDotDot):
        return '...'

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

    if isinstance(node, PyFromKeyword):
        return 'from'

    if isinstance(node, PyImportKeyword):
        return 'import'

    if isinstance(node, PyHashtag):
        return '#'

    if isinstance(node, PyVerticalBar):
        return '|'

    if isinstance(node, PyTilde):
        return '~'

    if isinstance(node, PyTypeKeyword):
        return 'type'

    if isinstance(node, PyOrKeyword):
        return 'or'

    if isinstance(node, PyAndKeyword):
        return 'and'

    if isinstance(node, PyNotKeyword):
        return 'not'

    if isinstance(node, PyIsKeyword):
        return 'is'

    if isinstance(node, PyDelKeyword):
        return 'del'

    if isinstance(node, PyCaret):
        return '^'

    if isinstance(node, PyAsKeyword):
        return 'as'

    if isinstance(node, PyAtSign):
        return '@'

    if isinstance(node, PyGreaterThan):
        return '>'

    if isinstance(node, PyGreaterThanEquals):
        return '>='

    if isinstance(node, PyLessThan):
        return '<'

    if isinstance(node, PyLessThanEquals):
        return '<='

    if isinstance(node, PyGreaterThan):
        return '>'

    if isinstance(node, PyLessThanLessThan):
        return '<<'

    if isinstance(node, PyGreaterThanGreaterThan):
        return '>>'

    if isinstance(node, PyEqualsEquals):
        return '=='

    if isinstance(node, PySemicolon):
        return ';'

    if isinstance(node, PyNonlocalKeyword):
        return 'nonlocal'

    if isinstance(node, PyGlobalKeyword):
        return 'global'

    if isinstance(node, PySlash):
        return '/'

    if isinstance(node, PyPlus):
        return '+'

    if isinstance(node, PyHyphen):
        return '-'

    if isinstance(node, PyExclamationMarkEquals):
        return '!='

    if isinstance(node, PyAmpersand):
        return '&'

    if isinstance(node, PyPercent):
        return '%'

    if isinstance(node, PySlash):
        return '/'

    if isinstance(node, PyAsteriskAsterisk):
        return '**'

    assert_never(node)

def emit(node: PyNode) -> str:

    string = StringIO()
    out = IndentWriter(string, indentation='    ')

    def visit_body(body: 'PyStmt | Sequence[PyStmt]', newline = '\n') -> None:
        if is_py_stmt(body):
            out.write(' ')
            visit(body)
        else:
            assert(isinstance(body, list))
            out.indent()
            for stmt in body:
                out.write(newline)
                visit(stmt)
            out.dedent()

    def visit_infix_op(op: PyInfixOp):
        if isinstance(op, tuple):
            out.write(' '.join(emit_token(element) for element in op))
            return
        visit_token(op)

    def visit_expr(node: PyExpr, info: tuple[int, _Assoc] | None = None) -> None:

        if isinstance(node, PyNamedExpr):
            visit_token(node.name)
            return

        if isinstance(node, PyEllipsisExpr):
            visit_token(node.dot_dot_dot)
            return

        if isinstance(node, PyInfixExpr):
            new_prec, new_assoc = _describe_infix_operator(node.op)
            should_nest = info is not None and (new_prec < info[0] or (new_prec == info[0] and new_assoc != info[1]))
            if should_nest:
                out.write('(')
            visit_expr(node.left, (new_prec, new_assoc))
            out.write(' ')
            visit_infix_op(node.op)
            out.write(' ')
            visit_expr(node.right, (new_prec, new_assoc))
            if should_nest:
                out.write(')')
            return

        if isinstance(node, PyIfExpr):
            visit_expr(node.then)
            out.write(' ')
            visit_token(node.if_keyword)
            out.write(' ')
            visit_expr(node.test)
            out.write(' ')
            visit_token(node.else_keyword)
            out.write(' ')
            visit_expr(node.alt)
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
            out.write(' ')
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

    prev_token = None

    def write_whitespace() -> None:
        out.write(' ')

    def visit_token(node: PyToken) -> None:
        nonlocal prev_token
        # if (is_py_keyword(prev_token) or isinstance(prev_token, PyIdent)) and (is_py_keyword(node) or isinstance(node, PyIdent)):
        #     write_whitespace()
        prev_token = node
        out.write(emit_token(node))
        if isinstance(node, PyComma):
            out.write(' ')

    def visit_base_arg(node: PyBaseArg) -> None:
        if isinstance(node, PyKeywordBaseArg):
            visit_token(node.name)
            visit_token(node.equals)
            visit_expr(node.expr)
            return
        if isinstance(node, PyClassBaseArg):
            visit_token(node.name)
            return
        assert_never(node)

    def visit_stmt(node: PyStmt) -> None:

        if isinstance(node, PyGlobalStmt):
            visit_token(node.global_keyword)
            out.write(' ')
            for name, comma in node.names:
                visit_token(name)
                if comma is not None:
                    visit_token(comma)
            return

        if isinstance(node, PyNonlocalStmt):
            visit_token(node.nonlocal_keyword)
            out.write(' ')
            for name, comma in node.names:
                visit_token(name)
                if comma is not None:
                    visit_token(comma)
            return

        if isinstance(node, PyBreakStmt):
            visit_token(node.break_keyword)
            return

        if isinstance(node, PyContinueStmt):
            visit_token(node.continue_keyword)
            return

        if isinstance(node, PyRaiseStmt):
            visit_token(node.raise_keyword)
            out.write(' ')
            visit_expr(node.expr)
            return

        if isinstance(node, PyExprStmt):
            visit_expr(node.expr)
            return

        if isinstance(node, PyRetStmt):
            visit_token(node.return_keyword)
            if node.expr is not None:
                out.write(' ')
                visit_expr(node.expr)
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
            return

        if isinstance(node, PyWhileStmt):
            visit_token(node.while_keyword)
            out.write(' ')
            visit_expr(node.expr)
            visit_token(node.colon)
            visit_body(node.body)
            if node.else_clause is not None:
                out.write('\n')
                else_keyword, colon, body = node.else_clause
                visit_token(else_keyword)
                visit_token(colon)
                visit_body(body)
            return

        if isinstance(node, PyTryStmt):
            visit_token(node.try_keyword)
            visit_token(node.colon)
            visit_body(node.body)
            for handler in node.handlers:
                out.write('\n')
                visit_token(handler.except_keyword)
                out.write(' ')
                visit_expr(handler.expr)
                visit_token(handler.colon)
                visit_body(handler.body)
            if node.else_clause is not None:
                out.write('\n')
                else_keyword, colon, body = node.else_clause
                visit_token(else_keyword)
                visit_token(colon)
                visit_body(body)
            if node.finally_clause is not None:
                out.write('\n')
                finally_keyword, colon, body = node.finally_clause
                visit_token(finally_keyword)
                visit_token(colon)
                visit_body(body)
            return

        if isinstance(node, PyIfStmt):
            visit(node.first)
            for alt in node.alternatives:
                out.write('\n')
                visit(alt)
            if node.last is not None:
                out.write('\n')
                visit(node.last)
            return

        if isinstance(node, PyAssignStmt):
            visit_pattern(node.pattern)
            if node.annotation is not None:
                colon, expr = node.annotation
                visit_token(colon)
                out.write(' ')
                visit_expr(expr)
            if node.value is not None:
                out.write(' ')
                equals, expr = node.value
                visit_token(equals)
                out.write(' ')
                visit_expr(expr)
            return

        if isinstance(node, PyAugAssignStmt):
            visit_pattern(node.pattern)
            if node.annotation is not None:
                colon, expr = node.annotation
                visit_token(colon)
                out.write(' ')
                visit_expr(expr)
            out.write(' ')
            visit_token(node.op)
            visit_token(node.equals)
            out.write(' ')
            visit_expr(node.expr)
            return

        if isinstance(node, PyPassStmt):
            visit_token(node.pass_keyword)
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
            return

        if isinstance(node, PyFuncDef):
            for decorator in node.decorators:
                visit_token(decorator.at_sign)
                visit_expr(decorator.expr)
                out.write('\n')
            if node.async_keyword is not None:
                visit_token(node.async_keyword)
            visit_token(node.def_keyword)
            out.write(' ')
            visit_token(node.name)
            visit_token(node.open_paren)
            for param, comma in node.params:
                visit_param(param)
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

        if isinstance(node, PyTypeAliasStmt):
            visit_token(node.type_keyword)
            out.write(' ')
            visit_token(node.name)
            if node.type_params is not None:
                open, params, close = node.type_params
                visit_token(open)
                for param, comma in params:
                    visit_expr(param)
                    if comma is not None:
                        visit_token(comma)
                visit_token(close)
            out.write(' ')
            visit_token(node.equals)
            out.write(' ')
            visit_expr(node.expr)
            return

        if isinstance(node, PyClassDef):
            visit_token(node.class_keyword)
            out.write(' ')
            visit_token(node.name)
            if node.bases is not None:
                open_paren, elements, close_paren = node.bases
                visit_token(open_paren)
                for arg, comma in elements:
                    visit_base_arg(arg)
                    if comma is not None:
                        visit_token(comma)
                visit_token(close_paren)
            visit_token(node.colon)
            visit_body(node.body, newline='\n\n')
            return

        if isinstance(node, PyImportFromStmt):
            visit_token(node.from_keyword)
            out.write(' ')
            visit(node.path)
            out.write(' ')
            visit_token(node.import_keyword)
            out.write(' ')
            for alias, comma in node.aliases:
                visit(alias)
                if comma is not None:
                    visit_token(comma)
            return

        if isinstance(node, PyImportStmt):
            visit_token(node.import_keyword)
            out.write(' ')
            for alias, comma in node.aliases:
                visit(alias)
                if comma is not None:
                    visit_token(comma)
            return

        if isinstance(node, PyDeleteStmt):
            visit_token(node.del_keyword)
            visit_pattern(node.pattern)
            return

        assert_never(node)

    def visit_param(node: PyParam) -> None:

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

        if isinstance(node, PyRestKeywordParam):
            visit_token(node.asterisk_asterisk)
            if node.name is not None:
                visit_token(node.name)
            if node.annotation is not None:
                visit_token(node.annotation[0])
                out.write(' ')
                visit_expr(node.annotation[1])
            return

        if isinstance(node, PyRestPosParam):
            visit_token(node.asterisk)
            if node.name is not None:
                visit_token(node.name)
            if node.annotation is not None:
                visit_token(node.annotation[0])
                out.write(' ')
                visit_expr(node.annotation[1])
            return

        if isinstance(node, PyKwSepParam):
            visit_token(node.asterisk)
            return

        if isinstance(node, PyPosSepParam):
            visit_token(node.slash)
            return

        assert_never(node)


    def visit(node: PyNode) -> None:

        if is_py_pattern(node):
            visit_pattern(node)
            return

        if is_py_expr(node):
            visit_expr(node)
            return

        if is_py_stmt(node):
            visit_stmt(node)
            return

        if isinstance(node, PyPosSepParam):
            visit_token(node.slash)
            return

        if isinstance(node, PyKwSepParam):
            visit_token(node.asterisk)
            return

        if isinstance(node, PyPatternSlice):
            if node.lower is not None:
                visit_pattern(node.lower)
            visit_token(node.colon)
            if node.upper is not None:
                visit_pattern(node.upper)
            if node.step is not None:
                colon, expr = node.step
                visit_token(colon)
                visit_pattern(expr)
            return

        if isinstance(node, PyExprSlice):
            if node.lower is not None:
                visit_expr(node.lower)
            visit_token(node.colon)
            if node.upper is not None:
                visit_expr(node.upper)
            if node.step is not None:
                colon, expr = node.step
                visit_token(colon)
                visit_expr(expr)
            return

        if isinstance(node, PyQualName):
            for name, dot in node.modules:
                visit_token(name)
                assert(dot is not None)
                visit_token(dot)
            visit_token(node.name)
            return

        if isinstance(node, PyRelativePath):
            for dot in node.dots:
                visit_token(dot)
            if node.name is not None:
                visit(node.name)
            # for name, dot in node.modules:
            #     visit_token(name)
            #     visit_token(dot)
            # if node.name is not None:
            #     visit_token(node.name)
            return

        if isinstance(node, PyAbsolutePath):
            visit(node.name)
            return
            # for name, dot in node.modules:
            #     visit_token(name)
            #     visit_token(dot)
            # if node.name is not None:
            #     visit_token(node.name)
            # return

        if isinstance(node, PyAlias):
            visit(node.path)
            if node.asname is not None:
                as_kw, name = node.asname
                out.write(' ')
                visit_token(as_kw)
                out.write(' ')
                visit_token(name)
            return

        if isinstance(node, PyFromAlias):
            visit_token(node.name)
            if node.asname is not None:
                as_kw, name = node.asname
                out.write(' ')
                visit_token(as_kw)
                out.write(' ')
                visit_token(name)
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

        if isinstance(node, PyModule):
            for stmt in node.stmts:
                visit(stmt)
                out.write('\n\n\n')
            return

        panic(f"Unexpected {node}")

    visit(node)

    return string.getvalue()

