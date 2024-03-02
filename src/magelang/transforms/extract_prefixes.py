
from typing import assert_never, cast

from ..ast import *

type Edge = str

class Prefix:

    def  __init__(self, rules: list[Rule] | None = None) -> None:
        if rules is None:
            rules = []
        self.rules = rules
        self.prefixes: Prefixes | None = None

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def nest(self) -> 'Prefixes':
        if self.prefixes is None:
            self.prefixes = Prefixes()
        return self.prefixes

Prefixes = dict[Edge, Prefix];

# FIXME make this transform target all ChoiceExpr
def extract_prefixes(grammar: Grammar) -> Grammar:

    global_prefixes = Prefixes()

    def populate(rule: Rule) -> None:
        prefixes = global_prefixes
        def visit(expr: Expr, is_last: bool) -> bool:
            nonlocal prefixes
            if isinstance(expr, LitExpr):
                prefix = None
                for ch in expr.text:
                    if ch not in prefixes:
                        prefixes[ch] = Prefix()
                    prefix = prefixes[ch]
                    prefixes = prefix.nest()
                if is_last:
                    cast(Prefix, prefix).add_rule(rule)
                return True
            if isinstance(expr, SeqExpr):
                for i, element in enumerate(expr.elements):
                    if not visit(element, i == len(expr.elements)-1):
                        return False
                return True
            if isinstance(expr, ChoiceExpr):
                can_continue = True
                for element in expr.elements:
                    if not visit(element, is_last):
                        can_continue = False
                return can_continue
            if isinstance(expr, RepeatExpr) \
                or isinstance(expr, RefExpr):
                return False
            raise RuntimeError(f'unexpected {expr}')
        visit(rule.expr, True)

    def char_at(expr: Expr, i: int) -> str | None:
        if isinstance(expr, SeqExpr):
            for child in expr.elements:
                char = char_at(child, i)
                if char is not None:
                    return char
        if isinstance(expr, LitExpr):
            if i < len(expr.text):
                return expr.text[i]

    for rule in grammar.rules:
        populate(rule)

    def build_expr(edge: Edge) -> Expr:
        if isinstance(edge, str):
            return LitExpr(edge)
        assert_never(edge)

    def generate(prefixes: Prefixes) -> Expr:
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
            expr = SeqExpr(seq_elements)
            expr.rules = data.rules
            elements.append(expr)
        return ChoiceExpr(elements)

    return Grammar([ Rule(True, True, '$token', generate(global_prefixes))])
