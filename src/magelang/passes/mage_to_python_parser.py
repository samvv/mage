
from magelang.helpers import PyCondCase, get_fields, infer_type, make_py_cond, make_py_or, make_py_union, to_py_class_name
from magelang.lang.mage.ast import *
from magelang.lang.python.cst import *
from magelang.lang.mage.constants import string_rule_type, builtin_types
from magelang.analysis import is_eof, is_tokenizable
from magelang.lang.treespec.ast import ExternType, Field, Type
from magelang.util import NameGenerator, unreachable

# FIXME every expr may only peek or fork so that when there is an error, the stream can correctly be skipped
# def ; def foo(): bar <- if ';' is consumed during parsing error we skip too many tokens

type AcceptFn = Callable[[], Generator[PyStmt]]
type RejectFn = Callable[[], Generator[PyStmt]]

MAX_LINES_DUPLICATE = 1

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


def count_stmt_lines(stmt: PyStmt) -> int:
    if isinstance(stmt, PyIfStmt):
        out = 1 + count_lines(stmt.first.body) + sum(1 + count_lines(alt.body) for alt in stmt.alternatives)
        if stmt.last is not None:
            out += 1 + count_lines(stmt.last.body)
        return out
    if isinstance(stmt, PyTryStmt):
        return 1 + count_lines(stmt.body) + sum(1 + count_lines(handler.body) for handler in stmt.handlers)
    if isinstance(stmt, PyContinueStmt) \
            or isinstance(stmt, PyRaiseStmt) \
            or isinstance(stmt, PyRetStmt) \
            or isinstance(stmt, PyBreakStmt) \
            or isinstance(stmt, PyPassStmt) \
            or isinstance(stmt, PyAssignStmt) \
            or isinstance(stmt, PyAugAssignStmt) \
            or isinstance(stmt, PyContinueStmt) \
            or isinstance(stmt, PyDeleteStmt) \
            or isinstance(stmt, PyExprStmt) \
            or isinstance(stmt, PyGlobalStmt) \
            or isinstance(stmt, PyNonlocalStmt) \
            or isinstance(stmt, PyImportStmt) \
            or isinstance(stmt, PyImportFromStmt) \
            or isinstance(stmt, PyTypeAliasStmt):
        return 1
    if isinstance(stmt, PyForStmt) or isinstance(stmt, PyWhileStmt):
        return 1 + count_lines(stmt.body)
    if isinstance(stmt, PyFuncDef):
        return 1 + count_lines(stmt.body)
    assert_never(stmt)


def count_lines(body: PyStmt | Sequence[PyStmt]) -> int:
    if is_py_stmt(body):
        body = [ body ]
    return sum(count_stmt_lines(stmt) for stmt in body)


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

def _is_stmt_noop(stmt: PyStmt) -> bool:
    """
    Returns `True` if the statement is guaranteed to have no side-effects.
    """
    if isinstance(stmt, PyIfStmt):
        return all(_is_noop(body) for test, body in _to_py_cond_cases(stmt))
    if isinstance(stmt, PyPassStmt):
        return True
    if isinstance(stmt, PyForStmt) or isinstance(stmt, PyWhileStmt):
        return _is_noop(stmt.body)
    if isinstance(stmt, PyTryStmt):
        return _is_noop(stmt.body) and all(_is_noop(handler.body) for handler in stmt.handlers)
    if isinstance(stmt, PyFuncDef):
        return True
    if isinstance(stmt, PyContinueStmt) or isinstance(stmt, PyBreakStmt):
        return False
    if isinstance(stmt, PyRaiseStmt) \
            or isinstance(stmt, PyRetStmt) \
            or isinstance(stmt, PyAssignStmt) \
            or isinstance(stmt, PyAugAssignStmt) \
            or isinstance(stmt, PyDeleteStmt) \
            or isinstance(stmt, PyExprStmt) \
            or isinstance(stmt, PyGlobalStmt) \
            or isinstance(stmt, PyNonlocalStmt) \
            or isinstance(stmt, PyImportStmt) \
            or isinstance(stmt, PyImportFromStmt) \
            or isinstance(stmt, PyTypeAliasStmt) \
            or isinstance(stmt, PyClassDef):
        return False
    assert_never(stmt)

