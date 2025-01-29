
# TODO extract union types and create 'anonymous' enumerations for these types

from magelang.lang.revolv.ast import *
from magelang.lang.rust import *
from magelang.manager import declare_pass

@declare_pass()
def revolv_to_rust(program: Program) -> RustSourceFile:

    items = []

    # TODO

    return RustSourceFile(items=items)

