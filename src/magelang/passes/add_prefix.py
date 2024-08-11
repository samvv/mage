
from ..ast import *

def add_prefix(grammar: Grammar, prefix: str) -> Grammar:

    def transform(name: str) -> str:
        return prefix + name

    def rewrite(expr: Expr) -> Expr | None:
        if isinstance(expr, RefExpr):
            return RefExpr(name=transform(expr.name), rules=expr.rules)

    def visit_rule(rule: Rule) -> Rule:
        expr = rewrite_expr(rule.expr, rewrite) if rule.expr is not None else None
        return Rule(comment=rule.comment, decorators=rule.decorators, flags=rule.flags, name=transform(rule.name), type_name=rule.type_name, expr=expr)

    return Grammar(rules=list(visit_rule(rule) for rule in grammar.rules))

