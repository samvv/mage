
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
from .fuzz import fuzz_all, fuzz_grammar

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

@dataclass
class Test:
    rule: MageRule
    text: str
    should_fail: bool

from tempfile import TemporaryDirectory

def _collect_tests(grammar: MageGrammar) -> list[Test]:
    tests = []
    for rule in grammar.rules:
        if rule.comment is not None:
            doc = parse_doc(rule.comment)
            for text in get_accept_blocks(doc):
                tests.append(Test(rule, text, False))
            for text in get_reject_blocks(doc):
                tests.append(Test(rule, text, True))
    return tests

def _test_external(filename: Path | str) -> bool:
    import pytest
    with TemporaryDirectory(prefix='mage-test-') as test_dir:
        generate('python', filename, enable_lexer=True, enable_parser=True, enable_parser_tests=True, out_dir=Path(test_dir))
        return pytest.main([ test_dir ]) == 0

def _test_internal(filename: Path | str) -> bool:
    grammar = load_grammar(filename)
    tests = _collect_tests(grammar)
    succeeded = set()
    failed = set()
    for test in tests:
        result = evaluate(grammar, test.rule.name, test.text)
        if result is None:
            if test.should_fail:
                succeeded.add(test)
            else:
                failed.add(test)
    if not failed:
        print(f'{len(succeeded)} tests succeeded, 0 failed')
        return True
    else:
        print(f'{len(succeeded)} tests failed, {len(succeeded)} succeedded.')
        return False

def test(filename: Path | str, *, generate: bool) -> int:
    test = _test_external if generate else _test_internal
    return test(filename)

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

def fuzz(filename: str | None, n: int = 100) -> int:
    if filename is None:
        fuzz_all(n)
        return 0
    grammar = load_grammar(filename)
    fuzz_grammar(grammar)
    return 0
