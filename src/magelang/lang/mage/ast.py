"""
Hand-written abstract syntax tree (AST) of the Mage grammar.

Also defines some visitors over Mage expressions and other useful procedures to
make handling the AST a bit easier.
"""

from typing import Self, TypedDict, Unpack
from dataclasses import dataclass
import sys
from functools import lru_cache
from typing import Any, Callable, Generator, Iterable, TypeGuard, TypeIs, assert_never, cast
import typing
from intervaltree import Interval, IntervalTree

from magelang.logging import debug
from magelang.runtime import Span, TextFile
from magelang.util import nonnull

from .constants import string_rule_type

ASCII_MIN = 0x00
ASCII_MAX = 0x7F


class MageNodeBase:

    span: Span | None

    def __init__(self, span: Span | None = None) -> None:
        self.span = span

    @property
    def grammar(self) -> 'MageGrammar':
        curr = self
        while curr is not None:
            if isinstance(curr, MageGrammar):
                return curr
            curr = curr.parent # type: ignore
        raise RuntimeError(f'Could not get the grammmar of a node. Are the parent pointers correctly set?')

    def get_fields(self) -> dict:
        out = {}
        for cls in self.__class__.__mro__:
            for name in typing.get_type_hints(cls):
                out[name] = getattr(self, name) # type: ignore
        return out

    def derive(self, **kwargs) -> Self:
        fields = self.get_fields()
        fields.update(kwargs)
        return self.__class__(**fields) # type: ignore

@dataclass
class ReturnAction:
    rule: 'MageRule'


@dataclass
class SetModeAction:
    mode: int


type Action = ReturnAction | SetModeAction


type MageExpr = MageLitExpr | MageRefExpr | MageCharSetExpr | MageLookaheadExpr | MageChoiceExpr | MageSeqExpr | MageHideExpr | MageListExpr | MageRepeatExpr


type MageExprParent = MageExpr | MageRule


