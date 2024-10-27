
from magelang.lang.rust.cst import *
from magelang.treespec import Specs, TokenSpec

def generate_tree(
    specs: Specs,
    prefix = ''
) -> RustSourceFile:

    items = []

    for spec in specs:
        if isinstance(spec, TokenSpec):
            items.append(RustStructItem(pub_keyword=RustPubKeyword(), name=spec.name, fields=[]))

    return RustSourceFile(items=items)
