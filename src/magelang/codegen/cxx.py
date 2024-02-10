
import sys
from abc import abstractmethod
from typing import override
from sweetener import BaseNode, IndentWriter

from ..ast import *
from ..util import to_camel_case

def cxx_escape(ch: str) -> str:
    if ch.isprintable():
        return ch
    code = ord(ch)
    return f'\\{code:02X}' if code <= 0x7F else f'\\u{code:04X}'

class CXXNode(BaseNode):

    @abstractmethod
    def emit(self, out: IndentWriter) -> None:
        raise NotImplementedError()

    def print(self) -> None:
        out = IndentWriter(sys.stdout)
        self.emit(out)

class CXXTypeExpr(CXXNode):
    pass

class CXXRefTypeExpr(CXXTypeExpr):
    ns: list[str]
    name: str

    @override
    def emit(self, out):
        for el in self.ns:
            out.write(el)
            out.write('::')
        out.write(self.name)

class CXXExpr(CXXNode):
    pass

class CXXNewExpr(CXXExpr):
    name: str
    args: list[CXXExpr] | None = None

    def emit(self, out: IndentWriter) -> None:
        out.write('new ')
        out.write(self.name)
        first = False
        if self.args is not None:
            out.write('(')
            for arg in self.args:
                if not first:
                    out.write(', ')
                arg.emit(out)
                first = False
            out.write(')')

class CXXRefExpr(CXXExpr):
    ns: list[str]
    name: str

    @override
    def emit(self, out):
        for el in self.ns:
            out.write(el)
            out.write('::')
        out.write(self.name)

class CXXCallExpr(CXXExpr):
    op: CXXExpr
    args: list[CXXExpr]

    def emit(self, out):
        self.op.emit(out)
        out.write('(')
        first = True
        for arg in self.args:
            if not first:
                out.write(', ')
            arg.emit(out)
            first = False
        out.write(')')

class CXXIntExpr(CXXExpr):
    value: int

    def emit(self, out):
        out.write(str(self.value))

class CXXCharExpr(CXXExpr):
    ch: str

    def emit(self, out):
        out.write("'")
        out.write(cxx_escape(self.ch))
        out.write("'")

class CXXBinExpr(CXXExpr):
    left: CXXExpr
    op: str
    right: CXXExpr

    @override
    def emit(self, out):
        self.left.emit(out)
        out.write(' ')
        out.write(self.op)
        out.write(' ')
        self.right.emit(out)

class CXXBody(CXXNode):
    stmts: list['CXXStmt']

    def emit(self, out):
        out.write('{')
        if self.stmts:
            out.write('\n')
            out.indent()
            for stmt in self.stmts:
                stmt.emit(out)
            out.dedent()
        out.write('}')

class CXXParam(CXXNode):
    type: CXXTypeExpr
    name: str

    @override
    def emit(self, out):
        self.type.emit(out)
        out.write(' ')
        out.write(self.name)

class CXXInit(CXXNode):
    name: str
    expr: CXXExpr

    @override
    def emit(self, out):
        out.write(self.name)
        out.write('(')
        self.expr.emit(out)
        out.write(')')

class CXXConstructor(CXXNode):
    inline: bool = False
    name: str
    params: list[CXXParam]
    inits: list[CXXInit]
    body: CXXBody | None = None

    @override
    def emit(self, out):
        if self.inline:
            out.write('inline ')
        out.write(self.name)
        out.write('(')
        first = True
        for param in self.params:
            if not first:
                out.write(', ')
            param.emit(out)
            first = False
        out.write(')')
        first = True
        for init in self.inits:
            out.write(' : ' if first else ', ')
            init.emit(out)
            first = False
        if self.body is not None:
            out.write(' ')
            self.body.emit(out)
        else:
            out.write(';')
        out.write('\n')

class CXXStmt(CXXNode):
    pass

class CXXIfStmt(CXXStmt):
    test: CXXExpr
    then: list[CXXStmt]
    alt: list[CXXStmt] | None = None

    @override
    def emit(self, out):
        out.write('if (')
        self.test.emit(out)
        out.write(') {\n')
        out.indent()
        for stmt in self.then:
            stmt.emit(out)
        out.dedent()
        if self.alt is not None:
            out.write('} else [\n')
            for stmt in self.alt:
                stmt.emit(out)
        out.write('}\n')

