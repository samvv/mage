
from typing import assert_never, cast
from magelang.lang.revolv.ast import *
from magelang.util import NameGenerator

IN_CASE_TEST = 1

def prepend(l, els):
    for el in reversed(els):
        l.insert(0, el)

def revolv_lift_assign_expr(source: Program) -> Program:

    generate_temporary = NameGenerator()

    def rewrite_as_block(expr: Expr, before: list[BodyElement]) -> tuple[list[BodyElement], Expr | None]:
        new_expr = rewrite_expr(expr, before)
        if isinstance(new_expr, BlockExpr):
            return list(new_expr.body), new_expr.last
        else:
            return [], new_expr

    def make_block(body: Body, last: Expr | None) -> Expr:
        return BlockExpr(body, last) if body or last is None else last

    def rewrite_expr(expr: Expr, before: list[BodyElement]) -> Expr:
        if isinstance(expr, CondExpr):
            cases = []
            prev_case_before = []
            for case in reversed(expr.cases):
                if prev_case_before:
                    # TODO assign `last`
                    cases = [ CondCase(LitExpr(True), BlockExpr([ *prev_case_before, CondExpr(cases) ])) ]
                new_case_before = []
                new_test = rewrite_expr(case.test, new_case_before)
                new_body, new_last = rewrite_as_block(case.body, new_case_before)
                # prepend(new_body, prev_case_before)
                cases.insert(0, CondCase(new_test, make_block(new_body, new_last)))
                prev_case_before = new_case_before
            before.extend(prev_case_before)
            return CondExpr(cases)
        if isinstance(expr, AssignExpr):
            temp = generate_temporary()
            before.append(AssignExpr(NamedPatt(temp), expr.expr))
            before.append(AssignExpr(expr.patt, PathExpr(temp)))
            return PathExpr(temp)
        if isinstance(expr, PathExpr):
            return expr
        if isinstance(expr, LitExpr):
            return expr
        if isinstance(expr, BreakExpr):
            new_value = expr.value and rewrite_expr(expr.value, before)
            return BreakExpr(new_value)
        if isinstance(expr, CallExpr):
            new_func = rewrite_expr(expr.func, before)
            new_args = list(rewrite_expr(arg, before) for arg in expr.args)
            return CallExpr(new_func, new_args)
        if isinstance(expr, TupleExpr):
            return TupleExpr(list(rewrite_expr(element, before) for element in expr.elements))
        if isinstance(expr, TupleIndexExpr):
            return TupleIndexExpr(rewrite_expr(expr.expr, before), expr.index)
        if isinstance(expr, RetExpr):
            return RetExpr(expr.value and rewrite_expr(expr.value, before))
        if isinstance(expr, LoopExpr):
            return LoopExpr(rewrite_body(expr.body))
        if isinstance(expr, ForExpr):
            return ForExpr(expr.patt, rewrite_expr(expr.iter, before), rewrite_body(expr.body))
        if isinstance(expr, NewExpr):
            return NewExpr(expr.name, list(rewrite_expr(arg, before) for arg in expr.args))
        if isinstance(expr, MatchExpr):
            new_value = rewrite_expr(expr.value, before)
            new_arms = []
            for arm in expr.arms:
                new_before = []
                body, last = rewrite_as_block(arm.expr, new_before)
                prepend(body, new_before)
                new_arms.append(MatchArm(arm.patt, make_block(body, last)))
            return MatchExpr(new_value, new_arms)
        if isinstance(expr, BlockExpr):
            new_body = rewrite_body(expr.body)
            last_before = []
            new_last = expr.last and rewrite_expr(expr.last, last_before)
            new_body.extend(last_before)
            return BlockExpr(new_body, new_last)
        assert_never(expr)

    def rewrite_body(elements: Sequence[BodyElement]) -> list[BodyElement]:
        return cast(list[BodyElement], rewrite_elements(cast(Sequence[BodyElement], elements)))

    def rewrite_element(element: ProgramElement | BodyElement, before) -> ProgramElement | BodyElement:
        if isinstance(element, AssignExpr):
            return element
        if is_expr(element):
            expr = rewrite_expr(element, before)
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
