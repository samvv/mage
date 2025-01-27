
from magelang.lang.mage.ast import POSINF, PUBLIC, Decorator, MageCharSetExpr, MageChoiceExpr, MageGrammar, MageRefExpr, MageRepeatExpr, MageRule, MageSeqExpr

any_syntax_rule_name = 'syntax'
any_keyword_rule_name = 'keyword'
any_node_rule_name = 'node'
any_token_rule_name = 'token'

def mage_insert_magic_rules(grammar: MageGrammar) -> MageGrammar:

    new_elements = list(grammar.elements)

    new_elements.append(MageRule(
        name=any_keyword_rule_name,
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if rule.is_keyword)),
        flags=PUBLIC
    ))

    new_elements.append(MageRule(
        name=any_token_rule_name,
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_token_rule(rule))),
        flags=PUBLIC
    ))

    new_elements.append(MageRule(
        name=any_node_rule_name,
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_parse_rule(rule) and not grammar.is_variant_rule(rule))),
        flags=PUBLIC
    ))

    new_elements.append(MageRule(
        name=any_syntax_rule_name,
        expr=MageChoiceExpr([ MageRefExpr('node'), MageRefExpr('token') ]),
        flags=PUBLIC,
    ))

    if grammar.keyword_rule is None:
        new_elements.append(MageRule(
            decorators=[ Decorator('keyword') ],
            name='__keyword',
            expr=MageSeqExpr([ MageCharSetExpr([ ('a', 'z') ], ci=True), MageRepeatExpr(MageCharSetExpr([ ('a', 'z'), ('0', '9') ], ci=True), min=0, max=POSINF) ]),
        ))

    return grammar.derive(elements=new_elements)
