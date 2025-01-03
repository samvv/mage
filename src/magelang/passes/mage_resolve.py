
from magelang.lang.mage.ast import *

def mage_resolve(grammar: MageGrammar) -> MageGrammar:

    def init_element(element: MageModuleElement) -> None:
        if isinstance(element, MageModule):
            if element.symbol is None:
                element.symbol = Symbol(SymbolType.module)
                element.symbol.definition = element
            for element_2 in element.elements:
                init_element(element_2)
        elif isinstance(element, MageRule):
            if element.symbol is None:
                element.symbol = Symbol(SymbolType.rule)
                element.symbol.definition = element
        else:
            assert_never(element)

    for element in grammar.elements:
        init_element(element)

    stack: list[MageGrammar | MageModule] = [ grammar ]

    def lookup_rule(module_path: list[str], name: str) -> MageRule | None:
        if not module_path:
            for module in reversed(stack):
                rule = module.lookup(name)
                if rule is not None:
                    return rule
        else:
            root_module_name = module_path[0]
            root_module: MageModule | None = None
            for module in reversed(stack):
                module_2 = module.lookup_module(root_module_name)
                if module_2 is not None:
                    root_module = module_2
                    break
            if root_module is None:
                return None
            parent_module = root_module
            for module_name in module_path[1:]:
                parent_module = parent_module.lookup_module(module_name)
                if parent_module is None:
                    return None
            return parent_module.lookup(name)

    def visit_expr(expr: MageExpr) -> None:
        if isinstance(expr, MageRefExpr):
            rule = lookup_rule(expr.module_path, expr.name)
            expr.symbol = rule and rule.symbol
            return
        for_each_direct_child_expr(expr, visit_expr)

    def visit_element(element: MageModuleElement) -> None:
        if isinstance(element, MageModule):
            stack.append(element)
            for element in element.elements:
                visit_element(element)
            stack.pop()
        elif isinstance(element, MageRule):
            if element.expr is not None:
                visit_expr(element.expr)
        else:
            assert_never(element)

    for element in grammar.elements:
        visit_element(element)

    return grammar
