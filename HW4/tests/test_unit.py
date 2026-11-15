"""Unit-тесты: даталоадер, block, model, training + граничные случаи."""

import math
from pathlib import Path

import pytest

from mlops_demo.data import Row, read_csv, split_rows
from mlops_demo.features import Standardizer
from mlops_demo.model import LogisticModel
from mlops_demo.training import fit


@pytest.mark.unit
def test_dataloader_schema_and_nonempty(raw_csv: Path) -> None:
    rows = read_csv(raw_csv)
    assert len(rows) == 120
    assert all(row.label in (0, 1) for row in rows)


@pytest.mark.unit
def test_dataloader_rejects_wrong_label(tmp_path: Path) -> None:
    wrong = tmp_path / "wrong.csv"
    wrong.write_text("x1,x2,label\n1,2,2\n3,4,1\n5,6,0\n7,8,1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Метка"):
        read_csv(wrong)


@pytest.mark.unit
def test_block_training_mean_and_constant_feature() -> None:
    sample = [Row(0, 7, 0), Row(2, 7, 1)]
    block = Standardizer.fit(sample)
    transformed = block.transform_many(sample)
    assert block.mean == (1.0, 7.0)
    assert block.scale == (1.0, 1.0)
    assert [row.x1 for row in transformed] == [-1.0, 1.0]
    assert all(row.x2 == 0.0 for row in transformed)


@pytest.mark.unit
def test_block_empty_fit_raises() -> None:
    with pytest.raises(ValueError, match="пустой"):
        Standardizer.fit([])


@pytest.mark.unit
def test_model_sigmoid_and_predict() -> None:
    model = LogisticModel(1.0, 0.0, 0.0)
    assert model.predict(Row(-3, 0, 0)) == 0
    assert model.predict(Row(3, 0, 1)) == 1
    assert math.isclose(model.predict_proba(Row(0, 0, 0)), 0.5)


@pytest.mark.unit
def test_model_large_score_is_finite() -> None:
    model = LogisticModel(5000.0, 0.0, 0.0)
    assert model.predict_proba(Row(-1, 0, 0)) == 0.0
    assert model.predict_proba(Row(1, 0, 1)) == 1.0


@pytest.mark.unit
def test_split_seed_reproducible(rows: list[Row]) -> None:
    first = split_rows(rows, test_ratio=0.25, seed=42)
    second = split_rows(rows, test_ratio=0.25, seed=42)
    assert first == second
    assert len(first[0]) == 3 and len(first[1]) == 1


@pytest.mark.unit
def test_training_reduces_loss(rows: list[Row]) -> None:
    result = fit(rows, epochs=100, learning_rate=0.2)
    assert result.final_loss < result.first_loss
    assert all(result.model.predict(row) == row.label for row in rows)


@pytest.mark.unit
@pytest.mark.parametrize("epochs,lr", [(0, 0.2), (10, 0.0), (10, 5.0)])
def test_training_rejects_invalid_hyperparameters(rows: list[Row], epochs: int, lr: float) -> None:
    with pytest.raises(ValueError):
        fit(rows, epochs=epochs, learning_rate=lr)
