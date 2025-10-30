
from abc import ABCMeta, abstractmethod
from collections.abc import Collection, Iterable, Iterator, Reversible, Sequence
from typing import Any, Protocol, SupportsIndex, TypeVar, cast, overload

# TODO move this into the runtime
from magelang.util import DropProxy, MapProxy

__all__ = [
    'SequenceLike',
    'ImmutablePunct',
    'Punctuated',
]


class SequenceLike[T](Reversible[T], Collection[T], Protocol):
    @overload
    @abstractmethod
    def __getitem__(self, index: int, /) -> T: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: slice, /) -> 'SequenceLike[T]': ...
    @abstractmethod
    def __getitem__(self, index: int | slice) -> 'T | SequenceLike[T]':
        raise NotImplementedError()
    # Mixin methods
    def index(self, value: Any, start: SupportsIndex = 0, stop: SupportsIndex = ..., /) -> int: ...
    def count(self, value: Any, /) -> int: ...
    def __contains__(self, value: object, /) -> bool: ...
    def __iter__(self) -> Iterator[T]: ...
    def __reversed__(self) -> Iterator[T]: ...


class ImmutablePunct[El, Sep](Reversible[tuple[El, Sep | None]], Iterable[tuple[El, Sep | None]], metaclass=ABCMeta):

    def __len__(self) -> int: ...

    def __contains__(self, value: object, /) -> bool: ...

    def __gt__(self, value: object, /) -> bool: ...

    def __ge__(self, value: object, /) -> bool: ...

    def __lt__(self, value: object, /) -> bool: ...

    def __le__(self, value: object, /) -> bool: ...

    def __reversed__(self) -> Iterator[tuple[El, Sep | None]]: ...

    def __iter__(self) -> Iterator[tuple[El, Sep | None]]: ...

    @property
    def elements(self) -> 'Sequence[El]': ...

    @property
    def delimited(self) -> 'Sequence[tuple[El, Sep]]': ...

    @property
    def last(self) -> 'El | None': ...


class Punctuated[El, Sep](ImmutablePunct[El, Sep]):

    def __init__(self, value: Iterable[tuple[El, Sep | None]] | None = None) -> None:
        super().__init__()
        self._storage = list(value) if value is not None else []

    def append(self, element: El, separator: Sep) -> None:
        self._storage.append((element, separator))

    def append_final(self, element: El, separator: Sep | None = None) -> None:
        self._storage.append((element, separator))

    def __len__(self) -> int:
        return len(self._storage)

    def __contains__(self, value: object) -> bool:
        return value in self._storage

    def __gt__(self, value: object, /) -> bool:
        if not isinstance(value, Punctuated):
            raise TypeError()
        return self._storage > value._storage

    def __ge__(self, value: object, /) -> bool:
        if not isinstance(value, Punctuated):
            raise TypeError()
        return self._storage >= value._storage

    def __lt__(self, value: object, /) -> bool:
        if not isinstance(value, Punctuated):
            raise TypeError()
        return self._storage < value._storage

    def __le__(self, value: object, /) -> bool:
        if not isinstance(value, Punctuated):
            raise TypeError()
        return self._storage <= value._storage

    def __reversed__(self) -> Iterator[tuple[El, Sep | None]]:
        return reversed(self._storage)

    def __iter__(self) -> Iterator[tuple[El, Sep | None]]:
        return iter(self._storage)

    def __getitem__(self, key: int | slice) -> tuple[El, Sep | None] | list[tuple[El, Sep | None]]:
        return self._storage[key]

    @property
    def elements(self) -> Sequence[El]:
        return MapProxy(self._storage, lambda pair: pair[0])

    @property
    def delimited(self) -> Sequence[tuple[El, Sep]]:
        return DropProxy(cast(list[tuple[El, Sep]], self._storage), 1) \
            if self and self.last_delimiter is None \
            else cast(list[tuple[El, Sep]], self._storage)

    @property
    def last(self) -> El | None:
        return self._storage[-1][0] if self else None

    @property
    def last_delimiter(self) -> Sep | None:
        return self._storage[-1][1] if self else None


ImmutablePunct.register(Punctuated) # type: ignore

