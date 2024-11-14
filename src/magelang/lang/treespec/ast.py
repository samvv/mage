

from collections.abc import Sequence
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, TypedDict, Unpack

from magelang.util import panic

type Type = ExternType | SpecType | NeverType | TupleType | ListType | PunctType | UnionType | NoneType | AnyType

def _is_copy(value: Any) -> bool:
    """
    Returns `True` whenever `value` is cloned whenever passed to a function parameter.

    In practice, this will be `True` for some of the built-in Python types.
    """
    return value is None \
        or isinstance(value, bool) \
        or isinstance(value, int) \
        or isinstance(value, float) \
        or isinstance(value, str)

def _clone_field(value: Any) -> Any:
    if _is_copy(value):
        return value
    if isinstance(value, list):
        return list(_clone_field(element) for element in value)
    if isinstance(value, tuple):
        return tuple(_clone_field(element) for element in value)
    if isinstance(value, NodeBase):
        return value
    panic(f"Unexepcted {value}")

def _derive(obj, kwargs):
    new_kwargs = {}
    for name, _ in obj.__dict__.items():
        if not name.startswith('_'):
            new_kwargs[name] = kwargs[name] if name in kwargs else _clone_field(getattr(obj, name))
    return obj.__class__(**new_kwargs)

class NodeBase:
    pass

class TypeBase(NodeBase):

    @abstractmethod
    def encode(self) -> Any: ...

    def __lt__(self, value: object, /) -> bool:
        return isinstance(value, TypeBase) and self.encode() < value.encode()

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, TypeBase) and self.encode() == value.encode()

    def __hash__(self) -> int:
        return hash(self.encode())

class SpecType(TypeBase):
    """
    Matches any declaration in the current program.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def encode(self) -> Any:
        return (1, self.name)

    def __repr__(self) -> str:
        return f'SpecType({self.name})'

class NeverType(TypeBase):
    """
    Represents a type that never matches. Mostly useful to close off a union type when generating types.
    """

    def encode(self) -> Any:
        return (4,)

    def __repr__(self) -> str:
        return 'NeverType()'

class TupleTypeDeriveKwargs(TypedDict, total=False):
    element_types: list[Type]

class TupleType(TypeBase):
    """
    A type that allows values to contain a specific sequence of types.
    """

    def __init__(self, element_types: list[Type]) -> None:
        super().__init__()
        self.element_types = element_types

    def derive(self, **kwargs: Unpack[TupleTypeDeriveKwargs]) -> 'TupleType':
       return _derive(self, kwargs)

    def encode(self) -> Any:
        return (5, tuple(ty.encode() for ty in self.element_types))

    def __repr__(self) -> str:
        return f"TupleType({', '.join(repr(ty) for ty in self.element_types)})"

class ListTypeDeriveKwargs(TypedDict, total=False):
    element_type: Type
    required: bool

class ListType(TypeBase):
    """
    A type that allows multiple values of the same underlying type.
    """

    def __init__(self, element_type: Type, required: bool) -> None:
        super().__init__()
        self.element_type = element_type
        self.required = required

    def derive(self, **kwargs: Unpack[ListTypeDeriveKwargs]) -> 'ListType':
        return _derive(self, kwargs)

    def encode(self) -> Any:
        return (6, self.element_type.encode(), self.required)

    def __repr__(self) -> str:
        return f'ListType({repr(self.element_type)})'

class PunctTypeDeriveKwargs(TypedDict, total=False):
    element_type: Type
    separator_type: Type
    required: bool

class PunctType(TypeBase):
    """
    A type that is like a list but where values are seperated by another type.
    """

    def __init__(
        self,
        element_type: Type,
        separator_type: Type,
        required: bool,
    ) -> None:
        super().__init__()
        self.element_type = element_type
        self.separator_type = separator_type
        self.required = required

    def derive(self, **kwargs: Unpack[PunctTypeDeriveKwargs]) -> 'PunctType':
        return _derive(self, kwargs)

    def encode(self) -> Any:
        return (7, self.element_type.encode(), self.separator_type.encode(), self.required)

    def __repr__(self) -> str:
        return f'PunctType({repr(self.element_type)}, {repr(self.separator_type)})'

class UnionTypeDeriveKwargs(TypedDict, total=False):
    types: Sequence[Type]

class UnionType(TypeBase):
    """
    A type where any of the member types are valid.
    """

    def __init__(self, types: list[Type]) -> None:
        super().__init__()
        self.types = types

    def derive(self, **kwargs: Unpack[UnionTypeDeriveKwargs]) -> 'UnionType':
        return _derive(self, kwargs)

    def encode(self) -> Any:
        return (8, tuple(ty.encode() for ty in self.types))

    def __repr__(self) -> str:
        return f"UnionType({', '.join(repr(ty) for ty in self.types)})"

class NoneType(TypeBase):
    """
    A type that indicates that the value is empty.

    This type is usually created in conjunction with a union type.
    """

    def encode(self) -> Any:
        return (9,)

    def __repr__(self) -> str:
        return 'NoneType()'

class ExternType(TypeBase):
    """
    A type that is directly representing the Foo part in a `pub foo -> Foo = bar` 
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def encode(self) -> Any:
        return (10, self.name)

    def __repr__(self) -> str:
        return f'ExternType({self.name})'

