from pathlib import Path
import pytest

from magelang.eval import RECMAX, Error, evaluate
from magelang.helpers import collect_tests
from magelang.lang.mage.ast import MageGrammar
from magelang.passes.mage_expand_pratt import mage_expand_pratt
from magelang import load_grammar

grammar_fnames = list((Path(__file__).parent.parent.parent / 'grammars').glob('**/*.mage'))

@pytest.mark.parametrize("grammar", [ pytest.param(load_grammar(fname), id=str(fname)) for fname in grammar_fnames ])
def test_grammar(grammar: MageGrammar):
    grammar = mage_expand_pratt(grammar)
    tests = collect_tests(grammar)
    for test in tests:
        result = evaluate(test.rule, test.text)
        if result == RECMAX:
            raise RuntimeError(f"maximum recursion depth reached while trying to evaluate {test.rule.name} with {repr(test.text)}.")
        elif test.should_fail != isinstance(result, Error):
            raise RuntimeError(f"Test for rule {test.rule.name} and {repr(test.text)} failed.")

