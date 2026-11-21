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

### 2026-11-20 · screen survivor 1 · `zmove_n24_z2.5.follow.none.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id bf95d1fc89). No stated reason.
- Screen years: 810 trades, profit factor 1.31, t-stat 3.81
- Confirm years: 376 trades, profit factor 0.97, -6.0R, t-stat -0.25 (needed 1.64); markets 3 of 6; double-cost profit factor 0.90; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 1.64 (bar for survivor 1)

### 2026-11-20 · screen batch · 100 ideas
- Passed the screen: 1. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 100 of 4000 catalogue ideas screened, 1 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-20 · screen rule amended
- The survivor bar now counts survivors as 20 until the real count passes 20 (bar of about 2.81 or higher). See `LAB_RULES.md`.
- Survivor 1 above was judged against 1.64 and failed at -0.25. It fails under the amended bar too.

### 2026-11-20 · screen batch · 100 ideas
- Passed the screen: 0. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 200 of 4000 catalogue ideas screened, 1 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-20 · screen survivor 2 · `big_bar_k2.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 5e1407c2e7). No stated reason.
- Screen years: 435 trades, profit factor 1.19, t-stat 1.66
- Confirm years: 249 trades, profit factor 1.04, +7.5R, t-stat 0.30 (needed 2.81); markets 3 of 6; double-cost profit factor 0.94; beats 68% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 2)

### 2026-11-20 · screen survivor 3 · `breakout_n168.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id d5f7529a14). No stated reason.
- Screen years: 661 trades, profit factor 1.15, t-stat 1.69
- Confirm years: 289 trades, profit factor 1.42, +81.7R, t-stat 2.78 (needed 2.81); markets 5 of 6; double-cost profit factor 1.30; beats 100% of random entries
- Failed: t-stat >= 2.81 (bar for survivor 3)

### 2026-11-20 · screen survivor 4 · `zmove_n24_z2.follow.none.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 00cf641ebe). No stated reason.
- Screen years: 1289 trades, profit factor 1.15, t-stat 2.25
- Confirm years: 573 trades, profit factor 1.20, +77.0R, t-stat 1.97 (needed 2.81); markets 4 of 6; double-cost profit factor 1.11; beats 99% of random entries
- Failed: t-stat >= 2.81 (bar for survivor 4)

### 2026-11-20 · screen survivor 5 · `zmove_n72_z2.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id ef57d5c967). No stated reason.
- Screen years: 731 trades, profit factor 1.14, t-stat 1.66
- Confirm years: 338 trades, profit factor 1.16, +39.4R, t-stat 1.26 (needed 2.81); markets 4 of 6; double-cost profit factor 1.07; beats 90% of random entries
- Failed: beats 95% of random entries; t-stat >= 2.81 (bar for survivor 5)

### 2026-11-20 · screen survivor 6 · `squeeze_break_n72.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id ad74896660). No stated reason.
- Screen years: 244 trades, profit factor 1.28, t-stat 1.80
- Confirm years: 116 trades, profit factor 1.05, +4.4R, t-stat 0.25 (needed 2.81); markets 3 of 6; double-cost profit factor 0.95; beats 51% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 6)

### 2026-11-20 · screen survivor 7 · `zmove_n72_z2.follow.high_vol.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 8cec3ab818). No stated reason.
- Screen years: 723 trades, profit factor 1.19, t-stat 2.27
- Confirm years: 336 trades, profit factor 1.07, +13.3R, t-stat 0.58 (needed 2.81); markets 4 of 6; double-cost profit factor 0.98; beats 94% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 7)

### 2026-11-20 · screen survivor 8 · `big_bar_k2.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 4e93361ea0). No stated reason.
- Screen years: 538 trades, profit factor 1.20, t-stat 2.05
- Confirm years: 269 trades, profit factor 1.20, +29.8R, t-stat 1.45 (needed 2.81); markets 4 of 6; double-cost profit factor 1.09; beats 97% of random entries
- Failed: t-stat >= 2.81 (bar for survivor 8)

### 2026-11-20 · screen survivor 9 · `zmove_n24_z2.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id c0d577564d). No stated reason.
- Screen years: 355 trades, profit factor 1.26, t-stat 1.99
- Confirm years: 168 trades, profit factor 1.43, +47.3R, t-stat 2.12 (needed 2.81); markets 3 of 6; double-cost profit factor 1.33; beats 97% of random entries
- Failed: t-stat >= 2.81 (bar for survivor 9)

### 2026-11-20 · screen survivor 10 · `clock_hour20_weekday-1.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 9d9e56acbd). No stated reason.
- Screen years: 1120 trades, profit factor 1.15, t-stat 2.21
- Confirm years: 607 trades, profit factor 1.15, +63.2R, t-stat 1.54 (needed 2.81); markets 5 of 6; double-cost profit factor 1.06; beats 38% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 10)

### 2026-11-20 · screen survivor 11 · `squeeze_break_n72.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a6e6e34133). No stated reason.
- Screen years: 451 trades, profit factor 1.19, t-stat 1.69
- Confirm years: 185 trades, profit factor 0.95, -6.7R, t-stat -0.30 (needed 2.81); markets 3 of 6; double-cost profit factor 0.86; beats 30% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 11)

### 2026-11-20 · screen survivor 12 · `zmove_n24_z2.5.follow.none.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 3e592b6b0b). No stated reason.
- Screen years: 488 trades, profit factor 1.50, t-stat 4.42
- Confirm years: 211 trades, profit factor 0.96, -5.4R, t-stat -0.30 (needed 2.81); markets 2 of 6; double-cost profit factor 0.89; beats 70% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 12)

### 2026-11-20 · screen survivor 13 · `big_bar_k3.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a769b9af48). No stated reason.
- Screen years: 1195 trades, profit factor 1.16, t-stat 2.31
- Confirm years: 460 trades, profit factor 1.14, +46.5R, t-stat 1.31 (needed 2.81); markets 3 of 6; double-cost profit factor 1.05; beats 94% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 13)

### 2026-11-20 · screen survivor 14 · `vol_spike_k2.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a9b2fb1dab). No stated reason.
- Screen years: 437 trades, profit factor 1.24, t-stat 2.02
- Confirm years: 234 trades, profit factor 1.09, +13.8R, t-stat 0.59 (needed 2.81); markets 2 of 6; double-cost profit factor 1.04; beats 82% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 14)

### 2026-11-20 · screen survivor 15 · `zmove_n24_z2.5.follow.high_vol.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 139a54bf21). No stated reason.
- Screen years: 764 trades, profit factor 1.30, t-stat 3.63
- Confirm years: 355 trades, profit factor 0.93, -16.2R, t-stat -0.70 (needed 2.81); markets 3 of 6; double-cost profit factor 0.86; beats 65% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 15)

### 2026-11-20 · screen survivor 16 · `zmove_n24_z2.5.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 95a6546d06). No stated reason.
- Screen years: 217 trades, profit factor 1.66, t-stat 3.47
- Confirm years: 107 trades, profit factor 1.26, +19.3R, t-stat 1.10 (needed 2.81); markets 5 of 6; double-cost profit factor 1.16; beats 94% of random entries
- Failed: beats 95% of random entries; t-stat >= 2.81 (bar for survivor 16)

### 2026-11-20 · screen survivor 17 · `zmove_n24_z2.5.follow.none.ny.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 359647fb12). No stated reason.
- Screen years: 505 trades, profit factor 1.23, t-stat 2.32
- Confirm years: 221 trades, profit factor 0.99, -1.5R, t-stat -0.08 (needed 2.81); markets 3 of 6; double-cost profit factor 0.89; beats 87% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 17)

### 2026-11-20 · screen survivor 18 · `zmove_n24_z2.5.follow.with_trend.ny.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a032412448). No stated reason.
- Screen years: 421 trades, profit factor 1.20, t-stat 1.81
- Confirm years: 179 trades, profit factor 1.01, +0.7R, t-stat 0.04 (needed 2.81); markets 3 of 6; double-cost profit factor 0.90; beats 85% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 18)

### 2026-11-20 · screen survivor 19 · `zmove_n24_z2.5.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 759518987a). No stated reason.
- Screen years: 254 trades, profit factor 1.49, t-stat 2.95
- Confirm years: 133 trades, profit factor 1.22, +20.0R, t-stat 1.03 (needed 2.81); markets 4 of 6; double-cost profit factor 1.11; beats 94% of random entries
- Failed: beats 95% of random entries; t-stat >= 2.81 (bar for survivor 19)

### 2026-11-20 · screen survivor 20 · `zmove_n24_z2.5.follow.high_vol.ny.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 4d844720cf). No stated reason.
- Screen years: 471 trades, profit factor 1.18, t-stat 1.76
- Confirm years: 208 trades, profit factor 0.99, -1.8R, t-stat -0.10 (needed 2.81); markets 4 of 6; double-cost profit factor 0.89; beats 88% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.81 (bar for survivor 20)

