"""Детерминированное обучение full-batch gradient descent."""

from dataclasses import dataclass

from mlops_demo.data import Row
from mlops_demo.model import LogisticModel


@dataclass(frozen=True)
class TrainingResult:
    model: LogisticModel
    first_loss: float
    final_loss: float
    epochs: int


def fit(rows: list[Row], *, epochs: int = 250, learning_rate: float = 0.25) -> TrainingResult:
    if not rows:
        raise ValueError("Нельзя обучать модель на пустых данных")
    if epochs <= 0:
        raise ValueError("epochs должно быть положительным")
    if learning_rate <= 0.0 or learning_rate > 1.0:
        raise ValueError("learning_rate должен лежать в интервале (0,1]")
    model = LogisticModel()
    first_loss, _, _, _ = model.loss_and_grad(rows)
    for _ in range(epochs):
        _, dw1, dw2, dbias = model.loss_and_grad(rows)
        model.w1 -= learning_rate * dw1
        model.w2 -= learning_rate * dw2
        model.bias -= learning_rate * dbias
    final_loss, _, _, _ = model.loss_and_grad(rows)
    return TrainingResult(model, first_loss, final_loss, epochs)
