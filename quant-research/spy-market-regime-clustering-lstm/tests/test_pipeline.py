"""Offline regression tests for the market-regime research pipeline."""

from __future__ import annotations

import numpy as np
import pandas as pd
import torch

from src.clustering import evaluate_cluster_counts, fit_kmeans
from src.features import FEATURE_COLUMNS, build_features, chronological_split, scale_splits
from src.model import RegimeLSTM, build_sequences


def synthetic_ohlcv() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.bdate_range("2009-01-01", "2025-12-31")
    log_returns = rng.normal(0.00025, 0.012, len(dates))
    close = 100 * np.exp(np.cumsum(log_returns))
    open_price = close * (1 + rng.normal(0, 0.002, len(dates)))
    high = np.maximum(open_price, close) * (1 + rng.uniform(0, 0.01, len(dates)))
    low = np.minimum(open_price, close) * (1 - rng.uniform(0, 0.01, len(dates)))
    return pd.DataFrame(
        {
            "Open": open_price,
            "High": high,
            "Low": low,
            "Close": close,
            "Adj Close": close,
            "Volume": rng.integers(40_000_000, 150_000_000, len(dates)),
        },
        index=dates,
    )


def test_features_and_chronological_splits_are_valid() -> None:
    features = build_features(synthetic_ohlcv())
    assert set(FEATURE_COLUMNS).issubset(features.columns)
    assert not features[FEATURE_COLUMNS].isna().any().any()

    splits = chronological_split(features)
    assert splits["train"].index.max() < splits["validation"].index.min()
    assert splits["validation"].index.max() < splits["test"].index.min()

    _, scaled = scale_splits(splits)
    np.testing.assert_allclose(scaled["train"].mean(axis=0), 0, atol=1e-10)
    assert scaled["validation"].shape[1] == len(FEATURE_COLUMNS)


def test_kmeans_selection_is_deterministic() -> None:
    rng = np.random.default_rng(42)
    samples = np.vstack(
        [
            rng.normal(-2, 0.5, size=(150, 4)),
            rng.normal(0, 0.5, size=(150, 4)),
            rng.normal(2, 0.5, size=(150, 4)),
        ]
    )
    first_diagnostics, first_k = evaluate_cluster_counts(samples, range(2, 6))
    second_diagnostics, second_k = evaluate_cluster_counts(samples, range(2, 6))
    assert first_k == second_k
    pd.testing.assert_frame_equal(first_diagnostics, second_diagnostics)
    np.testing.assert_array_equal(
        fit_kmeans(samples, first_k).labels_,
        fit_kmeans(samples, second_k).labels_,
    )


def test_sequence_alignment_and_lstm_output_shape() -> None:
    rng = np.random.default_rng(42)
    scaled = rng.normal(size=(100, len(FEATURE_COLUMNS))).astype(np.float32)
    labels = np.arange(100) % 4
    dates = pd.bdate_range("2020-01-01", periods=100)
    bundle = build_sequences(scaled, labels, dates, sequence_length=20)

    assert bundle.features.shape == (80, 20, len(FEATURE_COLUMNS))
    assert bundle.targets[0] == labels[20]
    assert bundle.current_regimes[0] == labels[19]
    assert bundle.target_dates[0] == dates[20]

    model = RegimeLSTM(input_size=len(FEATURE_COLUMNS), n_classes=4)
    logits = model(torch.from_numpy(bundle.features[:8]))
    assert tuple(logits.shape) == (8, 4)

