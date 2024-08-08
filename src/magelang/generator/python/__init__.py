
from magelang.ast import Grammar
from magelang.lang.python.emitter import emit
from magelang.util import Files
from .cst import generate_cst
from .lexer import generate_lexer
from .visitor import generate_visitor
from .test_lexer import generate_test_lexer

def generate(
    grammar: Grammar,
    prefix = '',
    cst_parent_pointers = False,
) -> Files:
    return [
        ('cst.py', emit(generate_cst(grammar, prefix=prefix, gen_parent_pointers=cst_parent_pointers))),
        ('lexer.py', emit(generate_lexer(grammar, prefix=prefix))),
        ('test_lexer.py', emit(generate_test_lexer(grammar, prefix=prefix))),
        ('visitor.py', emit(generate_visitor(grammar, prefix=prefix))),
    ]


