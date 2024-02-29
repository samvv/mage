
from typing import TypeVar


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

