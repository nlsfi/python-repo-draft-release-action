# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import pytest
from packaging.version import InvalidVersion

from draft_release.parse_version import main, parse_version


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("1.0.0", "1.0.0"),
        ("1.0.0.post0", "1.0.0.post0"),
        ("1.0.0-post0", "1.0.0.post0"),
        ("1.0.0.dev20260101", "1.0.0.dev20260101"),
        ("v1.0.0-RC1", "1.0.0rc1"),
    ],
)
def test_parse_version(version: str, expected: str):
    assert parse_version(version) == expected


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("1.0.0", "1.0.0"),
        ("1.0.0.post0", "1.0.0"),
        ("1.0.0.dev20260101", "1.0.0"),
        ("1.0.0rc1", "1.0.0"),
    ],
)
def test_parse_version_base(version: str, expected: str):
    assert parse_version(version, base=True) == expected


def test_parse_version_invalid():
    with pytest.raises(InvalidVersion):
        parse_version("latest")


def test_main(capsys: pytest.CaptureFixture[str]):
    main(["1.0.0-post0"])
    assert capsys.readouterr().out == "1.0.0.post0"


def test_main_base(capsys: pytest.CaptureFixture[str]):
    main(["1.0.0.post0", "base"])
    assert capsys.readouterr().out == "1.0.0"


def test_main_invalid_mode():
    with pytest.raises(SystemExit):
        main(["1.0.0", "foo"])
