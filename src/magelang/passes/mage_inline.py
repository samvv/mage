
from magelang.lang.mage.ast import *
from magelang.lang.mage.emitter import *

def mage_inline(grammar: MageGrammar) -> MageGrammar:

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageRefExpr):
            rule = nonnull(lookup_ref(expr))
            assert(isinstance(rule, MageRule))
            if rule is None or rule.is_public or rule.is_extern or rule.expr is None:
                return expr
            new_expr = rule.expr.derive(label=expr.label or rule.name)
            return rewrite_expr(new_expr)
        return rewrite_each_child_expr(expr, rewrite_expr)

    def rewrite_element(element: MageModuleElement) -> MageModuleElement:
        if isinstance(element, MageRule):
            if element.is_extern:
                return element
            if (element.is_public or element.is_skip) and element.expr is not None:
                new_expr = rewrite_expr(element.expr)
                if new_expr is element.expr:
                    return element
                new_element = element.derive(expr=new_expr)
                return new_element
            return element
        elif isinstance(element, MageModule):
            return rewrite_module(element, rewrite_element)
        else:
            assert_never(element)

    return rewrite_module(grammar, rewrite_element)

