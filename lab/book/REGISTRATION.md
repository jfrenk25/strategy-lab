# Book forward watch: three legs in one account

Registered November 25, 2026, before any price bar after that day existed. Nothing in this file changes after registration. A different book, size or rule is a new registration with a new start date.

## What is watched
One paper account of $100,000 running three rules at fixed sizes. This is the PASSED3 book at the 6% size from Study 20 (`claude/book2-result-2026-11-25.md` in the Trading Lab project).

| Leg | Market | Rule | Size, fixed in % of the starting balance |
|---|---|---|---|
| Cutler RSI dip-buy | NAS100 | Study 12, rule D, no stop | a position worth 0.3754 times the balance |
| Copy v3 | Gold | 4-hour swing breakout, three positions a signal, no entries in the news minutes | 0.2514% risked per position (0.754% per signal) |
| RTH open ATR breakout, version A | NAS100 | Study 17 (RTH breakout), as posted | 0.1457% risked per trade |

- Each leg runs exactly as in its own study. The code is in this folder: `book_members.py` (Cutler), `book2_members.py` (copy v3 and the breakout).
- Sizes do not grow or shrink with the account.

## Why it is here
- On April 2021 to April 2026 this book fit a $100k 1-step challenge at this size on both firms: every start passed, none breached, typical pass 159 trading days.
- Run as one unbroken account over that period, its closest call was 2.7% under the midnight balance, against a 3% limit.
- All three legs were picked because they had already made money on those years. That result is hindsight. This watch is the first test on prices nobody had seen.

## What counts
- Only trades entered at or after 00:00 UTC on November 26, 2026.
- Costs as in the studies: the lab cost table for the two NAS100 legs, plus an estimated 0.02% of price per night on the dip-buy. Copy v3 pays its "realistic" case (spread 0.0075%, commission 0.0025% a side, 0.005% slip on stop fills, swap 0.0175% a night long and 0.005% short).
- The account is marked hour by hour. Its low in an hour is the sum of each open trade's worst point in that hour.
- Firm day: midnight to midnight Prague time. Saturday counts with Friday and Sunday with Monday.
- A trade still open at the last price bar is counted when it closes. So the status can run one data refresh behind.
- Exchange days for the dip-buy come from a rule-built New York Stock Exchange holiday list. It gives the same days as the calendar file Study 12 used, 2021 to November 2026.

## Verdict (one paper challenge per firm, started on the first firm day from November 26, 2026)
| | FTMO 1-Step | The5ers 1-step |
|---|---|---|
| Target | 10% | 10% |
| Daily loss | 3% under the midnight balance, open trades counted | 3% under the higher of balance or account value at midnight |
| Max loss | 10% under the highest midnight balance | 6% under the start |
| Day rules | best day at most half of the profit | 3 days with at least 0.5% closed profit |

- **PAPER PASS:** at the end of a firm day the account value is at or above +10% and the day rules are met, with no breach before it.
- **PAPER FAIL:** the first breach of the daily or the max loss limit.
- **TOO SLOW:** 500 firm days with neither.
- **WATCHING:** until one of those.
- The verdict is given once per firm and is never revised.

## What a verdict means
- One start date is one draw. A PAPER PASS says the book survived one real stretch of new prices. It is a reason for Jeff to consider a demo account or a small challenge. It is not proof of an edge.
- A PAPER FAIL rejects this book at this size. It is not registered again with another size on the same forward bars.
- Also reported at each update, without a verdict: each leg's closed trades and profit, the book's worst day, its furthest point under the midnight balance and its deepest drawdown.

## Data it needs
- `lab/data_1m/NAS100_1m_full.csv.gz` and `lab/data_new/NAS100_1h.csv.gz`, refreshed as usual.
- `lab/data_1m/XAUUSD_1m_<year>.csv.gz`: gold 1-minute bars. The 2026 file was added at registration. Later bars come from the same refresh on Jeff's PC. A new year needs its own file.
- If the data is not refreshed, nothing moves.

## How to run
```
python lab/book/forward_book.py
```
It rebuilds the three legs from the price files and writes `lab/book/status.json`. Nothing in this folder except `status.json` is edited after registration.

## Checks at registration
- `python lab/book/forward_book.py selftest`: hand-built cases for the paper challenge and the holiday list.
- Replayed from January 1, 2024 with the same code, the script matches Study 20's own files on every one of 602 firm days (account value and day low, to the last digit shown) and gives the same outcome: passed on firm day 171 on both firms.

## Not modelled
- News rules beyond copy v3's own filter, firm limits on open risk or lot size, overnight and weekend holding rules, spread widening, real financing on the index leg, payouts and the funded phase.
