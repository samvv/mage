
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
    'Metadata',
    'Required',
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

@lru_cache
def _is_default_constructible(ty: Type) -> bool:
    if ty is None or ty is NoneType:
        return True
    origin = typing.get_origin(ty) or ty
    if origin is Annotated:
        real_ty, *annotations = typing.get_args(ty)
        for annotation in annotations:
            if isinstance(annotation, Required):
                return False
        return _is_default_constructible(real_ty)
    if origin is UnionType or origin is typing.Union:
        args = typing.get_args(ty)
        for arg in reversed(args):
            if _is_default_constructible(arg):
                return True
        return False
    if not inspect.isclass(origin):
        return False
    if issubclass(origin, BaseSyntax):
        for field_ty in typing.get_type_hints(origin).values():
            if not _is_default_constructible(field_ty):
                return False
        return True
    if issubclass(origin, tuple):
        args = typing.get_args(ty)
        for arg in args:
            if not _is_default_constructible(arg):
                return False
        return True
    if issubclass(origin, list) or issubclass(origin, Punctuated):
        return True
    return False

class ConstructError(RuntimeError):
    pass

def _construct_default(ty: Type) -> Any:
    """
    Construct the default value for a given type.

    For union types, this method will attempt to try each member type from left to right.
    """
    if ty is None or ty is NoneType:
        return None
    origin = typing.get_origin(ty) or ty
    if origin is UnionType or origin is typing.Union:
        args = typing.get_args(ty)
        for arg in reversed(args):
            if _is_default_constructible(arg):
                return _construct_default(arg)
        raise ConstructError()
    if type(ty) is TypeAliasType:
        return _construct_default(ty.__value__)
    assert(inspect.isclass(origin))
    if issubclass(origin, BaseSyntax):
        return origin()
    classes = [ list, Punctuated ]
    for cls in classes:
        if issubclass(origin, cls):
            return ty()
    raise ConstructError()

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

@dataclass(frozen=True)
class Metadata:
    isinstance_check: Callable[[Any], bool] | None = None

@dataclass(frozen=True)
class Required:
    pass

def ident[T](x: T) -> T: return x

def const[T](x: T) -> Callable[..., T]:
    def proc(*args, **kwargs):
        return x
    return proc

def coerce(value: Any, ty: Type) -> Any:
    proc = coercer(type(value), ty)
    return proc(value)

