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

### 2026-11-21 · screen survivor 149 · `dow_swing_k6.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0663b274f2). No stated reason.
- Screen years: 662 trades, profit factor 1.18, t-stat 1.98
- Confirm years: 365 trades, profit factor 1.14, +38.7R, t-stat 1.20 (needed 3.40); markets 11 of 15; double-cost profit factor 1.01; beats 91% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.40 (bar for survivor 149)

### 2026-11-21 · screen survivor 150 · `dow_swing_k6.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 92ed3a3b14). No stated reason.
- Screen years: 1404 trades, profit factor 1.12, t-stat 1.98
- Confirm years: 752 trades, profit factor 0.99, -4.4R, t-stat -0.10 (needed 3.40); markets 7 of 15; double-cost profit factor 0.89; beats 81% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.40 (bar for survivor 150)

### 2026-11-21 · screen survivor 151 · `dow_swing_k6.follow.low_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 002c1b450d). No stated reason.
- Screen years: 203 trades, profit factor 1.33, t-stat 1.90
- Confirm years: 104 trades, profit factor 1.17, +12.8R, t-stat 0.73 (needed 3.40); markets 8 of 15; double-cost profit factor 1.00; beats 82% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.40 (bar for survivor 151)

### 2026-11-21 · screen batch · 800 ideas
- New triggers registered: dow_swing, osler_hs_neckline, three_line_break.
- Passed the screen: 3. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 14160 of 14160 catalogue ideas screened, 151 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-21 · attempt 104 · `valeyre_ema_trend` · REJECT
- Source: S. Valeyre, "Breaking the Trend: How to Avoid Cherry-Picked Signals", arXiv:2504.10914 (naive 1/N version, Eqs. 5, 6, 9, 10)
- Reason claimed: The paper's model: prices carry a slow hidden trend that fades at one time scale, which it puts down to investors herding; one exponential average of volatility-scaled returns estimates that trend.
- Who loses: The paper names traders who pull prices back towards a fair value while a trend is still running. It does not show that they lose.
- Mode: position (daily weights across 15 markets)
- Out-of-sample: 4393 days in the market, Sharpe 0.41, total +14.4%, max drawdown -6.8%, t-stat 1.43 (needed 3.30)
- Profitable test years 9 of 15; markets contributing 9 of 15; double-cost total +13.4%; beats 2% of time-shifted copies
- Failed: Sharpe >= 0.8; beats 95% of time-shifted copies of itself; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-21 · screen batch · 160 ideas
- New triggers registered: supertrend_flip.
- Passed the screen: 0. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 14320 of 14320 catalogue ideas screened, 151 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-21 · intraday study 1 · opening range breakout · A FAIL, B FAIL
- Source: YouTube, "I Built a Trading Bot to Pass Prop Firm Challenges" (Jan - Algo Trader, 2026-10-29). Lab version of the core rule, fixed in LAB_RULES.md before the data arrived.
- Nasdaq 100, 1-minute bars, 2021-04-21 to 2026-11-20. Verdict from the years before 2024; needed t-stat 2.58.
- NAS100, test A (volume filter): before 2024: 306 trades, win rate 54%, average +0.0231% a trade, profit factor 1.28, t-stat 1.59. From 2024: 371 trades, win rate 49%, average -0.0001% a trade, profit factor 1.00, t-stat -0.01. Verdict: FAIL. Failed: average above zero with t-stat >= 2.58.
- NAS100, test B (no filter): before 2024: 306 trades, win rate 54%, average +0.0231% a trade, profit factor 1.28, t-stat 1.59. From 2024: 371 trades, win rate 49%, average -0.0001% a trade, profit factor 1.00, t-stat -0.01. Verdict: FAIL. Failed: average above zero with t-stat >= 2.58.
- SPX500, test A (volume filter): before 2024: 306 trades, win rate 51%, average +0.0050% a trade, profit factor 1.08, t-stat 0.47. From 2024: 349 trades, win rate 49%, average +0.0038% a trade, profit factor 1.07, t-stat 0.46. Reported only: FAIL.
- SPX500, test B (no filter): before 2024: 322 trades, win rate 51%, average +0.0056% a trade, profit factor 1.09, t-stat 0.54. From 2024: 369 trades, win rate 48%, average +0.0014% a trade, profit factor 1.03, t-stat 0.18. Reported only: FAIL.
- USA30, test A (volume filter): before 2024: 246 trades, win rate 51%, average -0.0019% a trade, profit factor 0.97, t-stat -0.18. From 2024: 293 trades, win rate 53%, average +0.0050% a trade, profit factor 1.09, t-stat 0.57. Reported only: FAIL.
- USA30, test B (no filter): before 2024: 270 trades, win rate 52%, average +0.0012% a trade, profit factor 1.02, t-stat 0.11. From 2024: 316 trades, win rate 52%, average +0.0038% a trade, profit factor 1.07, t-stat 0.45. Reported only: FAIL.

### 2026-11-22 · intraday study 3 · the video's own settings · A FAIL, B FAIL
- Settings from a screenshot of the video's panel: 1 ATR stop, 2 ATR target, 10-minute exit, volume filter 0.5 to 1.5, ATR regime 1 to 3. Rules fixed in LAB_RULES.md before the data arrived.
- Nasdaq 100, 1-minute bars, 2021-04-21 to 2026-11-20. Verdict from the years before 2024, with a bar that touches both stop and target counted as a loss; needed t-stat 2.58.
- NAS100, test A (all settings): before 2024: 35 trades, win rate 43%, average +0.0189% a trade, profit factor 1.28, t-stat 0.61. From 2024: 72 trades, win rate 35%, average -0.0141% a trade, profit factor 0.80, t-stat -0.81. Exits: {'stop': 62, 'target': 26, 'time': 19}. With both-touched bars counted as wins, before 2024: 35 trades, win rate 43%, average +0.0189% a trade, profit factor 1.28, t-stat 0.61. Verdict: FAIL. Failed: trades >= 150; average above zero with t-stat >= 2.58.
- NAS100, test B (no ATR regime filter): before 2024: 306 trades, win rate 40%, average +0.0048% a trade, profit factor 1.07, t-stat 0.51. From 2024: 371 trades, win rate 37%, average +0.0004% a trade, profit factor 1.01, t-stat 0.05. Exits: {'stop': 384, 'target': 193, 'time': 97, 'both': 3}. With both-touched bars counted as wins, before 2024: 306 trades, win rate 41%, average +0.0069% a trade, profit factor 1.10, t-stat 0.73. Verdict: FAIL. Failed: average above zero with t-stat >= 2.58; profit factor >= 1.15; average above zero at double cost.
- SPX500, test A (all settings): before 2024: 58 trades, win rate 26%, average -0.0341% a trade, profit factor 0.48, t-stat -2.46. From 2024: 97 trades, win rate 34%, average -0.0025% a trade, profit factor 0.94, t-stat -0.26. Exits: {'stop': 92, 'target': 40, 'time': 22, 'both': 1}. With both-touched bars counted as wins, before 2024: 58 trades, win rate 26%, average -0.0341% a trade, profit factor 0.48, t-stat -2.46. Reported only: FAIL.
- SPX500, test B (no ATR regime filter): before 2024: 306 trades, win rate 37%, average -0.0045% a trade, profit factor 0.91, t-stat -0.69. From 2024: 349 trades, win rate 38%, average -0.0010% a trade, profit factor 0.98, t-stat -0.20. Exits: {'stop': 375, 'target': 188, 'time': 88, 'both': 4}. With both-touched bars counted as wins, before 2024: 306 trades, win rate 37%, average -0.0029% a trade, profit factor 0.94, t-stat -0.44. Reported only: FAIL.
- USA30, test A (all settings): before 2024: 22 trades, win rate 14%, average -0.0527% a trade, profit factor 0.33, t-stat -2.07. From 2024: 34 trades, win rate 35%, average -0.0101% a trade, profit factor 0.80, t-stat -0.59. Exits: {'stop': 40, 'target': 11, 'time': 5}. With both-touched bars counted as wins, before 2024: 22 trades, win rate 14%, average -0.0527% a trade, profit factor 0.33, t-stat -2.07. Reported only: FAIL.
- USA30, test B (no ATR regime filter): before 2024: 246 trades, win rate 37%, average -0.0098% a trade, profit factor 0.81, t-stat -1.47. From 2024: 293 trades, win rate 39%, average -0.0017% a trade, profit factor 0.96, t-stat -0.31. Exits: {'stop': 313, 'target': 148, 'time': 76, 'both': 2}. With both-touched bars counted as wins, before 2024: 246 trades, win rate 38%, average -0.0086% a trade, profit factor 0.83, t-stat -1.28. Reported only: FAIL.
- Notes on studies 1 and 3, written after both ran:
  - Data check before the runs: no duplicate or out-of-order bars, no impossible highs or lows, and hour opens and highs match the lab's hourly files for all three markets. Study 1's Nasdaq result before 2024 was recomputed a second way and matched exactly.
  - The volume filter could not be tested on the Nasdaq. Dukascopy's Nasdaq volume barely moves from bar to bar: the 9:59 reading was outside 0.5 to 1.5 on 0.2% of days, so tests A and B in study 1 are the same trades.
  - The ATR regime filter, as the lab read it, left 35 Nasdaq trades before 2024. That is under the 150 needed, so study 3 test A fails on count and says little either way. The reading may not be the video's.
  - A 1-minute bar touched both stop and target in 3 of 677 Nasdaq trades. Tick data would not change either study 3 verdict.
  - The files include about six weekdays a year when the US cash market was closed and the index still quoted. The rules did not exclude them, so they were left in.
  - Study 3 from 2024, the video's own period: 371 Nasdaq trades without the regime filter, win rate 37%, profit factor 1.01. The video reports 296 trades, a 93% win rate and a profit factor of 2.45. The lab cannot reproduce that from the settings shown.

### 2026-11-22 · intraday study 2 · 36 opening range variations · 1 passed the screen, 0 confirmed
- Nasdaq 100, S&P 500 and Dow, 1-minute bars, 2021-04-21 to 2026-11-20. Screen: before 2024. Confirm: 2024 on, t-stat bar 2.33.
- `range5.breakout.exit10.with` · REJECT: screen 695 days, average -0.0223%, profit factor 0.69, t-stat -3.31
- `range5.breakout.exit10.against` · REJECT: screen 695 days, average +0.0123%, profit factor 1.23, t-stat 1.83; confirm 746 days, average -0.0079%, profit factor 0.84, t-stat -1.71. Failed: average above zero with t-stat >= 2.33; profit factor >= 1.15; positive on two of three markets; average above zero at double cost; positive in two of 2024, 2025, 2026
- `range5.breakout.exit60.with` · REJECT: screen 695 days, average -0.0040%, profit factor 0.97, t-stat -0.29
- `range5.breakout.exit60.against` · REJECT: screen 695 days, average -0.0060%, profit factor 0.95, t-stat -0.44
- `range5.breakout.exitclose.with` · REJECT: screen 674 days, average +0.0385%, profit factor 1.17, t-stat 1.35
- `range5.breakout.exitclose.against` · REJECT: screen 674 days, average -0.0485%, profit factor 0.82, t-stat -1.70
- `range5.fixed.exit10.with` · REJECT: screen 587 days, average -0.0104%, profit factor 0.85, t-stat -1.45
- `range5.fixed.exit10.against` · REJECT: screen 587 days, average +0.0004%, profit factor 1.01, t-stat 0.06
- `range5.fixed.exit60.with` · REJECT: screen 587 days, average +0.0231%, profit factor 1.16, t-stat 1.29
- `range5.fixed.exit60.against` · REJECT: screen 587 days, average -0.0331%, profit factor 0.81, t-stat -1.84
- `range5.fixed.exitclose.with` · REJECT: screen 570 days, average +0.0535%, profit factor 1.18, t-stat 1.45
- `range5.fixed.exitclose.against` · REJECT: screen 570 days, average -0.0635%, profit factor 0.82, t-stat -1.72
- `range15.breakout.exit10.with` · REJECT: screen 694 days, average -0.0079%, profit factor 0.86, t-stat -1.46
- `range15.breakout.exit10.against` · REJECT: screen 694 days, average -0.0021%, profit factor 0.96, t-stat -0.40
- `range15.breakout.exit60.with` · REJECT: screen 694 days, average -0.0027%, profit factor 0.98, t-stat -0.20
- `range15.breakout.exit60.against` · REJECT: screen 694 days, average -0.0073%, profit factor 0.94, t-stat -0.54
- `range15.breakout.exitclose.with` · REJECT: screen 673 days, average +0.0176%, profit factor 1.07, t-stat 0.59
- `range15.breakout.exitclose.against` · REJECT: screen 673 days, average -0.0276%, profit factor 0.90, t-stat -0.92
- `range15.fixed.exit10.with` · REJECT: screen 466 days, average +0.0045%, profit factor 1.07, t-stat 0.50
- `range15.fixed.exit10.against` · REJECT: screen 466 days, average -0.0145%, profit factor 0.81, t-stat -1.62
- `range15.fixed.exit60.with` · REJECT: screen 466 days, average +0.0019%, profit factor 1.01, t-stat 0.10
- `range15.fixed.exit60.against` · REJECT: screen 466 days, average -0.0119%, profit factor 0.92, t-stat -0.62
- `range15.fixed.exitclose.with` · REJECT: screen 455 days, average +0.0429%, profit factor 1.14, t-stat 1.02
- `range15.fixed.exitclose.against` · REJECT: screen 455 days, average -0.0529%, profit factor 0.85, t-stat -1.26
- `range30.breakout.exit10.with` · REJECT: screen 683 days, average -0.0140%, profit factor 0.76, t-stat -2.51
- `range30.breakout.exit10.against` · REJECT: screen 683 days, average +0.0040%, profit factor 1.08, t-stat 0.72
- `range30.breakout.exit60.with` · REJECT: screen 683 days, average -0.0149%, profit factor 0.89, t-stat -1.14
- `range30.breakout.exit60.against` · REJECT: screen 683 days, average +0.0049%, profit factor 1.04, t-stat 0.37
- `range30.breakout.exitclose.with` · REJECT: screen 663 days, average -0.0019%, profit factor 0.99, t-stat -0.06
- `range30.breakout.exitclose.against` · REJECT: screen 663 days, average -0.0081%, profit factor 0.97, t-stat -0.26
- `range30.fixed.exit10.with` · REJECT: screen 414 days, average +0.0053%, profit factor 1.10, t-stat 0.70
- `range30.fixed.exit10.against` · REJECT: screen 414 days, average -0.0153%, profit factor 0.75, t-stat -2.02
- `range30.fixed.exit60.with` · REJECT: screen 413 days, average +0.0126%, profit factor 1.10, t-stat 0.70
- `range30.fixed.exit60.against` · REJECT: screen 413 days, average -0.0226%, profit factor 0.84, t-stat -1.25
- `range30.fixed.exitclose.with` · REJECT: screen 402 days, average +0.0696%, profit factor 1.26, t-stat 1.65
- `range30.fixed.exitclose.against` · REJECT: screen 402 days, average -0.0796%, profit factor 0.77, t-stat -1.88
- Notes on study 2, written after it ran:
  - Data check before the run: no duplicate or out-of-order bars, no impossible highs or lows, and every bar in the first-hour files matches the full-session files to within rounding.
  - The one screen survivor (5-minute range, breakout, 10-minute exit, against the break) lost money in the confirm years: negative in 2024, 2025 and 2026 and on all three markets. Its screen and confirm figures were recomputed a second way and matched.
  - Nearest miss at the screen: 30-minute range, fixed check, exit at 15:55, with the break. t-stat 1.645 against 1.65, profit factor 1.26, positive on all three markets, but 2021 was negative. It is rejected under the rules and its confirm years were not computed or looked at.
  - Five of the six "with the break, exit at 15:55" versions had a positive screen average. None reached the screen bar. This is an observation, not a result.
  - About 50 weekdays in the files are US holidays or half days, when the index quoted for part of the session. The rules did not exclude them. Versions that exit at 15:55 skip most of them because that bar is missing.

### 2026-11-22 · intraday study 4 · hold to the close, six versions as one group · FAIL
- Nasdaq 100, S&P 500 and Dow, 1-minute bars, 2024-01-02 to 2026-11-20. One test, t-stat bar 2.58. Rules fixed in LAB_RULES.md before these versions were computed on these years.
- Group: 720 days, win rate 47%, average +0.0110% a day, profit factor 1.07, t-stat 0.50. By year: {2024: -0.562, 2025: 10.856, 2026: -2.405}. Average at double cost +0.0060%. Per market: {'NAS100': 0.012, 'SPX500': 0.0111, 'USA30': -0.0147}.
- Long trades alone: 4715 trades, win rate 55%, average +0.0159% a trade. Short trades alone: 4570 trades, win rate 48%, average +0.0194% a trade.
- `range5.breakout.exitclose.with` alone: 720 days, win rate 52%, average +0.0303% a day, profit factor 1.17, t-stat 1.19
- `range5.fixed.exitclose.with` alone: 614 days, win rate 50%, average +0.0167% a day, profit factor 1.07, t-stat 0.53
- `range15.breakout.exitclose.with` alone: 720 days, win rate 50%, average +0.0149% a day, profit factor 1.08, t-stat 0.57
- `range15.fixed.exitclose.with` alone: 534 days, win rate 52%, average +0.0036% a day, profit factor 1.02, t-stat 0.12
- `range30.breakout.exitclose.with` alone: 709 days, win rate 51%, average +0.0205% a day, profit factor 1.10, t-stat 0.79
- `range30.fixed.exitclose.with` alone: 438 days, win rate 52%, average -0.0084% a day, profit factor 0.96, t-stat -0.26
- Verdict: FAIL. Failed: average above zero with t-stat >= 2.58; profit factor >= 1.15; positive in two of 2024, 2025, 2026.

