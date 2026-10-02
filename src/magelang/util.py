
from collections.abc import Iterable
import importlib.util
import io
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Callable, Generic, Iterator, Never, Protocol, Sequence, SupportsIndex, TextIO, TypeGuard, TypeIs, TypeVar, overload
import re


def plural(name: str) -> str:
    return name if name.endswith('s') else f'{name}s'


type Files = dict[str, str]


def constant[T](value: T) -> Callable[..., T]:
    def func(*args, **kwargs) -> T:
        return value
    return func


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


class Nothing:
    """
    An alternative to `None` that can be used in cases where `None` is already
    semantically taken.
    """
    pass


class Something[T]:

    def __init__(self, value: T) -> None:
        super().__init__()
        self.value = value

    def to_maybe_none(self) -> T | None:
        return self.value


type Option[T] = Something[T] | Nothing


def is_nothing(opt: Option[Any]) -> TypeIs[Nothing]:
    return isinstance(opt, Nothing)


def is_something(opt: Option[Any]) -> TypeIs[Something]:
    return isinstance(opt, Something)


def to_maybe_none[T](value: Option[T]) -> T | None:
    return value.value if isinstance(value, Something) else None


def nonnull[T](value: T | None) -> T:
    assert(value is not None)
    return value


class Eq(Protocol):
    def __eq__(self, value: object, /) -> bool: ...


class MiniSeq[T](Protocol):
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, i: SupportsIndex, /) -> T: ...
    @overload
    def __getitem__(self, s: slice, /) -> list[T]: ...


def get_common_suffix[T: Eq](names: Sequence[MiniSeq[T]]) -> MiniSeq[T]:
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

    def writeln(self, text: str = '') -> None:
        self.write(text)
        self.write('\n')


class NameGenerator:

    def __init__(
        self,
        namespace: str | None = None,
        default_prefix: str | None= 'tmp',
        hide_first: bool = False
    ) -> None:
        self._counts: dict[str, int] = {}
        self.namespace = namespace
        self._hide_first = hide_first
        self._default_prefix = default_prefix

    def is_free(self, name: str) -> bool:
        return True

    def __call__(
        self,
        prefix: str | None = None,
        suffix: str | None = None,
        hide: bool = False,
        hide_first: bool | None = None
    ) -> str:
        if prefix is None:
            prefix = self._default_prefix
        if hide_first is None:
            hide_first = self._hide_first
        while True:
            chunks = []
            if self.namespace is not None:
                chunks.append(self.namespace)
            if prefix is not None:
                chunks.append(prefix)
            if suffix is not None:
                chunks.append(suffix)
            assert(len(chunks) > 0)
            name = '_'.join(chunks)
            count = self._counts.get(name, 0)
            if count > 0 or not hide_first:
                name += '_' + str(count)
            if hide:
                name = '_' + name
            if self.is_free(name):
                self._counts[name] = count + 1
                return name

    def reset(self) -> None:
        self._counts = {}


# Proxies for sequences

class MapProxy[T, R](Sequence[R]):

    def __init__(self, elements: Sequence[T], proc: Callable[[T], R]) -> None:
        super().__init__()
        self._elements = elements
        self._proc = proc

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self) -> Iterator[R]:
        for element in self._elements:
            yield self._proc(element)

    def __reversed__(self) -> Iterator[R]:
        for element in reversed(self._elements):
            yield self._proc(element)

    @overload
    def __getitem__(self, key: int) -> R: ...

    @overload
    def __getitem__(self, key: slice) -> Sequence[R]: ...

    def __getitem__(self, key: int | slice) -> R | Sequence[R]:
        if isinstance(key, slice):
            return list(self._proc(element) for element in self._elements[key])
        else:
            return self._proc(self._elements[key])


