"""Simple, dependency-free evaluation metrics for GitFlow exercises."""

MODEL_THRESHOLD = 0.5


def accuracy(y_true: list[int], y_pred: list[int]) -> float:
    """Return classification accuracy; inputs must be aligned non-empty labels."""
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("Labels must be non-empty and have the same length")
    return sum(a == b for a, b in zip(y_true, y_pred, strict=True)) / len(y_true)


def binary_precision(y_true: list[int], y_pred: list[int]) -> float:
    """Precision with a defined 0.0 result for no predicted positives."""
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("Labels must be non-empty and aligned")
    tp = sum(a == b == 1 for a, b in zip(y_true, y_pred, strict=True))
    fp = sum(a == 0 and b == 1 for a, b in zip(y_true, y_pred, strict=True))
    return tp / (tp + fp) if (tp + fp) else 0.0