### 2026-11-22 · screen batch · 480 ideas
- New triggers registered: supercycle_surge, trendilo_turn.
- Passed the screen: 0. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 14800 of 14800 catalogue ideas screened, 151 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-22 · screen batch · 920 ideas
- New triggers registered: gtja160_down_vol, lagged_session_sign, obv_divergence, tweezer.
- Passed the screen: 0. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 15720 of 15720 catalogue ideas screened, 151 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-22 · intraday study 6 · Coil Reclaim, first-hour breakout with a pullback entry · FAIL (too few trades)
- Source: github.com/Allencake/coil-reclaim-indicator, default settings. Nasdaq 100, S&P 500 and Dow, 5-minute bars built from 1-minute bars, New York first hour, June 1, 2021 to November 19, 2026. One test, t-stat bar 2.58, verdict on fill B. Rules fixed in LAB_RULES.md and pushed before the code was written.
- Fill B (as it could be traded): 53 trades on 50 days, win rate 51%, average +0.157R a day, profit factor 1.40, t-stat 1.06. By year: {2021: -3.1, 2022: +1.3, 2023: +3.0, 2024: +8.4, 2025: -0.9, 2026: -0.8}. Average at double cost +0.120R. Per market: {'NAS100': +0.231 (15 days), 'SPX500': +0.631 (17 days), 'USA30': -0.243 (20 days)}.
- Long trades alone: 29 trades, average +0.338R. Short trades alone: 24 trades, average -0.020R. Cost averaged 0.039R a trade. Endings: 19 stops, 14 break-even, 11 targets, 9 "too fast". 51% of trades reached 1R.
- Fill A (the indicator's own bookkeeping): 61 trades on 56 days, win rate 44%, average +0.087R a day, profit factor 1.20, t-stat 0.60.
- Orders: 135 placed. 65 cancelled because price reached the order with no pullback first, 17 because a bar closed back inside the range. Breakout bars turned away: 1,302 too large for their range, 418 blocked at a daily level, 287 outside a clean zone, 40 waiting for a pullback.
- Dry run on made-up prices with no cost, before the real run: fill A 238 trades, average -0.022R a day, t-stat -0.31; fill B 214 trades, average -0.040R a day, t-stat -0.54. Both about zero, as they should be with no edge.
- Verdict: FAIL (too few trades). Failed: at least 150 traded days; average above zero with t-stat >= 2.58; positive in four of six years; longs and shorts each above zero.
- Notes on study 6, written after it ran:
  - Only 450 of 1,414 days per market were usable, all between November and mid-March. The cause is a mistake in the registered rules, not the rule under test. The rules say the 1-minute files run from 8:00 to 16:14 New York time. They start at 13:00 UTC every day, which is 8:00 in winter and 9:00 in summer. The day rule needed bars from 8:00, so every summer day was skipped.
  - The mistake was found from the day counts after the run. Nothing was re-run. The summer days were never computed by this study.
  - Even with every day usable, the rule trades about once in 25 market-days here, so about 165 trades on roughly 155 days. That is close to the 150-day floor.
  - What the 50 days show: a positive average that is well inside what luck gives (t-stat 1.06), carried by 2024 and by long trades. It is not evidence for the rule and not evidence against it.
  - Fill B came out ahead of fill A. On 50 days that difference means nothing.

### 2026-11-23 · study 7 · "7H Profile · Fractal Model" script on 1-hour bars · FAIL
- Source: an anonymous Pine Script paste, pastebin.com/9AMMivPh, default settings. Fifteen markets, 1-hour bars, trades entered June 1, 2021 to April 20, 2026. One test, t-stat bar 2.58. Rules fixed in LAB_RULES.md and pushed before the code was written. Quarantine bars not touched.
- After costs: 1,167 trades on 758 days, win rate 42%, average -0.082R a day, profit factor 0.78, t-stat -2.71. By year: {2021: -8.4, 2022: -15.0, 2023: -16.0, 2024: -3.8, 2025: -18.7, 2026: -0.2}. Average at double cost -0.192R.
- Before costs: average +0.028R a day, profit factor 1.09, t-stat 0.92. Costs averaged 0.110R a trade.
- Long trades alone: 634 trades, average -0.037R. Short trades alone: 533 trades, average -0.168R.
- Per market, average R a trade after costs (trades): BTCUSD +0.066 (107), ETHUSD -0.087 (94), XAUUSD -0.023 (62), GBPJPY +0.013 (60), USA30 -0.030 (92), DEU30 -0.224 (59), NAS100 -0.031 (98), SPX500 -0.163 (95), USOIL -0.271 (62), EURUSD +0.006 (68), GBPUSD -0.336 (72), USDJPY -0.186 (96), AUDUSD -0.109 (67), USDCAD +0.013 (69), EURJPY -0.176 (66). Positive on 4 of 15.
- By group: crypto -0.006 (201), forex -0.118 (498), gold and oil -0.147 (124), indices -0.100 (344). By profile: Asia -0.133 (294), London -0.065 (304), New York -0.095 (569).
- Endings: 784 closed at the 15:00 time exit, 298 stops, 85 targets.
- How often it sets up: 20,513 market-days, a daily direction on 15,638 of them, 10,628 profiles formed, 7,113 of those invalidated, 1,191 triggers.
- Dry run on made-up prices with no cost, before the real run: 261 trades, average +0.034R a day, t-stat 0.62. About zero, as it should be with no edge.
- Verdict: FAIL. Failed: average above zero with t-stat >= 2.58; profit factor >= 1.15; average above zero at double cost; positive on 8 of 15 markets; positive in four of six years; longs and shorts each above zero.
- Notes on study 7, written after it ran:
  - Before costs the rule is not distinguishable from zero. After the lab's normal costs it loses in every year.
  - Two thirds of the trades never reach the stop or the target and are closed at 15:00. On 1-hour bars the stop sits at a sweep low up to 20 hours old, so the 2R target is far away.
  - This is the script's slowest allowed chart, not the 15-minute or 5-minute chart it recommends. The result says nothing certain about those.

### 2026-11-23 · screen survivor 152 · `gtja003_pressure_sum_n6.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 21fe7d06e8). No stated reason.
- Screen years: 416 trades, profit factor 1.26, t-stat 2.13
- Confirm years: 294 trades, profit factor 1.06, +12.6R, t-stat 0.45 (needed 3.41); markets 10 of 15; double-cost profit factor 0.94; beats 87% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.41 (bar for survivor 152)

### 2026-11-23 · screen survivor 153 · `gtja003_pressure_sum_n6.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0012c62c25). No stated reason.
- Screen years: 850 trades, profit factor 1.15, t-stat 1.87
- Confirm years: 596 trades, profit factor 0.98, -8.4R, t-stat -0.21 (needed 3.41); markets 6 of 15; double-cost profit factor 0.90; beats 74% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.41 (bar for survivor 153)

### 2026-11-23 · screen survivor 154 · `gtja003_pressure_sum_n20.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c919ace888). No stated reason.
- Screen years: 847 trades, profit factor 1.13, t-stat 1.68
- Confirm years: 477 trades, profit factor 0.99, -2.1R, t-stat -0.06 (needed 3.41); markets 6 of 15; double-cost profit factor 0.88; beats 74% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.41 (bar for survivor 154)

### 2026-11-23 · screen survivor 155 · `gtja009_ease_of_movement_n15.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4ade681196). No stated reason.
- Screen years: 1559 trades, profit factor 1.11, t-stat 1.88
- Confirm years: 719 trades, profit factor 1.02, +10.0R, t-stat 0.23 (needed 3.41); markets 7 of 15; double-cost profit factor 0.93; beats 82% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.41 (bar for survivor 155)

### 2026-11-23 · screen batch · 1480 ideas
- New triggers registered: gtja003_pressure_sum, gtja009_ease_of_movement, gtja118_open_reach, lunar_phase, td_differential, vsa_no_demand.
- Passed the screen: 4. Confirmed on unseen years: 0. Candidates: 0.
- Totals: 17200 of 17200 catalogue ideas screened, 155 survivors, 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-23 · study 8 · sweep, fair value gap, return to the gap · 96 scenarios · 0 passed the screen, 0 confirmed
- Source: a post by @L2WTrades on X (x.com/L2WTrades/status/2124841683896406023). Nasdaq 100, S&P 500 and Dow, 1-minute bars, 9:30 to 12:00 New York time.
- Screen: 2021-06-01 to 2023-12-31. Confirm: 2024-01-01 to 2026-11-19, t-stat bar 2.33. Results in R after a cost of 0.005% of price per round trip.
- The family in the screen years: 39 of 96 scenarios with trades had an average above zero after costs, 52 before costs. Median average -0.036R a day after costs, +0.026R before. Median cost 0.066R a trade. 62 scenarios had 150 or more traded days.
- `pdhl.window.m1.edge.gapstop.2r` · REJECT: screen 231 days, average -0.243R (-0.055R before costs), profit factor 0.67, t-stat -2.65
- `pdhl.window.m1.edge.gapstop.3r` · REJECT: screen 231 days, average -0.194R (-0.007R before costs), profit factor 0.76, t-stat -1.80
- `pdhl.window.m1.edge.gapstop.opp` · REJECT: screen 192 days, average -0.136R (+0.049R before costs), profit factor 0.88, t-stat -0.41
- `pdhl.window.m1.edge.sweepstop.2r` · REJECT: screen 231 days, average -0.036R (+0.011R before costs), profit factor 0.94, t-stat -0.42
- `pdhl.window.m1.edge.sweepstop.3r` · REJECT: screen 231 days, average +0.010R (+0.057R before costs), profit factor 1.01, t-stat 0.09
- `pdhl.window.m1.edge.sweepstop.opp` · REJECT: screen 187 days, average +0.016R (+0.063R before costs), profit factor 1.02, t-stat 0.09
- `pdhl.window.m1.mid.gapstop.2r` · REJECT: screen 222 days, average -0.573R (-0.196R before costs), profit factor 0.42, t-stat -5.29
- `pdhl.window.m1.mid.gapstop.3r` · REJECT: screen 222 days, average -0.528R (-0.151R before costs), profit factor 0.49, t-stat -4.47
- `pdhl.window.m1.mid.gapstop.opp` · REJECT: screen 183 days, average -0.535R (-0.168R before costs), profit factor 0.60, t-stat -1.39
- `pdhl.window.m1.mid.sweepstop.2r` · REJECT: screen 222 days, average -0.104R (-0.048R before costs), profit factor 0.84, t-stat -1.22
- `pdhl.window.m1.mid.sweepstop.3r` · REJECT: screen 222 days, average +0.010R (+0.066R before costs), profit factor 1.01, t-stat 0.09
- `pdhl.window.m1.mid.sweepstop.opp` · REJECT: screen 181 days, average -0.012R (+0.043R before costs), profit factor 0.99, t-stat -0.06
- `pdhl.window.m5.edge.gapstop.2r` · REJECT: screen 124 days, average -0.136R (-0.053R before costs), profit factor 0.81, t-stat -1.12
- `pdhl.window.m5.edge.gapstop.3r` · REJECT: screen 124 days, average -0.105R (-0.023R before costs), profit factor 0.87, t-stat -0.70
- `pdhl.window.m5.edge.gapstop.opp` · REJECT: screen 101 days, average -0.207R (-0.126R before costs), profit factor 0.78, t-stat -0.70
- `pdhl.window.m5.edge.sweepstop.2r` · REJECT: screen 124 days, average -0.143R (-0.119R before costs), profit factor 0.77, t-stat -1.33
- `pdhl.window.m5.edge.sweepstop.3r` · REJECT: screen 124 days, average -0.104R (-0.081R before costs), profit factor 0.84, t-stat -0.85
- `pdhl.window.m5.edge.sweepstop.opp` · REJECT: screen 82 days, average -0.226R (-0.199R before costs), profit factor 0.70, t-stat -1.24
- `pdhl.window.m5.mid.gapstop.2r` · REJECT: screen 107 days, average -0.323R (-0.150R before costs), profit factor 0.61, t-stat -2.42
- `pdhl.window.m5.mid.gapstop.3r` · REJECT: screen 107 days, average -0.204R (-0.031R before costs), profit factor 0.76, t-stat -1.27
- `pdhl.window.m5.mid.gapstop.opp` · REJECT: screen 90 days, average -0.445R (-0.280R before costs), profit factor 0.60, t-stat -1.08
- `pdhl.window.m5.mid.sweepstop.2r` · REJECT: screen 107 days, average -0.155R (-0.126R before costs), profit factor 0.76, t-stat -1.29
- `pdhl.window.m5.mid.sweepstop.3r` · REJECT: screen 107 days, average -0.164R (-0.135R before costs), profit factor 0.77, t-stat -1.18
- `pdhl.window.m5.mid.sweepstop.opp` · REJECT: screen 80 days, average -0.256R (-0.223R before costs), profit factor 0.68, t-stat -1.25
- `pdhl.overnight.m1.edge.gapstop.2r` · REJECT: screen 595 days, average -0.279R (-0.102R before costs), profit factor 0.54, t-stat -6.23
- `pdhl.overnight.m1.edge.gapstop.3r` · REJECT: screen 595 days, average -0.232R (-0.056R before costs), profit factor 0.64, t-stat -4.52
- `pdhl.overnight.m1.edge.gapstop.opp` · REJECT: screen 579 days, average +0.060R (+0.236R before costs), profit factor 1.06, t-stat 0.29
- `pdhl.overnight.m1.edge.sweepstop.2r` · REJECT: screen 595 days, average +0.011R (+0.039R before costs), profit factor 1.02, t-stat 0.25
- `pdhl.overnight.m1.edge.sweepstop.3r` · REJECT: screen 595 days, average +0.037R (+0.066R before costs), profit factor 1.07, t-stat 0.72
- `pdhl.overnight.m1.edge.sweepstop.opp` · REJECT: screen 482 days, average +0.082R (+0.117R before costs), profit factor 1.12, t-stat 0.79
- `pdhl.overnight.m1.mid.gapstop.2r` · REJECT: screen 588 days, average -0.488R (-0.129R before costs), profit factor 0.41, t-stat -8.95
- `pdhl.overnight.m1.mid.gapstop.3r` · REJECT: screen 588 days, average -0.474R (-0.115R before costs), profit factor 0.46, t-stat -8.02
- `pdhl.overnight.m1.mid.gapstop.opp` · REJECT: screen 572 days, average -0.297R (+0.061R before costs), profit factor 0.77, t-stat -1.37
- `pdhl.overnight.m1.mid.sweepstop.2r` · REJECT: screen 588 days, average +0.009R (+0.042R before costs), profit factor 1.02, t-stat 0.20
- `pdhl.overnight.m1.mid.sweepstop.3r` · REJECT: screen 588 days, average +0.055R (+0.088R before costs), profit factor 1.11, t-stat 1.03
- `pdhl.overnight.m1.mid.sweepstop.opp` · REJECT: screen 479 days, average +0.038R (+0.079R before costs), profit factor 1.05, t-stat 0.36
- `pdhl.overnight.m5.edge.gapstop.2r` · REJECT: screen 455 days, average -0.118R (-0.035R before costs), profit factor 0.80, t-stat -2.10
- `pdhl.overnight.m5.edge.gapstop.3r` · REJECT: screen 455 days, average -0.127R (-0.045R before costs), profit factor 0.82, t-stat -1.90
- `pdhl.overnight.m5.edge.gapstop.opp` · REJECT: screen 433 days, average -0.140R (-0.057R before costs), profit factor 0.85, t-stat -0.99
- `pdhl.overnight.m5.edge.sweepstop.2r` · REJECT: screen 455 days, average +0.011R (+0.028R before costs), profit factor 1.02, t-stat 0.22
- `pdhl.overnight.m5.edge.sweepstop.3r` · REJECT: screen 455 days, average +0.022R (+0.038R before costs), profit factor 1.05, t-stat 0.38
- `pdhl.overnight.m5.edge.sweepstop.opp` · REJECT: screen 293 days, average -0.078R (-0.056R before costs), profit factor 0.88, t-stat -0.85
- `pdhl.overnight.m5.mid.gapstop.2r` · REJECT: screen 423 days, average -0.243R (-0.072R before costs), profit factor 0.65, t-stat -4.03
- `pdhl.overnight.m5.mid.gapstop.3r` · REJECT: screen 423 days, average -0.236R (-0.065R before costs), profit factor 0.70, t-stat -3.31
- `pdhl.overnight.m5.mid.gapstop.opp` · REJECT: screen 399 days, average -0.147R (+0.025R before costs), profit factor 0.86, t-stat -0.62
- `pdhl.overnight.m5.mid.sweepstop.2r` · REJECT: screen 423 days, average +0.033R (+0.053R before costs), profit factor 1.07, t-stat 0.62
- `pdhl.overnight.m5.mid.sweepstop.3r` · REJECT: screen 423 days, average +0.049R (+0.068R before costs), profit factor 1.10, t-stat 0.78
- `pdhl.overnight.m5.mid.sweepstop.opp` · REJECT: screen 286 days, average -0.006R (+0.019R before costs), profit factor 0.99, t-stat -0.06
- `swing4h.window.m1.edge.gapstop.2r` · REJECT: screen 158 days, average -0.226R (-0.043R before costs), profit factor 0.70, t-stat -2.10
- `swing4h.window.m1.edge.gapstop.3r` · REJECT: screen 158 days, average -0.154R (+0.029R before costs), profit factor 0.81, t-stat -1.18
- `swing4h.window.m1.edge.gapstop.opp` · REJECT: screen 126 days, average +0.202R (+0.384R before costs), profit factor 1.19, t-stat 0.44
- `swing4h.window.m1.edge.sweepstop.2r` · REJECT: screen 158 days, average +0.005R (+0.051R before costs), profit factor 1.01, t-stat 0.04
- `swing4h.window.m1.edge.sweepstop.3r` · REJECT: screen 158 days, average +0.051R (+0.097R before costs), profit factor 1.07, t-stat 0.38
- `swing4h.window.m1.edge.sweepstop.opp` · REJECT: screen 126 days, average +0.207R (+0.251R before costs), profit factor 1.26, t-stat 0.83
- `swing4h.window.m1.mid.gapstop.2r` · REJECT: screen 149 days, average -0.711R (-0.339R before costs), profit factor 0.31, t-stat -6.82
- `swing4h.window.m1.mid.gapstop.3r` · REJECT: screen 149 days, average -0.709R (-0.337R before costs), profit factor 0.35, t-stat -6.01
- `swing4h.window.m1.mid.gapstop.opp` · REJECT: screen 119 days, average -0.597R (-0.225R before costs), profit factor 0.55, t-stat -1.23
- `swing4h.window.m1.mid.sweepstop.2r` · REJECT: screen 149 days, average -0.008R (+0.048R before costs), profit factor 0.99, t-stat -0.07
- `swing4h.window.m1.mid.sweepstop.3r` · REJECT: screen 149 days, average +0.029R (+0.085R before costs), profit factor 1.04, t-stat 0.21
- `swing4h.window.m1.mid.sweepstop.opp` · REJECT: screen 119 days, average +0.072R (+0.125R before costs), profit factor 1.08, t-stat 0.28
- `swing4h.window.m5.edge.gapstop.2r` · REJECT: screen 78 days, average +0.020R (+0.100R before costs), profit factor 1.03, t-stat 0.13
- `swing4h.window.m5.edge.gapstop.3r` · REJECT: screen 78 days, average +0.175R (+0.255R before costs), profit factor 1.24, t-stat 0.85
- `swing4h.window.m5.edge.gapstop.opp` · REJECT: screen 60 days, average -0.196R (-0.114R before costs), profit factor 0.79, t-stat -0.54
- `swing4h.window.m5.edge.sweepstop.2r` · REJECT: screen 78 days, average -0.032R (-0.009R before costs), profit factor 0.95, t-stat -0.22
- `swing4h.window.m5.edge.sweepstop.3r` · REJECT: screen 78 days, average +0.016R (+0.039R before costs), profit factor 1.03, t-stat 0.10
- `swing4h.window.m5.edge.sweepstop.opp` · REJECT: screen 54 days, average +0.056R (+0.081R before costs), profit factor 1.09, t-stat 0.23
- `swing4h.window.m5.mid.gapstop.2r` · REJECT: screen 65 days, average -0.393R (-0.227R before costs), profit factor 0.54, t-stat -2.40
- `swing4h.window.m5.mid.gapstop.3r` · REJECT: screen 65 days, average -0.218R (-0.052R before costs), profit factor 0.75, t-stat -1.05
- `swing4h.window.m5.mid.gapstop.opp` · REJECT: screen 51 days, average -0.712R (-0.542R before costs), profit factor 0.37, t-stat -2.07
- `swing4h.window.m5.mid.sweepstop.2r` · REJECT: screen 65 days, average -0.037R (-0.010R before costs), profit factor 0.94, t-stat -0.22
- `swing4h.window.m5.mid.sweepstop.3r` · REJECT: screen 65 days, average -0.045R (-0.018R before costs), profit factor 0.94, t-stat -0.23
- `swing4h.window.m5.mid.sweepstop.opp` · REJECT: screen 46 days, average -0.029R (+0.000R before costs), profit factor 0.96, t-stat -0.09
- `swing4h.overnight.m1.edge.gapstop.2r` · REJECT: screen 330 days, average -0.241R (-0.062R before costs), profit factor 0.66, t-stat -3.47
- `swing4h.overnight.m1.edge.gapstop.3r` · REJECT: screen 330 days, average -0.254R (-0.074R before costs), profit factor 0.68, t-stat -3.16
- `swing4h.overnight.m1.edge.gapstop.opp` · REJECT: screen 285 days, average +0.613R (+0.793R before costs), profit factor 1.58, t-stat 1.34
- `swing4h.overnight.m1.edge.sweepstop.2r` · REJECT: screen 330 days, average +0.057R (+0.089R before costs), profit factor 1.11, t-stat 0.85
- `swing4h.overnight.m1.edge.sweepstop.3r` · REJECT: screen 330 days, average +0.076R (+0.108R before costs), profit factor 1.13, t-stat 0.94
- `swing4h.overnight.m1.edge.sweepstop.opp` · REJECT: screen 244 days, average +0.281R (+0.319R before costs), profit factor 1.39, t-stat 1.54
- `swing4h.overnight.m1.mid.gapstop.2r` · REJECT: screen 320 days, average -0.512R (-0.145R before costs), profit factor 0.46, t-stat -6.20
- `swing4h.overnight.m1.mid.gapstop.3r` · REJECT: screen 320 days, average -0.569R (-0.202R before costs), profit factor 0.44, t-stat -6.53
- `swing4h.overnight.m1.mid.gapstop.opp` · REJECT: screen 274 days, average -0.046R (+0.323R before costs), profit factor 0.97, t-stat -0.09
- `swing4h.overnight.m1.mid.sweepstop.2r` · REJECT: screen 320 days, average +0.094R (+0.131R before costs), profit factor 1.19, t-stat 1.36
- `swing4h.overnight.m1.mid.sweepstop.3r` · REJECT: screen 320 days, average +0.079R (+0.117R before costs), profit factor 1.14, t-stat 0.97
- `swing4h.overnight.m1.mid.sweepstop.opp` · REJECT: screen 236 days, average +0.155R (+0.199R before costs), profit factor 1.21, t-stat 0.93
- `swing4h.overnight.m5.edge.gapstop.2r` · REJECT: screen 203 days, average -0.010R (+0.072R before costs), profit factor 0.98, t-stat -0.11
- `swing4h.overnight.m5.edge.gapstop.3r` · REJECT: screen 203 days, average -0.023R (+0.059R before costs), profit factor 0.97, t-stat -0.20
- `swing4h.overnight.m5.edge.gapstop.opp` · REJECT: screen 169 days, average +0.412R (+0.498R before costs), profit factor 1.46, t-stat 1.29
- `swing4h.overnight.m5.edge.sweepstop.2r` · REJECT: screen 203 days, average +0.094R (+0.111R before costs), profit factor 1.20, t-stat 1.14
- `swing4h.overnight.m5.edge.sweepstop.3r` · REJECT: screen 203 days, average +0.102R (+0.119R before costs), profit factor 1.21, t-stat 1.09
- `swing4h.overnight.m5.edge.sweepstop.opp` · REJECT: screen 131 days, average +0.133R (+0.154R before costs), profit factor 1.25, t-stat 0.92
- `swing4h.overnight.m5.mid.gapstop.2r` · REJECT: screen 181 days, average -0.177R (-0.007R before costs), profit factor 0.75, t-stat -1.78
- `swing4h.overnight.m5.mid.gapstop.3r` · REJECT: screen 181 days, average -0.011R (+0.158R before costs), profit factor 0.99, t-stat -0.09
- `swing4h.overnight.m5.mid.gapstop.opp` · REJECT: screen 150 days, average +0.211R (+0.385R before costs), profit factor 1.20, t-stat 0.44
- `swing4h.overnight.m5.mid.sweepstop.2r` · REJECT: screen 181 days, average +0.067R (+0.087R before costs), profit factor 1.14, t-stat 0.78
- `swing4h.overnight.m5.mid.sweepstop.3r` · REJECT: screen 181 days, average +0.119R (+0.139R before costs), profit factor 1.23, t-stat 1.16
- `swing4h.overnight.m5.mid.sweepstop.opp` · REJECT: screen 116 days, average +0.069R (+0.093R before costs), profit factor 1.12, t-stat 0.42
- Verdict: all 96 REJECTED at the screen. No scenario reached the confirm years, so January 2024 to November 2026 was never computed for this rule.
- Dry run on made-up prices with no cost, before the real run: 0 of 96 passed, 46 of 94 scenarios with trades had an average above zero, median average -0.004R a day. About zero, as it should be with no edge.
- Notes on study 8, written after it ran:
  - Usable days: Nasdaq 1,404, S&P 500 1,394, Dow 1,404. 62 scenarios had 150 or more traded days in the screen years; 34 are rejects marked "too few trades", 32 of them `window` scenarios.
  - Best t-stat 1.54 (`swing4h.overnight.m1.edge.sweepstop.opp`) against a screen bar of 1.65. 23 scenarios lost with a t-stat of -1.65 or worse.
  - Before costs, 52 of 96 were above zero and the median was +0.026R a day. The dry run with no edge in it gave 46 of 94. The family as a whole is not distinguishable from zero before costs and is below zero after them.
  - Stop at the gap: 7 of 48 above zero after costs, median -0.212R a day, median cost 0.173R a trade. With `m1` gaps and a `mid` entry the cost is about 0.35R a trade. The post's own stop is the part that does the damage.
  - Stop at the sweep extreme: 32 of 48 above zero after costs, median +0.019R a day, none with a t-stat of 1.65. This is where the least bad results are. It is not evidence of an edge, and under this study's rules it is not re-run or narrowed on these files.
  - Win rate: 27% for the median scenario. Endings over all scenarios: 29,674 stops (7,452 of them in the fill minute), 7,029 targets, 5,022 time exits.
  - Fourth sweep-and-reverse test to show nothing here, and the first on the small charts the method is sold for.

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `channel_bounce` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies (2018), section 3.15, https://ssrn.com/abstract=3247865
- Reason claimed: Price inside a range tends to bounce off its edges.
- Who loses: Breakout traders who enter at the edge of a range that holds.
- Out-of-sample: 3105 trades, profit factor 0.86, -279.2R, t-stat -3.84 (needed 3.30)
- Profitable test years 0 of 3; markets 1 of 6; double-cost profit factor 0.79; beats 10% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `donchian_breakout` · REJECT
- Source: Textbook trend-following rule (Donchian channel)
- Reason claimed: Large moves start with a break of the recent range, and trends persist longer than chance.
- Who loses: Traders fading new highs and lows, and hedgers who must trade regardless of price.
- Out-of-sample: 1908 trades, profit factor 1.06, +73.5R, t-stat 1.08 (needed 3.30)
- Profitable test years 2 of 3; markets 3 of 6; double-cost profit factor 0.97; beats 95% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `ibs_reversion` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies (2018), section 4.4, https://ssrn.com/abstract=3247865 (single-market adaptation; the book ranks many ETFs against each other)
- Reason claimed: A close near the day's low is cheap and a close near the high is rich, and short-term extremes tend to revert.
- Who loses: Traders who need to sell or buy urgently into the close and pay for immediacy.
- Out-of-sample: 1437 trades, profit factor 0.88, -107.0R, t-stat -2.14 (needed 3.30)
- Profitable test years 0 of 3; markets 1 of 6; double-cost profit factor 0.82; beats 44% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `pivot_support_resistance` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies (2018), section 3.14, https://ssrn.com/abstract=3247865
- Reason claimed: Not stated in the book. Common explanation: many traders watch the same daily levels, so price reacts around them.
- Who loses: Traders who fade a move through a widely watched level.
- Out-of-sample: 4342 trades, profit factor 0.89, -231.9R, t-stat -3.04 (needed 3.30)
- Profitable test years 1 of 3; markets 3 of 6; double-cost profit factor 0.78; beats 45% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `rsi2_reversion` · REJECT
- Source: Textbook short-term mean-reversion rule (2-period RSI with a trend filter)
- Reason claimed: Short, sharp pullbacks inside a longer trend tend to snap back.
- Who loses: Traders who sell in panic on a short pullback, and stop orders placed too close.
- Out-of-sample: 1878 trades, profit factor 0.90, -127.9R, t-stat -2.02 (needed 3.30)
- Profitable test years 0 of 3; markets 1 of 6; double-cost profit factor 0.83; beats 8% of random entries
- Failed: profit factor >= 1.15; profitable in 60% of test years; profitable in half the markets; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `ts_momentum` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies, section 10.4 (after Moskowitz, Ooi and Pedersen, 2012)
- Reason claimed: Trends persist for months because information spreads slowly and investors adjust positions gradually.
- Who loses: Hedgers and slow movers who trade against a move that has not finished.
- Mode: position (daily weights across 6 markets)
- Out-of-sample: 1096 days in the market, Sharpe 1.17, total +30.6%, max drawdown -9.4%, t-stat 2.03 (needed 3.30)
- Profitable test years 3 of 3; markets contributing 4 of 6; double-cost total +29.8%; beats 10% of time-shifted copies
- Failed: beats 95% of time-shifted copies of itself; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `valeyre_ema_trend` · REJECT
- Source: S. Valeyre, "Breaking the Trend: How to Avoid Cherry-Picked Signals", arXiv:2504.10914 (naive 1/N version, Eqs. 5, 6, 9, 10)
- Reason claimed: The paper's model: prices carry a slow hidden trend that fades at one time scale, which it puts down to investors herding; one exponential average of volatility-scaled returns estimates that trend.
- Who loses: The paper names traders who pull prices back towards a fair value while a trend is still running. It does not show that they lose.
- Mode: position (daily weights across 15 markets)
- Out-of-sample: 1096 days in the market, Sharpe 0.89, total +9.0%, max drawdown -4.3%, t-stat 1.54 (needed 3.30)
- Profitable test years 3 of 3; markets contributing 8 of 15; double-cost total +8.8%; beats 0% of time-shifted copies
- Failed: beats 95% of time-shifted copies of itself; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · version 4 re-run, bar for attempt 104 · `xs_contrarian` · REJECT
- Source: Kakushadze and Serur, 151 Trading Strategies, section 10.3
- Reason claimed: Short-term moves away from the group partly reverse as temporary buying or selling pressure fades.
- Who loses: Traders who chase last week's leaders, and those forced to trade into a temporary imbalance.
- Mode: position (daily weights across 6 markets)
- Out-of-sample: 1096 days in the market, Sharpe -0.54, total -16.2%, max drawdown -22.5%, t-stat -0.93 (needed 3.30)
- Profitable test years 1 of 3; markets contributing 1 of 6; double-cost total -23.2%; beats 42% of time-shifted copies
- Failed: Sharpe >= 0.8; profitable in 60% of test years; half the markets contribute a profit; still profitable at double costs; beats 95% of time-shifted copies of itself; t-stat >= 3.30 (bar for attempt 104)

### 2026-11-23 · screen survivor 156 · `zmove_n24_z2.5.follow.none.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id bf95d1fc89). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1136 trades, profit factor 1.13, t-stat 2.09
- Confirm years: 807 trades, profit factor 0.93, -37.1R, t-stat -1.06 (needed 3.41); markets 5 of 15; double-cost profit factor 0.88; beats 53% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.41 (bar for survivor 156)

### 2026-11-23 · screen survivor 157 · `prev_day_break.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 7f6ec07829). No stated reason.
- Screen years: 2034 trades, profit factor 1.11, t-stat 2.10
- Confirm years: 1396 trades, profit factor 0.99, -5.2R, t-stat -0.09 (needed 3.42); markets 7 of 15; double-cost profit factor 0.92; beats 53% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.42 (bar for survivor 157)

### 2026-11-23 · screen survivor 158 · `big_bar_k3.fade.none.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b9c8a0d82a). No stated reason.
- Screen years: 841 trades, profit factor 1.13, t-stat 1.80
- Confirm years: 450 trades, profit factor 0.81, -55.0R, t-stat -2.14 (needed 3.42); markets 3 of 15; double-cost profit factor 0.76; beats 9% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.42 (bar for survivor 158)

### 2026-11-23 · screen survivor 159 · `squeeze_break_n72.fade.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 623705aa6b). No stated reason.
- Screen years: 267 trades, profit factor 1.30, t-stat 1.97
- Confirm years: 188 trades, profit factor 0.91, -13.2R, t-stat -0.60 (needed 3.42); markets 6 of 15; double-cost profit factor 0.83; beats 44% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.42 (bar for survivor 159)

### 2026-11-23 · screen survivor 160 · `clock_hour0_weekday0.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 04897006ed). No stated reason.
- Screen years: 1037 trades, profit factor 1.13, t-stat 1.73
- Confirm years: 719 trades, profit factor 1.24, +116.7R, t-stat 2.60 (needed 3.42); markets 12 of 15; double-cost profit factor 1.17; beats 82% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.42 (bar for survivor 160)

### 2026-11-23 · screen survivor 161 · `zmove_n24_z2.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2c893dea6d). No stated reason.
- Screen years: 932 trades, profit factor 1.13, t-stat 1.69
- Confirm years: 670 trades, profit factor 0.93, -36.1R, t-stat -0.88 (needed 3.42); markets 7 of 15; double-cost profit factor 0.87; beats 48% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.42 (bar for survivor 161)

### 2026-11-23 · screen survivor 162 · `gap.fade.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1d53a30188). No stated reason.
- Screen years: 594 trades, profit factor 1.15, t-stat 1.68
- Confirm years: 617 trades, profit factor 1.12, +44.5R, t-stat 1.43 (needed 3.42); markets 9 of 13; double-cost profit factor 1.07; beats 88% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.42 (bar for survivor 162)

### 2026-11-23 · screen survivor 163 · `streak_k5.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4c32cbb833). No stated reason.
- Screen years: 1556 trades, profit factor 1.10, t-stat 1.75
- Confirm years: 1093 trades, profit factor 0.98, -16.0R, t-stat -0.30 (needed 3.43); markets 6 of 15; double-cost profit factor 0.93; beats 33% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.43 (bar for survivor 163)

### 2026-11-23 · screen survivor 164 · `clock_hour20_weekday-1.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9d9e56acbd). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1675 trades, profit factor 1.16, t-stat 2.73
- Confirm years: 1354 trades, profit factor 1.14, +137.7R, t-stat 2.27 (needed 3.43); markets 11 of 15; double-cost profit factor 1.09; beats 48% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.43 (bar for survivor 164)

### 2026-11-23 · screen survivor 165 · `streak_k4.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 562b94a397). No stated reason.
- Screen years: 2394 trades, profit factor 1.12, t-stat 2.50
- Confirm years: 1671 trades, profit factor 0.94, -65.8R, t-stat -1.10 (needed 3.43); markets 6 of 15; double-cost profit factor 0.87; beats 26% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.43 (bar for survivor 165)

### 2026-11-23 · screen survivor 166 · `zmove_n24_z2.5.follow.none.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3e592b6b0b). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 653 trades, profit factor 1.18, t-stat 2.08
- Confirm years: 433 trades, profit factor 0.89, -29.3R, t-stat -1.15 (needed 3.43); markets 3 of 15; double-cost profit factor 0.85; beats 40% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.43 (bar for survivor 166)

### 2026-11-23 · screen survivor 167 · `big_bar_k3.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a769b9af48). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1625 trades, profit factor 1.11, t-stat 1.88
- Confirm years: 1055 trades, profit factor 1.04, +32.6R, t-stat 0.62 (needed 3.43); markets 7 of 15; double-cost profit factor 0.99; beats 81% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.43 (bar for survivor 167)

### 2026-11-23 · screen survivor 168 · `vol_spike_k3.follow.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f4d4947afa). No stated reason.
- Screen years: 2878 trades, profit factor 1.11, t-stat 2.34
- Confirm years: 1991 trades, profit factor 1.04, +51.4R, t-stat 0.80 (needed 3.43); markets 10 of 15; double-cost profit factor 0.98; beats 98% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.43 (bar for survivor 168)

### 2026-11-23 · screen survivor 169 · `streak_k5.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id be57e72ba4). No stated reason.
- Screen years: 1186 trades, profit factor 1.12, t-stat 1.71
- Confirm years: 904 trades, profit factor 1.13, +83.9R, t-stat 1.70 (needed 3.44); markets 10 of 15; double-cost profit factor 1.07; beats 93% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.44 (bar for survivor 169)

### 2026-11-23 · screen survivor 170 · `gap.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c4d98a96e2). No stated reason.
- Screen years: 576 trades, profit factor 1.17, t-stat 1.81
- Confirm years: 670 trades, profit factor 0.78, -99.0R, t-stat -3.18 (needed 3.44); markets 3 of 13; double-cost profit factor 0.74; beats 1% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.44 (bar for survivor 170)

### 2026-11-23 · screen survivor 171 · `vol_spike_k2.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a9b2fb1dab). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 541 trades, profit factor 1.20, t-stat 1.92
- Confirm years: 419 trades, profit factor 0.94, -18.5R, t-stat -0.60 (needed 3.44); markets 5 of 12; double-cost profit factor 0.88; beats 53% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.44 (bar for survivor 171)

### 2026-11-23 · screen survivor 172 · `zmove_n24_z2.5.follow.high_vol.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 139a54bf21). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1060 trades, profit factor 1.11, t-stat 1.71
- Confirm years: 763 trades, profit factor 0.91, -45.3R, t-stat -1.33 (needed 3.44); markets 5 of 15; double-cost profit factor 0.86; beats 44% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.44 (bar for survivor 172)

### 2026-11-23 · screen survivor 173 · `zmove_n24_z2.5.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 95a6546d06). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 294 trades, profit factor 1.42, t-stat 2.74
- Confirm years: 207 trades, profit factor 1.07, +10.2R, t-stat 0.43 (needed 3.44); markets 8 of 15; double-cost profit factor 1.00; beats 87% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.44 (bar for survivor 173)

### 2026-11-23 · screen survivor 174 · `big_bar_k3.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b953a83b2a). No stated reason.
- Screen years: 160 trades, profit factor 1.42, t-stat 2.17
- Confirm years: 140 trades, profit factor 0.84, -14.5R, t-stat -1.01 (needed 3.44); markets 5 of 15; double-cost profit factor 0.80; beats 35% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.44 (bar for survivor 174)

### 2026-11-23 · screen survivor 175 · `breakout_n168.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 199199a5da). No stated reason.
- Screen years: 645 trades, profit factor 1.16, t-stat 1.68
- Confirm years: 448 trades, profit factor 1.03, +10.9R, t-stat 0.31 (needed 3.44); markets 6 of 15; double-cost profit factor 0.99; beats 75% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.44 (bar for survivor 175)

### 2026-11-23 · screen survivor 176 · `sweep_n72.follow.with_trend.ny.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 506190c981). No stated reason.
- Screen years: 1043 trades, profit factor 1.12, t-stat 1.81
- Confirm years: 688 trades, profit factor 0.86, -63.9R, t-stat -1.97 (needed 3.45); markets 3 of 15; double-cost profit factor 0.78; beats 30% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.45 (bar for survivor 176)

### 2026-11-23 · screen survivor 177 · `zmove_n24_z2.5.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 759518987a). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 338 trades, profit factor 1.30, t-stat 2.23
- Confirm years: 261 trades, profit factor 1.04, +7.3R, t-stat 0.28 (needed 3.45); markets 8 of 15; double-cost profit factor 0.97; beats 83% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.45 (bar for survivor 177)

### 2026-11-23 · screen survivor 178 · `big_bar_k3.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e15d0a0d8a). No stated reason.
- Screen years: 159 trades, profit factor 1.46, t-stat 2.20
- Confirm years: 135 trades, profit factor 1.04, +4.1R, t-stat 0.22 (needed 3.45); markets 7 of 15; double-cost profit factor 1.00; beats 68% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.45 (bar for survivor 178)

### 2026-11-23 · screen survivor 179 · `zmove_n24_z2.5.follow.with_trend.any.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e802b56c1a). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1004 trades, profit factor 1.12, t-stat 1.83
- Confirm years: 705 trades, profit factor 0.93, -30.1R, t-stat -0.91 (needed 3.45); markets 8 of 15; double-cost profit factor 0.86; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.45 (bar for survivor 179)

### 2026-11-23 · screen survivor 180 · `zmove_n24_z2.5.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 79af0a1dae). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 520 trades, profit factor 1.28, t-stat 2.80
- Confirm years: 348 trades, profit factor 0.93, -15.6R, t-stat -0.68 (needed 3.45); markets 7 of 15; double-cost profit factor 0.88; beats 51% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.45 (bar for survivor 180)

### 2026-11-23 · screen survivor 181 · `zmove_n24_z2.5.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d5c9d133ea). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 317 trades, profit factor 1.27, t-stat 2.11
- Confirm years: 245 trades, profit factor 0.87, -21.1R, t-stat -1.11 (needed 3.45); markets 4 of 15; double-cost profit factor 0.83; beats 35% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.45 (bar for survivor 181)

### 2026-11-23 · screen survivor 182 · `big_bar_k3.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4748263e62). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 311 trades, profit factor 1.26, t-stat 2.04
- Confirm years: 259 trades, profit factor 0.86, -23.8R, t-stat -1.21 (needed 3.46); markets 6 of 15; double-cost profit factor 0.80; beats 35% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.46 (bar for survivor 182)

### 2026-11-23 · screen survivor 183 · `vol_spike_k3.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 10ba9de10d). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 190 trades, profit factor 1.48, t-stat 2.68
- Confirm years: 150 trades, profit factor 1.01, +0.9R, t-stat 0.06 (needed 3.46); markets 6 of 11; double-cost profit factor 0.94; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.46 (bar for survivor 183)

### 2026-11-23 · screen survivor 184 · `vol_spike_k3.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1c88d14e95). No stated reason.
- Screen years: 246 trades, profit factor 1.42, t-stat 2.47
- Confirm years: 212 trades, profit factor 1.03, +4.6R, t-stat 0.20 (needed 3.46); markets 4 of 11; double-cost profit factor 0.96; beats 75% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.46 (bar for survivor 184)

### 2026-11-23 · screen survivor 185 · `big_bar_k2.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e91b55fcab). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 2427 trades, profit factor 1.16, t-stat 3.31
- Confirm years: 1685 trades, profit factor 0.96, -45.8R, t-stat -0.70 (needed 3.46); markets 7 of 15; double-cost profit factor 0.91; beats 30% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.46 (bar for survivor 185)

### 2026-11-23 · screen survivor 186 · `zmove_n24_z2.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b960fe78cd). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 914 trades, profit factor 1.14, t-stat 2.01
- Confirm years: 659 trades, profit factor 0.88, -49.2R, t-stat -1.56 (needed 3.46); markets 7 of 15; double-cost profit factor 0.84; beats 20% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.46 (bar for survivor 186)

### 2026-11-23 · screen survivor 187 · `zmove_n24_z2.5.follow.high_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a7ca51ac6f). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 972 trades, profit factor 1.17, t-stat 2.27
- Confirm years: 703 trades, profit factor 0.96, -20.9R, t-stat -0.50 (needed 3.46); markets 6 of 15; double-cost profit factor 0.92; beats 58% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.46 (bar for survivor 187)

### 2026-11-23 · screen survivor 188 · `vol_spike_k3.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6d25eec9f3). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 181 trades, profit factor 1.75, t-stat 3.43
- Confirm years: 146 trades, profit factor 0.80, -22.1R, t-stat -1.24 (needed 3.46); markets 5 of 11; double-cost profit factor 0.75; beats 24% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.46 (bar for survivor 188)

### 2026-11-23 · screen survivor 189 · `big_bar_k3.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3fad6108aa). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1066 trades, profit factor 1.16, t-stat 2.25
- Confirm years: 656 trades, profit factor 0.84, -79.9R, t-stat -2.01 (needed 3.47); markets 2 of 15; double-cost profit factor 0.80; beats 4% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.47 (bar for survivor 189)

### 2026-11-23 · screen survivor 190 · `zmove_n24_z2.5.follow.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 13d15d69a5). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 569 trades, profit factor 1.18, t-stat 1.78
- Confirm years: 390 trades, profit factor 0.98, -6.6R, t-stat -0.21 (needed 3.47); markets 6 of 15; double-cost profit factor 0.93; beats 66% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.47 (bar for survivor 190)

### 2026-11-23 · screen survivor 191 · `vol_spike_k3.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 7d6b65a2a8). No stated reason.
- Screen years: 193 trades, profit factor 1.36, t-stat 1.96
- Confirm years: 176 trades, profit factor 0.83, -23.2R, t-stat -1.11 (needed 3.47); markets 3 of 11; double-cost profit factor 0.75; beats 37% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.47 (bar for survivor 191)

### 2026-11-23 · screen survivor 192 · `big_bar_k3.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id be528f983b). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 304 trades, profit factor 1.35, t-stat 2.37
- Confirm years: 253 trades, profit factor 1.01, +2.4R, t-stat 0.09 (needed 3.47); markets 7 of 15; double-cost profit factor 0.95; beats 76% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.47 (bar for survivor 192)

### 2026-11-23 · screen survivor 193 · `squeeze_break_n24.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5cd692bfd4). No stated reason.
- Screen years: 1242 trades, profit factor 1.17, t-stat 2.55
- Confirm years: 851 trades, profit factor 0.89, -75.6R, t-stat -1.61 (needed 3.47); markets 6 of 15; double-cost profit factor 0.80; beats 14% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.47 (bar for survivor 193)

### 2026-11-23 · screen survivor 194 · `vol_spike_k3.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 03f297087c). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 193 trades, profit factor 1.56, t-stat 2.85
- Confirm years: 151 trades, profit factor 0.82, -20.7R, t-stat -1.10 (needed 3.47); markets 4 of 11; double-cost profit factor 0.76; beats 42% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.47 (bar for survivor 194)

### 2026-11-23 · screen survivor 195 · `zmove_n24_z2.5.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f4a5852e9a). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 292 trades, profit factor 1.31, t-stat 2.27
- Confirm years: 207 trades, profit factor 0.89, -13.8R, t-stat -0.78 (needed 3.47); markets 8 of 15; double-cost profit factor 0.85; beats 42% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.47 (bar for survivor 195)

### 2026-11-23 · screen survivor 196 · `zmove_n72_z2.5.fade.against_trend.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b8761f436b). No stated reason.
- Screen years: 286 trades, profit factor 1.24, t-stat 1.77
- Confirm years: 192 trades, profit factor 1.01, +1.0R, t-stat 0.06 (needed 3.48); markets 6 of 15; double-cost profit factor 0.95; beats 70% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 196)

