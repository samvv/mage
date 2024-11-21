
from typing import assert_never

from magelang.lang.python.cst import *
from magelang.lang.mage.ast import *
from magelang.util import NameGenerator, nonnull
from magelang.helpers import make_py_cond, make_py_or, extern_type_to_py_type, to_py_class_name

def mage_to_python_lexer(
    grammar: MageGrammar,
    prefix = '',
) -> PyModule:

    lexer_class_name = to_py_class_name('lexer', prefix)
    token_type_name = to_py_class_name('token', prefix)

    generate_temporary = NameGenerator()

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

        if expr.action is not None:
            rule = expr.action
            old_success = success
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
            success = lambda: [
                *old_success(),
                PyAssignStmt(PyAttrPattern(PyNamedPattern('self'), '_curr_offset'), value=PyNamedExpr(char_offset_name)),
                PyRetStmt(expr=PyCallExpr(operator=PyNamedExpr(to_py_class_name(nonnull(rule).name, prefix)), args=token_args))
            ]

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
                    PyAssignStmt(PyNamedPattern(matches_name), value=PyNamedExpr('True')),
                    *lex_visit(expr.expr, lambda: [
                        PyAssignStmt(PyNamedPattern(char_offset_name), value=PyNamedExpr(keep_name)),
                        PyAssignStmt(PyNamedPattern(matches_name), value=PyNamedExpr('False'))
                    ]),
                    PyAssignStmt(PyNamedPattern(char_offset_name), value=PyNamedExpr(keep_name)),
                    *make_py_cond([ (PyNamedExpr(matches_name), success()) ])
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

            return [
                PyAssignStmt(
                    pattern=PyNamedPattern(ch_name),
                    value=PyCallExpr(
                        operator=PyAttrExpr(expr=PyNamedExpr('self'), name='_char_at'),
                        args=[ PyNamedExpr(char_offset_name) ]
                    )
                ),
                *make_py_cond([(
                    make_py_or(make_charset_predicate(element, PyNamedExpr(ch_name)) for element in expr.elements),
                    [
                        PyAugAssignStmt(PyNamedPattern(char_offset_name), PyPlus(), PyConstExpr(1)),
                        *success()
                    ]
                )]),
            ]

        if isinstance(expr, MageRepeatExpr):

            if expr.min == 0 and expr.max == 1:
                return lex_visit_backtrack_on_fail(expr.expr, success)

            matches_var_name = generate_temporary('matches')

            out: list[PyStmt] = []

            if expr.min > 0:
                out.append(PyAssignStmt(PyNamedPattern(matches_var_name), value=PyNamedExpr('True')))
                out.append(PyForStmt(
                    pattern=PyNamedPattern('_'),
                    expr=PyCallExpr(operator=PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.min) ]),
                    body=[
                        *lex_visit(expr.expr, contin),
                        PyAssignStmt(PyNamedPattern(matches_var_name), value=PyNamedExpr('False')),
                        PyBreakStmt(),
                    ]
                ))

            max_body = []
            assert(expr.max > 0)
            if expr.max == POSINF:
                max_body.append(PyWhileStmt(expr=PyNamedExpr('True'), body=[
                    *lex_visit(expr.expr, contin),
                    PyBreakStmt(),
                ]))
            else:
                max_body.append(PyForStmt(
                    pattern=PyNamedPattern('_'),
                    expr=PyCallExpr(operator=PyNamedExpr('range'), args=[ PyConstExpr(0), PyConstExpr(expr.max - expr.min) ]),
                    body=[
                        *lex_visit(expr.expr, contin),
                        PyBreakStmt(),
                    ]
                ))
            max_body.extend(success())

            if expr.min > 0:
                out.append(PyIfStmt(first=PyIfCase(test=PyNamedExpr(matches_var_name), body=max_body)))
            else:
                out.extend(max_body)

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
        rule.expr.action = rule
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
