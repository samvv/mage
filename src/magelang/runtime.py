
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from collections.abc import Collection, Reversible, Sequence
from typing import Any, Iterable, Iterator, Protocol, SupportsIndex, TypeVar, assert_never, cast, overload

from magelang.util import DropProxy, MapProxy


EOF = '\uFFFF'


class TextPos:

    def __init__(self, offset: int, line: int, column: int) -> None:
        self.offset = offset
        self.line = line
        self.column = column


class Span:

    def __init__(self, start_offset: int, end_offset: int) -> None:
        self.start_offset = start_offset
        self.end_offset = end_offset

    def __len__(self) -> int:
        return self.end_offset - self.start_offset


class BaseSyntax:

    def __init__(self) -> None:
        self._parent = None

    def has_parent(self) -> bool:
        return self._parent is not None


class BaseNode(BaseSyntax):
    pass


class BaseToken(BaseSyntax):

    def __init__(self, span: Span | None = None) -> None:
        super().__init__()
        self.span = span


_Element_cov = TypeVar('_Element_cov', covariant=True)
_Separator_cov = TypeVar('_Separator_cov', covariant=True)

_T = TypeVar('_T')
_T_co = TypeVar('_T_co', covariant=True)
_R = TypeVar('_R')

class SequenceLike(Reversible[_T_co], Collection[_T_co], Protocol[_T_co]):
    @overload
    @abstractmethod
    def __getitem__(self, index: int, /) -> _T_co: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: slice, /) -> 'SequenceLike[_T_co]': ...
    @abstractmethod
    def __getitem__(self, index: int | slice) -> '_T_co | SequenceLike[_T_co]':
        raise NotImplementedError()
    # Mixin methods
    def index(self, value: Any, start: SupportsIndex = 0, stop: SupportsIndex = ..., /) -> int: ...
    def count(self, value: Any, /) -> int: ...
    def __contains__(self, value: object, /) -> bool: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def __reversed__(self) -> Iterator[_T_co]: ...


class ImmutablePunct(Reversible[tuple[_Element_cov, _Separator_cov | None]], Iterable[tuple[_Element_cov, _Separator_cov | None]], metaclass=ABCMeta):

    def __len__(self) -> int: ...

    def __contains__(self, value: object, /) -> bool: ...

    def __gt__(self, value: object, /) -> bool: ...

    def __ge__(self, value: object, /) -> bool: ...

    def __lt__(self, value: object, /) -> bool: ...

    def __le__(self, value: object, /) -> bool: ...

    def __reversed__(self) -> Iterator[tuple[_Element_cov, _Separator_cov | None]]: ...

    def __iter__(self) -> Iterator[tuple[_Element_cov, _Separator_cov | None]]: ...

    @property
    def elements(self) -> 'Sequence[_Element_cov]': ...

    @property
    def delimited(self) -> 'Sequence[tuple[_Element_cov, _Separator_cov]]': ...

    @property
    def last(self) -> '_Element_cov | None': ...


_Element = TypeVar('_Element')
_Separator = TypeVar('_Separator')

class Punctuated(ImmutablePunct[_Element, _Separator]):

    def __init__(self, value: Iterable[tuple[_Element, _Separator | None]] | None = None) -> None:
        super().__init__()
        self._storage = list(value) if value is not None else []

    def append(self, element: _Element, separator: _Separator) -> None:
        self._storage.append((element, separator))

    def append_final(self, element: _Element, separator: _Separator | None = None) -> None:
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

    def __reversed__(self) -> Iterator[tuple[_Element, _Separator | None]]:
        return reversed(self._storage)

    def __iter__(self) -> Iterator[tuple[_Element, _Separator | None]]:
        return iter(self._storage)

    def __getitem__(self, key: int | slice) -> tuple[_Element, _Separator | None] | list[tuple[_Element, _Separator | None]]:
        return self._storage[key]

    @property
    def elements(self) -> Sequence[_Element]:
        return MapProxy(self._storage, lambda pair: pair[0])

    @property
    def delimited(self) -> Sequence[tuple[_Element, _Separator]]:
        return DropProxy(cast(list[tuple[_Element, _Separator]], self._storage), 1) \
            if self and self.last_delimiter is None \
            else cast(list[tuple[_Element, _Separator]], self._storage)

    @property
    def last(self) -> _Element | None:
        return self._storage[-1][0] if self else None

    @property
    def last_delimiter(self) -> _Separator | None:
        return self._storage[-1][1] if self else None



ImmutablePunct.register(Punctuated) # type: ignore


class ScanError(RuntimeError):
    pass


class LineColumn:

    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column


class AbstractLexer:

    def __init__(self, text: str, start_offset = 0, start_line = 1, start_column = 1) -> None:
        self._text = text
        self._curr_offset = start_offset
        self._curr_pos = LineColumn(start_line, start_column)

    def _char_at(self, offset: int) -> str:
        return self._text[offset] if offset < len(self._text) else EOF

    def _peek_char(self, offset = 0) -> str:
        k = self._curr_offset + offset
        return self._text[k] if k < len(self._text) else EOF

    def at_eof(self) -> bool:
        return self._curr_offset >= len(self._text)

    def _get_char(self) -> str:
        if self._curr_offset >= len(self._text):
            return EOF
        ch = self._text[self._curr_offset]
        self._curr_offset += 1
        if ch == '\n':
            self._curr_pos.line += 1
            self._curr_pos.column = 1
        else:
            self._curr_pos.column += 1
        return ch

## -- Designed for the emitter

type Doc = ConsDoc | EmptyDoc | TextDoc

@dataclass
class DocBase:
    pass

@dataclass
class ConsDoc(DocBase):
    head: Doc
    tail: Doc


@dataclass
class EmptyDoc(DocBase):
    pass


@dataclass
class TextDoc(DocBase):
    text: str


def empty() -> Doc:
    return EmptyDoc()


def seq(elements: Sequence[Doc]) -> Doc:
    out = EmptyDoc()
    for element in reversed(elements):
        out = ConsDoc(element, out)
    return out

def text(contents: str) -> TextDoc:
    return TextDoc(contents)

def generate(doc: Doc) -> str:
    if isinstance(doc, EmptyDoc):
        return ''
    if isinstance(doc, ConsDoc):
        return generate(doc.head) + generate(doc.tail)
    if isinstance(doc, TextDoc):
        return doc.text
    assert_never(doc)
