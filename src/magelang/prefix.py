
from typing import assert_never, cast

from .ast import ChoiceExpr, Grammar, Expr, LitExpr, Rule, SeqExpr

type Edge = str

class Prefix:

    def  __init__(self, exps: list[Expr] | None = None) -> None:
        if exps is None:
            exps = []
        self.exps = exps
        self.prefixes: Prefixes | None = None

    def add_expr(self, expr: Expr) -> None:
        self.exps.append(expr)

    def nest(self) -> 'Prefixes':
        if self.prefixes is None:
            self.prefixes = Prefixes()
        return self.prefixes

Prefixes = dict[Edge, Prefix];

def transform(grammar: Grammar) -> Grammar:

    global_prefixes = Prefixes()

    def populate(rule: Rule) -> None:
        prefixes = global_prefixes
        def visit(expr: Expr, is_last: bool) -> None:
            nonlocal prefixes
            if isinstance(expr, LitExpr):
                prefix = None
                for ch in expr.text:
                    if ch not in prefixes:
                        prefixes[ch] = Prefix()
                    prefix = prefixes[ch]
                    prefixes = prefix.nest()
                if is_last:
                    cast(Prefix, prefix).add_expr(expr)
            if isinstance(expr, SeqExpr):
                for i, element in enumerate(expr.elements):
                    visit(element, i == len(expr.elements)-1)
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

    def visit(prefixes: Prefixes) -> Expr:
        elements = []
        for edge, data in prefixes.items():
            seq_elements = []
            seq_elements.append(build_expr(edge))
            choice_elements = []
            for expr in data.exps:
                choice_elements.append(expr)
            if data.prefixes is not None:
                choice_elements.append(visit(data.prefixes))
            seq_elements.append(ChoiceExpr(choice_elements))
            elements.append(SeqExpr(seq_elements))
        return ChoiceExpr(elements)

    return Grammar([ Rule(True, True, '$token', visit(global_prefixes))])
