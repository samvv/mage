
import io
from typing import Any, Callable, Generic, Iterator, Never, Protocol, Sequence, SupportsIndex, TextIO, TypeGuard, TypeVar, overload
import re


def plural(name: str) -> str:
    return name if name.endswith('s') else f'{name}s'


type Files = list[tuple[str, str]]


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

def unreachable() -> Never:
    raise RuntimeError(f'Some code was executed that was not meant to be executed. This is a bug.')


_T = TypeVar('_T')


def nonnull(value: _T | None) -> _T:
    assert(value is not None)
    return value

class Eq(Protocol):
    def __eq__(self, value: object, /) -> bool: ...

_Elem = TypeVar('_Elem')

class Seq(Generic[_Elem], Protocol):
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, i: SupportsIndex, /) -> _Elem: ...
    @overload
    def __getitem__(self, s: slice, /) -> list[_Elem]: ...

_K = TypeVar('_K', bound=Eq)

def get_common_suffix(names: Sequence[Seq[_K]]) -> Seq[_K]:
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


_T0 = TypeVar('_T0')
_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')
_T3 = TypeVar('_T3')
_T4 = TypeVar('_T4')
_T5 = TypeVar('_T5')
_T6 = TypeVar('_T6')
_T7 = TypeVar('_T7')
_T8 = TypeVar('_T8')
_T9 = TypeVar('_T9')
_T10 = TypeVar('_T10')
_T11 = TypeVar('_T11')
_T12 = TypeVar('_T12')
_T13 = TypeVar('_T13')
_T14 = TypeVar('_T14')
_T15 = TypeVar('_T15')
_T16 = TypeVar('_T16')
_T17 = TypeVar('_T17')
_T18 = TypeVar('_T18')
_T19 = TypeVar('_T19')
_T20 = TypeVar('_T20')
_T21 = TypeVar('_T21')
_T22 = TypeVar('_T22')
_T23 = TypeVar('_T23')
_T24 = TypeVar('_T24')

@overload
def pipe(arg0: _T0, /) -> _T0: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], /) -> _T1: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], /) -> _T2: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], /) -> _T3: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], /) -> _T4: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], /) -> _T5: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], /) -> _T6: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], /) -> _T7: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], /) -> _T8: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], /) -> _T9: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], /) -> _T10: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], /) -> _T11: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], /) -> _T12: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], /) -> _T13: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], /) -> _T14: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], /) -> _T15: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], /) -> _T16: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], /) -> _T17: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], f17: Callable[[_T17], _T18], /) -> _T18: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], f17: Callable[[_T17], _T18], f18: Callable[[_T18], _T19], /) -> _T19: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], f17: Callable[[_T17], _T18], f18: Callable[[_T18], _T19], f19: Callable[[_T19], _T20], /) -> _T20: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], f17: Callable[[_T17], _T18], f18: Callable[[_T18], _T19], f19: Callable[[_T19], _T20], f20: Callable[[_T20], _T21], /) -> _T21: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], f17: Callable[[_T17], _T18], f18: Callable[[_T18], _T19], f19: Callable[[_T19], _T20], f20: Callable[[_T20], _T21], f21: Callable[[_T21], _T22], /) -> _T22: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], f17: Callable[[_T17], _T18], f18: Callable[[_T18], _T19], f19: Callable[[_T19], _T20], f20: Callable[[_T20], _T21], f21: Callable[[_T21], _T22], f22: Callable[[_T22], _T23], /) -> _T23: ...

@overload
def pipe(arg0: _T0, f0: Callable[[_T0], _T1], f1: Callable[[_T1], _T2], f2: Callable[[_T2], _T3], f3: Callable[[_T3], _T4], f4: Callable[[_T4], _T5], f5: Callable[[_T5], _T6], f6: Callable[[_T6], _T7], f7: Callable[[_T7], _T8], f8: Callable[[_T8], _T9], f9: Callable[[_T9], _T10], f10: Callable[[_T10], _T11], f11: Callable[[_T11], _T12], f12: Callable[[_T12], _T13], f13: Callable[[_T13], _T14], f14: Callable[[_T14], _T15], f15: Callable[[_T15], _T16], f16: Callable[[_T16], _T17], f17: Callable[[_T17], _T18], f18: Callable[[_T18], _T19], f19: Callable[[_T19], _T20], f20: Callable[[_T20], _T21], f21: Callable[[_T21], _T22], f22: Callable[[_T22], _T23], f23: Callable[[_T23], _T24], /) -> _T24: ...

def pipe(arg0, *fs):
    result = arg0
    for f in fs:
        result = f(result)
    return result