@lru_cache
def coercer(src: Type, dst: Type) -> Callable[[Any], Any]:
    """
    Compile a function that can coerce a value of a source type to a destination type.

    Special annotations may modifiy the behavior of this function.

    In the absence of type hints, this function will compile a dynamic function
    that inspects the type at runtime. This should be considered an implementation detail.
    """

    visited = set()

    def proc(src: Type, dst: Type) -> Callable[[Any], Any]:

        key = (src, dst)
        if key in visited:
            raise CoerceError(src, dst, "infinite recursion")
        visited.add((src, dst))

        # process annotated types
        if typing.get_origin(src) is Annotated:
            src, *annotations= typing.get_args(src)
        if typing.get_origin(dst) is Annotated:
            dst, *annotations= typing.get_args(dst)

        # short-circuit on the case where src is already a dst
        if inspect.isclass(dst) and issubclass(src, dst):
            return ident

        # coercing to any always succeeds
        if dst is Any:
            return ident

        # cover the cases where the value is `None`
        if src is None or src is NoneType:
            if _is_optional(dst):
                return const(None)
            if _is_default_constructible(dst):
                return lambda _: _construct_default(dst)
            raise CoerceError(src, dst, "type does not allow None and is also not default-constructible")

        if dst is None:
            raise CoerceError(src, dst, "cannot coerce non-null source type to None")

        # resolve type aliases
        if type(dst) is TypeAliasType:
            return proc(src, dst.__value__)

        src_origin = typing.get_origin(src) or src
        dst_origin = typing.get_origin(dst) or dst

        # try all element types in a union type
        if dst_origin is typing.Union or dst_origin is UnionType:
            args = typing.get_args(dst)
            for arg in args:
                try:
                    return proc(src, arg)
                except CoerceError:
                    pass
            raise CoerceError(src, dst, f"could not coerce {src} to any of the union elements in {dst}")

        # all special types should be handled by now
        assert(inspect.isclass(dst_origin))

        # construct a node or token from its single field
        if issubclass(dst_origin, BaseSyntax):
            hints = typing.get_type_hints(dst_origin)
            required = []
            for field_name, field_ty in hints.items():
                print(field_name, field_ty, _is_default_constructible(field_ty))
                if not _is_default_constructible(field_ty):
                    required.append((field_name, field_ty))
            print(dst_origin, required)
            if len(required) == 1:
                field_name, field_ty = required[0]
                coerce_field = proc(src, field_ty)
                def apply(value):
                    return dst_origin(**{
                        field_name: coerce_field(value),
                    })
                return apply

        # map coercion over a tuple type
        if src_origin is tuple and dst_origin is tuple:
            src_args = typing.get_args(src)
            dst_args = typing.get_args(dst)
            if len(dst_args) == 0:
                return ident
            if len(src_args) == 0:
                def apply(value):
                    assert(len(value) == len(dst_args))
                    return tuple(coerce(element, ty) for element, ty in zip(value, dst_args))
                return apply
            if len(src_args) != len(dst_args):
                raise CoerceError(src, dst, f"tuple types are not of equal size")
            el_coercers = [ proc(arg_1, arg_2) for arg_1, arg_2 in zip(src_args, dst_args) ]
            def apply(value):
                assert(len(value) == len(el_coercers))
                return tuple(el_coercers[i](value[i]) for i in range(len(el_coercers)))
            return apply

        # construct a tuple when there is only one required element
        if dst_origin is tuple:
            args = typing.get_args(dst)
            k = None
            for i, arg in enumerate(args):
                try:
                    print(src, arg)
                    coerce_main = proc(src, arg)
                except CoerceError:
                    if not _is_default_constructible(arg):
                        raise CoerceError(src, arg, f"the element {arg} of the tuple should be default-constructible")
                    continue
                if k:
                    raise CoerceError(src, dst, "tuple has more than one candidate into which the given value fits")
                k = i
            if k is not None:
                def apply(value):
                    return tuple(coerce_main(value) if i == k else _construct_default(args[i]) for i in range(len(args)))
                return apply
            # raise CoerceError(src, dst, "could not coerce value to any of the tuple elements")

        # repeat a punctuated type
        if issubclass(src_origin, int) and dst_origin is Punctuated:
            args = typing.get_args(dst)
            item_ty = _get(args, 0, Any)
            sep_ty = _get(args, 1, Any)
            def apply(value):
                out = Punctuated()
                for _ in range(value-1):
                    out.append(
                        _construct_default(item_ty),
                        _construct_default(sep_ty)
                    )
                out.append_final(_construct_default(item_ty))
                return out
            return apply

        # coerce list to a punctuated type
        if issubclass(src_origin, list) and dst_origin is Punctuated:
            src_args = typing.get_args(src)
            dst_args = typing.get_args(dst)
            src_el_ty = _get(src_args, 0, Any)
            dst_item_ty = _get(dst_args, 0, Any)
            dst_sep_ty = _get(dst_args, 1, Any)
            if len(src_args) == 0:
                def apply(value):
                    out = Punctuated()
                    last = len(value)-1
                    for i, element in enumerate(value):
                        if i == last:
                            new_item, _new_sep = coerce(element, tuple[dst_item_ty, None])
                            out.append_final(new_item)
                        else:
                            new_item, new_sep = coerce(element, tuple[dst_item_ty, dst_sep_ty])
                            out.append(new_item, new_sep)
                    return out
                return apply
            coerce_mid = proc(src_el_ty, tuple[dst_item_ty, dst_sep_ty])
            coerce_final = proc(src_el_ty, tuple[dst_item_ty, None])
            def apply(value):
                out = Punctuated()
                last = len(value)-1
                for i, element in enumerate(value):
                    if i == last:
                        new_item = coerce_final(element)
                        out.append_final(new_item)
                    else:
                        new_item, new_sep = coerce_mid(element)
                        out.append(new_item, new_sep)
                return out
            return apply

        # map coercion over a punctuated type
        if issubclass(src_origin, Punctuated) and dst_origin is Punctuated:
            src_args = typing.get_args(src)
            dst_args = typing.get_args(dst)
            src_el_ty = _get(src_args, 0, Any)
            src_sep_ty = _get(src_args, 1, Any)
            dst_item_ty = _get(dst_args, 0, Any)
            dst_sep_ty = _get(dst_args, 1, Any)
            if len(dst_args) == 0:
                return ident
            if len(src_args) == 0:
                def apply(value):
                    out = Punctuated()
                    for item, separator in value:
                        new_item = coerce(item, dst_item_ty)
                        if separator is not None:
                            new_separator = coerce(separator, dst_sep_ty)
                            out.append(new_item, new_separator)
                        else:
                            out.append_final(new_item)
                    return out
                return apply
            coerce_item = proc(src_el_ty, dst_item_ty)
            coerce_separator = proc(src_sep_ty, dst_sep_ty)
            def apply(value):
                out = Punctuated()
                for item, separator in value:
                    new_item = coerce_item(item)
                    if separator is not None:
                        new_separator = coerce_separator(separator)
                        out.append(new_item, new_separator)
                    else:
                        out.append_final(new_item)
                return out
            return apply

        # repeat a list type
        if issubclass(src_origin, int) and dst_origin is list:
            args = typing.get_args(dst)
            el_ty = _get(args, 0, Any)
            def apply(value):
                return [ _construct_default(el_ty) for _ in range(value) ]
            return apply

        # map coercion over a list
        if issubclass(src_origin, list) and dst_origin is list:
            src_args = typing.get_args(src)
            dst_args = typing.get_args(dst)
            src_el_ty = _get(src_args, 0, Any)
            dst_el_ty = _get(dst_args, 0, Any)
            if len(dst_args) == 0:
                return ident
            if len(src_args) == 0:
                def apply(value):
                    return [ coerce(element, dst_el_ty) for element in value ]
                return apply
            coerce_element = proc(src_el_ty, dst_el_ty)
            def apply(value):
                return [ coerce_element(element) for element in value ]
            return apply

        raise CoerceError(src, dst, f"no rules were able to coerce into the target type")

    return proc(src, dst)

