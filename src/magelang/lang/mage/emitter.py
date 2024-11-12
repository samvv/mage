
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

def emit(node: MageNode) -> str:

    string = StringIO()
    out = IndentWriter(string)

    def is_wide(expr: MageExpr) -> bool:
        if isinstance(expr, MageSeqExpr):
            return len(expr.elements) > 1 or any(is_wide(element) for element in expr.elements)
        return False

    def visit(node: MageNode) -> None:

        if isinstance(node, MageGrammar):
            for rule in node.rules:
                visit(rule)
            return

        if isinstance(node, MageRule):
            if node.is_public:
                out.write('pub ')
            if node.is_extern:
                out.write('extern ')
            if node.is_token:
                out.write('token ')
            out.write(node.name)
            if node.type_name is not None:
                out.write(' -> ')
                out.write(node.type_name)
            if node.expr is not None:
                out.write(' = ')
                visit(node.expr)
            out.write('\n')
            return

        if isinstance(node, MageRefExpr):
            out.write(node.name)
            return

        if isinstance(node, MageCharSetExpr):
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
            out.write(repr(node.text))
            return

        if isinstance(node, MageSeqExpr):
            first = True
            for element in node.elements:
                if first: first = False
                else: out.write(' ')
                visit(element)
            return

        if isinstance(node, MageChoiceExpr):
            out.write('(')
            first = True
            for element in node.elements:
                if first: first = False
                else: out.write(' | ')
                visit(element)
            out.write(')')
            return

        if isinstance(node, MageListExpr):
            out.write('(')
            visit(node.element)
            out.write(' % ')
            visit(node.separator)
            out.write(')')
            return

        if isinstance(node, MageHideExpr):
            out.write('\\')
            wide = is_wide(node)
            if wide:
                out.write('(')
            visit(node.expr)
            if wide:
                out.write(')')
            return

        if isinstance(node, MageLookaheadExpr):
            out.write('!' if node.is_negated else '&')
            wide = is_wide(node)
            if wide:
                out.write('(')
            visit(node.expr)
            if wide:
                out.write(')')
            return

        if isinstance(node, MageRepeatExpr):
            if node.min == 0 and node.max == 1:
                wide = is_wide(node.expr)
                if wide:
                    out.write('(')
                visit(node.expr)
                if wide:
                    out.write(')')
                out.write('?')
            elif node.min == 0 and node.max == POSINF:
                wide = is_wide(node.expr)
                if wide:
                    out.write('(')
                visit(node.expr)
                if wide:
                    out.write(')')
                out.write('*')
            elif node.min == 1 and node.max == POSINF:
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
                elif node.max == POSINF:
                    out.write(',')
                else:
                    out.write(',')
                    out.write(str(node.max))
                out.write('}')
            return

        raise RuntimeError(f'unexepected {node}')

    visit(node)

    return string.getvalue()

