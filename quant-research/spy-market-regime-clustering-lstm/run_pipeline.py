"""Run the complete SPY regime-clustering and LSTM research pipeline."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import pandas as pd

from src.clustering import (
    build_cluster_profiles,
    derive_regime_names,
    evaluate_cluster_counts,
    fit_kmeans,
    transition_matrix,
)
from src.data import load_spy_data
from src.evaluation import (
    classification_metrics,
    fit_logistic_baseline,
    predict_logistic,
)
from src.features import FEATURE_COLUMNS, build_features, chronological_split, scale_splits
from src.model import build_sequences, predict_lstm, train_lstm
from src.plotting import (
    plot_cluster_profiles,
    plot_confusion_matrix,
    plot_k_diagnostics,
    plot_pca_clusters,
    plot_regime_timeline,
    plot_training_history,
    plot_transition_matrix,
)


SEQUENCE_LENGTH = 20


def _json_dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _split_sequence_bundle(bundle) -> dict[str, np.ndarray]:
    dates = bundle.target_dates
    masks = {
        "train": dates <= "2019-12-31",
        "validation": (dates >= "2020-01-01") & (dates <= "2022-12-31"),
        "test": (dates >= "2023-01-01") & (dates <= "2025-12-31"),
    }
    return masks


def _metrics_table(metrics: dict) -> str:
    rows = [
        "| Model | Accuracy | Balanced Accuracy | Macro-F1 |",
        "|---|---:|---:|---:|",
    ]
    for name, label in [
        ("persistence", "Regime persistence"),
        ("logistic_regression", "Logistic regression"),
        ("lstm", "PyTorch LSTM"),
    ]:
        values = metrics["models"][name]
        rows.append(
            f"| {label} | {values['accuracy']:.3f} | "
            f"{values['balanced_accuracy']:.3f} | {values['macro_f1']:.3f} |"
        )
    return "\n".join(rows)


def _profiles_table(profiles: pd.DataFrame) -> str:
    rows = [
        "| Cluster | Descriptive Label | Share | Annualized Mean Log Return | "
        "Mean 20-Day Volatility | Mean Duration |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for row in profiles.itertuples():
        rows.append(
            f"| {int(row.cluster_id)} | {row.regime_name} | {row.share:.1%} | "
            f"{row.annualized_mean_log_return:.1%} | {row.mean_volatility_20d:.1%} | "
            f"{row.mean_duration_days:.1f} days |"
        )
    return "\n".join(rows)


def generate_report(
    report_path: Path,
    diagnostics: pd.DataFrame,
    profiles: pd.DataFrame,
    metrics: dict,
    metadata: dict,
) -> None:
    """Publish a portfolio-facing Markdown report from generated artifacts."""
    selected = diagnostics.loc[diagnostics["selected"]].iloc[0]
    figures = "../quant-research/spy-market-regime-clustering-lstm/outputs/figures"
    project = "../quant-research/spy-market-regime-clustering-lstm"
    content = f"""# SPY Market Regime Clustering and LSTM Forecasting for Options Strategy Research

**Published:** June 30, 2026  
**Project:** [Code, notebook, and reproducibility instructions]({project}/)  
**Data:** SPY daily OHLCV, {metadata['first_observation']} through {metadata['last_observation']}

## Executive Summary

This research applies K-Means Clustering to backward-looking SPY market features, then trains a PyTorch LSTM to predict the next trading day's model-generated regime. The project demonstrates unsupervised learning, deep-learning sequence modeling, chronological validation, and baseline comparison within the existing quantitative trading research portfolio.

The selected K-Means solution used **{int(metrics['selected_k'])} clusters**, with a training silhouette score of **{selected['silhouette']:.3f}** and Davies-Bouldin score of **{selected['davies_bouldin']:.3f}**. The deep-learning results are reported against persistence and logistic-regression baselines without requiring the LSTM to outperform them.

## Options-Research Relevance

Market regimes can provide context for options research because trend, realized volatility, drawdown, and transition behavior influence the environment in which covered-call rules are evaluated. This project does not model option premiums or covered-call profitability. It provides a systematic state-classification layer that could support future options-strategy research.

## Data and Chronological Validation

- **Train:** 2010-01-01 through 2019-12-31
- **Validation:** 2020-01-01 through 2022-12-31
- **Test:** 2023-01-01 through 2025-12-31
- **Source:** {metadata['source']}
- **Raw observations:** {metadata['rows']:,}

