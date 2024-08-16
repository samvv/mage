
import importlib
from pathlib import Path
from typing import Protocol

from magelang.ast import Grammar
from magelang.util import Files

here = Path(__file__).parent.resolve()

class _GenerateFn(Protocol):

    def __call__(
        self,
        grammar: Grammar,
        prefix: str = '',
        cst_parent_pointers: bool = False,
        debug: bool = False,
    ) -> Files: ...

_generate_by_language: dict[str, _GenerateFn] = {}

for fname in here.iterdir():
    if (fname / '__init__.py').exists():
        name = fname.stem
        _generate_by_language[name] = importlib.import_module(f'magelang.generator.{name}').generate

def get_generator_languages() -> list[str]:
    return list(_generate_by_language.keys())

def generate(
    grammar: Grammar,
    lang: str,
    prefix: str = '',
    cst_parent_pointers: bool = False,
    debug: bool = False,
) -> Files:
    generate = _generate_by_language[lang]
    return generate(grammar, prefix=prefix, cst_parent_pointers=cst_parent_pointers, debug=debug)

