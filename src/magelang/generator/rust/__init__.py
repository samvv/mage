
from magelang.ast import Grammar
from magelang.treespec import grammar_to_specs
from magelang.util import Files
from magelang.lang.rust.emitter_3 import rs_emit as emit # FIXME

#from .tree_types import generate_tree_types
#from .lexer import generate_lexer
#from .test_lexer import generate_test_lexer
#from .emitter import generate_emitter

def generate(
    grammar: Grammar,
    prefix = '',
    cst_parent_pointers = False,
    debug = False,
    enable_cst = False,
    enable_ast = False,
    enable_visitor = False,
    enable_lexer = False,
    enable_emitter = False,
) -> Files:
    specs = grammar_to_specs(grammar)
    files = []
    if enable_cst:
        from .tree import generate_tree
        files.append(('cst.rs', emit(generate_tree(specs, prefix=prefix))))
        if enable_visitor:
            from .visitor import generate_visitor
            files.append(('visitor.rs', emit(generate_visitor(grammar, prefix=prefix, debug=debug))))
    return files

