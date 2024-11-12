from pathlib import Path
import json

from magelang.eval import accepts
from magelang.lang.mage.ast import *

def mage_extract_literals(grammar: MageGrammar) -> MageGrammar:

    new_rules = []

    with open(Path(__file__).parent.parent / 'names.json', 'r') as f:
        names = json.load(f)

    literal_to_name: dict[str, str] = {}
    keywords = set[str]()

    token_counter = 0
    def generate_token_name() -> str:
        nonlocal token_counter
        name = f'token_{token_counter}'
        token_counter += 1
        return name

    def str_to_name(text: str) -> str | None:
        # If it's a single letter
        if len(text) == 1 and text.isalpha():
            # Letters such as 'i' and 'D' are not really keywords
            # They are represented with the lower_ or upper_ prefix
            return f'lower_{text}' if text.islower() else f'upper_{text.lower()}'
        # If the evaluation engine matches it as a keyword
        # FIXME Keyword detection should work with the @keyword decorator
        keyword_rule = grammar.keyword_rule
        if keyword_rule is not None and keyword_rule.expr is not None and accepts(keyword_rule.expr, text, grammar):
            name = f'{text}_keyword'
            keywords.add(name)
            return name
        if len(text) <= 4:
            # First try to name the entire word
            if text in names:
                return names[text]
            # Fall back to naming the individual characters
            return '_'.join(names[ch] for ch in text)

    def rewriter(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageLitExpr):
            name = str_to_name(expr.text)
            if name is None:
                name = generate_token_name()
            if expr.text not in literal_to_name:
                literal_to_name[expr.text] = name
            return MageRefExpr(name)
        return rewrite_each_child_expr(expr, rewriter)

    for rule in grammar.rules:
        if grammar.is_parse_rule(rule):
            assert(rule.expr is not None)
            new_rules.append(rule.derive(expr=rewriter(rule.expr)))
        else:
            new_rules.append(rule)

    for literal in reversed(sorted(literal_to_name.keys())):
        name = literal_to_name[literal]
        flags = PUBLIC | FORCE_TOKEN
        if name in keywords:
            flags |= FORCE_KEYWORD
        new_rules.append(MageRule(comment=None, decorators=[], flags=flags, name=name, expr=MageLitExpr(literal), type_name=string_rule_type))

    return MageGrammar(new_rules)

