# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import shutil
import subprocess
import tomllib
from pathlib import Path

from packaging.version import Version

VERSION_PREFIX = "__version__ = "
PYPROJECT = "pyproject.toml"


def _find_version_line(init_file: Path) -> str:
    for line in init_file.read_text(encoding="utf-8").splitlines():
        if line.startswith(VERSION_PREFIX):
            return line
    msg = "Init file is not in correct format"
    raise ValueError(msg)


def _read_pyproject_version(pyproject_file: Path) -> Version:
    with pyproject_file.open("rb") as file:
        data = tomllib.load(file)
    try:
        return Version(data["project"]["version"])
    except KeyError as error:
        msg = f"{pyproject_file} is missing static [project] version"
        raise ValueError(msg) from error


def _write_pyproject_version(pyproject_file: Path, version: Version) -> None:
    uv = shutil.which("uv")
    if uv is None:
        msg = "uv is required to set the version in pyproject.toml"
        raise RuntimeError(msg)
    project_dir = pyproject_file.parent
    lock_mode = "--no-sync" if (project_dir / "uv.lock").exists() else "--frozen"
    subprocess.run(  # noqa: S603
        [uv, "version", "--project", str(project_dir), lock_mode, str(version)],
        check=True,
    )


def read_version(version_file: Path) -> Version:
    """Read the version from an init file or a pyproject.toml."""
    if version_file.name == PYPROJECT:
        return _read_pyproject_version(version_file)
    return Version(
        _find_version_line(version_file).removeprefix(VERSION_PREFIX).strip('"')
    )


def write_version(version_file: Path, version: Version) -> None:
    """Write the version to an init file or a pyproject.toml."""
    if version_file.name == PYPROJECT:
        _write_pyproject_version(version_file, version)
        return
    version_line = _find_version_line(version_file)
    version_file.write_text(
        version_file.read_text(encoding="utf-8").replace(
            version_line, f'{VERSION_PREFIX}"{version}"', 1
        ),
        encoding="utf-8",
    )
