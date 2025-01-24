
import functools
from magelang.helpers import PyCondCase, get_field_name, make_py_cond, make_py_union, namespaced, to_py_class_name
from magelang.lang.mage.ast import *
from magelang.lang.python.cst import *
from magelang.logging import warn
from magelang.util import NameGenerator, unreachable

# FIXME every expr may only peek or fork so that when there is an error, the stream can correctly be skipped
# def ; def foo(): bar <- if ';' is consumed during parsing error we skip too many tokens

type AcceptFn = Callable[[], Generator[PyStmt]]
type RejectFn = Callable[[], Generator[PyStmt]]


def _lift_body(body: PyStmt | list[PyStmt]) -> list[PyStmt]:
    return body if isinstance(body, list) else [ body ]


def _to_py_cond_cases(stmt: PyIfStmt) -> list[PyCondCase]:
    cases = list[PyCondCase]()
    cases.append((stmt.first.test, _lift_body(stmt.first.body)))
    for alt in stmt.alternatives:
        cases.append((alt.test, _lift_body(alt.body)))
    if stmt.last:
        cases.append((None, _lift_body(stmt.last.body)))
    return cases


def _is_stmt_terminal(stmt: PyStmt) -> bool:
    """
    A heuristic implementation that checks whether a statement exits the current function.

    This function will give a false negative when having a `raise` inside ` try/catch-statement.
    """
    if isinstance(stmt, PyIfStmt):
        return all(_is_terminal(body) for test, body in _to_py_cond_cases(stmt))
    if isinstance(stmt, PyRetStmt):
        return True
    if isinstance(stmt, PyRaiseStmt):
        return True
    if isinstance(stmt, PyTryStmt):
        return False
    if isinstance(stmt, PyPassStmt) \
            or isinstance(stmt, PyFuncDef) \
            or isinstance(stmt, PyAssignStmt) \
            or isinstance(stmt, PyAugAssignStmt) \
            or isinstance(stmt, PyBreakStmt) \
            or isinstance(stmt, PyContinueStmt) \
            or isinstance(stmt, PyDeleteStmt) \
            or isinstance(stmt, PyExprStmt) \
            or isinstance(stmt, PyGlobalStmt) \
            or isinstance(stmt, PyNonlocalStmt) \
            or isinstance(stmt, PyImportStmt) \
            or isinstance(stmt, PyImportFromStmt) \
            or isinstance(stmt, PyTypeAliasStmt) \
            or isinstance(stmt, PyClassDef):
        return False
    if isinstance(stmt, PyWhileStmt) or isinstance(stmt, PyForStmt):
        return _is_terminal(stmt.body)
    assert_never(stmt)

def _is_terminal(body: PyStmt | Sequence[PyStmt]) -> bool:
    if is_py_stmt(body):
        body = [ body ]
    return any(_is_stmt_terminal(element) for element in body)