### 2026-11-20 · screen survivor 21 · `zmove_n24_z2.5.follow.none.any.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 2b4edc3b15). No stated reason.
- Screen years: 884 trades, profit factor 1.15, t-stat 2.11
- Confirm years: 406 trades, profit factor 0.97, -8.6R, t-stat -0.34 (needed 2.82); markets 3 of 6; double-cost profit factor 0.87; beats 91% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.82 (bar for survivor 21)

### 2026-11-20 · screen survivor 22 · `zmove_n24_z2.5.follow.with_trend.any.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id e802b56c1a). No stated reason.
- Screen years: 730 trades, profit factor 1.16, t-stat 1.99
- Confirm years: 326 trades, profit factor 0.98, -3.7R, t-stat -0.16 (needed 2.84); markets 3 of 6; double-cost profit factor 0.88; beats 89% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.84 (bar for survivor 22)

### 2026-11-20 · screen survivor 23 · `zmove_n24_z2.5.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 79af0a1dae). No stated reason.
- Screen years: 405 trades, profit factor 1.53, t-stat 4.25
- Confirm years: 172 trades, profit factor 1.03, +2.8R, t-stat 0.17 (needed 2.85); markets 4 of 6; double-cost profit factor 0.95; beats 77% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.85 (bar for survivor 23)

### 2026-11-20 · screen survivor 24 · `zmove_n24_z2.5.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id d5c9d133ea). No stated reason.
- Screen years: 240 trades, profit factor 1.49, t-stat 3.08
- Confirm years: 123 trades, profit factor 0.94, -4.6R, t-stat -0.34 (needed 2.87); markets 1 of 6; double-cost profit factor 0.88; beats 61% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.87 (bar for survivor 24)

### 2026-11-20 · screen survivor 25 · `zmove_n24_z2.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a96089f9e9). No stated reason.
- Screen years: 154 trades, profit factor 1.34, t-stat 1.66
- Confirm years: 61 trades, profit factor 1.06, +2.7R, t-stat 0.20 (needed 2.88); markets 3 of 6; double-cost profit factor 0.95; beats 52% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.88 (bar for survivor 25)

### 2026-11-20 · screen survivor 26 · `big_bar_k3.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 4748263e62). No stated reason.
- Screen years: 255 trades, profit factor 1.41, t-stat 2.74
- Confirm years: 144 trades, profit factor 1.02, +1.5R, t-stat 0.10 (needed 2.89); markets 3 of 6; double-cost profit factor 0.94; beats 80% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.89 (bar for survivor 26)

### 2026-11-20 · screen survivor 27 · `breakout_n72.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id d1f624eb0c). No stated reason.
- Screen years: 870 trades, profit factor 1.18, t-stat 2.28
- Confirm years: 395 trades, profit factor 1.28, +75.4R, t-stat 2.24 (needed 2.90); markets 6 of 6; double-cost profit factor 1.17; beats 98% of random entries
- Failed: t-stat >= 2.90 (bar for survivor 27)

### 2026-11-20 · screen survivor 28 · `vol_spike_k3.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 10ba9de10d). No stated reason.
- Screen years: 200 trades, profit factor 1.35, t-stat 2.10
- Confirm years: 104 trades, profit factor 1.08, +4.9R, t-stat 0.39 (needed 2.91); markets 3 of 6; double-cost profit factor 1.04; beats 78% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 2.91 (bar for survivor 28)

### 2026-11-20 · screen survivor 29 · `big_bar_k3.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 373c606198). No stated reason.
- Screen years: 1365 trades, profit factor 1.14, t-stat 2.31
- Confirm years: 519 trades, profit factor 1.11, +32.6R, t-stat 1.13 (needed 2.92); markets 3 of 6; double-cost profit factor 1.00; beats 98% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 2.92 (bar for survivor 29)

### 2026-11-20 · screen survivor 30 · `big_bar_k2.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id e91b55fcab). No stated reason.
- Screen years: 1594 trades, profit factor 1.12, t-stat 2.12
- Confirm years: 699 trades, profit factor 1.07, +35.2R, t-stat 0.81 (needed 2.94); markets 3 of 6; double-cost profit factor 0.98; beats 85% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.94 (bar for survivor 30)

### 2026-11-20 · screen survivor 31 · `big_bar_k3.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 1c272478ea). No stated reason.
- Screen years: 256 trades, profit factor 1.26, t-stat 1.73
- Confirm years: 144 trades, profit factor 1.06, +6.2R, t-stat 0.31 (needed 2.95); markets 3 of 6; double-cost profit factor 0.96; beats 85% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.95 (bar for survivor 31)

### 2026-11-20 · screen survivor 32 · `zmove_n24_z2.follow.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 229db4cc9e). No stated reason.
- Screen years: 676 trades, profit factor 1.16, t-stat 1.70
- Confirm years: 310 trades, profit factor 1.09, +19.1R, t-stat 0.67 (needed 2.96); markets 3 of 6; double-cost profit factor 1.02; beats 88% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 2.96 (bar for survivor 32)

### 2026-11-20 · screen survivor 33 · `zmove_n24_z2.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id b960fe78cd). No stated reason.
- Screen years: 649 trades, profit factor 1.18, t-stat 2.08
- Confirm years: 306 trades, profit factor 0.87, -26.4R, t-stat -1.22 (needed 2.96); markets 2 of 6; double-cost profit factor 0.80; beats 32% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.96 (bar for survivor 33)

### 2026-11-20 · screen survivor 34 · `big_bar_k2.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id d074413504). No stated reason.
- Screen years: 776 trades, profit factor 1.16, t-stat 1.85
- Confirm years: 421 trades, profit factor 1.04, +10.9R, t-stat 0.34 (needed 2.97); markets 4 of 6; double-cost profit factor 0.95; beats 75% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.97 (bar for survivor 34)

### 2026-11-20 · screen survivor 35 · `zmove_n24_z2.5.follow.high_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a7ca51ac6f). No stated reason.
- Screen years: 682 trades, profit factor 1.34, t-stat 3.45
- Confirm years: 325 trades, profit factor 1.04, +9.5R, t-stat 0.33 (needed 2.98); markets 4 of 6; double-cost profit factor 0.98; beats 80% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.98 (bar for survivor 35)

### 2026-11-20 · screen survivor 36 · `vol_spike_k3.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 6d25eec9f3). No stated reason.
- Screen years: 192 trades, profit factor 1.63, t-stat 3.07
- Confirm years: 100 trades, profit factor 0.84, -11.6R, t-stat -0.80 (needed 2.99); markets 1 of 6; double-cost profit factor 0.80; beats 28% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 2.99 (bar for survivor 36)

### 2026-11-20 · screen survivor 37 · `big_bar_k3.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 3fad6108aa). No stated reason.
- Screen years: 758 trades, profit factor 1.18, t-stat 2.08
- Confirm years: 284 trades, profit factor 0.88, -25.8R, t-stat -0.96 (needed 3.00); markets 1 of 6; double-cost profit factor 0.81; beats 27% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.00 (bar for survivor 37)

### 2026-11-20 · screen survivor 38 · `zmove_n24_z2.5.follow.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 13d15d69a5). No stated reason.
- Screen years: 419 trades, profit factor 1.37, t-stat 2.96
- Confirm years: 192 trades, profit factor 1.08, +11.1R, t-stat 0.49 (needed 3.01); markets 3 of 6; double-cost profit factor 1.02; beats 83% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.01 (bar for survivor 38)

### 2026-11-20 · screen survivor 39 · `big_bar_k3.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id be528f983b). No stated reason.
- Screen years: 251 trades, profit factor 1.41, t-stat 2.47
- Confirm years: 140 trades, profit factor 1.23, +21.7R, t-stat 1.10 (needed 3.02); markets 5 of 6; double-cost profit factor 1.15; beats 95% of random entries
- Failed: t-stat >= 3.02 (bar for survivor 39)

### 2026-11-20 · screen survivor 40 · `vol_spike_k3.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 03f297087c). No stated reason.
- Screen years: 206 trades, profit factor 1.44, t-stat 2.39
- Confirm years: 105 trades, profit factor 0.90, -7.5R, t-stat -0.48 (needed 3.02); markets 2 of 6; double-cost profit factor 0.85; beats 48% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.02 (bar for survivor 40)

### 2026-11-20 · screen survivor 41 · `zmove_n24_z2.5.follow.high_vol.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a1cc210dca). No stated reason.
- Screen years: 460 trades, profit factor 1.24, t-stat 2.15
- Confirm years: 199 trades, profit factor 1.08, +11.0R, t-stat 0.47 (needed 3.03); markets 4 of 6; double-cost profit factor 0.98; beats 90% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.03 (bar for survivor 41)

### 2026-11-20 · screen survivor 42 · `zmove_n24_z2.5.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id f4a5852e9a). No stated reason.
- Screen years: 215 trades, profit factor 1.59, t-stat 3.38
- Confirm years: 107 trades, profit factor 1.06, +3.6R, t-stat 0.28 (needed 3.04); markets 4 of 6; double-cost profit factor 0.99; beats 75% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.04 (bar for survivor 42)

