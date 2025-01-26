from collections.abc import Iterable
import random
from types import ModuleType
from typing import assert_never, cast
import importlib.util

import magelang
from magelang.analysis import is_eof
from magelang.intervaltree import nonnull
from magelang.lang.mage.ast import POSINF, PUBLIC, MageCharSetExpr, MageChoiceExpr, MageExpr, MageGrammar, MageHideExpr, MageLitExpr, MageLookaheadExpr, MageRefExpr, MageRepeatExpr, MageRule, MageSeqExpr, set_parents
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


def random_sentence(
    expr: MageExpr,
    max_inf_repeat: int = 10
) -> str:
    def visit(expr: MageExpr) -> str:
        if is_eof(expr):
            return ''
        if isinstance(expr, MageLitExpr):
            return expr.text
        if isinstance(expr, MageCharSetExpr):
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
    return visit(expr)

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
    random.seed(seed)
    parser = load_parser(grammar, native=True, enable_tokens=enable_tokens)
    print()
    count = 0
    done = False
    while True:
        for rule in grammar.rules:
            if not rule.is_public:
                continue
            for sentence in range(random.randrange(min_sentences_per_rule, max_sentences_per_rule)):
                if num_sentences is not None and count >= num_sentences:
                    done = True
                    break
                if rule.expr is None:
                    continue
                sentence = random_sentence(rule.expr)
                if not accepts(rule.expr, sentence, grammar=grammar):
                    continue
                stream = CharStream(sentence, sentry=EOF)
                parse = getattr(parser, f'parse_{rule.name}')
                if parse(stream) is None:
                    print(f"\nOn sentence {repr(sentence)} and rule {rule.name}: parser returned failure where success was expected.")
                    if break_on_failure:
                        return
                count += 1
                print(f'\r{count} sentences succeeded.', end='')
            if done:
                break
        if done:
            break
    print("\nFinished with no failures.")

