# Systematic Trading & Market Research Portfolio

A focused research portfolio covering options strategy analysis, systematic trading logic, Pine Script development, and quantitative backtesting.

**Systematic Trading & Market Research Portfolio Link** | `github.com/harsh-choksi/systematic-trading-market-research`

## Overview

This repository is organized as a public archive for market research papers and strategy-development work. It is designed to serve as a polished GitHub landing page for resume reviewers, recruiters, and anyone evaluating the research process behind the projects.

## Research Papers

| Date | Paper | Focus | Methods | Status |
|---|---|---|---|---|
| Jun 2026 | Sentiment-Adjusted Covered-Call Assignment Simulation | Covered calls and assignment risk | Black-Scholes modeling, put/call sentiment inputs, strike-selection rules, assignment probability analysis | PDF pending final export |

The first paper will be published at `research-papers/covered-call-assignment-simulation.pdf` once the final PDF export is available.

## TradingView Strategy

### [TREND-CATCHER [15m]](tradingview/trend-catcher-summary.md)

Pine Script strategy using trend-following logic, stochastic oscillator signals, dynamic thresholds, and rule-based trade management.

Backtested across 50+ trades with Sharpe > 1.2, win rate > 85%, and ~35% annualized return under defined strategy assumptions.

| Resource | Link |
|---|---|
| Strategy summary | [View summary](tradingview/trend-catcher-summary.md) |
| Public TradingView script | [Open on TradingView](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/) |
| Pine Script source | [View active script](trend-catcher_15m-v5) |

## Repository Structure

```text
systematic-trading-market-research/
  README.md
  trend-catcher_15m-v5
  research-papers/
    covered-call-assignment-simulation.pdf
  tradingview/
    trend-catcher-summary.md
  inactive/
    only-long_dt-v4
    only-long_dt-v5
    only-long_options
    trend-catcher_options (v1)
  temporarily-inactive/
    trend-catcher_calls (v2)
    trend-catcher_options (v2)
```

Historical strategy files are organized by status so the active TREND-CATCHER [15m] script remains easy to find at the repository root.

## Disclaimer

This repository is for research and educational purposes only and is not financial advice. Trading and investing involve risk, and all results shown are based on defined assumptions that may not reflect live market performance.