class CXXRetStmt(CXXStmt):
    value: CXXExpr | None

    @override
    def emit(self, out):
        out.write('return ')
        if self.value is not None:
            self.value.emit(out)
        out.write(';\n')

class CXXDecl(CXXNode):
    pass

class CXXClassDecl(CXXDecl):
    name: str
    inherits: list[CXXExpr]
    elements: list[CXXNode] | None

    @override
    def emit(self, out):
        out.write(f'class {self.name}')
        first = True
        for e in self.inherits:
            out.write(' : ' if first else ', ')
            e.emit(out)
            first = False
        if self.elements is not None:
            out.write(' {')
            if self.elements:
                out.write('\n')
                out.indent()
                for element in self.elements:
                    element.emit(out)
                out.dedent()
            out.write('}')
        else:
            out.write(';')
        out.write('\n')

class CXXFuncDecl(CXXDecl):
    retty: CXXTypeExpr
    ns: list[str]
    name: str
    params: list[CXXParam]
    body: CXXBody | None

    @override
    def emit(self, out):
        self.retty.emit(out)
        out.write(' ')
        for name in self.ns:
            out.write(name)
            out.write('::')
        out.write(self.name)
        out.write('(')
        first = True
        for param in self.params:
            if not first:
                out.write(', ')
            param.emit(out)
            first = False
        out.write(')')
        if self.body is not None:
            out.write(' ')
            self.body.emit(out)

class CXXVarDecl(CXXDecl):
    ty: CXXTypeExpr
    name: str
    expr: CXXExpr

    def emit(self, out: IndentWriter) -> None:
        self.ty.emit(out)
        out.write(' ')
        out.write(self.name)
        out.write(' = ')
        self.expr.emit(out)
        out.write(';\n')

type CXXStmtOrDecl = CXXStmt | CXXDecl

class CXXSourceFile(CXXNode):
    elements: list[CXXDecl]

    @override
    def emit(self, out):
        for element in self.elements:
            element.emit(out)
            out.write('\n')

type CXXFiles = dict[str, CXXSourceFile]

def generate(grammar: Grammar) -> CXXFiles:
    files = dict()
    decls = []
    for rule in grammar.get_token_rules():
        cxx_name = to_camel_case(rule.name)
        decl_elements = []
        decl_elements.append(CXXConstructor(name=cxx_name, params=[], inits=[ CXXInit('Token', CXXRefExpr(ns=[ 'NodeKind' ], name=cxx_name)) ], body=CXXBody([])))
        decl = CXXClassDecl(name=cxx_name, inherits=[ CXXRefExpr(name='Token') ], elements=decl_elements)
        decls.append(decl)
    scan_stmts = []
    scan_decl = CXXFuncDecl(retty=CXXRefTypeExpr(name='Token'), ns=['Scanner'], name='scan', body=CXXBody(scan_stmts))
    def visit(expr: Expr, stmts: list[CXXStmtOrDecl], rule):
        if isinstance(expr, LitExpr):
            i = 0
            for ch in expr.text:
                char_name = 'c' + str(i)
                then_stmts = []
                stmts.append(CXXVarDecl(ty=CXXRefTypeExpr(name='auto'), name=char_name, expr=CXXCallExpr(op=CXXRefExpr(name='peekToken'), args=[ CXXIntExpr(i) ])))
                stmts.append(CXXIfStmt(test=CXXBinExpr(op='==', left=CXXRefExpr(name=char_name), right=CXXCharExpr(ch)), then=then_stmts))
                stmts = then_stmts
                i += 1
            return stmts
        if isinstance(expr, ChoiceExpr):
            raise NotImplementedError()
        if isinstance(expr, SeqExpr):
            for element in expr.elements:
                stmts = visit(element, stmts, rule)
            return stmts
        raise RuntimeError(f'unexpected node {expr}')
    for rule in grammar.get_token_rules():
        stmts = visit(rule.expr, scan_stmts, rule)
        stmts.append(CXXRetStmt(value=CXXNewExpr(name=to_camel_case(rule.name))))
    decls.append(scan_decl)
    files['CST.hpp'] = CXXSourceFile(decls)
    return files

