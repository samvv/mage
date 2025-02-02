"""
Stand-alone module to launch command-line applications
"""

from enum import Enum, IntEnum, StrEnum
import math
import inspect
from collections.abc import Callable, Generator, Iterable, Sequence
from pathlib import Path
import sys
from types import ModuleType, UnionType
import types
from typing import Any, Generic, Literal, TypeAliasType, TypeVar, Union
import typing

from magelang.util import IndentWriter

def _to_kebab_case(name: str) -> str:
    return name.replace('_', '-')

def _to_snake_case(name: str) -> str:
    return name.replace('-', '_')

type _ArgValue = Any

type _ArgValues = dict[str, _ArgValue]

type _ArgFn = Callable[[str, _ArgValue, _ArgValues], None]

ARGFLAGS_FLAG = 1
ARGFLAGS_POSITIONAL = 2
ARGFLAGS_REST = 4

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

def _are_bits_set(mask: int, bit: int) -> bool:
    return mask & bit == bit

def _set_bit(mask: int, bit: int, enable: bool) -> int:
    if enable:
        return mask | bit
    else:
        return mask & ~bit

class _Argument:

    def __init__(self, name: str) -> None:
        self.name = name
        self.flags = 0
        self.ty: Any = None
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
    def is_rest(self) -> bool:
        return _are_bits_set(self.flags, ARGFLAGS_REST)

    @property
    def is_rest_flags(self) -> bool:
        return _are_bits_set(self.flags, ARGFLAGS_FLAG | ARGFLAGS_REST)

    @property
    def is_rest_pos(self) -> bool:
        return _are_bits_set(self.flags, ARGFLAGS_POSITIONAL | ARGFLAGS_REST)

    def set_flag(self, enable = True) -> None:
        self.flags = _set_bit(self.flags, ARGFLAGS_FLAG, enable)

    def set_rest(self, enable = True) -> None:
        self.flags = _set_bit(self.flags, ARGFLAGS_REST, enable)

    def set_positional(self, enable = True) -> None:
        self.flags = _set_bit(self.flags, ARGFLAGS_POSITIONAL, enable)

    def set_default(self, value: _ArgValue) -> None:
        self.default = value

    def set_no_max_count(self) -> None:
        self.max_count = math.inf

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
        self.description: str | None = None
        self.callback: Callable[..., int] | None = None
        self._subcommands = dict[str, _Command]()
        self._arguments = dict[str, _Argument]()
        self._pos_args: list[_Argument] = []
        self._rest_flags_argument = None
        # self._arguments_by_flag = dict[str, Argument]()

    def arguments(self) -> Iterable[_Argument]:
        return self._arguments.values()

    def subcommands(self) -> 'Iterable[_Command]':
        return self._subcommands.values()

    def add_subcommand(self, cmd: '_Command') -> None:
        """
        Add a subcommand to this command.

        This class expects the command to not be mutated anymore after it has been added.
        """
        assert(cmd.name not in self._subcommands)
        self._subcommands[cmd.name] = cmd

    def count_arguments(self) -> int:
        return len(self._arguments)

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

    def count_subcommands(self) -> int:
        return len(self._subcommands)

    def get_flag(self, name: str) -> _Argument | None:
        arg = self.get_argument(name)
        if arg is not None and arg.is_flag:
            return arg

    def get_subcommand(self, name: str) -> '_Command | None':
        return self._subcommands.get(name)

class Program(_Command):
    pass

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
    if issubclass(ty, StrEnum):
        try:
            return ty(text) # type: ignore
        except ValueError:
            raise ValueParseError()
    if issubclass(ty, IntEnum):
        try:
            return ty(int(text)) # type: ignore
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