class BaseSyntax:

    def __init__(self, *args, **kwargs) -> None:
        self.parent: BaseSyntax | None = None
        self._prev_sibling: BaseSyntax | Literal[False] | None = False
        self._next_sibling: BaseSyntax | Literal[False] | None = False

        hints = typing.get_type_hints(self.__class__, include_extras=True)

        # parse keyword arguments first
        for name, value in kwargs.items():
            if name not in hints:
                raise TypeError(f"keyword argument '{name}' does not name a field in {self.__class__.__name__}")
            setattr(self, name, coerce(value, hints[name]))

        opt = []

        k = 0
        for name in hints:
            if name in kwargs:
                continue
            ty = hints[name]
            if _is_default_constructible(ty):
                # defer optional arguments till after required arguments are parsed
                opt.append(name)
            else:
                # parse a positional required arg
                if k >= len(args):
                    raise TypeError(f"expected a value for required argument '{name}' in {self.__class__.__name__}")
                arg = args[k]
                k += 1
                setattr(self, name, coerce(arg, hints[name]))

        l = 0
        while k < len(args):
            if l >= len(opt):
                raise TypeError(f"excess positional arguments provided to {self.__class__.__name__}: {', '.join(args[k:])}")
            name = opt[l]
            l += 1
            arg = args[k]
            k += 1
            setattr(self, name, coerce(arg, hints[name]))

        # initialize omitted arguments with their defaults
        while l < len(opt):
            name = opt[l]
            l += 1
            setattr(self, name, _construct_default(hints[name]))

    def derive(self, **kwargs) -> Self:
        fields = self.get_fields()
        fields.update(kwargs)
        return self.__class__(**fields)

    def get_fields(self) -> dict[str, Any]:
        # TODO probably can be made faster
        d = {}
        for name in typing.get_type_hints(type(self)):
            d[name] = getattr(self, name)
        return d

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def keys(self) -> Iterable[str]:
        # TODO probably can be made faster
        return self.get_fields().keys()

    def _expand(self) -> Iterable[tuple[str, Any]]:
        return self.get_fields().items()

    def has_parent(self) -> bool:
        return self.parent is not None

    @cached_property
    def parent_path(self) -> list[int | str]:
        assert(self.parent is not None)
        for name, value in self.parent.get_fields().items():
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
            node = node.parent
            if node is None:
                break
        path.reverse()
        return path

    def set_parents(self) -> None:
        for child in self.get_child_nodes():
            child.parent = self
            child.set_parents()

    def get_child_nodes(self) -> Iterable['BaseSyntax']:
        for field_value in self.get_fields().values():
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
            path = decrement_key(self.parent, path, expand=_expand_no_syntax)
            # `path` may be `None`, but also `[]`
            if not path:
                return None
            value = resolve(self.parent, path)
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
        node = self.parent
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
        curr = self.parent
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
            if curr.parent is None:
                return
            path = curr.parent_path
            curr = curr.parent