### 2026-11-23 · screen survivor 197 · `vol_spike_k2.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 144864593a). No stated reason.
- Screen years: 325 trades, profit factor 1.23, t-stat 1.70
- Confirm years: 236 trades, profit factor 1.01, +1.0R, t-stat 0.04 (needed 3.48); markets 5 of 12; double-cost profit factor 0.91; beats 69% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 197)

### 2026-11-23 · screen survivor 198 · `zmove_n72_z2.5.fade.high_vol.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2240b50f63). No stated reason.
- Screen years: 244 trades, profit factor 1.39, t-stat 2.54
- Confirm years: 165 trades, profit factor 1.13, +12.3R, t-stat 0.76 (needed 3.48); markets 8 of 15; double-cost profit factor 1.08; beats 86% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 198)

### 2026-11-23 · screen survivor 199 · `vol_spike_k3.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 002180cfb1). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 179 trades, profit factor 1.36, t-stat 1.90
- Confirm years: 163 trades, profit factor 1.04, +4.5R, t-stat 0.22 (needed 3.48); markets 4 of 11; double-cost profit factor 0.96; beats 67% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 199)

### 2026-11-23 · screen survivor 200 · `zmove_n24_z2.5.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4e6833b069). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 319 trades, profit factor 1.27, t-stat 1.94
- Confirm years: 245 trades, profit factor 0.94, -10.5R, t-stat -0.42 (needed 3.48); markets 6 of 15; double-cost profit factor 0.89; beats 62% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 200)