Feature scaling and K-Means fitting use training data only. Validation and test observations are transformed with the frozen training scaler and assigned to the frozen training centroids.

## Features

The clustering input contains daily, 5-day, and 20-day returns; 10/20/60-day realized volatility; price/SMA and SMA/SMA ratios; RSI-14; normalized ATR-14; a 20-day volume z-score; and 252-day drawdown. Every feature is backward-looking at the observation date.

## K-Means Clustering

Candidate values from `k=2` through `k=8` were evaluated with inertia, silhouette score, Davies-Bouldin score, and minimum cluster share. The deterministic rule selected the highest-silhouette solution whose smallest training cluster represented at least 5% of observations; candidates within 0.01 of the best silhouette favored the smaller `k`.

![K-Means diagnostics]({figures}/k_selection.png)

![PCA visualization of training clusters]({figures}/pca_clusters.png)

## Regime Profiles

{_profiles_table(profiles)}

Descriptive labels are derived from training-period return and volatility profiles. Numeric cluster IDs remain the authoritative model output.

![SPY regime timeline]({figures}/regime_timeline.png)

![Standardized regime profiles]({figures}/cluster_profiles.png)

![Regime transition matrix]({figures}/transition_matrix.png)

## Deep Learning Model

The PyTorch model uses a 20-trading-day feature sequence, two LSTM layers, hidden size 64, dropout 0.20, and a linear classification head. Training uses weighted cross-entropy, AdamW, early stopping on validation macro-F1, and deterministic seed 42.

## Test Results

{_metrics_table(metrics)}

The persistence baseline predicts that tomorrow's regime will match today's. Logistic regression uses the flattened 20-day feature sequence. The LSTM is evaluated on the same fixed 2023-2025 test period.

![LSTM training history]({figures}/training_history.png)

![LSTM confusion matrix]({figures}/confusion_matrix.png)

## Limitations

- K-Means imposes spherical clusters and requires a chosen feature space and cluster count.
- Regime labels are model-generated descriptions, not objective market states.
- The LSTM predicts K-Means labels rather than returns, option prices, or trading profits.
- SPY history is one instrument and one sample period; other assets may produce different regimes.
- Market data, adjusted prices, and feature definitions can change results.
- Strong persistence can make a simple baseline difficult to beat and must be reported honestly.

## Reproducibility

The project includes modular Python source, an executable notebook, fixed date splits, deterministic random seeds, tests, generated metrics, cluster profiles, and regime assignments. Raw Yahoo Finance data is cached locally and excluded from Git.

## Disclaimer

