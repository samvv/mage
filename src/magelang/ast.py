
from functools import cache
import math
from typing import Generator

from sweetener import BaseNode

class Node(BaseNode):
    pass

class Expr(Node):

    label: str | None = None
    rules: list['Rule'] = []

    # def __init__(self, *args, rules: list['Rule'] | None = None, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)
    #     if rules is None:
    #         rules = []
    #     self.rules = rules

class LitExpr(Expr):
    text: str

class RefExpr(Expr):
    name: str

class LookaheadExpr(Expr):
    expr: Expr
    is_negated: bool

class CharSetExpr(Expr):
    elements: list[str | tuple[str, str]]

class ChoiceExpr(Expr):
    elements: list[Expr]

class SeqExpr(Expr):
    elements: list[Expr]

POSINF = math.inf

class RepeatExpr(Expr):
    min: int | float
    max: int | float
    expr: Expr

class Rule(Node):
    is_public: bool
    is_token: bool
    name: str
    expr: Expr

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._references_public_rule = False

class Grammar(Node):

    rules: list[Rule]

    def __init__(self, rules):
        super().__init__(rules)
        self._rules_by_name = dict()
        for rule in rules:
            self._rules_by_name[rule.name] = rule

    @cache
    def _is_token_rule(self, rule: Rule) -> bool:
        def visit(expr: Expr) -> bool:
            if isinstance(expr, RefExpr):
                rule = self.lookup(expr.name)
                if rule.is_public:
                    return False
                return visit(rule.expr)
            if isinstance(expr, SeqExpr) \
                    or isinstance(expr, ChoiceExpr):
                for element in expr.elements:
                    if not visit(element):
                        return False
                return True
            if isinstance(expr, RepeatExpr):
                return visit(expr.expr)
            if isinstance(expr, LookaheadExpr):
                return visit(expr.expr)
            if isinstance(expr, LitExpr) \
                    or isinstance(expr, CharSetExpr):
                return True
            raise RuntimeError(f'unexpected node {expr}')
        return rule.is_public and visit(rule.expr)

    def get_token_rules(self) -> Generator[Rule, None, None]:
        for rule in self.rules:
            if self._is_token_rule(rule):
                yield rule

    def get_parse_rules(self) -> Generator[Rule, None, None]:
        for rule in self.rules:
            if rule.is_public and not self._is_token_rule(rule):
                yield rule

    def lookup(self, name) -> Rule:
        if name not in self._rules_by_name:
            raise RuntimeError(f"a rule named '{name}' was not found in the current grammar")
        return self._rules_by_name[name]

