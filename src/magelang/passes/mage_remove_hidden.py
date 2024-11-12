
from magelang.lang.mage.ast import *

def mage_remove_hidden(grammar: MageGrammar) -> MageGrammar:
    """
    Remove hide expressions from the grammar and replace them with the empty string.

    Use simplify() to actually eliminate these empty sequences.
    """

    def filter_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageHideExpr):
            return MageSeqExpr([])
        return rewrite_each_child_expr(expr, filter_expr)

    new_rules = list[MageRule]()

    for rule in grammar.rules:
        if rule.expr is None:
            new_rules.append(rule)
        else:
            new_rules.append(rule.derive(expr=filter_expr(rule.expr)))

    return MageGrammar(new_rules)
