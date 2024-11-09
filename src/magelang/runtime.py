
from abc import abstractmethod
from dataclasses import dataclass
from collections.abc import Collection, Reversible, Sequence
import sys
from typing import Any, Iterable, Iterator, Protocol, SupportsIndex, TypeVar, assert_never, overload


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

_T_co = TypeVar('_T_co', covariant=True)

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

class ImmutableList(SequenceLike[_T_co]):
    pass

ImmutableList.register(list) # type: ignore

_T = TypeVar('_T')

class List(ImmutableList[_T]):

    def __init__(self, value: 'Iterable[_T] | None' = None) -> None:
        """
        Create a new `List` from either another List or any iterable
        producing values that will be stored in this list.
        """
        super().__init__()
        self._storage = list(value) if value is not None else []

    def __len__(self) -> int:
        return len(self._storage)

    def __contains__(self, value: object) -> bool:
        return value in self._storage

    def __gt__(self, value: object, /) -> bool:
        if not isinstance(value, List):
            raise TypeError()
        return self._storage > value._storage

    def __ge__(self, value: object, /) -> bool:
        if not isinstance(value, List):
            raise TypeError()
        return self._storage >= value._storage

    def __lt__(self, value: object, /) -> bool:
        if not isinstance(value, List):
            raise TypeError()
        return self._storage < value._storage

    def __le__(self, value: object, /) -> bool:
        if not isinstance(value, List):
            raise TypeError()
        return self._storage <= value._storage

    def __reversed__(self) -> Iterator[_T]:
        return reversed(self._storage)

    def prepend(self, value: _T, /) -> None:
        self._storage.insert(0, value)

    def append(self, value: _T, /) -> None:
        self._storage.append(value)

    def insert(self, index: SupportsIndex, value: _T, /) -> None:
        self._storage.insert(index, value)

    def index(self, value: _T, start: SupportsIndex = 0, stop: SupportsIndex = sys.maxsize, /) -> int:
        return self._storage.index(value, start, stop)

    def count(self, value: _T, /) -> int:
        return self._storage.count(value)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._storage)

    @overload
    def __getitem__(self, index: int) -> '_T': ...

    @overload
    def __getitem__(self, index: slice) -> 'List[_T]': ...

    def __getitem__(self, index: int | slice) -> '_T | List[_T]':
        return List(self._storage[index]) \
            if isinstance(index, slice) \
            else self._storage[index]

class ImmutablePunct(SequenceLike[tuple[_Element_cov, _Separator_cov | None]]):

    @property
    def elements(self) -> Iterable[_Element_cov]: ...

    @property
    def separators(self) -> Iterable[_Separator_cov | None]: ...

_Element = TypeVar('_Element')
_Separator = TypeVar('_Separator')

class Punctuated(ImmutablePunct[_Element, _Separator], List[tuple[_Element, _Separator | None]]):

    def push(self, element: _Element, separator: _Separator | None = None) -> None: # FIXME
        super().append((element, separator))

    def push_final(self, element: _Element, separator: _Separator | None = None) -> None:
        super().append((element, separator))

    @property
    def last(self) -> _Separator | None:
        return self[-1][1] if self else None

    @property
    def separators(self) -> Iterable[_Separator | None]:
        for _, sep in self:
            yield sep

    @property
    def elements(self) -> Iterable[_Element]:
        for element, _ in self:
            yield element


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
