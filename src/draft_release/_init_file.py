# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

from pathlib import Path

from packaging.version import Version

VERSION_PREFIX = "__version__ = "


def find_version_line(init_file: Path) -> str:
    for line in init_file.read_text(encoding="utf-8").splitlines():
        if line.startswith(VERSION_PREFIX):
            return line
    msg = "Init file is not in correct format"
    raise ValueError(msg)


def parse_version_line(line: str) -> Version:
    return Version(line.removeprefix(VERSION_PREFIX).strip('"'))


def read_version(init_file: Path) -> Version:
    return parse_version_line(find_version_line(init_file))
