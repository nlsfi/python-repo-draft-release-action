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
TITLE = "# CHANGELOG"


def _has_unreleased_header(text: str) -> bool:
    return any(line.startswith(UNRELEASED_HEADER) for line in text.splitlines())


def add_unreleased_header(changelog_file: Path) -> None:
    """Add an Unreleased header below the changelog title."""
    text = changelog_file.read_text(encoding="utf-8")
    if _has_unreleased_header(text):
        msg = f"{changelog_file.stem} already has a header '{UNRELEASED}'"
        raise ValueError(msg)
    if TITLE not in text:
        msg = f"{changelog_file.stem} is missing title '{TITLE}'"
        raise ValueError(msg)
    changelog_file.write_text(
        text.replace(TITLE, f"{TITLE}\n\n{UNRELEASED_HEADER}", 1), encoding="utf-8"
    )


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
