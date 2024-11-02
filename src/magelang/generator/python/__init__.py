
from magelang.ast import Grammar
from magelang.lang.python.emitter import emit
from magelang.treespec import cst_to_ast, grammar_to_specs
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

    cst_specs = grammar_to_specs(grammar)

    files = []

    init_py_code = ''

    # if enable_ast:
    #     ast_specs = cst_to_ast(cst_specs)
    #     from .tree import generate_tree
    #     files.append(('ast.py', emit(generate_tree(ast_specs, prefix=prefix, gen_parent_pointers=cst_parent_pointers))))
    #     init_py_code += 'from .ast import *\n'
    #     if enable_visitor:
    #         from .visitor import generate_visitor
    #         files.append(('ast_visitor.py', emit(generate_visitor(ast_specs, prefix=prefix, debug=debug))))
    #         init_py_code += 'from .ast_visitor import *\n'

    if enable_cst:
        from .tree import generate_tree
        files.append(('cst.py', emit(generate_tree(cst_specs, prefix=prefix, gen_parent_pointers=cst_parent_pointers))))
        #files.append(('cst.pyi', emit(generate_tree_types(specs, prefix=prefix, gen_parent_pointers=cst_parent_pointers))))
        init_py_code += 'from .cst import *\n'
        if enable_visitor:
            from .visitor import generate_visitor
            files.append(('cst_visitor.py', emit(generate_visitor(cst_specs, prefix=prefix, debug=debug))))
            init_py_code += 'from .cst_visitor import *\n'

    if enable_lexer:
        from .lexer import generate_lexer
        from .test_lexer import generate_test_lexer
        files.append(('lexer.py', emit(generate_lexer(grammar, prefix=prefix))))
        init_py_code += 'from .lexer import *\n'
        files.append(('test_lexer.py', emit(generate_test_lexer(grammar, prefix=prefix))))

    if enable_emitter:
        from .emitter import generate_emitter
        init_py_code += 'from .emitter import *\n'
        files.append(('emitter.py', emit(generate_emitter(grammar, prefix=prefix))))

    files.append(('__init__.py', init_py_code))

    return files
