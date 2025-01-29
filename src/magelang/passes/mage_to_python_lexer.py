
from typing import assert_never

from magelang.lang.python.cst import *
from magelang.lang.mage.ast import *
from magelang.manager import declare_pass
from magelang.util import NameGenerator, constant, nonnull
from magelang.helpers import make_py_cond, make_py_or, extern_type_to_py_type, to_py_class_name

@declare_pass()
def mage_to_python_lexer(
    grammar: MageGrammar,
    prefix = '',
) -> PyModule:

    lexer_class_name = to_py_class_name('lexer', prefix)
    token_type_name = to_py_class_name('token', prefix)

    generate_temporary = NameGenerator()

    keywords = []
    for rule in grammar.rules:
        if rule.is_keyword:
            assert(isinstance(rule.expr, MageLitExpr))
            keywords.append((rule.name, rule.expr.text))

    def make_charset_predicate(element: CharSetElement, target: PyExpr) -> PyExpr:
        if isinstance(element, str):
            return PyInfixExpr(left=target, op=PyEqualsEquals(), right=PyConstExpr(literal=element))
        if isinstance(element, tuple):
            low, high = element
            return PyNestExpr(expr=PyInfixExpr(
                left=PyInfixExpr(
                    left=PyCallExpr(
                        operator=PyNamedExpr('ord'),
                        args=[ target ]
                    ),
                    op=PyGreaterThanEquals(),
                    right=PyConstExpr(literal=ord(low))
                ),
                op=PyAndKeyword(),
                right=PyInfixExpr(
                    left=PyCallExpr(
                        operator=PyNamedExpr('ord'),
                        args=[ target ]
                    ),
                    op=PyLessThanEquals(),
                    right=PyConstExpr(literal=ord(high))
                )
            ))
        assert_never(element)

    body: list[PyStmt] = []

    char_offset_name = 'i'

    def noop() -> list[PyStmt]: return [ PyPassStmt() ]

    def brk() -> list[PyStmt]: return [ PyBreakStmt() ]

    def contin() -> list[PyStmt]: return [ PyContinueStmt() ]

    def lex_visit_backtrack_on_fail(expr: MageExpr, success: Callable[[], list[PyStmt]]) -> list[PyStmt]:
        keep_name = generate_temporary(prefix='keep')
        return [
            PyAssignStmt(PyNamedPattern(keep_name), value=PyNamedExpr(char_offset_name)),
            *lex_visit(expr, success),
            PyAssignStmt(PyNamedPattern(char_offset_name), value=PyNamedExpr(keep_name)),
        ]

    def lex_visit(expr: MageExpr, success: Callable[[], list[PyStmt]]) -> list[PyStmt]:
        """
        Generate lexer logic for a specific Mage expression.

        This function will return a body that on a successful lex will halt
        control flow by either throwing an exception or returning. If the
        returrned body let control continue, this implicitly means that lexing
        failed and the surrounding logic is assumed to try the next token.
        """

        rule = expr.returns
        if rule is not None:

            token_args = []

            if not grammar.is_static_token_rule(rule):
                token_args.append(
                    PyCallExpr(
                        # PyNamedExpr(f'_parse_{to_snake_case(spec.field_type)}'),
                        extern_type_to_py_type(rule.type_name),
                        args=[
                            PySubscriptExpr(
                                PyAttrExpr(PyNamedExpr('self'), '_text'),
                                slices=[ PyExprSlice(lower=PyNamedExpr('start'), upper=PyNamedExpr(char_offset_name)) ]
                            )
                        ]
                    )
                )

            old_success = success

            def new_success() -> list[PyStmt]:
                assert(rule is not None) # required because of a pyright limitation
                out = old_success()
                out.append(PyAssignStmt(PyAttrPattern(PyNamedPattern('self'), '_curr_offset'), value=PyNamedExpr(char_offset_name)))
                if rule.is_keyword_def:
                    out.append(PyAssignStmt(
                        PyNamedPattern('text'),
                        value=PySubscriptExpr(
                            PyAttrExpr(PyNamedExpr('self'), '_text'),
                            slices=[ PyExprSlice(lower=PyNamedExpr('start'), upper=PyNamedExpr(char_offset_name)) ]
                        )
                    ))
                    out.extend(make_py_cond(list((
                        PyInfixExpr(PyNamedExpr('text'), PyEqualsEquals(), PyConstExpr(kw_text)),
                        [ PyRetStmt(expr=PyCallExpr(operator=PyNamedExpr(to_py_class_name(kw_name, prefix)))) ]
                    ) for kw_name, kw_text in keywords)))
                out.append(PyRetStmt(expr=PyCallExpr(operator=PyNamedExpr(to_py_class_name(nonnull(rule).name, prefix)), args=token_args)))
                return out

            success = new_success

        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            assert(rule is not None)
            assert(rule.expr is not None)
            return lex_visit(rule.expr, success)

        if isinstance(expr, MageLookaheadExpr):
            keep_name = generate_temporary(prefix='keep')
            matches_name = generate_temporary(prefix='matches')
            if expr.is_negated:
                return [
                    PyAssignStmt(PyNamedPattern(keep_name), value=PyNamedExpr(char_offset_name)),
                    PyAssignStmt(PyNamedPattern(matches_name), value=PyNamedExpr('False')),
                    *lex_visit(expr.expr, lambda: [
                        PyAssignStmt(PyNamedPattern(char_offset_name), value=PyNamedExpr(keep_name)),
                        PyAssignStmt(PyNamedPattern(matches_name), value=PyNamedExpr('True'))
                    ]),
                    PyAssignStmt(PyNamedPattern(char_offset_name), value=PyNamedExpr(keep_name)),
                    *make_py_cond([ (PyPrefixExpr(PyNotKeyword(), PyNamedExpr(matches_name)), success()) ])
                ]
            return [
                PyAssignStmt(PyNamedPattern(keep_name), value=PyNamedExpr(char_offset_name)),
                *lex_visit(expr.expr, lambda: [
                    PyAssignStmt(PyNamedPattern(char_offset_name), value=PyNamedExpr(keep_name)),
                    *success()
                ]),
                PyAssignStmt(PyNamedPattern(char_offset_name), value=PyNamedExpr(keep_name)),
            ]

        if isinstance(expr, MageLitExpr):

            def next_char(k: int) -> list[PyStmt]:
                if k == len(expr.text):
                    return success()
                ch_name = generate_temporary(prefix='ch')
                ch = expr.text[k]
                return [
                    PyAssignStmt(
                        pattern=PyNamedPattern(ch_name),
                        value=PyCallExpr(
                            operator=PyAttrExpr(expr=PyNamedExpr('self'), name='_char_at'),
                            args=[ PyNamedExpr(char_offset_name) ]
                        )
                    ),
                    *make_py_cond([(
                        PyInfixExpr(left=PyNamedExpr(ch_name), op=PyEqualsEquals(), right=PyConstExpr(literal=ch)),
                        [
                            PyAugAssignStmt(PyNamedPattern(char_offset_name), PyPlus(), PyConstExpr(1)),
                            *next_char(k+1)
                        ]
                    )])
                ]

            return next_char(0)

        if isinstance(expr, MageSeqExpr):

            def next_element(n: int) -> list[PyStmt]:
                if n == len(expr.elements):
                    return success()
                return lex_visit(expr.elements[n], lambda: next_element(n+1))

            return next_element(0)

        if isinstance(expr, MageCharSetExpr):

            ch_name = generate_temporary(prefix='ch')

            body = [
                PyAugAssignStmt(PyNamedPattern(char_offset_name), PyPlus(), PyConstExpr(1)),
                *success()
            ]

            if expr.contains_range(chr(ASCII_MIN), chr(ASCII_MAX)):
                return body

            return [
                PyAssignStmt(
                    pattern=PyNamedPattern(ch_name),
                    value=PyCallExpr(
                        operator=PyAttrExpr(expr=PyNamedExpr('self'), name='_char_at'),
                        args=[ PyNamedExpr(char_offset_name) ]
                    )
                ),
                *make_py_cond([(
                    make_py_or(make_charset_predicate(element, PyNamedExpr(ch_name)) for element in expr.canonical_elements),
                    body
                )]),
            ]

        if isinstance(expr, MageRepeatExpr):

            if expr.min == 0 and expr.max == 1:
                return lex_visit_backtrack_on_fail(expr.expr, success)

            matches_var_name = generate_temporary('matches')

            out: list[PyStmt] = []

            max_body = []
            assert(expr.max > 0)
            if expr.max == POSINF:
                max_body.append(PyWhileStmt(expr=PyNamedExpr('True'), body=[
                    *lex_visit(expr.expr, contin),
                    PyBreakStmt(),
                ]))
            elif expr.max > expr.min:
                max_body.append(PyForStmt(
                    pattern=PyNamedPattern('_'),
                    expr=PyCallExpr(operator=PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.max - expr.min) ]),
                    body=[
                        *lex_visit(expr.expr, contin),
                        PyBreakStmt(),
                    ]
                ))
            max_body.extend(success())

            if expr.min == 0:
                out.extend(max_body)
            elif expr.min == 1:
                out.extend([
                    PyAssignStmt(PyNamedPattern(matches_var_name), value=PyNamedExpr('False')),
                    *lex_visit(expr.expr, constant(max_body))
                ])
            else:
                out.append(PyAssignStmt(PyNamedPattern(matches_var_name), value=PyNamedExpr('True')))
                out.append(PyForStmt(
                    pattern=PyNamedPattern('_'),
                    expr=PyCallExpr(operator=PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.min) ]),
                    body=[
                        *lex_visit(expr.expr, contin),
                        PyAssignStmt(PyNamedPattern(matches_var_name), value=PyNamedExpr('False')),
                        PyBreakStmt(),
                    ],
                ))
                out.append(PyIfStmt(first=PyIfCase(test=PyNamedExpr(matches_var_name), body=max_body)))

            return out

        if isinstance(expr, MageChoiceExpr):

            out: list[PyStmt] = []
            for element in expr.elements:
                out.extend(lex_visit_backtrack_on_fail(element, success))

            return out

        assert_never(expr)

    body.append(PyAssignStmt(PyNamedPattern(char_offset_name), value=PyAttrExpr(PyNamedExpr('self'), '_curr_offset')))

    if grammar.skip_rule:
        assert(grammar.skip_rule.expr is not None)
        # FIXME success() might assume termination of lexing procedure
        body.extend(lex_visit(grammar.skip_rule.expr, noop))

    body.append(PyAssignStmt(PyNamedPattern('start'), value=PyNamedExpr(char_offset_name)))

    choices = []
    for rule in grammar.rules:
        if not rule.is_token or rule.expr is None or rule.is_keyword:
            continue
        rule.expr.actions.append(ReturnAction(rule))
        choices.append(rule.expr)

    body.extend(lex_visit(MageChoiceExpr(choices), noop))

    body.append(PyRaiseStmt(expr=PyCallExpr(operator=PyNamedExpr('ScanError'), args=[])))

    return PyModule(stmts=[
        PyImportFromStmt(
            PyRelativePath(dots=[ PyDot() ], name=PyQualName('cst')),
            aliases=[ PyFromAlias(PyAsterisk()), ]
        ),
        PyImportFromStmt(PyAbsolutePath(PyQualName(modules=[ 'magelang' ], name='runtime')), aliases=[
            PyFromAlias('AbstractLexer'),
            PyFromAlias('ScanError'),
        ]),
        PyClassDef(lexer_class_name, bases=[ PyClassBaseArg('AbstractLexer') ], body=[
            PyFuncDef('lex', params=[ PyNamedParam(PyNamedPattern('self')) ], return_type=PyNamedExpr(token_type_name), body=body),
        ])
    ])
