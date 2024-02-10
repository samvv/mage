
from functools import cache
import math
from typing import Generator, List, Union, Tuple

from sweetener import BaseNode

class Node(BaseNode):
    pass

class Expr(Node):
    pass

class LitExpr(Expr):
    text: str

class RefExpr(Expr):
    name: str

class CharSetExpr(Expr):
    elements: List[Union[str, Tuple[str, str]]]

class ChoiceExpr(Expr):
    elements: List[Expr]

class SeqExpr(Expr):
    elements: List[Expr]

POSINF = math.inf

class RepeatExpr(Expr):
    min: Union[int, float]
    max: Union[int, float]
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

    rules: List[Rule]

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
            if isinstance(expr, LitExpr) \
                    or isinstance(expr, CharSetExpr):
                return True
            raise RuntimeError(f'unexpected node {expr}')
        return rule.is_public and visit(rule.expr)

    def get_token_rules(self) -> Generator[Rule, None, None]:
        for rule in self.rules:
            if self._is_token_rule(rule):
                yield rule

    def lookup(self, name):
        if name not in self._rules_by_name:
            raise RuntimeError(f"a rule named '{name}' was not found in the current grammar")
        return self._rules_by_name[name]