This report is for research and educational purposes only and is not financial advice. The analysis does not recommend an options position or claim that identified regimes will persist in live markets.
"""
    report_path.write_text(content, encoding="utf-8")


def run_pipeline(
    project_root: Path | str | None = None,
    refresh_data: bool = False,
    max_epochs: int = 100,
) -> dict:
    """Run data acquisition, clustering, forecasting, evaluation, and reporting."""
    project_root = Path(project_root or Path(__file__).resolve().parent).resolve()
    repo_root = project_root.parents[1]
    output_dir = project_root / "outputs"
    figure_dir = output_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    raw, metadata = load_spy_data(project_root / "data" / "raw" / "spy.csv", refresh=refresh_data)
    features = build_features(raw)
    splits = chronological_split(features)
    scaler, scaled_splits = scale_splits(splits)

    diagnostics, selected_k = evaluate_cluster_counts(scaled_splits["train"])
    kmeans = fit_kmeans(scaled_splits["train"], selected_k)
    labels_by_split = {
        name: kmeans.predict(scaled)
        for name, scaled in scaled_splits.items()
    }

    combined_frame = pd.concat([splits["train"], splits["validation"], splits["test"]])
    combined_scaled = np.vstack(
        [scaled_splits["train"], scaled_splits["validation"], scaled_splits["test"]]
    )
    combined_labels = np.concatenate(
        [labels_by_split["train"], labels_by_split["validation"], labels_by_split["test"]]
    )

    training_profiles = build_cluster_profiles(splits["train"], labels_by_split["train"])
    regime_names = derive_regime_names(training_profiles)
    profiles = build_cluster_profiles(combined_frame, combined_labels)
    profiles["regime_name"] = profiles["cluster_id"].map(regime_names)
    transitions = transition_matrix(combined_labels, selected_k)

    assignments = combined_frame[["adjusted_close", "forward_return_1d"]].copy()
    assignments["cluster_id"] = combined_labels
    assignments["regime_name"] = assignments["cluster_id"].map(regime_names)
    assignments["split"] = np.select(
        [
            assignments.index <= "2019-12-31",
            assignments.index <= "2022-12-31",
        ],
        ["train", "validation"],
        default="test",
    )

    sequence_bundle = build_sequences(
        combined_scaled,
        combined_labels,
        combined_frame.index,
        sequence_length=SEQUENCE_LENGTH,
    )
    masks = _split_sequence_bundle(sequence_bundle)
    train_x = sequence_bundle.features[masks["train"]]
    train_y = sequence_bundle.targets[masks["train"]]
    validation_x = sequence_bundle.features[masks["validation"]]
    validation_y = sequence_bundle.targets[masks["validation"]]
    test_x = sequence_bundle.features[masks["test"]]
    test_y = sequence_bundle.targets[masks["test"]]

    logistic = fit_logistic_baseline(train_x, train_y)
    logistic_predictions = predict_logistic(logistic, test_x)
    persistence_predictions = sequence_bundle.current_regimes[masks["test"]]

    lstm, history = train_lstm(
        train_x,
        train_y,
        validation_x,
        validation_y,
        n_classes=selected_k,
        max_epochs=max_epochs,
    )
    lstm_predictions = predict_lstm(lstm, test_x)

    metrics = {
        "selected_k": selected_k,
        "sequence_length": SEQUENCE_LENGTH,
        "train_sequences": int(len(train_x)),
        "validation_sequences": int(len(validation_x)),
        "test_sequences": int(len(test_x)),
        "models": {
            "persistence": classification_metrics(test_y, persistence_predictions, selected_k),
            "logistic_regression": classification_metrics(test_y, logistic_predictions, selected_k),
            "lstm": classification_metrics(test_y, lstm_predictions, selected_k),
        },
    }

    predictions = pd.DataFrame(
        {
            "actual_cluster": test_y,
            "persistence_prediction": persistence_predictions,
            "logistic_prediction": logistic_predictions,
            "lstm_prediction": lstm_predictions,
        },
        index=sequence_bundle.target_dates[masks["test"]],
    )
    predictions.index.name = "Date"

    diagnostics.round(12).to_csv(output_dir / "clustering_diagnostics.csv", index=False)
    profiles.to_csv(output_dir / "cluster_profiles.csv", index=False)
    transitions.to_csv(output_dir / "transition_matrix.csv")
    assignments.to_csv(output_dir / "regime_assignments.csv", index_label="Date")
    predictions.to_csv(output_dir / "test_predictions.csv")
    history.to_csv(output_dir / "training_history.csv", index=False)
    _json_dump(output_dir / "metrics.json", metrics)
    _json_dump(
        output_dir / "run_metadata.json",
        {
            **metadata,
            "feature_columns": FEATURE_COLUMNS,
            "selected_k": selected_k,
            "split_rows": {name: int(len(split)) for name, split in splits.items()},
            "sequence_length": SEQUENCE_LENGTH,
            "random_seed": 42,
        },
    )

    plot_k_diagnostics(diagnostics, figure_dir / "k_selection.png")
    plot_pca_clusters(scaled_splits["train"], labels_by_split["train"], figure_dir / "pca_clusters.png")
    plot_regime_timeline(assignments, figure_dir / "regime_timeline.png")
    plot_cluster_profiles(profiles, figure_dir / "cluster_profiles.png")
    plot_transition_matrix(transitions, figure_dir / "transition_matrix.png")
    plot_training_history(history, figure_dir / "training_history.png")
    plot_confusion_matrix(
        np.asarray(metrics["models"]["lstm"]["confusion_matrix"]),
        figure_dir / "confusion_matrix.png",
    )

    report_path = repo_root / "research-papers" / "2026-06-30-spy-market-regime-clustering-lstm-report.md"
    generate_report(report_path, diagnostics, profiles, metrics, metadata)
    return {
        "selected_k": selected_k,
        "metrics_path": str(output_dir / "metrics.json"),
        "report_path": str(report_path),
        "epochs_trained": int(history["epoch"].max()),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-data", action="store_true", help="Ignore the local raw-data cache")
    parser.add_argument("--epochs", type=int, default=100, help="Maximum LSTM training epochs")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    result = run_pipeline(refresh_data=arguments.refresh_data, max_epochs=arguments.epochs)
    print(json.dumps(result, indent=2))
