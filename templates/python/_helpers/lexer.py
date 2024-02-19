
import ast
import astor

from magelang import Grammar

def generate_lexer_logic(grammar: Grammar) -> str:
    stmts = []
    for rule in grammar.rules:
        if not rule.is_token:
            continue
    return astor.to_source(ast.Module(body=stmts))
