
from magelang.ast import Grammar
from magelang.lang.python.emitter import emit
from magelang.treespec import grammar_to_specs
from magelang.util import Files
from .tree import generate_tree
from .tree_types import generate_tree_types
from .lexer import generate_lexer
from .visitor import generate_visitor
from .test_lexer import generate_test_lexer

def generate(
    grammar: Grammar,
    prefix = '',
    cst_parent_pointers = False,
    debug = False,
) -> Files:
    specs = grammar_to_specs(grammar)
    return [
        ('cst.py', emit(generate_tree(specs, prefix=prefix, gen_parent_pointers=cst_parent_pointers))),
        #('cst.pyi', emit(generate_tree_types(specs, prefix=prefix, gen_parent_pointers=cst_parent_pointers))),
        ('lexer.py', emit(generate_lexer(grammar, prefix=prefix))),
        ('test_lexer.py', emit(generate_test_lexer(grammar, prefix=prefix))),
        ('visitor.py', emit(generate_visitor(grammar, prefix=prefix, debug=debug))),
    ]

