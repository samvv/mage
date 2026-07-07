
import inspect
from abc import abstractmethod
from typing import Any, Callable, Protocol, cast, overload

from .logging import info
from .util import Nothing, Option, Something, is_nothing, panic, to_maybe_none, to_snake_case

type Pass[X, Y] = PassFn[X, Y] | PassBase[X, Y]

class PassFn[X, Y](Protocol):

    __name__: str

    @abstractmethod
    def __call__(self, input: X, /, *args, **kwargs) -> Y: ...

class PassBase[X, Y]:

    @abstractmethod
    def apply(self, input: X, /, *args, **kwargs) -> Y: ...

    def get_depends(self) -> Pass[Any, X]:
        return identity

    @property
    def name(self) -> str:
        return to_snake_case(self.__class__.__name__)

    def getfullargspec(self) -> inspect.FullArgSpec:
        return inspect.getfullargspec(self.apply)

class LiftedPass[X, Y](PassBase[X, Y]):

    def __init__(self, fn: PassFn[X, Y]) -> None:
        super().__init__()
        self._fn = fn

    def apply(self, input: X, /, *args, **kwargs) -> Y:
        return self._fn(input, *args, **kwargs)

    @property
    def name(self) -> str:
        return self._fn.__name__

    def getfullargspec(self) -> inspect.FullArgSpec:
        return inspect.getfullargspec(self._fn)

class Context:

    def __init__(self, opts: dict[str, Any], silent: bool = False) -> None:
        self.opts = opts
        self.silent = silent

    def has_option(self, name: str) -> bool:
        return name in self.opts

    def get_option(self, name: str, default: Any = None) -> Any:
        return self.opts.get(name, default)

_pass_registry = dict[str, Pass[Any, Any]]()

def declare_pass[X, Y]() -> Callable[[PassFn[X, Y]], PassFn[X, Y]]:
    def decorator(func: PassFn[X, Y]) -> PassFn[X, Y]:
        _pass_registry[func.__name__] = func
        return func
    return decorator

def get_pass_by_name(name: str) -> Pass[Any, Any] | None:
    return _pass_registry.get(name)

def lift[X, Y](pass_: Pass[X, Y]) -> PassBase[X, Y]:
    if callable(pass_):
        return LiftedPass(pass_)
    return pass_

def apply[X, Y](ctx: Context, input: X, pass_: Pass[X, Y]) -> Y:

    pass_ = lift(pass_)

    def get_dependency(name: str, ty: type | None, default: Option[Any]) -> Any:
        if ty is Context:
            return ctx
        if is_nothing(default) and not ctx.has_option(name):
            panic(f"Option {name} has no default and no value is provided.")
        return ctx.get_option(name, to_maybe_none(default))

    def apply_inject(pass_: PassBase[X, Y], *in_args, **in_kwargs) -> Y:

        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = pass_.getfullargspec()

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

        return pass_.apply(*out_args, **out_kwargs)

    name = pass_.name
    if name != '_wrapper' and not ctx.silent:
        info(f'Running {name}')

    return apply_inject(pass_, input)

def distribute[K, T, R](map: dict[K, Pass[T, R]]) -> Pass[T, dict[K, R]]:
    """
    Compose a dictionary of passes to a pass producing a dictionary with equal
    keys and the values of the given passes.

    ```
    apply(
        distribute({
            one: lambda x: x + 1,
            two: lambda x: x + 2,
        }),
        { one: 0, two: 0 }
    )
    # result is { one: 1, two: 2 }
    ```
    """

    def _wrapper(input: T, ctx: Context) -> dict[K, R]:
        out = dict[K, R]()
        for key, value in map.items():
            out[key] = apply(ctx, input, value)
        return out

    return _wrapper

def merge[T, K, R](left: Pass[T, dict[K, R]], right: Pass[T, dict[K, R]]) -> Pass[T, dict[K, R]]:
    """
    Compose two passes producing dictionaries to one pass producing a merged
    dictionary.
    """
    def _wrapper(input: T, ctx: Context) -> dict[K, R]:
        out = dict[K, R]()
        for key, value in apply(ctx, input, left).items():
            out[key] = value
        for key, value in apply(ctx, input, right).items():
            out[key] = value
        return out

    return _wrapper


