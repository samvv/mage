
from collections.abc import Callable, Iterable, Sequence
from types import UnionType, NoneType
import typing
from typing import Any, Literal, Self, TypeAliasType
import inspect
from copy import copy

from magelang.runtime.collections import Punctuated
from magelang.runtime.text import Span

__all__ = [
    'BaseSyntax',
    'BaseNode',
    'BaseToken',
]

type Type = Any

class CoerceError(RuntimeError):

    def __init__(self, value: Any, ty: Type) -> None:
        super().__init__(f"failed to coerce {value} to {ty}")

def get_default_values(cls) -> dict[str, Any]:
    boring = dir(type('dummy', (object,), {}))
    d = {}
    for name, value in inspect.getmembers(cls):
        if not name.startswith('_') and not callable(value) and name not in boring and not isinstance(value, property):
            d[name] = value
    return d

def _get[T](seq: Sequence[T], index: int, default: T) -> T:
    return default if index >= len(seq) or index < 0 else seq[index]

def _is_default_constructible(ty: Type) -> bool:
    cls = typing.get_origin(ty) or ty
    if not inspect.isclass(cls):
        return False
    if issubclass(cls, BaseToken):
        ann = typing.get_type_hints(cls)
        defs = get_default_values(cls)
        return not bool(ann.keys() - defs.keys())
    return cls in [ list, Punctuated ]

def _construct_default(ty: Type) -> Any:
    return None if _is_optional(ty) else ty()

def _is_optional(ty: Type) -> bool:
    if ty is NoneType:
        return True
    origin = typing.get_origin(ty)
    if origin is typing.Union or origin is UnionType:
        args = typing.get_args(ty)
        return any(_is_optional(arg) for arg in args)
    return False

def hasmethod(value: Any, name: str) -> bool:
    return hasattr(value, name) \
        and callable(getattr(value, name))

def expand(value: Any) -> Iterable[tuple[Any, Any]]:
    if isinstance(value, list) or isinstance(value, tuple):
        for i in range(len(value)):
            yield i, value[i]
    elif isinstance(value, dict):
        yield from value.items()
    elif hasmethod(value, '_expand'):
        yield from value._expand()
    else:
        pass

def resolve(value: Any, key: Any) -> Any:
    if hasmethod(key, '_resolve'):
        method = getattr(key, '_resolve')
        return method(value)
    if isinstance(key, list):
        result = value
        for element in key:
            result = resolve(result, element)
        return result
    if isinstance(key, int) or isinstance(key, str):
        return value[key]
    raise TypeError(f'could not determine how to resolve a value with key {key}')

def last[T](iterator: Iterable[T]) -> T | None:
    try:
        last_element = next(iter(iterator))
    except StopIteration:
        return
    for element in iterator:
        last_element = element
    return last_element

def first[T](iterator: Iterable[T]) -> T | None:
    try:
        return next(iter(iterator))
    except StopIteration:
        pass

def increment_key(value: Any, key: Any, expand=expand) -> Any | None:

    if hasmethod(key, 'increment'):
        return key.increment(value)

    match key:

        case list():

            # pre-populate a list of child nodes of self.root so we can access them
            # easily
            values = [ value ]
            for element in key:
                value = resolve(value, element)
                values.append(value)

            # if we still can go deeper we should try that first
            result = first(expand(value))
            if result is not None:
                element, _child = result
                new_key = copy(key)
                new_key.append(element)
                return new_key

            # go up until we find a key that we can increment
            for i in reversed(range(0, len(key))):
                element = key[i]
                new_element = increment_key(values[i], element)
                if new_element is not None:
                    new_key = key[:i]
                    new_key.append(new_element)
                    return new_key

            # we went up beyond the root node
            return None

        case int():
            return key+1 if key < len(value)-1 else None

        case str():
            keys = iter(value.keys())
            for k in keys:
                if k == key:
                    break
            try:
                return next(keys)
            except StopIteration:
                return None

        case _:
            raise RuntimeError(f'did not know how to increment key {key}')

