
from typing import cast
from .cst import *

def preorder(expr: PyExpr) -> list[PyExpr]:
    out = []
    def visit(expr: PyExpr) -> None:
        out.append(expr)
        for_each_py_expr(expr, visit)
    visit(expr)
    return out

def assert_order(expected: Sequence[Any], actual: Sequence[Any]) -> None:
    assert(len(expected) == len(actual))
    for a, b in zip(expected, actual):
        assert(a is b)

def test_coerce_named_expr_name():
    e = PyNamedExpr('foo')
    assert(isinstance(e.name, PyIdent))

def test_coerce_def_keyword():
    stmt = PyFuncDef(name='hello', body=[])
    assert(isinstance(stmt.def_keyword, PyDefKeyword))

def test_visit_infix_expr():
    e1 = PyNamedExpr('foo')
    e2 = PyNamedExpr('bar')
    e3 = PyInfixExpr(e1, PyPlus(), e2)
    assert_order([ e3, e1, e2 ], preorder(e3))

def test_visit_list_expr():
    e1 = PyConstExpr(1)
    e2 = PyConstExpr(2)
    e3 = PyListExpr(elements=[ e1, e2 ])
    assert_order([e3, e1, e2], preorder(e3))

def test_rewrite_call_expr():
    e1 = PyNamedExpr('foo')
    e2 = PyConstExpr(1)
    e3 = PyConstExpr(2)
    e4 = PyCallExpr(e1, args=[ e2, e3 ])

    def rewrite(expr: PyExpr) -> PyExpr:
        if isinstance(expr, PyConstExpr):
            return expr.derive(literal=cast(PyInteger, expr.literal).value + 1)
        return rewrite_each_py_expr(expr, rewrite)

    r = rewrite(e4)

    assert(isinstance(r, PyCallExpr))
    assert(r.operator is e1)
    assert(r.args[0] is not e2)
    assert(r.args[1] is not e3)
    assert(isinstance(r.args[0][0], PyConstExpr))
    assert(cast(PyInteger, r.args[0][0].literal).value == 2)
    assert(isinstance(r.args[1][0], PyConstExpr))
    assert(r.args[1][0].literal.value == 3)

