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

## Methodology

- Radius Trend logic identifies market direction and adjusts dynamic bands as price action changes.
- Stochastic oscillator inputs help identify overbought and oversold conditions.
- Dynamic thresholds support trend-sensitive trade decisions rather than fixed price levels alone.
- Trade-management rules define entries, exits, profit targets, and stop-loss behavior.

## Backtest Summary

Backtested across 50+ trades with Sharpe > 1.2, win rate > 85%, and ~35% annualized return under defined strategy assumptions.

These results should be interpreted as strategy-development research, not as a guarantee of future performance.

## Resources

- [Public TradingView script](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/)
- [Active TREND-CATCHER Pine Script](../trend-catcher_15m-v5%20%5BActive%5D)

## Assumptions and Limitations

- Performance depends on the selected market, timeframe, execution assumptions, commissions, slippage, and TradingView backtest settings.
- Backtest results can change when strategy settings, data history, or market conditions change.
- Additional historical strategy variants may remain in the repository for context, but they are not part of the featured portfolio presentation.

## Disclaimer

This strategy summary is for research and educational purposes only and is not financial advice. Trading involves risk, including the possible loss of capital.
