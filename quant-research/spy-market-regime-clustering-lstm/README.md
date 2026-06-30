# SPY Market Regime Clustering and LSTM Forecasting

This supplementary quantitative research project identifies historical SPY market regimes with K-Means Clustering and trains a PyTorch LSTM to forecast the next trading day's regime. It is framed as market research that may inform options-strategy analysis; it does not claim to model covered-call profitability.

## Portfolio Evidence

- **K-Means Clustering:** training-only regime discovery with reproducible model-selection diagnostics.
- **Deep Learning:** two-layer PyTorch LSTM sequence classifier.
- **Time-Series Validation:** fixed chronological train, validation, and test periods.
- **Benchmarking:** persistence and multinomial logistic-regression baselines.
- **Research Communication:** executable notebook, generated figures, metrics, and a portfolio-facing report.

## Data Window

| Split | Dates |
|---|---|
| Train | 2010-01-01 through 2019-12-31 |
| Validation | 2020-01-01 through 2022-12-31 |
| Test | 2023-01-01 through 2025-12-31 |

SPY daily OHLCV data is downloaded through `yfinance`. Raw downloads are cached locally and excluded from Git.

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_pipeline.py
.\.venv\Scripts\python.exe -m pytest
```

Execute the notebook after the pipeline environment is installed:

```powershell
.\.venv\Scripts\jupyter.exe nbconvert --execute --inplace notebooks\01-spy-market-regime-analysis.ipynb
```

## Artifacts

- [Portfolio-facing report](../../research-papers/2026-06-30-spy-market-regime-clustering-lstm-report.md)
- [Executable notebook](notebooks/01-spy-market-regime-analysis.ipynb)
- [Generated metrics](outputs/metrics.json)
- [Cluster profiles](outputs/cluster_profiles.csv)
- [Regime assignments](outputs/regime_assignments.csv)
- [Figures](outputs/figures/)

## Results Snapshot

K-Means selected `k=2` using the training-only selection rule, with silhouette score `0.400`. The two descriptive profiles were a bullish/low-volatility regime and a bearish/high-volatility regime.

| Test Model | Accuracy | Balanced Accuracy | Macro-F1 |
|---|---:|---:|---:|
| Regime persistence | 0.940 | 0.913 | 0.912 |
| Logistic regression | 0.940 | 0.917 | 0.913 |
| PyTorch LSTM | 0.936 | 0.924 | 0.909 |

The LSTM did not outperform every baseline on every metric. This is reported directly because the project is intended to demonstrate a reproducible research process rather than cherry-picked model superiority.

## Important Interpretation

K-Means regime labels are descriptive groupings of engineered historical features. The LSTM predicts those model-generated labels, not market returns or guaranteed trading outcomes. Results depend on the selected features, data period, preprocessing, cluster solution, and training procedure.
