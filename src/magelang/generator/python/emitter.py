
# FIXME This emitter generator doesn't work (yet). It is disabled by default.

from collections.abc import Generator
from typing import assert_never
from magelang.analysis import is_empty, intersects, is_eof
from magelang.emitter import emit
from magelang.ast import CharSetExpr, ChoiceExpr, Expr, Grammar, HideExpr, ListExpr, LitExpr, LookaheadExpr, RefExpr, RepeatExpr, SeqExpr, flatten_choice, static_expr_to_str
from magelang.treespec import TokenSpec, grammar_to_specs, NodeSpec, infer_type, is_unit
from magelang.lang.python.cst import *
from magelang.util import todo
from .util import Case, build_cond, gen_shallow_test, namespaced, to_class_name, build_isinstance

def generate_emitter(
    grammar: Grammar,
    prefix = '',
) -> PyModule:

    specs = grammar_to_specs(grammar, include_hidden=True)

    skip_rule = grammar.skip_rule
    emit_node_fn_name = namespaced('emit', prefix)
    visit_fn_name = 'visit'
    emit_token_fn_name = namespaced('emit_token', prefix)
    token_param_name = 'token'
    param_name = 'node'
    out_name = 'out'

    def gen_visit_node(target: PyExpr) -> Generator[PyStmt, None, None]:
        yield PyExprStmt(PyCallExpr(PyNamedExpr(visit_fn_name), args=[ target ]))

    def gen_write_token(target: PyExpr) -> Generator[PyStmt, None, None]:
        yield gen_write(PyCallExpr(PyNamedExpr(emit_token_fn_name), args=[ target ]))

    def gen_write(expr: PyExpr) -> PyStmt:
        return PyAssignStmt(PyNamedPattern(out_name), value=PyInfixExpr(PyNamedExpr(out_name), PyPlus(), expr))

    def gen_skip() -> Generator[PyStmt, None, None]:
        assert(skip_rule is not None and skip_rule.expr is not None)
        return gen_emit_expr(skip_rule.expr, None, False)

    def eliminate_choices(expr: ChoiceExpr, last: bool) -> list[Expr]:
        out = []
        for element in flatten_choice(expr):
            if not last and is_eof(element):
                continue
            out.append(element)
        return out

    def gen_emit_expr(expr: Expr, target: PyExpr | None, last: bool) -> Generator[PyStmt, None, None]:
        # NOTE This logic must be in sync with infer_type() in magelang.treespec
        if isinstance(expr, LitExpr):
            yield gen_write(PyConstExpr(expr.text))
        elif isinstance(expr, RepeatExpr):
            if target is None:
                # We only generate the minimum amount of tokens so that our grammar is correct.
                # Any excessive tokens are not produced by this logic
                for _ in range(0, expr.min):
                    yield from gen_emit_expr(expr.expr, target, last)
            else:
                if expr.min == 0 and expr.max == 1:
                    yield PyIfStmt(first=PyIfCase(
                        test=PyInfixExpr(target, (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                        body=list(gen_emit_expr(expr.expr, target, last))
                    ))
                    return
                element_name = 'element'
                yield PyForStmt(pattern=PyNamedPattern(element_name), expr=target, body=list(gen_emit_expr(expr.expr, PyNamedExpr(element_name), last)))
        elif isinstance(expr, CharSetExpr):
            if target is None:
                # We assume this CharSetExpr has been reduced to its most canonical form.
                # In other words, we assume this expression has at least 2 different characters.
                # This means we cannot 'choose' the right character, so do nothing.
                pass
            else:
                yield gen_write(PyCallExpr(PyNamedExpr(emit_token_fn_name), args=[ target ]))
        elif isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None:
                return
            if rule.is_extern:
                return # TODO
            if rule.expr is None:
                return
            if not rule.is_public or target is None:
                yield from gen_emit_expr(rule.expr, target, True)
                return
            if grammar.is_token_rule(rule):
                yield from gen_write_token(target)
                return
            yield from gen_visit_node(target)
        elif isinstance(expr, ChoiceExpr):
            if target is None:
                # We cannot decide what rule we should take without additional
                # information, so do nothing.
                choices = eliminate_choices(expr, last)
                if len(choices) == 1:
                    yield from gen_emit_expr(choices[0], target, last)
            else:
                cases: list[Case] = []
                for element in expr.elements:
                    body = list(gen_emit_expr(element, target, last))
                    if body:
                        cases.append((
                            gen_shallow_test(infer_type(element, grammar), target, prefix),
                            body
                        ))
                yield from build_cond(cases)
        elif isinstance(expr, LookaheadExpr):
            # A LookaheadExpr never parses/emits anything.
            pass
        elif isinstance(expr, HideExpr):
            # `target` is set to `None` because it won't hold any information about a hidden expression
            yield from gen_emit_expr(expr.expr, None, last)
        elif isinstance(expr, SeqExpr):
            if target is None:
                n = len(expr.elements)
                for i, element in enumerate(expr.elements):
                    yield from gen_emit_expr(element, target, last and i+1 == n)
            else:
                n = len(expr.elements)
                m = len(list(filter(lambda element: not is_unit(infer_type(element, grammar)), expr.elements)))
                k = 0 # Keeps track of the tuple index in the struct
                for i, element in enumerate(expr.elements):
                    if is_unit(infer_type(element, grammar)):
                        yield from gen_emit_expr(element, None, last)
                    else:
                        yield from gen_emit_expr(element, target if m == 1 else PySubscriptExpr(target, [ PyConstExpr(k) ]), last and i == n)
                        k += 1
        elif isinstance(expr, ListExpr):
            if target is None:
                if expr.min_count > 0:
                    yield from gen_emit_expr(expr.element, target, last)
                    for _ in range(1, expr.min_count):
                        yield from gen_emit_expr(expr.separator, target, last)
                        yield from gen_emit_expr(expr.element, target, last)
            else:
                element_name = 'element'
                separator_name = 'separator'
                yield PyForStmt(
                    pattern=PyTuplePattern(
                        elements=[
                            PyNamedPattern(element_name),
                            PyNamedPattern(separator_name)
                        ],
                    ),
                    expr=PyAttrExpr(target, 'elements'),
                    body=[
                        *gen_emit_expr(expr.element, PyNamedExpr(element_name), last),
                        *gen_emit_expr(expr.separator, PyNamedExpr(separator_name), last),
                    ]
                )
                yield PyIfStmt(first=PyIfCase(
                    test=PyInfixExpr(PyAttrExpr(target, 'last'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                    body=list(gen_emit_expr(expr.element, PyAttrExpr(target, 'last'), last))
                ))
        else:
            assert_never(expr)

    emit_token_body = []
    prev_expr = None

    visit_node_body: list[PyStmt] = [
        PyNonlocalStmt([ out_name ]),
    ]

    for spec in specs:

        if isinstance(spec, TokenSpec):
            if spec.is_static:
                assert(spec.rule is not None)
                assert(spec.rule.expr is not None)
                expr = PyConstExpr(static_expr_to_str(spec.rule.expr))
            else:
                expr = PyCallExpr(PyNamedExpr('str'), args=[ PyAttrExpr(PyNamedExpr(token_param_name), 'value') ])
            emit_token_body.append(
                PyIfStmt(PyIfCase(
                    test=build_isinstance(PyNamedExpr(token_param_name), PyNamedExpr(to_class_name(spec.name, prefix))),
                    body=[ PyRetStmt(expr=expr) ]
                ))
            )

        elif isinstance(spec, NodeSpec):
            if_body = []
            n  = len(spec.fields)
            # FIXME iterating over the fields skips some expressions
            for i, field in enumerate(spec.fields):
                if prev_expr is not None and intersects(prev_expr, field.expr, grammar):
                    if_body.extend(gen_skip())
                prev_expr = field.expr
                if_body.extend(gen_emit_expr(field.expr, PyAttrExpr(PyNamedExpr(param_name), field.name), i == n))
            if_body.append(PyRetStmt())
            visit_node_body.append(PyIfStmt(first=PyIfCase(
                test=build_isinstance(PyNamedExpr(param_name), PyNamedExpr(to_class_name(spec.name, prefix))),
                body=if_body
            )))

    emit_token_body.append(
        PyExprStmt(PyCallExpr(PyNamedExpr('assert_never'), args=[ PyNamedExpr(token_param_name) ]))
    )

    return PyModule(stmts=[
        PyImportFromStmt(
            PyAbsolutePath('typing'),
            [ PyFromAlias('assert_never') ],
        ),
        PyImportFromStmt(
            PyRelativePath(dots=1, name='cst'),
            [ PyFromAlias(PyAsterisk()) ],
        ),
        PyFuncDef(
            name=emit_token_fn_name,
            params=[ PyNamedParam(PyNamedPattern(token_param_name)) ],
            body=emit_token_body,
        ),
        PyFuncDef(
            name=emit_node_fn_name,
            params=[ PyNamedParam(PyNamedPattern(param_name)) ],
            body=[
                PyAssignStmt(PyNamedPattern(out_name), value=PyConstExpr('')),
                PyFuncDef(
                    name=visit_fn_name,
                    params=[ PyNamedParam(PyNamedPattern(param_name)) ],
                    body=visit_node_body
                ),
                PyExprStmt(PyCallExpr(PyNamedExpr(visit_fn_name), args=[ PyNamedExpr(param_name) ])),
                PyRetStmt(expr=PyNamedExpr(out_name)),
            ],
        ),
    ])

