
from magelang.lang.mage.ast import MageExpr, MageGrammar, MageRefExpr, MageSeqExpr, rewrite_each_child_expr

def mage_insert_skip(grammar: MageGrammar) -> MageGrammar:

    assert(grammar.skip_rule is not None)
    skip_name = grammar.skip_rule.name

    def rewrite_expr(expr: MageExpr) -> MageExpr:

        def recurse(expr: MageExpr) -> MageExpr:
            return rewrite_each_child_expr(expr, rewrite_expr)

        if isinstance(expr, MageSeqExpr):
            new_elements = []
            iterator = iter(expr.elements)
            try:
                element = next(iterator)
            except StopIteration:
                return expr
            new_elements.append(recurse(element))
            while True:
                try:
                    element = next(iterator)
                except StopIteration:
                    break
                new_elements.append(MageRefExpr(skip_name))
                new_elements.append(recurse(element))
            return expr.derive(elements=new_elements)

        return rewrite_each_child_expr(expr, rewrite_expr)

    new_rules = []

    for rule in grammar.rules:
        if rule.expr is None:
            new_rule = rule
        else:
            new_rule = rule.derive(expr=rewrite_expr(rule.expr))
        new_rules.append(new_rule)

    return MageGrammar(rules=new_rules)
