
from functools import cache
import math
from typing import Callable, Generator, TypeVar

from sweetener import BaseNode, warn, write_excerpt

from .util import nonnull

class Node(BaseNode):
    pass

class Expr(Node):
    label: str | None = None
    rules: list['Rule'] = []

class LitExpr(Expr):
    text: str

class RefExpr(Expr):
    name: str

class LookaheadExpr(Expr):
    expr: Expr
    is_negated: bool

class CharSetExpr(Expr):
    elements: list[str | tuple[str, str]]
    ci: bool
    invert: bool

class ChoiceExpr(Expr):
    elements: list[Expr]

class SeqExpr(Expr):
    elements: list[Expr]

class ListExpr(Expr):
    element: Expr
    separator: Expr

class HideExpr(Expr):
    expr: Expr

POSINF = math.inf

class RepeatExpr(Expr):
    min: int | float
    max: int | float
    expr: Expr

class Decorator(Node):
    name: str
    args: list[str | int]

EXTERN = 1
PUBLIC = 2
FORCE_TOKEN  = 4

class Rule(Node):
    decorators: list[Decorator]
    flags: int
    name: str
    expr: Expr | None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._references_public_rule = False

    @property
    def is_public(self) -> bool:
        return (self.flags & PUBLIC) > 0

    @property
    def is_extern(self) -> bool:
        return (self.flags & EXTERN) > 0

    @property
    def is_token(self) -> bool:
        return (self.flags & FORCE_TOKEN) > 0

    def has_decorator(self, name: str) -> bool:
        for decorator in self.decorators:
            if decorator.name == name:
                return True
        return False

class Grammar(Node):

    rules: list[Rule]

    def __init__(self, rules):
        super().__init__(rules)
        self._rules_by_name = dict()
        for rule in rules:
            self._rules_by_name[rule.name] = rule

    def is_fragment(self, rule: Rule) -> bool:
        return not rule.is_public #and (rule.is_extern or not self._references_pub_rule(nonnull(rule.expr)))

    def _references_pub_rule(self, expr: Expr) -> bool:
        if isinstance(expr, RefExpr):
            rule = self.lookup(expr.name)
            if rule.is_public:
                return True
            if rule.is_extern:
                return False
            assert(rule.expr is not None)
            return self._references_pub_rule(rule.expr)
        if isinstance(expr, SeqExpr) \
                or isinstance(expr, ChoiceExpr):
            for element in expr.elements:
                if self._references_pub_rule(element):
                    return True
            return False
        if isinstance(expr, RepeatExpr):
            return self._references_pub_rule(expr.expr)
        if isinstance(expr, LookaheadExpr):
            return self._references_pub_rule(expr.expr)
        if isinstance(expr, LitExpr) \
                or isinstance(expr, CharSetExpr):
            return False
        raise RuntimeError(f'unexpected node {expr}')

    @cache
    def is_token_rule(self, rule: Rule) -> bool:
        if rule.is_extern:
            return rule.is_token
        assert(rule.expr is not None)
        return rule.is_public and not self._references_pub_rule(rule.expr)

    def is_parse_rule(self, rule: Rule) -> bool:
        if rule.is_extern:
            return not rule.is_token
        return rule.is_public and not self.is_token_rule(rule)

    def get_token_rules(self) -> Generator[Rule, None, None]:
        for rule in self.rules:
            if self.is_token_rule(rule):
                yield rule

    def get_parse_rules(self) -> Generator[Rule, None, None]:
        for rule in self.rules:
            if self.is_parse_rule(rule):
                yield rule

    def lookup(self, name) -> Rule:
        if name not in self._rules_by_name:
            raise RuntimeError(f"a rule named '{name}' was not found in the current grammar")
        return self._rules_by_name[name]

def for_each_expr(node: Expr, proc: Callable[[Expr], None]) -> None:
    if isinstance(node, LitExpr) or isinstance(node, CharSetExpr) or isinstance(node, RefExpr):
        return
    if isinstance(node, RepeatExpr) or isinstance(node, LookaheadExpr) or isinstance(node, HideExpr):
        proc(node.expr)
        return
    if isinstance(node, ListExpr):
        proc(node.element)
        proc(node.separator)
        return
    if isinstance(node, ChoiceExpr) or isinstance(node, SeqExpr):
        for element in node.elements:
            proc(element)
        return
    raise RuntimeError(f'unexpected {node}')
