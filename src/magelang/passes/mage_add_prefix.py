
from magelang.lang.mage.ast import *

def mage_add_prefix(grammar: MageGrammar, prefix: str) -> MageGrammar:

    def rename(name: str) -> str:
        return prefix + name

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageRefExpr):
            return expr.derive(name=rename(expr.name))
        return rewrite_each_child_expr(expr, rewrite_expr)

    def visit_rule(rule: MageRule) -> MageRule:
        expr = rewrite_expr(rule.expr) if rule.expr is not None else None
        return MageRule(comment=rule.comment, decorators=rule.decorators, flags=rule.flags, name=rename(rule.name), type_name=rule.type_name, expr=expr)

    return MageGrammar(rules=list(visit_rule(rule) for rule in grammar.rules))

