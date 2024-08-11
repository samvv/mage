
import argparse
from pathlib import Path
from sweetener.logging import error
from sweetener.visual import visualize

from .util import pipe
from .ast import *
from .scanner import Scanner
from .parser import Parser
from .passes import extract_literals, inline
from .generator import generate, get_generator_languages

project_dir = Path(__file__).parent.parent.parent
modules_dir = Path(__file__).parent

def _do_generate(args) -> int:

    file = args.file[0]
    dest_dir = Path(args.out_dir)
    prefix = args.prefix
    lang = args.lang
    enable_linecol = True

    with open(file, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=file)
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    #grammar = transform_prefix(grammar)
    #grammar = transform_reduce(grammar)
    grammar = pipe(grammar, inline, extract_literals)
    #visualize(grammar, format='png')

    cst_parent_pointers = args.feat_all or args.feat_cst_parent_pointers

    prefix = prefix + '_' if prefix else ''

    for fname, text in generate(grammar, lang, prefix=prefix, cst_parent_pointers=cst_parent_pointers):
        out_path = dest_dir / fname
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w') as f:
            f.write(text)

    return 0

def main() -> int:

    arg_parser = argparse.ArgumentParser()

    subparsers = arg_parser.add_subparsers()

    generate_parser = subparsers.add_parser('generate', help='Generate programming code from a grammar')

    generate_parser.add_argument('lang', choices=get_generator_languages(), help='The name of the template to use')
    generate_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    generate_parser.add_argument('--feat-all', action=argparse.BooleanOptionalAction, default=False, help='Enable all output features (off by default)')
    generate_parser.add_argument('--feat-linecol', action=argparse.BooleanOptionalAction, default=False, help='Track line/column information during lexing (unless grammar requires it off by default)')
    generate_parser.add_argument('--feat-cst-parent-pointers', action=argparse.BooleanOptionalAction, default=False, help='Generate references to the parent of a CST node (off by default)')
    generate_parser.add_argument('--force', action=argparse.BooleanOptionalAction, default=False, help='Add this flag to always overwrite files that already exist')
    generate_parser.add_argument('--out-dir', default='output', help='Where to place the generated files')
    generate_parser.add_argument('--prefix', default='', help='Prefix all rules in the grammar with this value')
    generate_parser.set_defaults(func=_do_generate)

    args = arg_parser.parse_args()

    if 'func' not in args:
        error('You must provide a subcommand.')
        return 1

    return args.func(args)

