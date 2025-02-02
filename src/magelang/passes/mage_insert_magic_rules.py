
from magelang.lang.mage.ast import POSINF, PUBLIC, Decorator, MageCharSetExpr, MageChoiceExpr, MageExpr, MageGrammar, MageRefExpr, MageRepeatExpr, MageRule, MageSeqExpr
from magelang.manager import declare_pass

any_syntax_rule_name = 'syntax'
any_keyword_rule_name = 'keyword'
any_node_rule_name = 'node'
any_token_rule_name = 'token'

@declare_pass()
def mage_insert_magic_rules(grammar: MageGrammar) -> MageGrammar:

    new_elements = list(grammar.elements)
    syntax_rules = []

    keyword_rules = list[MageExpr](MageRefExpr(rule.name) for rule in grammar.rules if rule.is_keyword)
    if keyword_rules:
        new_elements.append(MageRule(
            name=any_keyword_rule_name,
            expr=MageChoiceExpr(keyword_rules),
            flags=PUBLIC
        ))

    token_rules = list[MageExpr](MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_token_rule(rule))
    if token_rules:
        new_elements.append(MageRule(
            name=any_token_rule_name,
            expr=MageChoiceExpr(token_rules),
            flags=PUBLIC
        ))
        syntax_rules.append(MageRefExpr(any_token_rule_name))

    node_rules = list[MageExpr](MageRefExpr(rule.name) for rule in grammar.rules if grammar.is_parse_rule(rule) and not grammar.is_variant_rule(rule))
    if node_rules:
        new_elements.append(MageRule(
            name=any_node_rule_name,
            expr=MageChoiceExpr(node_rules),
            flags=PUBLIC
        ))
        syntax_rules.append(MageRefExpr(any_node_rule_name))

    new_elements.append(MageRule(
        name=any_syntax_rule_name,
        expr=MageChoiceExpr(syntax_rules),
        flags=PUBLIC,
    ))

    if grammar.keyword_rule is None:
        new_elements.append(MageRule(
            decorators=[ Decorator('keyword') ],
            name='__keyword',
            expr=MageSeqExpr([ MageCharSetExpr([ ('a', 'z') ], ci=True), MageRepeatExpr(MageCharSetExpr([ ('a', 'z'), ('0', '9') ], ci=True), min=0, max=POSINF) ]),
        ))

    return grammar.derive(elements=new_elements)
