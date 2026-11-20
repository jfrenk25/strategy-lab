# "151 Trading Strategies": what the lab can and cannot test

Source: Z. Kakushadze and J. A. Serur, 2018, https://ssrn.com/abstract=3247865 (free). The book gives formulas and no backtests.
This file is a triage in our own words. The book itself is not stored in this repo.

## By chapter

| Ch. | Topic | Strategies | Testable here? |
|---|---|---|---|
| 2 | Options | 2.2 to 2.57 | No. Needs options prices. |
| 3 | Stocks | 3.1 to 3.20 | A few. See below. Most need a stock universe and fundamentals. |
| 4 | ETFs | 4.1 to 4.6 | 4.4 as a single-market adaptation. Rotation needs a portfolio engine. |
| 5 | Fixed income | 5.2 to 5.15 | No. Needs bond and swap data. |
| 6 | Indexes | 6.2 to 6.5 | No, except 6.5 (volatility targeting), which is sizing, not a signal. |
| 7 | Volatility | 7.2 to 7.6 | No. Needs VIX futures and options. |
| 8 | FX | 8.1 to 8.5 | 8.1 can run in position mode. Carry needs interest-rate data. |
| 9 | Commodities | 9.1 to 9.6 | No. Needs futures curves and positioning data. |
| 10 | Futures | 10.1 to 10.4 | 10.3 and 10.4 tested in position mode 2026-11-19: both rejected. |
| 11 to 17 | Structured, convertibles, tax, distressed, real estate, cash | all | No. Not tradable from price bars. |
| 18 | Crypto | 18.2, 18.3 | 18.2 is a 15-minute model (costs). 18.3 needs tweet data. |
| 19, 20 | Global macro, infrastructure | all | No. Needs macro data. |

## Chapter 3 detail

| Section | Idea | Status |
|---|---|---|
| 3.1, 3.2, 3.3, 3.4, 3.6, 3.7 | Cross-sectional stock factors | Needs a stock universe |
| 3.8, 3.9, 3.10 | Pairs and cluster mean reversion | Position mode |
| 3.11, 3.12, 3.13 | One, two and three moving averages | Dead class (indicator crossovers) |
| 3.14 | Pivot-point support and resistance | Carded 2026-11-19 |
| 3.15 | Channel: bounce off floor and ceiling | Carded 2026-11-19 (the breakout version is already rejected) |
| 3.17 | k-nearest-neighbour forecast | Position mode |
| 3.18 | Stat arb by optimisation | Position mode |
| 3.19 | Market making | Needs order-book data |
| 3.20 | Alpha combination | Position mode and many signals |

## What this means
- Roughly 10 of the 151 can be tested with price bars at all.
- Three fit the lab as it is: 3.14, 3.15 and 4.4.
- The rest of the testable ones (3.8 to 3.10, 3.17, 3.18, 3.20, 8.1, 10.3, 10.4) hold positions day by day or across a basket. They run in position mode. 10.3 and 10.4 are done.
