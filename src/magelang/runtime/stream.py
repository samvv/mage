
from collections.abc import Sequence
from typing import Self, cast


class Stream[T]:

    def __init__(self, buffer: Sequence[T], sentry: T, offset: int = 0, ) -> None:
        self._offset = offset
        self._buffer = buffer
        self.sentry = sentry
        # self._buffers = list(deque() for _ in range(0, num_modes))

    def peek(self, offset = 0) -> T:
        i = self._offset + offset
        return self._buffer[i] if i < len(self._buffer) else self.sentry

    def get(self) -> T:
        i = self._offset
        if i == len(self._buffer):
            return self.sentry
        self._offset += 1
        return self._buffer[i]

    def fork(self) -> Self:
        # Ugly hack to ensure derived classes fork to their derived class
        return cast(Self, Stream(self._buffer, self.sentry, self._offset))

    # def _peek(self, mode: int, offset = 0) -> BaseToken:
    #     buffer = self._buffers[mode]
    #     while len(buffer) <= offset:
    #         buffer.append(self._lexer.lex(mode))
    #     return buffer[offset]

    # def _get(self, mode: int) -> BaseToken:
    #     buffer = self._buffers[mode]
    #     token = buffer.popleft() if buffer else self._lexer.lex(mode)
    #     for k in range(0, self._num_modes):
    #         if k != mode:
    #             self._buffers[k].clear()
    #     return token

    def join_to(self, other: 'Stream[T]') -> None:
        self._offset = other._offset

    def at_eof(self) -> bool:
        return self._offset == len(self._buffer)

