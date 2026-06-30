"""Leakage-aware market feature engineering and chronological splits."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "log_return_1d",
    "return_5d",
    "return_20d",
    "volatility_10d",
    "volatility_20d",
    "volatility_60d",
    "price_sma20_ratio",
    "price_sma50_ratio",
    "sma20_sma50_ratio",
    "rsi_14",
    "atr_14_normalized",
    "volume_zscore_20d",
    "drawdown_252d",
]


def build_features(raw: pd.DataFrame) -> pd.DataFrame:
    """Build backward-looking SPY features and a one-day forward return."""
    frame = raw.copy().sort_index()
    adjusted_close = frame["Adj Close"].astype(float)
    close = frame["Close"].astype(float)
    high = frame["High"].astype(float)
    low = frame["Low"].astype(float)
    volume = frame["Volume"].astype(float)

    output = pd.DataFrame(index=frame.index)
    output["adjusted_close"] = adjusted_close
    output["log_return_1d"] = np.log(adjusted_close / adjusted_close.shift(1))
    output["return_5d"] = adjusted_close.pct_change(5)
    output["return_20d"] = adjusted_close.pct_change(20)

    output["volatility_10d"] = output["log_return_1d"].rolling(10).std() * np.sqrt(252)
    output["volatility_20d"] = output["log_return_1d"].rolling(20).std() * np.sqrt(252)
    output["volatility_60d"] = output["log_return_1d"].rolling(60).std() * np.sqrt(252)

    sma_20 = adjusted_close.rolling(20).mean()
    sma_50 = adjusted_close.rolling(50).mean()
    output["price_sma20_ratio"] = adjusted_close / sma_20 - 1
    output["price_sma50_ratio"] = adjusted_close / sma_50 - 1
    output["sma20_sma50_ratio"] = sma_20 / sma_50 - 1

    delta = adjusted_close.diff()
    average_gain = delta.clip(lower=0).rolling(14).mean()
    average_loss = -delta.clip(upper=0).rolling(14).mean()
    relative_strength = average_gain / average_loss.replace(0, np.nan)
    output["rsi_14"] = (100 - 100 / (1 + relative_strength)).fillna(100) / 100

    previous_close = close.shift(1)
    true_range = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    output["atr_14_normalized"] = true_range.rolling(14).mean() / adjusted_close

    volume_mean = volume.rolling(20).mean()
    volume_std = volume.rolling(20).std().replace(0, np.nan)
    output["volume_zscore_20d"] = (volume - volume_mean) / volume_std
    output["drawdown_252d"] = adjusted_close / adjusted_close.rolling(252).max() - 1
    output["forward_return_1d"] = adjusted_close.shift(-1) / adjusted_close - 1

    output = output.replace([np.inf, -np.inf], np.nan)
    return output.dropna(subset=FEATURE_COLUMNS + ["forward_return_1d"])


def chronological_split(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return fixed, non-overlapping train/validation/test partitions."""
    splits = {
        "train": frame.loc["2010-01-01":"2019-12-31"].copy(),
        "validation": frame.loc["2020-01-01":"2022-12-31"].copy(),
        "test": frame.loc["2023-01-01":"2025-12-31"].copy(),
    }
    if any(split.empty for split in splits.values()):
        empty = [name for name, split in splits.items() if split.empty]
        raise ValueError(f"Chronological split produced empty partitions: {empty}")
    if not splits["train"].index.max() < splits["validation"].index.min():
        raise ValueError("Training and validation periods overlap")
    if not splits["validation"].index.max() < splits["test"].index.min():
        raise ValueError("Validation and test periods overlap")
    return splits


def scale_splits(
    splits: dict[str, pd.DataFrame],
) -> tuple[StandardScaler, dict[str, np.ndarray]]:
    """Fit a scaler on training features and transform every partition."""
    scaler = StandardScaler()
    scaled = {"train": scaler.fit_transform(splits["train"][FEATURE_COLUMNS])}
    scaled["validation"] = scaler.transform(splits["validation"][FEATURE_COLUMNS])
    scaled["test"] = scaler.transform(splits["test"][FEATURE_COLUMNS])
    return scaler, scaled

