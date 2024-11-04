
from magelang.ast import MageGrammar
from magelang.lang.rust.cst import RustNode, RustSourceFile


def generate_visitor(
    grammar: MageGrammar,
    prefix: str = '',
    debug: bool = False
) -> RustNode:

    items = []

    # TODO

    return RustSourceFile(items=items)
