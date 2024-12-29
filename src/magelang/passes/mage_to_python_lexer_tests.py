
from textwrap import dedent
import marko
from magelang.util import NameGenerator
from magelang.lang.mage.ast import MageGrammar
from magelang.lang.python.cst import *
from magelang.helpers import make_py_isinstance, get_marko_element_text, to_py_class_name

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

    for rule in grammar.rules:
        if not grammar.is_token_rule(rule) or rule.comment is None:
            continue
        this_class_name = to_py_class_name(rule.name, prefix)
        doc = marko.parse(dedent(rule.comment))
        i = 0
        for child in doc.children:
            if isinstance(child, marko.block.FencedCode):
                input = get_marko_element_text(child.children[0]).strip()
                body: list[PyStmt] = [
                    PyAssignStmt(PyNamedPattern('lexer'), value=PyCallExpr(PyNamedExpr(lexer_class_name), args=[ PyConstExpr(input) ])),
                    PyAssignStmt(PyNamedPattern(f't{i}'), value=PyCallExpr(PyAttrExpr(PyNamedExpr('lexer'), 'lex'))),
                    PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ make_py_isinstance(PyNamedExpr(f't{i}'), PyNamedExpr(this_class_name)) ])),
                    PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ PyCallExpr(PyAttrExpr(PyNamedExpr('lexer'), 'at_eof')) ])),
                ]
                i += 1
                stmts.append(PyFuncDef(
                    name=generate_temporary(prefix=f'test_{rule.name}'),
                    body=body,
                ))

    return PyModule(stmts=stmts)
