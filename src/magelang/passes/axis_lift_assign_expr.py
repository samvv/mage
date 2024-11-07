
from typing import assert_never, cast
from magelang.ir.ast import *
from magelang.util import NameGenerator

IN_CASE_TEST = 1

def prepend(l, els):
    for el in reversed(els):
        l.insert(0, el)

def axis_lift_assign_expr(source: Program) -> Program:

    generate_temporary = NameGenerator()

    def rewrite_as_block(expr: Expr) -> tuple[list[BodyElement], Expr | None]:
        new_expr, before = rewrite_expr(expr)
        out = []
        if isinstance(new_expr, BlockExpr):
            out.extend(new_expr.body)
            last = new_expr.last
        else:
            out.append(new_expr)
            last = None
        return out, last

    def rewrite_expr(expr: Expr) -> tuple[Expr, list[BodyElement]]:
        if isinstance(expr, CondExpr):
            prev_body = []
            cases = []
            for case in reversed(expr.cases):
                if prev_body:
                    cases = [ CondCase(ConstExpr(True), CondExpr(cases)) ]
                new_test, new_test_pre = rewrite_expr(case.test)
                new_body, new_last = rewrite_as_block(case.body)
                cases.insert(0, CondCase(new_test, BlockExpr(new_body, new_last)))
                prepend(new_body, prev_body)
                prev_body = new_test_pre
            return CondExpr(cases), prev_body
        if isinstance(expr, AssignExpr):
            temp = generate_temporary()
            return PathExpr(temp), [
                AssignExpr(NamedPatt(temp), expr.expr),
                AssignExpr(expr.patt, PathExpr(temp)),
            ]
        if isinstance(expr, PathExpr):
            return expr, []
        if isinstance(expr, BreakExpr):
            if expr.value is not None:
                new_value, before = rewrite_expr(expr.value)
            else:
                new_value = None
                before = []
            return BreakExpr(new_value), before
        if isinstance(expr, CallExpr):
            before = []
            new_func, func_before = rewrite_expr(expr.func)
            before.extend(func_before)
            new_args = []
            for arg in expr.args:
                arg_expr, arg_before = rewrite_expr(arg)
                before.extend(arg_before)
                new_args.append(arg_expr)
            return CallExpr(new_func, new_args), before
        return expr, [] # FIXME
        assert_never(expr)

    def rewrite_element(element: ProgramElement | BodyElement, before) -> ProgramElement | BodyElement:
        if isinstance(element, AssignExpr):
            return element
        if is_expr(element):
            expr, expr_before = rewrite_expr(element)
            before.extend(expr_before)
            return expr
        return element

    def rewrite_elements(elements: Sequence[ProgramElement| BodyElement]) -> list[ProgramElement | BodyElement]:
        out = []
        for element in elements:
            before = []
            new_element = rewrite_element(element, before)
            out.extend(before)
            out.append(new_element)
        return out

    return source.derive(elements=cast(Sequence[ProgramElement], rewrite_elements(source.elements)))
