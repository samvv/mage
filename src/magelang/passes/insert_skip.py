
from ..ast import Expr, Grammar, RefExpr, SeqExpr, rewrite_expr

def insert_skip(grammar: Grammar) -> Grammar:

    assert(grammar.skip_rule is not None)
    skip_name = grammar.skip_rule.name

    def rewriter(expr: Expr) -> Expr | None:
        if isinstance(expr, SeqExpr):
            new_elements = []
            iterator = iter(expr.elements)
            try:
                element = next(iterator)
            except StopIteration:
                return expr
            new_elements.append(rewrite(element))
            while True:
                try:
                    element = next(iterator)
                except StopIteration:
                    break
                new_elements.append(RefExpr(skip_name))
                new_elements.append(rewrite(element))
            return expr.derive(elements=new_elements)

    def rewrite(expr: Expr) -> Expr:
        return rewrite_expr(expr, rewriter)

    new_rules = []

    for rule in grammar.rules:
        if rule.expr is None:
            new_rule = rule
        else:
            new_rule = rule.derive(expr=rewrite(rule.expr))
        new_rules.append(new_rule)

    return Grammar(rules=new_rules)
