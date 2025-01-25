
from magelang.helpers import PyCondCase, get_field_name, get_fields, infer_type, make_py_cond, make_py_or, make_py_union, to_py_class_name
from magelang.lang.mage.ast import *
from magelang.lang.python.cst import *
from magelang.lang.mage.constants import string_rule_type, builtin_types
from magelang.analysis import is_eof, is_tokenizable
from magelang.lang.treespec.ast import ExternType, Field, Type
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


def _is_stmt_terminal(stmt: PyStmt, in_loop: bool) -> bool:
    """
    A heuristic implementation that checks whether a statement exits the current function.

    This function will give a false negative when having a `raise` inside a try/catch-statement.
    """
    if isinstance(stmt, PyIfStmt):
        return all(_is_terminal(body, in_loop) for test, body in _to_py_cond_cases(stmt))
    if isinstance(stmt, PyRetStmt):
        return True
    if isinstance(stmt, PyRaiseStmt):
        return True
    if isinstance(stmt, PyTryStmt):
        return False
    if isinstance(stmt, PyBreakStmt):
        return not in_loop
    if isinstance(stmt, PyPassStmt) \
            or isinstance(stmt, PyFuncDef) \
            or isinstance(stmt, PyAssignStmt) \
            or isinstance(stmt, PyAugAssignStmt) \
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
        return _is_terminal(stmt.body, True)
    assert_never(stmt)

def _is_terminal(body: PyStmt | Sequence[PyStmt], in_loop: bool) -> bool:
    if is_py_stmt(body):
        body = [ body ]
    return any(_is_stmt_terminal(element, in_loop) for element in body)

