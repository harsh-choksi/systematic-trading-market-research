# Data Policy

The pipeline downloads daily SPY OHLCV data from Yahoo Finance through `yfinance` for `2010-01-01` through `2025-12-31`.

Raw data is cached under `data/raw/` for local reproducibility but is intentionally excluded from Git. Generated metadata records the ticker, requested date range, source, row count, and download timestamp.

Committed outputs contain derived research results rather than a redistributed raw market-data snapshot.

