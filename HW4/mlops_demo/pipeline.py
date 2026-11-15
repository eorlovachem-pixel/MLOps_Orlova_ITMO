"""CLI стадии: prepare -> train -> evaluate. JSON-артефакты участвуют в DVC DAG."""

import argparse
import json
from pathlib import Path
from typing import Any

from mlops_demo.data import Row, read_csv, split_rows
from mlops_demo.features import Standardizer
from mlops_demo.model import LogisticModel
from mlops_demo.training import fit


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8")


def _to_record(row: Row) -> dict[str, float | int]:
    return {"x1": row.x1, "x2": row.x2, "label": row.label}


def _read_rows(records: list[dict[str, float | int]]) -> list[Row]:
    return [Row(float(rec["x1"]), float(rec["x2"]), int(rec["label"])) for rec in records]


def prepare(input_path: Path, output_path: Path, *, test_ratio: float, seed: int) -> None:
    rows = read_csv(input_path)
    train, test = split_rows(rows, test_ratio=test_ratio, seed=seed)
    # Ключевой инвариант: fit только на train, иначе leakage из тестовой выборки.
    scaler = Standardizer.fit(train)
    result: dict[str, Any] = {
        "train": [_to_record(row) for row in scaler.transform_many(train)],
        "test": [_to_record(row) for row in scaler.transform_many(test)],
        "scaler": {"mean": list(scaler.mean), "scale": list(scaler.scale)},
        "seed": seed,
    }
    _write_json(output_path, result)


def train(input_path: Path, output_path: Path, *, epochs: int, learning_rate: float) -> None:
    prepared = json.loads(input_path.read_text(encoding="utf-8"))
    rows = _read_rows(prepared["train"])
    result = fit(rows, epochs=epochs, learning_rate=learning_rate)
    _write_json(
        output_path,
        {
            "weights": [result.model.w1, result.model.w2],
            "bias": result.model.bias,
            "first_loss": result.first_loss,
            "final_loss": result.final_loss,
            "epochs": result.epochs,
            "scaler": prepared["scaler"],
        },
    )


def evaluate(input_path: Path, model_path: Path, output_path: Path) -> None:
    prepared = json.loads(input_path.read_text(encoding="utf-8"))
    saved = json.loads(model_path.read_text(encoding="utf-8"))
    rows = _read_rows(prepared["test"])
    model = LogisticModel(
        float(saved["weights"][0]),
        float(saved["weights"][1]),
        float(saved["bias"]),
    )
    preds = [model.predict(row) for row in rows]
    correct = sum(int(pred == row.label) for pred, row in zip(preds, rows, strict=True))
    accuracy = correct / len(rows)
    true_positive = sum(int(p == 1 and r.label == 1) for p, r in zip(preds, rows, strict=True))
    false_positive = sum(int(p == 1 and r.label == 0) for p, r in zip(preds, rows, strict=True))
    false_negative = sum(int(p == 0 and r.label == 1) for p, r in zip(preds, rows, strict=True))
    predicted_positive = true_positive + false_positive
    precision = true_positive / predicted_positive if predicted_positive else 0.0
    relevant_positive = true_positive + false_negative
    recall = true_positive / relevant_positive if relevant_positive else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    _write_json(
        output_path,
        {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "n_test": len(rows),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="ITMO MLOps: ML pipeline")
    sub = parser.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("prepare", help="train/test + стандартизация на train")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--test-ratio", type=float, default=0.25)
    p.add_argument("--seed", type=int, default=2026)
    t = sub.add_parser("train", help="обучить логистическую регрессию")
    t.add_argument("--input", type=Path, required=True)
    t.add_argument("--output", type=Path, required=True)
    t.add_argument("--epochs", type=int, default=250)
    t.add_argument("--lr", type=float, default=0.25)
    e = sub.add_parser("evaluate", help="измерить качество на test")
    e.add_argument("--input", type=Path, required=True)
    e.add_argument("--model", type=Path, required=True)
    e.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.stage == "prepare":
        prepare(args.input, args.output, test_ratio=args.test_ratio, seed=args.seed)
    elif args.stage == "train":
        train(args.input, args.output, epochs=args.epochs, learning_rate=args.lr)
    else:
        evaluate(args.input, args.model, args.output)


if __name__ == "__main__":
    main()
