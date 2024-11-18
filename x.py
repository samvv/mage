#!/usr/bin/env python3

from collections.abc import Callable
import sys
import subprocess
from pathlib import Path
from typing import TypeVar

project_root = Path(__file__).parent.resolve()
lang_dir = project_root / 'src' / 'magelang' / 'lang'

_T = TypeVar('_T')
_R = TypeVar('_R')
_V = TypeVar('_V')

def _map_keys(mapping: dict[_T, _V], proc: Callable[[_T], _R]) -> dict[_R, _V]:
    out = {}
    for key, value in mapping.items():
        out[proc(key)] = value
    return out

def main() -> int:

    import magelang

    files = magelang.generate_files(
        'grammars/python.mage',
        'python',
        prefix='py',
        enable_cst=True,
        enable_ast=True,
    )

    files = _map_keys(files, lambda fname: str((lang_dir / 'python' / fname).resolve()))

    output_modified = False
    result = subprocess.run('git status --porcelain=v1', stdout=subprocess.PIPE, check=True, shell=True)
    for line in result.stdout.decode('utf-8').splitlines():
        state = line[:2].strip()
        path = str((project_root / line[3:]).resolve())
        if path in files:
            del files[path]
            print(f"Not generating {path} because it has local changes on disk")
            output_modified = True

    magelang.write_files(files, dest_dir=project_root, force=True)

    return 0

if __name__ == '__main__':
    sys.exit(main())