### 2026-11-23 · screen survivor 201 · `zmove_n24_z2.5.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 44419fd0ec). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 523 trades, profit factor 1.18, t-stat 1.71
- Confirm years: 348 trades, profit factor 1.05, +11.7R, t-stat 0.38 (needed 3.48); markets 9 of 15; double-cost profit factor 0.98; beats 87% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 201)

### 2026-11-23 · screen survivor 202 · `zmove_n24_z2.5.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 99f5d073b7). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 930 trades, profit factor 1.20, t-stat 2.74
- Confirm years: 654 trades, profit factor 0.91, -38.8R, t-stat -1.23 (needed 3.48); markets 6 of 15; double-cost profit factor 0.86; beats 38% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 202)

### 2026-11-23 · screen survivor 203 · `zmove_n24_z2.5.follow.with_trend.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1e29f84414). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 297 trades, profit factor 1.27, t-stat 2.03
- Confirm years: 214 trades, profit factor 0.95, -6.7R, t-stat -0.37 (needed 3.48); markets 7 of 15; double-cost profit factor 0.88; beats 73% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.48 (bar for survivor 203)

### 2026-11-23 · screen survivor 204 · `zmove_n24_z2.5.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9feaa06be3). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 323 trades, profit factor 1.26, t-stat 1.89
- Confirm years: 253 trades, profit factor 1.05, +8.7R, t-stat 0.34 (needed 3.49); markets 8 of 15; double-cost profit factor 1.00; beats 77% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.49 (bar for survivor 204)

### 2026-11-23 · screen survivor 205 · `big_bar_k3.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 684f2f77bc). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1177 trades, profit factor 1.12, t-stat 1.84
- Confirm years: 710 trades, profit factor 0.92, -37.9R, t-stat -1.15 (needed 3.49); markets 4 of 15; double-cost profit factor 0.86; beats 36% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.49 (bar for survivor 205)

### 2026-11-23 · screen survivor 206 · `big_bar_k3.fade.none.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 49d67cb6f9). No stated reason.
- Screen years: 822 trades, profit factor 1.15, t-stat 1.77
- Confirm years: 447 trades, profit factor 0.93, -23.5R, t-stat -0.71 (needed 3.49); markets 3 of 15; double-cost profit factor 0.87; beats 32% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.49 (bar for survivor 206)

### 2026-11-23 · screen survivor 207 · `zmove_n24_z2.5.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 7c734c694e). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 858 trades, profit factor 1.21, t-stat 2.59
- Confirm years: 599 trades, profit factor 1.01, +4.2R, t-stat 0.11 (needed 3.49); markets 7 of 15; double-cost profit factor 0.96; beats 72% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.49 (bar for survivor 207)

### 2026-11-23 · screen survivor 208 · `zmove_n24_z2.5.follow.none.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9ddbbca581). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1049 trades, profit factor 1.18, t-stat 2.38
- Confirm years: 736 trades, profit factor 1.00, -0.1R, t-stat -0.00 (needed 3.49); markets 6 of 15; double-cost profit factor 0.96; beats 72% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.49 (bar for survivor 208)

### 2026-11-23 · screen survivor 209 · `zmove_n24_z2.5.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0224cd7dec). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 336 trades, profit factor 1.27, t-stat 2.16
- Confirm years: 261 trades, profit factor 0.95, -7.8R, t-stat -0.39 (needed 3.49); markets 6 of 15; double-cost profit factor 0.91; beats 58% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.49 (bar for survivor 209)

### 2026-11-23 · screen survivor 210 · `breakout_n168.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0b39e791c8). No stated reason.
- Screen years: 701 trades, profit factor 1.16, t-stat 1.92
- Confirm years: 490 trades, profit factor 1.02, +6.8R, t-stat 0.25 (needed 3.49); markets 8 of 15; double-cost profit factor 0.97; beats 80% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.49 (bar for survivor 210)

### 2026-11-23 · screen survivor 211 · `big_bar_k3.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 88aa5bd8fe). No stated reason.
- Screen years: 213 trades, profit factor 1.38, t-stat 2.16
- Confirm years: 174 trades, profit factor 1.17, +20.3R, t-stat 0.93 (needed 3.50); markets 10 of 15; double-cost profit factor 1.09; beats 90% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.50 (bar for survivor 211)

### 2026-11-23 · screen survivor 212 · `vol_spike_k3.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b7ff9bc0fb). No stated reason.
- Screen years: 258 trades, profit factor 1.30, t-stat 2.05
- Confirm years: 225 trades, profit factor 1.10, +12.7R, t-stat 0.68 (needed 3.50); markets 6 of 11; double-cost profit factor 1.01; beats 94% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 212)

### 2026-11-23 · screen survivor 213 · `squeeze_break_n24.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8ac53e3faf). No stated reason.
- Screen years: 1968 trades, profit factor 1.10, t-stat 1.93
- Confirm years: 1411 trades, profit factor 0.95, -54.3R, t-stat -0.91 (needed 3.50); markets 7 of 15; double-cost profit factor 0.88; beats 10% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 213)

### 2026-11-23 · screen survivor 214 · `big_bar_k3.fade.with_trend.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 44c1a69586). No stated reason.
- Screen years: 310 trades, profit factor 1.22, t-stat 1.70
- Confirm years: 176 trades, profit factor 1.01, +0.7R, t-stat 0.04 (needed 3.50); markets 8 of 15; double-cost profit factor 0.94; beats 60% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 214)

### 2026-11-23 · screen survivor 215 · `zmove_n24_z2.5.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ef3791d00e). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 304 trades, profit factor 1.24, t-stat 1.68
- Confirm years: 237 trades, profit factor 0.99, -2.5R, t-stat -0.10 (needed 3.50); markets 8 of 15; double-cost profit factor 0.95; beats 63% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 215)

### 2026-11-23 · screen survivor 216 · `clock_hour0_weekday4.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 12f80190e0). No stated reason.
- Screen years: 971 trades, profit factor 1.15, t-stat 1.95
- Confirm years: 681 trades, profit factor 1.07, +35.5R, t-stat 0.82 (needed 3.50); markets 9 of 15; double-cost profit factor 1.01; beats 27% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 216)

### 2026-11-23 · screen survivor 217 · `zmove_n24_z2.5.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2a1f6a6e72). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 279 trades, profit factor 1.27, t-stat 1.81
- Confirm years: 200 trades, profit factor 1.00, +0.2R, t-stat 0.01 (needed 3.50); markets 8 of 15; double-cost profit factor 0.96; beats 63% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 217)

### 2026-11-23 · screen survivor 218 · `big_bar_k3.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 21a1890074). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 217 trades, profit factor 1.26, t-stat 1.66
- Confirm years: 179 trades, profit factor 1.04, +4.8R, t-stat 0.29 (needed 3.50); markets 7 of 15; double-cost profit factor 0.97; beats 84% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 218)

### 2026-11-23 · screen survivor 219 · `zmove_n24_z2.5.follow.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id eb72b15884). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 615 trades, profit factor 1.18, t-stat 1.83
- Confirm years: 413 trades, profit factor 1.03, +8.4R, t-stat 0.26 (needed 3.50); markets 9 of 15; double-cost profit factor 0.98; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.50 (bar for survivor 219)

### 2026-11-23 · screen survivor 220 · `streak_k5.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b120889724). No stated reason.
- Screen years: 1128 trades, profit factor 1.12, t-stat 1.74
- Confirm years: 830 trades, profit factor 1.24, +134.3R, t-stat 2.85 (needed 3.51); markets 9 of 15; double-cost profit factor 1.15; beats 100% of random entries
- Failed: t-stat >= 3.51 (bar for survivor 220)

### 2026-11-23 · screen survivor 221 · `zmove_n72_z2.5.fade.high_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3b2a2cfcf3). No stated reason.
- Screen years: 243 trades, profit factor 1.27, t-stat 1.72
- Confirm years: 165 trades, profit factor 1.07, +8.0R, t-stat 0.38 (needed 3.51); markets 6 of 15; double-cost profit factor 1.02; beats 69% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; beats 95% of random entries; t-stat >= 3.51 (bar for survivor 221)

### 2026-11-23 · screen survivor 222 · `zmove_n24_z2.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8977a9d333). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 690 trades, profit factor 1.15, t-stat 1.80
- Confirm years: 498 trades, profit factor 1.00, -0.7R, t-stat -0.03 (needed 3.51); markets 6 of 15; double-cost profit factor 0.94; beats 74% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.51 (bar for survivor 222)

### 2026-11-23 · screen survivor 223 · `zmove_n72_z2.5.fade.none.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2bf1f7a964). No stated reason.
- Screen years: 304 trades, profit factor 1.23, t-stat 1.77
- Confirm years: 198 trades, profit factor 1.00, -0.3R, t-stat -0.01 (needed 3.51); markets 6 of 15; double-cost profit factor 0.94; beats 66% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.51 (bar for survivor 223)

### 2026-11-23 · screen survivor 224 · `zmove_n24_z2.5.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b6aebe09c4). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 489 trades, profit factor 1.25, t-stat 2.23
- Confirm years: 331 trades, profit factor 1.04, +10.1R, t-stat 0.34 (needed 3.51); markets 8 of 15; double-cost profit factor 1.00; beats 77% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.51 (bar for survivor 224)

### 2026-11-23 · screen survivor 225 · `squeeze_break_n72.fade.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id da48fc1c51). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 264 trades, profit factor 1.33, t-stat 2.31
- Confirm years: 183 trades, profit factor 0.84, -19.4R, t-stat -1.17 (needed 3.51); markets 5 of 15; double-cost profit factor 0.78; beats 22% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.51 (bar for survivor 225)

### 2026-11-23 · screen survivor 226 · `big_bar_k3.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b5f2262ce8). No stated reason.
- Screen years: 1880 trades, profit factor 1.11, t-stat 2.02
- Confirm years: 1195 trades, profit factor 0.95, -41.5R, t-stat -0.75 (needed 3.51); markets 6 of 15; double-cost profit factor 0.88; beats 62% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.51 (bar for survivor 226)

### 2026-11-23 · screen survivor 227 · `vol_spike_k2.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 77f2f740c0). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 525 trades, profit factor 1.40, t-stat 3.53
- Confirm years: 394 trades, profit factor 1.07, +18.5R, t-stat 0.57 (needed 3.51); markets 4 of 13; double-cost profit factor 0.99; beats 79% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.51 (bar for survivor 227)

### 2026-11-23 · screen survivor 228 · `zmove_n24_z2.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 967c1296b7). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 842 trades, profit factor 1.15, t-stat 1.80
- Confirm years: 611 trades, profit factor 0.97, -12.6R, t-stat -0.32 (needed 3.52); markets 5 of 15; double-cost profit factor 0.93; beats 51% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 228)

### 2026-11-23 · screen survivor 229 · `vol_spike_k3.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b00aef2684). No stated reason.
- Screen years: 261 trades, profit factor 1.37, t-stat 2.32
- Confirm years: 227 trades, profit factor 0.90, -16.6R, t-stat -0.70 (needed 3.52); markets 2 of 11; double-cost profit factor 0.81; beats 62% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 229)

### 2026-11-23 · screen survivor 230 · `big_bar_k3.follow.with_trend.ny.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3f68d8ef21). No stated reason.
- Screen years: 1226 trades, profit factor 1.11, t-stat 1.85
- Confirm years: 735 trades, profit factor 0.84, -78.5R, t-stat -2.36 (needed 3.52); markets 2 of 15; double-cost profit factor 0.77; beats 22% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 230)

### 2026-11-23 · screen survivor 231 · `big_bar_k3.fade.high_vol.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a243fd3cee). No stated reason.
- Screen years: 448 trades, profit factor 1.18, t-stat 1.70
- Confirm years: 232 trades, profit factor 0.91, -13.6R, t-stat -0.72 (needed 3.52); markets 6 of 15; double-cost profit factor 0.86; beats 35% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 231)

### 2026-11-23 · screen survivor 232 · `zmove_n24_z2.5.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 50a7905a6e). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 948 trades, profit factor 1.17, t-stat 2.19
- Confirm years: 655 trades, profit factor 0.99, -6.5R, t-stat -0.16 (needed 3.52); markets 8 of 15; double-cost profit factor 0.92; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 232)

### 2026-11-23 · screen survivor 233 · `squeeze_break_n24.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5270986dd1). No stated reason.
- Screen years: 1104 trades, profit factor 1.17, t-stat 2.34
- Confirm years: 774 trades, profit factor 0.89, -68.1R, t-stat -1.54 (needed 3.52); markets 4 of 15; double-cost profit factor 0.83; beats 4% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 233)

### 2026-11-23 · screen survivor 234 · `open_distance_frac1.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 60219371f9). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1841 trades, profit factor 1.12, t-stat 2.23
- Confirm years: 1318 trades, profit factor 0.96, -35.0R, t-stat -0.60 (needed 3.52); markets 3 of 15; double-cost profit factor 0.90; beats 65% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 234)

### 2026-11-23 · screen survivor 235 · `open_distance_frac1.follow.with_trend.any.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d4c7a89544). No stated reason.
- Screen years: 1943 trades, profit factor 1.10, t-stat 2.09
- Confirm years: 1390 trades, profit factor 0.95, -42.1R, t-stat -0.91 (needed 3.52); markets 2 of 15; double-cost profit factor 0.87; beats 87% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 235)

### 2026-11-23 · screen survivor 236 · `open_distance_frac1.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6b27319d49). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 198 trades, profit factor 1.78, t-stat 3.75
- Confirm years: 180 trades, profit factor 0.78, -32.0R, t-stat -1.56 (needed 3.52); markets 5 of 15; double-cost profit factor 0.72; beats 18% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.52 (bar for survivor 236)

### 2026-11-23 · screen survivor 237 · `open_distance_frac1.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 976464a120). No stated reason.
- Screen years: 164 trades, profit factor 1.53, t-stat 2.50
- Confirm years: 144 trades, profit factor 0.76, -27.8R, t-stat -1.53 (needed 3.53); markets 5 of 15; double-cost profit factor 0.71; beats 19% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.53 (bar for survivor 237)

### 2026-11-23 · screen survivor 238 · `open_distance_frac1.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 59397f8804). No stated reason.
- Screen years: 166 trades, profit factor 1.99, t-stat 4.15
- Confirm years: 143 trades, profit factor 0.83, -18.7R, t-stat -1.00 (needed 3.53); markets 6 of 15; double-cost profit factor 0.77; beats 31% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.53 (bar for survivor 238)

### 2026-11-23 · screen survivor 239 · `open_distance_frac0.5.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ec387ffd4c). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 847 trades, profit factor 1.18, t-stat 2.23
- Confirm years: 674 trades, profit factor 1.15, +69.7R, t-stat 1.64 (needed 3.53); markets 11 of 15; double-cost profit factor 1.08; beats 94% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.53 (bar for survivor 239)

### 2026-11-23 · screen survivor 240 · `open_distance_frac1.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6103de0193). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 192 trades, profit factor 1.71, t-stat 3.40
- Confirm years: 174 trades, profit factor 0.81, -25.2R, t-stat -1.26 (needed 3.53); markets 7 of 15; double-cost profit factor 0.77; beats 16% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.53 (bar for survivor 240)

### 2026-11-23 · screen survivor 241 · `open_distance_frac1.follow.with_trend.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9b44ccc13d). No stated reason.
- Screen years: 166 trades, profit factor 1.74, t-stat 3.56
- Confirm years: 143 trades, profit factor 1.21, +17.0R, t-stat 1.13 (needed 3.53); markets 13 of 15; double-cost profit factor 1.11; beats 97% of random entries
- Failed: t-stat >= 3.53 (bar for survivor 241)

### 2026-11-23 · screen survivor 242 · `open_distance_frac1.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6477157db3). No stated reason.
- Screen years: 160 trades, profit factor 1.48, t-stat 2.25
- Confirm years: 138 trades, profit factor 0.85, -15.8R, t-stat -0.88 (needed 3.53); markets 8 of 15; double-cost profit factor 0.81; beats 28% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.53 (bar for survivor 242)

### 2026-11-23 · screen survivor 243 · `open_distance_frac1.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ba5d06265e). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 663 trades, profit factor 1.17, t-stat 1.81
- Confirm years: 438 trades, profit factor 1.18, +53.5R, t-stat 1.55 (needed 3.53); markets 8 of 15; double-cost profit factor 1.11; beats 90% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.53 (bar for survivor 243)

### 2026-11-23 · screen survivor 244 · `open_distance_frac1.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id dfc2d6c9ac). No stated reason.
- Screen years: 163 trades, profit factor 1.88, t-stat 4.00
- Confirm years: 143 trades, profit factor 0.95, -4.6R, t-stat -0.31 (needed 3.53); markets 7 of 15; double-cost profit factor 0.90; beats 58% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.53 (bar for survivor 244)

### 2026-11-23 · screen survivor 245 · `open_distance_frac1.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 12cbe38677). No stated reason.
- Screen years: 162 trades, profit factor 1.94, t-stat 3.92
- Confirm years: 138 trades, profit factor 0.78, -23.7R, t-stat -1.33 (needed 3.53); markets 7 of 15; double-cost profit factor 0.74; beats 10% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.53 (bar for survivor 245)

### 2026-11-23 · screen survivor 246 · `open_distance_frac0.5.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9fa8ebd0bd). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 419 trades, profit factor 1.35, t-stat 2.78
- Confirm years: 371 trades, profit factor 1.06, +17.1R, t-stat 0.55 (needed 3.54); markets 5 of 15; double-cost profit factor 0.98; beats 77% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 246)

### 2026-11-23 · screen survivor 247 · `open_distance_frac0.5.follow.low_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 26555b6a88). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 435 trades, profit factor 1.18, t-stat 1.69
- Confirm years: 383 trades, profit factor 1.08, +18.4R, t-stat 0.75 (needed 3.54); markets 6 of 15; double-cost profit factor 0.99; beats 90% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 247)

### 2026-11-23 · screen survivor 248 · `open_distance_frac0.5.fade.high_vol.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3174241af6). No stated reason.
- Screen years: 1815 trades, profit factor 1.11, t-stat 2.13
- Confirm years: 1255 trades, profit factor 0.92, -58.8R, t-stat -1.38 (needed 3.54); markets 6 of 15; double-cost profit factor 0.87; beats 42% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 248)

### 2026-11-23 · screen survivor 249 · `open_distance_frac0.5.follow.low_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1ad5d72682). No stated reason.
- Screen years: 441 trades, profit factor 1.19, t-stat 1.71
- Confirm years: 385 trades, profit factor 1.25, +68.2R, t-stat 2.03 (needed 3.54); markets 7 of 15; double-cost profit factor 1.12; beats 100% of random entries
- Failed: profitable in half the markets that traded; t-stat >= 3.54 (bar for survivor 249)

### 2026-11-23 · screen survivor 250 · `open_distance_frac1.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 29891fbafa). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 195 trades, profit factor 2.07, t-stat 5.08
- Confirm years: 179 trades, profit factor 0.95, -5.2R, t-stat -0.31 (needed 3.54); markets 8 of 15; double-cost profit factor 0.90; beats 57% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 250)

### 2026-11-23 · screen survivor 251 · `open_distance_frac0.5.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ba644a6c83). No stated reason.
- Screen years: 1742 trades, profit factor 1.12, t-stat 2.07
- Confirm years: 1224 trades, profit factor 1.06, +53.0R, t-stat 0.97 (needed 3.54); markets 8 of 15; double-cost profit factor 1.00; beats 83% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 251)

### 2026-11-23 · screen survivor 252 · `open_distance_frac1.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2e0c1938b2). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1586 trades, profit factor 1.12, t-stat 1.99
- Confirm years: 1104 trades, profit factor 0.99, -7.5R, t-stat -0.14 (needed 3.54); markets 7 of 15; double-cost profit factor 0.94; beats 50% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 252)

### 2026-11-23 · screen survivor 253 · `open_distance_frac1.follow.high_vol.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e209bf2d70). No stated reason.
- Screen years: 164 trades, profit factor 1.42, t-stat 2.20
- Confirm years: 144 trades, profit factor 1.02, +1.9R, t-stat 0.13 (needed 3.54); markets 7 of 15; double-cost profit factor 0.95; beats 82% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 253)

### 2026-11-23 · screen survivor 254 · `open_distance_frac0.5.fade.high_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b6bbc03a16). No stated reason.
- Screen years: 1735 trades, profit factor 1.13, t-stat 2.35
- Confirm years: 1209 trades, profit factor 0.93, -61.9R, t-stat -1.21 (needed 3.54); markets 6 of 15; double-cost profit factor 0.87; beats 33% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.54 (bar for survivor 254)

### 2026-11-23 · screen survivor 255 · `open_distance_frac1.follow.none.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8fefaa1bf3). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 198 trades, profit factor 1.65, t-stat 3.49
- Confirm years: 181 trades, profit factor 1.09, +9.4R, t-stat 0.55 (needed 3.55); markets 10 of 15; double-cost profit factor 1.00; beats 95% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 255)

