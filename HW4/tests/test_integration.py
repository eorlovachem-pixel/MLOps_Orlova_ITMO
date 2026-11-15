"""Integration-тесты проверяют реальные интерфейсы между стадиями ML."""

import json
from pathlib import Path

import pytest

from mlops_demo.pipeline import prepare, train


@pytest.mark.integration
def test_prepare_splits_data_and_prevents_leakage(raw_csv: Path, tmp_path: Path) -> None:
    path = tmp_path / "prepared.json"
    prepare(raw_csv, path, test_ratio=0.25, seed=2026)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert len(payload["train"]) == 90
    assert len(payload["test"]) == 30
    # Стандартизация по train => train-mean около нуля, а test-mean может быть не нулём.
    assert abs(sum(row["x1"] for row in payload["train"]) / 90) < 1e-12
    assert "scaler" in payload


@pytest.mark.integration
def test_prepare_to_train_contract(raw_csv: Path, tmp_path: Path) -> None:
    processed = tmp_path / "prepared.json"
    model = tmp_path / "model.json"
    prepare(raw_csv, processed, test_ratio=0.25, seed=2026)
    train(processed, model, epochs=250, learning_rate=0.25)
    saved = json.loads(model.read_text(encoding="utf-8"))
    assert len(saved["weights"]) == 2
    assert saved["final_loss"] < saved["first_loss"]
    assert saved["epochs"] == 250
