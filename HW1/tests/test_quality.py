"""Checks for the tiny example function."""

import pytest

from quality import normalized_mean


def test_mean() -> None:
    assert normalized_mean([0.2, 0.4, 0.6]) == pytest.approx(0.4)


@pytest.mark.parametrize("scores", [[], [float("nan")], [1.5], [-0.01]])
def test_invalid_scores(scores: list[float]) -> None:
    with pytest.raises(ValueError):
        normalized_mean(scores)
