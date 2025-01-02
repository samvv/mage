"""
Hand-written abstract syntax tree (AST) of the Mage grammar.

Also defines some visitors over Mage expressions and other useful procedures to
make handling the AST a bit easier.
"""

from dataclasses import dataclass
import sys
from functools import lru_cache
from typing import Any, Callable, Generator, Iterable, TypeIs, TypeVar, assert_never, cast
from intervaltree import Interval, IntervalTree

from magelang.lang.mage.cst import MageRuleParent
from magelang.logging import debug, warn
from magelang.util import nonnull

from .constants import string_rule_type

ASCII_MIN = 0x00
ASCII_MAX = 0x7F

class MageNodeBase:
    pass


@dataclass
class ReturnAction:
    rule: 'MageRule'


@dataclass
class SetModeAction:
    mode: int


type Action = ReturnAction | SetModeAction


type MageExpr = MageLitExpr | MageRefExpr | MageCharSetExpr | MageLookaheadExpr | MageChoiceExpr | MageSeqExpr | MageHideExpr | MageListExpr | MageRepeatExpr


class MageExprBase(MageNodeBase):

    def __init__(
        self,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExpr | MageRule | None' = None
    ) -> None:
        if actions is None:
            actions = []
        self.label = label
        self.actions = actions
        self.parent = parent

    @property
    def returns(self) -> 'MageRule | None':
        for action in self.actions:
            if isinstance(action, ReturnAction):
                return action.rule


