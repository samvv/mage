
from typing import Callable, TypeVar, overload


def to_camel_case(snake_str: str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def to_lower_camel_case(snake_str):
    camel_string = to_camel_case(snake_str)
    return snake_str[0].lower() + camel_string[1:]

T = TypeVar('T')

def nonnull(value: T | None) -> T:
    assert(value is not None)
    return value

class NameGenerator:

    def __init__(self, default_prefix = 'tmp_') -> None:
        self._mapping: dict[str, int] = {}
        self._default_prefix = default_prefix

    def __call__(self, prefix: str | None = None) -> str:
        if prefix is None:
            prefix = self._default_prefix
        count = self._mapping.get(prefix, 0)
        name = prefix + str(count)
        self._mapping[prefix] = count + 1
        return name

    def reset(self) -> None:
        self._mapping = {}


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

