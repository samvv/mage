
from magelang.lang.mage.ast import *
from magelang.manager import declare_pass
from magelang.util import to_snake_case

# FIXME Reference expressions will point to the wrong module
@declare_pass()
def mage_flatten_grammars(grammar: MageGrammar) -> MageGrammar:

    def mangle(parent: str, name: str) -> str:
        return parent + '_' + name

    mode = 1

    new_elements = list[MageModuleElement]()

    def visit_module(node: MageModule) -> None:
        nonlocal mode

        for element in node.elements:
            if isinstance(element, MageRule):
                new_elements.append(element.derive(name=mangle(to_snake_case(node.name), element.name), mode=mode))
            elif isinstance(element, MageModule):
                visit_module(element)
            else:
                new_elements.append(element)

        mode += 1

    for element in grammar.elements:
        if isinstance(element, MageModule):
            visit_module(element)
        else:
            new_elements.append(element)

    return grammar.derive(elements=new_elements)
