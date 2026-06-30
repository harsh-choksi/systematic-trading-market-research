"""PyTorch sequence model and deterministic training utilities."""

from __future__ import annotations

import copy
import random
from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


RANDOM_STATE = 42


def set_deterministic(seed: int = RANDOM_STATE) -> None:
    """Configure reproducible CPU execution."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


@dataclass
class SequenceBundle:
    features: np.ndarray
    targets: np.ndarray
    current_regimes: np.ndarray
    target_dates: pd.DatetimeIndex


def build_sequences(
    scaled_features: np.ndarray,
    labels: np.ndarray,
    dates: pd.DatetimeIndex,
    sequence_length: int = 20,
) -> SequenceBundle:
    """Use a window ending at t to predict the regime at t+1."""
    sequences: list[np.ndarray] = []
    targets: list[int] = []
    current_regimes: list[int] = []
    target_dates: list[pd.Timestamp] = []
    for end_index in range(sequence_length - 1, len(scaled_features) - 1):
        start_index = end_index - sequence_length + 1
        sequences.append(scaled_features[start_index : end_index + 1])
        current_regimes.append(int(labels[end_index]))
        targets.append(int(labels[end_index + 1]))
        target_dates.append(pd.Timestamp(dates[end_index + 1]))
    return SequenceBundle(
        features=np.asarray(sequences, dtype=np.float32),
        targets=np.asarray(targets, dtype=np.int64),
        current_regimes=np.asarray(current_regimes, dtype=np.int64),
        target_dates=pd.DatetimeIndex(target_dates),
    )


class RegimeLSTM(nn.Module):
    """Two-layer LSTM classifier for next-day regime prediction."""

    def __init__(
        self,
        input_size: int,
        n_classes: int,
        hidden_size: int = 64,
        num_layers: int = 2,
        dropout: float = 0.20,
    ) -> None:
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True,
        )
        self.classifier = nn.Linear(hidden_size, n_classes)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        outputs, _ = self.lstm(inputs)
        return self.classifier(outputs[:, -1, :])


def _make_loader(
    features: np.ndarray,
    targets: np.ndarray,
    batch_size: int,
    shuffle: bool,
) -> DataLoader:
    generator = torch.Generator().manual_seed(RANDOM_STATE)
    dataset = TensorDataset(torch.from_numpy(features), torch.from_numpy(targets))
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        generator=generator,
        num_workers=0,
    )


def predict_lstm(model: RegimeLSTM, features: np.ndarray, batch_size: int = 256) -> np.ndarray:
    """Return class predictions for a sequence matrix."""
    model.eval()
    predictions: list[np.ndarray] = []
    placeholder = np.zeros(len(features), dtype=np.int64)
    loader = _make_loader(features, placeholder, batch_size=batch_size, shuffle=False)
    with torch.no_grad():
        for batch_features, _ in loader:
            logits = model(batch_features)
            predictions.append(logits.argmax(dim=1).cpu().numpy())
    return np.concatenate(predictions)


def train_lstm(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    validation_features: np.ndarray,
    validation_targets: np.ndarray,
    n_classes: int,
    max_epochs: int = 100,
    patience: int = 10,
    batch_size: int = 64,
) -> tuple[RegimeLSTM, pd.DataFrame]:
    """Train with weighted loss and early stopping on validation macro-F1."""
    set_deterministic()
    model = RegimeLSTM(
        input_size=train_features.shape[-1],
        n_classes=n_classes,
    )

    counts = np.bincount(train_targets, minlength=n_classes).astype(float)
    if np.any(counts == 0):
        raise ValueError("Every K-Means regime must appear in LSTM training targets")
    weights = len(train_targets) / (n_classes * counts)
    criterion = nn.CrossEntropyLoss(weight=torch.tensor(weights, dtype=torch.float32))
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    train_loader = _make_loader(train_features, train_targets, batch_size=batch_size, shuffle=True)

    best_score = -np.inf
    best_state: dict | None = None
    epochs_without_improvement = 0
    history: list[dict] = []

    for epoch in range(1, max_epochs + 1):
        model.train()
        running_loss = 0.0
        examples = 0
        for batch_features, batch_targets in train_loader:
            optimizer.zero_grad()
            logits = model(batch_features)
            loss = criterion(logits, batch_targets)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            running_loss += float(loss.item()) * len(batch_targets)
            examples += len(batch_targets)

        validation_predictions = predict_lstm(model, validation_features)
        validation_f1 = f1_score(
            validation_targets,
            validation_predictions,
            average="macro",
            zero_division=0,
        )
        history.append(
            {
                "epoch": epoch,
                "training_loss": running_loss / examples,
                "validation_macro_f1": float(validation_f1),
            }
        )

        if validation_f1 > best_score + 1e-6:
            best_score = validation_f1
            best_state = copy.deepcopy(model.state_dict())
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= patience:
                break

    if best_state is None:
        raise RuntimeError("LSTM training did not produce a checkpoint")
    model.load_state_dict(best_state)
    return model, pd.DataFrame(history)

