"""End-to-end: как пользователь, запускаем модули через CLI в отдельном процессе."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from mlops_demo.pipeline import evaluate, prepare, train


@pytest.mark.e2e
def test_full_pipeline_cli(raw_csv: Path, tmp_path: Path) -> None:
    processed = tmp_path / "processed.json"
    model = tmp_path / "model.json"
    metrics = tmp_path / "metrics.json"
    commands = [
        ["prepare", "--input", str(raw_csv), "--output", str(processed), "--seed", "2026"],
        ["train", "--input", str(processed), "--output", str(model), "--epochs", "250"],
        ["evaluate", "--input", str(processed), "--model", str(model), "--output", str(metrics)],
    ]
    for cmd in commands:
        subprocess.run([sys.executable, "-m", "mlops_demo.pipeline", *cmd], check=True)
    report = json.loads(metrics.read_text(encoding="utf-8"))
    assert report["n_test"] == 30
    assert 0.85 <= report["accuracy"] <= 1.0
    assert 0 <= report["f1"] <= 1.0


@pytest.mark.e2e
def test_repeated_pipeline_is_byte_reproducible(raw_csv: Path, tmp_path: Path) -> None:
    outputs: list[bytes] = []
    for index in range(2):
        target = tmp_path / str(index)
        target.mkdir()
        proc, model, metrics = target / "p.json", target / "m.json", target / "r.json"
        prepare(raw_csv, proc, test_ratio=0.25, seed=777)
        train(proc, model, epochs=100, learning_rate=0.2)
        evaluate(proc, model, metrics)
        outputs.append(proc.read_bytes() + model.read_bytes() + metrics.read_bytes())
    assert outputs[0] == outputs[1]
