#!/usr/bin/env python3

from collections.abc import Callable
import sys
import subprocess
from pathlib import Path
from typing import Any, Iterable, TypeVar
import shutil
from packaging.version import Version, parse as parse_version
import git

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

def _get_pyproject_toml() -> dict[str, Any]:
    import toml
    return toml.load(project_root / 'pyproject.toml')

def _get_version() -> Version:
    toml = _get_pyproject_toml()
    return parse_version(toml['project']['version'])

def _build_version(major: int, minor: int, micro: int, dev: int | None) -> str:
    out = f'{major}.{minor}.{micro}'
    if dev is not None:
        out += f'.dev{dev}'
    return out

def _path_part_of(root: Path, child: Path) -> bool:
    return root.absolute() in child.absolute().parents

def _git_list_files_in_dir(repo: git.Repo, root: Path) -> Iterable[Path]:
    for entry in repo.commit().tree.traverse():
        path = Path(entry.path) # type: ignore
        if not path.is_dir() and _path_part_of(root, path):
            yield path

def bump(
    major: bool = False,
    minor: bool = False,
    micro: bool = False,
    dev: bool = False,
    commit: bool = True,
    test_upload: bool = False,
    upload: bool = True
) -> int:

    import toml

    # none = not (major or minor or patch or dev)

    pyproject_toml = _get_pyproject_toml()

    old_version = parse_version(pyproject_toml['project']['version'])
    v_maj = old_version.major
    v_min = old_version.minor
    v_micro = old_version.micro
    v_dev = old_version.dev

    # Increment version components
    if major:
        v_maj += 1
        v_dev = None
    if minor:
        v_min += 1
        v_dev = None
    if micro:
        v_micro += 1
        v_dev = None
    if dev:
        v_dev = 0 if v_dev is None else v_dev + 1

    # Infer whether this is a stable or nightly package
    mode = 'stable' if v_dev is None else 'nightly'

    new_version = _build_version(v_maj, v_min, v_micro, v_dev)

    # This lists all the files that will be added to the package
    files = [ 'src', 'pyproject.toml', 'README.md', 'LICENSE.txt' ]

    files = list(Path(fname) for fname in files)
    out_dir = project_root / 'pkg' / mode

    repo = git.Repo(project_root)

    # Check whether there are unstaged changes on these scanned files
    dirty = set[Path]()
    for entry in repo.index.diff(None):
        path = Path(entry.a_path)
        for other in files:
            if _path_part_of(other, path):
                dirty.add(path)

    if mode == 'stable' and repo.is_dirty():
        print(f'Error: in order to commit the new version the repository must be clean')
        return 1

    if 'pyproject.toml' in dirty:
        print(f"Error: action would overwrite changes in pyproject.toml. Please discard these changes before continuing.")
        return 1

    # Scan for files that need to be published
    to_copy = set[Path]()
    for path in files:
        if path.is_dir():
            to_copy.update(_git_list_files_in_dir(repo, path))
        else:
            to_copy.add(path)

    if dirty:
        print(f"Error: there are unsaved changes:")
        for path in dirty:
            print(f' - {path}')
        return 1

    # At this point all pre-flight checks have been performed

    print(f'Now building {mode} package for {new_version}')

    # Overwrite pyproject.toml with the bumped version number
    pyproject_toml['project']['version'] = new_version
    with open(project_root / 'pyproject.toml', 'w') as f:
        f.write('# This file is programmatically overwritten. Do not attempt to format or add comments.\n')
        toml.dump(pyproject_toml, f)

    # Start with a fresh slate in the package directory
    # These files should be tracked by Git so it is not dangerous to remove then
    shutil.rmtree(out_dir, ignore_errors=True)

    # Copy the actual files
    print('Copying files ...')
    for path in sorted(to_copy):
        new_path = out_dir / path
        new_path.parent.mkdir(parents=True, exist_ok=True)
        print(f' - {path}')
        shutil.copy(path, new_path)

    if not commit:
        return 0

    if mode == 'stable':
        repo.index.add('pkg/stable')
        repo.index.commit(f'Bump stable version to {new_version}')

    if not upload:
        return 0

    try:
        from build import ProjectBuilder
    except ImportError:
        print(f"Error: could not locate the 'build' package. Ensure that it is installed with `python3 -m pip install --upgrade build`")
        return 1

    try:
        from twine.commands.upload import upload as twine_upload
        from twine.settings import Settings
    except ImportError:
        print(f"Error: could not locate the 'twine' package. Ensure that it is installed with `python3 -m pip install --upgrade twine`")
        return 1

    builder = ProjectBuilder(out_dir)
    dist_path = builder.build('wheel', out_dir / 'dist')
    repo_name = 'testpypi' if test_upload else 'pypi'
    twine_upload(Settings(repository_name=repo_name), [ dist_path ])

    return 0

def test() -> int:
    import pytest
    return pytest.main([ 'src/magelang' ])

if __name__ == '__main__':
    from magelang.cli import run
    sys.exit(run(__name__))
