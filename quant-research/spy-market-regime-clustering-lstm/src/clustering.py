"""K-Means model selection, regime profiling, and transition analysis."""

from __future__ import annotations

import os

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score


RANDOM_STATE = 42


def evaluate_cluster_counts(
    train_scaled: np.ndarray,
    k_values: range = range(2, 9),
    minimum_cluster_share: float = 0.05,
) -> tuple[pd.DataFrame, int]:
    """Evaluate candidate cluster counts and apply the deterministic selection rule."""
    rows: list[dict] = []
    for k in k_values:
        model = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init=20,
            max_iter=500,
        )
        labels = model.fit_predict(train_scaled)
        shares = np.bincount(labels, minlength=k) / len(labels)
        rows.append(
            {
                "k": k,
                "inertia": float(model.inertia_),
                "silhouette": float(silhouette_score(train_scaled, labels)),
                "davies_bouldin": float(davies_bouldin_score(train_scaled, labels)),
                "minimum_cluster_share": float(shares.min()),
                "eligible": bool(shares.min() >= minimum_cluster_share),
            }
        )

    diagnostics = pd.DataFrame(rows)
    eligible = diagnostics.loc[diagnostics["eligible"]].copy()
    if eligible.empty:
        raise RuntimeError("No K-Means candidate met the minimum cluster-share rule")
    maximum_silhouette = eligible["silhouette"].max()
    near_best = eligible.loc[eligible["silhouette"] >= maximum_silhouette - 0.01]
    selected_k = int(near_best.sort_values("k").iloc[0]["k"])
    diagnostics["selected"] = diagnostics["k"].eq(selected_k)
    return diagnostics, selected_k


def fit_kmeans(train_scaled: np.ndarray, n_clusters: int) -> KMeans:
    """Fit the final training-only K-Means model."""
    return KMeans(
        n_clusters=n_clusters,
        random_state=RANDOM_STATE,
        n_init=20,
        max_iter=500,
    ).fit(train_scaled)


def _mean_regime_duration(labels: np.ndarray) -> dict[int, float]:
    runs: dict[int, list[int]] = {}
    current = int(labels[0])
    length = 1
    for label in labels[1:]:
        label = int(label)
        if label == current:
            length += 1
        else:
            runs.setdefault(current, []).append(length)
            current = label
            length = 1
    runs.setdefault(current, []).append(length)
    return {cluster: float(np.mean(lengths)) for cluster, lengths in runs.items()}


def build_cluster_profiles(frame: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """Summarize regime behavior with return, volatility, trend, and duration statistics."""
    profiled = frame.copy()
    profiled["cluster_id"] = labels
    durations = _mean_regime_duration(labels)
    profiles = (
        profiled.groupby("cluster_id")
        .agg(
            observations=("cluster_id", "size"),
            mean_daily_log_return=("log_return_1d", "mean"),
            mean_forward_return_1d=("forward_return_1d", "mean"),
            median_forward_return_1d=("forward_return_1d", "median"),
            mean_volatility_20d=("volatility_20d", "mean"),
            mean_return_20d=("return_20d", "mean"),
            mean_price_sma50_ratio=("price_sma50_ratio", "mean"),
            mean_drawdown_252d=("drawdown_252d", "mean"),
        )
        .reset_index()
    )
    profiles["share"] = profiles["observations"] / len(profiled)
    profiles["annualized_mean_log_return"] = profiles["mean_daily_log_return"] * 252
    profiles["mean_duration_days"] = profiles["cluster_id"].map(durations)
    return profiles.sort_values("cluster_id").reset_index(drop=True)


def derive_regime_names(training_profiles: pd.DataFrame) -> dict[int, str]:
    """Create descriptive labels from training-only return and volatility profiles."""
    volatility_median = training_profiles["mean_volatility_20d"].median()
    names: dict[int, str] = {}
    used: dict[str, int] = {}
    for row in training_profiles.itertuples():
        annual_return = row.annualized_mean_log_return
        if annual_return > 0.03:
            direction = "Bullish"
        elif annual_return < -0.03:
            direction = "Bearish"
        else:
            direction = "Neutral"
        volatility = "High Volatility" if row.mean_volatility_20d >= volatility_median else "Low Volatility"
        base = f"{direction} / {volatility}"
        used[base] = used.get(base, 0) + 1
        names[int(row.cluster_id)] = base if used[base] == 1 else f"{base} (Cluster {int(row.cluster_id)})"
    return names


def transition_matrix(labels: np.ndarray, n_clusters: int) -> pd.DataFrame:
    """Calculate a row-normalized one-day regime transition matrix."""
    counts = np.zeros((n_clusters, n_clusters), dtype=float)
    for current, following in zip(labels[:-1], labels[1:]):
        counts[int(current), int(following)] += 1
    row_totals = counts.sum(axis=1, keepdims=True)
    normalized = np.divide(counts, row_totals, out=np.zeros_like(counts), where=row_totals != 0)
    return pd.DataFrame(
        normalized,
        index=[f"Cluster {i}" for i in range(n_clusters)],
        columns=[f"Cluster {i}" for i in range(n_clusters)],
    )
