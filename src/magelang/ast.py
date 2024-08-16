"""
Hand-written abstract syntax tree (AST) of the Mage grammar.

Also defines some visitors over Mage expressions and other useful procedures to
make handling the AST a bit easier.
"""

from functools import cache
import sys
from typing import TYPE_CHECKING, Callable, Generator, assert_never


if TYPE_CHECKING:
    from .treespec import Type


class Node:
    pass


type Expr = LitExpr | RefExpr | CharSetExpr | LookaheadExpr | ChoiceExpr | SeqExpr | HideExpr | ListExpr | RepeatExpr


class ExprBase(Node):

    def __init__(self, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        if rules is None:
            rules = []
        self.label = label
        self.rules = rules
        self.field_name = field_name
        self.field_type = field_type
        self.action = action # FIXME merge with `self.rules`


class LitExpr(ExprBase):

    def __init__(self, text: str, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.text = text

    def derive(self, text: str | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'LitExpr':
        if text is None:
            text = self.text
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return LitExpr(text=text, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)

class RefExpr(ExprBase):

    def __init__(self, name: str, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.name = name

    def derive(self, name: str | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'RefExpr':
        if name is None:
            name = self.name
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return RefExpr(name=name, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)


class LookaheadExpr(ExprBase):

    def __init__(self, expr: Expr, is_negated: bool, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.expr = expr
        self.is_negated = is_negated

    def derive(self, expr: Expr | None = None, is_negated: bool | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'LookaheadExpr':
        if expr is None:
            expr = self.expr
        if is_negated is None:
            is_negated = self.is_negated
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return LookaheadExpr(expr=expr, is_negated=is_negated, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)


type CharSetElement = str | tuple[str, str]


class CharSetExpr(ExprBase):

    def __init__(self, elements: list[CharSetElement], ci: bool, invert: bool, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.elements = elements
        self.ci = ci
        self.invert = invert

    def derive(self, elements: list[CharSetElement] | None = None, ci: bool | None = None, invert: bool | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'CharSetExpr':
        if elements is None:
            elements = self.elements
        if ci is None:
            ci = self.ci
        if invert is None:
            invert = self.invert
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return CharSetExpr(elements=elements, ci=ci, invert=invert, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)


class ChoiceExpr(ExprBase):

    def __init__(self, elements: list[Expr], label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.elements = elements

    def derive(self, elements: list[Expr] | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'ChoiceExpr':
        if elements is None:
            elements = self.elements
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return ChoiceExpr(elements=elements, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)


class SeqExpr(ExprBase):

    def __init__(self, elements: list[Expr], label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.elements = elements

    def derive(self, elements: list[Expr] | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'SeqExpr':
        if elements is None:
            elements = self.elements
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return SeqExpr(elements=elements, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)


class ListExpr(ExprBase):

    def __init__(self, element: Expr, separator: Expr, min_count: int, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.element = element
        self.separator = separator
        self.min_count = min_count

    def derive(self, element: Expr | None = None, separator: Expr | None = None, min_count: int | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'ListExpr':
        if element is None:
            element = self.element
        if separator is None:
            separator = self.separator
        if min_count is None:
            min_count = self.min_count
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return ListExpr(element=element, separator=separator, min_count=min_count, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)


class HideExpr(ExprBase):

    def __init__(self, expr: Expr, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.expr = expr

    def derive(self, expr: Expr | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'HideExpr':
        if expr is None:
            expr = self.expr
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return HideExpr(expr=expr, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)

POSINF = sys.maxsize

class RepeatExpr(ExprBase):

    def __init__(self, expr: Expr, min: int, max: int, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> None:
        super().__init__(label, rules, field_name, field_type, action)
        self.expr = expr
        self.min = min 
        self.max = max

    def derive(self, expr: Expr | None = None, min: int | None = None, max: int | None = None, label: str | None = None, rules: list['Rule'] | None = None, field_name: str | None = None, field_type: 'Type | None' = None, action: 'Rule | None' = None) -> 'RepeatExpr':
        if expr is None:
            expr = self.expr
        if min is None:
            min = self.min
        if max is None:
            max = self.max
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if field_name is None:
            field_name = self.field_name
        if field_type is None:
            field_type = self.field_type
        if action is None:
            action = self.action
        return RepeatExpr(expr=expr, min=min, max=max, label=label, rules=rules, field_name=field_name, field_type=field_type, action=action)


class Decorator(Node):

    def __init__(self, name: str, args: list[str | int] | None = None) -> None:
        super().__init__()
        if args is None:
            args = []
        self.name = name
        self.args = args

EXTERN        = 1
PUBLIC        = 2
FORCE_TOKEN   = 4
FORCE_KEYWORD = 8

unit_rule_name = 'void'
string_rule_type = 'String'
integer_rule_type = 'Integer'

builtin_types = {
    unit_rule_name,
    string_rule_type,
    integer_rule_type,
}

class Rule(Node):

    def __init__(self, name: str, expr: Expr | None, comment: str | None = None, decorators: list[Decorator] | None = None, flags: int = 0, type_name: str = string_rule_type) -> None:
        super().__init__()
        if decorators is None:
            decorators = []
        self.comment = comment
        self.decorators = decorators
        self.flags = flags
        self.name = name
        self.type_name = type_name
        self.expr = expr

    def derive(self, comment: str | None = None, decorators: list[Decorator] | None = None, flags: int | None = None, name: str | None = None, type_name: str | None = None, expr: Expr | None = None) -> 'Rule':
        if name is None:
            name = self.name
        if expr is None:
            expr = self.expr
        if comment is None:
            comment = self.comment
        if decorators is None:
            decorators = self.decorators
        if flags is None:
            flags = self.flags
        if type_name is None:
            type_name = self.type_name
        return Rule(name=name, expr=expr, comment=comment, decorators=decorators, flags=flags, type_name=type_name)

    @property
    def is_public(self) -> bool:
        return (self.flags & PUBLIC) > 0

    @property
    def is_extern(self) -> bool:
        return (self.flags & EXTERN) > 0

    @property
    def is_token(self) -> bool:
        return (self.flags & FORCE_TOKEN) > 0

    @property
    def is_keyword(self) -> bool:
        return (self.flags & FORCE_KEYWORD) > 0

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

    @property
    def is_keyword_def(self) -> bool:
        return self.has_decorator('keyword')

class Grammar(Node):

    def __init__(self, rules: list[Rule] | None = None) -> None:
        super().__init__()
        if rules is None:
            rules = []
        self.rules = rules
        self._rules_by_name = dict[str, Rule]()
        for rule in self.rules:
            self._rules_by_name[rule.name] = rule

    def is_fragment(self, rule: Rule) -> bool:
        return not rule.is_public

    @property
    @cache
    def skip_rule(self) -> Rule | None:
        for rule in self.rules:
            if rule.is_skip:
                return rule

    def is_token_rule(self, rule: Rule) -> bool:
        return rule.is_token

    def is_static_token(self, expr: Expr):
        if isinstance(expr, RefExpr):
            rule = self.lookup(expr.name)
            if rule is None:
                return False
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
        if isinstance(expr, ListExpr):
            return False
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

    @property
    @cache
    def keyword_rule(self) -> Rule | None:
        for rule in self.rules:
            if rule.is_keyword_def:
                return rule

    def lookup(self, name: str) -> Rule | None:
        return self._rules_by_name.get(name)

def rewrite_expr(expr: Expr, proc: Callable[[Expr], Expr | None]) -> Expr:
    """
    Rewrite an expression according to a procedure that either returns a new
    node if the expression needs to be rewritten or `None` otherwise.

    This works recursively, e.g. a deeply nested `LitExpr` will be rewritten
    with only a top-level call to `rewrite_expr`.
    """

    def visit(expr: Expr) -> Expr:

        updated = proc(expr)
        if updated is not None:
            return updated

        if isinstance(expr, LitExpr) or isinstance(expr, CharSetExpr) or isinstance(expr, RefExpr):
            return expr
        if isinstance(expr, RepeatExpr):
            new_expr = visit(expr.expr)
            if new_expr is expr.expr:
                return expr
            return RepeatExpr(min=expr.min, max=expr.max, expr=new_expr, rules=expr.rules, label=expr.label)
        if isinstance(expr, LookaheadExpr):
            new_expr = visit(expr.expr)
            if new_expr is expr.expr:
                return expr
            return LookaheadExpr(expr=new_expr, is_negated=expr.is_negated, rules=expr.rules, label=expr.label)
        if isinstance(expr, HideExpr):
            new_expr = visit(expr.expr)
            if new_expr is expr.expr:
                return expr
            return HideExpr(expr=new_expr, rules=expr.rules, label=expr.label)
        if isinstance(expr, ListExpr):
            new_element = visit(expr.element)
            new_separator = visit(expr.separator)
            if new_element is expr.element and new_separator is expr.separator:
                return expr
            return ListExpr(element=new_element, separator=new_separator, min_count=expr.min_count, rules=expr.rules, label=expr.label)
        if isinstance(expr, ChoiceExpr):
            new_elements = []
            changed = False
            for element in expr.elements:
                new_element = visit(element)
                if new_element is not element:
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
                if new_element is not element:
                    changed = True
                new_elements.append(new_element)
            if not changed:
                return expr
            return SeqExpr(elements=new_elements, rules=expr.rules, label=expr.label)
        assert_never(expr)

    return visit(expr)

def for_each_expr(node: Expr, proc: Callable[[Expr], None]) -> None:
    """
    Visit each direct child of a given expression exactly once.

    In the case that an expression does not have direct children, this function does nothing.
    """
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
    assert_never(node)
