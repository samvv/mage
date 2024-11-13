
import inspect
from abc import abstractmethod
from typing import Any, Callable, Generic, Protocol, TypeVar, overload
from .logging import info

from magelang.util import Nothing, Option, Something, is_nothing, panic, to_maybe_none

_X = TypeVar('_X', contravariant=True)
_Y = TypeVar('_Y', covariant=True)

type Pass[_X, _Y] = PassFn[_X, _Y] | type[PassBase[_X, _Y]]

class PassFn(Protocol[_X, _Y]):

    @abstractmethod
    def __call__(self, input: _X, /, *args, **kwargs) -> _Y: ...

class PassBase(Generic[_X, _Y]):

    @abstractmethod
    def apply(self, input: _X, /, *args, **kwargs) -> _Y: ...

    def get_depends(self) -> Pass:
        return identity

class Context:

    def __init__(self, opts: dict[str, Any]) -> None:
        self.opts = opts

    def has_option(self, name: str) -> bool:
        return name in self.opts

    def get_option(self, name: str, default: Any = None) -> Any:
        return self.opts.get(name, default)

_K = TypeVar('_K')
_K1 = TypeVar('_K1')
_K2 = TypeVar('_K2')
_T = TypeVar('_T')
_R = TypeVar('_R')
_S = TypeVar('_S')

class Returns(Protocol[_Y]):

    def __call__(self, *args: Any, **kwds: Any) -> _Y: ...

def apply(ctx: Context, input: _T, pass_: Pass[_T, _R]) -> _R:

    def get_dependency(name: str, ty: type | None, default: Option[Any]) -> Any:
        if ty is Context:
            return ctx
        if ty is None or ty is bool or ty is str or ty is float or ty is int:
            if is_nothing(default) and not ctx.has_option(name):
                panic(f"Option {name} has no default and is not provided.")
            return ctx.get_option(name, to_maybe_none(default))
        panic(f"Trying to inject an unknown type {ty} in {pass_}")

    def apply_inject(fn: Returns[_Y], *in_args, **in_kwargs) -> _Y:

        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(fn)

        # These structures are not supported
        assert(varargs is None)
        assert(varkw is None)

        # `self` should be added by Python itself, not us
        if 'self' in args:
            args.remove('self')

        out_args = list(in_args)
        for i, name in enumerate(args[len(in_args):]):
            ty = annotations.get(name)
            default = Nothing()
            if defaults is not None:
                k = i+len(in_args)-(len(args)-len(defaults))
                if k >= 0:
                    default = Something(defaults[k])
            out_args.append(get_dependency(name, ty, default))

        out_kwargs = dict(in_kwargs)
        for name in kwonlyargs:
            if name not in in_kwargs:
                ty = annotations.get(name)
                default = Nothing()
                if kwonlydefaults is not None and name in kwonlydefaults:
                    default = Something(kwonlydefaults[name])
                out_kwargs[name] = get_dependency(name, ty, default)

        return fn(*out_args, **out_kwargs)

    name = pass_.__name__ # type: ignore
    if name != '_wrapper':
        info(f'Running {name}')

    fn = apply_inject(pass_).apply if inspect.isclass(pass_) else pass_

    return apply_inject(fn, input)

def distribute(map: dict[_K, Pass[_T, _R]]) -> Pass[_T, dict[_K, _R]]:

    def _wrapper(input: _T, ctx: Context) -> dict[_K, _R]:
        out = dict[_K, _R]()
        for key, value in map.items():
            out[key] = apply(ctx, input, value)
        return out

    return _wrapper

def merge(left: Pass[_T, dict[_K, _R]], right: Pass[_T, dict[_K, _R]]) -> Pass[_T, dict[_K, _R]]:

    def _wrapper(input: _T, ctx: Context) -> dict[_K, _R]:
        out = dict[_K, _R]()
        for key, value in apply(ctx, input, left).items():
            out[key] = value
        for key, value in apply(ctx, input, right).items():
            out[key] = value
        return out

    return _wrapper


def each_value(pass_: Pass[_T, _R]) -> Pass[dict[_K, _T], dict[_K, _R]]:

    def _wrapper(input: dict[_K, _T], ctx: Context) -> dict[_K, _R]:
        out = dict[_K, _R]()
        for key, value in input.items():
            out[key] = apply(ctx, value, pass_)
        return out

    return _wrapper

def map_key(proc: Callable[[_K1], _K2]) -> Pass[dict[_K1, _T], dict[_K2, _T]]:

    def _wrapper(input: dict[_K1, _T]) -> dict[_K2, _T]:
        out = dict[_K2, _T]()
        for key, value in input.items():
            out[proc(key)] = value
        return out

    return _wrapper

def compose(a: Pass[_T, _R], b: Pass[_R, _S]) -> Pass[_T, _S]:
    def _wrapper(input: _T, ctx: Context) -> _S:
        return apply(ctx, apply(ctx, input, a), b)
    return _wrapper

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
    for pass_ in passes:
        out = compose(out, pass_)
    return out

def identity(input: _T) -> _T:
    return input

