
from collections.abc import Sequence
from types import UnionType
import typing
from typing import Any, Self
import inspect

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

def _get[T](seq: Sequence[T], index: int, default: T) -> T:
    return default if index >= len(seq) or index < 0 else seq[index]

def is_default_constructible(ty: Type) -> bool:
    cls = typing.get_origin(ty) or ty
    if issubclass(cls, BaseToken):
        return not typing.get_type_hints(cls)
    return cls in [ list, Punctuated ]

def construct_default(ty: Type) -> Any:
    return ty()

def is_optional(ty: Type) -> bool:
    if ty is None:
        return True
    origin = typing.get_origin(ty)
    if origin is typing.Union or origin is UnionType:
        args = typing.get_args(ty)
        return any(is_optional(arg) for arg in args)
    return False

def coerce(value: Any, ty: Type, forbid_default: bool = False) -> Any:

    # short-circuit on the case where value is already a ty
    if inspect.isclass(ty) and isinstance(value, ty):
        return value

    # handle special types
    if ty is Any:
        return value

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
    if value is None and not forbid_default and is_default_constructible(ty):
        return construct_default(ty)

    # map coercion over a tuple type
    if type(value) is tuple and origin is tuple:
        args = typing.get_args(ty)
        new_elements = []
        for i, element in enumerate(value):
            new_elements.append(coerce(element, args[i], False))
        return tuple(new_elements)

    if origin is tuple:
        args = typing.get_args(ty)
        required = [ (i, arg) for i, arg in enumerate(args) if not is_optional(arg) and not is_default_constructible(arg) ]
        if len(required) == 1:
            k, main_ty = required[0]
            new_elements = []
            for i, arg in enumerate(args):
                new_elements.append(coerce(value, main_ty, True) if i == k else construct_default(arg))
            return tuple(new_elements)

    # repeat a punctuated type
    if isinstance(value, int) and origin is Punctuated:
        p = Punctuated()
        args = typing.get_args(ty)
        el_ty = _get(args, 0, Any)
        sep_ty = _get(args, 1, Any)
        for _ in range(value-1):
            p.append(
                construct_default(el_ty),
                construct_default(sep_ty)
            )
        p.append_final(construct_default(el_ty))

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
        return [ construct_default(el_ty) for _ in range(value) ]

    # map coercion over a list
    if type(value) is list and origin is list:
        args = typing.get_args(ty)
        el_ty = _get(args, 0, Any)
        return [ coerce(element, el_ty, True) for element in value ]

    raise CoerceError(value, ty)

class BaseSyntax:

    def __init__(self, *args, **kwargs) -> None:
        self._parent = None
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
        hints = typing.get_type_hints(self.__class__)
        for name in hints:
            if name not in kwargs:
                kwargs[name] = getattr(self, name)
        return self.__class__(**kwargs)

    def has_parent(self) -> bool:
        return self._parent is not None


class BaseNode(BaseSyntax):
    pass


class BaseToken(BaseSyntax):

    def __init__(self, span: Span | None = None) -> None:
        super().__init__()
        self.span = span

