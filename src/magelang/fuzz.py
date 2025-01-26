from collections.abc import Iterable
import random
from types import ModuleType
from typing import assert_never, cast
import importlib.util
import time

import magelang
from magelang.analysis import is_eof
from magelang.intervaltree import nonnull
from magelang.lang.mage.ast import ASCII_MAX, ASCII_MIN, POSINF, PUBLIC, MageCharSetExpr, MageChoiceExpr, MageExpr, MageGrammar, MageHideExpr, MageLitExpr, MageLookaheadExpr, MageRefExpr, MageRepeatExpr, MageRule, MageSeqExpr, set_parents
from magelang.eval import accepts
from magelang.runtime import EOF, CharStream, ParseStream

def load_parser(grammar: MageGrammar, native: bool = False, enable_tokens: bool = True) -> ModuleType:
    if native:
        source = cast(str, magelang.generate_files(grammar, lang='python', enable_cst=True, enable_parser=True, emit_single_file=True))
        spec = importlib.util.spec_from_loader('magelang.fuzzparser', loader=None)
        assert(spec is not None)
        module = importlib.util.module_from_spec(spec)
        exec(source, module.__dict__)
        return module
    raise NotImplementedError()

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


def random_grammar(
    min_rules: int = 0,
    max_rules: int = 100
) -> MageGrammar:
    # FIXME Also generate random modules and references to them
    elements = []
    n = random.randrange(min_rules, max_rules)
    for _ in range(0, n):
        name = random_name()
        elements.append(MageRule(name=name, flags=PUBLIC, expr=random_expr()))
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
    max_inf_repeat: int = 10,
    max_char_delta = 5,
) -> tuple[str, bool]:

    fails = False

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
            grammar = expr.get_grammar()
            rule = grammar.lookup(expr.name)
            assert(rule is not None and rule.expr is not None)
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

def fuzz_all(count: int | None = None) -> None:
    for i in xrange(count):
        grammar = random_grammar()
        fuzz_grammar(grammar, seed=i)


def fuzz_grammar(
    grammar: MageGrammar,
    seed: int | None = None,
    num_sentences: int | None = None,
    min_sentences_per_rule = 10,
    max_sentences_per_rule = 100,
    enable_tokens: bool = False,
    break_on_failure: bool = False
) -> None:
    parser = load_parser(grammar, native=True, enable_tokens=enable_tokens)
    succeeded = 0
    done = False
    if seed is None:
        seed = round(time.time() * 1000)
    n = 0
    while True:
        for rule in grammar.rules:
            if not rule.is_public:
                continue
            for sentence in range(random.randrange(min_sentences_per_rule, max_sentences_per_rule)):
                if num_sentences is not None and succeeded >= num_sentences:
                    done = True
                    break
                if rule.expr is None:
                    continue
                local_seed = seed + n
                random.seed(local_seed)
                sentence, fails = random_sentence(rule.expr)
                n += 1
                valid = accepts(rule.expr, sentence, grammar=grammar)
                if (not fails and not valid) or (fails and valid):
                    continue
                stream = CharStream(sentence, sentry=EOF)
                parse = getattr(parser, f'parse_{rule.name}')
                node = parse(stream)
                if (node is None) != fails:
                    message = f"\nOn sentence {repr(sentence)} and rule {rule.name} with seed {local_seed}: "
                    if fails:
                        message += "parser returned success where failure was expected."
                    else:
                        message += "parser returned failure where success was expected."
                    print(message)
                    if break_on_failure:
                        return
                succeeded += 1
                print(f'\r{succeeded} sentences succeeded.', end='')
            if done:
                break
        if done:
            break
    print("\nFinished with no failures.")