class AnyType(TypeBase):
    """
    A type that is used as a placeholder when no more specific type is known.
    """

    def encode(self) -> Any:
        return (11,)

    def __repr__(self) -> str:
        return 'AnyType()'

def rewrite_each_child_type(ty: Type, proc: Callable[[Type], Type]) -> Type:
    if isinstance(ty, NoneType) \
        or isinstance(ty, AnyType) \
        or isinstance(ty, NeverType) \
        or isinstance(ty, SpecType) \
        or isinstance(ty, ExternType):
        return ty
    if isinstance(ty, ListType):
        new_element_type = proc(ty.element_type)
        if new_element_type is ty.element_type:
            return ty
        return ty.derive(element_type=new_element_type)
    if isinstance(ty, PunctType):
        new_element_type = proc(ty.element_type)
        new_separator_type = proc(ty.separator_type)
        if new_element_type is ty.element_type and new_separator_type is ty.separator_type:
            return ty
        return ty.derive(element_type=new_element_type, separator_type=new_separator_type)
    if isinstance(ty, TupleType):
        new_types = list[Type]()
        changed = False
        for ty_2 in ty.element_types:
            new_ty_2 = proc(ty_2)
            if new_ty_2 is not ty_2:
                changed = True
            new_types.append(new_ty_2)
        if not changed:
            return ty
        return ty.derive(element_types=new_types)
    if isinstance(ty, UnionType):
        new_types = list[Type]()
        changed = False
        for ty_2 in ty.types:
            new_ty_2 = proc(ty_2)
            if new_ty_2 is not ty_2:
                changed = True
            new_types.append(new_ty_2)
        if not changed:
            return ty
        return ty.derive(types=new_types)
    assert_never(ty)


@dataclass
class Field:
    name: str
    ty: Type

@dataclass
class Variant:
    name: str
    ty: Type

@dataclass
class SpecBase:
    name: str

@dataclass
class TokenSpec(SpecBase):
    field_type: str
    is_static: bool

@dataclass
class TypeSpec(SpecBase):
    ty: Type

@dataclass
class NodeSpec(SpecBase):
    name: str
    fields: list[Field]

@dataclass
class EnumSpec(SpecBase):
    members: list[Variant]

@dataclass
class ConstEnumSpec(SpecBase):
    members: list[tuple[str, int]]

Spec = TokenSpec | NodeSpec | EnumSpec | ConstEnumSpec | TypeSpec

class Specs:

    def __init__(self, elements: Sequence[Spec]) -> None:
        self.elements = elements

