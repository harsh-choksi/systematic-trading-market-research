"""Baselines and classification metrics."""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


def fit_logistic_baseline(
    train_sequences: np.ndarray,
    train_targets: np.ndarray,
) -> LogisticRegression:
    """Fit a balanced multinomial linear baseline on flattened windows."""
    model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42,
        solver="lbfgs",
    )
    model.fit(train_sequences.reshape(len(train_sequences), -1), train_targets)
    return model


def predict_logistic(model: LogisticRegression, sequences: np.ndarray) -> np.ndarray:
    return model.predict(sequences.reshape(len(sequences), -1))


def classification_metrics(
    targets: np.ndarray,
    predictions: np.ndarray,
    n_classes: int,
) -> dict:
    """Build JSON-serializable aggregate and per-class metrics."""
    labels = list(range(n_classes))
    return {
        "accuracy": float(accuracy_score(targets, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(targets, predictions)),
        "macro_f1": float(f1_score(targets, predictions, average="macro", zero_division=0)),
        "per_class": classification_report(
            targets,
            predictions,
            labels=labels,
            output_dict=True,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(targets, predictions, labels=labels).tolist(),
    }

