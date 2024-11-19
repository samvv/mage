"""
Hand-written abstract syntax tree (AST) of the Mage grammar.

Also defines some visitors over Mage expressions and other useful procedures to
make handling the AST a bit easier.
"""

import sys
from functools import cache, lru_cache
from typing import Any, Callable, Generator, TypeGuard, TypeIs, assert_never
from intervaltree import Interval, IntervalTree

from magelang.logging import debug
from .constants import string_rule_type

ASCII_MIN = 0x00
ASCII_MAX = 0x7F

class MageNode:
    pass


type MageExpr = MageLitExpr | MageRefExpr | MageCharSetExpr | MageLookaheadExpr | MageChoiceExpr | MageSeqExpr | MageHideExpr | MageListExpr | MageRepeatExpr


class MageExprBase(MageNode):

    def __init__(
        self,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> None:
        if rules is None:
            rules = []
        self.label = label
        self.rules = rules
        self.action = action # FIXME merge with `self.rules`


class MageLitExpr(MageExprBase):

    def __init__(
        self,
        text: str,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> None:
        super().__init__(label, rules, action)
        self.text = text

    def derive(self, text: str | None = None, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> 'MageLitExpr':
        if text is None:
            text = self.text
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if action is None:
            action = self.action
        return MageLitExpr(text=text, label=label, rules=rules, action=action)

class MageRefExpr(MageExprBase):

    def __init__(
        self,
        name: str,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> None:
        super().__init__(label, rules, action)
        self.name = name

    def derive(
        self,
        *,
        name: str | None = None,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> 'MageRefExpr':
        if name is None:
            name = self.name
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if action is None:
            action = self.action
        return MageRefExpr(name=name, label=label, rules=rules, action=action)


class MageLookaheadExpr(MageExprBase):

    def __init__(
        self,
        expr: MageExpr,
        is_negated: bool,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> None:
        super().__init__(label, rules, action)
        self.expr = expr
        self.is_negated = is_negated

    def derive(
        self,
        *,
        expr: MageExpr | None = None,
        is_negated: bool | None = None,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> 'MageLookaheadExpr':
        if expr is None:
            expr = self.expr
        if is_negated is None:
            is_negated = self.is_negated
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if action is None:
            action = self.action
        return MageLookaheadExpr(expr=expr, is_negated=is_negated, label=label, rules=rules, action=action)


type CharSetElement = str | tuple[str, str]

_LOWERCASE = Interval(97, 122+1)
_UPPERCASE = Interval(65, 90+1)

class MageCharSetExpr(MageExprBase):

    def __init__(
        self,
        elements: list[CharSetElement],
        ci: bool = False,
        invert: bool = False,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> None:
        super().__init__(label, rules, action)
        self.ci = ci
        self.invert = invert
        self.elements = []
        self.tree = IntervalTree()
        for element in elements:
            if isinstance(element, str):
                self.add_char(element)
            else:
                low, high = element
                self.add_char_range(low, high)

    def derive(
        self,
        *,
        elements: list[CharSetElement] | None = None,
        ci: bool | None = None,
        invert: bool | None = None,
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> 'MageCharSetExpr':
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
        if action is None:
            action = self.action
        return MageCharSetExpr(elements=elements, ci=ci, invert=invert, label=label, rules=rules, action=action)

    def add_char(self, ch: str) -> None:
        self.elements.append(ch)
        code = ord(ch)
        self.tree.addi(code, code+1)

    def add_char_range(self, low: str, high: str) -> None:
        self.elements.append((low, high))
        if low > high:
            debug(f'Refused to index an invalid CharSetExpr element where low > high')
            return
        interval = Interval(ord(low), ord(high)+1)
        self.tree.add(interval)
        if self.ci:
            lc_range = intersect_interval(interval, _LOWERCASE)
            if lc_range is not None:
                self.tree.addi(lc_range.begin-32, lc_range.end-32)
            uc_range = intersect_interval(interval, _UPPERCASE)
            if uc_range is not None:
                self.tree.addi(uc_range.begin+32, uc_range.end+32)

    def __len__(self) -> int:
        n = 0
        for interval in self.tree:
            n += interval.end - interval.begin
        return n

    def contains(self, ch: str) -> bool:
        return self.tree.overlaps_point(ord(ch)) != self.invert

    @staticmethod
    def overlaps(a: 'MageCharSetExpr', b: 'MageCharSetExpr') -> bool:
        invert = a.invert != b.invert
        for interval in b.tree:
            if bool(a.tree.overlap(interval)) != invert:
                return True
        return False

def intersect_interval(a: Interval, b: Interval) -> Interval | None:
    if a.begin == a.end or b.begin == b.end:
        return
    if a.begin > b.begin and a.end < b.end:
        low = a.begin
        high = a.end
        return Interval(low, high)
    if b.begin > a.begin and b.end < a.end:
        low = b.begin
        high = b.end
        return Interval(low, high)
    # Using a non-strict comparison between `b.begin` and `a.end` because point
    # `b.begin` is included in the interval `b`. Likewise, `a.end` is NOT
    # included in the interval `a` so we use a strict comparison.
    if a.begin <= b.begin and b.begin < a.end:
        low = b.begin
        high = min(a.end, b.end)
        return Interval(low, high)
    # Using a strict comparison between `a.begin` and `b.end` because point `b.end`
    # is not part of the interval `b`
    if a.begin < b.end and b.end < a.end:
        low = max(a.begin, b.begin)
        high = b.end
        return Interval(low, high)

class MageChoiceExpr(MageExprBase):

    def __init__(
        self,
        elements: list[MageExpr],
        label: str | None = None,
        rules: list['MageRule'] | None = None,
        action: 'MageRule | None' = None
    ) -> None:
        super().__init__(label, rules, action)
        self.elements = elements

    def derive(self, elements: list[MageExpr] | None = None, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> 'MageChoiceExpr':
        if elements is None:
            elements = self.elements
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if action is None:
            action = self.action
        return MageChoiceExpr(elements=elements, label=label, rules=rules, action=action)


class MageSeqExpr(MageExprBase):

    def __init__(self, elements: list[MageExpr], label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> None:
        super().__init__(label, rules, action)
        self.elements = elements

    def derive(self, elements: list[MageExpr] | None = None, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> 'MageSeqExpr':
        if elements is None:
            elements = self.elements
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if action is None:
            action = self.action
        return MageSeqExpr(elements=elements, label=label, rules=rules, action=action)


class MageListExpr(MageExprBase):

    def __init__(self, element: MageExpr, separator: MageExpr, min_count: int, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> None:
        super().__init__(label, rules, action)
        self.element = element
        self.separator = separator
        self.min_count = min_count

    def derive(self, element: MageExpr | None = None, separator: MageExpr | None = None, min_count: int | None = None, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> 'MageListExpr':
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
        if action is None:
            action = self.action
        return MageListExpr(element=element, separator=separator, min_count=min_count, label=label, rules=rules, action=action)


class MageHideExpr(MageExprBase):

    def __init__(self, expr: MageExpr, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> None:
        super().__init__(label, rules, action)
        self.expr = expr

    def derive(self, expr: MageExpr | None = None, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> 'MageHideExpr':
        if expr is None:
            expr = self.expr
        if label is None:
            label = self.label
        if rules is None:
            rules = self.rules
        if action is None:
            action = self.action
        return MageHideExpr(expr=expr, label=label, rules=rules, action=action)

POSINF = sys.maxsize

class MageRepeatExpr(MageExprBase):

    def __init__(self, expr: MageExpr, min: int, max: int, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> None:
        super().__init__(label, rules, action)
        self.expr = expr
        self.min = min 
        self.max = max

    def derive(self, expr: MageExpr | None = None, min: int | None = None, max: int | None = None, label: str | None = None, rules: list['MageRule'] | None = None, action: 'MageRule | None' = None) -> 'MageRepeatExpr':
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
        if action is None:
            action = self.action
        return MageRepeatExpr(expr=expr, min=min, max=max, label=label, rules=rules, action=action)


class Decorator(MageNode):

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

class MageRule(MageNode):

    def __init__(self, name: str, expr: MageExpr | None, comment: str | None = None, decorators: list[Decorator] | None = None, flags: int = 0, type_name: str = string_rule_type) -> None:
        super().__init__()
        if decorators is None:
            decorators = []
        self.comment = comment
        self.decorators = decorators
        self.flags = flags
        self.name = name
        self.type_name = type_name
        self.expr = expr

    def derive(self, comment: str | None = None, decorators: list[Decorator] | None = None, flags: int | None = None, name: str | None = None, type_name: str | None = None, expr: MageExpr | None = None) -> 'MageRule':
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
        return MageRule(name=name, expr=expr, comment=comment, decorators=decorators, flags=flags, type_name=type_name)

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

class MageGrammar(MageNode):

    def __init__(self, rules: list[MageRule] | None = None) -> None:
        super().__init__()
        if rules is None:
            rules = []
        self.rules = rules
        self._rules_by_name = dict[str, MageRule]()
        for rule in self.rules:
            self._rules_by_name[rule.name] = rule

    def is_fragment(self, rule: MageRule) -> bool:
        return not rule.is_public

    @property
    @lru_cache
    def skip_rule(self) -> MageRule | None:
        for rule in self.rules:
            if rule.is_skip:
                return rule

    def is_token_rule(self, rule: MageRule) -> bool:
        return rule.is_token

    def is_static(self, expr: MageExpr) -> bool:
        if isinstance(expr, MageRefExpr):
            rule = self.lookup(expr.name)
            return rule is not None and self.is_static_token_rule(rule)
        if isinstance(expr, MageLitExpr):
            return True
        if isinstance(expr, MageCharSetExpr):
            return len(expr) == 1
        if isinstance(expr, MageSeqExpr):
            return all(self.is_static(element) for element in expr.elements)
        if isinstance(expr, MageChoiceExpr):
            # FIXME should I check whether the choices are actually different?
            return False
        if isinstance(expr, MageRepeatExpr):
            # Only return true if we're dealing with a fixed width repition
            return expr.min == expr.max and self.is_static(expr.expr)
        if isinstance(expr, MageListExpr):
            # List expressions always repeat an unpredictable amount of times
            return False
        if isinstance(expr, MageLookaheadExpr):
            # Lookahead has no effect on what (non-)static characters are generated
            return True
        if isinstance(expr, MageHideExpr):
            return self.is_static(expr.expr)
        assert_never(expr)

    def is_static_token_rule(self, rule: MageRule) -> bool:
        if rule.is_extern:
            return False
        assert(rule.expr is not None)
        return self.is_static(rule.expr)

    def is_parse_rule(self, rule: MageRule) -> bool:
        if rule.is_extern:
            return not rule.is_token
        return rule.is_public and not self.is_token_rule(rule)

    def is_variant_rule(self, rule: MageRule) -> bool:
        if rule.is_extern or rule.is_wrap:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(rule.expr is not None)
        return isinstance(rule.expr, MageChoiceExpr)

    def is_token_variant_rule(self, rule: MageRule) -> bool:
        if rule.is_extern or rule.is_wrap:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(rule.expr is not None)
        if not isinstance(rule, MageChoiceExpr):
            return False
        for expr in flatten_choice(rule.expr):
            if not isinstance(expr, MageRefExpr):
                return False
            rule_2 = self.lookup(expr.name)
            if rule_2 is None or not self.is_token_rule(rule_2):
                return False
        return True

    def get_token_rules(self) -> Generator[MageRule, None, None]:
        for rule in self.rules:
            if self.is_token_rule(rule):
                yield rule

    def get_parse_rules(self) -> Generator[MageRule, None, None]:
        for rule in self.rules:
            if self.is_parse_rule(rule):
                yield rule

    @property
    @lru_cache
    def keyword_rule(self) -> MageRule | None:
        for rule in self.rules:
            if rule.is_keyword_def:
                return rule

    def lookup(self, name: str) -> MageRule | None:
        return self._rules_by_name.get(name)

type MageSyntax = MageExpr | MageRule | MageGrammar

def is_mage_syntax(value: Any) -> TypeIs[MageSyntax]:
    return isinstance(value, MageNode)

def rewrite_each_child_expr(expr: MageExpr, proc: Callable[[MageExpr], MageExpr]) -> MageExpr:
    """
    Rewrite an expression according to a procedure that either returns a new
    node if the expression needs to be rewritten or the node itself otherwise.
    """
    if isinstance(expr, MageLitExpr) or isinstance(expr, MageCharSetExpr) or isinstance(expr, MageRefExpr):
        return expr
    if isinstance(expr, MageRepeatExpr):
        new_expr = proc(expr.expr)
        if new_expr is expr.expr:
            return expr
        return MageRepeatExpr(min=expr.min, max=expr.max, expr=new_expr, rules=expr.rules, label=expr.label)
    if isinstance(expr, MageLookaheadExpr):
        new_expr = proc(expr.expr)
        if new_expr is expr.expr:
            return expr
        return MageLookaheadExpr(expr=new_expr, is_negated=expr.is_negated, rules=expr.rules, label=expr.label)
    if isinstance(expr, MageHideExpr):
        new_expr = proc(expr.expr)
        if new_expr is expr.expr:
            return expr
        return MageHideExpr(expr=new_expr, rules=expr.rules, label=expr.label)
    if isinstance(expr, MageListExpr):
        new_element = proc(expr.element)
        new_separator = proc(expr.separator)
        if new_element is expr.element and new_separator is expr.separator:
            return expr
        return MageListExpr(element=new_element, separator=new_separator, min_count=expr.min_count, rules=expr.rules, label=expr.label)
    if isinstance(expr, MageChoiceExpr):
        new_elements = []
        changed = False
        for element in expr.elements:
            new_element = proc(element)
            if new_element is not element:
                changed = True
            new_elements.append(new_element)
        if not changed:
            return expr
        return MageChoiceExpr(elements=new_elements, rules=expr.rules, label=expr.label)
    if isinstance(expr, MageSeqExpr):
        new_elements = []
        changed = False
        for element in expr.elements:
            new_element = proc(element)
            if new_element is not element:
                changed = True
            new_elements.append(new_element)
        if not changed:
            return expr
        return MageSeqExpr(elements=new_elements, rules=expr.rules, label=expr.label)
    assert_never(expr)

def for_each_expr(node: MageExpr, proc: Callable[[MageExpr], None]) -> None:
    """
    Visit each direct child of a given expression exactly once.

    In the case that an expression does not have direct children, this function does nothing.
    """
    if isinstance(node, MageLitExpr) or isinstance(node, MageCharSetExpr) or isinstance(node, MageRefExpr):
        return
    if isinstance(node, MageRepeatExpr) or isinstance(node, MageLookaheadExpr) or isinstance(node, MageHideExpr):
        proc(node.expr)
        return
    if isinstance(node, MageListExpr):
        proc(node.element)
        proc(node.separator)
        return
    if isinstance(node, MageChoiceExpr) or isinstance(node, MageSeqExpr):
        for element in node.elements:
            proc(element)
        return
    assert_never(node)

def static_expr_to_str(expr: MageExpr) -> str:
    if isinstance(expr, MageLitExpr):
        return expr.text
    if isinstance(expr, MageSeqExpr):
        out = ''
        for element in expr.elements:
            out += static_expr_to_str(element)
        return out
    raise RuntimeError(f'could not extract text from {expr}: expression is non-static or not normalised')

def flatten_sequence(expr: MageExpr) -> Generator[MageExpr, None, None]:
    if isinstance(expr, MageSeqExpr):
        for element in expr.elements:
            yield from flatten_sequence(element)
    else:
        yield expr

def flatten_choice(expr: MageExpr) -> Generator[MageExpr, None, None]:
    if isinstance(expr, MageChoiceExpr):
        for element in expr.elements:
            yield from flatten_choice(element)
    else:
        yield expr

