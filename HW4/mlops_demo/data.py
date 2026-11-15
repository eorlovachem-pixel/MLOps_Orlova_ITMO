"""Даталоадер CSV и разделение train/test без утечки данных."""

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Row:
    x1: float
    x2: float
    label: int


def read_csv(path: Path) -> list[Row]:
    """Строго проверить схему и значения синтетического датасета."""
    if not path.is_file():
        raise FileNotFoundError(f"Не найден CSV: {path}")
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["x1", "x2", "label"]:
            raise ValueError("Ожидаемые столбцы в точном порядке: x1,x2,label")
        rows: list[Row] = []
        for line, record in enumerate(reader, start=2):
            try:
                x1 = float(record["x1"])
                x2 = float(record["x2"])
                label = int(record["label"])
            except (ValueError, KeyError, TypeError) as error:
                raise ValueError(f"Некорректные данные в строке {line}") from error
            if not math.isfinite(x1) or not math.isfinite(x2):
                raise ValueError(f"Не конечный признак в строке {line}")
            if label not in (0, 1):
                raise ValueError(f"Метка должна быть 0 или 1, строка {line}")
            rows.append(Row(x1=x1, x2=x2, label=label))
    if len(rows) < 4:
        raise ValueError("Для train/test требуется минимум четыре записи")
    return rows


def split_rows(rows: list[Row], *, test_ratio: float, seed: int) -> tuple[list[Row], list[Row]]:
    """Стабильно перемешать без изменения исходного списка и разрезать на две части."""
    if not 0.0 < test_ratio < 1.0:
        raise ValueError("test_ratio должен принадлежать интервалу (0, 1)")
    if len(rows) < 4:
        raise ValueError("Слишком мало наблюдений")
    shuffled = rows.copy()
    random.Random(seed).shuffle(shuffled)
    test_size = max(1, min(len(rows) - 1, round(len(rows) * test_ratio)))
    return shuffled[test_size:], shuffled[:test_size]
