#!/usr/bin/env python3

from functools import lru_cache
import sys
import subprocess
from pathlib import Path
from typing import Any, Literal
import shutil
from packaging.version import Version, parse as parse_version
import git

project_root = Path(__file__).parent.resolve()

repo = git.Repo(project_root)

def _ensure_package(name: str, install_with: str) -> None:
    import importlib
    try:
        importlib.import_module(name)
    except ImportError:
        print(f"Error: could not locate the '{name}' package. Ensure that it is installed with `python3 -m pip install --upgrade {install_with}`")
        sys.exit(1)

def _generate_internal(name: str, prefix: str, force: bool) -> int:

    import magelang

    files = magelang.generate_files(
        project_root / 'grammars' / (name + '.mage'),
        'python',
        prefix=prefix,
        enable_cst=True,
        enable_lexer=True,
        # enable_ast=True,
    )

    out_dir = project_root / 'src' / 'magelang' / 'lang' / name

    if not force:

        # Filter out those files that would lose changes when they are actually written.

        for path in _get_dirty():
            if _path_same_or_part_of(out_dir, path):
                rel_path = str(path.absolute().relative_to(out_dir))
                if rel_path in files:
                    del files[rel_path]
                    print(f"Not generating {path} because it has uncommitted changes on disk")

    # Write the files with force because even though Git might report the file
    # as unchanged, it still takes up space on disk.
    magelang.write_files(files, dest_dir=out_dir, force=True)

    return 0

def generate(*, next: bool = False, force: bool = False) -> int:
    src_dir = project_root / ('src' if next else 'pkg/stable')
    sys.path.insert(0, str(src_dir))
    _generate_internal('mage', 'mage', force=force)
    # _generate_checked('treespec', force=force)
    _generate_internal('python', 'py', force=force)
    return 0

@lru_cache
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

def _path_same_or_part_of(root: Path, child: Path) -> bool:
    return root == child or root.absolute() in child.absolute().parents

@lru_cache
def _get_dirty() -> set[Path]:
    return set(Path(entry.a_path) for entry in repo.index.diff(None) if not Path(entry.a_path).is_dir())

def bump(
    major: bool = False,
    minor: bool = False,
    micro: bool = False,
    dev: bool = False,
    force: bool = False
) -> int:

    import toml

    none = not (major or minor or micro or dev)

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

    new_version = _build_version(v_maj, v_min, v_micro, v_dev)

    dirty = _get_dirty()

    if not force and Path('pyproject.toml') in dirty:
        print(f"Error: action would overwrite changes in pyproject.toml. Please discard these changes before continuing or use --force.")
        return 1

    # Overwrite pyproject.toml with the bumped version number
    pyproject_toml['project']['version'] = new_version
    with open(project_root / 'pyproject.toml', 'w') as f:
        f.write('# This file is programmatically overwritten. Do not attempt to format or add comments.\n')
        toml.dump(pyproject_toml, f)

    return 0

type PackageType = Literal['stable', 'nightly']

def build() -> int:

    version = _get_version()

    # Infer whether this is a stable or nightly package
    mode = 'stable' if version.dev is None else 'nightly'

    print(f'Now building {mode} package for {version}')

    # This lists all the files that will be made available for packaging
    include = [ 'src', 'pyproject.toml', 'README.md', 'LICENSE.txt', 'Dockerfile' ]

    include = list(Path(fname) for fname in include)
    out_dir = project_root / 'pkg' / mode

    # Scan for files that need to be published
    to_copy = set[Path]()
    for entry in repo.commit().tree.traverse():
        child = Path(entry.path) # type: ignore
        print(child, any(_path_same_or_part_of(root, child) for root in include))
        if not child.is_dir() and any(_path_same_or_part_of(root, child) for root in include):
            to_copy.add(child)

    # Check whether there are unstaged changes on these scanned files
    dirty = _get_dirty()
    if any(path in dirty for path in to_copy):
        print(f'Error: trying to build a package from files that have uncommitted changes')
        return 1

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

    _ensure_package('build', install_with='build')

    from build import ProjectBuilder

    builder = ProjectBuilder(out_dir)
    builder.build('sdist', out_dir / 'dist')
    builder.build('wheel', out_dir / 'dist')

    return 0

def test(mode: PackageType | None = None) -> int:
    if mode is None:
        import pytest
        return pytest.main([ 'src/magelang' ])
    else:
        out_dir = project_root / 'pkg' / mode
        container_name = f'magelang-{mode}'
        subprocess.run([ 'docker', 'build', '.', '-t', container_name ], cwd=out_dir, check=True)
        subprocess.run([ 'docker', 'run', '--entrypoint', 'pytest', '-it', container_name, '--pyargs', 'magelang' ], check=True)
        subprocess.run([ 'docker', 'run', '-it', container_name, 'help'  ], check=True)
    return 0

def commit(force: bool = False) -> int:
    if not force and len(repo.index.diff('HEAD')):
        print(f'Error: in order to commit the new version the staging area must be clean or use --force if you know what you are doing')
        return 1
    version = _get_version()
    repo.index.add('pyproject.toml')
    repo.index.add('pkg/stable')
    repo.index.commit(f'Bump stable version to {version}')
    return 0

def publish(testing: bool = False) -> int:

    version = _get_version()

    # Infer whether this is a stable or nightly package
    mode = 'stable' if version.dev is None else 'nightly'

    out_dir = project_root / 'pkg' / mode

    dist_paths = list(str(path) for path in (out_dir / 'dist').iterdir())

    _ensure_package('twine', install_with='twine')

    from twine.commands.upload import upload as twine_upload
    from twine.settings import Settings

    repo_name = 'testpypi' if testing else 'pypi'
    twine_upload(Settings(repository_name=repo_name), dist_paths)

    return 0

if __name__ == '__main__':
    from magelang.cli import run
    sys.exit(run(__name__))
