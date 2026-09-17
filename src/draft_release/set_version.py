# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import argparse
from collections.abc import Sequence
from pathlib import Path

from packaging.version import Version

from draft_release._init_file import find_version_line, parse_version_line


def validate_version(new_version: Version, current_version: Version) -> None:
    """Raise ValueError if the new version is not allowed after the current one."""
    if new_version.is_devrelease:
        if Version(new_version.base_version) != Version(current_version.base_version):
            msg = (
                f"New dev version {new_version} must always have the same base "
                f"version than the current version ({current_version})"
            )
            raise ValueError(msg)
    elif new_version <= current_version:
        msg = (
            f"Version {new_version} must be higher than "
            f"the current version ({current_version})"
        )
        raise ValueError(msg)


def set_version(init_file: Path, version: str) -> Version:
    """Set the version in the given init file and return it."""
    new_version = Version(version)
    version_line = find_version_line(init_file)
    validate_version(new_version, parse_version_line(version_line))
    init_file.write_text(
        init_file.read_text(encoding="utf-8").replace(
            version_line, f'__version__ = "{new_version}"', 1
        ),
        encoding="utf-8",
    )
    return new_version


def main(argv: Sequence[str] | None = None) -> None:
    """Set the version in the given init file."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("init_file", type=Path)
    parser.add_argument("version")
    args = parser.parse_args(argv)
    set_version(args.init_file, args.version)


if __name__ == "__main__":
    main()
