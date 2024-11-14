
# FIXME

from collections.abc import Generator
from typing import assert_never, cast

from magelang.analysis import intersects, can_be_empty
from magelang.lang.mage.ast import MageCharSetExpr, MageChoiceExpr, MageExpr, MageGrammar, MageHideExpr, MageListExpr, MageLitExpr, MageLookaheadExpr, MageRefExpr, MageRepeatExpr, MageRule, MageSeqExpr, static_expr_to_str
from magelang.helpers import Field, get_fields, infer_type, is_unit_type
from magelang.lang.python.cst import *
from magelang.util import unreachable
from magelang.helpers import PyCondCase, make_py_cond, treespec_type_to_shallow_py_test, namespaced, to_py_class_name, make_py_isinstance

def mage_to_python_emitter(
    grammar: MageGrammar,
    prefix: str = '',
    include_hidden: bool = False,
) -> PyModule:

    skip_rule = MageRule('___', MageLitExpr(' ')) # grammar.skip_rule # FIXME
    emit_node_fn_name = namespaced('emit', prefix)
    visit_fn_name = 'visit'
    emit_token_fn_name = namespaced('emit_token', prefix)
    token_param_name = 'token'
    param_name = 'node'
    out_name = 'out'

    is_token_name = f"is_{namespaced('token', prefix)}"

    def references_token_rule(expr: MageExpr) -> bool:
        if  not isinstance(expr, MageRefExpr):
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

    def get_expr(item: MageExpr | Field) -> MageExpr:
        return item.expr if isinstance(item, Field) else item

    def is_skip(elements: Sequence[MageExpr | Field], i: int) -> bool:
        expr = get_expr(elements[i])
        for k in range(i+1, len(items)):
            item_2 = items[k]
            expr_2 = item_2.expr if isinstance(item_2, Field) else item_2
            if intersects(expr, expr_2, grammar=grammar):
                return True
            if not can_be_empty(expr_2, grammar=grammar):
                break
        return False

    def is_empty(expr: MageExpr) -> bool:
        # HACK Infer whether it is a hidden field or a lookahead expression
        return is_unit_type(infer_type(expr, grammar))

    # def eliminate_choices(expr: ChoiceExpr, last: bool) -> list[MageExpr]:
    #     out = []
    #     for element in flatten_choice(expr):
    #         if not last and is_eof(element):
    #             continue
    #         out.append(element)
    #     return out

    def gen_emit_expr(expr: MageExpr, target: PyExpr | None, skip: bool) -> Generator[PyStmt, None, None]:
        # NOTE This logic must be in sync with infer_type() in magelang.treespec
        if isinstance(expr, MageLitExpr):
            yield gen_write(PyConstExpr(expr.text))
        elif isinstance(expr, MageRepeatExpr):
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
        elif isinstance(expr, MageCharSetExpr):
            if target is None:
                # We assume this CharSetExpr has been reduced to its most canonical form.
                # In other words, we assume this expression has at least 2 different characters.
                # This means we cannot 'choose' the right character, so do nothing.
                pass
            else:
                yield gen_write(PyCallExpr(PyNamedExpr(emit_token_fn_name), args=[ target ]))
        elif isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None:
                return
            if rule.is_extern:
                if target is None:
                    pass # TODO cover case where target is not set
                else:
                    yield from gen_write_token(target)
                return
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
                expr = cast(MageChoiceExpr, rule.expr)
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
        elif isinstance(expr, MageChoiceExpr):
            if target is None:
                # We cannot decide what rule we should take without additional
                # information, so do nothing.
                # choices = eliminate_choices(expr)
                # if len(choices) == 1:
                #     yield from gen_emit_expr(choices[0], target)
                pass
            else:
                cases: list[PyCondCase] = []
                for element in expr.elements:
                    body = list(gen_emit_expr(element, target, skip))
                    if body:
                        cases.append((
                            treespec_type_to_shallow_py_test(infer_type(element, grammar), target, prefix),
                            body
                        ))
                yield from make_py_cond(cases)
        elif isinstance(expr, MageLookaheadExpr):
            # A LookaheadExpr never parses/emits anything.
            pass
        elif isinstance(expr, MageHideExpr):
            # `target` is set to `None` because by definition it won't hold any information
            yield from gen_emit_expr(expr.expr, None, skip)
        elif isinstance(expr, MageSeqExpr):
            tuple_len = len(list(filter(lambda element: not is_empty(element), expr.elements)))
            tuple_index = 0
            for i, element in enumerate(expr.elements):
                new_skip = (i == 0 and skip) or is_skip(expr.elements, i)
                if target is None or is_empty(element):
                    yield from gen_emit_expr(element, None, new_skip)
                else:
                    yield from gen_emit_expr(element, target if tuple_len == 1 else PySubscriptExpr(target, [ PyConstExpr(tuple_index) ]), new_skip)
                    tuple_index += 1
        elif isinstance(expr, MageListExpr):
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
            if rule.expr is None:
                # TODO cover this case
                continue
            if grammar.is_static_token_rule(rule):
                expr = PyConstExpr(static_expr_to_str(rule.expr))
            else:
                expr = PyCallExpr(PyNamedExpr('str'), args=[ PyAttrExpr(PyNamedExpr(token_param_name), 'value') ])
            emit_token_body.append(
                PyIfStmt(PyIfCase(
                    test=make_py_isinstance(PyNamedExpr(token_param_name), PyNamedExpr(to_py_class_name(rule.name, prefix))),
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
                expr = get_expr(item)
                skip = is_skip(items, i)
                if isinstance(item, Field):
                    if_body.extend(gen_emit_expr(expr, PyAttrExpr(PyNamedExpr(param_name), item.name), skip))
                else:
                    if_body.extend(gen_emit_expr(expr, None, skip))
            if_body.append(PyRetStmt())
            visit_node_body.append(PyIfStmt(first=PyIfCase(
                test=make_py_isinstance(PyNamedExpr(param_name), PyNamedExpr(to_py_class_name(rule.name, prefix))),
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