def each_value[T, K, R](pass_: Pass[T, R]) -> Pass[dict[K, T], dict[K, R]]:
    """
    Transform each value of an incoming dictionary with the given pass.
    """

    def _wrapper(input: dict[K, T], ctx: Context) -> dict[K, R]:
        out = dict[K, R]()
        for key, value in input.items():
            out[key] = apply(ctx, value, pass_)
        return out

    return _wrapper

def map_key[T, K1, K2](proc: Callable[[K1], K2]) -> Pass[dict[K1, T], dict[K2, T]]:
    """
    Transform each key of an incoming dictionary with the given pass.
    """

    def _wrapper(input: dict[K1, T]) -> dict[K2, T]:
        out = dict[K2, T]()
        for key, value in input.items():
            out[proc(key)] = value
        return out

    return _wrapper

def compose[R, S, T](a: Pass[T, R], b: Pass[R, S]) -> Pass[T, S]:
    def _wrapper(input: T, ctx: Context) -> S:
        return apply(ctx, apply(ctx, input, a), b)
    return _wrapper
@overload
def pipeline[T0, T1](p0: Pass[T0, T1], /) -> Pass[T0, T1]: ...

@overload
def pipeline[T0, T1, T2](p0: Pass[T0, T1], p1: Pass[T1, T2], /) -> Pass[T0, T2]: ...

@overload
def pipeline[T0, T1, T2, T3](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], /) -> Pass[T0, T3]: ...

@overload
def pipeline[T0, T1, T2, T3, T4](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], /) -> Pass[T0, T4]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], /) -> Pass[T0, T5]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], /) -> Pass[T0, T6]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], /) -> Pass[T0, T7]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], /) -> Pass[T0, T8]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], /) -> Pass[T0, T9]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], /) -> Pass[T0, T10]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], /) -> Pass[T0, T11]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], /) -> Pass[T0, T12]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], /) -> Pass[T0, T13]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], /) -> Pass[T0, T14]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], /) -> Pass[T0, T15]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], /) -> Pass[T0, T16]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], /) -> Pass[T0, T17]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], p17: Pass[T17, T18], /) -> Pass[T0, T18]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], p17: Pass[T17, T18], p18: Pass[T18, T19], /) -> Pass[T0, T19]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], p17: Pass[T17, T18], p18: Pass[T18, T19], p19: Pass[T19, T20], /) -> Pass[T0, T20]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], p17: Pass[T17, T18], p18: Pass[T18, T19], p19: Pass[T19, T20], p20: Pass[T20, T21], /) -> Pass[T0, T21]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], p17: Pass[T17, T18], p18: Pass[T18, T19], p19: Pass[T19, T20], p20: Pass[T20, T21], p21: Pass[T21, T22], /) -> Pass[T0, T22]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22, T23](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], p17: Pass[T17, T18], p18: Pass[T18, T19], p19: Pass[T19, T20], p20: Pass[T20, T21], p21: Pass[T21, T22], p22: Pass[T22, T23], /) -> Pass[T0, T23]: ...

@overload
def pipeline[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22, T23, T24](p0: Pass[T0, T1], p1: Pass[T1, T2], p2: Pass[T2, T3], p3: Pass[T3, T4], p4: Pass[T4, T5], p5: Pass[T5, T6], p6: Pass[T6, T7], p7: Pass[T7, T8], p8: Pass[T8, T9], p9: Pass[T9, T10], p10: Pass[T10, T11], p11: Pass[T11, T12], p12: Pass[T12, T13], p13: Pass[T13, T14], p14: Pass[T14, T15], p15: Pass[T15, T16], p16: Pass[T16, T17], p17: Pass[T17, T18], p18: Pass[T18, T19], p19: Pass[T19, T20], p20: Pass[T20, T21], p21: Pass[T21, T22], p22: Pass[T22, T23], p23: Pass[T23, T24], /) -> Pass[T0, T24]: ...


def pipeline(*passes: Pass) -> Pass:
    out = identity
    for pass_ in passes:
        out = compose(out, pass_)
    return out

def identity[T](input: T) -> T:
    return input

