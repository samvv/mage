"""
Stand-alone module to launch command-line applications
"""

import math
import inspect
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
import sys
from types import ModuleType, UnionType
from typing import Any, Generic, Literal, TypeAliasType, TypeVar, Union
import typing

def _to_kebab_case(name: str) -> str:
    return name.replace('_', '-')

def _to_snake_case(name: str) -> str:
    return name.replace('-', '_')

type _ArgValue = Any

type _ArgValues = dict[str, _ArgValue]

type _ArgFn = Callable[[str, _ArgValue, _ArgValues], None]

ARGFLAGS_FLAG = 1
ARGFLAGS_POSITIONAL = 2
ARGFLAGS_RESTFLAGS = 4
ARGFLAGS_RESTPOS = 8

def _set_arg_value(name: str, value: Any, out: _ArgValues) -> None:
    out[name] = value

def _bool_setter(name: str, inverted: bool = False) -> _ArgFn:
    def func(_: str, value: Any, out: _ArgValues) -> None:
        out[name] = value != inverted
    return func

def _inserter(name: str) -> _ArgFn:
    def func(key: str, value: Any, out: _ArgValues) -> None:
        if name not in out:
            m = {}
            out[name] = m
        else:
            m = out[name]
        m[key] = value
    return func

def _append(name: str, value: Any, out: _ArgValues) -> None:
    if not name in out:
        out[name] = []
    out[name].append(value)

class _Argument:

    def __init__(self, name: str) -> None:
        self.name = name
        self.flags = 0
        self.ty = Any
        self.min_count = 1
        self.max_count = 1
        self.default: _ArgValue | None = None
        self.parse_callback: _ArgFn = _set_arg_value

    @property
    def is_positional(self) -> bool:
        return (self.flags & ARGFLAGS_POSITIONAL) > 0

    @property
    def is_flag(self) -> bool:
        return (self.flags & ARGFLAGS_FLAG) > 0

    @property
    def is_rest_flags(self) -> bool:
        return (self.flags & ARGFLAGS_RESTFLAGS) > 0

    @property
    def is_rest_pos(self) -> bool:
        return (self.flags & ARGFLAGS_RESTPOS) > 0

    def set_flag(self, enable = True) -> None:
        if enable:
            self.flags |= ARGFLAGS_FLAG
        else:
            self.flags &= ~ARGFLAGS_FLAG

    def set_rest_flags(self, enable = True) -> None:
        if enable:
            self.flags |= ARGFLAGS_RESTFLAGS
        else:
            self.flags &= ~ARGFLAGS_RESTFLAGS

    def set_default(self, value: _ArgValue) -> None:
        self.default = value

    def set_no_max_count(self) -> None:
        self.max_count = math.inf

    def set_positional(self, enable = True) -> None:
        if enable:
            self.flags |= ARGFLAGS_POSITIONAL
        else:
            self.flags &= ~ARGFLAGS_POSITIONAL

    def set_type(self, ty: Any) -> None:
        self.ty = ty

    def set_optional(self) -> None:
        self.min_count = 0

    def set_required(self) -> None:
        if self.min_count == 0:
            self.min_count = 1

    def set_callback(self, cb: _ArgFn) -> None:
        self.parse_callback = cb

class _Command:

    def __init__(self, name: str) -> None:
        self.name = name
        self.callback: Callable[..., int] | None = None
        self._subcommands = dict[str, _Command]()
        self._arguments = dict[str, _Argument]()
        self._pos_args: list[_Argument] = []
        self._rest_flags_argument = None
        # self._arguments_by_flag = dict[str, Argument]()

    def add_subcommand(self, cmd: '_Command') -> None:
        """
        Add a subcommand to this command.

        This class expects the command to not be mutated anymore after it has been added.
        """
        assert(cmd.name not in self._subcommands)
        self._subcommands[cmd.name] = cmd

    def add_argument(self, arg: _Argument) -> None:
        """
        Add an argument to this command.

        This class expects the argument to not be mutated anymore after it has been added.
        """
        assert(arg.name not in self._arguments)
        self._arguments[arg.name] = arg
        if arg.is_positional:
            self._pos_args.append(arg)
        if arg.is_rest_flags:
            assert(self._rest_flags_argument is None)
            self._rest_flags_argument = arg

    @property
    def rest_flags_argument(self) -> _Argument | None:
        return self._rest_flags_argument

    def set_callback(self, callback: Callable[..., Any]) -> None:
        self.callback = callback

    def get_argument(self, name: str) -> _Argument | None:
        return self._arguments.get(name)

    def get_flag(self, name: str) -> _Argument | None:
        arg = self.get_argument(name)
        if arg is not None and arg.is_flag:
            return arg

    def get_positional(self, index: int) -> _Argument | None:
        k = 0
        for i, arg in enumerate(self._pos_args):
            assert(i == len(self._pos_args)-1 or arg.min_count == arg.max_count)
            if index < k + arg.max_count:
                return arg
            k += arg.min_count

    def get_subcommand(self, name: str) -> '_Command | None':
        return self._subcommands.get(name)

