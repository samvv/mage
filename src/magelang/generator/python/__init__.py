
from magelang.ast import Grammar
from magelang.lang.python.emitter import emit
from magelang.treespec import grammar_to_specs
from magelang.util import Files

#from .tree_types import generate_tree_types

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
        files.append(('cst.py', emit(generate_tree(specs, prefix=prefix, gen_parent_pointers=cst_parent_pointers))))
        #('cst.pyi', emit(generate_tree_types(specs, prefix=prefix, gen_parent_pointers=cst_parent_pointers))),
        if enable_visitor:
            from .visitor import generate_visitor
            print('HERee')
            files.append(('cst_visitor.py', emit(generate_visitor(grammar, prefix=prefix, debug=debug))))

    if enable_lexer:
        from .lexer import generate_lexer
        from .test_lexer import generate_test_lexer
        files.append(('lexer.py', emit(generate_lexer(grammar, prefix=prefix))))
        files.append(('test_lexer.py', emit(generate_test_lexer(grammar, prefix=prefix))))

    if enable_emitter:
        from .emitter import generate_emitter
        files.append(('emitter.py', emit(generate_emitter(grammar, prefix=prefix))))

    print(files)
    return files
