
from collections.abc import Iterable
from typing import assert_never, cast

from magelang.logging import warn
from magelang.passes.mage_to_treespec import mage_to_treespec
from magelang.analysis import intersects, can_be_empty
from magelang.lang.mage.ast import *
from magelang.helpers import get_fields, infer_type, is_unit_type
from magelang.lang.python.cst import *
from magelang.manager import declare_pass
from magelang.util import NameGenerator, unreachable
from magelang.helpers import PyCondCase, make_py_cond, treespec_type_to_shallow_py_test, namespaced, to_py_class_name, make_py_isinstance

@declare_pass()
def mage_to_python_emitter(
    grammar: MageGrammar,
    prefix: str = '',
    include_hidden: bool = False,
) -> PyModule:
    """
    Expects:
     - mage_insert_magic_rules: support for some generic types
     - mage_insert_skip: correct handling of whitespace etc.
    Does NOT expect:
     - mage_inline
    """

    emit_node_fn_name = namespaced('emit', prefix)
    visit_fn_name = 'visit'
    emit_token_fn_name = namespaced('emit_token', prefix)
    token_param_name = 'token'
    param_name = 'node'
    out_name = 'out'

    # FIXME ideally we don't want to rely on this transformation directly
    specs = mage_to_treespec(grammar)

    hook_names = set[str]()

    is_token_name = f"is_{namespaced('token', prefix)}"

    generate = NameGenerator()

    def references_token_rule(expr: MageExpr) -> bool:
        if  not isinstance(expr, MageRefExpr):
            return False
        rule = grammar.lookup(expr.name)
        return rule is not None and rule.expr is not None and grammar.is_token_rule(rule)

    def gen_visit_node(target: PyExpr) -> Iterable[PyStmt]:
        yield PyExprStmt(PyCallExpr(PyNamedExpr(visit_fn_name), args=[ target ]))

    def gen_write_token(target: PyExpr) -> Iterable[PyStmt]:
        yield gen_write(PyCallExpr(PyNamedExpr(emit_token_fn_name), args=[ target ]))
        yield PyAssignStmt(PyNamedPattern('prev_token'), value=target)

    def gen_write(expr: PyExpr) -> PyStmt:
        return PyAugAssignStmt(PyNamedPattern(out_name), PyPlus(), expr)

    def is_empty(expr: MageExpr) -> bool:
        # HACK Infer whether it is a hidden field or a lookahead expression
        return is_unit_type(infer_type(expr, grammar))

    prev_target = None
    def gen_hook_stmt(expr: MageExpr) -> Iterable[PyStmt]:
        nonlocal prev_target
        if isinstance(expr, MageRefExpr):
            hook_name = f'gen_{expr.name}'
            hook_names.add(hook_name)
            yield gen_write(PyCallExpr(PyNamedExpr(hook_name), args=[ PyNamedExpr('ctx'), PyNamedExpr('prev_token') ]))
        elif isinstance(expr, MageRepeatExpr):
            # We only generate the minimum amount of tokens so that our grammar is correct.
            # Any excessive tokens are not produced by this logic
            # FIXME is this desired?
            for i in range(0, expr.min):
                yield from gen_hook_stmt(expr.expr)
        elif isinstance(expr, MageCharSetExpr):
            # We assume this CharSetExpr has been reduced to its most canonical form.
            # In other words, we assume this expression has at least 2 different characters.
            # This means we cannot 'choose' the right character, so do nothing.
            # FIXME is this desired?
            pass
        elif isinstance(expr, MageChoiceExpr):
            # We cannot decide what rule we should take without additional
            # information, so do nothing.
            # FIXME is this desired?
            pass
        elif isinstance(expr, MageLitExpr):
            yield gen_write(PyConstExpr(expr.text))
        elif isinstance(expr, MageLookaheadExpr):
            # A lookahead expression never parses/emits anything.
            pass
        else:
            assert_never(expr)

    def gen_emit_stmt(expr: MageExpr, target: PyExpr) -> Iterable[PyStmt]:
        nonlocal prev_target
        # NOTE This logic must be in sync with infer_type() in magelang.treespec
        if isinstance(expr, MageLitExpr):
            yield gen_write(PyConstExpr(expr.text))
        elif isinstance(expr, MageRepeatExpr):
            if expr.min == 0 and expr.max == 1:
                yield PyIfStmt(first=PyIfCase(
                    test=PyInfixExpr(target, (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                    body=list(gen_emit_stmt(expr.expr, target))
                ))
                return
            element_name = 'element'
            yield PyForStmt(pattern=PyNamedPattern(element_name), expr=target, body=list(gen_emit_stmt(expr.expr, PyNamedExpr(element_name))))
        elif isinstance(expr, MageCharSetExpr):
            yield gen_write(PyCallExpr(PyNamedExpr(emit_token_fn_name), args=[ target ]))
        elif isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None:
                pass
            elif rule.is_extern:
                yield from gen_write_token(target)
            elif rule.expr is None:
                pass
            elif not rule.is_public:
                yield from gen_emit_stmt(rule.expr, target)
            elif grammar.is_token_rule(rule):
                yield from gen_write_token(target)
            else:
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
            cases: list[PyCondCase] = []
            for element in expr.elements:
                body = list(gen_emit_stmt(element, target))
                if body:
                    cases.append((
                        treespec_type_to_shallow_py_test(infer_type(element, grammar), target, prefix=prefix, specs=specs),
                        body
                    ))
            yield from make_py_cond(cases)
        elif isinstance(expr, MageLookaheadExpr):
            # A lookahead expression never parses/emits anything.
            pass
        elif isinstance(expr, MageHideExpr):
            yield from gen_hook_stmt(expr.expr)
        elif isinstance(expr, MageSeqExpr):
            tuple_len = len(list(filter(lambda element: not is_empty(element), expr.elements)))
            tuple_index = 0
            for i, element in enumerate(expr.elements):
                yield from gen_emit_stmt(element, target if tuple_len == 1 else PySubscriptExpr(target, [ PyConstExpr(tuple_index) ]))
                if not is_empty(element):
                    tuple_index += 1
        elif isinstance(expr, MageListExpr):
            yield PyIfStmt(
                PyIfCase(target, [
                    PyForStmt(
                        PyTuplePattern(elements=[ PyNamedPattern('el'), PyNamedPattern('sep') ]),
                        target,
                        [
                            *gen_emit_stmt(expr.element, PyNamedExpr('el')),
                            PyIfStmt(PyIfCase(
                                test=PyInfixExpr(PyNamedExpr('sep'), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                                body=list(gen_emit_stmt(expr.separator, PyNamedExpr('sep'))),
                            )),
                        ]
                    ),
                ]),
            )
        else:
            assert_never(expr)
        prev_target = target

    emit_token_body = []

    visit_node_body: list[PyStmt] = [
        PyNonlocalStmt([ out_name, 'prev_token' ]),
        PyAssignStmt(PyNamedPattern('ctx'), value=PyCallExpr(PyNamedExpr('create_context'))),
    ]

    for rule in grammar.rules:

        if rule.is_lex:
            if rule.expr is None:
                # TODO cover this case by invoking an external API
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

        elif grammar.is_variant_rule(rule) or not rule.is_public:
           pass

        elif rule.is_parse:
            assert(rule.expr is not None)
            if_body = list[PyStmt]()
            for expr, field in get_fields(rule.expr, grammar=grammar):
                if field is not None:
                    if_body.extend(gen_emit_stmt(expr, PyAttrExpr(PyNamedExpr(param_name), field.name)))
                else:
                    if_body.extend(gen_hook_stmt(expr))
            if_body.append(PyRetStmt())
            visit_node_body.append(PyIfStmt(first=PyIfCase(
                test=make_py_isinstance(PyNamedExpr(param_name), PyNamedExpr(to_py_class_name(rule.name, prefix))),
                body=if_body
            )))

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
        PyImportFromStmt(
            PyRelativePath(dots=1, name='emit_hooks'),
            [ PyFromAlias('create_context'), *(PyFromAlias(name) for name in hook_names) ],
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
                PyAssignStmt(PyNamedPattern('prev_token'), value=PyNamedExpr('None')),
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

