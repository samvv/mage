
from magelang.lang.mage.ast import *
from magelang.lang.mage.emitter import *

def mage_inline(grammar: MageGrammar) -> MageGrammar:

    new_rules = []

    def inline_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None or rule.is_public or rule.is_extern:
                return expr
            assert(rule.expr is not None)
            new_expr = rule.expr.derive(label=expr.label or rule.name)
            return inline_expr(new_expr)
        return rewrite_each_child_expr(expr, inline_expr)

    for rule in grammar.rules:
        if rule.is_extern:
            new_rules.append(rule)
        elif rule.is_public or rule.is_skip:
            assert(rule.expr is not None)
            new_rules.append(rule.derive(
                expr=inline_expr(rule.expr)
            ))

    return MageGrammar(new_rules)
