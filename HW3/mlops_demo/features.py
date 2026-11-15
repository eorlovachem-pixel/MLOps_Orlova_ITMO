"""Изолированный блок стандартизации с явным fit/transform."""

import math
from dataclasses import dataclass
from typing import Self

from mlops_demo.data import Row


@dataclass(frozen=True)
class Standardizer:
    mean: tuple[float, float]
    scale: tuple[float, float]

    @classmethod
    def fit(cls, rows: list[Row]) -> Self:
        if not rows:
            raise ValueError("Нельзя подобрать стандартизацию на пустой выборке")
        n = len(rows)
        mu1 = sum(row.x1 for row in rows) / n
        mu2 = sum(row.x2 for row in rows) / n
        sd1 = math.sqrt(sum((row.x1 - mu1) ** 2 for row in rows) / n)
        sd2 = math.sqrt(sum((row.x2 - mu2) ** 2 for row in rows) / n)
        # Константный столбец не приводит к делению на нуль.
        return cls((mu1, mu2), (sd1 if sd1 > 1e-12 else 1.0, sd2 if sd2 > 1e-12 else 1.0))

    def transform(self, row: Row) -> Row:
        return Row(
            x1=(row.x1 - self.mean[0]) / self.scale[0],
            x2=(row.x2 - self.mean[1]) / self.scale[1],
            label=row.label,
        )

    def transform_many(self, rows: list[Row]) -> list[Row]:
        return [self.transform(row) for row in rows]
