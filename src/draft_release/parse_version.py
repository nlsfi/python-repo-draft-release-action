# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import argparse
import sys
from collections.abc import Sequence

from packaging.version import Version


def parse_version(version: str, *, base: bool = False) -> str:
    """Return the normalized form or the base version of the given version."""
    parsed = Version(version)
    return parsed.base_version if base else str(parsed)


def main(argv: Sequence[str] | None = None) -> None:
    """Print the normalized form or the base version of the given version."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("version")
    parser.add_argument("mode", nargs="?", choices=["base"])
    args = parser.parse_args(argv)
    sys.stdout.write(parse_version(args.version, base=args.mode == "base"))


if __name__ == "__main__":
    main()
