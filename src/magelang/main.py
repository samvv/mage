from pathlib import Path
from pprint import pprint
from typing import Unpack

from magelang import GenerateConfig, TargetLanguage, generate_files, load_grammar, mage_check, write_files
from magelang.constants import SEED_FILENAME_PREFIX
from magelang.eval import NO_MATCH, RECMAX, RULE_NOT_FOUND, Error, evaluate
from magelang.fuzz import fuzz_all, fuzz_grammar, generate_and_load_parser, random_grammar
from magelang.helpers import collect_tests
from magelang.lang.mage.ast import *
from magelang.lang.mage.emitter import emit as mage_emit
from magelang.lang.mage.parser import Parser
from magelang.lang.mage.scanner import Scanner
from magelang.lang.magedown.cst import MagedownNode
from magelang.lang.python.cst import PyModule
from magelang.lang.python.emitter import emit as py_emit
from magelang.lang.revolv.ast import Program
from magelang.logging import error, info, warn
from magelang.machine import call_machine_function, link_machine
from magelang.passes import mage_to_machine, mage_extract_literals
from magelang.manager import Context, apply, compose, get_pass_by_name, identity
from magelang.util import Files, Progress, load_py_file

@dataclass
class EvalMode:
    pass

@dataclass
class MachineMode:
    pass

@dataclass
class CodegenMode:
    dest_dir: Path

type Mode = (
    EvalMode
    | MachineMode
    | CodegenMode
)


def _grammar_from_file_or_seed(filename: str) -> MageGrammar:
    if filename.startswith(SEED_FILENAME_PREFIX):
        import random
        seed = int(filename[len(SEED_FILENAME_PREFIX):])
        info(f"Using seed {seed}")
        random.seed(seed)
        return random_grammar()
    return load_grammar(filename)


def _run_parse_rule(config: Mode, grammar: MageGrammar, rule_name: str, input: str) -> Any | Error:
    if isinstance(config, EvalMode):
        entry = grammar.lookup(rule_name)
        if entry is None:
            return RULE_NOT_FOUND
        return evaluate(entry, input)
    elif isinstance(config, CodegenMode):
        parser = generate_and_load_parser(grammar, config.dest_dir)
        parse = getattr(parser, f'parse_{rule_name}')
        try:
            return parse(input)
        except parser.ParseError:
            return NO_MATCH
    elif isinstance(config, MachineMode):
        grammar = mage_extract_literals(grammar)
        m = mage_to_machine(grammar)
        m.dump()
        link_machine(m)
        return call_machine_function(m, rule_name,  input)

def _get_cache_dir() -> Path:
    return Path.home() / '.cache' / 'magelang'

def eval(filename: str, input: str, /, *, rule: str | None = None, generate: bool = False, machine: bool = False) -> int:

    cache_dir = _get_cache_dir()

    grammar = _grammar_from_file_or_seed(filename)

    if rule is None:
        if grammar.start_rule is None:
            error("Grammar has no rules")
            return 1
        rule = grammar.start_rule.name

    dest_dir = cache_dir / 'last-eval'
    # hash = hash_grammar(grammar)
    # dest_dir = cache_dir / f'{hash:010d}'
    dest_dir.mkdir(parents=True, exist_ok=True)

    if generate:
        mode = CodegenMode(dest_dir)
    elif machine:
        mode = MachineMode()
    else:
        mode = EvalMode()

    result = _run_parse_rule(mode, grammar, rule, input)
    if result is RULE_NOT_FOUND:
        error(f"Rule '{rule}' was not found in the grammar")
        return 1
    if result is RECMAX:
        error("Maximum recursion depth exceeded. Your grammar probably contains loops that consume nothing.")
        return 1
    if result is NO_MATCH:
        error("Failed to parse sentence.");
        return 1
    print(result)
    return 0


def generate_for_lang(
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

from tempfile import TemporaryDirectory

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

def _run_test(filename: str, mode: Mode) -> tuple[int, int]:
    grammar = load_grammar(filename)
    tests = collect_tests(grammar)
    succeeded = set()
    failed = set()
    for test in tests:
        result = _run_parse_rule(mode, grammar, rule_name=test.rule.name, input=test.text)
        if result == RECMAX:
            warn(f"recursion depth reached while trying to evaluate a test.")
        elif test.should_fail == isinstance(result, Error):
            succeeded.add(test)
        else:
            print(f"Test for rule {test.rule.name} and {repr(test.text)} failed.")
            failed.add(test)
    return len(succeeded), len(failed)

def test(*filenames: str, generate: bool = False, machine: bool = False, dest_dir: str | None = None) -> int:
    """
    Test the examples inside the documentation of a grammar
    """
    cache_dir = _get_cache_dir()

    # Codegen needs to be handled separately
    if generate:
        dest_dir_path = cache_dir / 'last-test' if dest_dir is None else Path(dest_dir)
        import pytest
        fail = 0
        for filename in filenames:
            generate_for_lang(
                'python',
                filename,
                enable_parser=True,
                enable_emitter=False,
                enable_ast=False,
                enable_lexer_tests=True,
                enable_parser_tests=True,
                out_dir=dest_dir_path,
            )
            if pytest.main([ str(dest_dir) ]) != 0:
                fail += 1
            return int(fail > 0)

    if machine:
        mode = MachineMode()
    else:
        mode = EvalMode()
    code = 0
    for filename in filenames:
        succ, fail = _run_test(filename, mode)
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