class DropProxy[T](Sequence[T]):

    def __init__(self, elements: 'Sequence[T]', count: int) -> None:
        assert(count <= len(elements))
        self._elements = elements
        self._to_drop = count

    def __len__(self) -> int:
        return len(self._elements)-self._to_drop

    def __iter__(self) -> Iterator[T]:
        n = len(self._elements)
        for i in range(0, n-self._to_drop):
            yield self._elements[i]

    def __reversed__(self) -> Iterator[T]:
        n = len(self._elements)
        for i in range(0, n-self._to_drop):
            yield self._elements[n-i-1]

    @overload
    def __getitem__(self, key: int) -> T: ...

    @overload
    def __getitem__(self, key: slice) -> Sequence[T]: ...

    def __getitem__(self, key: int | slice) -> T | Sequence[T]:
        max_index = len(self._elements)-self._to_drop
        if isinstance(key, slice):
            start = min(key.start, max_index)
            stop = min(key.stop, max_index)
            return self._elements[start:stop]
        else:
            if key >= max_index:
                raise IndexError(f'index {key} out of bounds')
            return self._elements[key]


class SeqSet[T]:
    """
    Like a set, but the order in which the elements are inserted is preserved.
    """

    def __init__(self, iter: Iterable[T] | None = None) -> None:
        if iter is None:
            iter = []
        self._list = list(iter)
        self._set = set(iter)

    def append(self, element: T) -> None:
        if element not in self._set:
            self._list.append(element)
            self._set.add(element)

    def __len__(self) -> int:
        return len(self._list)

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    @overload
    def __getitem__(self, key: int) -> T: ...

    @overload
    def __getitem__(self, key: slice) -> list[T]: ...

    def __getitem__(self, key: int | slice) -> T | list[T]:
        return self._list[key]


def load_py_file(path: Path, /) -> ModuleType:
    module_name = f'{path.parent.name}.{path.stem}'
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert(spec is not None)
    module = importlib.util.module_from_spec(spec)
    package_dir = str(path.parent.parent)
    sys.path.insert(0, package_dir)
    try:
        sys.modules[module_name] = module
        assert(spec.loader is not None)
        spec.loader.exec_module(module)
    finally:
        del sys.path[0]
    return module


def load_py_source(source: str) -> ModuleType:
    spec = importlib.util.spec_from_loader('magelang.dynamic.module', loader=None)
    assert(spec is not None)
    module = importlib.util.module_from_spec(spec)
    exec(source, module.__dict__)
    return module


ANSI_CLEAR_LINE = '\33[2K\r'


class Progress:

    def __init__(self, out: TextIO = sys.stderr) -> None:
        self.started = False
        self.out = out
        self._progress_text = ''

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False

    def replace_last_line(self, text: str) -> None:
        self.out.write(ANSI_CLEAR_LINE + '\r' + text)

    def _write_progress(self) -> None:
        assert(self.started)
        self.replace_last_line(self._progress_text)

    def status(self, text: str) -> None:
        assert(self.started)
        self._progress_text = text
        self._write_progress()

    def write_line(self, text: str) -> None:
        if self.started:
            self.replace_last_line(text)
            self.out.write('\n')
            self._write_progress()
        else:
            self.out.write(text + '\n')

    def finish(self, message: str) -> None:
        assert(self.started)
        self.stop()
        self.replace_last_line(message)
        self.out.write('\n')


class DynamicNode:

    def __init__(self, name: str, fields: Sequence[tuple[str, Any]]) -> None:
        self.name = name
        self.fields = fields
        self._mapping = {}
        for name, value in fields:
            self._mapping[name] = value

    def get_field(self, key: str) -> Any:
        return self._mapping[key]

    def offsets(self) -> Iterable[tuple[int, int]]:
        l = []
        def visit(x):
            if isinstance(x, DynamicNode):
                for _, value in x.fields:
                    visit(value)
            elif isinstance(x, DynamicToken):
                l.append(x.start)
                l.append(x.end)
            else:
                l.append(x)
        visit(self)
        return l

    def __repr__(self) -> str:
        return f'{self.name}({', '.join(f'{k}={repr(v)}' for k, v in self.fields)})'


class DynamicToken:

    def __init__(self, name: str, start: int, end: int) -> None:
        self.name = name
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f'{self.name}[{self.start}, {self.end}]'