def mage_to_python_parser(grammar: MageGrammar, prefix: str) -> PyModule:

    stmts = list[PyStmt]()

    stmts.append(PyImportFromStmt(
        PyAbsolutePath(PyQualName(modules=[ 'magelang' ], name='runtime')),
        [ PyFromAlias('BaseParser'), PyFromAlias('Punctuated') ]
    ))

    def get_parse_method_name(rule: MageRule) -> str:
         return f'parse_{rule.name}'

    noop: list[PyStmt] = []

    def gen_parse_body(rule: MageRule) -> list[PyStmt]:

        generate_name = NameGenerator()
        generate_name('stream') # Mark function parameter as being in use

        fields = list[str]()

        def visit_prim_field_inner(expr: MageExpr, stream_name: str, target_name: str, accept: list[PyStmt], reject: list[PyStmt], invert: bool) -> Generator[PyStmt]:
            """
            Generate parse logic for a single expression.

            It is assumed that the code generated in `accept` and `reject` eventually terminates control flow, either by returning of by throwing an exception.

            Setting `invert` to `True` makes `reject` be the main control flow and `accept` an edge case.
            """

            if isinstance(expr, MageLitExpr):
                unreachable()

            elif isinstance(expr, MageCharSetExpr):
                unreachable()

            elif isinstance(expr, MageSeqExpr):
                unreachable()

            elif isinstance(expr, MageRefExpr):

                assert(expr.symbol is not None)

                rule = cast(MageRule, expr.symbol.definition)

                accept_terminates = _is_terminal(accept)
                reject_terminates = _is_terminal(reject)

                def gen_assert(test: PyExpr, accept: list[PyStmt], reject: list[PyStmt]) -> Generator[PyStmt]:
                    if invert:
                        cases: list[PyCondCase] = [
                            (test, accept),
                        ]
                        print(reject)
                        if not accept_terminates and reject:
                            cases.append((None, reject))
                        yield from make_py_cond(cases)
                        if accept_terminates:
                            yield from reject
                    else:
                        cases: list[PyCondCase] = [
                            (PyPrefixExpr(PyNotKeyword(), test), reject),
                        ]
                        if not reject_terminates and accept:
                            cases.append((None, accept))
                        yield from make_py_cond(cases)
                        if reject_terminates:
                            yield from accept

                if rule.expr is None:
                    yield from accept
                    return # TODO figure out what to yield

                elif not rule.is_public:
                    yield from visit_field_inner(rule.expr, stream_name, target_name, accept, reject, invert)

                # elif grammar.is_variant_rule(rule):
                #     if all_tokens(rule.expr):
                #         yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                #         yield from gen_assert(
                #             PyCallExpr(PyNamedExpr(f'is_{namespaced(target_name, prefix=prefix)}') , args=[ PyNamedExpr(target_name) ]),
                #             [ PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))) ] + accept,
                #             reject
                #         )

                elif grammar.is_parse_rule(rule):
                    method_name = get_parse_method_name(rule)
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr('self'), method_name), args=[ PyNamedExpr(stream_name) ]))
                    yield from gen_assert(
                        PyInfixExpr(PyNamedExpr(target_name), (PyIsKeyword(), PyNotKeyword()), PyNamedExpr('None')),
                        accept,
                        reject
                    )

                elif grammar.is_token_rule(rule):
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                    yield from gen_assert(
                        PyCallExpr(PyNamedExpr('isinstance'), args=[ PyNamedExpr(target_name), PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)) ]),
                        [ PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))) ] + accept,
                        reject
                    )

                else:
                    unreachable()

            elif isinstance(expr, MageChoiceExpr):
                head = reject
                for element in reversed(expr.elements):
                    new_stream_name = generate_name('stream')
                    new_accept = list(accept)
                    new_accept.insert(0, PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])))
                    head = list(visit_field_inner(element, new_stream_name, target_name, new_accept, head, True))
                    head.insert(0, PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))))
                yield from head

            elif isinstance(expr, MageRepeatExpr):

                if expr.min == 0 and expr.max == 1:

                    # Optimisation
                    # if grammar.is_token_rule(expr.expr):
                    #     # TODO
                    #     return

                    new_stream_name = generate_name('stream')
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyNamedExpr('None'))
                    yield PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork')))
                    temp_name = generate_name('temp')
                    new_accept = [
                        PyAssignStmt(PyNamedPattern(target_name), value=PyNamedExpr(temp_name)),
                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])),
                    ]
                    yield from visit_field_inner(expr.expr, new_stream_name, temp_name, new_accept, noop, not invert)
                    yield from accept
                    return

                #elements_name = generate_field_name(prefix=f'{target_name}_elements')
                element_name = generate_name(prefix=f'{target_name}_element')

                yield PyAssignStmt(PyNamedPattern(target_name), value=PyListExpr())

                min_to_max = []
                if expr.max > expr.min:
                    if expr.max == POSINF:
                        new_stream_name = generate_name('stream')
                        min_to_max.append(PyWhileStmt(
                            PyConstExpr(True),
                            [
                                PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))),
                                *visit_field_inner(
                                    expr.expr,
                                    new_stream_name,
                                    element_name,
                                    [
                                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ]))
                                    ],
                                    [
                                        PyBreakStmt()
                                    ],
                                    False
                                ),
                                PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(target_name), 'append'), args=[ PyNamedExpr(element_name) ]))
                            ]
                        ))
                    else: # expr.max == expr.min
                        new_stream_name = generate_name('stream')
                        min_to_max.append(PyForStmt(
                            PyNamedPattern('_'),
                            PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.min) ]),
                            body=[
                                PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))),
                                *visit_field_inner(
                                    expr.expr,
                                    new_stream_name,
                                    element_name,
                                    [
                                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ]))
                                    ],
                                    [
                                        PyBreakStmt()
                                    ],
                                    False
                                ),
                                PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(target_name), 'append'), args=[ PyNamedExpr(element_name) ]))
                            ]
                        ))

                def gen_body():
                    new_accept = min_to_max
                    new_accept.append(PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(target_name), 'append'), args=[ PyNamedExpr(element_name) ])))
                    yield from visit_field_inner(expr.expr, stream_name, element_name, new_accept, reject, False)

                if expr.min == 0:
                    yield from min_to_max

                elif expr.min == 1:
                    yield from gen_body()

                else:
                    yield PyForStmt(
                        PyNamedPattern('_'),
                        PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.min) ]),
                        body=list(gen_body())
                    )

                yield from accept

            elif isinstance(expr, MageHideExpr):
                yield from visit_field_inner(expr.expr, stream_name, target_name, accept, reject, invert)

            elif isinstance(expr, MageListExpr):

                # TODO process expr.min_count

                yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyNamedExpr('Punctuated')))

                element_name = generate_name(prefix=f'{target_name}_element')
                separator_name = generate_name(prefix=f'{target_name}_separator')

                yield PyWhileStmt(
                    PyConstExpr(True),
                    [
                        *visit_field_inner(
                            expr.element,
                            stream_name,
                            element_name,
                            list(visit_field_inner(
                                expr.separator,
                                stream_name,
                                separator_name,
                                [
                                    PyExprStmt(
                                        PyCallExpr(
                                            PyAttrExpr(PyNamedExpr(element_name), 'append'),
                                            args=[ PyNamedExpr(element_name), PyNamedExpr(separator_name) ]
                                        )
                                    )
                                ],
                                reject,
                                invert
                            )),
                            [ PyBreakStmt() ],
                            invert
                        ),
                    ]
                )

                yield from accept

            elif isinstance(expr, MageLookaheadExpr):
                if expr.is_negated:
                    yield from visit_field_inner(expr.expr, stream_name, target_name, reject, accept, invert)
                else:
                    yield from visit_field_inner(expr.expr, stream_name, target_name, accept, reject, invert)

            else:
                assert_never(expr)

        def visit_field_inner(expr: MageExpr, stream_name: str, target_name: str, accept: list[PyStmt], reject: list[PyStmt], invert: bool) -> Generator[PyStmt]:
            if isinstance(expr, MageSeqExpr):
                indices = list[int]()
                n = len(expr.elements)
                for i, element in enumerate(expr.elements):
                    if not isinstance(element, MageHideExpr):
                        indices.append(i)
                if len(indices) == 1:
                    # Tuple only contains one value
                    value = PyNamedExpr(f'{target_name}_{indices[0]}')
                else:
                    # Tuple contains many elements
                    value = PyTupleExpr(elements=list(PyNamedExpr(f'{target_name}_{i}') for i in indices))
                head: list[PyStmt]
                head = [ PyAssignStmt(PyNamedPattern(target_name), value=value) ] + accept
                for i, element in enumerate(reversed(expr.elements)):
                    if isinstance(element, MageHideExpr):
                        element_name = generate_name('unused')
                    else:
                        element_name = f'{target_name}_{n - i}'
                    head = list(visit_field_inner(element, stream_name, element_name, head, reject, invert))
                yield from head
            else:
                yield from visit_prim_field_inner(expr, stream_name, target_name, accept, reject, invert)

        def visit_fields(expr: MageExpr, stream_name: str, accept: list[PyStmt], reject: list[PyStmt]) -> Generator[PyStmt]:

            if isinstance(expr, MageSeqExpr):
                head = accept
                for element in reversed(expr.elements):
                    if isinstance(element, MageSeqExpr):
                        head = list(visit_fields(element, stream_name, head, reject))
                        return
                    field_name = get_field_name(element)
                    assert(field_name is not None) # FIXME generate a field name instead
                    fields.append(field_name)
                    head = list(visit_field_inner(element, stream_name, field_name, head, reject, False))
                yield from head

            else:
                field_name = get_field_name(expr)
                assert(field_name is not None) # FIXME generate a field name instead
                fields.append(field_name)
                yield from visit_prim_field_inner(expr, stream_name, field_name, accept, reject, False)

        if grammar.is_variant_rule(rule):
            def c_return_result() -> Generator[PyStmt]:
                yield PyRetStmt(expr=PyNamedExpr('result'))
            return list(visit_field_inner(
                nonnull(rule.expr),
                'stream',
                'result',
                [ PyRetStmt(expr=PyNamedExpr('result')) ],
                [ PyRetStmt() ],
                False
            ))

        return_struct: list[PyStmt] = [
            # FIXME analyse `fields` up front
            PyRetStmt(
                expr=PyCallExpr(
                    PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)),
                    args=list(PyKeywordArg(name, PyNamedExpr(name)) for name in fields)
                )
            )
        ]

        return list(visit_fields(nonnull(rule.expr), 'stream', return_struct, [ PyRetStmt() ]))

    parser_body = []

    for element in grammar.elements:
        if grammar.is_parse_rule(element):
            parser_body.append(PyFuncDef(
                name=f'parse_{element.name}',
                params=[ PyNamedParam(PyNamedPattern('self')), PyNamedParam(PyNamedPattern('stream'), annotation=PyNamedExpr('ParseStream')) ],
                return_type=make_py_union([
                    PyNamedExpr(to_py_class_name(element.name, prefix=prefix)),
                    PyNamedExpr('None'),
                ]),
                body=gen_parse_body(element)
            ))

    stmts.append(PyClassDef(
        name=to_py_class_name('parser', prefix),
        bases=[ PyClassBaseArg('BaseParser') ],
        body=parser_body,
    ))

    return PyModule(stmts=stmts)
