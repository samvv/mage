
from textwrap import dedent

from magelang.helpers import collect_tests, make_py_isinstance, to_py_class_name
from magelang.lang.mage.ast import MageGrammar
from magelang.lang.python.cst import *
from magelang.manager import declare_pass
from magelang.util import NameGenerator


@declare_pass()
def mage_to_python_lexer_tests(
    grammar: MageGrammar,
    prefix = '',
) -> PyModule:

    lexer_class_name = to_py_class_name('lexer', prefix)

    stmts: list[PyStmt] = [
        PyImportFromStmt(
            PyRelativePath(dots=[ PyDot() ], name=PyQualName('cst')),
            aliases=[ PyFromAlias(PyAsterisk()) ]),
        PyImportFromStmt(
            PyRelativePath(dots=[ PyDot() ], name=PyQualName('lexer')),
            aliases=[ PyFromAlias(lexer_class_name) ]
        ),
    ]

    generate_temporary = NameGenerator()

    for i, test in enumerate(collect_tests(grammar)):
        token_class_name = to_py_class_name(test.rule.name, prefix)
        body: list[PyStmt] = [
            PyAssignStmt(PyNamedPattern('lexer'), value=PyCallExpr(PyNamedExpr(lexer_class_name), args=[ PyConstExpr(test.text) ])),
            PyAssignStmt(PyNamedPattern(f't{i}'), value=PyCallExpr(PyAttrExpr(PyNamedExpr('lexer'), 'lex'))),
            PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ make_py_isinstance(PyNamedExpr(f't{i}'), PyNamedExpr(token_class_name)) ])),
            PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ PyCallExpr(PyAttrExpr(PyNamedExpr('lexer'), 'at_eof')) ])),
        ]
        stmts.append(PyFuncDef(
            name=generate_temporary(prefix=f'test_{test.rule.name}'),
            body=body,
        ))

    return PyModule(stmts=stmts)
