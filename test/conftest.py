# Copyright (c) 2026 National Land Survey of Finland
# (https://www.maanmittauslaitos.fi/en).
# This file is part of the Pinta.
# Licensed under the MIT License; see the repository LICENSE file.

from pathlib import Path

import pytest

CHANGELOG = """# CHANGELOG

## Unreleased

- feat: new feature

## 1.0.0 - 2026-01-01

- feat: initial release
"""


@pytest.fixture
def init_file(tmp_path: Path) -> Path:
    file = tmp_path / "__init__.py"
    file.write_text('"""Package."""\n\n__version__ = "1.0.0.post0"\n', encoding="utf-8")
    return file


@pytest.fixture
def changelog_file(tmp_path: Path) -> Path:
    file = tmp_path / "CHANGELOG.md"
    file.write_text(CHANGELOG, encoding="utf-8")
    return file
