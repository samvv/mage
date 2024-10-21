
from magelang.lang.rust.cst import *
from magelang.treespec import Specs

def generate_tree(
    specs: Specs,
    prefix = ''
) -> RustSourceFile:

    items = []

    return RustSourceFile(items=items)