### 2026-11-23 · screen survivor 256 · `open_distance_frac1.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 232bf4ce49). No stated reason.
- Screen years: 165 trades, profit factor 2.28, t-stat 5.36
- Confirm years: 142 trades, profit factor 1.03, +2.5R, t-stat 0.17 (needed 3.55); markets 11 of 15; double-cost profit factor 0.97; beats 68% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 256)

### 2026-11-23 · screen survivor 257 · `a158_cntd_n20.follow.against_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a698cd1ab1). No stated reason.
- Screen years: 545 trades, profit factor 1.18, t-stat 1.78
- Confirm years: 446 trades, profit factor 1.06, +20.1R, t-stat 0.58 (needed 3.55); markets 7 of 15; double-cost profit factor 0.97; beats 95% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 257)

### 2026-11-23 · screen survivor 258 · `a158_cntd_n20.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 93b946b84c). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 710 trades, profit factor 1.17, t-stat 2.03
- Confirm years: 462 trades, profit factor 1.34, +81.5R, t-stat 3.04 (needed 3.55); markets 12 of 15; double-cost profit factor 1.26; beats 100% of random entries
- Failed: t-stat >= 3.55 (bar for survivor 258)

### 2026-11-23 · screen survivor 259 · `a158_cntd_n20.follow.high_vol.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e545d974ff). No stated reason.
- Screen years: 731 trades, profit factor 1.13, t-stat 1.67
- Confirm years: 477 trades, profit factor 1.00, +0.4R, t-stat 0.02 (needed 3.55); markets 10 of 15; double-cost profit factor 0.92; beats 91% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 259)

### 2026-11-23 · screen survivor 260 · `a158_cntd_n20.follow.against_trend.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 245cdabcf0). No stated reason.
- Screen years: 553 trades, profit factor 1.18, t-stat 1.88
- Confirm years: 448 trades, profit factor 0.87, -39.1R, t-stat -1.49 (needed 3.55); markets 5 of 15; double-cost profit factor 0.78; beats 52% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 260)

### 2026-11-23 · screen survivor 261 · `a158_cord_n60.follow.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5af7f61a61). No stated reason.
- Screen years: 1049 trades, profit factor 1.15, t-stat 2.00
- Confirm years: 710 trades, profit factor 1.09, +42.9R, t-stat 1.00 (needed 3.55); markets 8 of 15; double-cost profit factor 1.02; beats 92% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 261)

### 2026-11-23 · screen survivor 262 · `a158_cord_n20.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4970aba2e8). No stated reason.
- Screen years: 668 trades, profit factor 1.16, t-stat 1.69
- Confirm years: 425 trades, profit factor 1.03, +9.1R, t-stat 0.28 (needed 3.55); markets 7 of 15; double-cost profit factor 0.98; beats 77% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 262)

### 2026-11-23 · screen survivor 263 · `a158_cord_n60.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5759b9f731). No stated reason.
- Screen years: 621 trades, profit factor 1.23, t-stat 2.36
- Confirm years: 389 trades, profit factor 1.08, +22.7R, t-stat 0.70 (needed 3.55); markets 9 of 15; double-cost profit factor 1.02; beats 75% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 263)

### 2026-11-23 · screen survivor 264 · `a158_cord_n20.fade.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 35ba1c4c90). No stated reason.
- Screen years: 723 trades, profit factor 1.17, t-stat 1.89
- Confirm years: 466 trades, profit factor 1.03, +8.7R, t-stat 0.25 (needed 3.55); markets 7 of 15; double-cost profit factor 0.95; beats 87% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.55 (bar for survivor 264)

### 2026-11-23 · screen survivor 265 · `a158_cord_n20.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1442c23e13). No stated reason.
- Screen years: 692 trades, profit factor 1.20, t-stat 2.39
- Confirm years: 437 trades, profit factor 1.09, +23.7R, t-stat 0.92 (needed 3.56); markets 9 of 15; double-cost profit factor 1.04; beats 95% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.56 (bar for survivor 265)

### 2026-11-23 · screen survivor 266 · `a158_corr_n60.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 978f603cef). No stated reason.
- Screen years: 877 trades, profit factor 1.19, t-stat 2.38
- Confirm years: 560 trades, profit factor 1.03, +11.5R, t-stat 0.30 (needed 3.56); markets 7 of 15; double-cost profit factor 0.98; beats 64% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.56 (bar for survivor 266)

### 2026-11-23 · screen survivor 267 · `a158_corr_n60.follow.low_vol.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4224a0fa27). No stated reason.
- Screen years: 771 trades, profit factor 1.14, t-stat 1.75
- Confirm years: 452 trades, profit factor 1.15, +38.9R, t-stat 1.46 (needed 3.56); markets 9 of 15; double-cost profit factor 1.07; beats 97% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.56 (bar for survivor 267)

### 2026-11-23 · screen survivor 268 · `a158_corr_n60.follow.with_trend.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b86aa36491). No stated reason.
- Screen years: 627 trades, profit factor 1.18, t-stat 2.07
- Confirm years: 397 trades, profit factor 1.00, +0.5R, t-stat 0.02 (needed 3.56); markets 6 of 15; double-cost profit factor 0.94; beats 62% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.56 (bar for survivor 268)

### 2026-11-23 · screen survivor 269 · `a158_corr_n60.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id adb40dc5d9). No stated reason.
- Screen years: 953 trades, profit factor 1.18, t-stat 2.47
- Confirm years: 615 trades, profit factor 1.10, +34.5R, t-stat 1.11 (needed 3.56); markets 9 of 15; double-cost profit factor 1.04; beats 96% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.56 (bar for survivor 269)

### 2026-11-23 · screen survivor 270 · `a158_corr_n60.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5105d0c461). No stated reason.
- Screen years: 1585 trades, profit factor 1.13, t-stat 2.28
- Confirm years: 1007 trades, profit factor 0.98, -14.7R, t-stat -0.29 (needed 3.56); markets 8 of 15; double-cost profit factor 0.93; beats 42% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.56 (bar for survivor 270)

### 2026-11-23 · screen survivor 271 · `a158_corr_n60.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d35f35d691). No stated reason.
- Screen years: 742 trades, profit factor 1.16, t-stat 1.84
- Confirm years: 425 trades, profit factor 1.26, +74.9R, t-stat 2.19 (needed 3.56); markets 12 of 15; double-cost profit factor 1.19; beats 99% of random entries
- Failed: t-stat >= 3.56 (bar for survivor 271)

### 2026-11-23 · screen survivor 272 · `a158_corr_n60.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id fe28ffa7a3). No stated reason.
- Screen years: 992 trades, profit factor 1.15, t-stat 2.02
- Confirm years: 629 trades, profit factor 1.06, +28.5R, t-stat 0.69 (needed 3.56); markets 9 of 15; double-cost profit factor 0.99; beats 90% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.56 (bar for survivor 272)

### 2026-11-23 · screen survivor 273 · `a158_corr_n60.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 08ef337cfd). No stated reason.
- Screen years: 1824 trades, profit factor 1.11, t-stat 2.17
- Confirm years: 1166 trades, profit factor 1.01, +8.7R, t-stat 0.21 (needed 3.56); markets 8 of 15; double-cost profit factor 0.95; beats 76% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.56 (bar for survivor 273)

### 2026-11-23 · screen survivor 274 · `a158_resi_n60.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 85e8b82a1b). No stated reason.
- Screen years: 1129 trades, profit factor 1.14, t-stat 2.05
- Confirm years: 753 trades, profit factor 1.03, +16.1R, t-stat 0.36 (needed 3.56); markets 9 of 15; double-cost profit factor 0.96; beats 92% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.56 (bar for survivor 274)

### 2026-11-23 · screen survivor 275 · `a158_resi_n20.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id eae536674a). No stated reason.
- Screen years: 178 trades, profit factor 1.37, t-stat 1.92
- Confirm years: 154 trades, profit factor 1.01, +1.2R, t-stat 0.06 (needed 3.57); markets 6 of 15; double-cost profit factor 0.93; beats 72% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 275)

### 2026-11-23 · screen survivor 276 · `a158_resi_n20.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 86508b0cde). No stated reason.
- Screen years: 1367 trades, profit factor 1.14, t-stat 2.11
- Confirm years: 818 trades, profit factor 1.12, +62.5R, t-stat 1.40 (needed 3.57); markets 9 of 15; double-cost profit factor 1.04; beats 98% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.57 (bar for survivor 276)

### 2026-11-23 · screen survivor 277 · `a158_resi_n20.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3ceb13bc1a). No stated reason.
- Screen years: 1833 trades, profit factor 1.14, t-stat 2.49
- Confirm years: 1127 trades, profit factor 0.92, -65.4R, t-stat -1.22 (needed 3.57); markets 6 of 15; double-cost profit factor 0.86; beats 49% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 277)

### 2026-11-23 · screen survivor 278 · `a158_resi_n60.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 845cbd8d83). No stated reason.
- Screen years: 1576 trades, profit factor 1.14, t-stat 2.40
- Confirm years: 1068 trades, profit factor 1.02, +13.7R, t-stat 0.26 (needed 3.57); markets 9 of 15; double-cost profit factor 0.97; beats 75% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 278)

### 2026-11-23 · screen survivor 279 · `a158_resi_n60.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d468fc8200). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1030 trades, profit factor 1.20, t-stat 2.66
- Confirm years: 669 trades, profit factor 1.07, +32.8R, t-stat 0.78 (needed 3.57); markets 10 of 15; double-cost profit factor 1.02; beats 90% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 279)

### 2026-11-23 · screen survivor 280 · `a158_resi_n60.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d44e0df43e). No stated reason.
- Screen years: 541 trades, profit factor 1.17, t-stat 1.78
- Confirm years: 414 trades, profit factor 0.86, -36.6R, t-stat -1.50 (needed 3.57); markets 3 of 15; double-cost profit factor 0.81; beats 25% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 280)

### 2026-11-23 · screen survivor 281 · `a158_resi_n60.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 35fd4d48bc). No stated reason.
- Screen years: 477 trades, profit factor 1.26, t-stat 2.25
- Confirm years: 294 trades, profit factor 1.36, +69.2R, t-stat 2.42 (needed 3.57); markets 10 of 15; double-cost profit factor 1.29; beats 100% of random entries
- Failed: t-stat >= 3.57 (bar for survivor 281)

### 2026-11-23 · screen survivor 282 · `a158_resi_n60.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 749fd5a00e). No stated reason.
- Screen years: 1788 trades, profit factor 1.10, t-stat 1.86
- Confirm years: 1264 trades, profit factor 0.90, -96.0R, t-stat -1.71 (needed 3.57); markets 3 of 15; double-cost profit factor 0.84; beats 35% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 282)

### 2026-11-23 · screen survivor 283 · `a158_resi_n20.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c8b0987c8e). No stated reason.
- Screen years: 839 trades, profit factor 1.15, t-stat 1.78
- Confirm years: 456 trades, profit factor 1.12, +37.9R, t-stat 1.10 (needed 3.57); markets 10 of 15; double-cost profit factor 1.05; beats 94% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 283)

### 2026-11-23 · screen survivor 284 · `a158_resi_n60.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c30d88b7c4). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 344 trades, profit factor 1.24, t-stat 1.99
- Confirm years: 290 trades, profit factor 0.88, -22.7R, t-stat -1.09 (needed 3.57); markets 4 of 15; double-cost profit factor 0.83; beats 33% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.57 (bar for survivor 284)

### 2026-11-23 · screen survivor 285 · `a158_resi_n60.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a46f22cf04). No stated reason.
- Screen years: 752 trades, profit factor 1.20, t-stat 2.27
- Confirm years: 462 trades, profit factor 1.23, +70.0R, t-stat 2.01 (needed 3.57); markets 11 of 15; double-cost profit factor 1.15; beats 99% of random entries
- Failed: t-stat >= 3.57 (bar for survivor 285)

### 2026-11-23 · screen survivor 286 · `a158_resi_n60.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ac9606c5ac). No stated reason.
- Screen years: 636 trades, profit factor 1.18, t-stat 2.05
- Confirm years: 501 trades, profit factor 0.88, -36.2R, t-stat -1.35 (needed 3.58); markets 4 of 15; double-cost profit factor 0.83; beats 32% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.58 (bar for survivor 286)

### 2026-11-23 · screen survivor 287 · `a158_resi_n20.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ce9e422839). No stated reason.
- Screen years: 1579 trades, profit factor 1.11, t-stat 1.93
- Confirm years: 955 trades, profit factor 0.87, -95.9R, t-stat -1.99 (needed 3.58); markets 4 of 15; double-cost profit factor 0.83; beats 8% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.58 (bar for survivor 287)

### 2026-11-23 · screen survivor 288 · `a158_rsqr_n20.follow.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 35a2c2e4a1). No stated reason.
- Screen years: 1195 trades, profit factor 1.20, t-stat 3.14
- Confirm years: 783 trades, profit factor 1.23, +98.1R, t-stat 2.83 (needed 3.58); markets 14 of 15; double-cost profit factor 1.15; beats 100% of random entries
- Failed: t-stat >= 3.58 (bar for survivor 288)

### 2026-11-23 · screen survivor 289 · `a158_rsqr_n20.follow.low_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8785da4231). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 577 trades, profit factor 1.24, t-stat 2.58
- Confirm years: 390 trades, profit factor 1.19, +41.5R, t-stat 1.68 (needed 3.58); markets 10 of 15; double-cost profit factor 1.10; beats 97% of random entries
- Failed: t-stat >= 3.58 (bar for survivor 289)

### 2026-11-23 · screen survivor 290 · `a158_rsqr_n20.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 318b6c91ef). No stated reason.
- Screen years: 1132 trades, profit factor 1.13, t-stat 1.85
- Confirm years: 747 trades, profit factor 1.22, +109.7R, t-stat 2.48 (needed 3.58); markets 11 of 15; double-cost profit factor 1.16; beats 99% of random entries
- Failed: t-stat >= 3.58 (bar for survivor 290)

### 2026-11-23 · screen survivor 291 · `a158_rsqr_n20.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 68f31264b8). No stated reason.
- Screen years: 833 trades, profit factor 1.22, t-stat 2.60
- Confirm years: 540 trades, profit factor 1.15, +59.5R, t-stat 1.54 (needed 3.58); markets 11 of 15; double-cost profit factor 1.07; beats 98% of random entries
- Failed: t-stat >= 3.58 (bar for survivor 291)

### 2026-11-23 · screen survivor 292 · `a158_rsqr_n20.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9a5466a101). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 558 trades, profit factor 1.27, t-stat 2.57
- Confirm years: 378 trades, profit factor 1.05, +14.7R, t-stat 0.47 (needed 3.58); markets 9 of 15; double-cost profit factor 0.98; beats 66% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.58 (bar for survivor 292)

### 2026-11-23 · screen survivor 293 · `a158_rsqr_n20.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1ca3ca41d9). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 764 trades, profit factor 1.19, t-stat 2.19
- Confirm years: 500 trades, profit factor 1.19, +66.3R, t-stat 1.79 (needed 3.58); markets 11 of 15; double-cost profit factor 1.13; beats 96% of random entries
- Failed: t-stat >= 3.58 (bar for survivor 293)

### 2026-11-23 · screen survivor 294 · `a158_rsqr_n20.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 244f489882). No stated reason.
- Screen years: 630 trades, profit factor 1.21, t-stat 2.39
- Confirm years: 415 trades, profit factor 1.25, +57.1R, t-stat 2.26 (needed 3.58); markets 10 of 15; double-cost profit factor 1.19; beats 100% of random entries
- Failed: t-stat >= 3.58 (bar for survivor 294)

### 2026-11-23 · screen survivor 295 · `a158_rsqr_n20.follow.low_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ed73f39ccf). No stated reason.
- Screen years: 607 trades, profit factor 1.20, t-stat 2.03
- Confirm years: 436 trades, profit factor 1.32, +92.4R, t-stat 2.64 (needed 3.58); markets 12 of 15; double-cost profit factor 1.21; beats 100% of random entries
- Failed: t-stat >= 3.58 (bar for survivor 295)

### 2026-11-23 · screen survivor 296 · `a158_rsqr_n20.follow.against_trend.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 29512473d1). No stated reason.
- Screen years: 414 trades, profit factor 1.19, t-stat 1.65
- Confirm years: 289 trades, profit factor 1.14, +28.4R, t-stat 1.01 (needed 3.58); markets 8 of 15; double-cost profit factor 1.06; beats 92% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.58 (bar for survivor 296)

### 2026-11-23 · screen survivor 297 · `a158_rsqr_n20.follow.high_vol.asia.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 529b682ff1). No stated reason.
- Screen years: 652 trades, profit factor 1.14, t-stat 1.67
- Confirm years: 426 trades, profit factor 1.10, +25.8R, t-stat 1.00 (needed 3.59); markets 9 of 15; double-cost profit factor 1.02; beats 98% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.59 (bar for survivor 297)

### 2026-11-23 · screen survivor 298 · `a158_rsqr_n20.follow.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8365f6b609). No stated reason.
- Screen years: 640 trades, profit factor 1.16, t-stat 1.70
- Confirm years: 421 trades, profit factor 1.23, +66.9R, t-stat 1.96 (needed 3.59); markets 12 of 15; double-cost profit factor 1.16; beats 99% of random entries
- Failed: t-stat >= 3.59 (bar for survivor 298)

### 2026-11-23 · screen survivor 299 · `a158_rsqr_n20.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 74072a5926). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 818 trades, profit factor 1.27, t-stat 3.37
- Confirm years: 529 trades, profit factor 1.16, +49.1R, t-stat 1.71 (needed 3.59); markets 10 of 15; double-cost profit factor 1.09; beats 98% of random entries
- Failed: t-stat >= 3.59 (bar for survivor 299)

### 2026-11-23 · screen survivor 300 · `a158_rsqr_n20.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 55a1feb748). No stated reason.
- Screen years: 1213 trades, profit factor 1.15, t-stat 2.29
- Confirm years: 796 trades, profit factor 1.14, +80.9R, t-stat 1.74 (needed 3.59); markets 12 of 15; double-cost profit factor 1.06; beats 100% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.59 (bar for survivor 300)

### 2026-11-23 · screen survivor 301 · `a158_rsqr_n20.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e80f5a143d). No stated reason.
- Screen years: 2110 trades, profit factor 1.11, t-stat 2.06
- Confirm years: 1449 trades, profit factor 1.18, +169.2R, t-stat 2.78 (needed 3.59); markets 12 of 15; double-cost profit factor 1.09; beats 100% of random entries
- Failed: t-stat >= 3.59 (bar for survivor 301)

### 2026-11-23 · screen survivor 302 · `a158_rsqr_n20.follow.low_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d0e19c2411). No stated reason.
- Screen years: 586 trades, profit factor 1.19, t-stat 1.89
- Confirm years: 392 trades, profit factor 1.06, +17.2R, t-stat 0.53 (needed 3.59); markets 7 of 15; double-cost profit factor 0.96; beats 81% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.59 (bar for survivor 302)

### 2026-11-23 · screen survivor 303 · `a158_shadow_q0.99.follow.high_vol.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 694b2c3091). No stated reason.
- Screen years: 1071 trades, profit factor 1.15, t-stat 2.22
- Confirm years: 655 trades, profit factor 0.99, -2.6R, t-stat -0.08 (needed 3.59); markets 7 of 15; double-cost profit factor 0.94; beats 69% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.59 (bar for survivor 303)

### 2026-11-23 · screen survivor 304 · `a158_shadow_q0.99.follow.against_trend.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4fa92aa9a0). No stated reason.
- Screen years: 755 trades, profit factor 1.17, t-stat 2.08
- Confirm years: 466 trades, profit factor 0.97, -7.6R, t-stat -0.28 (needed 3.59); markets 7 of 15; double-cost profit factor 0.92; beats 65% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.59 (bar for survivor 304)

### 2026-11-23 · screen survivor 305 · `a158_shadow_q0.99.follow.against_trend.london.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e4460bfc77). No stated reason.
- Screen years: 769 trades, profit factor 1.18, t-stat 2.14
- Confirm years: 476 trades, profit factor 0.94, -21.6R, t-stat -0.62 (needed 3.59); markets 7 of 15; double-cost profit factor 0.87; beats 51% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.59 (bar for survivor 305)

### 2026-11-23 · screen survivor 306 · `a158_shadow_q0.99.follow.none.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 27dd33c06d). No stated reason.
- Screen years: 1381 trades, profit factor 1.12, t-stat 1.99
- Confirm years: 851 trades, profit factor 1.01, +3.5R, t-stat 0.10 (needed 3.59); markets 8 of 15; double-cost profit factor 0.95; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.59 (bar for survivor 306)

### 2026-11-23 · screen survivor 307 · `a158_shadow_q0.99.follow.against_trend.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3f91f4c981). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 725 trades, profit factor 1.22, t-stat 2.45
- Confirm years: 444 trades, profit factor 1.02, +5.4R, t-stat 0.16 (needed 3.59); markets 8 of 15; double-cost profit factor 0.97; beats 69% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.59 (bar for survivor 307)

### 2026-11-23 · screen survivor 308 · `a158_shadow_q0.99.follow.high_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 83427bdf8a). No stated reason.
- Screen years: 1027 trades, profit factor 1.16, t-stat 2.12
- Confirm years: 627 trades, profit factor 0.94, -26.6R, t-stat -0.70 (needed 3.59); markets 8 of 15; double-cost profit factor 0.89; beats 30% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.59 (bar for survivor 308)

### 2026-11-23 · screen survivor 309 · `a158_vsumd_n20.follow.against_trend.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 242a4aace2). No stated reason.
- Screen years: 453 trades, profit factor 1.24, t-stat 2.12
- Confirm years: 262 trades, profit factor 0.93, -14.3R, t-stat -0.56 (needed 3.60); markets 5 of 13; double-cost profit factor 0.86; beats 53% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 309)

