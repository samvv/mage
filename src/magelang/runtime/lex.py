
from abc import abstractmethod

from magelang.runtime.node import BaseToken
from magelang.runtime.stream import Stream

__all__ = [
    'EOF',
    'ScanError',
    'CharStream',
    'LineColumn',
    'AbstractLexer'
]


EOF = '\uFFFF'


class ScanError(RuntimeError):
    pass


class CharStream(Stream[str]):

    def __init__(self, buffer: str, offset: int = 0) -> None:
        super().__init__(buffer, EOF, offset)


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

    def skip(self) -> None:
        pass

    def set_location(self, other: 'AbstractLexer') -> None:
        self._curr_offset = other._curr_offset
        self._curr_pos = other._curr_pos

    def at_eof(self) -> bool:
        self.skip()
        return self._curr_offset >= len(self._text)

    @abstractmethod
    #def lex(self, mode: int) -> BaseToken:
    def lex(self) -> BaseToken:
        raise NotImplementedError()

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

