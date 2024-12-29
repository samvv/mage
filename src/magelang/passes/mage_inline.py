
from magelang.lang.mage.ast import *
from magelang.lang.mage.emitter import *

def mage_inline(grammar: MageGrammar) -> MageGrammar:

    def inline_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name) # FIXME This lookup may fail when inside a module
            if rule is None or rule.is_public or rule.is_extern:
                return expr
            assert(rule.expr is not None)
            new_expr = rule.expr.derive(label=expr.label or rule.name)
            return inline_expr(new_expr)
        return rewrite_each_child_expr(expr, inline_expr)

    def rewrite_elements(elements: list[MageModuleElement]) -> list[MageModuleElement]:
        new_rules = []
        for element in elements:
            if isinstance(element, MageRule):
                if element.is_extern:
                    new_rules.append(element)
                elif element.is_public or element.is_skip:
                    assert(element.expr is not None)
                    new_rules.append(element.derive(
                        expr=inline_expr(element.expr)
                    ))
            elif isinstance(element, MageModule):
                new_rules.append(element.derive(elements=rewrite_elements(element.elements)))
            else:
                assert_never(element)
        return new_rules

    return grammar.derive(elements=rewrite_elements(grammar.elements))
