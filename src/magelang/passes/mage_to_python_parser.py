
import magelang.genparser
from magelang.lang.mage.ast import MageGrammar
from magelang.lang.python.cst import PyModule

def mage_to_python_parser(grammar: MageGrammar, prefix: str) -> PyModule:
    return magelang.genparser.mage_to_python_parser(grammar, prefix)
