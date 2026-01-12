
from enum import StrEnum
import os
from pathlib import Path
from types import ModuleType
from typing import Literal

from .logging import error
from .runtime import ConsoleDiagnostics, Diagnostics
from .util import Files, load_py_file
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
    mage_insert_skip,
    mage_hide_lookaheads,
    mage_extract_literals,
)

python_optimise = pipeline(
    python_remove_pass_stmts,
)

def load_grammar(filename: Path | str) -> MageGrammar:
    file = TextFile.load(filename)
    scanner = Scanner(file)
    parser = Parser(scanner, file)
    grammar = parser.parse_grammar()
    set_parents(grammar)
    return grammar

class Engine(StrEnum):
    NEW = 'new'
    OLD = 'old'
    _default = OLD

type TargetLanguage = Literal['python', 'rust']

def _is_functional(lang: str) -> bool:
    return lang in [ 'elm', 'purescript', 'haskell', 'agda', 'idris' ]

class YesNoAuto(StrEnum):
    AUTO = 'auto'
    YES = 'yes'
    NO = 'no'

    _true = YES
    _false = NO
    _default = AUTO

    def __bool__(self) -> bool:
        assert(self != YesNoAuto.AUTO)
        return self == YesNoAuto.YES

    @staticmethod
    def from_bool(enable: bool) -> 'YesNoAuto':
        return YesNoAuto.YES if enable else YesNoAuto.NO

class GenerateConfig(TypedDict, total=False):
    engine: Engine
    """
    What internal generator to use.

    new - The future engine (experimental)
    old - An engine that is guaranteed to work
    """
    prefix: str
    """
    Prepend this name to all classes and functions.

    This value should be lowercase without trailing underscore.
    """
    skip_checks: bool
    """
    Do not perform any sanity checks except for the ones that prevent crashing the compiler.

    This might provide a small performance boost to grammars that are already known to be correct.
    """
    silent: bool
    """
    Do not print information on standard output.
    """
    emit_single_file: bool
    """
    Concatenate all files into one big file.
    """
    enable_cst: bool
    """
    Generate a concrete syntax tree (CST)

    A CST is a direct representation of a source text in tree form.
    """
    enable_ast: bool
    """
    Generate an abstract syntax tree (AST)

    An AST is like a CST but with some information removed.
    """
    enable_asserts: bool
    """
    Generate additional assertions in the source code. This has a slight
    performance impact and it generally not recommended for production.
    """
    enable_lexer: YesNoAuto
    """
    Set to `YesNoAuto.AUTO` to automatically try to enable the lexer and fall
    back to parsing without if the grammar does not support it.
    """
    enable_lexer_tests: bool
    """
    Generate additional tests specifically for the lexer.

    This value may be set to `True` even when no lexer is being generated. In
    that case, no tests will be generated.
    """
    enable_parser: bool
    """
    Generate a parser based on the given grammar.
    """
    enable_parser_tests: bool
    """
    Generate additional tests specifically for the parser.

    This value may be set to `True` even when no parser is being generated. In
    that case, no parser tests will be generated.
    """
    enable_emitter: bool
    """
    Attempt to write an experimental emitter.
    """
    enable_cst_parent_pointers: bool
    """
    Add parent pointers to the CST.
    """
    enable_ast_parent_pointers: bool
    """
    Add parent pointers to the AST.
    """
    enable_visitor: bool
    """
    Generate in addition to an AST and/or CST functions that traverse over the tree.
    """
    enable_rewriter: bool
    """
    Generate in addition to an AST and/or CST functions that rewrite the tree.
    """
    enable_linecol: bool
    """
    Enable tracking of line/column numbers in the lexer/parser.
    """
    max_named_chars: int
    """
    The maximum amount of characters to give an explicit name before falling
    back to generating a special name.
    """
    diagnostics: Diagnostics
    """
    The diagnostics reporter to use.
    """

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
        enable_lexer=YesNoAuto.AUTO,
        enable_lexer_tests=is_debug,
        enable_parser=True,
        enable_parser_tests=is_debug,
        enable_emitter=True,
        enable_cst_parent_pointers=not _is_functional(lang),
        enable_ast_parent_pointers=not _is_functional(lang),
        enable_visitor=True,
        enable_rewriter=True,
        enable_linecol=False,
        max_named_chars=4,
        diagnostics=ConsoleDiagnostics(),
    )

