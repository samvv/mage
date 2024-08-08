
from textwrap import dedent
import marko
from magelang.util import NameGenerator
from magelang.ast import Grammar
from magelang.lang.python.cst import *
from .util import build_isinstance, get_marko_element_text, to_class_name

def generate_test_lexer(
    grammar: Grammar,
    prefix = '',
) -> PyModule:

    lexer_class_name = to_class_name('lexer', prefix)

    stmts: list[PyStmt] = [
       PyImportFromStmt(PyRelativePath(dots=[ PyDot() ], name=PyQualName('cst')), aliases=[ PyAlias(PyAbsolutePath(PyQualName('*'))) ]),
       PyImportFromStmt(PyRelativePath(dots=[ PyDot() ], name=PyQualName('lexer')), aliases=[ PyAlias(PyAbsolutePath(PyQualName(lexer_class_name))) ]),
    ]

    generate_temporary = NameGenerator()

    for rule in grammar.rules:
        if not grammar.is_token_rule(rule) or rule.comment is None:
            continue
        this_class_name = to_class_name(rule.name, prefix)
        doc = marko.parse(dedent(rule.comment))
        i = 0
        for child in doc.children:
            if isinstance(child, marko.block.FencedCode):
                input = get_marko_element_text(child.children[0]).strip()
                body: list[PyStmt] = [
                    PyAssignStmt(PyNamedPattern('lexer'), PyCallExpr(PyNamedExpr(lexer_class_name), args=[ PyConstExpr(input) ])),
                    PyAssignStmt(PyNamedPattern(f't{i}'), PyCallExpr(PyAttrExpr(PyNamedExpr('lexer'), 'lex'))),
                    PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ PyCallExpr(PyAttrExpr(PyNamedExpr('lexer'), 'at_eof')) ])),
                    PyExprStmt(PyCallExpr(PyNamedExpr('assert'), args=[ build_isinstance(PyNamedExpr(f't{i}'), PyNamedExpr(this_class_name)) ])),
                ]
                i += 1
                stmts.append(PyFuncDef(
                    name=generate_temporary(prefix=f'test_{rule.name}_'),
                    body=body,
                ))

    return PyModule(stmts=stmts)