### 2026-11-20 · screen survivor 43 · `clock_hour0_weekday4.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 6065a7dff0). No stated reason.
- Screen years: 679 trades, profit factor 1.17, t-stat 1.88
- Confirm years: 316 trades, profit factor 1.30, +66.1R, t-stat 2.14 (needed 3.05); markets 5 of 6; double-cost profit factor 1.18; beats 83% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.05 (bar for survivor 43)

### 2026-11-20 · screen survivor 44 · `vol_spike_k3.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 002180cfb1). No stated reason.
- Screen years: 201 trades, profit factor 1.36, t-stat 1.97
- Confirm years: 119 trades, profit factor 1.31, +24.5R, t-stat 1.34 (needed 3.05); markets 3 of 6; double-cost profit factor 1.25; beats 92% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.05 (bar for survivor 44)

### 2026-11-20 · screen survivor 45 · `zmove_n72_z2.follow.high_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 5a57fa9cad). No stated reason.
- Screen years: 638 trades, profit factor 1.20, t-stat 2.14
- Confirm years: 297 trades, profit factor 1.18, +37.4R, t-stat 1.30 (needed 3.06); markets 3 of 6; double-cost profit factor 1.10; beats 96% of random entries
- Failed: t-stat >= 3.06 (bar for survivor 45)

### 2026-11-20 · screen survivor 46 · `zmove_n24_z2.5.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 4e6833b069). No stated reason.
- Screen years: 242 trades, profit factor 1.44, t-stat 2.61
- Confirm years: 123 trades, profit factor 1.07, +6.6R, t-stat 0.36 (needed 3.07); markets 3 of 6; double-cost profit factor 0.99; beats 84% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.07 (bar for survivor 46)

### 2026-11-20 · screen survivor 47 · `big_bar_k2.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id a7c18e099b). No stated reason.
- Screen years: 379 trades, profit factor 1.24, t-stat 2.08
- Confirm years: 208 trades, profit factor 0.95, -5.9R, t-stat -0.34 (needed 3.07); markets 3 of 6; double-cost profit factor 0.89; beats 63% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.07 (bar for survivor 47)

### 2026-11-20 · screen survivor 48 · `zmove_n24_z2.5.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 44419fd0ec). No stated reason.
- Screen years: 409 trades, profit factor 1.38, t-stat 3.03
- Confirm years: 173 trades, profit factor 1.20, +24.0R, t-stat 1.08 (needed 3.08); markets 4 of 6; double-cost profit factor 1.09; beats 96% of random entries
- Failed: t-stat >= 3.08 (bar for survivor 48)

### 2026-11-20 · screen survivor 49 · `zmove_n72_z2.follow.none.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 70d3fb53c3). No stated reason.
- Screen years: 818 trades, profit factor 1.16, t-stat 1.98
- Confirm years: 374 trades, profit factor 1.10, +27.0R, t-stat 0.84 (needed 3.08); markets 4 of 6; double-cost profit factor 1.02; beats 83% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.08 (bar for survivor 49)

### 2026-11-20 · screen survivor 50 · `zmove_n24_z2.5.follow.high_vol.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id d8c2a34d4d). No stated reason.
- Screen years: 787 trades, profit factor 1.19, t-stat 2.20
- Confirm years: 358 trades, profit factor 1.06, +16.5R, t-stat 0.53 (needed 3.09); markets 4 of 6; double-cost profit factor 0.97; beats 94% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.09 (bar for survivor 50)

### 2026-11-20 · screen survivor 51 · `zmove_n24_z2.5.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 99f5d073b7). No stated reason.
- Screen years: 667 trades, profit factor 1.32, t-stat 3.52
- Confirm years: 302 trades, profit factor 1.01, +1.9R, t-stat 0.09 (needed 3.10); markets 2 of 6; double-cost profit factor 0.94; beats 84% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.10 (bar for survivor 51)

### 2026-11-20 · screen survivor 52 · `zmove_n24_z2.5.follow.with_trend.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 1e29f84414). No stated reason.
- Screen years: 220 trades, profit factor 1.33, t-stat 2.11
- Confirm years: 111 trades, profit factor 1.11, +7.3R, t-stat 0.55 (needed 3.10); markets 5 of 6; double-cost profit factor 1.01; beats 90% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.10 (bar for survivor 52)

### 2026-11-20 · screen survivor 53 · `zmove_n24_z2.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 0474cdab48). No stated reason.
- Screen years: 1123 trades, profit factor 1.11, t-stat 1.74
- Confirm years: 501 trades, profit factor 0.99, -4.6R, t-stat -0.17 (needed 3.11); markets 2 of 6; double-cost profit factor 0.90; beats 76% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.11 (bar for survivor 53)

### 2026-11-20 · screen survivor 54 · `zmove_n24_z2.5.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 9feaa06be3). No stated reason.
- Screen years: 242 trades, profit factor 1.42, t-stat 2.49
- Confirm years: 128 trades, profit factor 1.25, +21.9R, t-stat 1.16 (needed 3.11); markets 5 of 6; double-cost profit factor 1.18; beats 94% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.11 (bar for survivor 54)

### 2026-11-20 · screen survivor 55 · `big_bar_k3.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 684f2f77bc). No stated reason.
- Screen years: 836 trades, profit factor 1.14, t-stat 1.90
- Confirm years: 307 trades, profit factor 0.89, -22.1R, t-stat -1.00 (needed 3.12); markets 2 of 6; double-cost profit factor 0.80; beats 44% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.12 (bar for survivor 55)

### 2026-11-20 · screen survivor 56 · `zmove_n24_z2.5.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 7c734c694e). No stated reason.
- Screen years: 595 trades, profit factor 1.30, t-stat 2.94
- Confirm years: 276 trades, profit factor 1.13, +26.0R, t-stat 0.95 (needed 3.12); markets 4 of 6; double-cost profit factor 1.06; beats 90% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.12 (bar for survivor 56)

### 2026-11-20 · screen survivor 57 · `zmove_n24_z2.5.follow.none.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 9ddbbca581). No stated reason.
- Screen years: 726 trades, profit factor 1.34, t-stat 3.59
- Confirm years: 344 trades, profit factor 1.10, +24.1R, t-stat 0.80 (needed 3.13); markets 4 of 6; double-cost profit factor 1.03; beats 90% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.13 (bar for survivor 57)

### 2026-11-20 · screen survivor 58 · `zmove_n24_z2.5.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 0224cd7dec). No stated reason.
- Screen years: 252 trades, profit factor 1.51, t-stat 3.24
- Confirm years: 133 trades, profit factor 1.06, +4.7R, t-stat 0.32 (needed 3.13); markets 4 of 6; double-cost profit factor 0.99; beats 82% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.13 (bar for survivor 58)

### 2026-11-20 · screen survivor 59 · `zmove_n24_z2.5.follow.high_vol.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id df5a1a04bf). No stated reason.
- Screen years: 456 trades, profit factor 1.43, t-stat 3.80
- Confirm years: 198 trades, profit factor 0.91, -11.4R, t-stat -0.66 (needed 3.14); markets 2 of 6; double-cost profit factor 0.85; beats 53% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.14 (bar for survivor 59)

### 2026-11-20 · screen survivor 60 · `zmove_n72_z2.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id ab7e1caa53). No stated reason.
- Screen years: 266 trades, profit factor 1.31, t-stat 2.19
- Confirm years: 123 trades, profit factor 1.05, +3.6R, t-stat 0.26 (needed 3.14); markets 2 of 6; double-cost profit factor 0.98; beats 77% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.14 (bar for survivor 60)

### 2026-11-20 · screen survivor 61 · `breakout_n24.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 3b9ab60428). No stated reason.
- Screen years: 1275 trades, profit factor 1.13, t-stat 2.05
- Confirm years: 559 trades, profit factor 1.25, +94.4R, t-stat 2.38 (needed 3.15); markets 6 of 6; double-cost profit factor 1.14; beats 99% of random entries
- Failed: t-stat >= 3.15 (bar for survivor 61)

### 2026-11-20 · screen survivor 62 · `zmove_n24_z2.5.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id ef3791d00e). No stated reason.
- Screen years: 231 trades, profit factor 1.37, t-stat 2.20
- Confirm years: 118 trades, profit factor 1.14, +11.7R, t-stat 0.65 (needed 3.15); markets 5 of 6; double-cost profit factor 1.08; beats 85% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.15 (bar for survivor 62)

### 2026-11-20 · screen survivor 63 · `zmove_n24_z2.5.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 2a1f6a6e72). No stated reason.
- Screen years: 204 trades, profit factor 1.47, t-stat 2.54
- Confirm years: 103 trades, profit factor 1.27, +18.6R, t-stat 1.09 (needed 3.16); markets 5 of 6; double-cost profit factor 1.19; beats 89% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.16 (bar for survivor 63)

### 2026-11-20 · screen survivor 64 · `clock_hour0_weekday4.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id c628c7fb75). No stated reason.
- Screen years: 783 trades, profit factor 1.13, t-stat 1.74
- Confirm years: 353 trades, profit factor 1.07, +15.5R, t-stat 0.63 (needed 3.16); markets 3 of 6; double-cost profit factor 0.96; beats 56% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.16 (bar for survivor 64)