class Program(_Command):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._commands = dict[str, _Command]()


_T = TypeVar('_T')

class Peek(Generic[_T]):

    def __init__(self, iter: Iterable[_T]) -> None:
        self._elements = list(iter)
        self._offset = 0

    def get(self) -> _T | None:
        if self._offset >= len(self._elements):
            return None
        element = self._elements[self._offset]
        self._offset += 1
        return element

    def peek(self) -> _T | None:
        return self._elements[self._offset] if self._offset < len(self._elements) else None

def _find(l: Sequence[_T], pred: Callable[[_T], bool]) -> int | None:
    for i, element in enumerate(l):
        if pred(element):
            return i

class CLIError(RuntimeError):
    pass

class ValueParseError(CLIError):
    pass

class ValueMissingError(CLIError):

    def __init__(self, name: str) -> None:
        super().__init__(f"value missing for argument '{name}'")

class UnknownArgError(CLIError):

    def __init__(self, arg: str) -> None:
        super().__init__(f"unknown argument received: '{arg}'")

def _infer_type(value: Any) -> Any:
    return value.__class__ if value is not None else None

def _try_parse_value(text: str, types: Iterable[Any]) -> Any:
    for ty_2 in types:
        try:
            return _parse_value(text, ty_2)
        except ValueParseError:
            pass
    raise ValueParseError(f'unable to parse as any of {types}')

def _parse_value(text: str, ty: Any) -> Any:
    if isinstance(ty, TypeAliasType):
        assert(not ty.__type_params__)
        ty = ty.__value__
    origin = typing.get_origin(ty)
    if origin is UnionType:
        args = typing.get_args(ty)
        return _try_parse_value(text, args)
    if origin is Literal:
        args = typing.get_args(ty)
        for arg in args:
            try:
                value = _parse_value(text, _infer_type(arg))
            except ValueParseError:
                continue
            if value != arg:
                return value
        raise ValueParseError(f"no literal types matched")
    if ty is Path:
        return Path(text)
    if ty is float:
        try:
            return float(text)
        except ValueError:
            raise ValueParseError()
    if ty is str:
        return text
    if ty is Any:
        return _try_parse_value(text, [ bool, int, float, str ])
    if ty is bool:
        if text in [ 'on', 'true', '1' ]:
            return True
        if text in [ 'off', 'false', '0' ]:
            return False
        raise ValueParseError()
    if ty is int:
        try:
            return int(text)
        except ValueError:
            raise ValueParseError()
    raise RuntimeError(f'parsing the given value according to {ty} is not supported')

def _is_optional(ty: Any) -> bool:
    origin = typing.get_origin(ty)
    if origin is UnionType:
        args = typing.get_args(ty)
        for arg in args:
            if arg is None:
                return True
    return False

def _unwrap_optional(ty: Any) -> Any:
    origin = typing.get_origin(ty)
    if origin is UnionType:
        args = typing.get_args(ty)
        return Union[*(arg for arg in args if arg is not None)]
    return ty

