# Lab rules

These are fixed. An idea is rejected unless it passes every check. Do not edit thresholds to rescue an idea.

## Data and fills
- 1-hour bars for BTCUSD, ETHUSD, XAUUSD, GBPJPY, USA30 and DEU30 (`lab/data`).
- Entry at the next bar's open. Stops and targets are checked on highs and lows. Gaps fill at the open. If stop and target fall in one bar, the stop is hit first.
- Fees per side: BTC 0.03%, ETH 0.04%, gold 0.02%, GBPJPY 0.015%, indices 0.025%. Stop slippage 0.02%.
- Exits are the same for every idea: stop at 2 or 3 ATR, target at 1.5 or 2.5 times the stop. Six-bar cooldown.

## Walk-forward
- A block is 12 months starting April 21.
- For each market and each test block, the config is chosen on the three blocks before it (two if only two exist), by t-stat, with at least 20 trades.
- Results are pooled over markets and test blocks.

## Checks (all must pass)
1. Profit factor of 1.15 or more.
2. At least 150 out-of-sample trades.
3. Profitable in at least 60% of test years.
4. Profitable in at least half of the markets.
5. Profit factor above 1.0 with costs doubled.
6. Beats 95% of 1,000 random-entry runs with the same trade count, sides and exits.
7. t-stat at or above the bar for the attempt number.

## Permutation test (added November 19, 2026, before any idea beyond the two seeds)
- Runs only for an idea that passes all seven checks, and before quarantine.
- Each market's bars are shuffled into 200 random paths. Gaps and in-bar moves are shuffled separately, so volatility and drift stay and real patterns are destroyed.
- The whole walk-forward, including config selection, is re-run on each path.
- p is the share of shuffled paths that do at least as well as the real one. The idea needs p of 0.01 or less.
- A parameter plateau is checked by hand before promotion: the neighbouring settings must also be profitable.

## Position mode (added November 19, 2026)
For ideas that hold weights across markets day by day: trend, relative value, stat arb. The idea file sets `mode="position"`.

- Daily bars built from the hourly data. The day rolls at 22:00 UTC. A weight decided at a day's close earns the next day's return.
- Total exposure is capped at 1. Every change in a weight pays that market's fee plus slippage.
- Walk-forward is the same: the parameter set for each test year is chosen on the three years before it.
- Checks (all must pass):
  1. Annualised Sharpe of 0.8 or more.
  2. At least 500 days in the market.
  3. Profitable in at least 60% of test years.
  4. At least half of the markets contribute a profit.
  5. Still profitable with costs doubled.
  6. Beats 95% of 1,000 copies of itself with the positions shifted in time.
  7. t-stat at or above the rising bar.
  8. Permutation test, p of 0.01 or less. Days are shuffled jointly across markets, so same-day links between markets survive.
- Quarantine: at least 100 days in the held-back block and a positive total.

## The rising bar
- Every idea tested is one attempt. The counter started at 96, the number of ideas tested before the lab existed.
- Required t-stat = the normal quantile at 1 - 0.05 / attempts. At attempt 100 that is about 3.3.
- The bar only goes up. Changing an idea file and re-running it is a new attempt.

## Quarantine
- The block starting April 21, 2026 is held back. No idea sees it during the checks.
- An idea that passes all seven checks and the permutation test gets exactly one run on it. It needs 20 or more trades and a profit factor above 1.0.
- An idea that passes quarantine is a CANDIDATE. That means "worth watching on new data", never "proven".

## Ensembles
- Only CANDIDATE ideas may be combined. Weights are equal and fixed.
- An ensemble is itself an idea: it counts as an attempt and must pass the same checks.

## Journal
- Every run appends to `JOURNAL.md`. Entries are never edited or deleted.

## Screen and confirm (added November 20, 2026, before any idea ran under it)
A second track, separate from the one above. It tests many machine-built ideas cheaply, then checks the survivors on years the screen never saw. Code: `lab/screen.py`.

### Ideas
- An idea is built from parts: trigger, direction (follow or fade), regime filter, session filter and one of the four standard exits.
- The catalogue is fixed at 4,000 ideas (version 1) and is screened in a fixed shuffled order. Each idea is screened once.
- These ideas have no stated reason and no stated loser. Fresh data replaces the reason.
- Fills, fees, slippage and the six-bar cooldown are the same as above. One exit per idea, so nothing is tuned.