def mage_to_python_parser(grammar: MageGrammar, prefix: str) -> PyModule:

    enable_tokens = is_tokenizable(grammar)
    buffer_name = 'buffer'

    if not enable_tokens:
        print('Warning: grammar could not be tokenized. We will fall back to a more generic algorithm.')

    stmts = list[PyStmt]()

    stmts.append(PyImportFromStmt(
        PyAbsolutePath(PyQualName(modules=[ 'magelang' ], name='runtime')),
        [ PyFromAlias('AbstractParser'), PyFromAlias('Punctuated'), PyFromAlias('CharStream'), PyFromAlias('EOF') ]
    ))
    stmts.append(PyImportFromStmt(
        PyRelativePath(1, name='cst'),
        [ PyAsterisk() ]
    ))

    def get_parse_method_name(rule: MageRule) -> str:
         return f'parse_{rule.name}'

    def make_init(ty: Type) -> PyExpr:
        if isinstance(ty, ExternType):
            if ty.name == string_rule_type:
                return PyConstExpr('')
            elif ty.name not in builtin_types:
                return PyCallExpr(PyNamedExpr(ty.name))
        return PyListExpr()

    def make_append(ty: Type, target: str, value: PyExpr) -> PyStmt:
        if isinstance(ty, ExternType):
            if ty.name == string_rule_type:
                return PyAugAssignStmt(PyNamedPattern(target), PyPlus(), value)
        return PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(target), 'append'), args=[ value ]))

    noop: list[PyStmt] = []

    def gen_parse_body(rule: MageRule) -> Generator[PyStmt]:

        is_token = grammar.is_token_rule(rule)

        generate_name = NameGenerator()
        generate_name('stream') # Mark function parameter as being in use
        generate_name('buffer') # Mark buffer as being in use
        generate_name('c') # Start counting from 0

        def visit_prim_field_internals(expr: MageExpr, stream_name: str, target_name: str, accept: list[PyStmt], reject: list[PyStmt], invert: bool) -> Generator[PyStmt]:
            """
            Generate parse logic for a single expression.

            It is assumed that the code generated in either `accept` or `reject` eventually terminates control flow, either by returning of by throwing an exception.

            Setting `invert` to `True` makes `reject` be the main control flow and `accept` a terminating edge case.
            """

            def gen_accept_reject(test: PyExpr, accept: list[PyStmt], reject: list[PyStmt], test_negated: bool) -> Generator[PyStmt]:
                accept_terminates = _is_terminal(accept, False)
                reject_terminates = _is_terminal(reject, False)
                if invert:
                    cases: list[PyCondCase] = [
                        (PyPrefixExpr(PyNotKeyword(), test) if test_negated else test, accept),
                    ]
                    if not accept_terminates and reject:
                        cases.append((None, reject))
                    yield from make_py_cond(cases)
                    if accept_terminates:
                        yield from reject
                else:
                    cases: list[PyCondCase] = [
                        (test if test_negated else PyPrefixExpr(PyNotKeyword(), test), reject),
                    ]
                    if not reject_terminates and accept:
                        cases.append((None, accept))
                    yield from make_py_cond(cases)
                    if reject_terminates:
                        yield from accept

            if is_eof(expr):
                temp = generate_name('c')
                if invert:
                    yield PyAssignStmt(PyNamedPattern(temp), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                    yield PyIfStmt(PyIfCase(test=PyInfixExpr(PyNamedExpr(temp), PyEqualsEquals(), PyNamedExpr('EOF')), body=[
                        *accept
                    ]))
                    yield from reject
                else:
                    temp = generate_name('c')
                    yield PyAssignStmt(PyNamedPattern(temp), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                    yield PyIfStmt(PyIfCase(test=PyInfixExpr(PyNamedExpr(temp), PyExclamationMarkEquals(), PyNamedExpr('EOF')), body=reject))
                    yield from accept

            elif isinstance(expr, MageLitExpr):
                if invert:
                    head = reject
                    for ch in reversed(expr.text):
                        head = [
                            PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek'))),
                            PyIfStmt(PyIfCase(test=PyInfixExpr(PyNamedExpr(target_name), PyEqualsEquals(), PyConstExpr(ch)), body=[
                                PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))),
                                *accept
                            ]))
                        ]
                    yield from head
                else:
                    for ch in expr.text:
                        yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                        yield PyIfStmt(PyIfCase(test=PyInfixExpr(PyNamedExpr(target_name), PyExclamationMarkEquals(), PyConstExpr(ch)), body=reject))
                        yield PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get')))
                    yield from accept

            elif isinstance(expr, MageCharSetExpr):
                tests = []
                yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                for element in expr.elements:
                    if isinstance(element, tuple):
                        low, high = element
                        tests.append(PyInfixExpr(
                            PyInfixExpr(PyNamedExpr(target_name), PyGreaterThanEquals(), PyConstExpr(low)),
                            PyAndKeyword(),
                            PyInfixExpr(PyNamedExpr(target_name), PyLessThanEquals(), PyConstExpr(high)),
                        ))
                    else:
                        tests.append(PyInfixExpr(PyNamedExpr(target_name), PyEqualsEquals(), PyConstExpr(element)))
                test = make_py_or(tests)
                if not invert:
                    test = PyPrefixExpr(PyNotKeyword(), test)
                if_body = accept if invert else reject
                accept.insert(0, PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))))
                yield PyIfStmt(PyIfCase(test=test, body=if_body))
                yield from reject if invert else accept

            elif isinstance(expr, MageSeqExpr):
                unreachable()

            elif isinstance(expr, MageRefExpr):

                assert(expr.symbol is not None)

                rule = cast(MageRule, expr.symbol.definition)

                if rule.expr is None:
                    yield from accept
                    return # TODO figure out what generic logic to yield

                if not rule.is_public:
                    yield from visit_field_internals(rule.expr, stream_name, target_name, accept, reject, invert)
                    return

                if grammar.is_parse_rule(rule):
                    method_name = get_parse_method_name(rule)
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr('self'), method_name), args=[ PyNamedExpr(stream_name) ]))
                    yield from gen_accept_reject(
                        PyInfixExpr(PyNamedExpr(target_name), PyIsKeyword(), PyNamedExpr('None')),
                        accept,
                        reject,
                        True
                    )
                    return

                # elif grammar.is_variant_rule(rule):
                #     if all_tokens(rule.expr):
                #         yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                #         yield from gen_assert(
                #             PyCallExpr(PyNamedExpr(f'is_{namespaced(target_name, prefix=prefix)}') , args=[ PyNamedExpr(target_name) ]),
                #             [ PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))) ] + accept,
                #             reject
                #         )

                assert(grammar.is_token_rule(rule))

                if enable_tokens:
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                    yield from gen_accept_reject(
                        PyCallExpr(PyNamedExpr('isinstance'), args=[ PyNamedExpr(target_name), PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)) ]),
                        [ PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))) ] + accept,
                        reject,
                        False
                    )
                else:
                    method_name = get_parse_method_name(rule)
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr('self'), method_name), args=[ PyNamedExpr(stream_name) ]))
                    yield from gen_accept_reject(
                        PyInfixExpr(PyNamedExpr(target_name), PyIsKeyword(), PyNamedExpr('None')),
                        accept,
                        reject,
                        True
                    )
                    return
                    #yield from visit_field_inner(rule.expr, stream_name, target_name, accept, reject, invert)

            elif isinstance(expr, MageChoiceExpr):

                new_stream_name = generate_name('stream')

                head = []
                match_name = generate_name('match')
                yield PyAssignStmt(PyNamedPattern(match_name), value=PyConstExpr(False))
                for element in reversed(expr.elements):
                    new_accept = [
                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])),
                        PyAssignStmt(PyNamedPattern(match_name), value=PyConstExpr(True)),
                    ]
                    head = list(visit_field_internals(element, new_stream_name, target_name, new_accept, head, not invert))
                    head.insert(0, PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))))
                yield from head
                yield from gen_accept_reject(PyNamedExpr(match_name), accept, reject, False)

                # head = reject
                # for element in reversed(expr.elements):
                #     new_accept = [
                #         PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])),
                #         *accept,
                #     ]
                #     head = list(visit_field_internals(element, new_stream_name, target_name, new_accept, head, not invert))
                #     head.insert(0, PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))))
                # yield from head

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
                    yield from visit_field_internals(expr.expr, new_stream_name, temp_name, new_accept, noop, not invert)
                    yield from accept
                    return

                element_name = generate_name(prefix=f'{target_name}_element')
                ty = infer_type(expr.expr, grammar=grammar)

                yield PyAssignStmt(PyNamedPattern(target_name), value=make_init(ty))

                min_to_max = []
                if expr.max > expr.min:
                    if expr.max == POSINF:
                        new_stream_name = generate_name('stream')
                        min_to_max.append(PyWhileStmt(
                            PyConstExpr(True),
                            [
                                PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))),
                                *visit_field_internals(
                                    expr.expr,
                                    new_stream_name,
                                    element_name,
                                    [
                                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])),
                                        make_append(ty, target_name, PyNamedExpr(element_name)),
                                    ],
                                    [
                                        PyBreakStmt()
                                    ],
                                    invert
                                ),
                            ]
                        ))
                    else: # expr.max == expr.min
                        new_stream_name = generate_name('stream')
                        min_to_max.append(PyForStmt(
                            PyNamedPattern('_'),
                            PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.min) ]),
                            body=[
                                PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))),
                                *visit_field_internals(
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
                                make_append(ty, target_name, PyNamedExpr(element_name)),
                            ]
                        ))

                def gen_body():
                    new_accept = min_to_max
                    new_accept.insert(0, make_append(ty, target_name, PyNamedExpr(element_name)))
                    yield from visit_field_internals(expr.expr, stream_name, element_name, new_accept, reject, False)

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
                yield from visit_field_internals(expr.expr, stream_name, target_name, accept, reject, invert)

            elif isinstance(expr, MageListExpr):

                # TODO process expr.min_count

                yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyNamedExpr('Punctuated')))

                element_name = generate_name(prefix=f'{target_name}_element')
                separator_name = generate_name(prefix=f'{target_name}_separator')

                yield PyWhileStmt(
                    PyConstExpr(True),
                    [
                        *visit_field_internals(
                            expr.element,
                            stream_name,
                            element_name,
                            list(visit_field_internals(
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
                    yield from visit_field_internals(expr.expr, stream_name, target_name, reject, accept, not invert)
                else:
                    yield from visit_field_internals(expr.expr, stream_name, target_name, accept, reject, invert)

            else:
                assert_never(expr)

        def visit_field_internals(expr: MageExpr, stream_name: str, target_name: str, accept: list[PyStmt], reject: list[PyStmt], invert: bool) -> Generator[PyStmt]:
            if isinstance(expr, MageSeqExpr):
                indices = list[int]()
                n = len(expr.elements)
                for i, element in enumerate(expr.elements):
                    if not isinstance(element, MageHideExpr):
                        indices.append(i)
                if len(indices) == 1:
                    # Tuple only contains one value; extract it
                    value = PyNamedExpr(f'{target_name}_tuple_{indices[0]}')
                else:
                    # Tuple contains many elements
                    value = PyTupleExpr(elements=list(PyNamedExpr(f'{target_name}_{i}') for i in indices))
                head: list[PyStmt] = [ PyAssignStmt(PyNamedPattern(target_name), value=value) ] + accept
                for i, element in enumerate(reversed(expr.elements)):
                    if isinstance(element, MageHideExpr):
                        element_name = generate_name('unused')
                    else:
                        element_name = f'{target_name}_tuple_{n - i - 1}'
                    head = list(visit_field_internals(element, stream_name, element_name, head, reject, invert))
                yield from head
            else:
                yield from visit_prim_field_internals(expr, stream_name, target_name, accept, reject, invert)

        def visit_field(expr: MageExpr, stream_name: str, accept: list[PyStmt], reject: list[PyStmt]) -> Generator[PyStmt]:
            field_name = generate_name('temp') if is_token else expr.field_name
            assert(field_name is not None)
            if is_token:
                accept = [ PyAugAssignStmt(PyNamedPattern(buffer_name), PyPlus(), PyNamedExpr(field_name)), *accept ]
            yield from visit_field_internals(expr, stream_name, field_name, accept, reject, False)

        def visit_fields(expr: MageExpr, stream_name: str, accept: list[PyStmt], reject: list[PyStmt]) -> Generator[PyStmt]:
            if isinstance(expr, MageSeqExpr):
                head = accept
                for element in reversed(expr.elements):
                    if isinstance(element, MageSeqExpr):
                        head = list(visit_fields(element, stream_name, head, reject))
                    else:
                        head = list(visit_field(element, stream_name, head, reject))
                yield from head
            else:
                yield from visit_field(expr, stream_name, accept, reject)

        if grammar.is_variant_rule(rule):
            # FIXME does not do lookaheads
            yield from visit_field_internals(
                nonnull(rule.expr),
                'stream',
                'result',
                [ PyRetStmt(expr=PyNamedExpr('result')) ],
                [ PyRetStmt() ],
                False
            )
            return

        if is_token:
            yield PyAssignStmt(PyNamedPattern(buffer_name), value=PyConstExpr(''))
            args = []
            if not grammar.is_static_token_rule(rule):
                args.append(PyNamedExpr(buffer_name))
            yield from visit_fields(nonnull(rule.expr), 'stream', [ PyRetStmt(expr=PyCallExpr(PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)), args=args)) ], [ PyRetStmt() ])
            return

        fields = list(field for field in get_fields(nonnull(rule.expr), grammar=grammar) if isinstance(field, Field))
        return_struct: list[PyStmt] = [
            PyRetStmt(
                expr=PyCallExpr(
                    PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)),
                    args=list(PyKeywordArg(field.name, PyNamedExpr(field.name)) for field in fields)
                )
            )
        ]

        yield from visit_fields(nonnull(rule.expr), 'stream', return_struct, [ PyRetStmt() ])

    parser_body = []
    for element in grammar.elements:
        if grammar.is_parse_rule(element) or (not enable_tokens and grammar.is_token_rule(element)):
            parser_body.append(PyFuncDef(
                name=f'parse_{element.name}',
                params=[ PyNamedParam(PyNamedPattern('self')), PyNamedParam(PyNamedPattern('stream'), annotation=PyNamedExpr('ParseStream' if enable_tokens else 'CharStream')) ],
                return_type=make_py_union([
                    PyNamedExpr(to_py_class_name(element.name, prefix=prefix)),
                    PyNamedExpr('None'),
                ]),
                body=list(gen_parse_body(element))
            ))

    stmts.append(PyClassDef(
        name=to_py_class_name('parser', prefix),
        bases=[ PyClassBaseArg('AbstractParser') ],
        body=parser_body,
    ))


    return PyModule(stmts=stmts)
