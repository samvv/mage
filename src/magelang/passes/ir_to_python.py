
from collections.abc import Iterator
from typing import Generator, assert_never
from magelang.logging import warn
from magelang.util import is_iterator, to_camel_case, unreachable
from magelang.ir.ast import *
from magelang.ir.constants import *
from magelang.lang.python.cst import *

def _make_infix(it: Iterator[PyExpr], op: PyInfixOp, init: PyExpr) -> PyExpr:
    if not is_iterator(it):
        it = iter(it)
    try:
        out = next(it)
    except StopIteration:
        return init
    for expr in it:
        out = PyInfixExpr(left=out, op=op, right=expr)
    return out

def ir_to_python(node: Program) -> PyModule:

    imports = set[str]()

    def to_type_name(name: str) -> str:
        return to_camel_case(name)

    def to_var_name(name: str) -> str:
        return name

    def add_import(module_path: str, name: str) -> None:
        imports.add(module_path + '.' + name)

    def collect_methods(elements: Sequence[Node], name: str) -> Generator[FuncDecl]:
        for element in elements:
            if isinstance(element, FuncDecl):
                if element.self == name:
                    yield element

    def make_never_type() -> PyExpr:
        add_import('typing', 'Never')
        return PyNamedExpr('Never')

    def make_any_type() -> PyExpr:
        add_import('typing', 'Any')
        return PyNamedExpr('Any')

    def make_cond(iter: Iterator[tuple[PyExpr | None, Sequence[PyStmt]]]) -> list[PyStmt]:
        cases = list(iter)
        if len(cases) == 0:
            return []
        test, body = cases[0]
        if len(cases) == 1 and test is None:
            return list(body)
        assert(test is not None)
        first = PyIfCase(test=test, body=body)
        alternatives: list[PyElifCase] = []
        last = None
        for test, body in cases[1:]:
            if test is None:
                last = PyElseCase(body=body)
                break
            alternatives.append(PyElifCase(test=test, body=body))
        return [ PyIfStmt(first=first, alternatives=alternatives, last=last) ]


    def visit_ir_expr(expr: Expr) -> PyExpr:
        if isinstance(expr, PathExpr):
            return PyNamedExpr(to_var_name(expr.name))
        if isinstance(expr, AndExpr):
            return PyInfixExpr(visit_ir_expr(expr.left), PyAndKeyword(), visit_ir_expr(expr.right))
        if isinstance(expr, OrExpr):
            return PyInfixExpr(visit_ir_expr(expr.left), PyOrKeyword(), visit_ir_expr(expr.right))
        if isinstance(expr, ConstExpr):
            return PyConstExpr(expr.value)
        if isinstance(expr, CallExpr):
            return PyCallExpr(
                visit_ir_expr(expr.func),
                args=list(visit_ir_expr(arg) for arg in expr.args)
            )
        if isinstance(expr, IsExpr):
            return PyCallExpr(PyNamedExpr('isinstance'), args=[ visit_ir_expr(expr.expr), PyNamedExpr(to_type_name(expr.name)) ])
        if isinstance(expr, TupleExpr):
            return PyTupleExpr(elements=list(visit_ir_expr(element) for element in expr.elements))
        if isinstance(expr, TupleIndexExpr):
            return PySubscriptExpr(visit_ir_expr(expr.expr), [ PyConstExpr(expr.index) ])
        if isinstance(expr, NoneExpr):
            return PyNamedExpr('None')
        assert_never(expr)

    def visit_ir_type(ty: Type) -> PyExpr:
        if isinstance(ty, AnyType):
            return make_any_type()
        if isinstance(ty, NeverType):
            return make_never_type()
        if isinstance(ty, TupleType):
            return PySubscriptExpr(PyNamedExpr('tuple'), list(visit_ir_type(el_ty) for el_ty in ty.types))
        if isinstance(ty, UnionType):
            return _make_infix((visit_ir_type(el_ty) for el_ty in ty.types), PyVerticalBar(), make_never_type())
        if isinstance(ty, PathType):
            if ty.name == name_type_integer:
                return PyNamedExpr('int')
            if ty.name == name_type_string:
                return PyNamedExpr('str')
            if ty.name == name_type_optional:
                assert(ty.args is not None and len(ty.args) == 1)
                return PyInfixExpr(visit_ir_type(ty.args[0]), PyVerticalBar(), PyNamedExpr('None'))
            if ty.name == name_type_array:
                assert(ty.args is not None and len(ty.args) == 1)
                return PySubscriptExpr(PyNamedExpr('list'), [ visit_ir_type(ty.args[0]) ])
            out = PyNamedExpr(to_type_name(ty.name))
            if ty.args is not None:
                out = PySubscriptExpr(out, list(visit_ir_type(arg) for arg in ty.args))
            return out
        if isinstance(ty, NoneType):
            return PyNamedExpr('None')
        assert_never(ty)

    def visit_ir_method(node: FuncDecl) -> PyFuncDef:
        params = [ PyNamedParam(PyNamedPattern('self'))  ]
        for param in node.params:
            params.append(PyNamedParam(PyNamedPattern(to_var_name(param.name)), annotation=visit_ir_type(param.ty), default=param.default and visit_ir_expr(param.default)))
        if node.name == 'new':
            body = visit_ir_elements(node.body)
            if not body:
                body.append(PyPassStmt())
            return PyFuncDef(
                name='__init__',
                params=params,
                body=body,
            )
        body = []
        if not body:
            body.append(PyPassStmt())
        return PyFuncDef(
            name=to_var_name(node.name),
            params=params,
            body=body,
        )

    def visit_ir_elements(elements: Sequence[Node]) -> list[PyStmt]:
        out = list[PyStmt]()
        for element in elements:
            if isinstance(element, StructDecl):
                methods = collect_methods(elements, element.name)
                body = list[PyStmt](visit_ir_method(method) for method in methods)
                if not body:
                    body.append(PyPassStmt())
                out.append(PyClassDef(
                    name=to_type_name(element.name),
                    body=body,
                ))
            elif isinstance(element, EnumDecl):
                out.append(PyTypeAliasStmt(
                    name=to_type_name(element.name),
                    expr=_make_infix((visit_ir_type(variant.ty) for variant in element.variants), PyVerticalBar(), make_never_type())
                ))
            elif isinstance(element, FuncDecl):
                if element.self is not None:
                    pass # TODO
            elif isinstance(element, RetExpr):
                out.append(PyRetStmt(expr=element.value and visit_ir_expr(element.value)))
            elif isinstance(element, CondExpr):
                out.extend(make_cond((case.test and visit_ir_expr(case.test), visit_ir_elements(case.body)) for case in element.cases))
            elif isinstance(element, FieldAssign):
                out.append(PyAssignStmt(PyAttrPattern(PyNamedPattern('self'), to_var_name(element.name)), value=visit_ir_expr(element.expr)))
            elif is_expr(element):
                out.append(PyExprStmt(visit_ir_expr(element)))
            else:
                unreachable()
        return out

    return PyModule(stmts=visit_ir_elements(node.elements))

