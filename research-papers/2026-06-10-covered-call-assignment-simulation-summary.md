# Sentiment-Adjusted Covered-Call Assignment Simulation

**Published:** June 10, 2026  
**Full paper:** [2026-06-10-covered-call-assignment-simulation.docx](2026-06-10-covered-call-assignment-simulation.docx)

## Abstract

This paper formalizes and stress-tests a weekly covered-call strategy for four high-volatility equity positions: RR, ONDS, POET, and USAR. The strategy sells one-week calls on Mondays only when the selected strike is at least the maximum of the modeled current stock price and the investor's average cost.

Among eligible strikes, the model chooses the highest strike whose modeled bid divided by strike is at least 1.38462%. Stock-price paths are modeled with a sentiment-adjusted geometric Brownian motion, option put/call volume modifies weekly drift, and call values are estimated with Black-Scholes before applying a modeled bid haircut.

## Methodology

The paper combines:

- Black-Scholes call pricing for weekly option valuation
- implied-volatility inputs to estimate weekly volatility
- put/call volume sentiment to adjust weekly drift
- a strict strike-selection rule that avoids below-cost assignment
- lognormal finish-above-strike assignment probability
- cumulative premium tracking and modeled profit if assigned

The assignment week reported in the main result is the week with the highest single-week modeled assignment probability under the final strike-selection rule.

## Model Inputs and Assumptions

| Input Area | Description |
|---|---|
| Positions | RR, ONDS, POET, and USAR |
| Strategy cadence | Weekly covered-call scan on Mondays |
| Strike floor | `max(modeled stock price, original average cost)` |
| Minimum premium rule | Modeled bid / strike must be at least 1.38462% |
| Volatility | Annualized implied volatility converted to weekly volatility |
| Sentiment | Put/call ratio translated into a capped weekly drift input |
| Bid estimate | Black-Scholes call value multiplied by 0.85, floored to cents |

## Key Modeled Outputs

| Ticker | Assignment Week | Selected Strike | Modeled Bid | Weekly Assignment Probability | Cumulative Premium / Share | Modeled Profit |
|---|---:|---:|---:|---:|---:|---:|
| RR | 13 | $4.00 | $0.14 | 43.02% | $0.31 | $3,922 |
| ONDS | 26 | $12.50 | $0.27 | 31.38% | $1.15 | $2,465 |
| POET | 5 | $13.50 | $0.27 | 26.85% | $1.13 | $6,664 |
| USAR | 59 | $27.00 | $0.56 | 29.11% | $5.59 | $2,256 |

## Interpretation

The model ranks POET as the strongest fit because it begins qualifying quickly, produces the earliest modeled assignment week, and combines premium income with above-cost assignment profit. RR ranks second due to strong modeled drift from call-heavy option flow, while ONDS and USAR are slower because above-cost strikes do not qualify until later in the modeled path.

## Limitations

- Black-Scholes assumes lognormal returns, constant volatility, frictionless markets, and European-style exercise.
- Listed equity options are generally American-style, so early exercise and real assignment behavior can differ.
- Actual option-chain bids, spreads, liquidity, and fill quality may differ materially from modeled bid assumptions.
- Put/call ratio is used as a controlled sentiment input, not as a guarantee of future direction.
- Results must be refreshed with current prices, implied volatility, put/call volume, and actual option-chain bids.

## Practical Checklist

The paper recommends refreshing live stock price, implied volatility, put/call volume, exact share count, and same-week option-chain bids before applying the strategy. If no above-cost strike satisfies the premium rule, the baseline model skips the trade rather than lowering the strike below average cost.

## Disclaimer

This summary is for research and educational purposes only and is not financial advice. Trading options involves risk, and modeled results may not reflect live execution, assignment behavior, liquidity, taxes, or broker constraints.
