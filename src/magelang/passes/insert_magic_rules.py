
from intervaltree.intervaltree import warn
from magelang.ast import PUBLIC, ChoiceExpr, Grammar, RefExpr, Rule

any_token_rule_name = 'token'

def insert_magic_rules(grammar: Grammar) -> Grammar:

    rules = list(grammar.rules)

    rules.append(Rule(
        name='keyword',
        expr=ChoiceExpr(list(RefExpr(rule.name) for rule in grammar.rules if rule.is_keyword)),
        flags=PUBLIC
    ))

    rules.append(Rule(
        name=any_token_rule_name,
        expr=ChoiceExpr(list(RefExpr(rule.name) for rule in grammar.rules if grammar.is_token_rule(rule))),
        flags=PUBLIC
    ))

    rules.append(Rule(
        name='node',
        expr=ChoiceExpr(list(RefExpr(rule.name) for rule in grammar.rules if grammar.is_parse_rule(rule) and not grammar.is_variant_rule(rule))),
        flags=PUBLIC
    ))

    rules.append(Rule(
        name='syntax',
        expr=ChoiceExpr([ RefExpr('node'), RefExpr('token') ]),
        flags=PUBLIC,
    ))

    return Grammar(rules)
