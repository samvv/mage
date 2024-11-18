#!/usr/bin/env python3

from collections.abc import Callable
import sys
import subprocess
from pathlib import Path
from typing import TypeVar

project_root = Path(__file__).parent.resolve()

_T = TypeVar('_T')
_R = TypeVar('_R')
_V = TypeVar('_V')

def _map_keys(mapping: dict[_T, _V], proc: Callable[[_T], _R]) -> dict[_R, _V]:
    out = {}
    for key, value in mapping.items():
        out[proc(key)] = value
    return out

def _generate_internal(name: str, force: bool) -> int:

    import magelang

    files = magelang.generate_files(
        project_root / 'grammars' / (name + '.mage'),
        'python',
        prefix='py',
        enable_cst=True,
        # enable_ast=True,
    )

    files = _map_keys(files, lambda fname: f'src/magelang/lang/{name}/{fname}')

    if not force:

        # Filter out those files that would lose changes when they are actually written.

        result = subprocess.run('git status --porcelain=v1', stdout=subprocess.PIPE, check=True, shell=True)
        for line in result.stdout.decode('utf-8').splitlines():
            state = line[:2].strip()
            path = line[3:]
            if path in files:
                del files[path]
                print(f"Not generating {path} because it has uncommitted changes on disk")

    # Write the files with force because even though Git might report the file
    # as unchanged, it still takes up space on disk.
    magelang.write_files(files, dest_dir=project_root, force=True)

    return 0

def generate(next: bool = False, force: bool = False) -> int:
    print(force)
    src_dir = project_root / ('src' if next else 'lkg')
    sys.path.insert(0, str(src_dir))
    _generate_internal('mage', force=force)
    # _generate_checked('treespec', force=force)
    _generate_internal('python', force=force)
    return 0

def test() -> int:
    import pytest
    return pytest.main([ 'src/magelang' ])

if __name__ == '__main__':
    from magelang.cli import run
    sys.exit(run(__name__))
