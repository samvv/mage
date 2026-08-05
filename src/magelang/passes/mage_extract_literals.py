from magelang.constants import DEFAULT_MAX_NAMED_CHARS
from magelang.helpers import lit_to_name
from pathlib import Path
import json
from typing import TypeVar, cast

from magelang.lang.mage.ast import *
from magelang.manager import declare_pass

@declare_pass()
def mage_extract_literals(
    grammar: MageGrammar,
    max_named_chars: int = DEFAULT_MAX_NAMED_CHARS,
    enable_lexer: bool = False
) -> MageGrammar:

    new_rules = []
    new_literal_rules = []

    literal_to_rule_name = dict[str, str]()
    keyword_rule_names = set[str]()

    def rewrite_expr(expr: MageExpr) -> MageExpr:
        if isinstance(expr, MageLitExpr):
            is_keyword, name = lit_to_name(expr.text, grammar, max_named_chars=max_named_chars)
            if is_keyword:
                keyword_rule_names.add(name)
            if expr.text not in literal_to_rule_name:
                literal_to_rule_name[expr.text] = name
            return MageRefExpr(name, parent=expr.parent, span=expr.span, decorators=expr.decorators)
        return rewrite_each_child_expr(expr, rewrite_expr)

    for element in grammar.elements:
        if isinstance(element, MageRule) and element.is_parse:
            assert(element.expr is not None)
            new_rules.append(element.derive(expr=rewrite_expr(element.expr)))
            continue
        new_rules.append(element)

    for literal in reversed(sorted(literal_to_rule_name.keys())):
        name = literal_to_rule_name[literal]
        flags = PUBLIC | FORCE_TOKEN
        if name in keyword_rule_names:
            flags |= FORCE_KEYWORD
        new_literal_rules.append(MageRule(flags=flags, name=name, expr=MageLitExpr(literal), type_name=string_rule_type))

    return grammar.derive(elements=new_literal_rules + new_rules)

