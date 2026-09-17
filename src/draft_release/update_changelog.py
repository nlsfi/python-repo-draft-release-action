# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import argparse
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

UNRELEASED = "Unreleased"
UNRELEASED_HEADER = f"## {UNRELEASED}"


def _has_unreleased_header(text: str) -> bool:
    return any(line.startswith(UNRELEASED_HEADER) for line in text.splitlines())


def _unreleased_header_index(lines: list[str]) -> int:
    """Return the line index where the Unreleased header should be inserted.

    The header goes before the first version section, or after the title
    if the changelog has no sections yet.
    """
    for index, line in enumerate(lines):
        if line.startswith("## "):
            return index
    for index, line in enumerate(lines):
        if line.startswith("# "):
            return index + 1
    msg = "Changelog is missing a title or a version section"
    raise ValueError(msg)


def add_unreleased_header(changelog_file: Path) -> None:
    """Add an Unreleased header before the first version section."""
    text = changelog_file.read_text(encoding="utf-8")
    if _has_unreleased_header(text):
        msg = f"{changelog_file.stem} already has a header '{UNRELEASED}'"
        raise ValueError(msg)
    lines = text.splitlines(keepends=True)
    index = _unreleased_header_index(lines)
    lines.insert(index, f"{UNRELEASED_HEADER}\n\n")
    if index > 0 and lines[index - 1].strip():
        lines.insert(index, "\n")
    changelog_file.write_text("".join(lines), encoding="utf-8")


def release_unreleased_header(changelog_file: Path, version: str) -> None:
    """Replace the Unreleased header with a versioned and dated header."""
    text = changelog_file.read_text(encoding="utf-8")
    if not _has_unreleased_header(text):
        msg = f"{changelog_file.stem} is missing header '{UNRELEASED}'"
        raise ValueError(msg)
    timestamp = datetime.now(ZoneInfo("Europe/Helsinki")).date().isoformat()
    changelog_file.write_text(
        text.replace(UNRELEASED_HEADER, f"## {version} - {timestamp}", 1),
        encoding="utf-8",
    )


def update_changelog(changelog_file: Path, version: str) -> None:
    """Add an Unreleased header or release it as the given version."""
    if version == UNRELEASED:
        add_unreleased_header(changelog_file)
    else:
        release_unreleased_header(changelog_file, version)


def main(argv: Sequence[str] | None = None) -> None:
    """Replace the Unreleased header with a version or add a new Unreleased header."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("version", help=f"Version or '{UNRELEASED}'")
    parser.add_argument("changelog_file", nargs="?", type=Path, default="CHANGELOG.md")
    args = parser.parse_args(argv)
    update_changelog(args.changelog_file, args.version)


if __name__ == "__main__":
    main()
