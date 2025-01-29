
from pathlib import Path
from pprint import pprint

from magelang import GenerateConfig, TargetLanguage, default_config, generate_files, load_grammar, mage_check, write_files
from magelang.constants import SEED_FILENAME_PREFIX
from magelang.util import Files, Progress, load_py_file

from .manager import Context, apply, pipeline
from .logging import error, info
from .lang.mage.ast import *
from .lang.mage.emitter import emit as mage_emit
from .lang.mage.parser import Parser
from .lang.mage.scanner import Scanner
from .lang.python.emitter import emit as py_emit
from .passes import *
from .fuzz import fuzz_all, fuzz_grammar, random_grammar

def generate(
    lang: TargetLanguage,
    filename: str,
    /,
    *,
    out_dir: Path | str,
    debug: bool = False,
    force: bool = False,
    **opts: Unpack[GenerateConfig]
) -> int:
    """
    Generate programming code from a grammar
    """
    if filename.startswith(SEED_FILENAME_PREFIX):
        import random
        seed = int(filename[len(SEED_FILENAME_PREFIX):])
        info(f"Using seed {seed}")
        random.seed(seed)
        grammar = random_grammar()
    else:
        grammar = load_grammar(filename)
    out_dir = Path(out_dir)
    files = cast(Files, generate_files(
        grammar,
        lang,
        debug=debug,
        **opts,
    ))
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

@dataclass
class _Test:
    rule: MageRule
    text: str
    should_fail: bool

from tempfile import TemporaryDirectory

def _collect_tests(grammar: MageGrammar) -> list[_Test]:
    tests = []
    for rule in grammar.rules:
        if rule.comment is not None:
            doc = parse_doc(rule.comment)
            for text in get_accept_blocks(doc):
                tests.append(_Test(rule, text, False))
            for text in get_reject_blocks(doc):
                tests.append(_Test(rule, text, True))
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
    """
    Test the examples inside the documentation of a grammar
    """
    test = _test_external if generate else _test_internal
    return test(filename)

def dump(filename: str, *passes: str,  **opts: Any) -> int:
    """
    Dump specific transformations of a grammar
    """
    if filename.startswith(SEED_FILENAME_PREFIX):
        import random
        seed = int(filename[len(SEED_FILENAME_PREFIX):])
        info(f"Using seed {seed}")
        random.seed(seed)
        input = random_grammar()
    else:
        p = Path(filename)
        if p.suffix == '.mage':
            input = load_grammar(p)
        elif p.suffix == '.py':
            input = load_py_file(p).output
        else:
            error(f'unrecognised file type: {p.suffix}')
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

def fuzz(filename: str | None = None, /, *, all: bool = False, limit: int | None = None, break_on_failure: bool = False) -> int:
    progress = Progress()
    progress.start()
    if all:
        result = fuzz_all(limit, break_on_failure=break_on_failure, progress=progress)
    else:
        if filename is None:
            error("Provide a grammar to fuzz or use --all to fuzz mage itself.")
            return 1
        seed = None
        if filename.startswith(SEED_FILENAME_PREFIX):
            import random
            seed = int(filename[len(SEED_FILENAME_PREFIX):])
            info(f"Using seed {seed}")
            random.seed(seed)
            grammar = random_grammar()
        else:
            grammar = load_grammar(filename)
        result = fuzz_grammar(grammar, num_sentences=limit, break_on_failure=break_on_failure, progress=progress, grammar_seed=seed)
    if result:
        progress.finish("All test succeeded")
        return 0
    progress.finish("Some grammars failed.")
    return 1

