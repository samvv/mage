
from magelang.lang.mage.ast import PUBLIC, MageChoiceExpr, MageGrammar, MageRefExpr, MageRule

any_syntax_rule_name = 'syntax'
any_keyword_rule_name = 'keyword'
any_node_rule_name = 'node'
any_token_rule_name = 'token'

def mage_insert_magic_rules(grammar: MageGrammar) -> MageGrammar:

    rules = list(grammar.rules)

    rules.append(MageRule(
        name=any_keyword_rule_name,
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if rule.is_keyword)),
        flags=PUBLIC
    ))

    rules.append(MageRule(
        name=any_token_rule_name,
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_token_rule(rule))),
        flags=PUBLIC
    ))

    rules.append(MageRule(
        name=any_node_rule_name,
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_parse_rule(rule) and not grammar.is_variant_rule(rule))),
        flags=PUBLIC
    ))

    rules.append(MageRule(
        name=any_syntax_rule_name,
        expr=MageChoiceExpr([ MageRefExpr('node'), MageRefExpr('token') ]),
        flags=PUBLIC,
    ))

    return MageGrammar(rules)
