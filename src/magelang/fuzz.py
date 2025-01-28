from collections.abc import Iterable
from pathlib import Path
import random
from types import ModuleType
from typing import assert_never, cast
import time

import magelang
from magelang.analysis import is_eof
from magelang.constants import DEFAULT_FUZZ_DIR
from magelang.lang.mage.ast import ASCII_MAX, ASCII_MIN, POSINF, PUBLIC, MageCharSetExpr, MageChoiceExpr, MageExpr, MageGrammar, MageHideExpr, MageLitExpr, MageLookaheadExpr, MageRefExpr, MageRepeatExpr, MageRule, MageSeqExpr, set_parents
from magelang.eval import accepts
from magelang.runtime import EOF, CharStream, ParseStream
from magelang.util import Files, Progress, load_py_file, unreachable

def load_parser(grammar: MageGrammar, dest_dir: Path) -> ModuleType:
    # TODO conditionally enable the lexer and fuzz that as well
    files = cast(Files, magelang.generate_files(
        grammar,
        lang='python',
        enable_cst=True,
        enable_parser=True,
        silent=True,
        enable_ast=False,
        enable_emitter=False,
        enable_lexer=False
    ))
    magelang.write_files(files, dest_dir, force=True)
    return load_py_file(dest_dir / 'parser.py')

class Table:

    def __init__(self, elements: list[tuple[str, str]] | None = None) -> None:
        if elements is None:
            elements = []
        self._elements = elements

    def add(self, low, high) -> None:
        self._elements.append((low, high))

    def __len__(self):
        return sum(ord(high) - ord(low) + 1 for low, high in self._elements)

    def pick_char(self, n: int) -> str | None:
        for (low, high) in self._elements:
            x1 = ord(low)
            x2 = ord(high)
            d = x2 - x1 + 1
            if n < d:
                return chr(x1 + n)
            n -= d

    def pick_random_char(self) -> str:
        k = random.randrange(len(self))
        ch = self.pick_char(k)
        assert(ch is not None)
        return ch

ident_start_table = Table([
    ('a', 'z'),
    ('A', 'Z'),
])

ident_part_table = Table([
    ('a', 'z'),
    ('A', 'Z'),
    ('0', '9'),
])


def random_name() -> str:
    n = random.randrange(2, 10)
    out = ident_start_table.pick_random_char()
    for _ in range(0, n-1):
        out += ident_part_table.pick_random_char()
    return out


def random_expr(
    rule_names: list[str],
    max_choices: int = 2,
    max_repeat_min: int = 5,
    max_lit_chars: int = 10,
    max_repeat_min_max: int = 5,
    max_charset_elements: int = 20,
) -> MageExpr:
    def generate() -> MageExpr:
        n = random.randrange(7)
        if n == 0:
            out = ''
            for _ in range(random.randrange(1, max_lit_chars)):
                out += random_char()
            return MageLitExpr(out)
        if n == 1:
            elements = []
            for _ in range(random.randrange(1, max_choices)):
                elements.append(generate())
            return MageChoiceExpr(elements)
        if n == 2:
            elements = []
            for _ in range(random.randrange(1, max_choices)):
                elements.append(generate())
            return MageSeqExpr(elements)
        if n == 3:
            min = random.randrange(max_repeat_min)
            d = random.randrange(max_repeat_min_max+1)
            if d == max_repeat_min_max:
                max = POSINF
            else:
                max = min + d
            expr = generate()
            return MageRepeatExpr(expr, min, max)
        if n == 4:
            elements = []
            ci = toss()
            invert = toss()
            for _ in range(random.randrange(max_charset_elements)):
                l = random.randrange(ASCII_MIN, ASCII_MAX)
                h = random.randrange(l, ASCII_MAX)
                elements.append((chr(l), chr(h)))
            return MageCharSetExpr(elements, ci, invert)
        if n == 5:
            return MageHideExpr(generate())
        if n == 6:
            return MageRefExpr(random.choice(rule_names))
        unreachable()
    return generate()

def random_grammar(
    min_rules: int = 0,
    max_rules: int = 100
) -> MageGrammar:
    # FIXME Also generate random modules and references to them
    elements = []
    rule_names = []
    n = random.randrange(min_rules, max_rules)
    for _ in range(n):
        rule_names.append(random_name())
    for i in range(n):
        elements.append(MageRule(name=rule_names[i], flags=PUBLIC, expr=random_expr(rule_names)))
    grammar = MageGrammar(elements=elements)
    set_parents(grammar)
    return grammar

def random_char():
    return chr(random.randrange(ASCII_MIN, ASCII_MAX))

def toss():
    return random.randint(0, 1) == 0

