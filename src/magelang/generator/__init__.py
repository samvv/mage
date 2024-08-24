
import importlib
from pathlib import Path
from typing import Any

from magelang.ast import Grammar
from magelang.util import Files

here = Path(__file__).parent.resolve()

_generate_by_language: dict[str, Any] = {}

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
    enable_ast = False,
    enable_cst = False,
    enable_visitor = False,
    enable_lexer = False,
    enable_emitter = False,
) -> Files:
    generate = _generate_by_language[lang]
    return generate(
        grammar,
        prefix=prefix,
        cst_parent_pointers=cst_parent_pointers,
        debug=debug,
        enable_ast=enable_ast,
        enable_cst=enable_cst,
        enable_lexer=enable_lexer,
        enable_visitor=enable_visitor,
        enable_emitter=enable_emitter
    )

