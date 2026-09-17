# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

from pathlib import Path

import pytest

from draft_release.extract_changes import extract_changes, main


def test_extract_changes(changelog_file: Path):
    assert extract_changes(changelog_file, "1.0.0") == "- feat: initial release\n"


def test_extract_changes_from_middle(changelog_file: Path):
    assert extract_changes(changelog_file, "Unreleased") == "- feat: new feature\n"


def test_extract_changes_keeps_inner_blank_lines(changelog_file: Path):
    changelog_file.write_text(
        "# CHANGELOG\n\n## 1.0.0 - 2026-01-01\n\n\n### Added\n\n- feat: a\n\n\n",
        encoding="utf-8",
    )
    assert extract_changes(changelog_file, "1.0.0") == "### Added\n\n- feat: a\n"


@pytest.mark.parametrize("version", ["1.0", "1.0.0.post0", "2.0.0"])
def test_extract_changes_unknown_version(changelog_file: Path, version: str):
    with pytest.raises(ValueError, match=f"No changes found for version {version}"):
        extract_changes(changelog_file, version)


def test_extract_changes_empty_section(changelog_file: Path):
    changelog_file.write_text(
        "# CHANGELOG\n\n## Unreleased\n\n## 1.0.0 - 2026-01-01\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="No changes found"):
        extract_changes(changelog_file, "Unreleased")


def test_main(changelog_file: Path, capsys: pytest.CaptureFixture[str]):
    main(["1.0.0", str(changelog_file)])
    assert capsys.readouterr().out == "- feat: initial release\n"
