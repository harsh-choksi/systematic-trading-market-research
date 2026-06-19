# TREND-CATCHER [15m]

TREND-CATCHER [15m] is a Pine Script strategy focused on identifying trend reversals and managing trades with dynamic market conditions.

## Strategy Overview

The strategy combines trend-state detection with oscillator-based confirmation. It is designed for 15-minute chart analysis and uses rule-based entries, exits, and trade management.

## Indicators and Logic

- Radius Trend logic identifies market direction and adjusts dynamic bands as price action changes.
- Stochastic oscillator inputs help identify overbought and oversold conditions for potential entries and exits.
- Dynamic thresholds support trend-sensitive trade decisions rather than relying on fixed price levels alone.
- Trade management includes take-profit and stop-loss logic under defined strategy assumptions.

## Backtest Summary

Backtested across 50+ trades with Sharpe > 1.2, win rate > 85%, and ~35% annualized return under defined strategy assumptions.

These results should be interpreted as research and strategy-development output, not as a guarantee of future performance.

## Source

- [Public TradingView script](https://www.tradingview.com/script/KzwlYoYT-TREND-CATCHER-15m/)
- [Active TREND-CATCHER Pine Script](../trend-catcher_15m-v5%20%5BActive%5D)

## Assumptions and Limitations

- Performance depends on the selected market, timeframe, execution assumptions, commissions, slippage, and TradingView backtest settings.
- Backtest results can change when strategy settings, data history, or market conditions change.
- The inactive strategy variants in this repository are not part of the current featured portfolio presentation.

## Disclaimer

This strategy summary is for research and educational purposes only and is not financial advice. Trading involves risk, including the possible loss of capital.