### 2026-11-20 · screen survivor 65 · `big_bar_k3.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 21a1890074). No stated reason.
- Screen years: 178 trades, profit factor 1.35, t-stat 1.96
- Confirm years: 103 trades, profit factor 1.12, +7.4R, t-stat 0.58 (needed 3.17); markets 3 of 6; double-cost profit factor 1.05; beats 86% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.17 (bar for survivor 65)

### 2026-11-20 · screen survivor 66 · `zmove_n24_z2.5.follow.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id eb72b15884). No stated reason.
- Screen years: 450 trades, profit factor 1.42, t-stat 3.39
- Confirm years: 206 trades, profit factor 1.17, +24.6R, t-stat 1.04 (needed 3.17); markets 4 of 6; double-cost profit factor 1.10; beats 92% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.17 (bar for survivor 66)

### 2026-11-20 · screen survivor 67 · `zmove_n24_z2.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 38fce7e128). No stated reason.
- Screen years: 276 trades, profit factor 1.30, t-stat 2.02
- Confirm years: 119 trades, profit factor 1.03, +2.6R, t-stat 0.14 (needed 3.18); markets 2 of 6; double-cost profit factor 0.92; beats 46% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.18 (bar for survivor 67)

### 2026-11-20 · screen survivor 68 · `zmove_n24_z2.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 6eb933dc24). No stated reason.
- Screen years: 376 trades, profit factor 1.19, t-stat 1.68
- Confirm years: 181 trades, profit factor 1.12, +12.3R, t-stat 0.73 (needed 3.18); markets 4 of 6; double-cost profit factor 1.03; beats 85% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.18 (bar for survivor 68)

### 2026-11-20 · screen survivor 69 · `zmove_n24_z2.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 8977a9d333). No stated reason.
- Screen years: 487 trades, profit factor 1.18, t-stat 1.79
- Confirm years: 247 trades, profit factor 1.13, +17.9R, t-stat 0.91 (needed 3.18); markets 3 of 6; double-cost profit factor 1.04; beats 94% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.18 (bar for survivor 69)

### 2026-11-20 · screen survivor 70 · `zmove_n24_z2.5.follow.against_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id bcbd3b943e). No stated reason.
- Screen years: 154 trades, profit factor 1.35, t-stat 1.84
- Confirm years: 81 trades, profit factor 0.86, -7.3R, t-stat -0.66 (needed 3.19); markets 3 of 6; double-cost profit factor 0.80; beats 58% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.19 (bar for survivor 70)

### 2026-11-20 · screen survivor 71 · `zmove_n24_z2.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 0fc5487cf2). No stated reason.
- Screen years: 991 trades, profit factor 1.16, t-stat 2.16
- Confirm years: 439 trades, profit factor 1.17, +53.3R, t-stat 1.52 (needed 3.19); markets 4 of 6; double-cost profit factor 1.08; beats 97% of random entries
- Failed: t-stat >= 3.19 (bar for survivor 71)

### 2026-11-20 · screen survivor 72 · `vol_spike_k2.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 80fa06b2fc). No stated reason.
- Screen years: 480 trades, profit factor 1.17, t-stat 1.70
- Confirm years: 262 trades, profit factor 1.16, +24.2R, t-stat 1.20 (needed 3.20); markets 2 of 6; double-cost profit factor 1.09; beats 95% of random entries
- Failed: profitable in half the markets; t-stat >= 3.20 (bar for survivor 72)

### 2026-11-20 · screen survivor 73 · `squeeze_break_n72.fade.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 9b57973b1d). No stated reason.
- Screen years: 161 trades, profit factor 1.35, t-stat 1.74
- Confirm years: 77 trades, profit factor 1.03, +1.6R, t-stat 0.11 (needed 3.20); markets 2 of 6; double-cost profit factor 0.94; beats 59% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.20 (bar for survivor 73)

### 2026-11-20 · screen survivor 74 · `zmove_n24_z2.5.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id b6aebe09c4). No stated reason.
- Screen years: 375 trades, profit factor 1.42, t-stat 3.10
- Confirm years: 167 trades, profit factor 1.21, +24.8R, t-stat 1.14 (needed 3.20); markets 4 of 6; double-cost profit factor 1.14; beats 91% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.20 (bar for survivor 74)

### 2026-11-20 · screen survivor 75 · `zmove_n24_z2.5.follow.none.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 2e89bd76e2). No stated reason.
- Screen years: 492 trades, profit factor 1.30, t-stat 2.71
- Confirm years: 212 trades, profit factor 1.11, +17.4R, t-stat 0.72 (needed 3.21); markets 3 of 6; double-cost profit factor 1.01; beats 92% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.21 (bar for survivor 75)

### 2026-11-20 · screen survivor 76 · `squeeze_break_n72.fade.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id da48fc1c51). No stated reason.
- Screen years: 167 trades, profit factor 1.39, t-stat 2.10
- Confirm years: 78 trades, profit factor 0.89, -5.8R, t-stat -0.53 (needed 3.21); markets 2 of 6; double-cost profit factor 0.80; beats 43% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.21 (bar for survivor 76)

### 2026-11-20 · screen survivor 77 · `zmove_n24_z2.follow.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 9c5626c660). No stated reason.
- Screen years: 806 trades, profit factor 1.20, t-stat 2.36
- Confirm years: 360 trades, profit factor 1.09, +23.2R, t-stat 0.76 (needed 3.22); markets 4 of 6; double-cost profit factor 1.02; beats 88% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.22 (bar for survivor 77)

### 2026-11-20 · screen survivor 78 · `zmove_n24_z2.follow.high_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id ba163a63e9). No stated reason.
- Screen years: 1108 trades, profit factor 1.13, t-stat 1.89
- Confirm years: 498 trades, profit factor 1.19, +64.5R, t-stat 1.78 (needed 3.22); markets 4 of 6; double-cost profit factor 1.11; beats 99% of random entries
- Failed: t-stat >= 3.22 (bar for survivor 78)

### 2026-11-20 · screen survivor 79 · `vol_spike_k2.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 77f2f740c0). No stated reason.
- Screen years: 432 trades, profit factor 1.34, t-stat 2.77
- Confirm years: 231 trades, profit factor 1.24, +36.9R, t-stat 1.47 (needed 3.22); markets 2 of 6; double-cost profit factor 1.17; beats 93% of random entries
- Failed: profitable in half the markets; beats 95% of random entries; t-stat >= 3.22 (bar for survivor 79)

### 2026-11-20 · screen survivor 80 · `zmove_n24_z2.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 967c1296b7). No stated reason.
- Screen years: 599 trades, profit factor 1.24, t-stat 2.44
- Confirm years: 283 trades, profit factor 1.04, +9.1R, t-stat 0.33 (needed 3.23); markets 2 of 6; double-cost profit factor 0.97; beats 72% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.23 (bar for survivor 80)

### 2026-11-20 · screen survivor 81 · `big_bar_k2.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 9cd4841fdc). No stated reason.
- Screen years: 378 trades, profit factor 1.25, t-stat 1.97
- Confirm years: 217 trades, profit factor 0.93, -10.6R, t-stat -0.46 (needed 3.23); markets 3 of 6; double-cost profit factor 0.85; beats 63% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.23 (bar for survivor 81)

### 2026-11-20 · screen survivor 82 · `clock_hour20_weekday-1.follow.none.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 2067f54bb0). No stated reason.
- Screen years: 1820 trades, profit factor 1.11, t-stat 2.12
- Confirm years: 790 trades, profit factor 1.16, +89.7R, t-stat 1.91 (needed 3.23); markets 5 of 6; double-cost profit factor 1.08; beats 53% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.23 (bar for survivor 82)

### 2026-11-20 · screen survivor 83 · `clock_hour20_weekday-1.follow.high_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 40e12e50ec). No stated reason.
- Screen years: 1380 trades, profit factor 1.14, t-stat 2.21
- Confirm years: 608 trades, profit factor 1.13, +57.6R, t-stat 1.41 (needed 3.24); markets 5 of 6; double-cost profit factor 1.06; beats 43% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.24 (bar for survivor 83)

### 2026-11-20 · screen survivor 84 · `zmove_n24_z2.5.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 50a7905a6e). No stated reason.
- Screen years: 685 trades, profit factor 1.25, t-stat 2.73
- Confirm years: 304 trades, profit factor 1.17, +37.6R, t-stat 1.28 (needed 3.24); markets 3 of 6; double-cost profit factor 1.07; beats 99% of random entries
- Failed: t-stat >= 3.24 (bar for survivor 84)

### 2026-11-20 · screen survivor 85 · `squeeze_break_n24.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id fea6a4621e). No stated reason.
- Screen years: 442 trades, profit factor 1.19, t-stat 1.70
- Confirm years: 210 trades, profit factor 1.13, +20.3R, t-stat 0.82 (needed 3.24); markets 4 of 6; double-cost profit factor 0.96; beats 87% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.24 (bar for survivor 85)

