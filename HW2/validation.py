"""Validation of tiny classification labels."""


def validate_binary(labels: list[int]) -> None:
    """Reject data outside a binary classification problem."""
    if not labels:
        raise ValueError("Empty labels")
    if any(label not in (0, 1) for label in labels):
        raise ValueError("Labels must be 0 or 1")
