
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

