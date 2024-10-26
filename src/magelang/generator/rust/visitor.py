
from magelang.ast import Grammar
from magelang.lang.rust.cst import RustNode, RustSourceFile


def generate_visitor(
    grammar: Grammar,
    prefix: str = '',
    debug: bool = False
) -> RustNode:

    items = []

    # TODO

    return RustSourceFile(items=items)
