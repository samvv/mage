"""
Stand-alone module to launch command-line applications
"""

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

type ArgValue = Any

type ArgValues = dict[str, ArgValue]

type ArgFn = Callable[[str, ArgValue, ArgValues], None]

ARGFLAGS_FLAG = 1
ARGFLAGS_POSITIONAL = 2

def _set_arg_value(name: str, value: Any, out: ArgValues) -> None:
    out[name] = value

class Argument:

    def __init__(self, name: str) -> None:
        self.name = name
        self.flag_name = _to_kebab_case(name)
        self.flags = 0
        self.ty = Any
        self.min_count = 1
        self.max_count = 1
        self.default: ArgValue | None = None
        self.callback: ArgFn = _set_arg_value

    @property
    def is_positional(self) -> bool:
        return (self.flags & ARGFLAGS_POSITIONAL) > 0

    @property
    def is_flag(self) -> bool:
        return (self.flags & ARGFLAGS_FLAG) > 0

    def set_flag(self, enable = True) -> None:
        if enable:
            self.flags |= ARGFLAGS_FLAG
        else:
            self.flags &= ~ARGFLAGS_FLAG

    def set_default(self, value: ArgValue) -> None:
        self.default = value

    def set_flag_name(self, name: str) -> None:
        self.flag_name = name

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

    def set_callback(self, cb: ArgFn) -> None:
        self.callback = cb

class Command:

    def __init__(self, name: str) -> None:
        self.name = name
        self.callback: Callable[..., int] | None = None
        self._subcommands = dict[str, Command]()
        self._arguments = dict[str, Argument]()
        # self._arguments_by_flag = dict[str, Argument]()

    def add_subcommand(self, cmd: 'Command') -> None:
        """
        Add a subcommand to this command.

        This class expects the command to not be mutated anymore after it has been added.
        """
        assert(cmd.name not in self._subcommands)
        self._subcommands[cmd.name] = cmd

    def add_argument(self, arg: Argument) -> None:
        """
        Add an argument to this command.

        This class expects the argument to not be mutated anymore after it has been added.
        """
        assert(arg.name not in self._arguments)
        # assert(arg.flag_name not in self._arguments_by_flag)
        self._arguments[arg.name] = arg
        # self._arguments_by_flag[arg.flag_name] = arg

    def set_callback(self, callback: Callable[..., Any]) -> None:
        self.callback = callback

    def get_flag(self, name: str) -> Argument | None:
        arg = self._arguments.get(name)
        if arg is not None and arg.is_flag:
            return arg

    def get_positional(self, index: int) -> Argument | None:
        i = 0
        for arg in self._arguments.values():
            if arg.is_positional:
                assert(arg.min_count == arg.max_count)
                if index < i + arg.max_count:
                    return arg
                i += arg.min_count

    def get_subcommand(self, name: str) -> 'Command | None':
        return self._subcommands.get(name)

class Program(Command):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._commands = dict[str, Command]()


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

def is_value_required(ty: Any) -> bool:
    return ty not in [ bool ]

def try_parse_value(text: str, types: Iterable[Any]) -> Any:
    for ty_2 in types:
        try:
            return parse_value(text, ty_2)
        except ValueParseError:
            pass
    raise ValueParseError(f'unable to parse as any of {types}')

def infer_type(value: Any) -> Any:
    return value.__class__ if value is not None else None

def parse_value(text: str, ty: Any) -> Any:
    if isinstance(ty, TypeAliasType):
        assert(not ty.__type_params__)
        ty = ty.__value__
    origin = typing.get_origin(ty)
    if origin is UnionType:
        args = typing.get_args(ty)
        return try_parse_value(text, args)
    if origin is Literal:
        args = typing.get_args(ty)
        for arg in args:
            try:
                value = parse_value(text, infer_type(arg))
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
            return ValueParseError()
    if ty is str:
        return text
    if ty is Any:
        return try_parse_value(text, [ bool, int, float, str ])
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
            return ValueParseError()
    raise RuntimeError(f'parsing the given value according to {ty} is not supported')

def is_optional(ty: Any) -> bool:
    origin = typing.get_origin(ty)
    if origin is UnionType:
        args = typing.get_args(ty)
        for arg in args:
            if arg is None:
                return True
    return False

def unwrap_optional(ty: Any) -> Any:
    origin = typing.get_origin(ty)
    if origin is UnionType:
        args = typing.get_args(ty)
        return Union[*(arg for arg in args if arg is not None)]
    return ty