### 2026-11-20 · screen survivor 86 · `zmove_n72_z2.follow.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id b55e2d6d49). No stated reason.
- Screen years: 554 trades, profit factor 1.17, t-stat 1.65
- Confirm years: 252 trades, profit factor 1.07, +13.0R, t-stat 0.50 (needed 3.25); markets 3 of 6; double-cost profit factor 0.99; beats 73% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.25 (bar for survivor 86)

### 2026-11-20 · screen survivor 87 · `zmove_n24_z2.5.follow.none.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue v1, id 3a0e356ff2). No stated reason.
- Screen years: 830 trades, profit factor 1.21, t-stat 2.58
- Confirm years: 379 trades, profit factor 1.12, +31.7R, t-stat 0.98 (needed 3.25); markets 4 of 6; double-cost profit factor 1.02; beats 98% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.25 (bar for survivor 87)

### 2026-11-20 · screen batch · 3800 ideas
- Passed the screen: 86. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 4000 of 4000 catalogue ideas screened, 87 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-20 · forward watch · 12 ideas registered
- `zmove_n24_z2.follow.none.any.stop3_rr2.5`
- `zmove_n24_z2.follow.with_trend.any.stop3_rr2.5`
- `breakout_n24.follow.with_trend.asia.stop3_rr2.5`
- `zmove_n24_z2.5.follow.with_trend.ny.stop2_rr2.5`
- `big_bar_k2.follow.with_trend.asia.stop3_rr1.5`
- `zmove_n24_z2.5.follow.with_trend.any.stop2_rr2.5`
- `zmove_n72_z2.follow.high_vol.any.stop3_rr2.5`
- `zmove_n24_z2.follow.high_vol.any.stop3_rr2.5`
- `big_bar_k3.follow.none.asia.stop3_rr2.5`
- `zmove_n24_z2.follow.with_trend.asia.stop3_rr2.5`
- `breakout_n72.follow.with_trend.asia.stop3_rr2.5`
- `breakout_n168.follow.with_trend.asia.stop3_rr2.5`
- Forward trades count from 2026-11-21 00:00 UTC. Verdict at 200 trades. Rules: "Forward watch" in `LAB_RULES.md`.

### 2026-11-20 · unplanned look at held-back data · `breakout_n168.follow.with_trend.asia.stop3_rr2.5`
- While testing `forward.py`, this near miss was run from April 21, 2024 to the end of the data. That window includes the held-back block (April 21, 2026 on), which only confirmed ideas are meant to touch.
- Held-back block result: 35 trades, profit factor 1.40, +9.2R, on BTCUSD, ETHUSD and XAUUSD only.
- This is not a quarantine pass and changes no verdict: the idea stays a REJECT on the forward watch. The held-back block is now spent for this idea.
- No other idea's held-back result has been looked at.

### 2026-11-20 · screen survivor 88 · `open_distance_frac1.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 60219371f9). No stated reason.
- Screen years: 1280 trades, profit factor 1.18, t-stat 2.70
- Confirm years: 542 trades, profit factor 1.07, +29.7R, t-stat 0.77 (needed 3.25); markets 3 of 6; double-cost profit factor 0.96; beats 94% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.25 (bar for survivor 88)

### 2026-11-20 · screen survivor 89 · `open_distance_frac1.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 332a0116a2). No stated reason.
- Screen years: 802 trades, profit factor 1.18, t-stat 2.18
- Confirm years: 356 trades, profit factor 1.10, +25.2R, t-stat 0.81 (needed 3.26); markets 4 of 6; double-cost profit factor 1.02; beats 79% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.26 (bar for survivor 89)

### 2026-11-20 · screen survivor 90 · `open_distance_frac1.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id af38960c39). No stated reason.
- Screen years: 1239 trades, profit factor 1.14, t-stat 2.29
- Confirm years: 527 trades, profit factor 1.08, +25.4R, t-stat 0.88 (needed 3.26); markets 3 of 6; double-cost profit factor 0.99; beats 95% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.26 (bar for survivor 90)

### 2026-11-20 · screen survivor 91 · `open_distance_frac1.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6b27319d49). No stated reason.
- Screen years: 155 trades, profit factor 1.55, t-stat 2.54
- Confirm years: 79 trades, profit factor 0.88, -7.1R, t-stat -0.50 (needed 3.26); markets 3 of 6; double-cost profit factor 0.81; beats 47% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.26 (bar for survivor 91)

### 2026-11-20 · screen survivor 92 · `open_distance_frac1.follow.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 605f8cf4af). No stated reason.
- Screen years: 1062 trades, profit factor 1.15, t-stat 2.03
- Confirm years: 482 trades, profit factor 1.12, +40.6R, t-stat 1.14 (needed 3.27); markets 4 of 6; double-cost profit factor 1.04; beats 92% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.27 (bar for survivor 92)

### 2026-11-20 · screen survivor 93 · `open_distance_frac0.5.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ec387ffd4c). No stated reason.
- Screen years: 574 trades, profit factor 1.23, t-stat 2.27
- Confirm years: 318 trades, profit factor 1.19, +42.7R, t-stat 1.44 (needed 3.27); markets 4 of 6; double-cost profit factor 1.11; beats 90% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.27 (bar for survivor 93)

### 2026-11-20 · screen survivor 94 · `open_distance_frac1.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6103de0193). No stated reason.
- Screen years: 151 trades, profit factor 1.72, t-stat 3.08
- Confirm years: 76 trades, profit factor 0.93, -4.1R, t-stat -0.30 (needed 3.27); markets 3 of 6; double-cost profit factor 0.87; beats 41% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.27 (bar for survivor 94)

### 2026-11-20 · screen survivor 95 · `open_distance_frac1.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ba5d06265e). No stated reason.
- Screen years: 460 trades, profit factor 1.22, t-stat 1.93
- Confirm years: 175 trades, profit factor 1.34, +40.1R, t-stat 1.77 (needed 3.28); markets 3 of 6; double-cost profit factor 1.22; beats 95% of random entries
- Failed: t-stat >= 3.28 (bar for survivor 95)

### 2026-11-20 · screen survivor 96 · `open_distance_frac1.follow.none.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 46a69a6eaa). No stated reason.
- Screen years: 1684 trades, profit factor 1.12, t-stat 2.17
- Confirm years: 698 trades, profit factor 1.10, +52.8R, t-stat 1.20 (needed 3.28); markets 3 of 6; double-cost profit factor 0.99; beats 99% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.28 (bar for survivor 96)

### 2026-11-20 · screen survivor 97 · `open_distance_frac0.5.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5c0e132205). No stated reason.
- Screen years: 627 trades, profit factor 1.16, t-stat 1.85
- Confirm years: 353 trades, profit factor 1.04, +8.1R, t-stat 0.35 (needed 3.28); markets 4 of 6; double-cost profit factor 0.96; beats 75% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.28 (bar for survivor 97)

### 2026-11-20 · screen survivor 98 · `open_distance_frac1.follow.high_vol.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c8bedeacaf). No stated reason.
- Screen years: 1246 trades, profit factor 1.11, t-stat 1.75
- Confirm years: 531 trades, profit factor 1.07, +26.8R, t-stat 0.71 (needed 3.28); markets 3 of 6; double-cost profit factor 0.97; beats 97% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.28 (bar for survivor 98)

### 2026-11-20 · screen survivor 99 · `open_distance_frac0.5.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9fa8ebd0bd). No stated reason.
- Screen years: 319 trades, profit factor 1.34, t-stat 2.43
- Confirm years: 168 trades, profit factor 0.94, -8.2R, t-stat -0.40 (needed 3.29); markets 2 of 6; double-cost profit factor 0.86; beats 37% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.29 (bar for survivor 99)

### 2026-11-20 · screen survivor 100 · `open_distance_frac0.5.follow.low_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 26555b6a88). No stated reason.
- Screen years: 333 trades, profit factor 1.26, t-stat 2.06
- Confirm years: 174 trades, profit factor 0.98, -2.2R, t-stat -0.13 (needed 3.29); markets 2 of 6; double-cost profit factor 0.88; beats 58% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.29 (bar for survivor 100)

### 2026-11-20 · screen survivor 101 · `open_distance_frac1.follow.with_trend.london.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d9b2f3d819). No stated reason.
- Screen years: 339 trades, profit factor 1.27, t-stat 2.04
- Confirm years: 145 trades, profit factor 1.09, +9.7R, t-stat 0.48 (needed 3.29); markets 4 of 6; double-cost profit factor 0.97; beats 88% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.29 (bar for survivor 101)

### 2026-11-20 · screen survivor 102 · `open_distance_frac1.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 29891fbafa). No stated reason.
- Screen years: 152 trades, profit factor 1.86, t-stat 3.83
- Confirm years: 79 trades, profit factor 0.95, -2.3R, t-stat -0.21 (needed 3.30); markets 3 of 6; double-cost profit factor 0.89; beats 56% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for survivor 102)

