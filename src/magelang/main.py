
import argparse
from pathlib import Path

from magelang.emitter import emit
from magelang.passes import simplify

from .logging import error
from .util import pipe
from .ast import *
from .scanner import Scanner
from .parser import Parser
from .passes import extract_literals, inline, overlapping_charsets, extract_prefixes, check_undefined 
from .generator import generate, get_generator_languages

project_dir = Path(__file__).parent.parent.parent
modules_dir = Path(__file__).parent

def _load_grammar(filename: str) -> Grammar:
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=filename)
    parser = Parser(scanner)
    return parser.parse_grammar()

def _run_checks(grammar: Grammar) -> Grammar:
    return pipe(grammar, check_undefined, overlapping_charsets)

def _do_generate(args) -> int:

    filename = args.file[0]
    lang = args.lang
    opt = not args.no_opt
    debug = args.debug
    skip_checks = args.skip_checks
    prefix = args.prefix
    dest_dir = Path(args.out_dir)
    enable_linecol = True

    grammar = _load_grammar(filename)
    if not skip_checks:
        grammar = _run_checks(grammar)
    grammar = pipe(grammar, inline, extract_literals)
    # FIXME should only happen in the parser generator and lexer generator
    #if opt:
    #    grammar = pipe(grammar, extract_prefixes, simplify)
    #visualize(grammar, format='png')

    cst_parent_pointers = args.feat_all or args.feat_cst_parent_pointers

    prefix = prefix + '_' if prefix else ''

    for fname, text in generate(
        grammar,
        lang,
        prefix=prefix,
        cst_parent_pointers=cst_parent_pointers,
        debug=debug,
    ):
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

_passes = {
    'inline': inline,
    'simplify': simplify,
    'extract_prefixes': extract_prefixes,
    'extract_literals': extract_literals,
}

def _do_dump(args) -> int:
    filename = args.file[0]
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=filename)
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    for name in args.name:
        grammar = _passes[name](grammar)
    print(emit(grammar))
    return 0


def main() -> int:

    arg_parser = argparse.ArgumentParser()

    subparsers = arg_parser.add_subparsers()

    dump_parser = subparsers.add_parser('dump', help='Dump specific transformations on a grammar')

    dump_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    dump_parser.add_argument('name', nargs='*', help='Name of the pass to apply')
    dump_parser.set_defaults(func=_do_dump)

    check_parser = subparsers.add_parser('check', help='Check the given grammar for common mistakes')

    check_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    check_parser.set_defaults(func=_do_check)

    generate_parser = subparsers.add_parser('generate', help='Generate programming code from a grammar')
 
    generate_parser.add_argument('lang', choices=get_generator_languages(), help='The name of the template to use')
    generate_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    generate_parser.add_argument('--debug', action=argparse.BooleanOptionalAction, help='Generate extra checks that may affect performance')
    generate_parser.add_argument('--skip-checks', action=argparse.BooleanOptionalAction, help='Skip all sanity checks for the given grammar')
    generate_parser.add_argument('--no-opt', action=argparse.BooleanOptionalAction, help='Disable any optimisations')
    generate_parser.add_argument('--feat-all', action=argparse.BooleanOptionalAction, help='Enable all output features (off by default)')
    generate_parser.add_argument('--feat-linecol', action=argparse.BooleanOptionalAction, help='Track line/column information during lexing (unless grammar requires it off by default)')
    generate_parser.add_argument('--feat-cst-parent-pointers', action=argparse.BooleanOptionalAction, help='Generate references to the parent of a CST node (off by default)')
    generate_parser.add_argument('--force', action=argparse.BooleanOptionalAction, help='Ignore errors and always overwrite files that already exist')
    generate_parser.add_argument('--out-dir', default='output', help='Where to place the generated files')
    generate_parser.add_argument('--prefix', default='', help='Prefix all rules in the grammar with this value')
    generate_parser.set_defaults(func=_do_generate)

    args = arg_parser.parse_args()

    if 'func' not in args:
        error('You must provide a subcommand.')
        return 1

    return args.func(args)

