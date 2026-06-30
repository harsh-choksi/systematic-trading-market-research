"""Research figures for clustering and forecasting outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA


sns.set_theme(style="whitegrid")


def _save(figure: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(figure)


def plot_k_diagnostics(diagnostics: pd.DataFrame, path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(diagnostics["k"], diagnostics["inertia"], marker="o", color="#1f77b4")
    axes[0].set(title="K-Means Inertia", xlabel="Number of clusters (k)", ylabel="Inertia")
    axes[1].plot(diagnostics["k"], diagnostics["silhouette"], marker="o", label="Silhouette")
    axes[1].plot(diagnostics["k"], diagnostics["davies_bouldin"], marker="s", label="Davies-Bouldin")
    selected = diagnostics.loc[diagnostics["selected"], "k"].iloc[0]
    axes[1].axvline(selected, color="#d62728", linestyle="--", label=f"Selected k={selected}")
    axes[1].set(title="Cluster Diagnostics", xlabel="Number of clusters (k)")
    axes[1].legend()
    _save(figure, path)


def plot_pca_clusters(train_scaled: np.ndarray, labels: np.ndarray, path: Path) -> None:
    coordinates = PCA(n_components=2, random_state=42).fit_transform(train_scaled)
    figure, axis = plt.subplots(figsize=(8, 6))
    scatter = axis.scatter(coordinates[:, 0], coordinates[:, 1], c=labels, cmap="tab10", s=12, alpha=0.65)
    axis.set(title="Training Regimes in PCA Space", xlabel="Principal Component 1", ylabel="Principal Component 2")
    colorbar = figure.colorbar(scatter, ax=axis, label="Cluster ID")
    colorbar.set_ticks(sorted(np.unique(labels)))
    _save(figure, path)


def plot_regime_timeline(assignments: pd.DataFrame, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(12, 5))
    scatter = axis.scatter(
        assignments.index,
        assignments["adjusted_close"],
        c=assignments["cluster_id"],
        cmap="tab10",
        s=8,
    )
    axis.set(title="SPY Price Colored by K-Means Regime", xlabel="Date", ylabel="Adjusted Close")
    axis.set_yscale("log")
    colorbar = figure.colorbar(scatter, ax=axis, label="Cluster ID")
    colorbar.set_ticks(sorted(assignments["cluster_id"].unique()))
    _save(figure, path)


def plot_cluster_profiles(profiles: pd.DataFrame, path: Path) -> None:
    columns = [
        "annualized_mean_log_return",
        "mean_volatility_20d",
        "mean_return_20d",
        "mean_price_sma50_ratio",
        "mean_drawdown_252d",
        "mean_duration_days",
    ]
    values = profiles.set_index("regime_name")[columns]
    standardized = (values - values.mean()) / values.std(ddof=0).replace(0, 1)
    figure, axis = plt.subplots(figsize=(10, max(4, len(profiles) * 0.8)))
    sns.heatmap(standardized, cmap="vlag", center=0, annot=True, fmt=".2f", ax=axis)
    axis.set(title="Standardized Regime Profiles", xlabel="Profile Metric", ylabel="Regime")
    _save(figure, path)


def plot_transition_matrix(matrix: pd.DataFrame, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(7, 6))
    sns.heatmap(matrix, cmap="Blues", annot=True, fmt=".2f", vmin=0, vmax=1, ax=axis)
    axis.set(title="One-Day Regime Transition Probabilities", xlabel="Next Regime", ylabel="Current Regime")
    _save(figure, path)


def plot_training_history(history: pd.DataFrame, path: Path) -> None:
    figure, primary = plt.subplots(figsize=(9, 4))
    secondary = primary.twinx()
    primary.plot(history["epoch"], history["training_loss"], color="#1f77b4", label="Training loss")
    secondary.plot(history["epoch"], history["validation_macro_f1"], color="#ff7f0e", label="Validation macro-F1")
    primary.set(xlabel="Epoch", ylabel="Training loss", title="LSTM Training History")
    secondary.set_ylabel("Validation macro-F1")
    lines = primary.get_lines() + secondary.get_lines()
    primary.legend(lines, [line.get_label() for line in lines], loc="best")
    _save(figure, path)


def plot_confusion_matrix(matrix: np.ndarray, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(7, 6))
    sns.heatmap(matrix, cmap="Purples", annot=True, fmt="d", ax=axis)
    axis.set(title="LSTM Test Confusion Matrix", xlabel="Predicted Regime", ylabel="Actual Regime")
    _save(figure, path)
