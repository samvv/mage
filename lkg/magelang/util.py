
import io
from typing import Any, Callable, Generic, Iterator, Never, Protocol, Sequence, SupportsIndex, TextIO, TypeGuard, TypeIs, TypeVar, overload
import re


def plural(name: str) -> str:
    return name if name.endswith('s') else f'{name}s'


type Files = dict[str, str]


def is_iterator(value: Any) -> TypeGuard[Iterator[Any]]:
    return hasattr(value, '__next__') \
        and callable(getattr(value, '__next__'))


def to_camel_case(snake_str: str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def to_lower_camel_case(snake_str):
    camel_string = to_camel_case(snake_str)
    return snake_str[0].lower() + camel_string[1:]


def to_snake_case(name: str) -> str:
    if '-' in name:
        return name.replace('-', '_')
    else:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def todo() -> Never:
    raise NotImplementedError(f'This functionality has yet to be implemented.')


def panic(message: str) -> Never:
    raise RuntimeError(message)


def unreachable() -> Never:
    panic(f'Some code was executed that was not meant to be executed. This is a bug.')


_T = TypeVar('_T')
_R = TypeVar('_R')

class Nothing:
    """
    An alternative to `None` that can be used in cases where `None` is already
    semantically taken.
    """
    pass

class Something(Generic[_T]):

    def __init__(self, value: _T) -> None:
        super().__init__()
        self.value = value

    def to_maybe_none(self) -> _T | None:
        return self.value

type Option[_T] = Something[_T] | Nothing

def is_nothing(opt: Option[Any]) -> TypeIs[Nothing]:
    return isinstance(opt, Nothing)

def is_something(opt: Option[Any]) -> TypeIs[Something]:
    return isinstance(opt, Something)

def to_maybe_none(value: Option[_T]) -> _T | None:
    return value.value if isinstance(value, Something) else None

def nonnull(value: _T | None) -> _T:
    assert(value is not None)
    return value

class Eq(Protocol):
    def __eq__(self, value: object, /) -> bool: ...

class MiniSeq(Protocol[_T]):
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, i: SupportsIndex, /) -> _T: ...
    @overload
    def __getitem__(self, s: slice, /) -> list[_T]: ...

_K = TypeVar('_K', bound=Eq)

def get_common_suffix(names: Sequence[MiniSeq[_K]]) -> MiniSeq[_K]:
    i = 0
    name = names[0]
    while True:
        k = len(name) - i - 1
        if k < 0:
            break
        ch = name[k]
        match = True
        for name_2 in names[1:]:
            k = len(name_2) - i - 1
            if k < 0:
                match = False
                break
            if ch != name_2[k]:
                match = False
                break
        if not match:
            break
        i += 1
    return name[len(name) - i:]

class IndentWriter:

    def __init__(self, out: TextIO | None = None, indentation='  '):
        if out is None:
            out = io.StringIO()
        self.output = out
        self.at_blank_line = True
        self.newline_count = 0
        self.indent_level = 0
        self.indentation = indentation
        self._re_whitespace = re.compile('[\n\r\t ]')

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1

    def ensure_trailing_lines(self, count):
        self.write('\n' * max(0, count - self.newline_count))

    def write(self, text: str) -> None:
        for ch in text:
            if ch == '\n':
                self.newline_count = self.newline_count + 1 if self.at_blank_line else 1
                self.at_blank_line = True
            elif self.at_blank_line and not self._re_whitespace.match(ch):
                self.newline_count = 0
                self.output.write(self.indentation * self.indent_level)
                self.at_blank_line = False
            self.output.write(ch)


class NameGenerator:

    def __init__(self, namespace: str | None = None, default_prefix: str | None= 'tmp') -> None:
        self._counts: dict[str, int] = {}
        self.namespace = namespace
        self._default_prefix = default_prefix

    def __call__(self, prefix: str | None = None, hide: bool = False) -> str:
        if prefix is None:
            prefix = self._default_prefix
        name = ''
        if hide:
            name += '_'
        if self.namespace is not None:
            if name and not name.endswith('_'):
                name += '_'
            name += self.namespace
        if prefix is not None:
            if name and not name.endswith('_'):
                name += '_'
            name += prefix
        assert(len(name) > 0)
        count = self._counts.get(name, 0)
        self._counts[name] = count + 1
        if count > 0:
            name += '_' + str(count)
        return name

    def reset(self) -> None:
        self._counts = {}

# Proxies for sequences

class MapProxy(Sequence[_R], Generic[_T, _R]):

    def __init__(self, elements: Sequence[_T], proc: Callable[[_T], _R]) -> None:
        super().__init__()
        self._elements = elements
        self._proc = proc

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self) -> Iterator[_R]:
        for element in self._elements:
            yield self._proc(element)

    def __reversed__(self) -> Iterator[_R]:
        for element in reversed(self._elements):
            yield self._proc(element)

    @overload
    def __getitem__(self, key: int) -> _R: ...

    @overload
    def __getitem__(self, key: slice) -> Sequence[_R]: ...

    def __getitem__(self, key: int | slice) -> _R | Sequence[_R]:
        if isinstance(key, slice):
            return list(self._proc(element) for element in self._elements[key])
        else:
            return self._proc(self._elements[key])

class DropProxy(Sequence[_T]):

    def __init__(self, elements: 'Sequence[_T]', count: int) -> None:
        assert(count <= len(elements))
        self._elements = elements
        self._to_drop = count

    def __len__(self) -> int:
        return len(self._elements)-self._to_drop

    def __iter__(self) -> Iterator[_T]:
        n = len(self._elements)
        for i in range(0, n-self._to_drop):
            yield self._elements[i]

    def __reversed__(self) -> Iterator[_T]:
        n = len(self._elements)
        for i in range(0, n-self._to_drop):
            yield self._elements[n-i-1]

    @overload
    def __getitem__(self, key: int) -> _T: ...

    @overload
    def __getitem__(self, key: slice) -> Sequence[_T]: ...

    def __getitem__(self, key: int | slice) -> _T | Sequence[_T]:
        max_index = len(self._elements)-self._to_drop
        if isinstance(key, slice):
            start = min(key.start, max_index)
            stop = min(key.stop, max_index)
            return self._elements[start:stop]
        else:
            if key >= max_index:
                raise IndexError(f'index {key} out of bounds')
            return self._elements[key]


