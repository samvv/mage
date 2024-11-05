
from magelang.ast import MageGrammar
from magelang.ir.ast import Program
from magelang.util import Files

from .syntaxtree import gen_syntax_tree

def generate_ir(
    grammar: MageGrammar,
    prefix = '',
    cst_parent_pointers = False,
    debug = False,
    enable_cst = False,
    enable_ast = False,
    enable_visitor = False,
    enable_lexer = False,
    enable_emitter = False,
) -> list[tuple[str, Program]]:

    files = list[tuple[str, Program]]();

    if enable_cst:
        files.append(('cst', gen_syntax_tree(grammar, prefix=prefix)))

    return files
