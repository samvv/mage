
from magelang.helpers import collect_tests, namespaced
from magelang.manager import declare_pass
from magelang.util import NameGenerator, to_snake_case
from magelang.lang.mage.ast import MageGrammar
from magelang.lang.python.cst import *
from magelang.helpers import make_py_isinstance, to_py_class_name

@declare_pass()
def mage_to_python_parser_tests(
    grammar: MageGrammar,
    prefix = '',
) -> PyModule:

    stmts: list[PyStmt] = [
        PyImportFromStmt(
            PyRelativePath(dots=[ PyDot() ], name=PyQualName('cst')),
            aliases=[ PyFromAlias(PyAsterisk()) ]
        ),
        PyImportFromStmt(
            PyRelativePath(dots=[ PyDot() ], name=PyQualName('parser')),
            aliases=[ PyFromAlias(PyAsterisk()) ]
        ),
    ]

    generate_temporary = NameGenerator()

    for i, test in enumerate(collect_tests(grammar)):
        body: list[PyStmt] = [
            PyAssignStmt(PyNamedPattern(f'input'), value=PyCallExpr(PyNamedExpr('CharStream'), args=[ PyConstExpr(test.text) ])),
            PyAssignStmt(PyNamedPattern(f'x{i}'), value=PyCallExpr(PyNamedExpr(f'parse_{to_snake_case(test.rule.name)}'), args=[ PyNamedExpr('input') ])),
            PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ PyCallExpr(PyNamedExpr(f'is_{namespaced(test.rule.name, prefix)}'), args=[ PyNamedExpr(f'x{i}') ]) ])),
            PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ PyCallExpr(PyAttrExpr(PyNamedExpr('input'), 'at_eof')) ])),
        ]
        stmts.append(PyFuncDef(
            name=generate_temporary(prefix=f'test_{test.rule.name}'),
            body=body,
        ))

    return PyModule(stmts=stmts)
