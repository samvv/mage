
from magelang.lang.mage.ast import MageExpr, MageGrammar, MageRefExpr, MageRule, MageSeqExpr, rewrite_each_child_expr, rewrite_each_rule
from magelang.manager import declare_pass

@declare_pass()
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

    def rewrite_rule(rule: MageRule) -> MageRule:
        if rule.expr is None:
            return rule
        return rule.derive(expr=rewrite_expr(rule.expr))

    return rewrite_each_rule(grammar, rewrite_rule)
