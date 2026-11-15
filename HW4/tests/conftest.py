"""Общие pytest-фикстуры для независимых тестов."""

from pathlib import Path

import pytest

from mlops_demo.data import Row
from scripts.generate_data import generate


@pytest.fixture
def rows() -> list[Row]:
    return [Row(-2, -1, 0), Row(-1, 0, 0), Row(1, 0, 1), Row(2, 1, 1)]


@pytest.fixture
def raw_csv(tmp_path: Path) -> Path:
    target = tmp_path / "raw.csv"
    generate(target, n=120)
    return target
