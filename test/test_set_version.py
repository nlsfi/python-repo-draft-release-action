# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

from pathlib import Path

import pytest
from packaging.version import InvalidVersion, Version

from draft_release.get_version import get_version
from draft_release.set_version import main, set_version, validate_version


@pytest.mark.parametrize(
    "version", ["1.0.1", "1.1.0", "2.0.0", "1.0.0.post1", "1.0.0.dev20260101"]
)
def test_set_version(init_file: Path, version: str):
    assert set_version(init_file, version) == Version(version)
    assert get_version(init_file) == Version(version)


def test_set_version_keeps_other_content(init_file: Path):
    set_version(init_file, "1.1.0")
    assert (
        init_file.read_text(encoding="utf-8")
        == '"""Package."""\n\n__version__ = "1.1.0"\n'
    )


def test_set_version_normalizes_version(init_file: Path):
    set_version(init_file, "1.1.0-post0")
    assert '__version__ = "1.1.0.post0"' in init_file.read_text(encoding="utf-8")


@pytest.mark.parametrize("version", ["latest", "1.1.0.dev0.dev0"])
def test_set_version_invalid(init_file: Path, version: str):
    with pytest.raises(InvalidVersion):
        set_version(init_file, version)
    assert get_version(init_file) == Version("1.0.0.post0")


@pytest.mark.parametrize("version", ["1.0.0", "1.0.0.post0", "0.9.0"])
def test_set_version_not_higher(init_file: Path, version: str):
    with pytest.raises(ValueError, match="must be higher"):
        set_version(init_file, version)
    assert get_version(init_file) == Version("1.0.0.post0")


def test_set_version_dev_with_different_base(init_file: Path):
    with pytest.raises(ValueError, match="same base version"):
        set_version(init_file, "1.1.0.dev0")
    assert get_version(init_file) == Version("1.0.0.post0")


def test_set_version_without_version_line(init_file: Path):
    init_file.write_text("version = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="not in correct format"):
        set_version(init_file, "1.1.0")


@pytest.mark.parametrize(
    ("new_version", "current_version"),
    [
        ("1.0.1", "1.0.0"),
        ("1.0.0", "1.0.0.dev0"),
        ("1.0.0.post0", "1.0.0"),
        ("1.0.0.dev1", "1.0.0.dev0"),
        ("1.0.0.dev0", "1.0.0.post0"),
        ("1.0.0.dev0", "1.0.0rc1"),
    ],
)
def test_validate_version(new_version: str, current_version: str):
    validate_version(Version(new_version), Version(current_version))


@pytest.mark.parametrize(
    ("new_version", "current_version"),
    [
        ("1.0.0", "1.0.0"),
        ("1.0.0", "1.0.1"),
        ("1.0.0", "1.0.0.post0"),
        ("1.0.0rc1", "1.0.0"),
        ("1.0.1.dev0", "1.0.0"),
        ("1.0.0.dev0", "1.0.1.dev0"),
    ],
)
def test_validate_version_invalid(new_version: str, current_version: str):
    with pytest.raises(ValueError, match="must"):
        validate_version(Version(new_version), Version(current_version))


def test_main(init_file: Path):
    main([str(init_file), "1.1.0"])
    assert get_version(init_file) == Version("1.1.0")
