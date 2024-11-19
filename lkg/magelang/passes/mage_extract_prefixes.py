
from typing import assert_never, cast

from magelang.lang.mage.ast import *

type Edge = str

class Prefix:

    def  __init__(self, rules: list[MageRule] | None = None) -> None:
        if rules is None:
            rules = []
        self.rules = rules
        self.prefixes: Prefixes | None = None

    def add_rule(self, rule: MageRule) -> None:
        self.rules.append(rule)

    def nest(self) -> 'Prefixes':
        if self.prefixes is None:
            self.prefixes = Prefixes()
        return self.prefixes

Prefixes = dict[Edge, Prefix];

# FIXME make this transform target all ChoiceExpr
def mage_extract_prefixes(grammar: MageGrammar) -> MageGrammar:

    global_prefixes = Prefixes()

    def populate(rule: MageRule) -> None:
        prefixes = global_prefixes
        def visit(expr: MageExpr, is_last: bool) -> bool:
            nonlocal prefixes
            if isinstance(expr, MageLitExpr):
                prefix = None
                for ch in expr.text:
                    if ch not in prefixes:
                        prefixes[ch] = Prefix()
                    prefix = prefixes[ch]
                    prefixes = prefix.nest()
                if is_last:
                    cast(Prefix, prefix).add_rule(rule)
                return True
            if isinstance(expr, MageSeqExpr):
                for i, element in enumerate(expr.elements):
                    if not visit(element, i == len(expr.elements)-1):
                        return False
                return True
            if isinstance(expr, MageChoiceExpr):
                can_continue = True
                for element in expr.elements:
                    if not visit(element, is_last):
                        can_continue = False
                return can_continue
            if isinstance(expr, MageRepeatExpr) \
                or isinstance(expr, MageRefExpr):
                return False
            raise RuntimeError(f'unexpected {expr}')
        if rule.expr is not None:
            visit(rule.expr, True)

    def char_at(expr: MageExpr, i: int) -> str | None:
        if isinstance(expr, MageSeqExpr):
            for child in expr.elements:
                char = char_at(child, i)
                if char is not None:
                    return char
        if isinstance(expr, MageLitExpr):
            if i < len(expr.text):
                return expr.text[i]

    for rule in grammar.rules:
        populate(rule)

    def build_expr(edge: Edge) -> MageExpr:
        if isinstance(edge, str):
            return MageLitExpr(text=edge)
        assert_never(edge)

    def generate(prefixes: Prefixes) -> MageExpr:
        elements = []
        for edge, data in prefixes.items():
            seq_elements = []
            seq_elements.append(build_expr(edge))
            # choice_elements = []
            # for rule in data.rules:
            #     expr.rules.append(rule)
            if data.prefixes is not None and len(data.prefixes) > 0:
                seq_elements.append(generate(data.prefixes))
            # seq_elements.append(ChoiceExpr(choice_elements))
            expr = MageSeqExpr(elements=seq_elements)
            expr.rules = data.rules
            elements.append(expr)
        return MageChoiceExpr(elements=elements)

    return MageGrammar([ MageRule(flags=PUBLIC | FORCE_TOKEN, name='$token', expr=generate(global_prefixes))])
