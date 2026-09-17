# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from packaging.version import Version

from draft_release._version_file import read_version


def get_version(version_file: Path) -> Version:
    """Return the version defined in the given init file or pyproject.toml."""
    return read_version(version_file)


def main(argv: Sequence[str] | None = None) -> None:
    """Print the version defined in the given init file or pyproject.toml."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("version_file", type=Path)
    args = parser.parse_args(argv)
    sys.stdout.write(str(get_version(args.version_file)))


if __name__ == "__main__":
    main()