def run(mod: ModuleType | str, name: str | None = None) -> int:

    if name is None:
        name = Path(sys.argv[0]).stem

    if isinstance(mod, str):
        import importlib
        mod = importlib.import_module(mod)

    prog = Program(name)

    for name, proc in mod.__dict__.items():

        if not name.startswith('_') and callable(proc) and proc.__module__ == mod.__name__:

            cmd = _Command(_to_kebab_case(name))

            enable_flags = []
            disable_flags = []
            sig = inspect.signature(proc)

            for name, param in sig.parameters.items():

                ty = param.annotation

                arg = _Argument(name)

                arg.set_type(ty)

                if param.default is not param.empty:
                    arg.set_default(param.default)
                    arg.set_optional()

                if param.kind == param.POSITIONAL_ONLY or param.kind == param.POSITIONAL_OR_KEYWORD or param.kind == param.VAR_POSITIONAL:
                    arg.set_positional()
                if param.kind == param.KEYWORD_ONLY or param.kind == param.POSITIONAL_OR_KEYWORD or param.kind == param.VAR_KEYWORD:
                    arg.set_flag()

                is_rest = False
                if param.kind == param.VAR_KEYWORD:
                    is_rest = True
                    arg.set_rest_flags()
                    arg.set_callback(_inserter(name))
                if param.kind == param.VAR_POSITIONAL:
                    is_rest = True
                    arg.flags |= ARGFLAGS_RESTPOS
                    arg.set_no_max_count()
                    arg.set_callback(_append)

                # Generate special cases for flags such as '--enable-foo' and '--disable-bar'
                if not is_rest and ty is bool:
                    if name.startswith('enable_'):
                        suffix = name[7:]
                        enable_flags.append(arg)
                        arg.set_callback(_bool_setter(name))
                        inv_arg = _Argument('disable_' + suffix)
                        inv_arg.set_callback(_bool_setter(name, inverted=True))
                        inv_arg.set_optional()
                        inv_arg.set_type(bool)
                        inv_arg.set_flag()
                        cmd.add_argument(inv_arg)
                    elif name.startswith('disable_'):
                        suffix = name[8:]
                        disable_flags.append(name)
                        arg.set_callback(_bool_setter(name))
                        inv_arg = _Argument('enable_' + suffix)
                        inv_arg.set_optional()
                        inv_arg.set_flag()
                        inv_arg.set_type(bool)
                        inv_arg.set_callback(_bool_setter(name, inverted=True))

                cmd.add_argument(arg)

            if enable_flags or disable_flags:
                enable_all = _Argument('enable_all')
                enable_all.set_optional()
                enable_all.set_type(bool)
                def enable_all_cb(_: str, value: bool, out: _ArgValues) -> None:
                    for name in enable_flags:
                        out[name] = value
                    for name in disable_flags:
                        out[name] = not value
                enable_all.set_callback(enable_all_cb)
                cmd.add_argument(enable_all)
                disable_all = _Argument('disable_all')
                disable_all.set_optional()
                disable_all.set_type(bool)
                def disble_all_cb(_: str, value: bool, out: _ArgValues) -> None:
                    for name in disable_flags:
                        out[name] = value
                    for name in disable_flags:
                        out[name] = not value
                disable_all.set_callback(disble_all_cb)
                cmd.add_argument(disable_all)

            cmd.set_callback(proc)

            prog.add_subcommand(cmd)

    # Variables used during processing of the arguments
    cmd = prog
    args = Peek(sys.argv[1:])
    mapping: _ArgValues = {}
    k = 0

    # Process arguments one by one
    while True:

        arg = args.get()

        if arg is None:
            break # We're at the end of the arguments list

        if arg.startswith('-'): # We're dealing with a flag

            i = _find(arg, lambda ch: ch != '-')

            if i is None:
                raise UnknownArgError(arg)

            try:
                j = arg.index('=', i)
                name = _to_snake_case(arg[i:j])
                value_str = arg[j+1:]
            except ValueError:
                name = _to_snake_case(arg[i:])
                value_str = None

            arg_desc = cmd.get_flag(name)

            if arg_desc is None:
                arg_desc = cmd.rest_flags_argument
                if arg_desc is None:
                    raise UnknownArgError(arg)

            ty = arg_desc.ty

            value = None

            if value_str is not None:
                value = _parse_value(value_str, ty)
            else:
                # `value` is still `None` here
                next_arg = args.peek()
                if next_arg is not None and not next_arg.startswith('-'):
                    try:
                        value = _parse_value(next_arg, ty)
                        args.get()
                    except ValueParseError:
                        pass # `value` remains `None` and lookahead is discarded

            if value is None:
                if arg_desc.ty is bool or arg_desc.is_rest_flags:
                    # Assume `True` in the cases where a boolean is expected or
                    # when it could potentially be a boolean but we don't know
                    # for sure
                    value = True
                elif arg_desc.default is not None:
                    # For all types except bool, attempt to assign the default
                    # value of the flag.
                    value = arg_desc.default
                elif arg_desc.min_count > 0: # If the flag was required
                    raise ValueMissingError(name)

            arg_desc.parse_callback(name, value, mapping)

        else: # We're dealing with a positional argument

            # Try to parse the argument as a subcommand first
            subcmd = cmd.get_subcommand(arg)
            if subcmd is not None:
                cmd = subcmd
                k = 0
                continue

            # If that fails, process it as a plain positional argument
            arg_desc = cmd.get_positional(k)
            if arg_desc is None:
                raise UnknownArgError(arg)

            value = _parse_value(arg, arg_desc.ty)

            arg_desc.parse_callback(arg_desc.name, value, mapping)

            k += 1

    # Build positional arguments and keyword arguments from the mapping
    posargs = []
    kwargs = {}
    for name, value in mapping.items():
        arg_desc = cmd.get_argument(name)
        assert(arg_desc is not None)
        if arg_desc.is_positional:
            if arg_desc.is_rest_pos:
                posargs.extend(value)
            else:
                posargs.append(value)
        else:
            if arg_desc.is_rest_flags:
                kwargs.update(value)
            else:
                kwargs[name] = value

    if cmd.callback is None:
        print('Command could not be executed. Perhaps you specified the wrong arguments?')
        return 1

    # Call the function in user-space
    return cmd.callback(*posargs, **kwargs)

