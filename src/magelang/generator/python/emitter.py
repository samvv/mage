
from collections.abc import Generator
from typing import assert_never
from magelang.ast import CharSetExpr, ChoiceExpr, Expr, Grammar, HideExpr, ListExpr, LitExpr, LookaheadExpr, RefExpr, RepeatExpr, SeqExpr, static_expr_to_str
from magelang.treespec import AnyType, ExternType, ListType, NeverType, NodeType, NoneType, PunctType, TokenSpec, TokenType, TupleType, UnionType, VariantType, grammar_to_specs, NodeSpec, Type
from magelang.lang.python.cst import *
from .util import Case, build_cond, gen_shallow_test, namespaced, to_class_name, build_isinstance

def generate_emitter(
    grammar: Grammar,
    prefix = '',
) -> PyModule:

    specs = grammar_to_specs(grammar, include_hidden=True)

    emit_fn_name = namespaced('emit', prefix)
    visit_fn_name = 'visit'
    emit_token_fn_name = namespaced('emit_token', prefix)
    token_param_name = 'token'
    param_name = 'node'
    out_name = 'out'

    def gen_write(expr: PyExpr) -> PyStmt:
        return PyAssignStmt(PyNamedPattern(out_name), value=PyInfixExpr(PyNamedExpr(out_name), PyPlus(), expr))

    def gen_hidden_field_emit(expr: Expr) -> Generator[PyStmt, None, None]:
        if isinstance(expr, LitExpr):
            yield gen_write(PyConstExpr(expr.text))
            return
        if isinstance(expr, RepeatExpr):
            for _ in range(0, expr.min):
                yield from gen_hidden_field_emit(expr.expr)
            return
        if isinstance(expr, CharSetExpr):
            # We assume this CharSetExpr has been reduced to its most canonical form.
            # In other words, we assume this expression has at least 2 different characters.
            # This means we cannot 'choose' the right character, so do nothing.
            return
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None or rule.expr is None:
                return
            yield from gen_hidden_field_emit(rule.expr)
            return
        if isinstance(expr, ChoiceExpr):
            # We cannot decide what rule we should take without additional
            # information, so do nothing.
            return
        if isinstance(expr, LookaheadExpr):
            # A LookaheadExpr never parses/emits anything.
            return
        if isinstance(expr, HideExpr):
            yield from gen_hidden_field_emit(expr.expr)
            return
        if isinstance(expr, SeqExpr):
            for element in expr.elements:
                yield from gen_hidden_field_emit(element)
            return
        if isinstance(expr, ListExpr):
            if expr.min_count > 0:
                yield from gen_hidden_field_emit(expr.element)
                for _ in range(1, expr.min_count):
                    yield from gen_hidden_field_emit(expr.separator)
                    yield from gen_hidden_field_emit(expr.element)
            return
        assert_never(expr)

    def gen_field_emit(ty: Type, target: PyExpr) -> Generator[PyStmt, None, None]:
        for expr in ty.before:
            yield from gen_hidden_field_emit(expr)
        if isinstance(ty, NeverType):
            yield PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ PyNamedExpr('False') ]))
        elif isinstance(ty, NoneType) or isinstance(ty, AnyType):
            pass
        elif isinstance(ty, ExternType):
            yield PyExprStmt(PyCallExpr(PyNamedExpr('str'), args=[ target ]))
        elif isinstance(ty, TokenType):
            yield gen_write(PyCallExpr(PyNamedExpr(emit_token_fn_name), args=[ target ]))
        elif isinstance(ty, NodeType) or isinstance(ty, VariantType):
            yield PyExprStmt(PyCallExpr(PyNamedExpr(visit_fn_name), args=[ target ]))
        elif isinstance(ty, ListType):
            element_name = 'element'
            yield PyForStmt(pattern=PyNamedPattern(element_name), expr=target, body=list(gen_field_emit(ty.element_type, PyNamedExpr(element_name))))
        elif isinstance(ty, PunctType):
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
                    *gen_field_emit(ty.element_type, PyNamedExpr(element_name)),
                    *gen_field_emit(ty.separator_type, PyNamedExpr(separator_name)),
                ]
            )
            yield PyIfStmt(first=PyIfCase(
                test=PyInfixExpr(PyAttrExpr(target, 'last'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                body=list(gen_field_emit(ty.element_type, PyAttrExpr(target, 'last')))
            ))
        elif isinstance(ty, TupleType):
            for i, el_ty in enumerate(ty.element_types):
                yield from gen_field_emit(el_ty, PySubscriptExpr(target, [ PyConstExpr(i) ]))
        elif isinstance(ty, UnionType):
            cases: list[Case] = []
            for element_type in ty.types:
                body = list(gen_field_emit(element_type, target))
                if body:
                    cases.append((
                        gen_shallow_test(element_type, target, prefix),
                        body
                    ))
            yield from build_cond(cases)
        else:
            assert_never(ty)
        for expr in ty.after:
            yield from gen_hidden_field_emit(expr)

    emit_token_body = []

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
            for field in spec.fields:
                if_body.extend(gen_field_emit(field.ty, PyAttrExpr(PyNamedExpr(param_name), field.name)))
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
            name=emit_fn_name,
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
