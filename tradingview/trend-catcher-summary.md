# TREND-CATCHER [15m]

TREND-CATCHER [15m] is a Pine Script strategy built for 15-minute chart analysis. It combines trend-state detection with stochastic oscillator confirmation to identify trend reversals and manage trades under defined backtest assumptions.

## Strategy Profile

| Area | Description |
|---|---|
| Platform | TradingView |
| Script type | Pine Script strategy |
| Timeframe | 15-minute chart analysis |
| Core logic | Trend-following bands, oscillator confirmation, dynamic thresholds |
| Trade management | Rule-based entries, exits, take-profit logic, and stop-loss logic |

## Objective

The strategy is designed to identify potential trend reversals on a 15-minute chart and manage trades using predefined entry, re-entry, and exit behavior. It combines market-state detection with oscillator confirmation so entries are not based on price movement alone.

## Methodology

- Radius Trend logic identifies market direction and adjusts dynamic bands as price action changes.
- Stochastic oscillator inputs help identify overbought and oversold conditions.
- Dynamic thresholds support trend-sensitive trade decisions rather than fixed price levels alone.
- Trade-management rules define entries, exits, profit targets, and stop-loss behavior.

## Execution Flow

1. Detect market state using the Radius Trend band calculation.
2. Confirm potential entry or exit conditions with stochastic oscillator thresholds.
3. Create visual labels for upcoming entries, re-entries, and limit levels.
4. Size entries from the configured strategy capital and optional profit reinvestment setting.
5. Manage exits through calculated limit and stop levels.

## Backtest Summary

Backtested across 50+ trades with Sharpe > 1.2, win rate > 85%, and ~35% annualized return under defined strategy assumptions.

These results should be interpreted as strategy-development research, not as a guarantee of future performance.

## Implementation Notes

- The active Pine Script is kept at the repository root for easy review.
- The public TradingView link is included for direct platform access.
- Earlier strategy variants are separated into archive folders to keep the featured implementation easy to find.
- The script was formatted for readability without changing trading logic.

## Resources

- [Public TradingView script](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/)
- [Active TREND-CATCHER Pine Script](../trend-catcher_15m-v5.pine)
- [TradingView strategy hub](README.md)

## Assumptions and Limitations

- Performance depends on the selected market, timeframe, execution assumptions, commissions, slippage, and TradingView backtest settings.
- Backtest results can change when strategy settings, data history, or market conditions change.
- Historical strategy variants are organized by status folders and are not part of the featured portfolio presentation.

## Disclaimer

This strategy summary is for research and educational purposes only and is not financial advice. Trading involves risk, including the possible loss of capital.
