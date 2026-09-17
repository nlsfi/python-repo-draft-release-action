# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path


def extract_changes(changelog_file: Path, version: str) -> str:
    """Return the changelog section of the given version."""
    header = f"## {version}"
    found = False
    lines: list[str] = []
    for line in changelog_file.read_text(encoding="utf-8").splitlines():
        if found and line.startswith("## "):
            break
        if found:
            lines.append(line)
        elif line == header or line.startswith(f"{header} "):
            found = True
    changes = "\n".join(lines).strip("\n")
    if not changes:
        msg = f"No changes found for version {version}"
        raise ValueError(msg)
    return changes + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    """Print the changelog section of the given version."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("version")
    parser.add_argument("changelog_file", nargs="?", type=Path, default="CHANGELOG.md")
    args = parser.parse_args(argv)
    sys.stdout.write(extract_changes(args.changelog_file, args.version))


if __name__ == "__main__":
    main()