### 2026-11-20 · screen survivor 103 · `open_distance_frac1.follow.none.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 969ee20175). No stated reason.
- Screen years: 1421 trades, profit factor 1.18, t-stat 2.77
- Confirm years: 611 trades, profit factor 1.14, +57.1R, t-stat 1.43 (needed 3.30); markets 3 of 6; double-cost profit factor 1.05; beats 97% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.30 (bar for survivor 103)

### 2026-11-20 · screen survivor 104 · `open_distance_frac1.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2e0c1938b2). No stated reason.
- Screen years: 1066 trades, profit factor 1.20, t-stat 2.78
- Confirm years: 470 trades, profit factor 1.09, +30.1R, t-stat 0.85 (needed 3.30); markets 4 of 6; double-cost profit factor 1.01; beats 84% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.30 (bar for survivor 104)

### 2026-11-20 · screen survivor 105 · `open_distance_frac1.follow.high_vol.london.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8dd9640d0e). No stated reason.
- Screen years: 336 trades, profit factor 1.34, t-stat 2.51
- Confirm years: 149 trades, profit factor 0.96, -4.4R, t-stat -0.22 (needed 3.30); markets 2 of 6; double-cost profit factor 0.86; beats 73% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for survivor 105)

### 2026-11-20 · screen survivor 106 · `open_distance_frac1.follow.high_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 81040115fc). No stated reason.
- Screen years: 1077 trades, profit factor 1.14, t-stat 1.90
- Confirm years: 479 trades, profit factor 1.10, +33.9R, t-stat 0.97 (needed 3.31); markets 3 of 6; double-cost profit factor 1.03; beats 94% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.31 (bar for survivor 106)

### 2026-11-20 · screen survivor 107 · `open_distance_frac1.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8d2c4f30b3). No stated reason.
- Screen years: 338 trades, profit factor 1.25, t-stat 1.85
- Confirm years: 135 trades, profit factor 1.37, +34.1R, t-stat 1.70 (needed 3.31); markets 3 of 6; double-cost profit factor 1.25; beats 94% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.31 (bar for survivor 107)

### 2026-11-20 · screen survivor 108 · `open_distance_frac1.follow.high_vol.london.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 237ded6c00). No stated reason.
- Screen years: 339 trades, profit factor 1.21, t-stat 1.75
- Confirm years: 149 trades, profit factor 0.88, -11.4R, t-stat -0.75 (needed 3.31); markets 2 of 6; double-cost profit factor 0.78; beats 64% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.31 (bar for survivor 108)

### 2026-11-20 · screen survivor 109 · `open_distance_frac1.follow.none.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8fefaa1bf3). No stated reason.
- Screen years: 156 trades, profit factor 1.49, t-stat 2.46
- Confirm years: 79 trades, profit factor 1.19, +8.7R, t-stat 0.77 (needed 3.31); markets 4 of 6; double-cost profit factor 1.08; beats 93% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.31 (bar for survivor 109)

### 2026-11-20 · screen batch · 320 ideas
- New triggers registered: open_distance.
- Passed the screen: 22. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 4320 of 4320 catalogue ideas screened, 109 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-20 · forward watch · 1 ideas registered
- `open_distance_frac1.follow.low_vol.any.stop3_rr2.5`
- Forward trades count from 2026-11-21 00:00 UTC. Verdict at 200 trades. Rules: "Forward watch" in `LAB_RULES.md`.

### 2026-11-20 · new-market test · 13 watched ideas · 0 passed
- Markets: NAS100, SPX500, USOIL, EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, EURJPY.
- Hourly bars from 2021-04-21 to 2026-11-20. One run per idea. Needed t-stat 2.67.
- `breakout_n168.follow.with_trend.asia.stop3_rr2.5` · FAIL: 1176 trades, profit factor 0.89, -102.5R, t-stat -1.85, markets 2 of 9, double-cost profit factor 0.78, beats 53% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `breakout_n24.follow.with_trend.asia.stop3_rr2.5` · FAIL: 2154 trades, profit factor 0.88, -209.4R, t-stat -2.81, markets 1 of 9, double-cost profit factor 0.76, beats 44% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `breakout_n72.follow.with_trend.asia.stop3_rr2.5` · FAIL: 1549 trades, profit factor 0.85, -184.6R, t-stat -2.93, markets 1 of 9, double-cost profit factor 0.75, beats 25% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `zmove_n24_z2.follow.with_trend.asia.stop3_rr2.5` · FAIL: 544 trades, profit factor 0.85, -63.6R, t-stat -1.72, markets 2 of 9, double-cost profit factor 0.76, beats 41% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `zmove_n24_z2.follow.none.any.stop3_rr2.5` · FAIL: 2031 trades, profit factor 0.92, -127.3R, t-stat -1.81, markets 1 of 9, double-cost profit factor 0.82, beats 89% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `zmove_n24_z2.follow.high_vol.any.stop3_rr2.5` · FAIL: 1736 trades, profit factor 0.86, -183.0R, t-stat -2.85, markets 1 of 9, double-cost profit factor 0.77, beats 57% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `open_distance_frac1.follow.low_vol.any.stop3_rr2.5` · FAIL: 771 trades, profit factor 0.99, -8.0R, t-stat -0.18, markets 4 of 9, double-cost profit factor 0.86, beats 92% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `zmove_n24_z2.follow.with_trend.any.stop3_rr2.5` · FAIL: 1557 trades, profit factor 0.92, -96.4R, t-stat -1.52, markets 2 of 9, double-cost profit factor 0.82, beats 85% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `big_bar_k2.follow.with_trend.asia.stop3_rr1.5` · FAIL: 681 trades, profit factor 0.88, -52.6R, t-stat -1.61, markets 2 of 9, double-cost profit factor 0.75, beats 64% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `zmove_n72_z2.follow.high_vol.any.stop3_rr2.5` · FAIL: 1020 trades, profit factor 0.84, -130.0R, t-stat -2.58, markets 1 of 9, double-cost profit factor 0.76, beats 36% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `zmove_n24_z2.5.follow.with_trend.any.stop2_rr2.5` · FAIL: 971 trades, profit factor 0.84, -124.2R, t-stat -2.48, markets 2 of 9, double-cost profit factor 0.72, beats 79% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `big_bar_k3.follow.none.asia.stop3_rr2.5` · FAIL: 264 trades, profit factor 0.96, -7.8R, t-stat -0.30, markets 4 of 9, double-cost profit factor 0.85, beats 76% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67
- `zmove_n24_z2.5.follow.with_trend.ny.stop2_rr2.5` · FAIL: 508 trades, profit factor 0.90, -41.1R, t-stat -1.13, markets 4 of 9, double-cost profit factor 0.78, beats 87% of random entries. Failed: profit factor >= 1.15; profit factor > 1 at double costs; profitable in half the new markets; beats 95% of random entries; t-stat >= 2.67

### 2026-11-20 · attempt 101 · `channel_bounce` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies (2018), section 3.15, https://ssrn.com/abstract=3247865
- Reason claimed: Price inside a range tends to bounce off its edges.
- Who loses: Breakout traders who enter at the edge of a range that holds.
- Out-of-sample: 5055 trades, profit factor 0.82, -587.5R, t-stat -6.53 (needed 3.29)
- Profitable test years 0 of 16; markets 0 of 6; double-cost profit factor 0.72; beats 4% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.29 (bar for attempt 101)

### 2026-11-20 · attempt 102 · `ibs_reversion` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies (2018), section 4.4, https://ssrn.com/abstract=3247865 (single-market adaptation; the book ranks many ETFs against each other)
- Reason claimed: A close near the day's low is cheap and a close near the high is rich, and short-term extremes tend to revert.
- Who loses: Traders who need to sell or buy urgently into the close and pay for immediacy.
- Out-of-sample: 1994 trades, profit factor 0.83, -232.2R, t-stat -3.81 (needed 3.30)
- Profitable test years 4 of 16; markets 1 of 6; double-cost profit factor 0.73; beats 45% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for attempt 102)

### 2026-11-20 · attempt 103 · `pivot_support_resistance` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies (2018), section 3.14, https://ssrn.com/abstract=3247865
- Reason claimed: Not stated in the book. Common explanation: many traders watch the same daily levels, so price reacts around them.
- Who loses: Traders who fade a move through a widely watched level.
- Out-of-sample: 6921 trades, profit factor 0.88, -397.1R, t-stat -4.27 (needed 3.30)
- Profitable test years 3 of 16; markets 0 of 6; double-cost profit factor 0.75; beats 75% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for attempt 103)

### 2026-11-20 · screen survivor 110 · `a158_cntd_n20.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 93b946b84c). No stated reason.
- Screen years: 903 trades, profit factor 1.14, t-stat 2.00
- Confirm years: 462 trades, profit factor 1.25, +63.6R, t-stat 2.36 (needed 3.32); markets 12 of 15; double-cost profit factor 1.11; beats 100% of random entries
- Failed: t-stat >= 3.32 (bar for survivor 110)