def decrement_key(value: Any, key: Any, expand=expand) -> Any:

    if hasmethod(key, 'decrement'):
        return key.decrement(value)

    match key:

        case list():

            # pre-populate a list of child nodes of self.root so we can access them
            # easily
            last_value_parent = None
            for element in key:
                last_value_parent = value
                value = resolve(value, element)

            if not key:
                return None

            last_element = key[-1]
            new_element = decrement_key(last_value_parent, last_element)

            if new_element is None:
                return key[:-1]

            new_key = key[:-1]
            new_key.append(new_element)

            # get the rightmost node relative to the node on the new key
            value = resolve(last_value_parent, new_element)
            while True:
                result = last(expand(value))
                if result is None:
                    break
                child_key, value = result
                # self.elements.append(child_key)
                new_key.append(child_key)

            return new_key

        case int():
            return key-1 if key > 0 else None

        case str():
            last_key = None
            for k, _v in value.items():
                if k == key:
                    break
                last_key = k
            return last_key

        case _:
            raise RuntimeError(f'did not know how to decrement key {key}')

type ExpandFn = Callable[[Any], Iterable[tuple[Any, Any]]]

def preorder(root: Any, expand: ExpandFn = expand) -> Iterable[Any]:
    stack = [ root ]
    while stack:
        node = stack.pop()
        yield node
        for _key, value in reversed(list(expand(node))):
            stack.append(value)

def preorder_with_paths(root: Any, expand: ExpandFn = expand) -> Iterable[Any]:
    stack = [ ([], root) ]
    while stack:
        path, node = stack.pop()
        yield path, node
        for (key, value) in expand(node):
            stack.append((path + [ key ], value))

def coerce(value: Any, ty: Type, forbid_default: bool = False) -> Any:

    # short-circuit on the case where value is already a ty
    if inspect.isclass(ty) and isinstance(value, ty):
        return value

    # coercing to any always succeeds
    if ty is Any:
        return value

    if type(ty) is TypeAliasType:
        return coerce(value, ty.__value__)

    # try all element types in a union type
    origin = typing.get_origin(ty) or ty
    if origin is typing.Union or origin is UnionType:
        for arg in typing.get_args(ty):
            try:
                return coerce(value, arg, True)
            except CoerceError:
                pass
        raise CoerceError(value, ty)

    # if `value` is None and the type is not explicitly None, we attempt to
    # construct a default value
    if value is None and not forbid_default and _is_default_constructible(ty):
        return _construct_default(ty)

    # all special types should be handled by now
    # assert(inspect.isclass(origin))

    # construct a token from its single field
    if inspect.isclass(origin) and issubclass(origin, BaseToken):
        hints = typing.get_type_hints(origin)
        defs = get_default_values(origin)
        required = {}
        for field_name, field_ty in hints.items():
            if field_name not in defs:
                required[field_name] = field_ty
        if len(required) == 1:
            field_name, field_ty = next(iter(required.items()))
            kwargs = {
                field_name: coerce(value, field_ty),
            }
            return origin(**kwargs)

    # map coercion over a tuple type
    if type(value) is tuple and origin is tuple:
        args = typing.get_args(ty)
        new_elements = []
        for i, element in enumerate(value):
            new_elements.append(coerce(element, args[i], False))
        return tuple(new_elements)

    # construct a tuple when the main type is given
    if origin is tuple:
        args = typing.get_args(ty)
        required = [ (i, arg) for i, arg in enumerate(args) if not _is_optional(arg) and not _is_default_constructible(arg) ]
        if len(required) == 1:
            k, main_ty = required[0]
            new_elements = []
            for i, arg in enumerate(args):
                new_elements.append(coerce(value, main_ty, True) if i == k else _construct_default(arg))
            return tuple(new_elements)

    # repeat a punctuated type
    if isinstance(value, int) and origin is Punctuated:
        p = Punctuated()
        args = typing.get_args(ty)
        el_ty = _get(args, 0, Any)
        sep_ty = _get(args, 1, Any)
        for _ in range(value-1):
            p.append(
                _construct_default(el_ty),
                _construct_default(sep_ty)
            )
        p.append_final(_construct_default(el_ty))

    # coerce list to a punctuated type
    if type(value) is list and origin is Punctuated:
        args = typing.get_args(ty)
        el_ty = _get(args, 0, Any)
        sep_ty = _get(args, 1, Any)
        out = Punctuated()
        for element in value:
            new_el, new_sep = coerce(element, tuple[el_ty, sep_ty | None], True)
            if new_sep is not None:
                out.append(new_el, new_sep)
            else:
                out.append_final(new_el)
        return out

    # map coercion over a punctuated type
    if type(value) is Punctuated and origin is Punctuated:
        args = typing.get_args(ty)
        el_ty = _get(args, 0, Any)
        sep_ty = _get(args, 1, Any)
        out = Punctuated()
        for element, separator in value:
            new_element = coerce(element, el_ty, True)
            if separator is not None:
                new_separator = coerce(separator, sep_ty, True)
                out.append(new_element, new_separator)
            else:
                out.append_final(new_element)
        return out

    # repeat a list type
    if isinstance(value, int) and origin is list:
        args = typing.get_args(ty)
        el_ty = _get(args, 0, Any)
        return [ _construct_default(el_ty) for _ in range(value) ]

    # map coercion over a list
    if type(value) is list and origin is list:
        args = typing.get_args(ty)
        el_ty = _get(args, 0, Any)
        return [ coerce(element, el_ty, True) for element in value ]

    raise CoerceError(value, ty)