def _is_noop(body: PyStmt | Sequence[PyStmt]) -> bool:
    if is_py_stmt(body):
        body = [ body ]
    return all(_is_stmt_noop(stmt) for stmt in body)

def _is_terminal(body: PyStmt | Sequence[PyStmt], in_loop: bool = True) -> bool:
    if is_py_stmt(body):
        body = [ body ]
    return any(_is_stmt_terminal(element, in_loop) for element in body)

def mage_to_python_parser(
    grammar: MageGrammar,
    prefix: str = '',
    emit_single_file: bool = False,
    silent: bool = False,
) -> PyModule:

    enable_tokens = is_tokenizable(grammar)
    buffer_name = 'buffer'
    stream_type_name = 'ParseStream' if enable_tokens else 'CharStream'

    if not enable_tokens and not silent:
        print('Warning: grammar could not be tokenized. We will fall back to a more generic algorithm.')

    stmts = list[PyStmt]()

    stmts.append(PyImportFromStmt(
        PyAbsolutePath(PyQualName(modules=[ 'magelang' ], name='runtime')),
        [ PyFromAlias('Punctuated'), PyFromAlias(stream_type_name), PyFromAlias('EOF') ]
    ))
    if not emit_single_file:
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

        inside_token = grammar.is_token_rule(rule)

        generate_name = NameGenerator()
        generate_name('stream') # Mark function parameter as being in use
        generate_name('buffer') # Mark buffer as being in use
        generate_name('c') # Start counting from 0

        def visit_prim_field_internals(expr: MageExpr, stream_name: str, target_name: str, accept: list[PyStmt], reject: list[PyStmt]) -> Generator[PyStmt]:
            """
            Generate parse logic for a single expression.
            """

            def gen_if_stmt(test: PyExpr, accept: list[PyStmt], reject: list[PyStmt], test_negated: bool) -> Generator[PyStmt]:
                accept_terminates = _is_terminal(accept)
                reject_terminates = _is_terminal(reject)
                if (accept_terminates and (not reject_terminates or count_lines(accept) < count_lines(reject))) or _is_noop(reject):
                     yield PyIfStmt(PyIfCase(
                        PyPrefixExpr(PyNotKeyword(), test) if test_negated else test,
                        accept,
                     ))
                     yield from reject
                elif reject_terminates or _is_noop(accept):
                    yield PyIfStmt(PyIfCase(
                        test if test_negated else PyPrefixExpr(PyNotKeyword(), test),
                        reject,
                    ))
                    yield from accept
                elif count_lines(reject) < count_lines(accept): # FIXME doesn't count the actual lines
                    yield from make_py_cond([
                        (test if test_negated else PyPrefixExpr(PyNotKeyword(), test), reject),
                        (None, accept),
                    ])
                else:
                    yield from make_py_cond([
                        (PyPrefixExpr(PyNotKeyword(), test) if test_negated else test, accept),
                        (None, reject),
                    ])

            if is_eof(expr):
                temp = generate_name('c')
                yield PyAssignStmt(PyNamedPattern(temp), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                yield from gen_if_stmt(PyInfixExpr(PyNamedExpr(temp), PyEqualsEquals(), PyNamedExpr('EOF')), accept, reject, False)

            elif isinstance(expr, MageLitExpr):
                head = accept
                for ch in reversed(expr.text):
                    head = [
                        PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek'))),
                        *gen_if_stmt(
                            PyInfixExpr(PyNamedExpr(target_name), PyEqualsEquals(), PyConstExpr(ch)), [
                                PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))),
                                *head
                            ],
                            reject,
                            False
                        )
                    ]
                yield from head

            elif isinstance(expr, MageCharSetExpr):
                tests = []
                yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'peek')))
                for element in expr.canonical_elements:
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
                accept.insert(0, PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))))
                yield from gen_if_stmt(test, accept, reject, False)

            elif isinstance(expr, MageSeqExpr):
                unreachable()

            elif isinstance(expr, MageRefExpr):

                rule = lookup_ref(expr)

                if rule is None or rule.expr is None:
                    yield from accept
                    return # TODO figure out what fallback logic to yield

                if not rule.is_public:
                    yield from visit_field_internals(rule.expr, stream_name, target_name, accept, reject)
                    return

                if grammar.is_parse_rule(rule):
                    method_name = get_parse_method_name(rule)
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyNamedExpr(method_name), args=[ PyNamedExpr(stream_name) ]))
                    yield from gen_if_stmt(
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
                    yield from gen_if_stmt(
                        PyCallExpr(PyNamedExpr('isinstance'), args=[ PyNamedExpr(target_name), PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)) ]),
                        [ PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'get'))) ] + accept,
                        reject,
                        False
                    )
                else:
                    method_name = get_parse_method_name(rule)
                    yield PyAssignStmt(PyNamedPattern(target_name), value=PyCallExpr(PyNamedExpr(method_name), args=[ PyNamedExpr(stream_name) ]))
                    yield from gen_if_stmt(
                        PyInfixExpr(PyNamedExpr(target_name), PyIsKeyword(), PyNamedExpr('None')),
                        accept,
                        reject,
                        True
                    )
                    return
                    #yield from visit_field_inner(rule.expr, stream_name, target_name, accept, reject, invert)

            elif isinstance(expr, MageChoiceExpr):

                new_stream_name = generate_name('stream')

                # Optimisation
                # if _is_terminal(accept) and count_lines(accept) < MAX_LINES_DUPLICATE:
                #     head = reject
                #     for element in reversed(expr.elements):
                #         new_accept = [
                #             PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])),
                #             *accept,
                #         ]
                #         head = list(visit_field_internals(element, new_stream_name, target_name, new_accept, head))
                #         head.insert(0, PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))))
                #     yield from head
                #     return

                head = []
                match_name = generate_name('match')
                yield PyAssignStmt(PyNamedPattern(match_name), value=PyConstExpr(False))
                for element in reversed(expr.elements):
                    new_accept = [
                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])),
                        PyAssignStmt(PyNamedPattern(match_name), value=PyConstExpr(True)),
                    ]
                    head = list(visit_field_internals(element, new_stream_name, target_name, new_accept, head))
                    head.insert(0, PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))))
                yield from head
                yield from gen_if_stmt(PyNamedExpr(match_name), accept, reject, False)

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
                    yield from visit_field_internals(expr.expr, new_stream_name, temp_name, new_accept, noop)
                    yield from accept
                    return

                if expr.min == 1 and expr.max == 1:
                    yield from visit_field_internals(expr.expr, stream_name, target_name, accept, reject)
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
                                ),
                            ]
                        ))
                    else:
                        new_stream_name = generate_name('stream')
                        match_name = generate_name('match')
                        min_to_max.append(PyAssignStmt(PyNamedPattern(match_name), value=PyConstExpr(True)))
                        min_to_max.append(PyForStmt(
                            PyNamedPattern('_'),
                            PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(expr.min), PyConstExpr(expr.max) ]),
                            body=[
                                PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork'))),
                                *visit_field_internals(
                                    expr.expr,
                                    new_stream_name,
                                    element_name,
                                    [
                                        PyExprStmt(PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'join_to'), args=[ PyNamedExpr(new_stream_name) ])),
                                    ],
                                    [
                                        PyAssignStmt(PyNamedPattern(match_name), value=PyConstExpr(False)),
                                        PyBreakStmt()
                                    ],
                                ),
                                make_append(ty, target_name, PyNamedExpr(element_name)),
                            ]
                        ))

                min_to_max.extend(accept)

                if expr.min == 0:
                    yield from min_to_max

                elif expr.min == 1:
                    new_accept = [
                        make_append(ty, target_name, PyNamedExpr(element_name)),
                        *min_to_max,
                    ]
                    yield from visit_field_internals(expr.expr, stream_name, element_name, new_accept, reject)

                else:
                    yield PyForStmt(
                        PyNamedPattern('_'),
                        PyCallExpr(PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.min) ]),
                        body=[
                            *visit_field_internals(expr.expr, stream_name, element_name, [ make_append(ty, target_name, PyNamedExpr(element_name)) ], [ *reject, PyRetStmt() ]),
                        ]
                    )
                    yield from min_to_max

            elif isinstance(expr, MageHideExpr):
                new_target_name = generate_name('unused')
                yield from visit_field_internals(expr.expr, stream_name, new_target_name, accept, reject)

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
                            )),
                            [ PyBreakStmt() ],
                        ),
                    ]
                )

                yield from accept

            elif isinstance(expr, MageLookaheadExpr):
                new_stream_name = generate_name('stream')
                yield PyAssignStmt(PyNamedPattern(new_stream_name), value=PyCallExpr(PyAttrExpr(PyNamedExpr(stream_name), 'fork')))
                if expr.is_negated:
                    yield from visit_field_internals(expr.expr, new_stream_name, target_name, reject, accept)
                else:
                    yield from visit_field_internals(expr.expr, new_stream_name, target_name, accept, reject)

            else:
                assert_never(expr)

        def visit_field_internals(expr: MageExpr, stream_name: str, target_name: str, accept: list[PyStmt], reject: list[PyStmt]) -> Generator[PyStmt]:
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
                    head = list(visit_field_internals(element, stream_name, element_name, head, reject))
                yield from head
            else:
                yield from visit_prim_field_internals(expr, stream_name, target_name, accept, reject)

        def visit_field(expr: MageExpr, stream_name: str, accept: list[PyStmt], reject: list[PyStmt]) -> Generator[PyStmt]:
            field_name = generate_name('temp') if expr.field_name is None else expr.field_name
            if inside_token:
                accept = [ PyAugAssignStmt(PyNamedPattern(buffer_name), PyPlus(), PyNamedExpr(field_name)), *accept ]
            yield from visit_field_internals(expr, stream_name, field_name, accept, reject)

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
            yield from visit_field_internals(
                nonnull(rule.expr),
                'stream',
                'result',
                [ PyRetStmt(expr=PyNamedExpr('result')) ],
                [ PyRetStmt() ],
            )
            return

        if inside_token:
            yield PyAssignStmt(PyNamedPattern(buffer_name), value=PyConstExpr(''))
            args = []
            if not grammar.is_static_token_rule(rule):
                args.append(PyNamedExpr(buffer_name))
            yield from visit_fields(nonnull(rule.expr), 'stream', [ PyRetStmt(expr=PyCallExpr(PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)), args=args)) ], [ PyRetStmt() ])
            return

        fields = list(field for _, field in get_fields(nonnull(rule.expr), grammar=grammar) if field is not None)
        return_struct: list[PyStmt] = [
            PyRetStmt(
                expr=PyCallExpr(
                    PyNamedExpr(to_py_class_name(rule.name, prefix=prefix)),
                    args=list(PyKeywordArg(field.name, PyNamedExpr(field.name)) for field in fields)
                )
            )
        ]

        yield from visit_fields(nonnull(rule.expr), 'stream', return_struct, [ PyRetStmt() ])

    for element in grammar.elements:
        if grammar.is_parse_rule(element) or (not enable_tokens and grammar.is_token_rule(element)):
            stmts.append(PyFuncDef(
                name=f'parse_{element.name}',
                params=[ PyNamedParam(PyNamedPattern('stream'), annotation=PyNamedExpr(stream_type_name)) ],
                return_type=make_py_union([
                    PyNamedExpr(to_py_class_name(element.name, prefix=prefix)),
                    PyNamedExpr('None'),
                ]),
                body=list(gen_parse_body(element))
            ))

    return PyModule(stmts=stmts)
