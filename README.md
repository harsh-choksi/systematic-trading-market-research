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

The full paper is available as a Word document, with a Markdown summary provided for quick review. A PDF version can be added later once export is available.

## Featured Strategy

The current featured strategy is TREND-CATCHER [15m], a TradingView Pine Script strategy focused on trend reversals, stochastic oscillator confirmation, and rule-based trade management.

| Resource | Link |
|---|---|
| Strategy hub | [TradingView strategy archive](tradingview/) |
| Strategy summary | [View summary](tradingview/trend-catcher-summary.md) |
| Public TradingView script | [Open on TradingView](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/) |
| Pine Script source | [View active script](trend-catcher_15m-v5.pine) |

## Methodology

This portfolio separates research artifacts from strategy implementation:

- Research papers document model assumptions, inputs, outputs, limitations, and risk controls.
- TradingView scripts show implementation work and strategy-development iterations.
- Archive folders preserve earlier variants without distracting from the featured strategy.
- Disclosures and backtesting notes clarify that modeled or backtested results are conditional on assumptions.

## Archive Organization

Older strategy variants are retained for transparency and development history:

- [Inactive scripts](inactive-scripts/) contain retired or superseded strategy files.
- [Temporarily inactive scripts](temporarily-inactive-scripts/) contain paused variants that may still inform future development.
- [Research papers](research-papers/) contains the market research archive.
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

For a fast review, start with the portfolio snapshot, then read the research paper summary, then review the featured TradingView strategy and public script link. The archive folders are included for context, but the active strategy and research paper are the primary portfolio artifacts.

## Disclaimer

This repository is for research and educational purposes only and is not financial advice. Trading and investing involve risk, and all results shown are based on defined assumptions that may not reflect live market performance. See [disclosures/disclaimer.md](disclosures/disclaimer.md) and [disclosures/backtesting-limitations.md](disclosures/backtesting-limitations.md).
