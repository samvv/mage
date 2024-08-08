
from typing import Generic, Iterable, Iterator, TypeVar

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

_T = TypeVar('_T')
_P = TypeVar('_P')

class Punctuated(Generic[_T, _P]):

    def __init__(self, elements: Iterable[tuple[_T, _P | None]] | None = None) -> None:
        self.elements = []
        self.last = None
        if elements is not None:
          for element, sep  in elements:
              self.append(element, sep)

    def append(self, element: _T, separator: _P | None = None) -> None:
        if separator is None:
            assert(self.last is None)
            self.last = element
        else:
            self.elements.append((element, separator))

    def __iter__(self) -> Iterator[tuple[_T, _P | None]]:
        for item in self.elements:
            yield item
        if self.last is not None:
            yield self.last, None

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


