
import importlib.util
from pathlib import Path
from pprint import pprint
from typing import Literal

from magelang import generate_files, load_grammar, mage_check, write_files

from .manager import Context, apply, pipeline
from .logging import error
from .lang.mage.ast import *
from .lang.mage.emitter import emit as mage_emit
from .lang.mage.parser import Parser
from .lang.mage.scanner import Scanner
from .lang.python.emitter import emit as py_emit
from .passes import *

type TargetLanguage = Literal['python', 'rust']

def generate(
    lang: TargetLanguage,
    filename: Path | str,
    /,
    *,
    out_dir: Path | str,
    prefix: str = '',
    engine: str = 'old',
    skip_checks: bool = False,
    force: bool = False,
    enable_cst: bool = True,
    enable_ast: bool = True,
    enable_asserts: bool = False,
    enable_lexer: bool = True,
    enable_parser: bool = True,
    enable_emitter: bool = True,
    enable_cst_parent_pointers: bool = True,
    enable_ast_parent_pointers: bool = True,
    enable_visitor: bool = True,
    enable_rewriter: bool = True,
    enable_linecol: bool = False
) -> int:
    """
    Generate programming code from a grammar
    """
    filename = Path(filename)
    out_dir = Path(out_dir)
    files = generate_files(
        filename,
        lang,
        prefix=prefix,
        engine=engine,
        skip_checks=skip_checks,
        enable_cst=enable_cst,
        enable_ast=enable_ast,
        enable_asserts=enable_asserts,
        enable_lexer=enable_lexer,
        enable_parser=enable_parser,
        enable_emitter=enable_emitter,
        enable_cst_parent_pointers=enable_cst_parent_pointers,
        enable_ast_parent_pointers=enable_ast_parent_pointers,
        enable_visitor=enable_visitor,
        enable_rewriter=enable_rewriter,
        enable_linecol=enable_linecol,
    )
    write_files(files, out_dir, force)
    return 0

def check(filename: Path | str, /) -> int:
    """
    Check the given grammar for common mistakes
    """
    filename = Path(filename)
    with open(filename, 'r') as f:
        text = f.read()
    scanner = Scanner(text, filename=str(filename))
    parser = Parser(scanner)
    grammar = parser.parse_grammar()
    opts = {}
    ctx = Context(opts)
    apply(ctx, grammar, mage_check)
    return 0

def _load_script(path: Path, /) -> Any:
    module_name = f'magelang.imported.{path.stem}'
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert(spec is not None)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert(spec.loader is not None)
    spec.loader.exec_module(module)
    return module

def dump(filename: Path | str, *passes: str, **opts: Any) -> int:
    """
    Dump specific transformations of a grammar
    """
    filename = Path(filename)
    if filename.suffix == '.mage':
        input = load_grammar(filename)
    elif filename.suffix == '.py':
        input = _load_script(filename).output
    else:
        error(f'unrecognised file type: {filename.suffix}')
        return 1
    ctx = Context(opts)
    pass_ = pipeline(*(get_pass_by_name(name) for name in passes))
    result = apply(ctx, input, pass_)
    if is_mage_syntax(result):
        print(mage_emit(result))
    elif isinstance(result, Program):
        pprint(result)
    elif isinstance(result, PyModule):
        print(py_emit(result))
    else:
        error('Did not know how to print the resulting structure.')
        return 1
    return 0