def add_complements(prog: Program) -> None:
    """
    Generates additional arguments that are the inverse of existing arguments.

    Example: `--enable-foo` will ackquire `--disable-foo` and both will work.

    Two additional flags can also be enabled that enable/disable all flags at once.

    Example: `--enable-all` and `--disable-all`
    """

    def visit(cmd: _Command) -> None:

        enable_flags = []
        disable_flags = []

        for arg in list(cmd.arguments()):
            if not arg.is_rest and arg.ty is bool:
                if arg.name.startswith('enable_'):
                    suffix = arg.name[7:]
                    enable_flags.append(arg.name)
                    arg.set_callback(_bool_setter(arg.name))
                    inv_arg = _Argument('disable_' + suffix)
                    inv_arg.set_callback(_bool_setter(arg.name, inverted=True))
                    inv_arg.set_optional()
                    inv_arg.set_type(bool)
                    inv_arg.set_flag()
                    cmd.add_argument(inv_arg)
                elif arg.name.startswith('disable_'):
                    suffix = arg.name[8:]
                    disable_flags.append(arg.name)
                    arg.set_callback(_bool_setter(arg.name))
                    inv_arg = _Argument('enable_' + suffix)
                    inv_arg.set_optional()
                    inv_arg.set_flag()
                    inv_arg.set_type(bool)
                    inv_arg.set_callback(_bool_setter(arg.name, inverted=True))

        if enable_flags or disable_flags:
            enable_all = _Argument('enable_all')
            enable_all.set_flag()
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
            disable_all.set_flag()
            disable_all.set_optional()
            disable_all.set_type(bool)
            def disble_all_cb(_: str, value: bool, out: _ArgValues) -> None:
                for name in disable_flags:
                    out[name] = value
                for name in disable_flags:
                    out[name] = not value
            disable_all.set_callback(disble_all_cb)
            cmd.add_argument(disable_all)

        for subcmd in cmd.subcommands():
            visit(subcmd)

    visit(prog)

def describe_type(ty: Any) -> str:
    if type(ty) is typing.TypeAliasType:
        return describe_type(ty.__value__)
    origin = typing.get_origin(ty)
    if origin is None:
        return ty.__name__
    elif origin is typing.Union or origin is types.UnionType:
        return ' | '.join(describe_type(arg) for arg in typing.get_args(ty))
    elif origin is typing.Literal:
        return ' | '.join(repr(lit) for lit in typing.get_args(ty))
    else:
        raise NotImplementedError(f"{ty} cannot be printed yet")

def print_help_loop(cmd: _Command, out: IndentWriter, depth: int) -> None:
    out.write(f'{cmd.name}')
    if cmd.description is not None:
        out.write('    ')
        out.write(cmd.description)
    out.writeln()
    out.indent()
    if cmd.count_arguments() > 0 and depth == 0:
        out.writeln('Arguments and flags:')
        for arg in cmd.arguments():
            if arg.is_flag:
                if len(arg.name) == 1:
                    out.write(f'-{arg.name}')
                else:
                    out.write(f'--{arg.name}')
            elif arg.min_count == 0:
                if arg.max_count == 1:
                    out.write(f'[{arg.name}]')
                else:
                    out.write(f'[{arg.name}..]')
            else:
                if arg.max_count == 1:
                    out.write(f'<{arg.name}>')
                else:
                    out.write(f'<{arg.name}..>')
            out.write('    ')
            out.write(describe_type(arg.ty))
            out.writeln()
    if cmd.count_subcommands() > 0:
        out.writeln('\nSubcommands:')
        out.indent()
        for sub in cmd.subcommands():
            print_help_loop(sub, out, depth+1)
        out.dedent()
    out.dedent()

def print_help(cmd: _Command) -> None:
    out = IndentWriter(sys.stderr)
    print_help_loop(cmd, out, 0)
    exit(1)

def _flatten_union_type(ty: Any) -> Generator[Any]:
    origin = typing.get_origin(ty)
    if origin is typing.Union or origin is types.UnionType:
        for arg in typing.get_args(ty):
            yield from _flatten_union_type(arg)
    else:
        yield ty

def _get_type_default(ty: Any) -> Any:
    if isinstance(ty, Enum):
        if hasattr(ty, '_default_'):
            return getattr(ty, '_default_')

def _has_type(left: Any, right: Any) -> bool:
    """
    Check whether `right` occurs somewhere in `left`.

    For instance:
    has_type(int | bool | str, bool) == True
    has_type(int | bool | str, float) == False
    """
    return right in _flatten_union_type(left)