def bool_setter(name: str, inverted: bool = False) -> ArgFn:
    def func(_: str, value: Any, out: ArgValues) -> None:
        print(value, inverted, value != inverted)
        out[name] = value != inverted
    return func

def run(mod: ModuleType | str, name: str | None = None) -> int:

    if name is None:
        name = Path(sys.argv[1]).stem

    if isinstance(mod, str):
        import importlib
        mod = importlib.import_module(mod)

    prog = Program(name)

    for name, proc in mod.__dict__.items():
        if not name.startswith('_') and callable(proc) and proc.__module__ == mod.__name__:
            cmd = Command(_to_kebab_case(name))
            enable_flags = []
            disable_flags = []
            sig = inspect.signature(proc)
            for name, param in sig.parameters.items():
                ty = param.annotation
                arg = Argument(name)
                arg.set_type(ty)
                if param.default is not param.empty:
                    arg.set_default(param.default)
                    arg.set_optional()
                if param.kind == param.POSITIONAL_ONLY or param.kind == param.POSITIONAL_OR_KEYWORD:
                    arg.set_positional()
                if param.kind == param.KEYWORD_ONLY or param.kind == param.POSITIONAL_OR_KEYWORD:
                    arg.set_flag()
                if name.startswith('enable_'):
                    suffix = name[7:]
                    enable_flags.append(arg)
                    arg.set_callback(bool_setter(name))
                    inv_arg = Argument('disable_' + suffix)
                    inv_arg.set_callback(bool_setter(name, inverted=True))
                    inv_arg.set_optional()
                    inv_arg.set_type(bool)
                    inv_arg.set_flag()
                    cmd.add_argument(inv_arg)
                elif name.startswith('disable_'):
                    suffix = name[8:]
                    disable_flags.append(name)
                    arg.set_callback(bool_setter(name))
                    inv_arg = Argument('enable_' + suffix)
                    inv_arg.set_optional()
                    inv_arg.set_flag()
                    inv_arg.set_type(bool)
                    inv_arg.set_callback(bool_setter(name, inverted=True))
                cmd.add_argument(arg)
            if enable_flags or disable_flags:
                enable_all = Argument('enable_all')
                enable_all.set_optional()
                enable_all.set_type(bool)
                def enable_all_cb(_: str, value: bool, out: ArgValues) -> None:
                    for name in enable_flags:
                        out[name] = value
                    for name in disable_flags:
                        out[name] = not value
                enable_all.set_callback(enable_all_cb)
                cmd.add_argument(enable_all)
                disable_all = Argument('disable_all')
                disable_all.set_optional()
                disable_all.set_type(bool)
                def disble_all_cb(_: str, value: bool, out: ArgValues) -> None:
                    for name in disable_flags:
                        out[name] = value
                    for name in disable_flags:
                        out[name] = not value
                disable_all.set_callback(disble_all_cb)
                cmd.add_argument(disable_all)
            cmd.set_callback(proc)
            prog.add_subcommand(cmd)

    cmd = prog
    args = Peek(sys.argv[1:])
    posargs = []
    kwargs = {}
    k = 0
    while True:
        arg = args.get()
        if arg is None:
            break
        if arg.startswith('-'):
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
                raise UnknownArgError(arg)
            ty = arg_desc.ty
            value = None
            if value_str is not None:
                value = parse_value(value_str, ty)
            else:
                # `value` is still `None` here
                arg_1 = args.peek()
                if arg_1 is not None and not arg_1.startswith('-'):
                    try:
                        value = parse_value(arg_1, ty)
                        args.get()
                    except ValueParseError:
                        pass # `value` remains `None` and lookahead is discarded
            if value is None:
                if arg_desc.ty is bool:
                    value = True
                elif arg_desc.default is not None:
                    value = arg_desc.default
                elif arg_desc.min_count > 0:
                    raise ValueMissingError(name)
            arg_desc.callback(name, value, kwargs)
        else:
            subcmd = cmd.get_subcommand(arg)
            if subcmd is not None:
                cmd = subcmd
                continue
            arg_desc = cmd.get_positional(k)
            if arg_desc is None:
                raise UnknownArgError(arg)
            posargs.append(parse_value(arg, arg_desc.ty))
            k += 1

    assert(cmd.callback is not None)
    return cmd.callback(*posargs, **kwargs)

