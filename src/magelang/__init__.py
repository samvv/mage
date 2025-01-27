
from enum import StrEnum
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
    mage_insert_magic_rules,
    mage_hide_lookaheads,
    mage_inline,
    mage_extract_literals,
)
python_optimise = pipeline(
    python_remove_pass_stmts,
)

def load_grammar(filename: Path | str) -> MageGrammar:
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=str(filename))
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    set_parents(grammar)
    return grammar

class Engine(StrEnum):
    NEW = 'new'
    OLD = 'old'

type TargetLanguage = Literal['python', 'rust']

def _is_functional(lang: str) -> bool:
    return lang in [ 'elm', 'purescript', 'haskell', 'agda', 'idris' ]

class GenerateConfig(TypedDict, total=False):
    engine: Engine
    prefix: str
    skip_checks: bool
    silent: bool
    emit_single_file: bool
    enable_cst: bool
    enable_ast: bool
    enable_asserts: bool
    enable_lexer: bool
    enable_parser: bool
    enable_emitter: bool
    enable_cst_parent_pointers: bool
    enable_ast_parent_pointers: bool
    enable_visitor: bool
    enable_rewriter: bool
    enable_linecol: bool
    max_named_chars: int

def default_config(lang: TargetLanguage, is_debug: bool) -> GenerateConfig:
    return GenerateConfig(
        prefix='',
        engine=Engine.OLD,
        skip_checks=False,
        emit_single_file=False,
        silent=False,
        enable_cst=True,
        enable_ast=True,
        enable_asserts=is_debug,
        enable_lexer=True,
        enable_parser=True,
        enable_emitter=True,
        enable_cst_parent_pointers=not _is_functional(lang),
        enable_ast_parent_pointers=not _is_functional(lang),
        enable_visitor=True,
        enable_rewriter=True,
        enable_linecol=False,
        max_named_chars=4,
    )

def generate_files(
    grammar: MageGrammar | Path | str,
    lang: TargetLanguage,
    *,
    debug: bool = False,
    **config: Unpack[GenerateConfig]
) -> Files | str:

    for k, v in default_config(lang, debug).items():
        if k not in config:
            config[k] = v

    engine = nonnull(config.get('engine'))
    enable_cst = nonnull(config.get('enable_cst'))
    enable_ast = nonnull(config.get('enable_ast'))
    enable_emitter = nonnull(config.get('enable_emitter'))
    enable_parser = nonnull(config.get('enable_parser'))
    enable_lexer = nonnull(config.get('enable_lexer'))
    emit_single_file = nonnull(config.get('emit_single_file'))
    skip_checks = nonnull(config.get('skip_checks'))
    silent = nonnull(config.get('silent'))

    ctx = Context(cast(dict[str, Any], config), silent=True)

    # FIXME should only happen in the parser generator and lexer generator
    #if enable_opt:
    #    pass_ = pipeline(pass_, extract_prefixes, simplify)

    if not isinstance(grammar, MageGrammar):
        grammar = load_grammar(grammar)

    if engine == Engine.OLD:
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
        if enable_lexer:
            files['lexer.py'] = pipeline(mage_flatten_grammars, mage_to_python_lexer)
            files['test_lexer.py'] = mage_to_python_lexer_tests
        if enable_parser:
            files['parser.py'] = mage_to_python_parser
        mage_to_target = compose(
            merge(distribute(files), pipeline(mage_to_treespec, distribute(trees))),
            each_value(pipeline(python_optimise, python_to_text)),
        )
    elif engine == Engine.NEW:
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

    files = apply(ctx, grammar, pipeline(
        mage_prepare_grammar, # Inline rules etc
        identity if skip_checks or silent else mage_check , # User error reporting
        mage_to_target # Actual compilation
    ))

    if not emit_single_file:
        return files

    out = ''
    if enable_cst:
        out += '\n\n' + files['cst.py']
    if enable_ast:
        out += '\n\n' + files['ast.py']
    if enable_lexer:
        out += '\n\n' + files['lexer.py']
    if enable_parser:
        out += '\n\n' + files['parser.py']
    if enable_emitter:
        out += '\n\n' + files['emitter.py']
    return out

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
