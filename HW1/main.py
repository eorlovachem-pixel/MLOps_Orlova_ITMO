"""Run a minimal HW1 example."""

from quality import normalized_mean


def main() -> None:
    scores = [0.91, 0.85, 0.97]
    print(f"Average model score: {normalized_mean(scores):.3f}")


if __name__ == "__main__":
    main()
