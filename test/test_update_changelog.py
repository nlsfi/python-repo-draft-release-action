# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from conftest import CHANGELOG
from pytest_mock import MockerFixture

from draft_release.update_changelog import main, update_changelog


@pytest.fixture(autouse=True)
def now(mocker: MockerFixture) -> datetime:
    now = datetime(2026, 9, 17, 23, 30, tzinfo=ZoneInfo("Europe/Helsinki"))
    mocker.patch("draft_release.update_changelog.datetime").now.return_value = now
    return now


def test_release(changelog_file: Path):
    update_changelog(changelog_file, "1.1.0")
    assert changelog_file.read_text(encoding="utf-8") == CHANGELOG.replace(
        "## Unreleased", "## 1.1.0 - 2026-09-17"
    )


def test_release_uses_helsinki_date(changelog_file: Path, mocker: MockerFixture):
    mock = mocker.patch("draft_release.update_changelog.datetime")
    mock.now.return_value = datetime(2026, 9, 17, 23, 30, tzinfo=ZoneInfo("UTC"))
    update_changelog(changelog_file, "1.1.0")
    mock.now.assert_called_once_with(ZoneInfo("Europe/Helsinki"))


def test_release_without_unreleased_header(changelog_file: Path):
    changelog_file.write_text(
        "# CHANGELOG\n\n## 1.0.0 - 2026-01-01\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="missing header 'Unreleased'"):
        update_changelog(changelog_file, "1.1.0")


def test_release_ignores_unreleased_mentions_in_content(changelog_file: Path):
    changelog_file.write_text(
        "# CHANGELOG\n\n## 1.0.0 - 2026-01-01\n\n- fix: Unreleased thing\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="missing header 'Unreleased'"):
        update_changelog(changelog_file, "1.1.0")


def test_add_unreleased_header(changelog_file: Path):
    update_changelog(changelog_file, "1.1.0")
    update_changelog(changelog_file, "Unreleased")
    assert changelog_file.read_text(encoding="utf-8") == CHANGELOG.replace(
        "## Unreleased", "## Unreleased\n\n## 1.1.0 - 2026-09-17"
    )


def test_add_unreleased_header_when_already_present(changelog_file: Path):
    with pytest.raises(ValueError, match="already has a header 'Unreleased'"):
        update_changelog(changelog_file, "Unreleased")
    assert changelog_file.read_text(encoding="utf-8") == CHANGELOG


def test_add_unreleased_header_without_title(changelog_file: Path):
    changelog_file.write_text(
        "# Changelog\n\n## 1.0.0 - 2026-01-01\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="missing title '# CHANGELOG'"):
        update_changelog(changelog_file, "Unreleased")


def test_main(changelog_file: Path):
    main(["1.1.0", str(changelog_file)])
    assert "## 1.1.0 - 2026-09-17" in changelog_file.read_text(encoding="utf-8")


def test_main_default_changelog_file(
    changelog_file: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.chdir(changelog_file.parent)
    main(["1.1.0"])
    assert "## 1.1.0 - 2026-09-17" in changelog_file.read_text(encoding="utf-8")
