
from collections.abc import Sequence
from io import StringIO

from magelang.util import IndentWriter
from .ast import *

def escape(ch: str) -> str:
    if ch.isprintable():
        return ch
    code = ord(ch)
    if code <= 0x7F:
        return f'\\x{code:02X}'
    return f'\\u{code:04x}'

def emit(node: MageSyntax) -> str:

    string = StringIO()
    out = IndentWriter(string)

    def is_wide(expr: MageExpr) -> bool:
        if isinstance(expr, MageSeqExpr):
            if len(expr.elements) == 0:
                return False
            if len(expr.elements) == 1:
                return is_wide(expr.elements[0])
            return True
        return False

    def visit_decorators(decorators: Sequence[Decorator]) -> None:
        for decorator in decorators:
            out.write('@')
            out.write(decorator.name)
            if decorator.args:
                out.write('{')
                out.write(', '.join(str(arg) for arg in decorator.args))
                out.write('}')
            out.write(' ')

    def visit(node: MageSyntax) -> None:

        if isinstance(node, MageGrammar):
            for rule in node.elements:
                visit(rule)
            return

        if isinstance(node, MageRule):
            for decorator in node.decorators:
                out.write('@')
                out.write(decorator.name)
                if decorator.args:
                    out.write('(')
                    first = True
                    for arg in decorator.args:
                        if first: first = False
                        else: out.write(', ')
                        out.write(str(arg))
                    out.write(')')
                out.write('\n')
            if node.mode != 0:
                out.write('@mode')
                out.write('(')
                out.write(str(node.mode))
                out.write(')\n')
            if node.is_public:
                out.write('pub ')
            if node.is_extern:
                out.write('extern ')
            if node.is_lex:
                out.write('token ')
            out.write(node.name)
            if node.type_name is not None:
                out.write(' -> ')
                out.write(node.type_name)
            if node.expr is not None:
                out.write(' = ')
                visit(node.expr)
            out.write('\n\n')
            return

        if isinstance(node, MageRefExpr):
            visit_decorators(node.decorators)
            out.write(node.name)
            return

        if isinstance(node, MageCharSetExpr):
            visit_decorators(node.decorators)
            out.write('[')
            for element in node.elements:
                if isinstance(element, str):
                    out.write(escape(element))
                else:
                    low, high = element
                    out.write(escape(low))
                    out.write('-')
                    out.write(escape(high))
            out.write(']')
            return

        if isinstance(node, MageLitExpr):
            visit_decorators(node.decorators)
            out.write(repr(node.text))
            return

        if isinstance(node, MageSeqExpr):
            visit_decorators(node.decorators)
            first = True
            for element in node.elements:
                if first: first = False
                else: out.write(' ')
                visit(element)
            return

        if isinstance(node, MageChoiceExpr):
            visit_decorators(node.decorators)
            out.write('(')
            first = True
            for element in node.elements:
                if first: first = False
                else: out.write(' | ')
                visit(element)
            out.write(')')
            return

        if isinstance(node, MageListExpr):
            visit_decorators(node.decorators)
            out.write('(')
            visit(node.element)
            out.write(' %')
            for _ in range(node.min_count):
                out.write('%')
            out.write(' ')
            visit(node.separator)
            out.write(')')
            return

        if isinstance(node, MageHideExpr):
            visit_decorators(node.decorators)
            out.write('\\')
            wide = is_wide(node)
            if wide:
                out.write('(')
            visit(node.expr)
            if wide:
                out.write(')')
            return

        if isinstance(node, MageLookaheadExpr):
            visit_decorators(node.decorators)
            out.write('!' if node.is_negated else '&')
            wide = is_wide(node)
            if wide:
                out.write('(')
            visit(node.expr)
            if wide:
                out.write(')')
            return

        if isinstance(node, MageRepeatExpr):
            visit_decorators(node.decorators)
            if node.min == 0 and node.max == 1:
                wide = is_wide(node.expr)
                if wide:
                    out.write('(')
                visit(node.expr)
                if wide:
                    out.write(')')
                out.write('?')
            elif node.min == 0 and node.max == MAGE_REPEAT_INFINITY:
                wide = is_wide(node.expr)
                if wide:
                    out.write('(')
                visit(node.expr)
                if wide:
                    out.write(')')
                out.write('*')
            elif node.min == 1 and node.max == MAGE_REPEAT_INFINITY:
                wide = is_wide(node.expr)
                if wide:
                    out.write('(')
                visit(node.expr)
                if wide:
                    out.write(')')
                out.write('+')
            else:
                wide = is_wide(node.expr)
                if is_wide: out.write('(')
                visit(node.expr)
                if is_wide: out.write(')')
                out.write('{')
                out.write(str(node.min))
                if node.max == node.min:
                    pass
                elif node.max == MAGE_REPEAT_INFINITY:
                    out.write(',')
                else:
                    out.write(',')
                    out.write(str(node.max))
                out.write('}')
            return

        raise RuntimeError(f'unexepected {node}')

    visit(node)

    return string.getvalue()

