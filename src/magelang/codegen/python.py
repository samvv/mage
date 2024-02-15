
from sweetener import IndentWriter, warn
import ast

from ..ast import Grammar

type Files = dict[str, str]

def generate_cst(grammar: Grammar) -> Files:
    stmts = []
    for rule in grammar.get_parse_rules():
        stmts.append(ast.ClassDef(name=rule.name))
    mod = ast.Module(body=stmts)
    return {
        'cst.py': ast.dump(mod),
    }