### Data split
- Screen years: every trade entered before April 21, 2024.
- Confirm years: April 21, 2024 to April 20, 2026. The screen never reads results from these years.
- Quarantine: the block starting April 21, 2026, as above.
- Caveat: the 100 ideas tested before this track did use the confirm years. They are unseen only by screened ideas.

### Screen (loose on purpose; all must pass)
1. At least 150 trades.
2. Profit factor of 1.10 or more.
3. t-stat of 1.65 or more.
4. Profitable in at least half of the markets.
5. Profit factor above 1.0 with costs doubled.

### Confirm (one run per survivor; all must pass)
1. At least 60 trades in the confirm years.
2. Profit factor of 1.15 or more.
3. Profitable in at least half of the markets.
4. Profit factor above 1.0 with costs doubled.
5. Beats 95% of 1,000 random-entry runs with the same trade count, sides and exits.
6. t-stat at or above the survivor bar: the normal quantile at 1 - 0.05 / survivors, where survivors is the number of ideas ever sent to confirm, counted as 20 until it passes 20. So the bar starts at about 2.81 and only goes up.
   - Amended November 20, 2026, after the first batch of 100: the count of 20 was added because the first few survivors would otherwise face a bar as low as 1.64. One survivor had been judged by then. It failed with a t-stat of -0.25, so no verdict changed.

### After confirm
- A confirmed idea gets one quarantine run: 20 or more trades and a profit factor above 1.0. Passing makes it a CANDIDATE.
- A CANDIDATE from this track means the same as above: worth watching on new data, never proven.

### Counting
- Screened ideas do not raise the attempt counter of the main track, and main-track ideas do not raise the survivor bar.
- Every screened idea is logged in `lab/screen/log.csv`. Every survivor gets a journal entry and a file in `lab/screen/confirm/`.
- Changing a threshold, a part or the split means a new catalogue version and a new log. Past results stay.

## Growing catalogue (added November 20, 2026, before any new trigger ran)
Catalogue version 1 (4,000 ideas) is fully screened. From here the catalogue grows.

- A new trigger is one file in `lab/triggers`. It returns +1, -1 or 0 at each bar, using the current bar and earlier bars only.
- Every trigger must cite an outside source: a paper, a book, a public write-up or open-source code. It must not be designed from this lab's own confirm results.
- A trigger has at most 3 parameter sets. Each set is expanded into every direction, regime filter, session filter and exit: 160 ideas, or 40 for a time-based trigger.
- `screen.py` checks each new file for look-ahead and registers it. A registered file never changes. A changed idea is a new trigger with a new name.
- The catalogue is append-only. The 4,000 ideas of version 1 and their results stay as they are.
- Screen and confirm thresholds, the data split and the survivor bar are unchanged. The survivor count carries on from 87, so a new survivor needs a t-stat of about 3.25 or more on the confirm years.
- Caveat: every new survivor is judged on the same confirm years. The rising bar is the defence. The forward watch below is the final judge.

## Forward watch (added November 20, 2026, before any forward price bar existed)
The third gate. An idea is tracked on price bars that did not exist when it was registered. No money is involved. Code: `lab/forward.py`.

### Who is watched
- Every CANDIDATE.
- Every near miss: a screen survivor that passed every confirm check except the survivor bar. The 12 near misses of catalogue version 1 were registered on November 20, 2026.
- An idea is registered once, with its parts frozen. It is never edited or removed.

### What counts
- Only trades entered at or after 00:00 UTC on the day after registration.
- Fills, fees, slippage and exits are the same as everywhere else in the lab.
- A market added to the lab later counts from its first bar after the idea's start date.

### Verdict (given once, at the first run with 200 or more forward trades)
All must hold, or the idea fails:
1. Profit factor of 1.15 or more.
2. Profit factor above 1.0 with costs doubled.
3. Profitable in at least half of the markets that traded.
4. t-stat at or above the normal quantile at 1 - 0.05 / watched, where watched is the number of ideas ever registered.

- Before 200 trades the status is WATCHING. Nothing is concluded from a partial count.
- FORWARD PASS means the idea may go to the account-fit check. It is still not a guarantee.
- The forward watch needs new price bars in `lab/data`. If the data is not refreshed, nothing moves.
