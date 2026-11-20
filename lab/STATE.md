# STATE · strategy lab

## Goal
Find out whether any mechanical trading idea survives the checks in `LAB_RULES.md`. Rejections are results.

## Done
- Lab built and run on two seed ideas (both rejected). See `JOURNAL.md`.
- 96 ideas tested before the lab existed. None passed.

## Rules learned (read before every task)
- Costs decide most outcomes on short timeframes. Prefer ideas that trade less often.
- An idea with no stated loser has failed every time so far.
- Indicator crossovers on price alone show zero edge before costs. Do not add more of them.
- Public posts tend to leave out the part the author says makes the idea work. Log what is withheld.
- Never tune after a result. A changed idea is a new attempt.
- Trend-following breakouts beat most shuffled price paths but still lose after costs (donchian_breakout, diagnostic p about 0.07).

## Needs other data (not testable with price bars)
- Order flow and footprint ideas (delta, bid/ask volume).
- Funding and open-interest ideas (tested once outside the lab: rejected, best profit factor 0.99).

## Position mode
- Built 2026-11-19. Ideas that hold weights across markets now run with `mode="position"` (see `_TEMPLATE_POSITION.py`).
- Limit: six markets in three asset classes is a thin basket. Stat arb across 10 or more coins still needs more data.

## Book progress ("151 Trading Strategies")
- Full triage is in `BOOK_INDEX.md`. Use it instead of fetching the book.
- Carded 2026-11-19, waiting in the inbox: 3.14 pivot support and resistance, 3.15 channel bounce, 4.4 IBS reversion.
- Dead on arrival: 3.11 to 3.13 (moving-average crossovers).
- Tested in position mode 2026-11-19, both rejected: 10.4 time-series momentum (Sharpe 0.05), 10.3 cross-market contrarian (Sharpe 0.13).
- Still open for position mode: 3.8 to 3.10 pairs and cluster reversion, 3.17 nearest neighbours, 3.18 stat arb, 3.20 alpha combination, 8.1 HP-filter trend.

## Screen track
- Built 2026-11-20. `screen.py` builds 4,000 ideas from parts, screens them on trades before April 21, 2024, and gives each survivor one run on April 2024 to April 2026.
- Rules: "Screen and confirm" in `LAB_RULES.md`. Progress: `screen/state.json`. Every screened idea: `screen/log.csv`.
- First batch 2026-11-20: 100 screened, 1 survivor, 0 confirmed. The survivor (24-bar extreme move, follow) had a t-stat of 3.81 on the screen years and -0.25 on the confirm years.
- Second batch 2026-11-20: 100 screened, 0 survivors. Running totals: 200 of 4,000 screened, 1 survivor, 0 confirmed.
- On shuffled prices 0 of 400 ideas passed the screen, so a survivor is rarely pure luck in the screen years. It can still fail to carry forward, as the first one did.
- Limit: 1-hour bars and single-market triggers only. Cross-market triggers and other timeframes would be a new catalogue version.

## Next
- Fill `ideas/inbox/` from "151 Trading Strategies" (see `AGENT.md`) and from the X scout prompt in `GROK_SCOUT_PROMPT.md`.

## Last session
2026-11-19 · 4 tested (2 signal mode, 2 position mode), 4 rejected, 0 candidates
