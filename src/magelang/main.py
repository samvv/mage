
from pathlib import Path
from pprint import pprint
from typing import Unpack

from magelang import GenerateConfig, TargetLanguage, generate_files, load_grammar, mage_check, write_files
from magelang.constants import SEED_FILENAME_PREFIX
from magelang.lang.magedown.cst import MagedownDocument, MagedownNode, MagedownAccepts, MagedownRejects
from magelang.lang.python.cst import PyModule
from magelang.lang.revolv.ast import Program
from magelang.runtime import CharStream
from magelang.util import Files, Progress, load_py_file

from .manager import Context, apply, compose, get_pass_by_name, identity
from .logging import error, info, warn
from .lang.mage.ast import *
from .lang.mage.emitter import emit as mage_emit
from .lang.mage.parser import Parser
from .lang.mage.scanner import Scanner
from .lang.python.emitter import emit as py_emit
from .fuzz import fuzz_all, fuzz_grammar, generate_and_load_parser, random_grammar
from .eval import NO_MATCH, RECMAX, Error, evaluate


def _grammar_from_file_or_seed(filename: str) -> MageGrammar:
    if filename.startswith(SEED_FILENAME_PREFIX):
        import random
        seed = int(filename[len(SEED_FILENAME_PREFIX):])
        info(f"Using seed {seed}")
        random.seed(seed)
        return random_grammar()
    return load_grammar(filename)


def eval(filename: str, value: str, /, *, generate: bool = False, rule: str | None = None) -> int:
    cache_dir = Path.home() / '.cache' / 'magelang'
    grammar = _grammar_from_file_or_seed(filename)
    if rule is None:
        rules = list(grammar.rules)
        if not rules:
            error("Grammar has no rules")
            return 1
        rule = rules[-1].name
    dest_dir = cache_dir / 'last-eval'
    # hash = hash_grammar(grammar)
    # dest_dir = cache_dir / f'{hash:010d}'
    dest_dir.mkdir(parents=True, exist_ok=True)
    if generate:
        parser = generate_and_load_parser(grammar, dest_dir=dest_dir)
        parse = getattr(parser, f'parse_{rule}')
        print(parse(value))
        return 0
    else:
        entry = grammar.lookup(rule)
        if entry is None:
            error(f"Rule '{rule}' was not found in the grammar")
            return 1
        result = evaluate(entry, value)
        if result == NO_MATCH:
            error("Failed to parse sentence");
            return 1
        if result == RECMAX:
            error("Maximum recursion depth exceeded. Your grammar probably contains loops that consume nothing.")
            return 1
        print(result)
        return 0


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
    grammar = _grammar_from_file_or_seed(filename)
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
    file = TextFile.load(filename)
    scanner = Scanner(file)
    parser = Parser(scanner, file)
    grammar = parser.parse_grammar()
    opts = {}
    ctx = Context(opts)
    apply(ctx, grammar, mage_check)
    return 0

@dataclass(frozen=True)
class _Test:
    rule: MageRule
    text: str
    should_fail: bool

from tempfile import TemporaryDirectory

def _parse_doc(text: str) -> MagedownDocument:
    stream = CharStream(text)
    from magelang.lang.magedown.parser import parse_document
    doc = parse_document(stream)
    if doc is None:
        raise RuntimeError(f"failed to parse Magedown document")
    return doc

def magedown_emit(element: MagedownNode | str) -> str:
    if isinstance(element, str):
        return element
    raise NotImplementedError()

# def _get_special_blocks(doc: MagedownDocument, tag: str) -> Iterable[str]:
#     i = 0
#     while i < len(doc.elements):
#         element = doc.elements[i]
#         i += 1
#         if isinstance(element, MagedownOpenTag):
#             buffer = ''
#             while True:
#                 if i >= len(doc.elements):
#                     raise RuntimeError(f"while parsing a Magedown document: '{tag}' was not closed")
#                 child = doc.elements[i]
#                 i += 1
#                 if isinstance(child, MagedownCloseTag):
#                     break
#                 buffer += magedown_emit(child)
#             yield buffer

def _collect_tests(grammar: MageGrammar) -> list[_Test]:
    tests = []
    for rule in grammar.rules:
        if rule.comment is not None:
            doc = _parse_doc(rule.comment)
            for element in doc.elements:
                if isinstance(element, MagedownAccepts):
                    tests.append(_Test(rule, element.text.strip(), False))
                elif isinstance(element, MagedownRejects):
                    tests.append(_Test(rule, element.text.strip(), True))
    return tests

def _test_external(filename: str) -> tuple[int, int]:
    import pytest
    with TemporaryDirectory(prefix='mage-test-') as test_dir:
        generate('python', filename, enable_parser=True, enable_emitter=False, enable_ast=False, out_dir=Path(test_dir))
        if pytest.main([ test_dir ]) == 0:
            return 1, 0
        else:
            return 0, 1

def _test_internal(filename: Path | str) -> tuple[int, int]:
    grammar = load_grammar(filename)
    tests = _collect_tests(grammar)
    succeeded = set()
    failed = set()
    for test in tests:
        result = evaluate(test.rule, test.text)
        if result == RECMAX:
            warn(f"recursion depth reached while trying to evaluate a test.")
        elif test.should_fail == isinstance(result, Error):
            succeeded.add(test)
        else:
            print(f"Test for rule {test.rule.name} and {repr(test.text)} failed.")
            failed.add(test)
    return len(succeeded), len(failed)

def test(*filenames: str, generate: bool = False) -> int:
    """
    Test the examples inside the documentation of a grammar
    """
    code = 0
    for filename in filenames:
        proc = _test_external if generate else _test_internal
        succ, fail = proc(filename)
        print(f'Test {filename}: {succ} tests succeeded, {fail} failed')
        if fail:
            code = 1
    return code

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
    pass_ = identity
    for name in passes:
        found = get_pass_by_name(name)
        if found is None:
            error(f"failed to find a pass named '{name}'")
            return 1
        pass_ = compose(pass_, found)
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