### 2026-11-20 · screen survivor 111 · `a158_resi_n60.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d468fc8200). No stated reason.
- Screen years: 1328 trades, profit factor 1.13, t-stat 2.09
- Confirm years: 669 trades, profit factor 1.01, +6.3R, t-stat 0.15 (needed 3.32); markets 6 of 15; double-cost profit factor 0.92; beats 93% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.32 (bar for survivor 111)

### 2026-11-20 · screen survivor 112 · `a158_resi_n60.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c30d88b7c4). No stated reason.
- Screen years: 412 trades, profit factor 1.22, t-stat 2.02
- Confirm years: 290 trades, profit factor 0.85, -28.6R, t-stat -1.37 (needed 3.32); markets 5 of 15; double-cost profit factor 0.78; beats 38% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.32 (bar for survivor 112)

### 2026-11-20 · screen survivor 113 · `a158_rsqr_n20.follow.low_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8785da4231). No stated reason.
- Screen years: 721 trades, profit factor 1.18, t-stat 2.17
- Confirm years: 390 trades, profit factor 1.08, +19.0R, t-stat 0.76 (needed 3.32); markets 9 of 15; double-cost profit factor 0.91; beats 96% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.32 (bar for survivor 113)

### 2026-11-20 · screen survivor 114 · `a158_rsqr_n20.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9a5466a101). No stated reason.
- Screen years: 695 trades, profit factor 1.22, t-stat 2.44
- Confirm years: 378 trades, profit factor 0.97, -8.4R, t-stat -0.26 (needed 3.33); markets 9 of 15; double-cost profit factor 0.84; beats 62% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.33 (bar for survivor 114)

### 2026-11-20 · screen survivor 115 · `a158_rsqr_n20.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1ca3ca41d9). No stated reason.
- Screen years: 926 trades, profit factor 1.13, t-stat 1.66
- Confirm years: 500 trades, profit factor 1.12, +42.6R, t-stat 1.14 (needed 3.33); markets 11 of 15; double-cost profit factor 1.00; beats 96% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.33 (bar for survivor 115)

### 2026-11-20 · screen survivor 116 · `a158_rsqr_n20.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 74072a5926). No stated reason.
- Screen years: 986 trades, profit factor 1.18, t-stat 2.55
- Confirm years: 529 trades, profit factor 1.08, +25.2R, t-stat 0.87 (needed 3.33); markets 8 of 15; double-cost profit factor 0.95; beats 98% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.33 (bar for survivor 116)

### 2026-11-20 · screen survivor 117 · `a158_shadow_q0.99.follow.against_trend.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3f91f4c981). No stated reason.
- Screen years: 918 trades, profit factor 1.15, t-stat 1.95
- Confirm years: 444 trades, profit factor 0.95, -18.0R, t-stat -0.53 (needed 3.33); markets 7 of 15; double-cost profit factor 0.84; beats 72% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.33 (bar for survivor 117)

### 2026-11-20 · screen survivor 118 · `a158_vsumd_n20.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4fe5834ef0). No stated reason.
- Screen years: 596 trades, profit factor 1.31, t-stat 2.94
- Confirm years: 396 trades, profit factor 1.12, +34.4R, t-stat 1.05 (needed 3.34); markets 7 of 15; double-cost profit factor 1.02; beats 93% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; beats 95% of random entries; t-stat >= 3.34 (bar for survivor 118)

### 2026-11-20 · screen survivor 119 · `a158_vsumd_n20.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c5336d4832). No stated reason.
- Screen years: 370 trades, profit factor 1.26, t-stat 2.00
- Confirm years: 245 trades, profit factor 1.30, +50.1R, t-stat 1.89 (needed 3.34); markets 9 of 15; double-cost profit factor 1.17; beats 99% of random entries
- Failed: t-stat >= 3.34 (bar for survivor 119)

### 2026-11-20 · screen survivor 120 · `a158_vsumd_n20.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f513601a7e). No stated reason.
- Screen years: 404 trades, profit factor 1.27, t-stat 2.17
- Confirm years: 271 trades, profit factor 1.08, +15.6R, t-stat 0.58 (needed 3.34); markets 7 of 15; double-cost profit factor 0.98; beats 75% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.34 (bar for survivor 120)

### 2026-11-20 · screen survivor 121 · `a158_vsumd_n20.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 04d492437b). No stated reason.
- Screen years: 627 trades, profit factor 1.18, t-stat 2.06
- Confirm years: 411 trades, profit factor 1.03, +8.1R, t-stat 0.32 (needed 3.34); markets 6 of 15; double-cost profit factor 0.92; beats 88% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.34 (bar for survivor 121)

### 2026-11-20 · screen survivor 122 · `a158_vsumd_n20.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 25dece0e64). No stated reason.
- Screen years: 425 trades, profit factor 1.21, t-stat 1.94
- Confirm years: 281 trades, profit factor 1.00, +0.6R, t-stat 0.03 (needed 3.35); markets 5 of 15; double-cost profit factor 0.90; beats 71% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.35 (bar for survivor 122)

### 2026-11-20 · screen survivor 123 · `a158_vsumd_n20.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 74f24d56ff). No stated reason.
- Screen years: 258 trades, profit factor 1.33, t-stat 2.27
- Confirm years: 169 trades, profit factor 0.84, -17.8R, t-stat -1.12 (needed 3.35); markets 3 of 15; double-cost profit factor 0.77; beats 32% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.35 (bar for survivor 123)

### 2026-11-20 · screen survivor 124 · `a158_vsumd_n20.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f7417b10b9). No stated reason.
- Screen years: 264 trades, profit factor 1.29, t-stat 1.92
- Confirm years: 172 trades, profit factor 0.78, -30.4R, t-stat -1.50 (needed 3.35); markets 4 of 15; double-cost profit factor 0.71; beats 24% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.35 (bar for survivor 124)

### 2026-11-20 · screen survivor 125 · `alpha007_rank0.9.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 05f3427ba6). No stated reason.
- Screen years: 700 trades, profit factor 1.16, t-stat 1.80
- Confirm years: 493 trades, profit factor 0.99, -2.2R, t-stat -0.06 (needed 3.35); markets 5 of 15; double-cost profit factor 0.91; beats 81% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.35 (bar for survivor 125)

### 2026-11-20 · screen survivor 126 · `alpha007_rank0.9.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4dc51a60fa). No stated reason.
- Screen years: 901 trades, profit factor 1.14, t-stat 1.96
- Confirm years: 590 trades, profit factor 0.95, -18.2R, t-stat -0.60 (needed 3.35); markets 5 of 15; double-cost profit factor 0.85; beats 66% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.35 (bar for survivor 126)

### 2026-11-20 · screen survivor 127 · `alpha007_rank0.9.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5a842a5139). No stated reason.
- Screen years: 645 trades, profit factor 1.18, t-stat 1.97
- Confirm years: 384 trades, profit factor 1.24, +61.6R, t-stat 1.89 (needed 3.36); markets 10 of 15; double-cost profit factor 1.10; beats 98% of random entries
- Failed: t-stat >= 3.36 (bar for survivor 127)

### 2026-11-20 · screen survivor 128 · `alpha007_rank0.9.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c27f04f9f4). No stated reason.
- Screen years: 929 trades, profit factor 1.16, t-stat 2.11
- Confirm years: 613 trades, profit factor 0.97, -13.5R, t-stat -0.33 (needed 3.36); markets 5 of 15; double-cost profit factor 0.85; beats 84% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.36 (bar for survivor 128)

### 2026-11-20 · screen survivor 129 · `alpha035_q0.99.fade.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 433231768a). No stated reason.
- Screen years: 421 trades, profit factor 1.36, t-stat 2.94
- Confirm years: 267 trades, profit factor 1.01, +2.1R, t-stat 0.08 (needed 3.36); markets 6 of 15; double-cost profit factor 0.91; beats 66% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.36 (bar for survivor 129)

### 2026-11-20 · screen survivor 130 · `alpha035_q0.99.fade.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1d86cdfa1b). No stated reason.
- Screen years: 432 trades, profit factor 1.18, t-stat 1.73
- Confirm years: 272 trades, profit factor 0.87, -22.8R, t-stat -1.11 (needed 3.36); markets 5 of 15; double-cost profit factor 0.78; beats 37% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.36 (bar for survivor 130)

### 2026-11-20 · screen survivor 131 · `cmf_extreme_n20.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c9309c6915). No stated reason.
- Screen years: 1795 trades, profit factor 1.11, t-stat 2.03
- Confirm years: 1084 trades, profit factor 1.10, +75.6R, t-stat 1.38 (needed 3.37); markets 11 of 15; double-cost profit factor 0.98; beats 100% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.37 (bar for survivor 131)

### 2026-11-20 · screen survivor 132 · `realized_skew_n120.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 83e027b870). No stated reason.
- Screen years: 1296 trades, profit factor 1.19, t-stat 2.89
- Confirm years: 676 trades, profit factor 0.93, -38.8R, t-stat -0.92 (needed 3.37); markets 5 of 15; double-cost profit factor 0.83; beats 48% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.37 (bar for survivor 132)

