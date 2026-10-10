from pathlib import Path
import json
from typing import TypeVar, cast

from magelang.constants import DEFAULT_MAX_NAMED_CHARS
from magelang.util import NameGenerator
from magelang.helpers import lit_to_name
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

    def rewrite_rule(rule: MageRule) -> MageRule:

        assert(rule.expr is not None)
        generate_field_name = NameGenerator('field', hide_first=False)

        def rewrite_expr(expr: MageExpr) -> MageExpr:
            if isinstance(expr, MageLitExpr):
                name = lit_to_name(expr.text, grammar=grammar, max_named_chars=max_named_chars)
                if name is None:
                    name = generate_field_name()
                if expr.text not in literal_to_rule_name:
                    literal_to_rule_name[expr.text] = name
                return MageRefExpr(name, parent=expr.parent, span=expr.span, decorators=expr.decorators)
            return rewrite_each_child_expr(expr, rewrite_expr)

        return rule.derive(expr=rewrite_expr(rule.expr))

    for element in grammar.elements:
        if isinstance(element, MageRule) and element.is_parse and element.expr is not None:
            new_element = rewrite_rule(element)
        else:
            new_element = element
        new_rules.append(new_element)

    for literal in reversed(sorted(literal_to_rule_name.keys())):
        name = literal_to_rule_name[literal]
        flags = PUBLIC | FORCE_TOKEN
        new_literal_rules.append(MageRule(flags=flags, name=name, expr=MageLitExpr(literal), type_name=string_rule_type))

    return grammar.derive(elements=new_literal_rules + new_rules)

