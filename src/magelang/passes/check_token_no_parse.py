
from magelang.ast import *

def check_token_no_parse(grammar: Grammar) -> Grammar:

    def references_pub_rule(expr: Expr) -> bool:
        if isinstance(expr, RefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None:
                return True # FIXME maybe return False?
            if rule.is_public:
                return True
            if rule.is_extern:
                return False
            assert(rule.expr is not None)
            return references_pub_rule(rule.expr)
        if isinstance(expr, SeqExpr) \
                or isinstance(expr, ChoiceExpr):
            for element in expr.elements:
                if references_pub_rule(element):
                    return True
            return False
        if isinstance(expr, ListExpr):
            return references_pub_rule(expr.element) \
                or references_pub_rule(expr.separator)
        if isinstance(expr, RepeatExpr) or isinstance(expr, LookaheadExpr):
            return references_pub_rule(expr.expr)
        if isinstance(expr, LitExpr) \
                or isinstance(expr, CharSetExpr):
            return False
        raise RuntimeError(f'unexpected node {expr}')

    for rule in grammar.rules:
        if grammar.is_token_rule(rule) and rule.expr is not None and references_pub_rule(rule.expr):
            print(f"Error: token rule '{rule.name}' references another rule marked with 'pub'.")

    return grammar
