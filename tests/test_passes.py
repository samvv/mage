
import pytest
from magelang.parser import Parser
from magelang.scanner import Scanner
from magelang.passes.check_undefined import mage_check_undefined
from magelang.util import pipe

def parse_grammar(content: str):
    scanner = Scanner(content, filename="<test>")
    parser = Parser(scanner)
    return parser.parse_grammar()

def test_check_undefined_no_error():
    valid_grammar = """
    pub start = expr
    expr = 'foo'
    """
    grammar = parse_grammar(valid_grammar)
    print("Parsed Grammar Rules:", grammar.rules)  
    try:
        grammar = pipe(grammar, mage_check_undefined)
    except ValueError:
        pytest.fail("check_undefined raised ValueError unexpectedly")

def test_check_undefined_with_error():
    invalid_grammar = """
    pub start = expr
    expr = foo # 'foo' is not defined
    """
    grammar = parse_grammar(invalid_grammar)
    print("Parsed Grammar Rules:", grammar.rules)  
    with pytest.raises(ValueError, match="Undefined rule referenced: foo"):
        grammar = pipe(grammar, mage_check_undefined)