### 2026-11-23 · screen survivor 310 · `a158_vsumd_n20.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4fe5834ef0). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 478 trades, profit factor 1.29, t-stat 2.53
- Confirm years: 396 trades, profit factor 1.14, +38.0R, t-stat 1.17 (needed 3.60); markets 7 of 12; double-cost profit factor 1.05; beats 93% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 310)

### 2026-11-23 · screen survivor 311 · `a158_vsumd_n20.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c5336d4832). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 303 trades, profit factor 1.30, t-stat 2.09
- Confirm years: 245 trades, profit factor 1.31, +50.9R, t-stat 1.93 (needed 3.60); markets 9 of 12; double-cost profit factor 1.18; beats 99% of random entries
- Failed: t-stat >= 3.60 (bar for survivor 311)

### 2026-11-23 · screen survivor 312 · `a158_vsumd_n20.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a81153439c). No stated reason.
- Screen years: 190 trades, profit factor 1.49, t-stat 2.50
- Confirm years: 166 trades, profit factor 0.93, -8.8R, t-stat -0.43 (needed 3.60); markets 4 of 12; double-cost profit factor 0.88; beats 40% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 312)

### 2026-11-23 · screen survivor 313 · `a158_vsumd_n20.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f513601a7e). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 331 trades, profit factor 1.34, t-stat 2.47
- Confirm years: 271 trades, profit factor 1.09, +17.9R, t-stat 0.66 (needed 3.60); markets 6 of 12; double-cost profit factor 1.01; beats 76% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 313)

### 2026-11-23 · screen survivor 314 · `a158_vsumd_n20.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 25dece0e64). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 350 trades, profit factor 1.25, t-stat 2.06
- Confirm years: 281 trades, profit factor 1.02, +3.0R, t-stat 0.15 (needed 3.60); markets 8 of 12; double-cost profit factor 0.93; beats 72% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 314)

### 2026-11-23 · screen survivor 315 · `a158_vsumd_n20.follow.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 74f24d56ff). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 203 trades, profit factor 1.27, t-stat 1.68
- Confirm years: 169 trades, profit factor 0.86, -15.6R, t-stat -0.99 (needed 3.60); markets 2 of 12; double-cost profit factor 0.80; beats 32% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 315)

### 2026-11-23 · screen survivor 316 · `a158_vsumd_n60.fade.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2ab9051c00). No stated reason.
- Screen years: 1376 trades, profit factor 1.10, t-stat 1.79
- Confirm years: 944 trades, profit factor 0.92, -49.9R, t-stat -1.32 (needed 3.60); markets 4 of 15; double-cost profit factor 0.86; beats 23% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 316)

### 2026-11-23 · screen survivor 317 · `a158_vsumd_n60.fade.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 56665e97bd). No stated reason.
- Screen years: 1216 trades, profit factor 1.13, t-stat 1.92
- Confirm years: 848 trades, profit factor 0.97, -16.2R, t-stat -0.35 (needed 3.60); markets 6 of 15; double-cost profit factor 0.92; beats 37% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 317)

### 2026-11-23 · screen survivor 318 · `alpha007_rank0.9.follow.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 05f3427ba6). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 559 trades, profit factor 1.18, t-stat 1.75
- Confirm years: 493 trades, profit factor 1.03, +10.5R, t-stat 0.30 (needed 3.60); markets 6 of 15; double-cost profit factor 0.98; beats 79% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 318)

### 2026-11-23 · screen survivor 319 · `alpha007_rank0.9.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4dc51a60fa). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 731 trades, profit factor 1.15, t-stat 1.91
- Confirm years: 590 trades, profit factor 0.98, -5.7R, t-stat -0.19 (needed 3.60); markets 7 of 13; double-cost profit factor 0.91; beats 66% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 319)

### 2026-11-23 · screen survivor 320 · `alpha007_rank0.9.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 584f29f357). No stated reason.
- Screen years: 2608 trades, profit factor 1.11, t-stat 2.42
- Confirm years: 1777 trades, profit factor 0.99, -18.8R, t-stat -0.28 (needed 3.60); markets 9 of 15; double-cost profit factor 0.93; beats 50% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.60 (bar for survivor 320)

### 2026-11-23 · screen survivor 321 · `alpha007_rank0.9.follow.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c27f04f9f4). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 760 trades, profit factor 1.20, t-stat 2.35
- Confirm years: 613 trades, profit factor 1.01, +5.0R, t-stat 0.12 (needed 3.61); markets 7 of 13; double-cost profit factor 0.91; beats 83% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 321)

### 2026-11-23 · screen survivor 322 · `alpha012_q0.99.fade.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id aa0a0f7363). No stated reason.
- Screen years: 556 trades, profit factor 1.18, t-stat 1.85
- Confirm years: 415 trades, profit factor 0.96, -9.7R, t-stat -0.40 (needed 3.61); markets 6 of 15; double-cost profit factor 0.91; beats 65% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 322)

### 2026-11-23 · screen survivor 323 · `alpha012_q0.99.fade.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d05978ed1b). No stated reason.
- Screen years: 1413 trades, profit factor 1.13, t-stat 2.04
- Confirm years: 945 trades, profit factor 0.90, -73.7R, t-stat -1.54 (needed 3.61); markets 4 of 15; double-cost profit factor 0.85; beats 14% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 323)

### 2026-11-23 · screen survivor 324 · `alpha012_q0.99.fade.none.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 659dd13d17). No stated reason.
- Screen years: 674 trades, profit factor 1.14, t-stat 1.66
- Confirm years: 536 trades, profit factor 0.90, -33.6R, t-stat -1.21 (needed 3.61); markets 4 of 15; double-cost profit factor 0.85; beats 41% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 324)

### 2026-11-23 · screen survivor 325 · `alpha035_q0.99.fade.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 433231768a). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 353 trades, profit factor 1.49, t-stat 3.43
- Confirm years: 267 trades, profit factor 1.04, +7.8R, t-stat 0.29 (needed 3.61); markets 6 of 12; double-cost profit factor 0.96; beats 67% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 325)

### 2026-11-23 · screen survivor 326 · `alpha035_q0.99.fade.high_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id abe14df4be). No stated reason.
- Screen years: 267 trades, profit factor 1.32, t-stat 2.08
- Confirm years: 209 trades, profit factor 0.96, -6.4R, t-stat -0.28 (needed 3.61); markets 5 of 12; double-cost profit factor 0.90; beats 53% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 326)

### 2026-11-23 · screen survivor 327 · `alpha035_q0.99.fade.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 26df23110e). No stated reason.
- Screen years: 277 trades, profit factor 1.36, t-stat 2.51
- Confirm years: 210 trades, profit factor 0.82, -24.9R, t-stat -1.43 (needed 3.61); markets 3 of 12; double-cost profit factor 0.76; beats 20% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 327)

### 2026-11-23 · screen survivor 328 · `alpha035_q0.99.fade.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1d86cdfa1b). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 362 trades, profit factor 1.24, t-stat 2.01
- Confirm years: 272 trades, profit factor 0.90, -17.2R, t-stat -0.85 (needed 3.61); markets 6 of 12; double-cost profit factor 0.82; beats 38% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 328)

### 2026-11-23 · screen survivor 329 · `alpha035_q0.99.fade.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 54e2471e73). No stated reason.
- Screen years: 1455 trades, profit factor 1.12, t-stat 1.99
- Confirm years: 1030 trades, profit factor 1.12, +85.6R, t-stat 1.68 (needed 3.61); markets 10 of 15; double-cost profit factor 1.05; beats 96% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.61 (bar for survivor 329)

### 2026-11-23 · screen survivor 330 · `alpha035_q0.99.fade.high_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 343f1308f7). No stated reason.
- Screen years: 279 trades, profit factor 1.24, t-stat 1.65
- Confirm years: 212 trades, profit factor 0.79, -35.6R, t-stat -1.59 (needed 3.61); markets 3 of 12; double-cost profit factor 0.72; beats 21% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 330)

### 2026-11-23 · screen survivor 331 · `alpha035_q0.99.fade.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ba4394ac8f). No stated reason.
- Screen years: 366 trades, profit factor 1.21, t-stat 1.67
- Confirm years: 277 trades, profit factor 0.88, -25.3R, t-stat -0.95 (needed 3.61); markets 5 of 12; double-cost profit factor 0.79; beats 40% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 331)

### 2026-11-23 · screen survivor 332 · `alpha035_q0.99.fade.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id dec1d43fa6). No stated reason.
- Screen years: 569 trades, profit factor 1.28, t-stat 2.64
- Confirm years: 444 trades, profit factor 1.00, -0.5R, t-stat -0.02 (needed 3.61); markets 4 of 12; double-cost profit factor 0.92; beats 71% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.61 (bar for survivor 332)

### 2026-11-23 · screen survivor 333 · `alpha035_q0.99.fade.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 2cc192cdfb). No stated reason.
- Screen years: 1657 trades, profit factor 1.14, t-stat 2.47
- Confirm years: 1156 trades, profit factor 0.99, -7.3R, t-stat -0.13 (needed 3.62); markets 7 of 15; double-cost profit factor 0.94; beats 50% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 333)

### 2026-11-23 · screen survivor 334 · `alpha035_q0.99.fade.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d6b5af00a7). No stated reason.
- Screen years: 326 trades, profit factor 1.25, t-stat 1.82
- Confirm years: 248 trades, profit factor 1.04, +7.8R, t-stat 0.30 (needed 3.62); markets 6 of 12; double-cost profit factor 0.95; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 334)

### 2026-11-23 · screen survivor 335 · `alpha046_q0.95.fade.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 532a8e022a). No stated reason.
- Screen years: 767 trades, profit factor 1.17, t-stat 1.93
- Confirm years: 459 trades, profit factor 1.17, +53.0R, t-stat 1.53 (needed 3.62); markets 9 of 15; double-cost profit factor 1.11; beats 96% of random entries
- Failed: t-stat >= 3.62 (bar for survivor 335)

### 2026-11-23 · screen survivor 336 · `cmf_extreme_n20.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c9309c6915). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1425 trades, profit factor 1.15, t-stat 2.38
- Confirm years: 1084 trades, profit factor 1.16, +122.8R, t-stat 2.26 (needed 3.62); markets 11 of 15; double-cost profit factor 1.10; beats 100% of random entries
- Failed: t-stat >= 3.62 (bar for survivor 336)

### 2026-11-23 · screen survivor 337 · `opening_range_break_hour0.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id cd723a358e). No stated reason.
- Screen years: 1046 trades, profit factor 1.17, t-stat 2.36
- Confirm years: 702 trades, profit factor 0.87, -68.8R, t-stat -1.66 (needed 3.62); markets 4 of 15; double-cost profit factor 0.82; beats 11% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 337)

### 2026-11-23 · screen survivor 338 · `realized_skew_n120.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f6907147b2). No stated reason.
- Screen years: 1197 trades, profit factor 1.17, t-stat 2.74
- Confirm years: 758 trades, profit factor 1.00, +0.7R, t-stat 0.02 (needed 3.62); markets 7 of 15; double-cost profit factor 0.94; beats 73% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 338)

### 2026-11-23 · screen survivor 339 · `realized_skew_n120.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 83e027b870). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1031 trades, profit factor 1.27, t-stat 3.45
- Confirm years: 676 trades, profit factor 0.98, -10.4R, t-stat -0.25 (needed 3.62); markets 8 of 15; double-cost profit factor 0.92; beats 46% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 339)

### 2026-11-23 · screen survivor 340 · `realized_skew_n120.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1fa20b7c56). No stated reason.
- Screen years: 1265 trades, profit factor 1.16, t-stat 2.46
- Confirm years: 806 trades, profit factor 0.93, -45.0R, t-stat -0.98 (needed 3.62); markets 6 of 15; double-cost profit factor 0.85; beats 37% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 340)

### 2026-11-23 · screen survivor 341 · `realized_skew_n120.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id bc480fd372). No stated reason.
- Screen years: 397 trades, profit factor 1.21, t-stat 1.72
- Confirm years: 271 trades, profit factor 1.19, +36.7R, t-stat 1.33 (needed 3.62); markets 9 of 15; double-cost profit factor 1.12; beats 92% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.62 (bar for survivor 341)

### 2026-11-23 · screen survivor 342 · `realized_skew_n120.fade.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a26673b028). No stated reason.
- Screen years: 278 trades, profit factor 1.32, t-stat 2.12
- Confirm years: 219 trades, profit factor 1.09, +14.1R, t-stat 0.58 (needed 3.62); markets 8 of 15; double-cost profit factor 1.02; beats 65% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 342)

### 2026-11-23 · screen survivor 343 · `realized_skew_n120.follow.high_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9426048c70). No stated reason.
- Screen years: 1005 trades, profit factor 1.13, t-stat 1.80
- Confirm years: 658 trades, profit factor 1.04, +20.0R, t-stat 0.49 (needed 3.62); markets 10 of 15; double-cost profit factor 1.00; beats 86% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 343)

### 2026-11-23 · screen survivor 344 · `realized_skew_n120.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 67567e1ed3). No stated reason.
- Screen years: 690 trades, profit factor 1.15, t-stat 1.65
- Confirm years: 425 trades, profit factor 0.90, -34.3R, t-stat -1.04 (needed 3.62); markets 7 of 15; double-cost profit factor 0.82; beats 27% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 344)

### 2026-11-23 · screen survivor 345 · `realized_skew_n120.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id dd1ea04d3d). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 676 trades, profit factor 1.22, t-stat 2.56
- Confirm years: 415 trades, profit factor 0.93, -19.2R, t-stat -0.76 (needed 3.62); markets 6 of 15; double-cost profit factor 0.86; beats 40% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 345)

### 2026-11-23 · screen survivor 346 · `realized_skew_n120.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b4f52b88aa). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 618 trades, profit factor 1.28, t-stat 2.76
- Confirm years: 385 trades, profit factor 0.84, -47.0R, t-stat -1.54 (needed 3.62); markets 4 of 15; double-cost profit factor 0.79; beats 7% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.62 (bar for survivor 346)

### 2026-11-23 · screen survivor 347 · `realized_skew_n120.fade.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 610c13c269). No stated reason.
- Screen years: 383 trades, profit factor 1.22, t-stat 1.76
- Confirm years: 272 trades, profit factor 0.90, -20.8R, t-stat -0.79 (needed 3.63); markets 6 of 15; double-cost profit factor 0.84; beats 32% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 347)

### 2026-11-23 · screen survivor 348 · `realized_skew_n120.fade.with_trend.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id bfac53e603). No stated reason.
- Screen years: 306 trades, profit factor 1.24, t-stat 1.69
- Confirm years: 202 trades, profit factor 0.96, -5.6R, t-stat -0.25 (needed 3.63); markets 6 of 15; double-cost profit factor 0.90; beats 39% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 348)

### 2026-11-23 · screen survivor 349 · `same_hour_seasonality_k8.fade.against_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 96861433a7). No stated reason.
- Screen years: 438 trades, profit factor 1.20, t-stat 1.73
- Confirm years: 298 trades, profit factor 0.93, -14.7R, t-stat -0.54 (needed 3.63); markets 7 of 15; double-cost profit factor 0.88; beats 66% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 349)

### 2026-11-23 · screen survivor 350 · `same_hour_seasonality_k8.fade.high_vol.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9b3f41fbc0). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 445 trades, profit factor 1.21, t-stat 1.94
- Confirm years: 240 trades, profit factor 0.98, -2.8R, t-stat -0.15 (needed 3.63); markets 7 of 15; double-cost profit factor 0.93; beats 74% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 350)

### 2026-11-23 · screen survivor 351 · `same_hour_seasonality_k8.fade.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4e76d56fa2). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 405 trades, profit factor 1.31, t-stat 2.44
- Confirm years: 226 trades, profit factor 1.02, +3.2R, t-stat 0.13 (needed 3.63); markets 6 of 15; double-cost profit factor 0.97; beats 78% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 351)

### 2026-11-23 · screen survivor 352 · `same_hour_seasonality_k8.fade.none.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0b15930f2b). No stated reason.
- Screen years: 775 trades, profit factor 1.14, t-stat 1.77
- Confirm years: 496 trades, profit factor 0.91, -26.9R, t-stat -0.99 (needed 3.63); markets 6 of 15; double-cost profit factor 0.85; beats 54% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 352)

### 2026-11-23 · screen survivor 353 · `same_hour_seasonality_k8.fade.none.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 08fce77643). No stated reason.
- Screen years: 696 trades, profit factor 1.20, t-stat 2.23
- Confirm years: 454 trades, profit factor 0.94, -20.0R, t-stat -0.60 (needed 3.63); markets 6 of 15; double-cost profit factor 0.89; beats 62% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 353)

### 2026-11-23 · screen survivor 354 · `td_setup_count9.fade.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9334485735). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 872 trades, profit factor 1.18, t-stat 2.28
- Confirm years: 629 trades, profit factor 1.05, +24.5R, t-stat 0.60 (needed 3.63); markets 9 of 15; double-cost profit factor 1.00; beats 70% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 354)

### 2026-11-23 · screen survivor 355 · `td_setup_count9.fade.with_trend.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e47f255846). No stated reason.
- Screen years: 944 trades, profit factor 1.14, t-stat 1.83
- Confirm years: 692 trades, profit factor 1.12, +58.9R, t-stat 1.35 (needed 3.63); markets 9 of 15; double-cost profit factor 1.03; beats 96% of random entries
- Failed: profit factor >= 1.15; t-stat >= 3.63 (bar for survivor 355)

### 2026-11-23 · screen survivor 356 · `td_setup_count9.fade.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 403fad965e). No stated reason.
- Screen years: 1610 trades, profit factor 1.10, t-stat 1.79
- Confirm years: 1118 trades, profit factor 1.06, +42.0R, t-stat 0.81 (needed 3.63); markets 8 of 15; double-cost profit factor 0.99; beats 86% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.63 (bar for survivor 356)

### 2026-11-23 · screen survivor 357 · `td_setup_count9.fade.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id dd4d359411). No stated reason.
- Screen years: 1711 trades, profit factor 1.11, t-stat 1.99
- Confirm years: 1216 trades, profit factor 1.08, +65.2R, t-stat 1.15 (needed 3.63); markets 7 of 15; double-cost profit factor 0.98; beats 98% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; t-stat >= 3.63 (bar for survivor 357)

### 2026-11-23 · screen survivor 358 · `turn_of_month_hour13.follow.against_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 93f1232a81). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 470 trades, profit factor 1.21, t-stat 1.93
- Confirm years: 352 trades, profit factor 1.39, +91.6R, t-stat 2.83 (needed 3.63); markets 13 of 15; double-cost profit factor 1.31; beats 99% of random entries
- Failed: t-stat >= 3.63 (bar for survivor 358)

### 2026-11-23 · screen survivor 359 · `turn_of_month_hour0.fade.against_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 02d6d38afd). No stated reason.
- Screen years: 689 trades, profit factor 1.16, t-stat 1.82
- Confirm years: 432 trades, profit factor 1.20, +60.4R, t-stat 1.74 (needed 3.63); markets 10 of 15; double-cost profit factor 1.11; beats 100% of random entries
- Failed: t-stat >= 3.63 (bar for survivor 359)

### 2026-11-23 · screen survivor 360 · `turn_of_month_hour0.follow.against_trend.any.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 21eb4b40b1). No stated reason.
- Screen years: 580 trades, profit factor 1.17, t-stat 1.83
- Confirm years: 417 trades, profit factor 1.11, +26.7R, t-stat 1.04 (needed 3.64); markets 12 of 15; double-cost profit factor 1.01; beats 95% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 360)

### 2026-11-23 · screen survivor 361 · `alpha008_q0.95.fade.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id cd7b155b14). No stated reason.
- Screen years: 1828 trades, profit factor 1.13, t-stat 2.35
- Confirm years: 1208 trades, profit factor 0.89, -95.1R, t-stat -1.75 (needed 3.64); markets 4 of 15; double-cost profit factor 0.85; beats 10% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 361)

### 2026-11-23 · screen survivor 362 · `cl_three_outside_trend6.fade.with_trend.london.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 73028f8da0). No stated reason.
- Screen years: 385 trades, profit factor 1.22, t-stat 1.79
- Confirm years: 269 trades, profit factor 0.98, -5.0R, t-stat -0.19 (needed 3.64); markets 8 of 15; double-cost profit factor 0.89; beats 51% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 362)

### 2026-11-23 · screen survivor 363 · `cl_three_soldiers_trend6.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a6bd50d16e). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 725 trades, profit factor 1.19, t-stat 2.16
- Confirm years: 486 trades, profit factor 1.05, +17.9R, t-stat 0.50 (needed 3.64); markets 7 of 15; double-cost profit factor 1.00; beats 66% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 363)

### 2026-11-23 · screen survivor 364 · `cl_three_soldiers_trend6.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a2f9bc3b69). No stated reason.
- Screen years: 246 trades, profit factor 1.29, t-stat 1.85
- Confirm years: 141 trades, profit factor 1.12, +12.3R, t-stat 0.63 (needed 3.64); markets 7 of 15; double-cost profit factor 1.07; beats 67% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 364)

### 2026-11-23 · screen survivor 365 · `cl_three_soldiers_trend6.fade.with_trend.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b7dd9635f0). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 237 trades, profit factor 1.34, t-stat 2.04
- Confirm years: 170 trades, profit factor 1.08, +10.0R, t-stat 0.47 (needed 3.64); markets 8 of 15; double-cost profit factor 1.02; beats 66% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 365)

### 2026-11-23 · screen survivor 366 · `cl_three_soldiers_trend6.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 982f019728). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 273 trades, profit factor 1.26, t-stat 1.74
- Confirm years: 187 trades, profit factor 0.78, -32.1R, t-stat -1.54 (needed 3.64); markets 5 of 15; double-cost profit factor 0.74; beats 8% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 366)

