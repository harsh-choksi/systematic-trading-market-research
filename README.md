# Systematic Trading & Market Research Portfolio

A focused research portfolio covering options strategy analysis, systematic trading logic, Pine Script development, and quantitative backtesting.

**Systematic Trading & Market Research Portfolio Link** | `github.com/harsh-choksi/systematic-trading-market-research`

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
| Jun 10, 2026 | [Sentiment-Adjusted Covered-Call Assignment Simulation](research-papers/2026-06-10-covered-call-assignment-simulation.docx) | Covered calls and assignment risk | Black-Scholes modeling, put/call sentiment inputs, strike-selection rules, assignment probability analysis | DOCX available; PDF pending |

The first paper is available as a Word document. A PDF version can be added later once export is available.

## Featured Strategy

The current featured strategy is TREND-CATCHER [15m], a TradingView Pine Script strategy focused on trend reversals, stochastic oscillator confirmation, and rule-based trade management.

## TradingView Strategy

### [TREND-CATCHER [15m]](tradingview/trend-catcher-summary.md)

Pine Script strategy using trend-following logic, stochastic oscillator signals, dynamic thresholds, and rule-based trade management.

Backtested across 50+ trades with Sharpe > 1.2, win rate > 85%, and ~35% annualized return under defined strategy assumptions.

| Resource | Link |
|---|---|
| Strategy summary | [View summary](tradingview/trend-catcher-summary.md) |
| Public TradingView script | [Open on TradingView](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/) |
| Pine Script source | [View active script](trend-catcher_15m-v5) |

## Archive Organization

Older strategy variants are retained for transparency and development history:

- [Inactive strategies](inactive/) contain retired or superseded scripts.
- [Temporarily inactive strategies](temporarily-inactive/) contain paused variants that may still inform future development.
- [Research papers](research-papers/) contains the market research archive.

## Repository Structure

```text
systematic-trading-market-research/
  README.md
  trend-catcher_15m-v5
  research-papers/
    README.md
    2026-06-10-covered-call-assignment-simulation.docx
  tradingview/
    trend-catcher-summary.md
  inactive/
    README.md
    only-long_dt-v4
    only-long_dt-v5
    only-long_options
    trend-catcher_options (v1)
  temporarily-inactive/
    README.md
    trend-catcher_calls (v2)
    trend-catcher_options (v2)
```

Historical strategy files are organized by status so the active TREND-CATCHER [15m] script remains easy to find at the repository root.

## Review Notes

For resume review, start with the research table, then review the featured TradingView strategy and its public script link. The archive folders are included for context, but the active strategy and research paper are the primary portfolio artifacts.

## Disclaimer

This repository is for research and educational purposes only and is not financial advice. Trading and investing involve risk, and all results shown are based on defined assumptions that may not reflect live market performance.