def random_sentence(
    expr: MageExpr,
    failure_rate: float = 0.1,
    max_recurse = 3,
    max_inf_repeat: int = 10,
    max_char_delta = 5,
) -> tuple[str, bool]:

    fails = False
    visits = dict[MageRule, int]()

    def visit(expr: MageExpr) -> str:
        nonlocal fails
        if is_eof(expr):
            return ''
        if isinstance(expr, MageLitExpr):
            r = random.random()
            if r >= failure_rate:
                return expr.text
            fails = True
            out = ''
            k = random.randrange(len(expr.text))
            n = random.randrange(len(expr.text) - k)
            left = random.randrange(-max_char_delta, max_char_delta)
            right = random.randrange(-max_char_delta, max_char_delta)
            for _ in range(left + max_char_delta):
                out += random_char()
            for i in range(n):
                if toss():
                    out += random_char()
                else:
                    out += expr.text[i + k]
            for _ in range(right + max_char_delta):
                out += random_char()
            return out
        if isinstance(expr, MageCharSetExpr):
            r = random.random()
            if r < failure_rate:
                fails = True
                return random_char()
            table = Table()
            for element in expr.canonical_elements:
                if isinstance(element, tuple):
                    low, high = element
                else:
                    low = element
                    high = element
                table.add(low, high)
            return table.pick_random_char()
        if isinstance(expr, MageRefExpr):
            grammar = expr.grammar
            rule = grammar.lookup(expr.name)
            assert(rule is not None and rule.expr is not None)
            n = visits.get(rule, 0)
            if n >= max_recurse:
                return ''
            visits[rule] = n + 1
            return visit(rule.expr)
        if isinstance(expr, MageHideExpr):
            return visit(expr.expr)
        if isinstance(expr, MageLookaheadExpr):
            return '' # FIXME keep in mind what exps are not allowed
        if isinstance(expr, MageSeqExpr):
            out = ''
            for element in expr.elements:
                out += visit(element)
            return out
        if isinstance(expr, MageChoiceExpr):
            return visit(random.choice(expr.elements))
        if isinstance(expr, MageRepeatExpr):
            if expr.max == POSINF:
                n = expr.min + random.randrange(max_inf_repeat)
            elif expr.min == expr.max:
                n = expr.min
            else:
                n = random.randrange(expr.min, expr.max)
            out = ''
            for _ in range(0, n):
                out += visit(expr.expr)
            return out
        assert_never(expr)

    return visit(expr), fails

def xrange(n: int | None) -> Iterable[None]:
    if n is None:
        while True:
            yield
    return range(n)

def fuzz_all(
    count: int | None = None,
    num_sentences_per_grammar=50000,
    break_on_failure: bool = False,
    dest_dir: Path = DEFAULT_FUZZ_DIR,
    progress: Progress | None = None,
) -> None:
    if progress is None:
        progress = Progress()
    # sys.setrecursionlimit(10000)
    for i in xrange(count):
        # FIXME might lead to duplicate grammars
        seed = round(time.time() * 1000)
        random.seed(seed)
        grammar = random_grammar()
        progress.write_line(f"Starting fuzz of grammar with seed {seed}")
        if not fuzz_grammar(grammar, num_sentences=num_sentences_per_grammar, grammar_seed=seed, break_on_failure=break_on_failure, dest_dir=dest_dir):
            progress.write_line(f"Grammar with seed {seed} failed.")

def fuzz_grammar(
    grammar: MageGrammar,
    seed: int | None = None,
    grammar_seed: int | None = None,
    num_sentences: int | None = None,
    min_sentences_per_rule = 10,
    max_sentences_per_rule = 100,
    break_on_failure: bool = False,
    dest_dir: Path = DEFAULT_FUZZ_DIR,
    progress: Progress | None = None,
) -> bool:
    if progress is None:
        progress = Progress()
    try:
        parser = load_parser(grammar, dest_dir=dest_dir)
    except Exception as e:
        print(f"Failed to generate parser for grammar with seed {grammar_seed}: {e}")
        if break_on_failure:
            raise e
        return False
    succeeded = 0
    failed = 0
    done = False
    if seed is None:
        seed = round(time.time() * 1000)
    sentence_count = 0
    while True:
        keep = sentence_count
        for rule in grammar.rules:
            if not rule.is_public:
                continue
            for _ in range(random.randrange(min_sentences_per_rule, max_sentences_per_rule)):
                if num_sentences is not None and succeeded >= num_sentences:
                    done = True
                    break
                if rule.expr is None:
                    continue
                sentence_seed = seed + sentence_count
                random.seed(sentence_seed)
                sentence, fails = random_sentence(rule.expr)
                sentence_count += 1
                valid = accepts(rule.expr, sentence, grammar=grammar)
                if valid is None:
                    progress.write_line(f"Potential infinite rule {rule.name} in grammar with seed {seed}. Skipping.")
                    continue
                if (not fails and not valid) or (fails and valid):
                    continue
                stream = CharStream(sentence, sentry=EOF)
                parse = getattr(parser, f'parse_{rule.name}')
                try:
                    node = parse(stream)
                except Exception as e:
                    progress.write_line(f"Parser crashed during test of sentence {repr(sentence)} on grammar with seed {grammar_seed}")
                    if break_on_failure:
                        raise e
                    failed += 1
                    continue
                if stream.peek() != EOF:
                    node = None
                if (node is None) != fails:
                    if fails:
                        progress.write_line(f"Parser returned success on rule {rule.name} and sentence {repr(sentence)} where failure was expected.")
                    else:
                        progress.write_line(f"Parser returned failure on rule {rule.name} and sentence {repr(sentence)} where success was expected.")
                    failed += 1
                    if break_on_failure:
                        return False
                else:
                    succeeded += 1
                progress.status(f'{succeeded} sentences succeeded.')
            if done:
                break
        if sentence_count == keep:
            progress.write_line(f"Grammar with seed {seed} had no fuzzable rules")
            break
        if done:
            break
    return failed == 0