### 2026-11-23 · screen survivor 367 · `cl_three_soldiers_trend6.follow.with_trend.any.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 27f2b7a1cb). No stated reason.
- Screen years: 762 trades, profit factor 1.13, t-stat 1.66
- Confirm years: 516 trades, profit factor 0.95, -14.5R, t-stat -0.51 (needed 3.64); markets 6 of 15; double-cost profit factor 0.90; beats 37% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 367)

### 2026-11-23 · screen survivor 368 · `cl_three_soldiers_trend6.follow.with_trend.any.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 56e6b32180). No stated reason.
- Screen years: 775 trades, profit factor 1.17, t-stat 1.96
- Confirm years: 538 trades, profit factor 0.91, -37.4R, t-stat -1.01 (needed 3.64); markets 6 of 15; double-cost profit factor 0.84; beats 25% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 368)

### 2026-11-23 · screen survivor 369 · `cl_three_soldiers_trend6.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f996390d48). No stated reason.
- Screen years: 531 trades, profit factor 1.21, t-stat 2.03
- Confirm years: 338 trades, profit factor 1.22, +50.6R, t-stat 1.67 (needed 3.64); markets 9 of 15; double-cost profit factor 1.16; beats 98% of random entries
- Failed: t-stat >= 3.64 (bar for survivor 369)

### 2026-11-23 · screen survivor 370 · `serial_corr_n48.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0cc8e4df70). No stated reason.
- Screen years: 2233 trades, profit factor 1.10, t-stat 2.06
- Confirm years: 1634 trades, profit factor 1.02, +19.8R, t-stat 0.31 (needed 3.64); markets 8 of 15; double-cost profit factor 0.96; beats 63% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 370)

### 2026-11-23 · screen survivor 371 · `alexander_filter_k8.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4caf494ab6). No stated reason.
- Screen years: 529 trades, profit factor 1.20, t-stat 1.94
- Confirm years: 332 trades, profit factor 1.02, +4.6R, t-stat 0.15 (needed 3.64); markets 9 of 15; double-cost profit factor 0.96; beats 69% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 371)

### 2026-11-23 · screen survivor 372 · `alexander_filter_k8.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4517275dff). No stated reason.
- Screen years: 542 trades, profit factor 1.17, t-stat 1.65
- Confirm years: 335 trades, profit factor 1.03, +7.2R, t-stat 0.24 (needed 3.64); markets 9 of 15; double-cost profit factor 0.94; beats 81% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 372)

### 2026-11-23 · screen survivor 373 · `alexander_filter_k4.fade.high_vol.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 9280fe6852). No stated reason.
- Screen years: 691 trades, profit factor 1.14, t-stat 1.73
- Confirm years: 418 trades, profit factor 0.90, -27.7R, t-stat -1.11 (needed 3.64); markets 7 of 15; double-cost profit factor 0.84; beats 40% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.64 (bar for survivor 373)

### 2026-11-23 · screen survivor 374 · `alexander_filter_k8.follow.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 73dd8e26cd). No stated reason.
- Screen years: 541 trades, profit factor 1.16, t-stat 1.74
- Confirm years: 335 trades, profit factor 0.99, -3.0R, t-stat -0.13 (needed 3.65); markets 7 of 15; double-cost profit factor 0.92; beats 66% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 374)

### 2026-11-23 · screen survivor 375 · `alpha052_q0.95.follow.low_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 45c5aa3804). No stated reason.
- Screen years: 1315 trades, profit factor 1.14, t-stat 2.15
- Confirm years: 853 trades, profit factor 0.88, -70.5R, t-stat -1.62 (needed 3.65); markets 5 of 15; double-cost profit factor 0.81; beats 14% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 375)

### 2026-11-23 · screen survivor 376 · `alpha052_q0.95.fade.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 52cb777da0). No stated reason.
- Screen years: 1245 trades, profit factor 1.16, t-stat 2.39
- Confirm years: 943 trades, profit factor 1.20, +120.9R, t-stat 2.49 (needed 3.65); markets 12 of 15; double-cost profit factor 1.12; beats 99% of random entries
- Failed: t-stat >= 3.65 (bar for survivor 376)

### 2026-11-23 · screen survivor 377 · `alpha052_q0.95.fade.low_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d5557c273a). No stated reason.
- Screen years: 1351 trades, profit factor 1.10, t-stat 1.72
- Confirm years: 1045 trades, profit factor 1.16, +91.7R, t-stat 2.31 (needed 3.65); markets 11 of 15; double-cost profit factor 1.07; beats 100% of random entries
- Failed: t-stat >= 3.65 (bar for survivor 377)

### 2026-11-23 · screen survivor 378 · `alpha052_q0.95.fade.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id bfce676ac8). No stated reason.
- Screen years: 1557 trades, profit factor 1.14, t-stat 2.58
- Confirm years: 1230 trades, profit factor 0.98, -17.3R, t-stat -0.40 (needed 3.65); markets 8 of 15; double-cost profit factor 0.92; beats 34% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 378)

### 2026-11-23 · screen survivor 379 · `alpha052_q0.95.fade.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a563e637b6). No stated reason.
- Screen years: 1339 trades, profit factor 1.17, t-stat 2.61
- Confirm years: 1051 trades, profit factor 1.13, +97.3R, t-stat 1.83 (needed 3.65); markets 10 of 15; double-cost profit factor 1.07; beats 86% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 379)

### 2026-11-23 · screen survivor 380 · `alpha052_q0.95.fade.low_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b79a674091). No stated reason.
- Screen years: 1404 trades, profit factor 1.11, t-stat 1.85
- Confirm years: 1076 trades, profit factor 1.15, +114.7R, t-stat 2.13 (needed 3.65); markets 8 of 15; double-cost profit factor 1.04; beats 100% of random entries
- Failed: t-stat >= 3.65 (bar for survivor 380)

### 2026-11-23 · screen survivor 381 · `fair_value_gap_k1.follow.low_vol.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6cf82d42e7). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 377 trades, profit factor 1.22, t-stat 1.78
- Confirm years: 293 trades, profit factor 1.36, +70.8R, t-stat 2.41 (needed 3.65); markets 10 of 15; double-cost profit factor 1.21; beats 100% of random entries
- Failed: t-stat >= 3.65 (bar for survivor 381)

### 2026-11-23 · screen survivor 382 · `fair_value_gap_k1.fade.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d114ca28b8). No stated reason.
- Screen years: 1022 trades, profit factor 1.15, t-stat 2.01
- Confirm years: 606 trades, profit factor 0.95, -23.6R, t-stat -0.59 (needed 3.65); markets 4 of 15; double-cost profit factor 0.89; beats 40% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 382)

### 2026-11-23 · screen survivor 383 · `fair_value_gap_k1.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b54828e3aa). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 745 trades, profit factor 1.17, t-stat 1.99
- Confirm years: 588 trades, profit factor 1.02, +8.5R, t-stat 0.22 (needed 3.65); markets 7 of 15; double-cost profit factor 0.96; beats 72% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 383)

### 2026-11-23 · screen survivor 384 · `fair_value_gap_k1.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b0a3c4c594). No stated reason.
- Screen years: 1504 trades, profit factor 1.15, t-stat 2.40
- Confirm years: 972 trades, profit factor 0.94, -40.6R, t-stat -0.82 (needed 3.65); markets 7 of 15; double-cost profit factor 0.90; beats 34% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 384)

### 2026-11-23 · screen survivor 385 · `fair_value_gap_k1.fade.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d2741bc87e). No stated reason.
- Screen years: 999 trades, profit factor 1.17, t-stat 2.46
- Confirm years: 593 trades, profit factor 0.91, -33.3R, t-stat -1.11 (needed 3.65); markets 5 of 15; double-cost profit factor 0.86; beats 19% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 385)

### 2026-11-23 · screen survivor 386 · `fair_value_gap_k1.follow.against_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f87eecf809). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 246 trades, profit factor 1.36, t-stat 2.23
- Confirm years: 224 trades, profit factor 1.21, +32.8R, t-stat 1.32 (needed 3.65); markets 10 of 15; double-cost profit factor 1.14; beats 96% of random entries
- Failed: t-stat >= 3.65 (bar for survivor 386)

### 2026-11-23 · screen survivor 387 · `fair_value_gap_k1.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8b470053e4). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 369 trades, profit factor 1.41, t-stat 3.01
- Confirm years: 286 trades, profit factor 1.13, +26.2R, t-stat 0.94 (needed 3.65); markets 9 of 15; double-cost profit factor 1.05; beats 89% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 387)

### 2026-11-23 · screen survivor 388 · `lmw_triangle_w3.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 880889d5e0). No stated reason.
- Screen years: 265 trades, profit factor 1.25, t-stat 1.65
- Confirm years: 175 trades, profit factor 1.07, +8.9R, t-stat 0.41 (needed 3.65); markets 6 of 15; double-cost profit factor 0.98; beats 62% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.65 (bar for survivor 388)

### 2026-11-23 · screen survivor 389 · `dow_swing_k6.follow.low_vol.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0663b274f2). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 523 trades, profit factor 1.22, t-stat 2.10
- Confirm years: 365 trades, profit factor 1.22, +56.8R, t-stat 1.77 (needed 3.66); markets 11 of 15; double-cost profit factor 1.14; beats 92% of random entries
- Failed: beats 95% of random entries; t-stat >= 3.66 (bar for survivor 389)

### 2026-11-23 · screen survivor 390 · `dow_swing_k6.fade.with_trend.any.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 1e61a1f95c). No stated reason.
- Screen years: 295 trades, profit factor 1.26, t-stat 1.98
- Confirm years: 199 trades, profit factor 1.00, +0.2R, t-stat 0.01 (needed 3.66); markets 7 of 15; double-cost profit factor 0.92; beats 80% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 390)

### 2026-11-23 · screen survivor 391 · `dow_swing_k3.fade.high_vol.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 64c130f1c0). No stated reason.
- Screen years: 642 trades, profit factor 1.15, t-stat 1.71
- Confirm years: 450 trades, profit factor 1.02, +6.5R, t-stat 0.25 (needed 3.66); markets 8 of 15; double-cost profit factor 0.97; beats 78% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 391)

### 2026-11-23 · screen survivor 392 · `dow_swing_k6.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 92ed3a3b14). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1126 trades, profit factor 1.14, t-stat 1.95
- Confirm years: 752 trades, profit factor 1.05, +28.8R, t-stat 0.65 (needed 3.66); markets 7 of 15; double-cost profit factor 1.00; beats 80% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 392)

### 2026-11-23 · screen survivor 393 · `dow_swing_k6.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 6c5842cc7d). No stated reason.
- Screen years: 222 trades, profit factor 1.26, t-stat 1.68
- Confirm years: 161 trades, profit factor 1.10, +9.2R, t-stat 0.58 (needed 3.66); markets 6 of 15; double-cost profit factor 1.03; beats 80% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 393)

### 2026-11-23 · screen survivor 394 · `dow_swing_k3.fade.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 483fca3a55). No stated reason.
- Screen years: 316 trades, profit factor 1.29, t-stat 2.09
- Confirm years: 228 trades, profit factor 0.81, -33.8R, t-stat -1.46 (needed 3.66); markets 7 of 15; double-cost profit factor 0.75; beats 22% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 394)

### 2026-11-23 · screen survivor 395 · `osler_hs_neckline_k4.fade.with_trend.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e1201b3e82). No stated reason.
- Screen years: 330 trades, profit factor 1.21, t-stat 1.68
- Confirm years: 203 trades, profit factor 0.90, -13.0R, t-stat -0.74 (needed 3.66); markets 7 of 15; double-cost profit factor 0.85; beats 40% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 395)

### 2026-11-23 · screen survivor 396 · `osler_hs_neckline_k4.fade.against_trend.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5e755576b9). No stated reason.
- Screen years: 195 trades, profit factor 1.31, t-stat 1.84
- Confirm years: 123 trades, profit factor 1.13, +9.0R, t-stat 0.65 (needed 3.66); markets 9 of 15; double-cost profit factor 1.05; beats 89% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 396)

### 2026-11-23 · screen survivor 397 · `osler_hs_neckline_k4.fade.with_trend.ny.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 7da3dfd77f). No stated reason.
- Screen years: 334 trades, profit factor 1.25, t-stat 1.98
- Confirm years: 207 trades, profit factor 0.84, -21.4R, t-stat -1.21 (needed 3.66); markets 6 of 15; double-cost profit factor 0.77; beats 35% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 397)

### 2026-11-23 · screen survivor 398 · `three_line_break_lines3.follow.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5a7536540a). No stated reason.
- Screen years: 2220 trades, profit factor 1.10, t-stat 1.99
- Confirm years: 1466 trades, profit factor 0.96, -37.8R, t-stat -0.69 (needed 3.66); markets 6 of 15; double-cost profit factor 0.91; beats 49% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 398)

### 2026-11-23 · screen survivor 399 · `supertrend_flip_mult3_period10.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 27c315b27f). No stated reason.
- Screen years: 1498 trades, profit factor 1.11, t-stat 1.77
- Confirm years: 988 trades, profit factor 0.96, -28.4R, t-stat -0.57 (needed 3.66); markets 7 of 15; double-cost profit factor 0.91; beats 37% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 399)

### 2026-11-23 · screen survivor 400 · `supercycle_surge_chop_max38.2_chop_n14_cycle10_fast23_slow50_ss10.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id fb1e5f80f9). No stated reason.
- Screen years: 2031 trades, profit factor 1.11, t-stat 2.11
- Confirm years: 1386 trades, profit factor 1.05, +49.2R, t-stat 0.80 (needed 3.66); markets 9 of 15; double-cost profit factor 0.97; beats 95% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; t-stat >= 3.66 (bar for survivor 400)

### 2026-11-23 · screen survivor 401 · `supercycle_surge_chop_max38.2_chop_n14_cycle10_fast23_slow50_ss10.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 26c097ea7f). No stated reason.
- Screen years: 1660 trades, profit factor 1.10, t-stat 1.82
- Confirm years: 1057 trades, profit factor 1.09, +66.2R, t-stat 1.25 (needed 3.66); markets 11 of 15; double-cost profit factor 1.03; beats 86% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 401)

### 2026-11-23 · screen survivor 402 · `supercycle_surge_chop_max38.2_chop_n14_cycle10_fast23_slow50_ss10.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4d09a55002). No stated reason.
- Screen years: 1230 trades, profit factor 1.15, t-stat 2.22
- Confirm years: 921 trades, profit factor 1.11, +69.5R, t-stat 1.42 (needed 3.66); markets 9 of 15; double-cost profit factor 1.04; beats 94% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 402)

### 2026-11-23 · screen survivor 403 · `supercycle_surge_chop_max38.2_chop_n14_cycle10_fast23_slow50_ss10.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 5c1b86e9fa). No stated reason.
- Screen years: 1751 trades, profit factor 1.12, t-stat 2.10
- Confirm years: 1211 trades, profit factor 0.99, -11.5R, t-stat -0.21 (needed 3.66); markets 7 of 15; double-cost profit factor 0.93; beats 46% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 403)

### 2026-11-23 · screen survivor 404 · `trendilo_turn_mult1_n50_offset0.85_sigma6_smooth1.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ae9a69e46e). No stated reason.
- Screen years: 1992 trades, profit factor 1.11, t-stat 2.08
- Confirm years: 1395 trades, profit factor 1.01, +5.9R, t-stat 0.10 (needed 3.66); markets 8 of 15; double-cost profit factor 0.95; beats 58% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.66 (bar for survivor 404)

### 2026-11-23 · screen survivor 405 · `trendilo_turn_mult1_n50_offset0.85_sigma6_smooth1.fade.high_vol.london.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 23d0557718). No stated reason.
- Screen years: 1278 trades, profit factor 1.12, t-stat 1.96
- Confirm years: 783 trades, profit factor 0.84, -82.0R, t-stat -2.42 (needed 3.67); markets 3 of 15; double-cost profit factor 0.78; beats 7% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 405)

### 2026-11-23 · screen survivor 406 · `trendilo_turn_mult1_n50_offset0.85_sigma6_smooth1.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id ebc0c1d2bb). No stated reason.
- Screen years: 1876 trades, profit factor 1.12, t-stat 2.24
- Confirm years: 1285 trades, profit factor 1.07, +57.6R, t-stat 1.04 (needed 3.67); markets 9 of 15; double-cost profit factor 0.99; beats 87% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 406)

### 2026-11-23 · screen survivor 407 · `trendilo_turn_mult1_n50_offset0.85_sigma6_smooth1.follow.low_vol.ny.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 539c090a48). No stated reason.
- Screen years: 2005 trades, profit factor 1.10, t-stat 2.13
- Confirm years: 1373 trades, profit factor 1.04, +34.5R, t-stat 0.77 (needed 3.67); markets 9 of 15; double-cost profit factor 0.96; beats 93% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 407)

### 2026-11-23 · screen survivor 408 · `trendilo_turn_mult1_n50_offset0.85_sigma6_smooth1.fade.high_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 54a4fe8095). No stated reason.
- Screen years: 1240 trades, profit factor 1.18, t-stat 2.68
- Confirm years: 765 trades, profit factor 0.84, -88.6R, t-stat -2.15 (needed 3.67); markets 5 of 15; double-cost profit factor 0.80; beats 6% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 408)

### 2026-11-23 · screen survivor 409 · `gtja160_down_vol_n20.follow.with_trend.any.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a60ab5b982). No stated reason.
- Screen years: 1682 trades, profit factor 1.12, t-stat 2.05
- Confirm years: 1159 trades, profit factor 1.07, +55.9R, t-stat 1.01 (needed 3.67); markets 10 of 15; double-cost profit factor 1.00; beats 74% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 409)

### 2026-11-23 · screen survivor 410 · `gtja160_down_vol_n20.fade.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id a1afe30316). No stated reason.
- Screen years: 538 trades, profit factor 1.18, t-stat 1.75
- Confirm years: 344 trades, profit factor 0.94, -14.8R, t-stat -0.50 (needed 3.67); markets 9 of 15; double-cost profit factor 0.88; beats 29% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 410)

### 2026-11-23 · screen survivor 411 · `obv_divergence_n72.fade.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 606ef45a7f). No stated reason.
- Screen years: 1739 trades, profit factor 1.13, t-stat 2.36
- Confirm years: 1291 trades, profit factor 0.99, -10.5R, t-stat -0.18 (needed 3.67); markets 5 of 15; double-cost profit factor 0.94; beats 39% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 411)

### 2026-11-23 · screen survivor 412 · `gtja003_pressure_sum_n6.follow.low_vol.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 21fe7d06e8). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 321 trades, profit factor 1.39, t-stat 2.69
- Confirm years: 294 trades, profit factor 1.11, +22.3R, t-stat 0.79 (needed 3.67); markets 10 of 15; double-cost profit factor 1.03; beats 87% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 412)

### 2026-11-23 · screen survivor 413 · `gtja003_pressure_sum_n6.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 0012c62c25). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 693 trades, profit factor 1.19, t-stat 2.11
- Confirm years: 596 trades, profit factor 1.02, +9.7R, t-stat 0.25 (needed 3.67); markets 7 of 15; double-cost profit factor 0.97; beats 68% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 413)

### 2026-11-23 · screen survivor 414 · `gtja003_pressure_sum_n20.follow.low_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c919ace888). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 637 trades, profit factor 1.23, t-stat 2.36
- Confirm years: 477 trades, profit factor 1.06, +18.8R, t-stat 0.54 (needed 3.67); markets 8 of 15; double-cost profit factor 0.99; beats 74% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 414)

### 2026-11-23 · screen survivor 415 · `gtja003_pressure_sum_n20.follow.low_vol.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id d2f13c3aed). No stated reason.
- Screen years: 682 trades, profit factor 1.20, t-stat 2.21
- Confirm years: 498 trades, profit factor 1.09, +32.9R, t-stat 0.89 (needed 3.67); markets 8 of 15; double-cost profit factor 0.99; beats 94% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 415)

### 2026-11-23 · screen survivor 416 · `gtja009_ease_of_movement_n15.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 735e2d0389). No stated reason.
- Screen years: 794 trades, profit factor 1.14, t-stat 1.87
- Confirm years: 612 trades, profit factor 0.99, -4.0R, t-stat -0.13 (needed 3.67); markets 9 of 15; double-cost profit factor 0.93; beats 65% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 416)

### 2026-11-23 · screen survivor 417 · `gtja009_ease_of_movement_n15.follow.with_trend.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 4ade681196). No stated reason.
- This idea's confirm years were already read once under version 3 costs, so this is not a first look.
- Screen years: 1215 trades, profit factor 1.19, t-stat 2.78
- Confirm years: 719 trades, profit factor 1.06, +32.9R, t-stat 0.76 (needed 3.67); markets 9 of 15; double-cost profit factor 1.01; beats 80% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 417)

### 2026-11-23 · screen survivor 418 · `gtja009_ease_of_movement_n15.follow.with_trend.ny.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f240100598). No stated reason.
- Screen years: 1396 trades, profit factor 1.14, t-stat 2.24
- Confirm years: 809 trades, profit factor 1.06, +33.4R, t-stat 0.71 (needed 3.67); markets 9 of 15; double-cost profit factor 0.97; beats 93% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 418)

### 2026-11-23 · screen survivor 419 · `gtja118_open_reach_n20.follow.with_trend.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id b081b328e1). No stated reason.
- Screen years: 973 trades, profit factor 1.12, t-stat 1.74
- Confirm years: 690 trades, profit factor 0.97, -12.8R, t-stat -0.39 (needed 3.67); markets 4 of 15; double-cost profit factor 0.90; beats 52% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 419)

### 2026-11-23 · screen survivor 420 · `gtja118_open_reach_n20.follow.with_trend.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id f8550b806e). No stated reason.
- Screen years: 923 trades, profit factor 1.17, t-stat 2.16
- Confirm years: 656 trades, profit factor 1.02, +9.1R, t-stat 0.22 (needed 3.67); markets 7 of 15; double-cost profit factor 0.96; beats 56% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.67 (bar for survivor 420)

