"""Minimal type-annotated function for HW1; no runtime dependencies."""

import math
from collections.abc import Sequence


def normalized_mean(values: Sequence[float]) -> float:
    """Return mean of finite numbers, clamped into [0, 1].

    This can be used as a tiny model-quality indicator. Invalid data
    is rejected instead of silently returning NaN.
    """
    if not values:
        raise ValueError("A non-empty sequence is required")
    if any(not math.isfinite(value) for value in values):
        raise ValueError("Scores must be finite")
    if any(not 0.0 <= value <= 1.0 for value in values):
        raise ValueError("Scores must be in [0, 1]")
    return sum(values) / len(values)
