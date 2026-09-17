# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import shutil
import subprocess
from pathlib import Path

import pytest
from packaging.version import InvalidVersion, Version
from pytest_mock import MockerFixture, MockType

from draft_release._version_file import read_version, write_version
from draft_release.get_version import get_version
from draft_release.set_version import set_version

PYPROJECT = """[project]
name = "demo"
version = "1.0.0.post0"  # keep
requires-python = ">=3.12"
dependencies = []
"""


@pytest.fixture
def pyproject_file(tmp_path: Path) -> Path:
    file = tmp_path / "pyproject.toml"
    file.write_text(PYPROJECT, encoding="utf-8")
    return file


@pytest.fixture
def uv_run(mocker: MockerFixture) -> MockType:
    mocker.patch("draft_release._version_file.shutil.which", return_value="/bin/uv")
    return mocker.patch("draft_release._version_file.subprocess.run")


def test_read_pyproject_version(pyproject_file: Path):
    assert read_version(pyproject_file) == Version("1.0.0.post0")


@pytest.mark.parametrize(
    "content",
    ['[project]\nname = "demo"\ndynamic = ["version"]\n', '[tool.uv]\nfoo = "bar"\n'],
)
def test_read_pyproject_version_missing(pyproject_file: Path, content: str):
    pyproject_file.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError, match="missing static \\[project\\] version"):
        read_version(pyproject_file)


def test_read_pyproject_version_invalid(pyproject_file: Path):
    pyproject_file.write_text('[project]\nversion = "latest"\n', encoding="utf-8")
    with pytest.raises(InvalidVersion):
        read_version(pyproject_file)


def test_write_pyproject_version_without_lock(pyproject_file: Path, uv_run: MockType):
    write_version(pyproject_file, Version("1.1.0"))
    uv_run.assert_called_once_with(
        [
            "/bin/uv",
            "version",
            "--project",
            str(pyproject_file.parent),
            "--frozen",
            "1.1.0",
        ],
        check=True,
    )


def test_write_pyproject_version_with_lock(pyproject_file: Path, uv_run: MockType):
    (pyproject_file.parent / "uv.lock").touch()
    write_version(pyproject_file, Version("1.1.0"))
    uv_run.assert_called_once_with(
        [
            "/bin/uv",
            "version",
            "--project",
            str(pyproject_file.parent),
            "--no-sync",
            "1.1.0",
        ],
        check=True,
    )


def test_write_pyproject_version_without_uv(
    pyproject_file: Path, mocker: MockerFixture
):
    mocker.patch("draft_release._version_file.shutil.which", return_value=None)
    with pytest.raises(RuntimeError, match="uv is required"):
        write_version(pyproject_file, Version("1.1.0"))


def test_write_pyproject_version_uv_failure(pyproject_file: Path, uv_run: MockType):
    uv_run.side_effect = subprocess.CalledProcessError(2, "uv")
    with pytest.raises(subprocess.CalledProcessError):
        write_version(pyproject_file, Version("1.1.0"))


def test_set_version_pyproject_validates_before_writing(
    pyproject_file: Path, uv_run: MockType
):
    with pytest.raises(ValueError, match="must be higher"):
        set_version(pyproject_file, "0.9.0")
    uv_run.assert_not_called()


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not installed")
def test_set_version_pyproject_with_uv(
    pyproject_file: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    assert set_version(pyproject_file, "1.1.0") == Version("1.1.0")
    assert pyproject_file.read_text(encoding="utf-8") == PYPROJECT.replace(
        "1.0.0.post0", "1.1.0"
    )
    assert not (pyproject_file.parent / "uv.lock").exists()
    assert get_version(pyproject_file) == Version("1.1.0")


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not installed")
def test_set_version_pyproject_updates_lock(
    pyproject_file: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    subprocess.run(["uv", "lock", "--project", pyproject_file.parent], check=True)
    set_version(pyproject_file, "1.1.0")
    lock = (pyproject_file.parent / "uv.lock").read_text(encoding="utf-8")
    assert 'name = "demo"\nversion = "1.1.0"' in lock
    assert not (pyproject_file.parent / ".venv").exists()
