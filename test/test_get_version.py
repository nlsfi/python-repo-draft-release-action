# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

import sys
from pathlib import Path

import pytest
from packaging.version import InvalidVersion, Version
from pytest_mock import MockerFixture

from draft_release.get_version import get_version, main


def test_get_version(init_file: Path):
    assert get_version(init_file) == Version("1.0.0.post0")


def test_get_version_normalizes_version(init_file: Path):
    init_file.write_text('__version__ = "1.0.0-post0"\n', encoding="utf-8")
    assert str(get_version(init_file)) == "1.0.0.post0"


def test_get_version_without_version_line(init_file: Path):
    init_file.write_text("version = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="not in correct format"):
        get_version(init_file)


def test_get_version_with_invalid_version(init_file: Path):
    init_file.write_text('__version__ = "latest"\n', encoding="utf-8")
    with pytest.raises(InvalidVersion):
        get_version(init_file)


def test_main(init_file: Path, capsys: pytest.CaptureFixture[str]):
    main([str(init_file)])
    assert capsys.readouterr().out == "1.0.0.post0"


def test_main_uses_sys_argv(
    init_file: Path, capsys: pytest.CaptureFixture[str], mocker: MockerFixture
):
    mocker.patch.object(sys, "argv", ["get_version.py", str(init_file)])
    main()
    assert capsys.readouterr().out == "1.0.0.post0"
