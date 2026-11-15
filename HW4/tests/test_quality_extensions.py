"""Extra edge cases and gradient correctness checks for HW4."""

import math

import pytest

from mlops_demo.data import Row, split_rows
from mlops_demo.features import Standardizer
from mlops_demo.model import LogisticModel
from mlops_demo.training import fit


@pytest.mark.unit
def test_split_never_changes_input_order() -> None:
    original = [Row(float(i), float(-i), i % 2) for i in range(20)]
    snapshot = original.copy()
    train, test = split_rows(original, test_ratio=0.25, seed=17)
    assert original == snapshot
    assert len(train) + len(test) == len(original)
    assert not set(map(id, train)) & set(map(id, test))


@pytest.mark.unit
def test_constant_feature_standardization_is_finite() -> None:
    points = [Row(1.0, 3.0, 0), Row(1.0, 5.0, 1)]
    scaler = Standardizer.fit(points)
    actual = scaler.transform_many(points)
    assert all(math.isfinite(row.x1) and math.isfinite(row.x2) for row in actual)
    assert all(row.x1 == 0.0 for row in actual)


@pytest.mark.unit
@pytest.mark.parametrize("epochs,lr", [(0, 0.1), (2, 0.0), (2, 1.1)])
def test_training_rejects_invalid_hyperparameters(epochs: int, lr: float) -> None:
    with pytest.raises(ValueError):
        fit([Row(1.0, 0.0, 1)], epochs=epochs, learning_rate=lr)


@pytest.mark.unit
def test_bce_gradient_matches_finite_difference() -> None:
    rows = [Row(-1.0, 1.0, 0), Row(2.0, -0.5, 1), Row(0.5, 0.1, 1)]
    model = LogisticModel(0.2, -0.1, 0.3)
    _, dw1, dw2, db = model.loss_and_grad(rows)
    h = 1e-6
    for attr, analytical in [("w1", dw1), ("w2", dw2), ("bias", db)]:
        old = getattr(model, attr)
        setattr(model, attr, old + h)
        plus = model.loss_and_grad(rows)[0]
        setattr(model, attr, old - h)
        minus = model.loss_and_grad(rows)[0]
        setattr(model, attr, old)
        assert (plus - minus) / (2 * h) == pytest.approx(analytical, abs=1e-7)