class MageLitExpr(MageExprBase):

    def __init__(
        self,
        text: str,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.text = text

    def derive(
        self,
        text: str | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None
    ) -> 'MageLitExpr':
        if text is None:
            text = self.text
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageLitExpr(text=text, label=label, actions=actions)

class MageRefExpr(MageExprBase):

    def __init__(
        self,
        name: str,
        module_path: list[str] | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        if module_path is None:
            module_path = []
        self.name = name

    def derive(
        self,
        *,
        name: str | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> 'MageRefExpr':
        if name is None:
            name = self.name
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageRefExpr(name=name, label=label, actions=actions)


class MageLookaheadExpr(MageExprBase):

    def __init__(
        self,
        expr: MageExpr,
        is_negated: bool,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.expr = expr
        self.is_negated = is_negated

    def derive(
        self,
        *,
        expr: MageExpr | None = None,
        is_negated: bool | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> 'MageLookaheadExpr':
        if expr is None:
            expr = self.expr
        if is_negated is None:
            is_negated = self.is_negated
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageLookaheadExpr(expr=expr, is_negated=is_negated, label=label, actions=actions)


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
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.ci = ci
        self.invert = invert
        self.elements = []
        self.tree = IntervalTree()
        if invert:
            self.tree.addi(ASCII_MIN, ASCII_MAX+1)
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
        actions: list['Action'] | None = None,
    ) -> 'MageCharSetExpr':
        if elements is None:
            elements = self.elements
        if ci is None:
            ci = self.ci
        if invert is None:
            invert = self.invert
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageCharSetExpr(elements=elements, ci=ci, invert=invert, label=label, actions=actions)

    def _add_to_tree(self, interval: Interval) -> None:
        if self.invert:
            self.tree.chop(interval.begin, interval.end)
        else:
            self.tree.add(interval)

    def add_char(self, ch: str) -> None:
        self.elements.append(ch)
        code = ord(ch)
        self._add_to_tree(Interval(code, code+1))

    def add_char_range(self, low: str, high: str) -> None:
        self.elements.append((low, high))
        if low > high:
            debug(f'Refused to index an invalid CharSetExpr element where low > high')
            return
        interval = Interval(ord(low), ord(high)+1)
        self._add_to_tree(interval)
        if self.ci:
            lc_range = intersect_interval(interval, _LOWERCASE)
            if lc_range is not None:
                self._add_to_tree(Interval(lc_range.begin-32, lc_range.end-32))
            uc_range = intersect_interval(interval, _UPPERCASE)
            if uc_range is not None:
                self._add_to_tree(Interval(uc_range.begin+32, uc_range.end+32))

    def __len__(self) -> int:
        return sum(interval.end - interval.begin for interval in self.tree)

    def contains_char(self, ch: str) -> bool:
        return self.tree.overlaps_point(ord(ch))

    def contains_range(self, low: str, high: str) -> bool:
        i = Interval(ord(low), ord(high)+1)
        return any(ti.contains_interval(i) for ti in self.tree.overlap(i))

    @property
    def canonical_elements(self) -> Iterable[CharSetElement]:
        for interval in self.tree:
            if interval.begin == interval.end-1:
                yield chr(interval.begin)
            else:
                yield (chr(interval.begin), chr(interval.end-1))

    @staticmethod
    def overlaps(a: 'MageCharSetExpr', b: 'MageCharSetExpr') -> bool:
        for interval in b.tree:
            if bool(a.tree.overlap(interval)):
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
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.elements = elements

    def derive(
        self,
        elements: list[MageExpr] | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None
    ) -> 'MageChoiceExpr':
        if elements is None:
            elements = self.elements
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageChoiceExpr(elements=elements, label=label, actions=actions)


class MageSeqExpr(MageExprBase):

    def __init__(self,
        elements: list[MageExpr],
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.elements = elements

    def derive(
        self,
        elements: list[MageExpr] | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> 'MageSeqExpr':
        if elements is None:
            elements = self.elements
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageSeqExpr(elements=elements, label=label, actions=actions)


class MageListExpr(MageExprBase):

    def __init__(self,
        element: MageExpr,
        separator: MageExpr,
        min_count: int,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.element = element
        self.separator = separator
        self.min_count = min_count

    def derive(
        self,
        element: MageExpr | None = None,
        separator: MageExpr | None = None,
        min_count: int | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> 'MageListExpr':
        if element is None:
            element = self.element
        if separator is None:
            separator = self.separator
        if min_count is None:
            min_count = self.min_count
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageListExpr(element=element, separator=separator, min_count=min_count, label=label, actions=actions)


class MageHideExpr(MageExprBase):

    def __init__(self,
        expr: MageExpr,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.expr = expr

    def derive(
        self,
        expr: MageExpr | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> 'MageHideExpr':
        if expr is None:
            expr = self.expr
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageHideExpr(expr=expr, label=label, actions=actions)


POSINF = sys.maxsize


class MageRepeatExpr(MageExprBase):

    def __init__(
        self,
        expr: MageExpr,
        min: int,
        max: int,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> None:
        super().__init__(label, actions)
        self.expr = expr
        self.min = min
        self.max = max

    def derive(
        self,
        expr: MageExpr | None = None,
        min: int | None = None,
        max: int | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
    ) -> 'MageRepeatExpr':
        if expr is None:
            expr = self.expr
        if min is None:
            min = self.min
        if max is None:
            max = self.max
        if label is None:
            label = self.label
        if actions is None:
            actions = self.actions
        return MageRepeatExpr(expr=expr, min=min, max=max, label=label, actions=actions)


class Decorator(MageNodeBase):

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


class MageRule(MageNodeBase):

    def __init__(
        self,
        name: str,
        expr: MageExpr | None,
        comment: str | None = None,
        decorators: list[Decorator] | None = None,
        flags: int = 0,
        type_name: str = string_rule_type,
        mode: int = 0,
        parent: 'MageModule | MageGrammar | None' = None
    ) -> None:
        super().__init__()
        if decorators is None:
            decorators = []
        self.comment = comment
        self.decorators = decorators
        self.flags = flags
        self.name = name
        self.type_name = type_name
        self.expr = expr
        self.mode = mode
        self.parent = parent

    def derive(
        self,
        comment: str | None = None,
        decorators: list[Decorator] | None = None,
        flags: int | None = None,
        name: str | None = None,
        type_name: str | None = None,
        expr: MageExpr | None = None,
        mode: int | None = None
    ) -> 'MageRule':
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
        if mode is None:
            mode = self.mode
        return MageRule(name=name, expr=expr, comment=comment, decorators=decorators, flags=flags, type_name=type_name, mode=mode)

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


type MageModuleElement = MageRule | MageModule


class MageModuleBase(MageNodeBase):

    def __init__(self, elements: 'list[MageModuleElement] | None' = None, parent: 'MageGrammar | MageModule | None' = None) -> None:
        super().__init__()
        if elements is None:
            elements = []
        self.elements = elements
        self.parent = parent
        self._rules_by_name = dict[str, 'MageRule']()
        for element in elements:
            if isinstance(element, MageRule):
                self._rules_by_name[element.name] = element

    def lookup(self, name: str) -> 'MageRule | None':
        return self._rules_by_name.get(name)

    @property
    def rules(self) -> Iterable[MageRule]:
        return self._rules_by_name.values()

    def is_fragment(self, rule: MageRule) -> bool:
        return not rule.is_public

    @property
    @lru_cache
    def skip_rule(self) -> MageRule | None:
        for element in self.elements:
            if isinstance(element, MageRule) and element.is_skip:
                return element

    def is_token_rule(self, element: MageModuleElement) -> TypeIs[MageRule]:
        return isinstance(element, MageRule) and element.is_token

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

    def is_static_token_rule(self, element: MageModuleElement) -> TypeIs[MageRule]:
        if not isinstance(element, MageRule) or element.is_extern:
            return False
        assert(element.expr is not None)
        return self.is_static(element.expr)

    def is_parse_rule(self, element: MageModuleElement) -> TypeIs[MageRule]:
        if not isinstance(element, MageRule):
            return False
        if element.is_extern:
            return not element.is_token
        return element.is_public and not self.is_token_rule(element)

    def is_variant_rule(self, element: MageModuleElement) -> TypeIs[MageRule]:
        if not isinstance(element, MageRule) or element.is_extern or element.is_wrap:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(element.expr is not None)
        return isinstance(element.expr, MageChoiceExpr)

    def is_token_variant_rule(self, element: MageRule) -> TypeIs[MageRule]:
        if not isinstance(element, MageRule) or element.is_extern or element.is_wrap:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(element.expr is not None)
        if not isinstance(element, MageChoiceExpr):
            return False
        for expr in flatten_choice(element.expr):
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

class MageModule(MageModuleBase):

    def __init__(
        self,
        name: str,
        elements: 'list[MageRule | MageModule]',
        flags: int = 0,
        parent: 'MageModule | MageGrammar | None' = None
    ) -> None:
        super().__init__(elements, parent)
        self.name = name
        self.flags = flags

    def derive(
        self,
        name: str | None = None,
        elements: list[MageModuleElement] | None = None,
        flags: int | None = None,
    ) -> 'MageModule':
        if name is None:
            name = self.name
        if elements is None:
            elements = self.elements
        if flags is None:
            flags = self.flags
        return MageModule(name=name, elements=elements, parent=None)

class MageGrammar(MageModuleBase):

    def derive(self, elements: list[MageModuleElement] | None = None) -> 'MageGrammar':
        if elements is None:
            elements = self.elements
        return MageGrammar(elements)

type MageSyntax = MageExpr | MageRule | MageGrammar | MageModule

def is_mage_syntax(value: Any) -> TypeIs[MageSyntax]:
    return isinstance(value, MageNodeBase)

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
        out = MageRepeatExpr(min=expr.min, max=expr.max, expr=new_expr, actions=expr.actions, label=expr.label)
        new_expr.parent = out
        return out
    if isinstance(expr, MageLookaheadExpr):
        new_expr = proc(expr.expr)
        if new_expr is expr.expr:
            return expr
        out = MageLookaheadExpr(expr=new_expr, is_negated=expr.is_negated, actions=expr.actions, label=expr.label)
        new_expr.parent = out
        return out
    if isinstance(expr, MageHideExpr):
        new_expr = proc(expr.expr)
        if new_expr is expr.expr:
            return expr
        out = MageHideExpr(expr=new_expr, actions=expr.actions, label=expr.label)
        new_expr.parent = out
        return out
    if isinstance(expr, MageListExpr):
        new_element = proc(expr.element)
        new_separator = proc(expr.separator)
        if new_element is expr.element and new_separator is expr.separator:
            return expr
        out = MageListExpr(element=new_element, separator=new_separator, min_count=expr.min_count, actions=expr.actions, label=expr.label)
        new_element.parent = out
        new_separator.parent = out
        return out
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
        out = MageChoiceExpr(elements=new_elements, actions=expr.actions, label=expr.label)
        for new_element in new_elements:
            new_element.parent = out
        return out
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
        out = MageSeqExpr(elements=new_elements, actions=expr.actions, label=expr.label)
        for new_element in new_elements:
            new_element.parent = out
        return out
    assert_never(expr)

_T = TypeVar('_T', bound=MageGrammar | MageModule)

def rewrite_each_rule(node: _T, proc: Callable[[MageRule], MageRule]) -> _T:
    new_elements = list[MageModuleElement]()
    for element in node.elements:
        if isinstance(element, MageRule):
            new_elements.append(proc(element))
        elif isinstance(element, MageModule):
            new_elements.append(rewrite_each_rule(element, proc))
        else:
            assert_never(element)
    return cast(_T, node.derive(elements=new_elements))

def for_each_direct_child_expr(node: MageExpr, proc: Callable[[MageExpr], None]) -> None:
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

def for_each_expr(node: MageExpr, proc: Callable[[MageExpr], None]) -> None:
    proc(node)
    for_each_direct_child_expr(node, proc)

def for_each_rule(node: MageGrammar | MageModule, proc: Callable[[MageRule], None]) -> None:
    for element in node.elements:
        if isinstance(element, MageRule):
            proc(element)
        elif isinstance(element, MageModule):
            for_each_rule(element, proc)
        else:
            assert_never(element)

def is_expr(node: MageSyntax) -> TypeIs[MageExpr]:
    return isinstance(node, MageExprBase)

def for_each_direct_child_node(node: MageSyntax, proc: Callable[[MageSyntax], None]) -> None:
    if isinstance(node, MageGrammar) or isinstance(node, MageModule):
        for element in node.elements:
            proc(element)
    elif isinstance(node, MageRule):
        if node.expr is not None:
            proc(node.expr)
    elif is_expr(node):
        for_each_direct_child_expr(node, proc)
    else:
        assert_never(node)

def rewrite_module(module: _T, proc: Callable[[MageModuleElement], MageModuleElement]) -> _T:
    new_elements = []
    changed = False
    for element in module.elements:
        new_element = proc(element)
        if new_element is not element:
            changed = True
        new_elements.append(new_element)
    if not changed:
        return module
    out = module.derive(elements=new_elements)
    for new_element in new_elements:
        new_element.parent = out
    return cast(_T, out)

def set_parents(node: MageSyntax, parent: 'MageSyntax | None' = None) -> None:
    node.parent = parent # type: ignore
    for_each_direct_child_node(node, lambda child: set_parents(child, node))

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

def get_enclosing_module(node: MageRule | MageExpr | MageModule) -> MageModule | MageGrammar:
    while True:
        if isinstance(node.parent, MageModule) or isinstance(node.parent, MageGrammar):
            return node.parent
        node = nonnull(node.parent)

def lookup_ref(expr: MageRefExpr) -> MageRule | None:
    mod = get_enclosing_module(expr)
    while True:
        rule = mod.lookup(expr.name)
        if rule is not None:
            return rule
        if isinstance(mod, MageGrammar):
            break
        mod = nonnull(mod.parent)
