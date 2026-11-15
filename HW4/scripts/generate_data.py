"""Создать собственный небольшой датасет, без скачивания и приватных данных."""

import argparse
import csv
import random
from pathlib import Path


def generate(path: Path, *, seed: int = 2026, n: int = 120) -> None:
    if n < 4:
        raise ValueError("n >= 4")
    rng = random.Random(seed)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["x1", "x2", "label"])
        for _ in range(n):
            x1 = rng.uniform(-2, 2)
            x2 = rng.uniform(-2, 2)
            label = int(1.5 * x1 - 0.7 * x2 + rng.gauss(0, 0.15) > 0)
            writer.writerow([f"{x1:.6f}", f"{x2:.6f}", label])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw.csv"))
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--n", type=int, default=120)
    args = parser.parse_args()
    generate(args.output, seed=args.seed, n=args.n)
