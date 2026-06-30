"""SPY data acquisition and local caching."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


TICKER = "SPY"
START_DATE = "2010-01-01"
END_DATE_EXCLUSIVE = "2026-01-01"


def load_spy_data(cache_path: Path, refresh: bool = False) -> tuple[pd.DataFrame, dict]:
    """Load a fixed SPY history, downloading and caching it when needed."""
    cache_path = Path(cache_path)
    if cache_path.exists() and not refresh:
        frame = pd.read_csv(cache_path, parse_dates=["Date"], index_col="Date")
        source = "Yahoo Finance via yfinance (local cache)"
    else:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        frame = yf.download(
            TICKER,
            start=START_DATE,
            end=END_DATE_EXCLUSIVE,
            auto_adjust=False,
            actions=False,
            progress=False,
            threads=False,
        )
        if frame.empty:
            raise RuntimeError("yfinance returned no SPY rows")
        if isinstance(frame.columns, pd.MultiIndex):
            frame.columns = frame.columns.get_level_values(0)
        frame.index = pd.to_datetime(frame.index).tz_localize(None)
        frame.index.name = "Date"
        frame.to_csv(cache_path)
        source = "Yahoo Finance via yfinance"

    frame = frame.sort_index()
    frame.columns = [str(column).strip() for column in frame.columns]
    required = {"Open", "High", "Low", "Close", "Volume"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"SPY data is missing required columns: {missing}")
    if "Adj Close" not in frame.columns:
        frame["Adj Close"] = frame["Close"]

    frame = frame.loc[(frame.index >= START_DATE) & (frame.index < END_DATE_EXCLUSIVE)]
    metadata = {
        "ticker": TICKER,
        "requested_start": START_DATE,
        "requested_end_inclusive": "2025-12-31",
        "source": source,
        "rows": int(len(frame)),
        "first_observation": frame.index.min().date().isoformat(),
        "last_observation": frame.index.max().date().isoformat(),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    return frame, metadata
