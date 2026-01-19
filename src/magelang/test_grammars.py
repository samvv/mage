from pathlib import Path
import pytest

from magelang.eval import RECMAX, Error, evaluate
from magelang.helpers import collect_tests
from magelang.lang.mage.ast import MageGrammar
from magelang import load_grammar

grammar_fnames = list((Path(__file__).parent.parent.parent / 'grammars').glob('**/*.mage'))

@pytest.mark.parametrize("grammar", [ pytest.param(load_grammar(fname), id=str(fname)) for fname in grammar_fnames ])
def test_grammar(grammar: MageGrammar):
    for test in collect_tests(grammar):
        result = evaluate(test.rule, test.text)
        if result == RECMAX:
            warn(f"recursion depth reached while trying to evaluate a test. This most likely is an error.")
        elif test.should_fail != isinstance(result, Error):
            raise RuntimeError(f"Test for rule {test.rule.name} and {repr(test.text)} failed.")