def generate_files(
    grammar: MageGrammar | Path | str,
    lang: TargetLanguage,
    *,
    debug: bool = False,
    **config: Unpack[GenerateConfig]
) -> Files | str | None:

    for k, v in default_config(lang, debug).items():
        if k not in config:
            config[k] = v

    if not isinstance(grammar, MageGrammar):
        grammar = load_grammar(grammar)

    # TODO allow user to specify grammar name in grammar itself
    lang_name = Path(nonnull(grammar.file).filename).stem

    fname_init = f'__init__.py'
    fname_cst = f'cst.py'
    fname_cst_defs = f'cst.pyi'
    fname_ast = f'ast.py'
    fname_ast_defs = 'ast.pyi'
    fname_emitter = f'emitter.py'
    fname_lexer = f'lexer.py'
    fname_parser = f'parser.py'
    fname_test_lexer = f'test_lexer.py'
    fname_test_parser = f'test_parser.py'

    # TODO implement analysis step, checking how grammar can be tokenized
    can_lexer_be_enabled = False # any(rule.is_lex for rule in grammar.rules)
    if nonnull(config.get('enable_lexer')) == YesNoAuto.AUTO:
        config['enable_lexer'] = YesNoAuto.from_bool(can_lexer_be_enabled)

    engine = nonnull(config.get('engine'))
    enable_cst = nonnull(config.get('enable_cst'))
    enable_ast = nonnull(config.get('enable_ast'))
    enable_emitter = nonnull(config.get('enable_emitter'))
    enable_parser = nonnull(config.get('enable_parser'))
    enable_parser_tests = nonnull(config.get('enable_parser_tests'))
    emit_single_file = nonnull(config.get('emit_single_file'))
    skip_checks = nonnull(config.get('skip_checks'))
    silent = nonnull(config.get('silent'))
    enable_lexer = bool(nonnull(config.get('enable_lexer')))
    enable_lexer_tests = nonnull(config.get('enable_lexer_tests'))

    if enable_lexer and not can_lexer_be_enabled:
        error('could not enable lexer because there are no tokens defined in the grammar')
        return

    ctx = Context(cast(dict[str, Any], config), silent=True)

    # FIXME should only happen in the parser generator and lexer generator
    #if enable_opt:
    #    pass_ = pipeline(pass_, extract_prefixes, simplify)

    if engine == Engine.OLD:
        files = dict[str, Pass[MageGrammar, PyModule]]()
        trees = dict[str, Pass[Specs, PyModule]]()
        if enable_cst:
            # TODO add local `enable_cst_parent_pointers`
            trees[fname_cst] = treespec_to_python
            trees[fname_cst_defs] = treespec_to_python_interfaces
        if enable_ast:
            # TODO add local `enable_ast_parent_pointers`
            trees[fname_ast] = pipeline(treespec_cst_to_ast, treespec_to_python)
            trees[fname_ast_defs] = pipeline(treespec_cst_to_ast, treespec_to_python_interfaces)
        if enable_emitter:
            files[fname_emitter] = pipeline(mage_prepare_grammar, mage_to_python_emitter)
        if enable_lexer:
            files[fname_lexer] = pipeline(mage_inline, mage_prepare_grammar, mage_flatten_grammars, mage_to_python_lexer)
            if enable_lexer_tests:
                files[fname_test_lexer] = mage_to_python_lexer_tests
        if enable_parser:
            files[fname_parser] = pipeline(mage_inline, mage_prepare_grammar, mage_to_python_parser)
            if enable_parser_tests:
                files[fname_test_parser] = pipeline(mage_to_python_parser_tests)
        mage_to_target = compose(
            merge(distribute(files), pipeline(mage_inline, mage_prepare_grammar, mage_to_treespec, distribute(trees))),
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
        mage_insert_magic_rules,
        identity if skip_checks or silent else mage_check, # User error reporting
        mage_to_target # Actual compilation
    ))

    files[fname_init] = ''

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


def generate_and_load_parser(grammar: MageGrammar, dest_dir: Path | None = None) -> ModuleType:
    if dest_dir is None:
        # TODO maybe hash grammar and append the result to the path?
        dest_dir = Path.home() / '.cache' / 'magelang' / 'generated'
    files = cast(Files, generate_files(
        grammar,
        lang='python',
        enable_cst=True,
        enable_parser=True,
        silent=True,
        enable_ast=False,
        enable_emitter=False,
        enable_lexer=YesNoAuto.NO,
    ))
    write_files(files, dest_dir, force=True)
    os.sync()
    return load_parser(dest_dir)


def load_parser(dest_dir: Path) -> ModuleType:
    return load_py_file(dest_dir / 'parser.py')


def main() -> int:
    from turbolaunch import launch
    return launch('magelang.main')
