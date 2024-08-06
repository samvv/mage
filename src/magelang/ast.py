
from functools import cache
import math
from typing import TYPE_CHECKING, Callable, Generator

from sweetener import BaseNode

if TYPE_CHECKING:
    from .repr import Type

class Node(BaseNode):
    pass

type Expr = LitExpr | RefExpr | CharSetExpr | LookaheadExpr | ChoiceExpr | SeqExpr | HideExpr | ListExpr | RepeatExpr

class ExprBase(Node):

    label: str | None = None

    def __init__(self, *args, rules: list['Rule'] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if rules is None:
            rules = []
        self.rules: list['Rule'] = rules
        self.field_name: str | None = None
        self.field_type: Type | None = None
        self.action: Rule | None = None

class LitExpr(ExprBase):
    text: str

class RefExpr(ExprBase):
    name: str

class LookaheadExpr(ExprBase):
    expr: Expr
    is_negated: bool

type CharSetElement = str | tuple[str, str]

class CharSetExpr(ExprBase):
    elements: list[CharSetElement]
    ci: bool
    invert: bool

class ChoiceExpr(ExprBase):
    elements: list[Expr]

class SeqExpr(ExprBase):
    elements: list[Expr]

class ListExpr(ExprBase):
    element: Expr
    separator: Expr

class HideExpr(ExprBase):
    expr: Expr

POSINF = math.inf

class RepeatExpr(ExprBase):
    min: int
    max: int | float
    expr: Expr

class Decorator(Node):
    name: str
    args: list[str | int]

EXTERN = 1
PUBLIC = 2
FORCE_TOKEN  = 4

unit_rule_name = 'void'
string_rule_type = 'String'
integer_rule_type = 'Integer'

builtin_types = {
    unit_rule_name,
    string_rule_type,
    integer_rule_type,
}

class Rule(Node):
    comment: str | None
    decorators: list[Decorator]
    flags: int
    name: str
    type_name: str | None
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

    @property
    def is_skip(self) -> bool:
        return self.has_decorator('skip')

    @property
    def is_wrap(self) -> bool:
        return self.has_decorator('wrap')

class Grammar(Node):

    rules: list[Rule]

    def __init__(self, rules):
        super().__init__(rules)
        self._rules_by_name = dict[str, Rule]()
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
        if isinstance(expr, ListExpr):
            return self._references_pub_rule(expr.element) \
                or self._references_pub_rule(expr.separator)
        if isinstance(expr, RepeatExpr) or isinstance(expr, LookaheadExpr):
            return self._references_pub_rule(expr.expr)
        if isinstance(expr, LitExpr) \
                or isinstance(expr, CharSetExpr):
            return False
        raise RuntimeError(f'unexpected node {expr}')

    @property
    @cache
    def skip_rule(self) -> Rule | None:
        for rule in self.rules:
            if rule.is_skip:
                return rule

    @cache
    def is_token_rule(self, rule: Rule) -> bool:
        return rule.is_token
        # if rule.is_extern:
        #     return rule.is_token
        # assert(rule.expr is not None)
        # return rule.is_public and not self._references_pub_rule(rule.expr)

    def is_static_token(self, expr: Expr):
        if isinstance(expr, RefExpr):
            rule = self.lookup(expr.name)
            if rule.is_extern:
                return False
            assert(rule.expr is not None)
            return self.is_static_token(rule.expr)
        if isinstance(expr, LitExpr):
            return True
        if isinstance(expr, CharSetExpr):
            # FIXME should I check whether the range contains only one char?
            return False
        if isinstance(expr, SeqExpr):
            return all(self.is_static_token(element) for element in expr.elements)
        if isinstance(expr, ChoiceExpr):
            # FIXME should I check whether the choices are actually different?
            return False
        if isinstance(expr, RepeatExpr):
            if expr.min != expr.max:
                return False
            return self.is_static_token(expr.expr)
        if isinstance(expr, LookaheadExpr):
            # Lookahead has no effect on what (non-)static characters are generated
            return True
        raise RuntimeError(f'unexpected {expr}')

    def is_parse_rule(self, rule: Rule) -> bool:
        if rule.is_extern:
            return not rule.is_token
        return rule.is_public and not self.is_token_rule(rule)

    def is_variant(self, rule: Rule) -> bool:
        if rule.is_extern or rule.is_wrap:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(rule.expr is not None)
        return isinstance(rule.expr, ChoiceExpr)

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

def rewrite_expr(expr: Expr, proc: Callable[[Expr], Expr | None]) -> Expr:

    def visit(expr: Expr) -> Expr:

        updated = proc(expr)
        if updated is not None:
            return updated

        if isinstance(expr, LitExpr) or isinstance(expr, CharSetExpr) or isinstance(expr, RefExpr):
            return expr
        if isinstance(expr, RepeatExpr):
            new_expr = visit(expr.expr)
            if new_expr == expr.expr:
                return expr
            return RepeatExpr(min=expr.min, max=expr.max, expr=new_expr, rules=expr.rules, label=expr.label)
        if isinstance(expr, LookaheadExpr):
            new_expr = visit(expr.expr)
            if new_expr == expr.expr:
                return expr
            return LookaheadExpr(expr=new_expr, is_negated=expr.is_negated, rules=expr.rules, label=expr.label)
        if isinstance(expr, HideExpr):
            new_expr = visit(expr.expr)
            if new_expr == expr.expr:
                return expr
            return HideExpr(expr=new_expr, rules=expr.rules, label=expr.label)
        if isinstance(expr, ListExpr):
            new_element = visit(expr.element)
            new_separator = visit(expr.separator)
            if new_element == expr.element and new_separator == expr.separator:
                return expr
            return ListExpr(element=new_element, separator=new_separator, rules=expr.rules, label=expr.label)
        if isinstance(expr, ChoiceExpr):
            new_elements = []
            changed = False
            for element in expr.elements:
                new_element = visit(element)
                if new_element != element:
                    changed = True
                new_elements.append(new_element)
            if not changed:
                return expr
            return ChoiceExpr(elements=new_elements, rules=expr.rules, label=expr.label)
        if isinstance(expr, SeqExpr):
            new_elements = []
            changed = False
            for element in expr.elements:
                new_element = visit(element)
                if new_element != element:
                    changed = True
                new_elements.append(new_element)
            if not changed:
                return expr
            return SeqExpr(elements=new_elements, rules=expr.rules, label=expr.label)
        raise RuntimeError(f'unexpected {expr}')

    return visit(expr)

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
