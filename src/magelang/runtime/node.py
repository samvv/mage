
from dataclasses import dataclass
from collections.abc import Callable, Iterable, Sequence
from types import UnionType, NoneType
import typing
from typing import Any, Literal, Self, TypeAliasType, Annotated, Callable
import inspect
from functools import cached_property, lru_cache

from magelang.runtime.collections import Punctuated
from magelang.runtime.text import Span

__all__ = [
    'BaseSyntax',
    'BaseNode',
    'BaseToken',
]

type Type = Any

class CoerceError(RuntimeError):

    def __init__(self, value: Any, ty: Type, message: str | None) -> None:
        super().__init__(f"failed to coerce {repr(value)} to {ty}: {message}")

# def get_default_values(cls) -> dict[str, Any]:
#     boring = dir(type('dummy', (object,), {}))
#     d = {}
#     for name, value in inspect.getmembers(cls):
#         if not name.startswith('_') and not callable(value) and name not in boring and not isinstance(value, property):
#             d[name] = value
#     return d

def _get[T](seq: Sequence[T], index: int, default: T) -> T:
    return default if index >= len(seq) or index < 0 else seq[index]

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

            # go up until we find a key that we can increment
            for i in reversed(range(len(key))):
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

def preorder_with_paths(root: Any, expand: ExpandFn = expand, path: list[Any] | None = None) -> Iterable[Any]:
    if path is None:
        path = []
    stack = [ (path, root) ]
    while stack:
        path, node = stack.pop()
        yield path, node
        for (key, value) in expand(node):
            stack.append((path + [ key ], value))

class BaseSyntax:

    _fields_: tuple[str, ...]

    def __init__(self, *args, **kwargs) -> None:
        self._parent: BaseSyntax | None = None
        self._prev_sibling: BaseSyntax | Literal[False] | None = False
        self._next_sibling: BaseSyntax | Literal[False] | None = False

    def derive(self, **kwargs) -> Self:
        fields = self.get_fields()
        fields.update(kwargs)
        return self.__class__(**fields)

    def get_fields(self) -> dict[str, Any]:
        out = {}
        for name in self.keys():
            out[name] = getattr(self, name)
        return out

    def __getitem__(self, key: str) -> Any:
        assert(key in self.keys())
        return getattr(self, key)

    def keys(self) -> Iterable[str]:
        return self.__class__._fields_

    def values(self) -> Iterable[Any]:
        for name in self.keys():
            yield getattr(self, name)

    def _expand(self) -> Iterable[tuple[str, Any]]:
        for name in self.keys():
            yield name, getattr(self, name)

    def has_parent(self) -> bool:
        return self._parent is not None

    @cached_property
    def parent_path(self) -> list[int | str]:
        assert(self._parent is not None)
        for name, value in self._parent._expand():
            for path, node in preorder_with_paths(value, expand=_expand_no_syntax, path=[ name ]):
                if node is self:
                    return path
        raise RuntimeError(f"node {self} not found in its parent")

    def get_full_path(self):
        path = []
        node = self
        while True:
            assert(node.parent_path is not None)
            path.extend(reversed(node.parent_path))
            node = node._parent
            if node is None:
                break
        path.reverse()
        return path

    def set_parents(self) -> None:
        for child in self.get_child_nodes():
            child._parent = self
            child.set_parents()

    def get_child_nodes(self) -> Iterable['BaseSyntax']:
        for field_value in self.values():
            for child in preorder(field_value, expand=_expand_no_syntax):
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
    def prev_sibling(self) -> 'BaseSyntax | None':
        """
        Return the previous node that has the same parent as this node.
        """
        if self._prev_sibling != False:
            return self._prev_sibling
        path = self.parent_path
        while True:
            path = decrement_key(self._parent, path, expand=_expand_no_syntax)
            # `path` may be `None`, but also `[]`
            if not path:
                return None
            value = resolve(self._parent, path)
            if isinstance(value, BaseSyntax):
                node = value
                # while node.last_child:
                #     node = node.last_child
                break
        self._prev_sibling = node
        if node is not None:
            node._next_sibling = self
        return node

    @property
    def next_sibling(self) -> 'BaseSyntax | None':
        """
        Return the next node that has the same parent as this node.
        """
        if self._next_sibling != False:
            return self._next_sibling
        node = self._parent
        path = self.parent_path
        while True:
            if node is None:
                return None
            path = increment_key(node, path, expand=_expand_no_syntax)
            if path is None:
                return None
                # path = node.path
                # node = node.parent
            else:
                value = resolve(node, path)
                if isinstance(value, BaseSyntax):
                    node = value
                    break
        self._next_sibling = node
        if node is not None:
            node._prev_sibling = self
        return node

def _expand_no_syntax(value):
    if not isinstance(value, BaseSyntax):
        yield from expand(value)

class BaseNode(BaseSyntax):
    pass

class BaseToken(BaseSyntax):

    def __init__(self, *args, span: Span | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.span = span

    @cached_property
    def next_token(self) -> 'BaseToken | None':
        curr = self._parent
        if curr is None:
            return
        path = self.parent_path
        while curr is not None:
            path = increment_key(curr, path, expand=_expand_no_syntax)
            if path:
                value = resolve(curr, path)
                while True:
                    if not value:
                        break
                    if isinstance(value, BaseToken):
                        return value
                    key, value = next(iter(expand(value)))
                    path.append(key)
                continue
            if curr._parent is None:
                return
            path = curr.parent_path
            curr = curr._parent
