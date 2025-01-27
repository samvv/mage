from pathlib import Path
import json
from typing import TypeVar, cast

from magelang.eval import accepts
from magelang.lang.mage.ast import *
from magelang.analysis import is_tokenizable

T = TypeVar('T', bound=MageGrammar | MageModule)

def mage_extract_literals(
    grammar: MageGrammar,
    max_named_chars: int = 4,
) -> MageGrammar:

    enable_tokens = is_tokenizable(grammar)

    def rewrite_module(node: T) -> T:

        new_rules = []
        new_literal_rules = []

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
            keyword_rule = node.keyword_rule
            if keyword_rule is not None and keyword_rule.expr is not None and accepts(keyword_rule.expr, text, node):
                name = f'{text}_keyword'
                keywords.add(name)
                return name
            if len(text) <= max_named_chars:
                # First try to name the entire word
                if text in names:
                    return names[text]
                # Fall back to naming the individual characters
                return '_'.join(names[ch] for ch in text)

        def rewrite_expr(expr: MageExpr) -> MageExpr:
            if isinstance(expr, MageLitExpr):
                name = str_to_name(expr.text)
                if name is None:
                    name = generate_token_name()
                if expr.text not in literal_to_name:
                    literal_to_name[expr.text] = name
                return MageRefExpr(name)
            return rewrite_each_child_expr(expr, rewrite_expr)

        for element in node.elements:
            if isinstance(element, MageRule):
                if node.is_parse_rule(element):
                    assert(element.expr is not None)
                    new_rules.append(element.derive(expr=rewrite_expr(element.expr)))
                else:
                    new_rules.append(element)
            elif isinstance(element, MageModule):
                new_rules.append(rewrite_module(element))
            else:
                assert_never(element)

        for literal in reversed(sorted(literal_to_name.keys())):
            name = literal_to_name[literal]
            flags = PUBLIC
            if enable_tokens:
                flags |= FORCE_TOKEN
            if name in keywords:
                flags |= FORCE_KEYWORD
            new_literal_rules.append(MageRule(flags=flags, name=name, expr=MageLitExpr(literal), type_name=string_rule_type))

        return cast(T, node.derive(elements=new_literal_rules + new_rules))

    return rewrite_module(grammar)
