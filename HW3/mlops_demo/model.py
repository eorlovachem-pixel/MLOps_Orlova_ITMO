"""Логистическая регрессия и аналитические градиенты BCE (без внешних зависимостей)."""

import math
from dataclasses import dataclass

from mlops_demo.data import Row


@dataclass
class LogisticModel:
    w1: float = 0.0
    w2: float = 0.0
    bias: float = 0.0

    def predict_proba(self, row: Row) -> float:
        score = self.w1 * row.x1 + self.w2 * row.x2 + self.bias
        # Устойчивая реализация сигмоиды при больших |score|.
        if score >= 0:
            return 1.0 / (1.0 + math.exp(-score))
        e = math.exp(score)
        return e / (1.0 + e)

    def predict(self, row: Row) -> int:
        return int(self.predict_proba(row) >= 0.5)

    def loss_and_grad(self, rows: list[Row]) -> tuple[float, float, float, float]:
        if not rows:
            raise ValueError("Пустой batch")
        loss = g1 = g2 = gb = 0.0
        for row in rows:
            p = self.predict_proba(row)
            safe = min(max(p, 1e-15), 1.0 - 1e-15)
            loss -= row.label * math.log(safe) + (1 - row.label) * math.log(1 - safe)
            residual = p - row.label
            g1 += residual * row.x1
            g2 += residual * row.x2
            gb += residual
        n = len(rows)
        return loss / n, g1 / n, g2 / n, gb / n
