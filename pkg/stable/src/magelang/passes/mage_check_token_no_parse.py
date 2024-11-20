
from magelang.logging import error
from magelang.lang.mage.ast import *

def mage_check_token_no_parse(grammar: MageGrammar) -> MageGrammar:

    def references_pub_rule(expr: MageExpr) -> bool:
        if isinstance(expr, MageRefExpr):
            rule = grammar.lookup(expr.name)
            if rule is None:
                return True # FIXME maybe return False?
            if rule.is_public:
                return True
            if rule.is_extern:
                return False
            assert(rule.expr is not None)
            return references_pub_rule(rule.expr)
        if isinstance(expr, MageSeqExpr) \
                or isinstance(expr, MageChoiceExpr):
            for element in expr.elements:
                if references_pub_rule(element):
                    return True
            return False
        if isinstance(expr, MageListExpr):
            return references_pub_rule(expr.element) \
                or references_pub_rule(expr.separator)
        if isinstance(expr, MageRepeatExpr) or isinstance(expr, MageLookaheadExpr):
            return references_pub_rule(expr.expr)
        if isinstance(expr, MageLitExpr) \
                or isinstance(expr, MageCharSetExpr):
            return False
        if isinstance(expr, MageHideExpr):
            return references_pub_rule(expr.expr)
        assert_never(expr)

    for rule in grammar.rules:
        if grammar.is_token_rule(rule) and rule.expr is not None and references_pub_rule(rule.expr):
            error(f"token rule '{rule.name}' references another rule marked with 'pub'.")

    return grammar
