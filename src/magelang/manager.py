
import inspect
from abc import abstractmethod
from typing import Any, Callable, Protocol, TypeVar, get_type_hints, no_type_check, overload

from sortedcontainers.sortedlist import Sequence

from magelang.util import Seq

_X = TypeVar('_X', contravariant=True)
_Y = TypeVar('_Y', covariant=True)

class Pass(Protocol[_X, _Y]):

    @abstractmethod
    def __call__(self, input: _X, /, *args, **kwargs) -> _Y: ...

class Context:

    def __init__(self, opts: dict[str, Any]) -> None:
        self.opts = opts

    def get_option(self, name: str) -> Any:
        return self.opts[name]

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
def apply(ctx: Context, input: _T0, /) -> _T0: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], /) -> _T1: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], /) -> _T2: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], /) -> _T3: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], /) -> _T4: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], /) -> _T5: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], /) -> _T6: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], /) -> _T7: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], /) -> _T8: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], /) -> _T9: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], /) -> _T10: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], /) -> _T11: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], /) -> _T12: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], /) -> _T13: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], /) -> _T14: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], /) -> _T15: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], /) -> _T16: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], /) -> _T17: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], f17: Pass[_T17, _T18], /) -> _T18: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], f17: Pass[_T17, _T18], f18: Pass[_T18, _T19], /) -> _T19: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], f17: Pass[_T17, _T18], f18: Pass[_T18, _T19], f19: Pass[_T19, _T20], /) -> _T20: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], f17: Pass[_T17, _T18], f18: Pass[_T18, _T19], f19: Pass[_T19, _T20], f20: Pass[_T20, _T21], /) -> _T21: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], f17: Pass[_T17, _T18], f18: Pass[_T18, _T19], f19: Pass[_T19, _T20], f20: Pass[_T20, _T21], f21: Pass[_T21, _T22], /) -> _T22: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], f17: Pass[_T17, _T18], f18: Pass[_T18, _T19], f19: Pass[_T19, _T20], f20: Pass[_T20, _T21], f21: Pass[_T21, _T22], f22: Pass[_T22, _T23], /) -> _T23: ...

@overload
def apply(ctx: Context, input: _T0, f0: Pass[_T0, _T1], f1: Pass[_T1, _T2], f2: Pass[_T2, _T3], f3: Pass[_T3, _T4], f4: Pass[_T4, _T5], f5: Pass[_T5, _T6], f6: Pass[_T6, _T7], f7: Pass[_T7, _T8], f8: Pass[_T8, _T9], f9: Pass[_T9, _T10], f10: Pass[_T10, _T11], f11: Pass[_T11, _T12], f12: Pass[_T12, _T13], f13: Pass[_T13, _T14], f14: Pass[_T14, _T15], f15: Pass[_T15, _T16], f16: Pass[_T16, _T17], f17: Pass[_T17, _T18], f18: Pass[_T18, _T19], f19: Pass[_T19, _T20], f20: Pass[_T20, _T21], f21: Pass[_T21, _T22], f22: Pass[_T22, _T23], f23: Pass[_T23, _T24], /) -> _T24: ...

@no_type_check
def apply(ctx, input, *passes):
    output = input
    for pass_ in passes:
        output = apply_1(ctx, output, pass_)
    return output

_K = TypeVar('_K')
_K1 = TypeVar('_K1')
_K2 = TypeVar('_K2')
_T = TypeVar('_T')
_R = TypeVar('_R')

def apply_1(ctx: Context, input: _T, pass_: Pass[_T, _R]) -> _R:
    args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(pass_)
    assert(varargs is None)
    out_args = []
    for arg in args[1:]:
        if arg in annotations:
            ty = annotations[arg]
            if ty is Context:
                out_args.append(ctx)
    out_kwargs = {}
    return pass_(input, *out_args, **out_kwargs)

def distribute(map: dict[_K, Pass[_T, _R]]) -> Pass[_T, dict[_K, _R]]:

    def wrapper(input: _T, ctx: Context) -> dict[_K, _R]:
        out = dict[_K, _R]()
        for key, value in map.items():
            out[key] = apply(ctx, input, value)
        return out

    return wrapper

def each_value(pass_: Pass[_T, _R]) -> Pass[dict[_K, _T], dict[_K, _R]]:

    def wrapper(input: dict[_K, _T], ctx: Context) -> dict[_K, _R]:
        out = dict[_K, _R]()
        for key, value in input.items():
            out[key] = apply(ctx, value, pass_)
        return out

    return wrapper

def map_key(proc: Callable[[_K1], _K2]) -> Pass[dict[_K1, _T], dict[_K2, _T]]:

    def wrapper(input: dict[_K1, _T]) -> dict[_K2, _T]:
        out = dict[_K2, _T]()
        for key, value in input.items():
            out[proc(key)] = value
        return out

    return wrapper

def many(passes: Sequence[Pass]) -> Pass:
    def wrapper(input, ctx: Context) -> Any:
        return apply(ctx, input, *passes)
    return wrapper


