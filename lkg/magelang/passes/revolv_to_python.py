
from typing import Generator, TypeIs, assert_never, Iterable, Iterator
from magelang.util import is_iterator, panic, to_camel_case, todo
from magelang.lang.revolv.ast import *
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

# Expressions that by now should only appear as statements
type StmtExpr = BreakExpr | AssignExpr | ForExpr | LoopExpr | RetExpr

def is_stmt_expr(expr: Expr) -> TypeIs[StmtExpr]:
    return isinstance(expr, BreakExpr) \
        or isinstance(expr, AssignExpr) \
        or isinstance(expr, ForExpr) \
        or isinstance(expr, LoopExpr) \
        or isinstance(expr, RetExpr)

type PyCondCase = tuple[PyExpr | None, Sequence[PyStmt]]

def revolv_to_python(node: Program) -> PyModule:

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

    def make_cond(iter: Iterable[PyCondCase] | Iterator[PyCondCase]) -> list[PyStmt]:
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
        if isinstance(expr, LitExpr):
            return PyConstExpr(expr.value)
        if isinstance(expr, CallExpr):
            if isinstance(expr.func, PathExpr):
                if expr.func.name == name_fn_and:
                    assert(expr.args is not None)
                    return PyInfixExpr(visit_ir_expr(expr.args[0]), PyAndKeyword(), visit_ir_expr(expr.args[1]))
                if expr.func.name == name_fn_or:
                    assert(expr.args is not None)
                    return PyInfixExpr(visit_ir_expr(expr.args[0]), PyOrKeyword(), visit_ir_expr(expr.args[1]))
            return PyCallExpr(
                visit_ir_expr(expr.func),
                args=list(visit_ir_expr(arg) for arg in expr.args)
            )
        if isinstance(expr, IsExpr):
            if expr.name == name_variant_none: # FIXME
                return PyInfixExpr(visit_ir_expr(expr.expr), PyIsKeyword(), PyNamedExpr('None'))
            return PyCallExpr(PyNamedExpr('isinstance'), args=[ visit_ir_expr(expr.expr), PyNamedExpr(to_type_name(expr.name)) ])
        if isinstance(expr, TupleExpr):
            return PyTupleExpr(elements=list(visit_ir_expr(element) for element in expr.elements))
        if isinstance(expr, TupleIndexExpr):
            return PySubscriptExpr(visit_ir_expr(expr.expr), [ PyConstExpr(expr.index) ])
        if isinstance(expr, NoneExpr):
            return PyNamedExpr('None')
        if isinstance(expr, EnumExpr):
            if expr.name == name_variant_none:
                return PyNamedExpr('None')
            if expr.name == name_variant_some:
                return visit_ir_expr(expr.args[0])
            return PyCallExpr(PyNamedExpr(expr.name), args=list(visit_ir_expr(arg) for arg in expr.args))
        if isinstance(expr, NewExpr):
            return PyCallExpr(PyNamedExpr(expr.name), args=list(visit_ir_expr(arg) for arg in expr.args))
        if is_stmt_expr(expr):
            panic(f"Statement expressions such as {expr} should not occur here")
        panic(f"Expression should have been covered: {expr}")

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

    def visit_ir_patt(patt: Patt) -> PyPattern:
        assert(not isinstance(patt, VariantPatt))
        if isinstance(patt, NamedPatt):
            return PyNamedPattern(patt.name)
        if isinstance(patt, TuplePatt):
            return PyTuplePattern(elements=list(visit_ir_patt(element) for element in patt.elements))
        assert_never(patt)

    def block_to_body(expr: Expr) -> list[BodyElement]:
        if not isinstance(expr, BlockExpr):
            return [ expr ]
        out = list(expr.body)
        if expr.last is not None:
            out.append(expr.last)
        return out

    def visit_ir_elements(elements: Sequence[ProgramElement | BodyElement]) -> list[PyStmt]:
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
                if element.self is None:
                    out.append(PyFuncDef(
                        name=to_var_name(element.name),
                        params=list(PyNamedParam(PyNamedPattern(param.name), annotation=visit_ir_type(param.ty)) for param in element.params),
                        return_type=visit_ir_type(element.returns),
                        body=visit_ir_elements(element.body),
                    ))
            elif isinstance(element, VarDecl):
                todo()
            elif isinstance(element, RetExpr):
                out.append(PyRetStmt(expr=element.value and visit_ir_expr(element.value)))
            elif isinstance(element, CondExpr):
                py_cases = list[PyCondCase]()
                for case in element.cases:
                    body = block_to_body(case.body)
                    py_test = visit_ir_expr(case.test)
                    py_body = visit_ir_elements(body)
                    py_cases.append((py_test, py_body))
                out.extend(make_cond(py_cases))
            elif isinstance(element, AssignExpr):
                out.append(PyAssignStmt(visit_ir_patt(element.patt), value=visit_ir_expr(element)))
            elif isinstance(element, FieldAssignExpr):
                out.append(PyAssignStmt(PyAttrPattern(PyNamedPattern('self'), to_var_name(element.name)), value=visit_ir_expr(element.expr)))
            elif isinstance(element, BreakExpr):
                out.append(PyBreakStmt())
            else:
                out.append(PyExprStmt(visit_ir_expr(element)))
        return out

    return PyModule(stmts=visit_ir_elements(node.elements))