### 2026-11-20 · screen survivor 133 · `realized_skew_n120.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id dd1ea04d3d). No stated reason.
- Screen years: 841 trades, profit factor 1.18, t-stat 2.43
- Confirm years: 415 trades, profit factor 0.87, -34.9R, t-stat -1.37 (needed 3.37); markets 4 of 15; double-cost profit factor 0.77; beats 43% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.37 (bar for survivor 133)

### 2026-11-20 · screen survivor 134 · `realized_skew_n120.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b4f52b88aa). No stated reason.
- Screen years: 776 trades, profit factor 1.24, t-stat 2.75
- Confirm years: 385 trades, profit factor 0.80, -62.1R, t-stat -2.02 (needed 3.37); markets 4 of 15; double-cost profit factor 0.72; beats 8% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.37 (bar for survivor 134)

### 2026-11-20 · screen survivor 135 · `same_hour_seasonality_k8.fade.high_vol.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9b3f41fbc0). No stated reason.
- Screen years: 577 trades, profit factor 1.19, t-stat 2.10
- Confirm years: 240 trades, profit factor 0.93, -10.9R, t-stat -0.57 (needed 3.37); markets 8 of 15; double-cost profit factor 0.84; beats 80% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.37 (bar for survivor 135)

### 2026-11-20 · screen survivor 136 · `same_hour_seasonality_k8.fade.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4e76d56fa2). No stated reason.
- Screen years: 527 trades, profit factor 1.26, t-stat 2.39
- Confirm years: 226 trades, profit factor 0.97, -5.0R, t-stat -0.21 (needed 3.38); markets 6 of 15; double-cost profit factor 0.88; beats 82% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.38 (bar for survivor 136)

### 2026-11-20 · screen survivor 137 · `td_setup_count9.fade.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9334485735). No stated reason.
- Screen years: 1049 trades, profit factor 1.14, t-stat 2.00
- Confirm years: 629 trades, profit factor 0.99, -2.8R, t-stat -0.07 (needed 3.38); markets 9 of 15; double-cost profit factor 0.89; beats 72% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.38 (bar for survivor 137)

### 2026-11-20 · screen survivor 138 · `turn_of_month_hour13.follow.against_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 93f1232a81). No stated reason.
- Screen years: 603 trades, profit factor 1.16, t-stat 1.71
- Confirm years: 352 trades, profit factor 1.33, +80.3R, t-stat 2.47 (needed 3.38); markets 12 of 15; double-cost profit factor 1.20; beats 99% of random entries
- Failed: t-stat >= 3.38 (bar for survivor 138)

### 2026-11-20 · screen batch · 5920 ideas
- New triggers registered: a158_cntd, a158_cord, a158_corr, a158_resi, a158_rsqr, a158_shadow, a158_vsumd, alpha007, alpha012, alpha021, alpha023, alpha035, alpha046, alpha054, cmf_extreme, crabel_idnr, high_volume_premium, intraday_momentum, opening_range_break, realized_skew, round_number_cross, same_hour_seasonality, smash_day, td_setup, turn_of_month.
- Passed the screen: 29. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 10240 of 10240 catalogue ideas screened, 138 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-20 · forward watch · 4 ideas registered
- `alpha007_rank0.9.follow.low_vol.asia.stop3_rr2.5`
- `a158_cntd_n20.follow.high_vol.asia.stop3_rr1.5`
- `turn_of_month_hour13.follow.against_trend.any.stop3_rr2.5`
- `a158_vsumd_n20.follow.low_vol.asia.stop3_rr2.5`
- Forward trades count from 2026-11-21 00:00 UTC. Verdict at 200 trades. Rules: "Forward watch" in `LAB_RULES.md`.

### 2026-11-20 · screen survivor 139 · `cl_three_soldiers_trend6.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a6bd50d16e). No stated reason.
- Screen years: 938 trades, profit factor 1.15, t-stat 1.92
- Confirm years: 486 trades, profit factor 0.97, -10.6R, t-stat -0.30 (needed 3.38); markets 5 of 15; double-cost profit factor 0.86; beats 65% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.38 (bar for survivor 139)

### 2026-11-20 · screen survivor 140 · `cl_three_soldiers_trend6.fade.with_trend.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b7dd9635f0). No stated reason.
- Screen years: 292 trades, profit factor 1.30, t-stat 2.07
- Confirm years: 170 trades, profit factor 0.98, -2.1R, t-stat -0.10 (needed 3.38); markets 7 of 15; double-cost profit factor 0.85; beats 64% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.38 (bar for survivor 140)

### 2026-11-20 · screen survivor 141 · `cl_three_soldiers_trend6.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 982f019728). No stated reason.
- Screen years: 369 trades, profit factor 1.23, t-stat 1.85
- Confirm years: 187 trades, profit factor 0.73, -42.1R, t-stat -2.01 (needed 3.39); markets 3 of 15; double-cost profit factor 0.65; beats 9% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.39 (bar for survivor 141)

### 2026-11-20 · screen survivor 142 · `cl_three_soldiers_trend6.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id fad1a703e5). No stated reason.
- Screen years: 375 trades, profit factor 1.20, t-stat 1.74
- Confirm years: 191 trades, profit factor 0.88, -14.8R, t-stat -0.85 (needed 3.39); markets 6 of 15; double-cost profit factor 0.77; beats 52% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.39 (bar for survivor 142)

### 2026-11-20 · screen batch · 1280 ideas
- New triggers registered: alpha008, amihud_illiq, cl_morning_star, cl_three_inside, cl_three_outside, cl_three_soldiers, hikkake, serial_corr.
- Passed the screen: 4. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 11520 of 11520 catalogue ideas screened, 142 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-21 · screen survivor 143 · `fair_value_gap_k1.follow.against_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id def232ab10). No stated reason.
- Screen years: 344 trades, profit factor 1.22, t-stat 1.72
- Confirm years: 228 trades, profit factor 1.11, +19.1R, t-stat 0.75 (needed 3.39); markets 10 of 15; double-cost profit factor 0.96; beats 98% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.39 (bar for survivor 143)

### 2026-11-21 · screen survivor 144 · `fair_value_gap_k1.follow.low_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6cf82d42e7). No stated reason.
- Screen years: 488 trades, profit factor 1.21, t-stat 1.97
- Confirm years: 293 trades, profit factor 1.28, +59.1R, t-stat 2.00 (needed 3.39); markets 10 of 15; double-cost profit factor 1.10; beats 100% of random entries
- Failed: t-stat >= 3.39 (bar for survivor 144)

### 2026-11-21 · screen survivor 145 · `fair_value_gap_k1.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b54828e3aa). No stated reason.
- Screen years: 969 trades, profit factor 1.19, t-stat 2.43
- Confirm years: 588 trades, profit factor 0.98, -9.6R, t-stat -0.25 (needed 3.39); markets 7 of 15; double-cost profit factor 0.89; beats 75% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.39 (bar for survivor 145)

### 2026-11-21 · screen survivor 146 · `fair_value_gap_k1.follow.low_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6c30996866). No stated reason.
- Screen years: 486 trades, profit factor 1.17, t-stat 1.70
- Confirm years: 292 trades, profit factor 1.17, +28.4R, t-stat 1.32 (needed 3.40); markets 9 of 15; double-cost profit factor 1.03; beats 99% of random entries
- Failed: t-stat >= 3.40 (bar for survivor 146)

### 2026-11-21 · screen survivor 147 · `fair_value_gap_k1.follow.against_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f87eecf809). No stated reason.
- Screen years: 335 trades, profit factor 1.35, t-stat 2.55
- Confirm years: 224 trades, profit factor 1.16, +25.5R, t-stat 1.02 (needed 3.40); markets 9 of 15; double-cost profit factor 1.05; beats 97% of random entries
- Failed: t-stat >= 3.40 (bar for survivor 147)

### 2026-11-21 · screen survivor 148 · `fair_value_gap_k1.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8b470053e4). No stated reason.
- Screen years: 479 trades, profit factor 1.44, t-stat 3.67
- Confirm years: 286 trades, profit factor 1.09, +18.2R, t-stat 0.65 (needed 3.40); markets 9 of 15; double-cost profit factor 0.97; beats 88% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.40 (bar for survivor 148)

### 2026-11-21 · screen batch · 1840 ideas
- New triggers registered: alexander_filter, alpha052, bvc_imbalance, fair_value_gap, lmw_broadening, lmw_double, lmw_head_shoulders, lmw_rectangle, lmw_triangle, opex_week.
- Passed the screen: 6. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 13360 of 13360 catalogue ideas screened, 148 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-21 · forward watch · 3 ideas registered
- `fair_value_gap_k1.follow.low_vol.asia.stop3_rr1.5`
- `fair_value_gap_k1.follow.low_vol.asia.stop2_rr2.5`
- `fair_value_gap_k1.follow.against_trend.asia.stop3_rr2.5`
- Forward trades count from 2026-11-22 00:00 UTC. Verdict at 200 trades. Rules: "Forward watch" in `LAB_RULES.md`.
