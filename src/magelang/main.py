
import argparse
from pathlib import Path
from sweetener.logging import error
from sweetener.visual import visualize

import templaty

from .ast import *
from .scanner import Scanner
from .parser import Parser
from .transforms import extract_literals, inline

project_dir = Path(__file__).parent.parent.parent
modules_dir = Path(__file__).parent
templates_dir = project_dir / 'templates'

def _do_generate(args) -> int:

    file = args.file[0]
    dest_dir = Path(args.out_dir)
    prefix = args.prefix
    template_name = args.template
    enable_linecol = True

    with open(file, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=file)
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    #grammar = transform_prefix(grammar)
    #grammar = transform_reduce(grammar)
    grammar = inline(grammar)
    grammar = extract_literals(grammar)
    #visualize(grammar, format='png')

    ctx = {
        'prefix': prefix + '_' if prefix else '',
        'grammar': grammar,
        'enable_linecol': enable_linecol,
    }

    indentation = None
    if template_name == 'python':
        indentation = '    '

    templaty.execute_dir(templates_dir / template_name, dest_dir=dest_dir, ctx=ctx, force=args.force, indentation=indentation)

    return 0

def main() -> int:

    template_names = []
    for path in templates_dir.iterdir():
        if path.is_dir() and not str(path).startswith('_'):
            template_names.append(path.name)

    arg_parser = argparse.ArgumentParser()

    subparsers = arg_parser.add_subparsers()

    generate_parser = subparsers.add_parser('generate', help='Generate programming code from a grammar')

    generate_parser.add_argument('file', nargs=1, help='A path to a grammar file')
    generate_parser.add_argument('template', choices=template_names, help='The name of the template to use')
    generate_parser.add_argument('--force', action='store_true', help='Always overwrite files that already exist')
    generate_parser.add_argument('--out-dir', default='output', help='Where to place the generated files')
    generate_parser.add_argument('--prefix', default='', help='Prefix all rules in the grammar with this value')
    generate_parser.set_defaults(func=_do_generate)

    args = arg_parser.parse_args()

    if 'func' not in args:
        error('You must provide a subcommand.')
        return 1

    return args.func(args)

