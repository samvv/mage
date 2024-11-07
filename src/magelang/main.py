
import importlib.util
import argparse
from os import PathLike
from pathlib import Path
from pprint import pprint

from .manager import Context, apply, compose, each_value, distribute, identity, pipeline
from .logging import error
from .ast import *
from .lang.python.emitter import emit as py_emit
from .scanner import Scanner
from .parser import Parser
from .passes import *
from .emitter import emit

project_dir = Path(__file__).parent.parent.parent
modules_dir = Path(__file__).parent

supported_languages = [ 'python', 'rust' ]

def _load_grammar(filename: PathLike) -> MageGrammar:
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=str(filename))
    parser = Parser(scanner)
    return parser.parse_grammar()

mage_check = pipeline(check_token_no_parse, check_undefined, check_overlapping_charset_intervals, check_neg_charset_intervals)
mage_prepare_grammar = pipeline(inline, extract_literals, insert_magic_rules)

def _do_generate(args) -> int:

    engine = args.engine
    filename = args.file[0]
    lang = args.lang
    opt = not args.no_opt
    debug = args.debug
    skip_checks = args.skip_checks
    prefix = args.prefix
    dest_dir = Path(args.out_dir)
    enable_linecol = True

    opts = {
        'cst_parent_pointers': args.feat_all if args.feat_cst_parent_pointers is None else args.feat_cst_parent_pointers,
        'enable_visitor': args.feat_all if args.feat_visitor is None else args.feat_visitor,
        'enable_cst': args.feat_all if args.feat_cst is None else args.feat_cst,
        'enable_ast': args.feat_all if args.feat_ast is None else args.feat_ast,
        'enable_lexer': args.feat_all if args.feat_lexer is None else args.feat_lexer,
        'enable_emitter': args.feat_all if args.feat_emitter is None else args.feat_emitter,
        'prefix': prefix
    }

    ctx = Context(opts)

    # FIXME should only happen in the parser generator and lexer generator
    #if opt:
    #    pass_ = pipeline(pass_, extract_prefixes, simplify)

    grammar = _load_grammar(filename)

    if engine == 'old':
        mage_to_target = compose(
            distribute({
                'cst.py': mage_to_python_cst,
                'emitter.py': mage_to_python_emitter,
            }),
            each_value(python_to_text),
        )
    elif engine == 'next':
        if lang == 'python':
            revolv_to_target = each_value(pipeline(revolv_lift_assign_expr, revolv_to_python, python_to_text))
        elif lang == 'rust':
            revolv_to_target = each_value(pipeline(revolv_to_rust, rust_to_text))
        else:
            panic(f"Unrecognised language '{lang}'")
        mage_to_target = pipeline(
            distribute({
                'cst.rev': mage_to_revolv_syntax_tree,
            }),
            revolv_to_target
        )
    else:
        panic("Unrecognised engine used")

    grammar = _load_grammar(filename)
    files = apply(ctx, grammar, pipeline(
        mage_prepare_grammar,
        mage_check if not skip_checks else identity,
        mage_to_target
    ))
    for fname, text in files.items():
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
    opts = {}
    ctx = Context(opts)
    apply(ctx, grammar, mage_check)
    return 0

def _load_script(path: Path) -> Any:
    module_name = f'magelang.imported.{path.stem}'
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert(spec is not None)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert(spec.loader is not None)
    spec.loader.exec_module(module)
    return module

def _do_dump(args) -> int:
    filename = Path(args.file[0])
    if filename.suffix == '.mage':
        input = _load_grammar(filename)
    elif filename.suffix == '.py':
        input = _load_script(filename).output
    else:
        error(f'unrecognised file type: {filename.suffix}')
        return 1
    opts = {} # TODO
    ctx = Context(opts)
    pass_ = pipeline(*(get_pass_by_name(name) for name in args.name))
    result = apply(ctx, input, pass_)
    if is_mage_syntax(result):
        print(emit(result))
    elif isinstance(result, Program):
        pprint(result)
    elif isinstance(result, PyModule):
        print(py_emit(result))
    else:
        error('Did not know how to print the resulting structure.')
        return 1
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
    generate_parser.add_argument('--engine', default='old', help='Which engine to use')
    generate_parser.add_argument('--debug', choices=[ 'old', 'next' ], action=argparse.BooleanOptionalAction, help='Generate extra checks that may affect performance')
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

