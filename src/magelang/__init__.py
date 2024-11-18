
from pathlib import Path
from magelang.util import Files
from .manager import *
from .lang.mage import *
from .lang.python import *
from .lang.treespec import *
from .passes import *

mage_check = pipeline(
    mage_check_token_no_parse,
    mage_check_undefined,
    mage_check_overlapping_charset_intervals,
    mage_check_neg_charset_intervals
)
mage_prepare_grammar = pipeline(
    mage_inline,
    mage_extract_literals,
    mage_insert_magic_rules
)

def load_grammar(filename: Path | str) -> MageGrammar:
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=str(filename))
    parser = Parser(scanner)
    return parser.parse_grammar()

def generate_files(
    filename: Path | str,
    lang: str,
    prefix: str = '',
    engine: str = 'old',
    skip_checks: bool = False,
    enable_cst: bool = False,
    enable_ast: bool = False,
    enable_asserts: bool = False,
    enable_lexer: bool = False,
    enable_parser: bool = False,
    enable_emitter: bool = False,
    enable_cst_parent_pointers: bool = False,
    enable_ast_parent_pointers: bool = False,
    enable_visitor: bool = False,
    enable_rewriter: bool = False,
    enable_linecol: bool = False
) -> Files:

    opts: dict[str, Any] = {
        'prefix': prefix,
        'enable_asserts': enable_asserts,
    }

    ctx = Context(opts)

    # FIXME should only happen in the parser generator and lexer generator
    #if enable_opt:
    #    pass_ = pipeline(pass_, extract_prefixes, simplify)

    grammar = load_grammar(filename)

    if engine == 'old':
        files = dict[str, Pass[MageGrammar, PyModule]]()
        trees = dict[str, Pass[Specs, PyModule]]()
        if enable_cst:
            # TODO add local `enable_cst_parent_pointers`
            trees['cst.py'] = treespec_to_python
        if enable_ast:
            # TODO add local `enable_ast_parent_pointers`
            trees['ast.py'] = pipeline(treespec_cst_to_ast, treespec_to_python)
        if enable_emitter:
            files['emitter.py'] = mage_to_python_emitter
        mage_to_target = compose(
            merge(distribute(files), pipeline(mage_to_treespec, distribute(trees))),
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
        panic("Unrecognised engine requested")

    grammar = load_grammar(filename)

    return apply(ctx, grammar, pipeline(
        mage_prepare_grammar,
        mage_check if not skip_checks else identity,
        mage_to_target
    ))

def write_files(files: Files, dest_dir: Path, force: bool = False) -> None:
    for fname, text in files.items():
        out_path = dest_dir / fname
        info(f'Writing {out_path} ...')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w' if force else 'x') as f:
            f.write(text)

def main() -> int:
    from .cli import run
    return run('magelang.main')
