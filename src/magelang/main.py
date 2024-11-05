
import argparse
from pathlib import Path

from .logging import error
from .util import pipe, unreachable
from .ast import *
from .scanner import Scanner
from .parser import Parser
from .passes import *
from .emitter import emit
# from .generator import generate, get_generator_languages
from .ir import generate_ir
from .lang.python import emit as py_emit

project_dir = Path(__file__).parent.parent.parent
modules_dir = Path(__file__).parent

supported_languages = [ 'python', 'rust' ]

def _load_grammar(filename: str) -> MageGrammar:
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=filename)
    parser = Parser(scanner)
    return parser.parse_grammar()

def _run_checks(grammar: MageGrammar) -> MageGrammar:
    return pipe(grammar, check_token_no_parse, check_undefined, check_overlapping_charset_intervals, check_neg_charset_intervals)

def _do_generate(args) -> int:

    filename = args.file[0]
    lang = args.lang
    opt = not args.no_opt
    debug = args.debug
    skip_checks = args.skip_checks
    prefix = args.prefix
    dest_dir = Path(args.out_dir)
    enable_linecol = True

    grammar = pipe(_load_grammar(filename), inline, extract_literals, insert_magic_rules)
    if not skip_checks:
        grammar = _run_checks(grammar)
    # FIXME should only happen in the parser generator and lexer generator
    #if opt:
    #    grammar = pipe(grammar, extract_prefixes, simplify)
    #visualize(grammar, format='png')

    cst_parent_pointers = args.feat_all if args.feat_cst_parent_pointers is None else args.feat_cst_parent_pointers
    enable_visitor = args.feat_all if args.feat_visitor is None else args.feat_visitor
    enable_cst = args.feat_all if args.feat_cst is None else args.feat_cst
    enable_ast = args.feat_all if args.feat_ast is None else args.feat_ast
    enable_lexer = args.feat_all if args.feat_lexer is None else args.feat_lexer
    enable_emitter = args.feat_all if args.feat_emitter is None else args.feat_emitter

    # prefix = prefix + '_' if prefix else ''

    for fname, code in generate_ir(
        grammar,
        prefix=prefix,
        cst_parent_pointers=cst_parent_pointers,
        debug=debug,
        enable_emitter=enable_emitter,
        enable_cst=enable_cst,
        enable_ast=enable_ast,
        enable_visitor=enable_visitor,
        enable_lexer=enable_lexer
    ):
        if lang == 'python':
            text = py_emit(pipe(code, ir_to_python))
        elif lang == 'rust':
            text = rust_emit(pipe(code, ir_to_rust))
        else:
            unreachable()
        out_path = dest_dir / fname
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w') as f:
            f.write(text)

    return 0

def _do_check(args) -> int:
    filename = args.file[0]
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=filename)
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    _run_checks(grammar)
    return 0

def _do_dump(args) -> int:
    filename = args.file[0]
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=filename)
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    for name in args.name:
        grammar = mage_passes[name](grammar)
    print(emit(grammar))
    return 0


def main() -> int:

    arg_parser = argparse.ArgumentParser(prog='mage')

    subparsers = arg_parser.add_subparsers()

    dump_parser = subparsers.add_parser('dump', help='Dump specific transformations on a grammar')

    dump_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    dump_parser.add_argument('name', nargs='*', help='Name of the pass to apply')
    dump_parser.set_defaults(func=_do_dump)

    check_parser = subparsers.add_parser('check', help='Check the given grammar for common mistakes')

    check_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    check_parser.set_defaults(func=_do_check)

    generate_parser = subparsers.add_parser('generate', help='Generate programming code from a grammar')
 
    generate_parser.add_argument('lang', choices=supported_languages, help='The name of the template to use')
    generate_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    generate_parser.add_argument('--debug', action=argparse.BooleanOptionalAction, help='Generate extra checks that may affect performance')
    generate_parser.add_argument('--skip-checks', action=argparse.BooleanOptionalAction, help='Skip all sanity checks for the given grammar')
    generate_parser.add_argument('--no-opt', action=argparse.BooleanOptionalAction, help='Disable any optimisations')
    generate_parser.add_argument('--feat-all', action=argparse.BooleanOptionalAction, help='Enable all output features (off by default)')
    generate_parser.add_argument('--feat-linecol', action=argparse.BooleanOptionalAction, help='Track line/column information during lexing (unless grammar requires it off by default)')
    generate_parser.add_argument('--feat-cst-parent-pointers', action=argparse.BooleanOptionalAction, help='Generate references to the parent of a CST node (off by default)')
    generate_parser.add_argument('--feat-ast', action=argparse.BooleanOptionalAction, default=True, help='Generate an abstract syntax tree (on by default)')
    generate_parser.add_argument('--feat-cst', action=argparse.BooleanOptionalAction, default=True, help='Generate a concrete syntax tree (on by default)')
    generate_parser.add_argument('--feat-lexer', action=argparse.BooleanOptionalAction, default=True, help='Generate a lexer (on by default)')
    generate_parser.add_argument('--feat-visitor', action=argparse.BooleanOptionalAction, default=True, help='Generate AST/CST visitors (on by default)')
    generate_parser.add_argument('--feat-emitter', action=argparse.BooleanOptionalAction, default=True, help='Generate a highly experimental emitter (on by default)')
    generate_parser.add_argument('--force', action=argparse.BooleanOptionalAction, help='Ignore errors and always overwrite files that already exist')
    generate_parser.add_argument('--out-dir', default='output', help='Where to place the generated files')
    generate_parser.add_argument('--prefix', default='', help='Prefix all rules in the grammar with this value')
    generate_parser.set_defaults(func=_do_generate)

    args = arg_parser.parse_args()

    if 'func' not in args:
        error('You must provide a subcommand.')
        return 1

    return args.func(args)

