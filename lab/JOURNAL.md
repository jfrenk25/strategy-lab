# Lab journal

Append-only. Every idea tested is logged here with its verdict and the reason it failed.

## Before the lab (November 14 to 19, 2026)

| Idea class | Attempts | Result |
|---|---|---|
| 90 indicator strategies, six markets, 15m / 1h / 4h, walk-forward | 90 | No pick rule above profit factor 1.0; zero-cost result 1.01 |
| Elliott flat setup on BTC 1h | 1 | 0 of 18 variants passed |
| Gold "market shift" scalp, mechanical version, 2009 to 2026 | 1 | 8 variants rejected; coin flip before costs |
| Funding fade, liquidation flush, late-leverage fade, paid-to-hold | 4 | All rejected; best profit factor 0.99 |

Attempt counter starts at 96.

## Lab runs

### 2026-11-19 · attempt 97 · `donchian_breakout` · REJECT
- Source: Textbook trend-following rule (Donchian channel)
- Reason claimed: Large moves start with a break of the recent range, and trends persist longer than chance.
- Who loses: Traders fading new highs and lows, and hedgers who must trade regardless of price.
- Out-of-sample: 3075 trades, profit factor 0.98, -36.2R, t-stat -0.45 (needed 3.28)
- Profitable test years 6 of 16; markets 4 of 6; double-cost profit factor 0.87; beats 97% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profit factor > 1 at double costs; t-stat >= 3.28 (bar for attempt 97)

### 2026-11-19 · attempt 98 · `rsi2_reversion` · REJECT
- Source: Textbook short-term mean-reversion rule (2-period RSI with a trend filter)
- Reason claimed: Short, sharp pullbacks inside a longer trend tend to snap back.
- Who loses: Traders who sell in panic on a short pullback, and stop orders placed too close.
- Out-of-sample: 3020 trades, profit factor 0.90, -213.2R, t-stat -2.56 (needed 3.28)
- Profitable test years 6 of 16; markets 0 of 6; double-cost profit factor 0.79; beats 31% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.28 (bar for attempt 98)

### 2026-11-19 · attempt 99 · `ts_momentum` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies, section 10.4 (after Moskowitz, Ooi and Pedersen, 2012)
- Reason claimed: Trends persist for months because information spreads slowly and investors adjust positions gradually.
- Who loses: Hedgers and slow movers who trade against a move that has not finished.
- Mode: position (daily weights across 6 markets)
- Out-of-sample: 4712 days in the market, Sharpe 0.05, total +9.9%, max drawdown -43.2%, t-stat 0.18 (needed 3.29)
- Profitable test years 10 of 16; markets contributing 3 of 6; double-cost total +1.7%; beats 11% of time-shifted copies
- Failed: Sharpe >= 0.8; beats 95% of time-shifted copies of itself; t-stat >= 3.29 (bar for attempt 99)

### 2026-11-19 · attempt 100 · `xs_contrarian` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies, section 10.3
- Reason claimed: Short-term moves away from the group partly reverse as temporary buying or selling pressure fades.
- Who loses: Traders who chase last week's leaders, and those forced to trade into a temporary imbalance.
- Mode: position (daily weights across 6 markets)
- Out-of-sample: 1461 days in the market, Sharpe 0.13, total +5.4%, max drawdown -13.4%, t-stat 0.25 (needed 3.29)
- Profitable test years 2 of 4; markets contributing 3 of 6; double-cost total -6.3%; beats 82% of time-shifted copies
- Failed: Sharpe >= 0.8; profitable in 60% of test years; still profitable at double costs; beats 95% of time-shifted copies of itself; t-stat >= 3.29 (bar for attempt 100)