### 2026-11-23 · screen survivor 421 · `gtja118_open_reach_n20.follow.low_vol.london.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id c9e430d9cc). No stated reason.
- Screen years: 1141 trades, profit factor 1.13, t-stat 1.88
- Confirm years: 723 trades, profit factor 1.33, +156.7R, t-stat 3.50 (needed 3.68); markets 12 of 15; double-cost profit factor 1.23; beats 100% of random entries
- Failed: t-stat >= 3.68 (bar for survivor 421)

### 2026-11-23 · screen survivor 422 · `lunar_phase_synodic29.5306.fade.high_vol.any.stop2_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id aabfee74d4). No stated reason.
- Screen years: 461 trades, profit factor 1.20, t-stat 1.93
- Confirm years: 371 trades, profit factor 1.42, +82.1R, t-stat 3.36 (needed 3.68); markets 12 of 15; double-cost profit factor 1.31; beats 100% of random entries
- Failed: t-stat >= 3.68 (bar for survivor 422)

### 2026-11-23 · screen batch · 17200 ideas
- Passed the screen: 267. Confirmed on unseen years: 0. Candidates: 0.
- Totals under version 4: 17200 of 17200 catalogue ideas screened, 267 survivors (422 with the 155 from earlier versions, which set the bar), 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-23 · forward watch · 24 ideas registered
- `turn_of_month_hour0.fade.against_trend.any.stop2_rr2.5`
- `a158_rsqr_n20.follow.with_trend.asia.stop3_rr2.5`
- `a158_rsqr_n20.follow.high_vol.asia.stop3_rr1.5`
- `a158_rsqr_n20.follow.none.asia.stop3_rr2.5`
- `a158_rsqr_n20.follow.none.asia.stop3_rr1.5`
- `a158_resi_n60.follow.low_vol.ny.stop3_rr2.5`
- `alpha052_q0.95.fade.low_vol.asia.stop3_rr2.5`
- `alpha046_q0.95.fade.low_vol.ny.stop3_rr2.5`
- `a158_rsqr_n20.follow.with_trend.asia.stop2_rr2.5`
- `a158_rsqr_n20.follow.with_trend.asia.stop3_rr1.5`
- `a158_rsqr_n20.follow.high_vol.asia.stop2_rr2.5`
- `a158_rsqr_n20.follow.low_vol.asia.stop3_rr1.5`
- `open_distance_frac1.follow.with_trend.asia.stop2_rr1.5`
- `a158_resi_n60.follow.low_vol.any.stop3_rr2.5`
- `lunar_phase_synodic29.5306.fade.high_vol.any.stop2_rr1.5`
- `streak_k5.follow.low_vol.asia.stop3_rr2.5`
- `alpha052_q0.95.fade.low_vol.asia.stop2_rr2.5`
- `cmf_extreme_n20.follow.with_trend.ny.stop3_rr2.5`
- `gtja118_open_reach_n20.follow.low_vol.london.stop3_rr2.5`
- `a158_corr_n60.follow.low_vol.ny.stop3_rr2.5`
- `alpha052_q0.95.fade.low_vol.asia.stop3_rr1.5`
- `a158_rsqr_n20.follow.low_vol.any.stop3_rr2.5`
- `a158_rsqr_n20.follow.low_vol.london.stop3_rr2.5`
- `cl_three_soldiers_trend6.follow.none.asia.stop3_rr2.5`
- Forward trades count from 2026-11-24 00:00 UTC. Verdict at 200 trades. Rules: "Forward watch" in `LAB_RULES.md`.

### 2026-11-23 · rules version 4 · audit fixes and full re-run · 0 confirmed, 0 candidates
- Why: the audit of November 23, 2026 (outside-library cross-check, planted edges, independent code review). Rules: "Rules version 4" in `LAB_RULES.md`, pushed in commit 3e3e652 before anything ran under them.
- Changed: one cost table (`costs.py`), every market from April 21, 2021, every screened idea on fifteen markets, the position-mode time-shift check, the look-ahead checks, and four smaller holes. The bar did not change.
- Main track, eight ideas re-run once, all REJECT. Three test years each (2023, 2024, 2025).
  - `donchian_breakout`: 1,908 trades, profit factor 1.06, t-stat 1.08 against 3.30. Under version 3 it lost; at real costs it is about flat.
  - `ts_momentum`: Sharpe 1.17, +30.6%, profitable in 3 of 3 years, t-stat 2.03 against 3.30, and it beat only 10% of its own late copies. Holding the same positions 20 or more days late did as well.
  - `valeyre_ema_trend`: Sharpe 0.89, +9.0%, t-stat 1.54, beat 0% of its late copies.
  - `channel_bounce`, `ibs_reversion`, `pivot_support_resistance`, `rsi2_reversion`, `xs_contrarian`: all lost money. Profit factors 0.86 to 0.90 for the four signal ideas.
- Screen track: 17,200 ideas screened on fifteen markets. 267 passed the screen (155 under version 3; 91 passed under both). 0 confirmed.
  - Median profit factor in the screen years: 0.92 (0.86 under version 3). 16.8% of ideas were above 1.0 (6.9% before).
  - Confirm years: median t-stat 0.06, median profit factor 1.01. The typical survivor had nothing left.
  - Best: `gtja118_open_reach_n20.follow.low_vol.london.stop3_rr2.5`, 723 trades, profit factor 1.33, t-stat 3.50 against a bar of 3.68.
  - Second best: `lunar_phase_synodic29.5306.fade.high_vol.any.stop2_rr1.5`, 371 trades, profit factor 1.42, t-stat 3.36. A moon-phase rule this close to the bar shows what luck can do among 267 tries.
  - 21 survivors had a confirm t-stat of 2 or more and 3 had 3 or more. Luck alone would give about 6 and fewer than 1 if the ideas were independent. They are not: several share one trigger. A hint, not a result.
  - 29 survivors passed every confirm check except the bar. 24 were new to the forward watch, which now holds 44 ideas.
  - 91 of the 267 had their confirm years read before under version 3 costs. None of them confirmed either.
- No idea reached the quarantine block in either track. It is still unread.
- Tests of the changed code on made-up prices, before the run: no-edge runs passed 0 times at confirm; a planted edge of profit factor 1.37 on about 700 confirm trades was caught 88% of the time (38% under version 3 costs for the same planted move); peeking test files were caught on every market; the position-mode check passed 3% to 15% of no-edge runs for trend and contrarian alike.
- Not fixed: two confirm years cannot show a small edge. The cost table's spread part is an estimate, not FTMO's own figures.


### 2026-11-23 · study 9 · pull to the midnight open · NOT SUPPORTED
- Source: a post by @RHerman on X (x.com/rherman/status/2124971266839076991): on the Nasdaq, when the 9:30 open is below the midnight open and above the previous close, price got back to the midnight open in 82.5% of almost 300 sessions, 2015 to 2025.
- Lab data: 1-minute bars, 2021-04-22 to 2026-11-19. Costs from `costs.py`. No screen and confirm split: there are too few days.
- NAS100, the post's setup: 151 days of 1349. Midnight open touched on 85.4%. Reached before the phantom level the same distance below on 63 days, after it on 55, both in one minute on 31, neither on 2 (53.4% of decided days, p 0.260). Median distance 0.138% of price. Trade: 112 trades, average -0.047R after costs (+0.038R before), win rate 53%, profit factor 0.91, t-stat -0.49.
- SPX500, the post's setup: 135 days of 1348. Midnight open touched on 79.3%. Reached before the phantom level the same distance below on 53 days, after it on 60, both in one minute on 20, neither on 2 (46.9% of decided days, p 0.774). Median distance 0.094% of price. Trade: 101 trades, average -0.233R after costs (-0.117R before), win rate 44%, profit factor 0.63, t-stat -2.30.
- USA30, the post's setup: 119 days of 1348. Midnight open touched on 83.2%. Reached before the phantom level the same distance below on 44 days, after it on 55, both in one minute on 19, neither on 1 (44.4% of decided days, p 0.886). Median distance 0.076% of price. Trade: 84 trades, average -0.237R after costs (-0.108R before), win rate 44%, profit factor 0.62, t-stat -2.13.
- Nasdaq, `below_no_gap`: 488 days, touched 63.5%, level first on 50.4% of decided days (p 0.461).
- Nasdaq, `mirror_setup`: 128 days, touched 70.3%, level first on 44.6% of decided days (p 0.890).
- Nasdaq, `above_no_gap`: 582 days, touched 63.9%, level first on 48.2% of decided days (p 0.805).
- Checks failed: level reached before the phantom level on more than half of decided days (p <= 0.05); trade average above zero after costs with t-stat >= 1.65; trade average above zero at double cost.
- Notes on study 9, written after it ran:
  - The post's count holds up. The setup came up on 151 of 1,349 Nasdaq days (11%, the same share as the post's 300 sessions in eleven years) and the midnight open was touched on 85.4% of them, against the post's 82.5%.
  - The touch rate is explained by distance. On setup days the midnight open sits a median 0.138% of price from the open, about a third of the 0.42% on other days that open below it. Those other days were touched 63.5% of the time. In the nearest third of setup days (within 0.067%) the level was touched on 98%.
  - There is no sign of a pull. The midnight open was reached before the phantom level on 63 days and after it on 55 (53.4%, p 0.26). On 31 days both were reached in the same minute, because the level was that close.
  - The trade lost: 112 trades, +0.038R before costs and -0.047R after, profit factor 0.91. Costs average 0.085R a trade at this distance.
  - S&P 500 and Dow, reported only: level first on 46.9% and 44.4% of decided days, and the trade lost 0.23R and 0.24R.
  - Seen in the reported groups, not tested: on mirror-setup days (gap down, open above the midnight open) price reached the midnight open first less than half the time on all three indices (44.6%, 36.1%, 34.7%). That is one look at three markets that move together, in years when indices mostly rose, found after the fact. It is not a result and is not to be tested on these files. If it is ever tested, it needs new data and its own rules.
  - With 118 decided days the study could not have told 50% from 55%. It rules out a pull as strong as the post's wording suggests, not a small one.


### 2026-11-23 · study 10 · thirteen claims from @RHerman · 0 of 13 pass as a trade
- Source: posts on X by @RHerman, found in a scan of the account (about 1,400 posts back to August 2025). The posts give rates for a level being reached. They give no entry, stop or cost, and most say so.
- Lab data: 2021-05-03 to 2026-11-19. Hourly bars for the whole day, 1-minute bars from 8:00 or 9:00 New York time. Costs from `costs.py`. Test for each level claim: is the level reached before a phantom level the same distance on the other side, and does trading the claim's side pay after costs. Bar for a trade: at least 50 trades, average above zero, t-stat 2.67 or more, still above zero at double cost.
- `c01_sweep_reclaim_0800` (NAS100): 8:00 candle sweeps the 7:00 low and closes back above it; the 9:00 candle takes the 8:00 high. 183 events. Level reached on 84.2% (post: 85.9%). The claim's side came first on 53.4% of 174 decided events (p 0.202); on other days 48.0%. Trade: 138 trades, average -0.059 R after costs (+0.058 before), win rate 53%, profit factor 0.89, t-stat -0.67. No pass.
- `c02_hour_sweep_reclaim` (NAS100): 1H candle sweeps the prior low (high) and closes back inside; the next hour takes its high (low). 2660 events. Level reached on 60.0% (post: 60.4%). The claim's side came first on 50.2% of 2150 decided events (p 0.440); on other days 47.4%. Trade: 2238 trades, average -0.093 R after costs (+0.004 before), win rate 50%, profit factor 0.82, t-stat -4.61. No pass.
- `c03_hour_sweep_continue` (NAS100): 1H candle sweeps the prior low (high) and closes beyond it; the next hour takes that low (high) again. 3535 events. Level reached on 73.8% (post: 67.5%). The claim's side came first on 50.6% of 3011 decided events (p 0.256); on other days 49.4%. Trade: 2543 trades, average -0.098 R after costs (+0.022 before), win rate 51%, profit factor 0.82, t-stat -4.97. No pass.
- `c04_wide_breakout_holds` (NAS100): wide 1H candle breaks the prior high (low) and closes beyond; the next hour leaves its low (high) alone. 1261 events. Level reached on 10.6% (post: 13.2%). The claim's side came first on 56.2% of 290 decided events (p 0.020); on other days 51.6%. Trade: 1261 trades, average +0.019 R after costs (+0.039 before), win rate 52%, profit factor 1.08, t-stat 1.14. No pass.
- `c05_friday_last_hour` (NAS100): Friday: the 16:00 hour leaves the 15:00 high alone. 252 events. Level reached on 13.1% (post: 15.1%). The claim's side came first on 62.5% of 64 decided events (p 0.030); on other days 48.3%. Trade: 237 trades, average -0.029 R after costs (+0.047 before), win rate 46%, profit factor 0.88, t-stat -0.70. No pass.
- `c06_red_morning` (NAS100): red 9:30-11:59 morning; the 13:30-15:59 afternoon leaves the morning high alone. 632 events. Level reached on 18.4% (post: 14.5%). The claim's side came first on 55.6% of 207 decided events (p 0.063); on other days 51.6%. Trade: 623 trades, average +0.001 R after costs (+0.026 before), win rate 49%, profit factor 1.00, t-stat 0.05. No pass.
- `c07_asia_low_taken_below_opens` (NAS100): London took the Asia low, 9:30 open below the midnight and 18:00 opens; the Asia high survives. 428 events. Level reached on 46.0% (post: 25.6%). The claim's side came first on 48.8% of 322 decided events (p 0.692); on other days 49.3%. Trade: 428 trades, average -0.046 R after costs (-0.025 before), win rate 47%, profit factor 0.90, t-stat -1.07. No pass.
- `c08_dow_expansion_below_pdl` (USA30): London expanded past an Asia side, 9:30 open below yesterday's low; the overnight high survives. 120 events. Level reached on 20.0% (post: 16.7%). The claim's side came first on 57.9% of 57 decided events (p 0.145); on other days 48.0%. Trade: 120 trades, average +0.037 R after costs (+0.053 before), win rate 52%, profit factor 1.12, t-stat 0.54. No pass.
- `c09_quiet_london_above_pdh` (NAS100): narrow London, 9:30 open above yesterday's high; yesterday's New York low survives. 86 events. Level reached on 4.7% (post: 3.2%). The claim's side came first on 66.7% of 9 decided events (p 0.254); on other days 46.7%. Trade: 86 trades, average +0.117 R after costs (+0.125 before), win rate 58%, profit factor 1.80, t-stat 2.16. No pass.
- `c10_prior_low_only_bearish_london` (NAS100): yesterday took only the prior day's low, London red; the overnight low is taken after 8:00. 186 events. Level reached on 82.8% (post: 88.8%). The claim's side came first on 51.6% of 155 decided events (p 0.374); on other days 52.3%. Trade: 151 trades, average -0.022 R after costs (+0.039 before), win rate 52%, profit factor 0.96, t-stat -0.26. No pass.
- `c11_wide_day_untouched` (NAS100): wide day yesterday, neither of its ends taken by 8:00; the overnight high is taken after 8:00. 169 events. Level reached on 78.7% (post: 86.6%). The claim's side came first on 56.8% of 148 decided events (p 0.059); on other days 48.4%. Trade: 146 trades, average +0.104 R after costs (+0.159 before), win rate 58%, profit factor 1.24, t-stat 1.27. No pass.
- `c12_gold_below_two_opens` (XAUUSD): gold at 8:00 below yesterday's open and the midnight open; the overnight high survives. 165 events. Level reached on 12.7% (post: 13.2%). The claim's side came first on 58.0% of 50 decided events (p 0.161); on other days 52.7%. Trade: 165 trades, average +0.142 R after costs (+0.155 before), win rate 58%, profit factor 1.64, t-stat 2.27. No pass.
- `c13_weekday_direction` (NAS100): 9:30 to the close: long Monday, Tuesday, Friday; short Wednesday, Thursday. 1381 events. Trade: 1381 trades, average +0.031 percent of price after costs (+0.041 before), win rate 53%, profit factor 1.08, t-stat 0.97. No pass.
- Read: the posts' rates mostly hold up on the lab's prices. That shows the counting is honest, not that there is a trade. Against a level the same distance the other way, no claim's side came first often enough to clear p 0.0038, and no trade cleared t 2.67.
- Nearest: `c12_gold_below_two_opens` (t 2.27) and `c09_quiet_london_above_pdh` (t 2.16). Thirteen tests were run, so one or two results near t 2 are expected with no edge at all. Neither goes on the forward watch.
- The two hourly sweep rules were flat before costs and lost about 0.1R a trade after. On a one-hour window the level is close and costs are a tenth of the risk.

### 2026-11-24 · screen survivor 423 · `td_camouflage_back1.follow.none.asia.stop2_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 00a5a353cc). No stated reason.
- Screen years: 209 trades, profit factor 1.35, t-stat 1.96
- Confirm years: 168 trades, profit factor 0.76, -32.7R, t-stat -1.66 (needed 3.68); markets 5 of 13; double-cost profit factor 0.71; beats 10% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.68 (bar for survivor 423)

### 2026-11-24 · screen survivor 424 · `td_camouflage_back1.follow.none.asia.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 8c70e3b722). No stated reason.
- Screen years: 207 trades, profit factor 1.48, t-stat 2.55
- Confirm years: 168 trades, profit factor 0.84, -20.0R, t-stat -1.01 (needed 3.68); markets 7 of 13; double-cost profit factor 0.81; beats 20% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.68 (bar for survivor 424)

### 2026-11-24 · screen survivor 425 · `td_countdown_count13_setup9.follow.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 36775c8a6e). No stated reason.
- Screen years: 476 trades, profit factor 1.21, t-stat 1.90
- Confirm years: 315 trades, profit factor 0.88, -29.3R, t-stat -1.04 (needed 3.68); markets 8 of 15; double-cost profit factor 0.84; beats 29% of random entries
- Failed: profit factor >= 1.15; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.68 (bar for survivor 425)

### 2026-11-24 · screen survivor 426 · `td_countdown_count13_setup9.fade.high_vol.asia.stop3_rr1.5` · REJECT
- Source: machine-built from parts (screen catalogue, id e9d25e5d9e). No stated reason.
- Screen years: 347 trades, profit factor 1.20, t-stat 1.67
- Confirm years: 242 trades, profit factor 1.08, +11.5R, t-stat 0.59 (needed 3.68); markets 8 of 15; double-cost profit factor 1.02; beats 82% of random entries
- Failed: profit factor >= 1.15; beats 95% of random entries; t-stat >= 3.68 (bar for survivor 426)

### 2026-11-24 · screen survivor 427 · `td_line_break_k3.follow.high_vol.ny.stop3_rr2.5` · REJECT
- Source: machine-built from parts (screen catalogue, id 3ba5066200). No stated reason.
- Screen years: 1799 trades, profit factor 1.11, t-stat 1.93
- Confirm years: 1293 trades, profit factor 0.95, -38.5R, t-stat -0.74 (needed 3.68); markets 6 of 15; double-cost profit factor 0.90; beats 50% of random entries
- Failed: profit factor >= 1.15; profitable in half the markets that traded; profit factor > 1 at double costs; beats 95% of random entries; t-stat >= 3.68 (bar for survivor 427)

### 2026-11-24 · screen batch · 1400 ideas
- New triggers registered: acceleration, friday_monday_sign, td_camouflage, td_clop, td_clopwin, td_countdown, td_line_break, turnaround_tuesday.
- Passed the screen: 5. Confirmed on unseen years: 0. Candidates: 0.
- Totals under version 4: 18600 of 18600 catalogue ideas screened, 272 survivors (427 with the 155 from earlier versions, which set the bar), 0 confirmed, 0 candidates.
- Every screened idea is in `lab/screen/log.csv`.

### 2026-11-24 · study 11 · the 1-hour and 15-minute "CC" setups · 8 scenarios · 0 passed the screen, 0 confirmed
- Source: a post by @tradermike1234 on X (x.com/tradermike1234/status/2125172071374237862). Nasdaq 100, S&P 500 and Dow, 1-minute bars, 9:00 to 15:55 New York time.
- Screen: 2021-06-01 to 2023-12-31. Confirm: 2024-01-01 to 2026-11-19, t-stat bar 2.33. Every trade risks the distance to its target (1 to 1). Results in R after the costs in `costs.py`. A win rate of 50% before costs is what no edge looks like.
- `h1.early.plain` · REJECT: screen 234 days, 334 trades, win rate 47.6% before costs, average -0.182R (-0.077R before costs, cost 0.102R), profit factor 0.65, t-stat -3.01. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
- `h1.early.minstop` · REJECT: screen 213 days, 295 trades, win rate 46.1% before costs, average -0.154R (-0.075R before costs, cost 0.078R), profit factor 0.70, t-stat -2.45. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
- `h1.any.plain` · REJECT: screen 300 days, 453 trades, win rate 47.5% before costs, average -0.169R (-0.076R before costs, cost 0.091R), profit factor 0.66, t-stat -3.24. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
- `h1.any.minstop` · REJECT: screen 281 days, 410 trades, win rate 46.8% before costs, average -0.132R (-0.060R before costs, cost 0.071R), profit factor 0.73, t-stat -2.45. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
- `m15.two.early` · REJECT: screen 330 days, 566 trades, win rate 54.4% before costs, average -0.137R (+0.013R before costs, cost 0.140R), profit factor 0.73, t-stat -2.62. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
- `m15.two.any` · REJECT: screen 587 days, 1731 trades, win rate 51.1% before costs, average -0.148R (-0.028R before costs, cost 0.115R), profit factor 0.63, t-stat -4.76. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
- `m15.twothree.early` · REJECT: screen 346 days, 602 trades, win rate 54.0% before costs, average -0.136R (+0.013R before costs, cost 0.139R), profit factor 0.74, t-stat -2.67. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
- `m15.twothree.any` · REJECT: screen 599 days, 1929 trades, win rate 51.3% before costs, average -0.137R (-0.018R before costs, cost 0.114R), profit factor 0.64, t-stat -4.62. Failed: average above zero with t-stat >= 1.65; profit factor >= 1.1; positive on two of three markets; average above zero at double cost
