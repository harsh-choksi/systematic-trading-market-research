# Systematic Trading & Market Research Portfolio

A focused research portfolio covering options strategy analysis, systematic trading logic, Pine Script development, and quantitative backtesting.

**Systematic Trading & Market Research Portfolio Link** | `github.com/harsh-choksi/systematic-trading-market-research`

## Portfolio Snapshot

| Area | Current Artifact |
|---|---|
| Research focus | Options strategy modeling, covered-call recovery, assignment risk |
| Featured strategy | [TREND-CATCHER [15m]](tradingview/trend-catcher-summary.md) |
| Strategy platform | TradingView / Pine Script |
| Research methods | Black-Scholes modeling, put/call sentiment inputs, strike-selection rules, assignment probability analysis |
| Primary paper | [Sentiment-Adjusted Covered-Call Assignment Simulation](research-papers/2026-06-10-covered-call-assignment-simulation-summary.md) |
| Public script | [TREND-CATCHER [15m] on TradingView](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/) |
| Supplementary research | [SPY Market Regime Clustering and LSTM Forecasting](research-papers/2026-06-30-spy-market-regime-clustering-lstm-report.md) |

## Overview

This repository is organized as a public archive for market research papers and strategy-development work. It is designed to serve as a polished GitHub landing page for resume reviewers, recruiters, and anyone evaluating the research process behind the projects.

The work here emphasizes:

- quantitative reasoning around options strategies and assignment risk
- systematic strategy design using explicit entry, exit, and risk rules
- Pine Script implementation for TradingView strategy testing
- clear documentation of assumptions, limitations, and research status

## Research Papers

| Date | Paper | Focus | Methods | Status |
|---|---|---|---|---|
| Jun 10, 2026 | [Sentiment-Adjusted Covered-Call Assignment Simulation](research-papers/2026-06-10-covered-call-assignment-simulation-summary.md) | Covered calls and assignment risk | Black-Scholes modeling, put/call sentiment inputs, strike-selection rules, assignment probability analysis | Summary and DOCX available; PDF pending |
| Jun 30, 2026 | [SPY Market Regime Clustering and LSTM Forecasting](research-papers/2026-06-30-spy-market-regime-clustering-lstm-report.md) | Market-regime context for options-strategy research | K-Means Clustering, chronological validation, PyTorch LSTM, baseline comparison | Report, notebook, code, and generated results available |

The full paper is available as a Word document, with a Markdown summary provided for quick review. A PDF version can be added later once export is available.

## Featured Strategy

The current featured strategy is TREND-CATCHER [15m], a TradingView Pine Script strategy focused on trend reversals, stochastic oscillator confirmation, and rule-based trade management.

| Resource | Link |
|---|---|
| Strategy hub | [TradingView strategy archive](tradingview/) |
| Strategy summary | [View summary](tradingview/trend-catcher-summary.md) |
| Public TradingView script | [Open on TradingView](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/) |
| Pine Script source | [View active script](trend-catcher_15m-v5.pine) |

## Supplementary Quantitative Research

### [SPY Market Regime Clustering and LSTM Forecasting](research-papers/2026-06-30-spy-market-regime-clustering-lstm-report.md)

This secondary research project applies K-Means Clustering to historical SPY features and trains a PyTorch LSTM to forecast the next model-generated regime. It includes fixed chronological validation, persistence and logistic-regression baselines, an executable notebook, modular source code, generated figures, and reproducible metrics.

| Resource | Link |
|---|---|
| Research report | [Read report](research-papers/2026-06-30-spy-market-regime-clustering-lstm-report.md) |
| Project overview | [View project](quant-research/spy-market-regime-clustering-lstm/) |
| Executable notebook | [Open notebook](quant-research/spy-market-regime-clustering-lstm/notebooks/01-spy-market-regime-analysis.ipynb) |
| Generated metrics | [View metrics](quant-research/spy-market-regime-clustering-lstm/outputs/metrics.json) |

## Methodology

This portfolio separates research artifacts from strategy implementation:

- Research papers document model assumptions, inputs, outputs, limitations, and risk controls.
- TradingView scripts show implementation work and strategy-development iterations.
- Supplementary quantitative research demonstrates K-Means Clustering, deep learning, and leakage-aware time-series validation.
- Archive folders preserve earlier variants without distracting from the featured strategy.
- Disclosures and backtesting notes clarify that modeled or backtested results are conditional on assumptions.

## Archive Organization

Older strategy variants are retained for transparency and development history:

- [Inactive scripts](inactive-scripts/) contain retired or superseded strategy files.
- [Temporarily inactive scripts](temporarily-inactive-scripts/) contain paused variants that may still inform future development.
- [Research papers](research-papers/) contains the market research archive.
- [Quantitative research extensions](quant-research/) contains supporting machine-learning analysis and reproducible code.
- [Disclosures](disclosures/) contains portfolio-wide risk and backtesting notes.

## Repository Structure

```text
systematic-trading-market-research/
  README.md
  .gitattributes
  trend-catcher_15m-v5.pine
  research-papers/
    README.md
    2026-06-10-covered-call-assignment-simulation.docx
    2026-06-10-covered-call-assignment-simulation-summary.md
    2026-06-30-spy-market-regime-clustering-lstm-report.md
  quant-research/
    README.md
    spy-market-regime-clustering-lstm/
      README.md
      run_pipeline.py
      requirements.txt
      notebooks/
      src/
      tests/
      outputs/
  tradingview/
    README.md
    trend-catcher-summary.md
  inactive-scripts/
    README.md
    only-long_dt-v4.pine
    only-long_dt-v5.pine
    only-long_options.pine
    trend-catcher_options-v1.pine
  temporarily-inactive-scripts/
    README.md
    trend-catcher_calls-v2.pine
    trend-catcher_options-v2.pine
  disclosures/
    disclaimer.md
    backtesting-limitations.md
```

Historical strategy files are organized by status so the active TREND-CATCHER [15m] script remains easy to find at the repository root.

## Review Path

For a fast review, start with the portfolio snapshot, then read the covered-call research summary, then review the featured TradingView strategy and public script link. The SPY regime project is supplementary evidence of K-Means and deep-learning experience; the existing options research and TREND-CATCHER strategy remain the primary portfolio artifacts.

## Disclaimer

This repository is for research and educational purposes only and is not financial advice. Trading and investing involve risk, and all results shown are based on defined assumptions that may not reflect live market performance. See [disclosures/disclaimer.md](disclosures/disclaimer.md) and [disclosures/backtesting-limitations.md](disclosures/backtesting-limitations.md).