class BaseSyntax:

    def __init__(self, *args, **kwargs) -> None:
        self.parent = None
        self._prev_sibling: BaseSyntax | Literal[False] | None = False
        self._next_sibling: BaseSyntax | Literal[False] | None = False
        hints = typing.get_type_hints(self.__class__)
        to_visit = list(hints)
        for name, value in kwargs.items():
            setattr(self, name, coerce(value, hints[name]))
            to_visit.remove(name)
        for arg in args:
            name = to_visit[0]
            setattr(self, name, coerce(arg, hints[name]))
            to_visit.remove(name)
        for name in to_visit:
            setattr(self, name, coerce(None, hints[name]))

    def derive(self, **kwargs) -> Self:
        fields = self.get_fields()
        fields.update(kwargs)
        return self.__class__(**fields)

    def get_fields(self) -> dict[str, Any]:
        d = {}
        for name in typing.get_type_hints(type(self)):
            d[name] = getattr(self, name)
        return d

    def _expand(self) -> Iterable[tuple[str, Any]]:
        return self.get_fields().items()

    def has_parent(self) -> bool:
        return self.parent is not None

    @property
    def parent_path(self) -> list[int | str]:
        assert(self.parent is not None)
        for path, node in preorder_with_paths(self.parent, expand=_expand_no_basenode):
            if node is self:
                return path
        raise RuntimeError(f"node {self} not found in its parent")

    def get_full_path(self):
        path = []
        node = self
        while True:
            assert(node.parent_path is not None)
            path.extend(reversed(node.parent_path))
            node = node.parent
            if node is None:
                break
        path.reverse()
        return path

    def get_child_nodes(self) -> Iterable['BaseSyntax']:
        for field_value in self.get_fields().values():
            for child in preorder(field_value, expand=_expand_no_basenode):
                if isinstance(child, BaseSyntax):
                    yield child

    @property
    def first_child(self) -> 'BaseSyntax | None':
        return first(self.get_child_nodes())

    @property
    def last_child(self) -> 'BaseSyntax | None':
        # TODO optimize this
        return last(self.get_child_nodes())

    @property
    def prev_token(self) -> 'BaseToken | None':
        prev = self.prev_sibling
        while prev is not None and not isinstance(prev, BaseToken):
            prev = prev.last_child
        return prev

    @property
    def next_token(self) -> 'BaseToken | None':
        next = self.next_sibling
        while next is not None and not isinstance(next, BaseToken):
            next = next.first_child
        return next

    @property
    def prev_sibling(self) -> 'BaseSyntax | None':
        """
        Return the previous node that has the same parent as this node.
        """
        if self._prev_sibling != False:
            return self._prev_sibling
        path = self.parent_path
        while True:
            path = decrement_key(self.parent, path, expand=_expand_no_basenode)
            # `path` may be `None`, but also `[]`
            if not path:
                return None
            value = resolve(self.parent, path)
            if isinstance(value, BaseNode):
                node = value
                # while node.last_child:
                #     node = node.last_child
                break
        self._prev_sibling = node
        if node is not None:
            node._next_sibling = self
        return node

    def set_parents(self) -> None:
        for child in self.get_child_nodes():
            child.parent = self
            child.set_parents()

    @property
    def next_sibling(self) -> 'BaseSyntax | None':
        """
        Return the next node that has the same parent as this node.
        """
        if self._next_sibling != False:
            return self._next_sibling
        node = self.parent
        path = self.parent_path
        while True:
            if node is None:
                return None
            path = increment_key(node, path, expand=_expand_no_basenode)
            if path is None:
                return None
                # path = node.path
                # node = node.parent
            else:
                value = resolve(node, path)
                if isinstance(value, BaseNode):
                    node = value
                    break
        self._next_sibling = node
        if node is not None:
            node._prev_sibling = self
        return node

def _expand_no_basenode(value):
    if not isinstance(value, BaseNode):
        yield from expand(value)

class BaseNode(BaseSyntax):
    pass

class BaseToken(BaseSyntax):
    span: Span | None = None
