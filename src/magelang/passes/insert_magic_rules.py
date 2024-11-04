
from intervaltree.intervaltree import warn
from magelang.ast import PUBLIC, MageChoiceExpr, MageGrammar, MageRefExpr, MageRule

any_token_rule_name = 'token'

def insert_magic_rules(grammar: MageGrammar) -> MageGrammar:

    rules = list(grammar.rules)

    rules.append(MageRule(
        name='keyword',
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if rule.is_keyword)),
        flags=PUBLIC
    ))

    rules.append(MageRule(
        name=any_token_rule_name,
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_token_rule(rule))),
        flags=PUBLIC
    ))

    rules.append(MageRule(
        name='node',
        expr=MageChoiceExpr(list(MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_parse_rule(rule) and not grammar.is_variant_rule(rule))),
        flags=PUBLIC
    ))

    rules.append(MageRule(
        name='syntax',
        expr=MageChoiceExpr([ MageRefExpr('node'), MageRefExpr('token') ]),
        flags=PUBLIC,
    ))

    return MageGrammar(rules)
