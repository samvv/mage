
from io import StringIO
from sweetener import IndentWriter

from .cst import *

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

    def visit(node: PySyntax) -> None:

        if isinstance(node, PyIdent):
            if node.value is not None:
                out.write(node.value)
                return
            if node.span is not None:
                raise NotImplementedError()
            raise RuntimeError(f'PyIdent does not contain any value')

        if isinstance(node, PyString):
            if node.value is not None:
                out.write(repr(node.value))
                return
            if node.span is not None:
                raise NotImplementedError()
            raise RuntimeError(f'PyString does not contain any value')

        if isinstance(node, PyInteger):
            if node.value is not None:
                out.write(str(node.value))
                return
            if node.span is not None:
                raise NotImplementedError()
            raise RuntimeError(f'PyInteger does not contain any value')

        if isinstance(node, PyOpenBracket):
            out.write('[')
            return

        if isinstance(node, PyCloseBracket):
            out.write(']')
            return

        if isinstance(node, PyOpenParen):
            out.write('(')
            return

        if isinstance(node, PyCloseParen):
            out.write(')')
            return

        if isinstance(node, PyColon):
            out.write(':')
            return

        if isinstance(node, PyHyphenGreaterThan):
            out.write('->')
            return

        if isinstance(node, PyComma):
            out.write(',')
            return

        if isinstance(node, PyAsterisk):
            out.write('*')
            return

        if isinstance(node, PyDot):
            out.write('.')
            return

        if isinstance(node, PyEquals):
            out.write('=')
            return

        if isinstance(node, PyIfKeyword):
            out.write('if')
            return

        if isinstance(node, PyElifKeyword):
            out.write('elif')
            return

        if isinstance(node, PyElseKeyword):
            out.write('else')
            return

        if isinstance(node, PyWhileKeyword):
            out.write('while')
            return

        if isinstance(node, PyDefKeyword):
            out.write('def')
            return

        if isinstance(node, PyTryKeyword):
            out.write('try')
            return

        if isinstance(node, PyAsyncKeyword):
            out.write('async')
            return

        if isinstance(node, PyClassKeyword):
            out.write('class')
            return

        if isinstance(node, PyReturnKeyword):
            out.write('return')
            return

        if isinstance(node, PyPassKeyword):
            out.write('pass')
            return

        if isinstance(node, PyForKeyword):
            out.write('for')
            return

        if isinstance(node, PyInKeyword):
            out.write('in')
            return

        if isinstance(node, PyExceptKeyword):
            out.write('except')
            return

        if isinstance(node, PyRaiseKeyword):
            out.write('raise')
            return

        if isinstance(node, PyInfixOp):
            if node.value is not None:
                out.write(node.value)
                return
            if node.span is not None:
                raise NotImplementedError()
            raise RuntimeError(f'PyIdent does not contain any value')

        if isinstance(node, PyNamedExpr):
            visit(node.name)
            return

        if isinstance(node, PyListExpr):
            visit(node.open_bracket)
            for element in node.elements:
                expr, comma = element
                visit(expr)
                if comma is not None:
                    visit(comma)
                    out.write(' ')
            visit(node.close_bracket)
            return

        if isinstance(node, PyConstExpr):
            visit(node.literal)
            return

        if isinstance(node, PyTupleExpr):
            visit(node.open_paren)
            for element, comma in node.elements:
                visit(element)
                if comma is not None:
                    visit(comma)
                    out.write(' ')
            visit(node.close_paren)
            return

        if isinstance(node, PyAttrExpr):
            visit(node.expr)
            visit(node.dot)
            visit(node.name)
            return

        if isinstance(node, PyKeywordArg):
            visit(node.name)
            visit(node.equals)
            visit(node.expr)
            return

        if isinstance(node, PyNestExpr):
            out.write('(')
            visit(node.expr)
            out.write(')')
            return

        if isinstance(node, PyPosArg):
            visit(node.expr)
            return

        if isinstance(node, PyCallExpr):
            visit(node.operator)
            visit(node.open_paren)
            for arg, comma in node.args:
                visit(arg)
                if comma is not None:
                    visit(comma)
                    out.write(' ')
            visit(node.close_paren)
            return

        if isinstance(node, PySubscriptExpr):
            visit(node.expr)
            visit(node.open_bracket)
            for s, comma in node.slices:
                visit(s)
                if comma is not None:
                    visit(comma)
            visit(node.close_bracket)
            return

        if isinstance(node, PyNamedPattern):
            visit(node.name)
            return

        if isinstance(node, PyAttrPattern):
            visit(node.pattern)
            visit(node.dot)
            visit(node.name)
            return

        if isinstance(node, PyTuplePattern):
            out.write('(')
            for element, comma in node.elements:
                visit(element)
                if comma is not None:
                    visit(comma)
            out.write(')')
            return

        if isinstance(node, PyNamedParam):
            visit(node.pattern)
            if node.annotation is not None:
                colon, expr = node.annotation
                visit(colon)
                out.write(' ')
                visit(expr)
            if node.default is not None:
                equals, expr = node.default
                out.write(' ')
                visit(equals)
                out.write(' ')
                visit(expr)
            return

        if isinstance(node, PySepParam):
            visit(node.asterisk)
            return

        if isinstance(node, PyInfixExpr):
            visit(node.left)
            out.write(' ')
            visit(node.op)
            out.write(' ')
            visit(node.right)
            return

        if isinstance(node, PyBreakStmt):
            out.write('break')
            out.write('\n')
            return

        if isinstance(node, PyRaiseStmt):
            out.write('raise ');
            visit(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyExprStmt):
            visit(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyRetStmt):
            visit(node.return_keyword)
            if node.expr is not None:
                out.write(' ')
                visit(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyIfCase):
            visit(node.if_keyword)
            out.write(' ')
            visit(node.test)
            visit(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyElifCase):
            visit(node.elif_keyword)
            out.write(' ')
            visit(node.test)
            visit(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyElseCase):
            visit(node.else_keyword)
            visit(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyForStmt):
            visit(node.for_keyword)
            out.write(' ')
            visit(node.pattern)
            out.write(' ')
            visit(node.in_keyword)
            out.write(' ')
            visit(node.expr)
            visit(node.colon)
            visit_body(node.body)
            out.write('\n')
            return

        if isinstance(node, PyWhileStmt):
            visit(node.while_keyword)
            out.write(' ')
            visit(node.expr)
            visit(node.colon)
            visit_body(node.body)
            if node.else_clause is not None:
                else_keyword, colon, body = node.else_clause
                visit(else_keyword)
                visit(colon)
                visit_body(body)
            out.write('\n')
            return

        if isinstance(node, PyTryStmt):
            visit(node.try_keyword)
            visit(node.colon)
            visit_body(node.body)
            for handler in node.handlers:
                visit(handler.except_keyword)
                out.write(' ')
                visit(handler.expr)
                # visit(handler.colon)
                out.write(':') # FIXME
                visit_body(handler.body)
            if node.else_clause is not None:
                else_keyword, colon, body = node.else_clause
                visit(else_keyword)
                visit(colon)
                visit_body(body)
            if node.finally_clause is not None:
                finally_keyword, colon, body = node.finally_clause
                visit(finally_keyword)
                visit(colon)
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
            visit(node.pattern)
            if node.annotation is not None:
                colon, expr = node.annotation
                visit(colon)
                out.write(' ')
                visit(expr)
            out.write(' ')
            visit(node.equals)
            out.write(' ')
            visit(node.expr)
            out.write('\n')
            return

        if isinstance(node, PyPassStmt):
            visit(node.pass_keyword)
            out.write('\n')
            return

        if isinstance(node, PyRaiseStmt):
            visit(node.raise_keyword)
            out.write(' ')
            visit(node.expr)
            if node.cause is not None:
                from_keyword, expr = node.cause
                out.write(' ')
                visit(from_keyword)
                out.write(' ')
                visit(expr)
            out.write('\n')
            return

        if isinstance(node, PyFuncDef):
            if node.async_keyword is not None:
                visit(node.async_keyword)
            visit(node.def_keyword)
            out.write(' ')
            visit(node.name)
            visit(node.open_paren)
            for param, comma in node.params:
                visit(param)
                if comma is not None:
                    visit(comma)
                    out.write(' ')
            visit(node.close_paren)
            if node.return_type is not None:
                rarrow, expr = node.return_type
                out.write(' ')
                visit(rarrow)
                out.write(' ')
                visit(expr)
            visit(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyClassDef):
            visit(node.class_keyword)
            out.write(' ')
            visit(node.name)
            if node.bases:
                open_paren, elements, close_paren = node.bases
                visit(open_paren)
                for name, comma in elements:
                    visit(name)
                    if comma is not None:
                        visit(comma)
                        out.write(' ')
                visit(close_paren)
            visit(node.colon)
            visit_body(node.body)
            return

        if isinstance(node, PyModule):
            for stmt in node.stmts:
                visit(stmt)
                out.write('\n\n')
            return

        raise RuntimeError(f'unexpected {node}')

    visit(node)

    return string.getvalue()

