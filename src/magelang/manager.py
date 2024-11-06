
import inspect
from abc import abstractmethod
from typing import Any, Callable, Protocol, TypeVar, overload

from magelang.util import panic

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

_K = TypeVar('_K')
_K1 = TypeVar('_K1')
_K2 = TypeVar('_K2')
_T = TypeVar('_T')
_R = TypeVar('_R')
_S = TypeVar('_S')

def apply(ctx: Context, input: _T, pass_: Pass[_T, _R]) -> _R:
    def get_injectable(ty) -> Any:
        if ty is Context:
            return ctx
        else:
            panic("Trying to inject an unknown type")
    args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(pass_)
    assert(varargs is None)
    assert(varkw is None)
    out_args = []
    for arg in args[1:]:
        if arg in annotations:
            ty = annotations[arg]
            out_args.append(get_injectable(ty))
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

def compose(a: Pass[_T, _R], b: Pass[_R, _S]) -> Pass[_T, _S]:
    def wrapper(input: _T, ctx: Context) -> _S:
        return apply(ctx, apply(ctx, input, a), b)
    return wrapper

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
def pipeline(p0: Pass[_T0, _T1], /) -> Pass[_T0, _T1]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], /) -> Pass[_T0, _T2]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], /) -> Pass[_T0, _T3]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], /) -> Pass[_T0, _T4]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], /) -> Pass[_T0, _T5]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], /) -> Pass[_T0, _T6]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], /) -> Pass[_T0, _T7]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], /) -> Pass[_T0, _T8]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], /) -> Pass[_T0, _T9]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], /) -> Pass[_T0, _T10]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], /) -> Pass[_T0, _T11]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], /) -> Pass[_T0, _T12]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], /) -> Pass[_T0, _T13]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], /) -> Pass[_T0, _T14]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], /) -> Pass[_T0, _T15]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], /) -> Pass[_T0, _T16]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], /) -> Pass[_T0, _T17]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], p17: Pass[_T17, _T18], /) -> Pass[_T0, _T18]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], p17: Pass[_T17, _T18], p18: Pass[_T18, _T19], /) -> Pass[_T0, _T19]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], p17: Pass[_T17, _T18], p18: Pass[_T18, _T19], p19: Pass[_T19, _T20], /) -> Pass[_T0, _T20]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], p17: Pass[_T17, _T18], p18: Pass[_T18, _T19], p19: Pass[_T19, _T20], p20: Pass[_T20, _T21], /) -> Pass[_T0, _T21]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], p17: Pass[_T17, _T18], p18: Pass[_T18, _T19], p19: Pass[_T19, _T20], p20: Pass[_T20, _T21], p21: Pass[_T21, _T22], /) -> Pass[_T0, _T22]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], p17: Pass[_T17, _T18], p18: Pass[_T18, _T19], p19: Pass[_T19, _T20], p20: Pass[_T20, _T21], p21: Pass[_T21, _T22], p22: Pass[_T22, _T23], /) -> Pass[_T0, _T23]: ...

@overload
def pipeline(p0: Pass[_T0, _T1], p1: Pass[_T1, _T2], p2: Pass[_T2, _T3], p3: Pass[_T3, _T4], p4: Pass[_T4, _T5], p5: Pass[_T5, _T6], p6: Pass[_T6, _T7], p7: Pass[_T7, _T8], p8: Pass[_T8, _T9], p9: Pass[_T9, _T10], p10: Pass[_T10, _T11], p11: Pass[_T11, _T12], p12: Pass[_T12, _T13], p13: Pass[_T13, _T14], p14: Pass[_T14, _T15], p15: Pass[_T15, _T16], p16: Pass[_T16, _T17], p17: Pass[_T17, _T18], p18: Pass[_T18, _T19], p19: Pass[_T19, _T20], p20: Pass[_T20, _T21], p21: Pass[_T21, _T22], p22: Pass[_T22, _T23], p23: Pass[_T23, _T24], /) -> Pass[_T0, _T24]: ...

def pipeline(first: Pass, *passes: Pass) -> Pass:
    out = first
    for pass_ in reversed(passes):
        out = compose(out, pass_)
    return out

def identity(input: _T) -> _T:
    return input
