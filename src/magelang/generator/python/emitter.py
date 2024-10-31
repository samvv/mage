
# FIXME This emitter generator doesn't work (yet). It is disabled by default.

from collections.abc import Generator
from typing import assert_never, cast

from intervaltree.intervaltree import warn
from magelang.analysis import intersects, can_be_empty
from magelang.ast import CharSetExpr, ChoiceExpr, Expr, Grammar, HideExpr, ListExpr, LitExpr, LookaheadExpr, RefExpr, RepeatExpr, Rule, SeqExpr, static_expr_to_str
from magelang.emitter import emit
from magelang.treespec import Field, get_fields, grammar_to_specs, infer_type, is_unit
from magelang.lang.python.cst import *
from magelang.util import unreachable
from .util import Case, build_cond, gen_shallow_test, namespaced, to_class_name, build_isinstance

def generate_emitter(
    grammar: Grammar,
    prefix = '',
    include_hidden: bool = False,
) -> PyModule:

    specs = grammar_to_specs(grammar, include_hidden=True)

    skip_rule = Rule('___', LitExpr(' ')) # grammar.skip_rule # FIXME
    emit_node_fn_name = namespaced('emit', prefix)
    visit_fn_name = 'visit'
    emit_token_fn_name = namespaced('emit_token', prefix)
    token_param_name = 'token'
    param_name = 'node'
    out_name = 'out'

    is_token_name = f"is_{namespaced('token', prefix)}"

    def references_token_rule(expr: Expr) -> bool:
        if  not isinstance(expr, RefExpr):
            return False
        rule = grammar.lookup(expr.name)
        return rule is not None and rule.expr is not None and grammar.is_token_rule(rule)

    def gen_visit_node(target: PyExpr) -> Generator[PyStmt, None, None]:
        yield PyExprStmt(PyCallExpr(PyNamedExpr(visit_fn_name), args=[ target ]))

    def gen_write_token(target: PyExpr) -> Generator[PyStmt, None, None]:
        yield gen_write(PyCallExpr(PyNamedExpr(emit_token_fn_name), args=[ target ]))

    def gen_write(expr: PyExpr) -> PyStmt:
        return PyAugAssignStmt(PyNamedPattern(out_name), PyPlus(), expr)

    def gen_skip() -> Generator[PyStmt, None, None]:
        assert(skip_rule is not None and skip_rule.expr is not None)
        return gen_emit_expr(skip_rule.expr, None, False)

    # def eliminate_choices(expr: ChoiceExpr, last: bool) -> list[Expr]:
    #     out = []
    #     for element in flatten_choice(expr):
    #         if not last and is_eof(element):
    #             continue
    #         out.append(element)
    #     return out

    def gen_emit_expr(expr: Expr, target: PyExpr | None, skip: bool) -> Generator[PyStmt, None, None]:
        # NOTE This logic must be in sync with infer_type() in magelang.treespec
        if isinstance(expr, LitExpr):
            yield gen_write(PyConstExpr(expr.text))
        elif isinstance(expr, RepeatExpr):
            if target is None:
                # We only generate the minimum amount of tokens so that our grammar is correct.
                # Any excessive tokens are not produced by this logic
                for i in range(0, expr.min):
                    yield from gen_emit_expr(expr.expr, target, skip)
            else:
                if expr.min == 0 and expr.max == 1:
                    yield PyIfStmt(first=PyIfCase(
                        test=PyInfixExpr(target, (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                        body=list(gen_emit_expr(expr.expr, target, skip))
                    ))
                    return
                element_name = 'element'
                yield PyForStmt(pattern=PyNamedPattern(element_name), expr=target, body=list(gen_emit_expr(expr.expr, PyNamedExpr(element_name), skip)))
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
                assert(target is not None)
                yield from gen_write_token(target)
                return # TODO
            if rule.expr is None:
                return
            if not rule.is_public or target is None:
                yield from gen_emit_expr(rule.expr, target, skip)
                return
            if grammar.is_token_rule(rule):
                yield from gen_write_token(target)
                if skip:
                    yield from gen_skip()
                return
            if grammar.is_variant_rule(rule):
                expr = cast(ChoiceExpr, rule.expr)
                token_count = sum(int(references_token_rule(element)) for element in expr.elements)
                if token_count == len(expr.elements):
                    yield from gen_write_token(target)
                elif token_count > 0:
                    yield PyIfStmt(
                        first=PyIfCase(
                            test=PyCallExpr(PyNamedExpr(is_token_name), args=[ target ]),
                            body=list(gen_write_token(target)),
                        ),
                        last=list(gen_visit_node(target)),
                    )
            yield from gen_visit_node(target)
        elif isinstance(expr, ChoiceExpr):
            if target is None:
                # We cannot decide what rule we should take without additional
                # information, so do nothing.
                # choices = eliminate_choices(expr)
                # if len(choices) == 1:
                #     yield from gen_emit_expr(choices[0], target)
                pass
            else:
                cases: list[Case] = []
                for element in expr.elements:
                    body = list(gen_emit_expr(element, target, skip))
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
            yield from gen_emit_expr(expr.expr, None, skip)
        elif isinstance(expr, SeqExpr):
            if target is None:
                n = len(expr.elements)
                for i, element in enumerate(expr.elements):
                    yield from gen_emit_expr(element, target, skip)
            else:
                n = len(expr.elements)
                m = len(list(filter(lambda element: not is_unit(infer_type(element, grammar)), expr.elements)))
                k = 0 # Keeps track of the tuple index in the struct
                for i, element in enumerate(expr.elements):
                    if is_unit(infer_type(element, grammar)):
                        yield from gen_emit_expr(element, None, skip and i == 0)
                    else:
                        yield from gen_emit_expr(element, target if m == 1 else PySubscriptExpr(target, [ PyConstExpr(k) ]), skip and i == 0)
                        k += 1
        elif isinstance(expr, ListExpr):
            if target is None:
                if expr.min_count > 0:
                    yield from gen_emit_expr(expr.element, target, skip)
                    for _ in range(1, expr.min_count):
                        yield from gen_emit_expr(expr.separator, target, skip)
                        yield from gen_emit_expr(expr.element, target, skip)
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
                        *gen_emit_expr(expr.element, PyNamedExpr(element_name), skip),
                        *gen_emit_expr(expr.separator, PyNamedExpr(separator_name), skip),
                    ]
                )
                yield PyIfStmt(first=PyIfCase(
                    test=PyInfixExpr(PyAttrExpr(target, 'last'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                    body=list(gen_emit_expr(expr.element, PyAttrExpr(target, 'last'), skip))
                ))
        else:
            assert_never(expr)

    emit_token_body = []

    visit_node_body: list[PyStmt] = [
        PyNonlocalStmt([ out_name ]),
    ]

    for rule in grammar.rules:

        if grammar.is_token_rule(rule):
            assert(rule.expr is not None)
            if grammar.is_static_token(rule.expr):
                expr = PyConstExpr(static_expr_to_str(rule.expr))
            else:
                expr = PyCallExpr(PyNamedExpr('str'), args=[ PyAttrExpr(PyNamedExpr(token_param_name), 'value') ])
            emit_token_body.append(
                PyIfStmt(PyIfCase(
                    test=build_isinstance(PyNamedExpr(token_param_name), PyNamedExpr(to_class_name(rule.name, prefix))),
                    body=[ PyRetStmt(expr=expr) ]
                ))
            )

        elif grammar.is_variant_rule(rule):
           pass

        elif grammar.is_parse_rule(rule):
            assert(rule.expr is not None)
            if_body = []
            items = list(get_fields(rule.expr, include_hidden=include_hidden, grammar=grammar))
            for i, item in enumerate(items):
                expr = item.expr if isinstance(item, Field) else item
                skip = False
                for k in range(i+1, len(items)):
                    item_2 = items[k]
                    expr_2 = item_2.expr if isinstance(item_2, Field) else item_2
                    if intersects(expr, expr_2, grammar=grammar):
                        print('------------')
                        print(emit(expr))
                        print(emit(expr_2))
                        skip = True
                        break
                    if not can_be_empty(expr_2, grammar=grammar):
                        break
                if isinstance(item, Field):
                    if_body.extend(gen_emit_expr(expr, PyAttrExpr(PyNamedExpr(param_name), item.name), skip))
                else:
                    if_body.extend(gen_emit_expr(expr, None, skip))
            if_body.append(PyRetStmt())
            visit_node_body.append(PyIfStmt(first=PyIfCase(
                test=build_isinstance(PyNamedExpr(param_name), PyNamedExpr(to_class_name(rule.name, prefix))),
                body=if_body
            )))

        elif rule == grammar.skip_rule:
            pass

        else:
            print(rule.name)
            unreachable()

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