def run(mod: ModuleType | str, name: str | None = None) -> int:

    if name is None:
        name = Path(sys.argv[0]).stem

    if isinstance(mod, str):
        import importlib
        mod = importlib.import_module(mod)

    prog = Program(name)


    for name, proc in mod.__dict__.items():

        if not name.startswith('_') and callable(proc) and proc.__module__ == mod.__name__:

            try:
                sig = inspect.signature(proc)
            except ValueError:
                continue

            cmd = _Command(_to_kebab_case(name))

            types = typing.get_type_hints(proc)

            for name, param in sig.parameters.items():

                ty = types[param.name]

                arg = _Argument(name)

                arg.set_type(ty)

                if param.default is not param.empty:
                    arg.set_default(param.default)
                    arg.set_optional()

                if param.kind == param.POSITIONAL_ONLY or param.kind == param.POSITIONAL_OR_KEYWORD or param.kind == param.VAR_POSITIONAL:
                    arg.set_positional()
                if param.kind == param.KEYWORD_ONLY or param.kind == param.POSITIONAL_OR_KEYWORD or param.kind == param.VAR_KEYWORD:
                    arg.set_flag()

                if param.kind == param.VAR_KEYWORD:
                    if typing.get_origin(ty) is typing.Unpack:
                        args = typing.get_args(ty)
                        total = args[0].__total__
                        for k, v in typing.get_type_hints(args[0]).items():
                            arg = _Argument(k)
                            arg.set_flag()
                            required = True
                            if typing.get_origin(v) is typing.NotRequired:
                                required = False
                                v = typing.get_args(v)[0]
                            arg.set_type(v)
                            if not total or not required:
                                arg.set_optional()
                            cmd.add_argument(arg)
                        continue
                    else:
                        arg.set_rest()
                        arg.set_callback(_inserter(name))
                if param.kind == param.VAR_POSITIONAL:
                    arg.set_rest()
                    arg.set_no_max_count()
                    arg.set_callback(_append)

                cmd.add_argument(arg)

            cmd.set_callback(proc)

            help_arg = _Argument('help')
            help_arg.set_flag()
            help_arg.set_type(bool)
            help_arg.set_callback(lambda key, value, out, cmd=cmd: print_help(cmd))
            cmd.add_argument(help_arg)

            prog.add_subcommand(cmd)

    help_arg = _Argument('help')
    help_arg.set_flag()
    help_arg.set_type(bool)
    help_arg.set_callback(lambda key, value, out: print_help(prog))
    prog.add_argument(help_arg)

    add_complements(prog)

    # Variables used during processing of the arguments
    cmd = prog
    args = Peek(sys.argv[1:])
    mapping: _ArgValues = {}
    pos_index = 0
    pos_arg_count = 0

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
                if _has_type(arg_desc.ty, bool) or arg_desc.is_rest_flags:
                    # Assume `True` in the cases where a boolean is expected or
                    # when it could potentially be a boolean but we don't know
                    # for sure
                    value = True
                elif arg_desc.default is not None:
                    # For all types except bool, attempt to assign the default
                    # value of the flag.
                    value = arg_desc.default
                else:
                    # If the user didn't explicitly specify a default, maybe we
                    # can derive a default from the type.
                    default = _get_type_default(arg_desc.ty)
                    if default is not None:
                        value = default
                    elif arg_desc.min_count > 0: # If the flag was required
                        raise ValueMissingError(name)

            arg_desc.parse_callback(name, value, mapping)

        else: # We're dealing with a positional argument

            # Try to parse the argument as a subcommand first
            subcmd = cmd.get_subcommand(arg)
            if subcmd is not None:
                cmd = subcmd
                pos_index = 0
                pos_arg_count = 0
                continue

            # If that fails, process it as a plain positional argument

            while True:
                if pos_index >= len(cmd._pos_args):
                    raise UnknownArgError(arg)
                arg_desc = cmd._pos_args[pos_index]
                if pos_arg_count >= arg_desc.max_count:
                    pos_index += 1
                    pos_arg_count = 0
                    continue
                value = _parse_value(arg, arg_desc.ty)
                arg_desc.parse_callback(arg_desc.name, value, mapping)
                pos_arg_count += 1
                break

    # TODO check that required arguments have been set

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

