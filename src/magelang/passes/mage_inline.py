
from magelang.lang.mage.ast import *
from magelang.lang.mage.emitter import *

def mage_inline(grammar: MageGrammar) -> MageGrammar:

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageRefExpr):
            rule = nonnull(expr.symbol).definition
            assert(isinstance(rule, MageRule))
            if rule is None or rule.is_public or rule.is_extern or rule.expr is None:
                return expr
            new_expr = rule.expr.derive(label=expr.label or rule.name)
            transfer_symbols(rule.expr, new_expr)
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
                return element.derive(expr=new_expr)
            return element
        elif isinstance(element, MageModule):
            return rewrite_module(element, rewrite_element)
        else:
            assert_never(element)

    def transfer_symbols(old_expr: MageExpr, new_expr: MageExpr) -> None:
        if isinstance(old_expr, MageRefExpr) and isinstance(new_expr, MageRefExpr):
            new_expr.symbol = old_expr.symbol

    return rewrite_module(grammar, rewrite_element)