class MageExprBase(MageNodeBase):

    label: str | None
    actions: list['Action']
    parent: 'MageExprParent | None'
    decorators: list['Decorator']

    def __init__(
        self,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(span)
        if actions is None:
            actions = []
        if decorators is None:
            decorators = []
        self.label = label
        self.actions = actions
        self.parent = parent
        self.decorators = decorators
        self.field_name: str | None = None

    @property
    def returns(self) -> 'MageRule | None':
        for action in self.actions:
            if isinstance(action, ReturnAction):
                return action.rule


class MageLitExprDeriveArgs(TypedDict, total=False):
    text: str
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageLitExpr(MageExprBase):

    text: str

    def __init__(
        self,
        text: str,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None,
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        self.text = text

    def set_parents(self) -> None:
        pass

    def derive(self, **kwargs: Unpack[MageLitExprDeriveArgs]) -> 'MageLitExpr':
        return super().derive(**kwargs)


class MageRefExprDeriveArgs(TypedDict, total=False):
    name: str
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageRefExpr(MageExprBase):

    name: str

    def __init__(
        self,
        name: str,
        module_path: list[str] | None = None,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        if module_path is None:
            module_path = []
        self.name = name
        self.module_path = module_path

    def set_parents(self) -> None:
        pass

    def derive(self, **kwargs: Unpack[MageRefExprDeriveArgs]) -> 'MageRefExpr':
        return super().derive(**kwargs)


class MageLookaheadExprDeriveArgs(TypedDict, total=False):
    expr: MageExpr
    is_negated: bool
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageLookaheadExpr(MageExprBase):

    expr: MageExpr
    is_negated: bool

    def __init__(
        self,
        expr: MageExpr,
        is_negated: bool,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        self.expr = expr
        self.is_negated = is_negated
        self.set_parents()

    def set_parents(self) -> None:
        self.expr.parent = self

    def derive(self, **kwargs: Unpack[MageLookaheadExprDeriveArgs]) -> 'MageLookaheadExpr':
        return super().derive(**kwargs)


ASSOC_LEFT = 1
ASSOC_RIGHT = 2


type CharSetElement = str | tuple[str, str]


_LOWERCASE = Interval(97, 122+1)
_UPPERCASE = Interval(65, 90+1)


class MageCharSetExprDeriveArgs(TypedDict, total=False):
    elements: list[CharSetElement]
    ci: bool
    invert: bool
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageCharSetExpr(MageExprBase):

    elements: list[CharSetElement]
    ci: bool
    invert: bool

    def __init__(
        self,
        elements: list[CharSetElement],
        ci: bool = False,
        invert: bool = False,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
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

    def set_parents(self) -> None:
        pass

    def derive(self, **kwargs: Unpack[MageCharSetExprDeriveArgs]) -> 'MageCharSetExpr':
        return super().derive(**kwargs)

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


class MageChoiceExprDeriveArgs(TypedDict, total=False):
    elements: list[MageExpr]
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageChoiceExpr(MageExprBase):

    elements: list[MageExpr]

    def __init__(
        self,
        elements: list[MageExpr],
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        self.elements = elements
        self.set_parents()

    def set_parents(self) -> None:
        for element in self.elements:
            element.parent = self

    def derive(self, **kwargs: Unpack[MageChoiceExprDeriveArgs]) -> 'MageChoiceExpr':
        return super().derive(**kwargs)


class MageSeqExprDeriveArgs(TypedDict, total=False):
    elements: list[MageExpr]
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageSeqExpr(MageExprBase):

    elements: list[MageExpr]

    def __init__(
        self,
        elements: list[MageExpr],
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        self.elements = elements
        self.set_parents()

    def set_parents(self) -> None:
        for element in self.elements:
            element.parent = self

    def derive(self, **kwargs: Unpack[MageSeqExprDeriveArgs]) -> 'MageSeqExpr':
        return super().derive(**kwargs)


class MageListExprDeriveArgs(TypedDict, total=False):
    element: MageExpr
    separator: MageExpr
    min_count: int
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageListExpr(MageExprBase):

    element: MageExpr
    separator: MageExpr
    min_count: int

    def __init__(
        self,
        element: MageExpr,
        separator: MageExpr,
        min_count: int,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        self.element = element
        self.separator = separator
        self.min_count = min_count
        self.set_parents()

    def set_parents(self) -> None:
        self.element.parent = self
        self.separator.parent = self

    def derive(self, **kwargs: Unpack[MageListExprDeriveArgs]) -> 'MageListExpr':
        return super().derive(**kwargs)


class MageHideExprDeriveArgs(TypedDict, total=False):
    expr: MageExpr
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageHideExpr(MageExprBase):

    expr: MageExpr

    def __init__(
        self,
        expr: MageExpr,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        self.expr = expr
        self.set_parents()

    def set_parents(self) -> None:
        self.expr.parent = self

    def derive(self, **kwargs: Unpack[MageHideExprDeriveArgs]) -> 'MageHideExpr':
        return super().derive(**kwargs)


POSINF = sys.maxsize # FIXME if we ever persist this value there will be trouble


class MageRepeatExprDeriveArgs(TypedDict, total=False):
    expr: MageExpr
    min: int
    max: int
    label: str | None
    actions: list['Action']
    decorators: list['Decorator']
    span: Span | None


class MageRepeatExpr(MageExprBase):

    expr: MageExpr
    min: int
    max: int

    def __init__(
        self,
        expr: MageExpr,
        min: int,
        max: int,
        label: str | None = None,
        actions: list['Action'] | None = None,
        parent: 'MageExprParent | None' = None,
        decorators: list['Decorator'] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(label, actions, parent, decorators, span)
        self.expr = expr
        self.min = min
        self.max = max
        self.set_parents()

    def set_parents(self) -> None:
        self.expr.parent = self

    def derive(self, **kwargs: Unpack[MageRepeatExprDeriveArgs]) -> 'MageRepeatExpr':
        return super().derive(**kwargs)


class DecoratorDeriveArgs(TypedDict, total=False):
    name: str
    args: list[str | int]
    span: Span | None


class Decorator(MageNodeBase):

    name: str
    args: list[str | int]

    def __init__(
        self,
        name: str,
        args: list[str | int] | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(span)
        if args is None:
            args = []
        self.name = name
        self.args = args

    def derive(self, **kwargs: Unpack[DecoratorDeriveArgs]) -> Self:
        return super().derive(**kwargs)


EXTERN        = 1
PUBLIC        = 2
FORCE_TOKEN   = 4
FORCE_KEYWORD = 8


class MageRuleDeriveArgs(TypedDict, total=False):
    expr: MageExpr | None
    comment: str | None
    decorators: list[Decorator]
    flags: int
    name: str
    type_name: str
    mode: int
    span: Span | None


class MageRule(MageNodeBase):

    name: str
    expr: MageExpr | None
    comment: str | None
    decorators: list[Decorator]
    flags: int
    type_name: str
    mode: int
    parent: 'MageModule | MageGrammar | None'

    def __init__(
        self,
        name: str,
        expr: MageExpr | None,
        comment: str | None = None,
        decorators: list[Decorator] | None = None,
        flags: int = 0,
        type_name: str = string_rule_type,
        mode: int = 0,
        parent: 'MageModule | MageGrammar | None' = None,
        span: Span | None = None
    ) -> None:
        super().__init__(span)
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
        self.set_parents()

    def set_parents(self) -> None:
        if self.expr is not None:
            self.expr.parent = self

    def derive(self, **kwargs: Unpack[MageRuleDeriveArgs]) -> 'MageRule':
        return super().derive(**kwargs)

    @property
    def is_public(self) -> bool:
        return (self.flags & PUBLIC) > 0

    @property
    def is_extern(self) -> bool:
        return (self.flags & EXTERN) > 0

    @property
    def is_lex(self) -> bool:
        """
        Check if this rule is a lexing rule.

        A lexing rule is any public rule that contains the `token` keyword.
        """
        return self.is_public and (self.flags & FORCE_TOKEN) > 0

    @property
    def is_parse(self) -> bool:
        """
        Check if this rule is a parse rule.

        A parse rule is any public rule that misses the `token` keyword.
        """
        return self.is_public and (self.flags & FORCE_TOKEN) == 0

    @property
    def is_fragment(self) -> bool:
        """
        Check if this rule is merely a fragment.

        Fragments are inlined into whatever rule references them, be it a parse
        rule, a token rule or another fragment.
        """
        return not self.is_public

    @property
    def is_keyword(self) -> bool:
        """
        Check a virtual property that is used internally.
        """
        return (self.flags & FORCE_KEYWORD) > 0

    def has_decorator(self, name: str) -> bool:
        for decorator in self.decorators:
            if decorator.name == name:
                return True
        return False

    @property
    def is_noskip(self) -> bool:
        return self.has_decorator('noskip')

    @property
    def is_skip_def(self) -> bool:
        return self.has_decorator('skip')

    @property
    def is_wrap(self) -> bool:
        return self.has_decorator('wrap')

    @property
    def is_keyword_def(self) -> bool:
        return self.has_decorator('keyword')


type MageModuleElement = MageRule | MageModule


class MageModuleBase(MageNodeBase):

    elements: list[MageModuleElement]

    def __init__(
        self,
        elements: 'list[MageModuleElement] | None' = None,
        span: Span | None = None
    ) -> None:
        super().__init__(span)
        if elements is None:
            elements = []
        self.elements = elements
        self._rules_by_name = dict[str, 'MageRule']()
        self._modules_by_name = dict[str, 'MageModule']()
        for element in elements:
            if isinstance(element, MageRule):
                self._rules_by_name[element.name] = element
            elif isinstance(element, MageModule):
                self._modules_by_name[element.name] = element

    def lookup(self, name: str) -> 'MageRule | None':
        return self._rules_by_name.get(name)

    def lookup_module(self, name: str) -> 'MageModule | None':
        return self._modules_by_name.get(name)

    @property
    def rules(self) -> Iterable[MageRule]:
        return self._rules_by_name.values()

    @property
    @lru_cache
    def skip_rule(self) -> MageRule | None:
        for element in self.elements:
            if isinstance(element, MageRule) and element.is_skip_def:
                return element

    def is_token_rule(self, element: MageModuleElement) -> TypeGuard[MageRule]:
        return isinstance(element, MageRule) and element.is_public and element.is_lex

    def is_static_token_rule(self, element: MageModuleElement) -> TypeGuard[MageRule]:
        return self.is_token_rule(element) \
            and not element.is_extern \
            and is_static(nonnull(element.expr))

    def is_variant_rule(self, element: MageModuleElement) -> TypeGuard[MageRule]:
        if not isinstance(element, MageRule) or element.is_extern or element.is_wrap:
            return False
        # only Rule(is_extern=True) can not hold an expression
        assert(element.expr is not None)
        return isinstance(element.expr, MageChoiceExpr)

    def is_token_variant_rule(self, element: MageModuleElement) -> TypeGuard[MageRule]:
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
            if rule.is_parse:
                yield rule

    @property
    @lru_cache
    def keyword_rule(self) -> MageRule | None:
        for rule in self.rules:
            if rule.is_keyword_def:
                return rule


class MageModuleDeriveArgs(TypedDict, total=False):
    name: str
    elements: list[MageModuleElement]
    flags: int
    span: Span | None


class MageModule(MageModuleBase):

    name: str
    parent: 'MageModule | MageGrammar | None'

    def __init__(
        self,
        name: str,
        elements: 'list[MageRule | MageModule]',
        flags: int = 0,
        parent: 'MageModule | MageGrammar | None' = None,
        span: Span | None = None
    ) -> None:
        super().__init__(elements, span)
        self.name = name
        self.flags = flags
        self.parent = parent
        self.set_parents()

    def set_parents(self) -> None:
        for element in self.elements:
            element.parent = self

    def derive(self, **kwargs: Unpack[MageModuleDeriveArgs]) -> 'MageModule':
        return super().derive(**kwargs)


class MageGrammarDeriveArgs(TypedDict, total=False):
    elements: list[MageRule | MageModule]
    file: TextFile | None
    span: Span | None


class MageGrammar(MageModuleBase):

    file: TextFile | None

    def __init__(
        self,
        elements: 'list[MageRule | MageModule] | None' = None,
        file: TextFile | None = None,
        span: Span | None = None
    ) -> None:
        super().__init__(elements, span)
        self.file = file
        self.parent = None
        self.set_parents()

    def set_parents(self) -> None:
        for element in self.elements:
            element.parent = self

    def derive(self, **kwargs: Unpack[MageGrammarDeriveArgs]) -> 'MageGrammar':
        return super().derive(**kwargs)


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
        return MageRepeatExpr(min=expr.min, max=expr.max, expr=new_expr, actions=expr.actions, label=expr.label, parent=expr.parent)
    if isinstance(expr, MageLookaheadExpr):
        new_expr = proc(expr.expr)
        if new_expr is expr.expr:
            return expr
        return MageLookaheadExpr(expr=new_expr, is_negated=expr.is_negated, actions=expr.actions, label=expr.label, parent=expr.parent)
    if isinstance(expr, MageHideExpr):
        new_expr = proc(expr.expr)
        if new_expr is expr.expr:
            return expr
        return MageHideExpr(expr=new_expr, actions=expr.actions, label=expr.label, parent=expr.parent)
    if isinstance(expr, MageListExpr):
        new_element = proc(expr.element)
        new_separator = proc(expr.separator)
        if new_element is expr.element and new_separator is expr.separator:
            return expr
        return MageListExpr(element=new_element, separator=new_separator, min_count=expr.min_count, actions=expr.actions, label=expr.label, parent=expr.parent)
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
        return MageChoiceExpr(elements=new_elements, actions=expr.actions, label=expr.label, parent=expr.parent)
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
        return MageSeqExpr(elements=new_elements, actions=expr.actions, label=expr.label, parent=expr.parent)
    assert_never(expr)

def rewrite_each_rule[T: MageGrammar | MageModule](node: T, proc: Callable[[MageRule], MageRule]) -> T:
    new_elements = list[MageModuleElement]()
    for element in node.elements:
        if isinstance(element, MageRule):
            new_elements.append(proc(element))
        elif isinstance(element, MageModule):
            new_elements.append(rewrite_each_rule(element, proc))
        else:
            assert_never(element)
    return cast(T, node.derive(elements=new_elements))

def rewrite_each_expr(grammar: MageGrammar, proc: Callable[[MageExpr], MageExpr]) -> MageGrammar:
    def rewrite_rule(rule: MageRule) -> MageRule:
        if rule.expr is None:
            return rule
        return rule.derive(expr=proc(rule.expr))
    return rewrite_each_rule(grammar, rewrite_rule)

def rewrite_module[T: MageGrammar | MageModule](module: T, proc: Callable[[MageModuleElement], MageModuleElement]) -> T:
    new_elements = []
    changed = False
    for element in module.elements:
        new_element = proc(element)
        if new_element is not element:
            changed = True
        new_elements.append(new_element)
    if not changed:
        return module
    return cast(T, module.derive(elements=new_elements))

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

def referenced(expr: MageExpr) -> list[MageRule]:
    out = []
    def visit(expr: MageExpr) -> None:
        if isinstance(expr, MageRefExpr):
            rule = lookup_ref(expr)
            if rule is not None:
                out.append(rule)
            return
        for_each_direct_child_expr(expr, visit)
    visit(expr)
    return out

def is_static(expr: MageExpr, visited: set[MageRule] | None = None) -> bool:
    if visited is None:
        visited = set[MageRule]()
    if isinstance(expr, MageRefExpr):
        rule = expr.grammar.lookup(expr.name)
        if rule is None or rule.expr is None or rule in visited:
            return False
        visited.add(rule)
        return is_static(rule.expr, visited)
    if isinstance(expr, MageLitExpr):
        return True
    if isinstance(expr, MageCharSetExpr):
        return len(expr) == 1
    if isinstance(expr, MageSeqExpr):
        return all(is_static(element, visited) for element in expr.elements)
    if isinstance(expr, MageChoiceExpr):
        # FIXME should I check whether the choices are actually different?
        return False
    if isinstance(expr, MageRepeatExpr):
        # Only return true if we're dealing with a fixed width repition
        return expr.min == expr.max and is_static(expr.expr, visited)
    if isinstance(expr, MageListExpr):
        # List expressions always repeat an unpredictable amount of times
        return False
    if isinstance(expr, MageLookaheadExpr):
        # Lookahead has no effect on what (non-)static characters are generated
        return True
    if isinstance(expr, MageHideExpr):
        return is_static(expr.expr, visited)
    assert_never(expr)


def is_token(rule: MageRule, visited: set[MageRule] | None = None) -> bool:
    if visited is None:
        visited = set[MageRule]()
    if rule.is_lex:
        # A rule that was explicitly declared a token is always a token
        return True
    if rule.expr is None:
        # If it was not explicitly declared a lexer token, a rule with no
        # expression can never be a token
        return False
    return is_static(rule.expr, visited) and not any(is_token(rule, visited) for rule in referenced(rule.expr))


def make_list_expr(element: MageExpr, separator: MageExpr, min_count = 0) -> MageExpr:
    out = MageSeqExpr([
        element,
        MageRepeatExpr(
            min=max(0, min_count-1),
            max=POSINF,
            expr=MageSeqExpr([
                separator,
                element,
            ])
        )
    ])
    if min_count > 0:
        return out
    return MageChoiceExpr([ out, MageLitExpr('') ])


def match_list_expr(expr: MageExpr) -> tuple[MageExpr, MageExpr, int] | None:
    """
    Try to detect a compiled list expression.

    List expressions used to be part of the grammar but are now composed out of
    other constructs.

    This function assumes that the expression has been simplified before this
    function was called. For example, `(a* | a) | ''` will not be detected,
    while `a* | a | ''` will be.
    """
    min_count = 1
    if isinstance(expr, MageChoiceExpr):
        if len(expr.elements) != 2 or not isinstance(expr.elements[1], MageLitExpr) or expr.elements[1].text != '':
            return
        expr = expr.elements[0]
        min_count = 0
    if not (isinstance(expr, MageSeqExpr)
            and len(expr.elements) == 2
            and isinstance(expr.elements[1], MageRepeatExpr)
            and isinstance(expr.elements[1].expr, MageSeqExpr)):
        return
    min_count += expr.elements[1].min
    element = expr.elements[1].expr.elements[1]
    separator = expr.elements[1].expr.elements[0]
    return element, separator, min_count

