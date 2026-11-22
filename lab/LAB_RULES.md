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

## New-market test (added November 20, 2026, before any new-market data arrived)
A one-time check of the watched ideas on markets the lab has never used. It asks one question: does the rule work somewhere it was never looked at?

- Markets: NAS100, SPX500, USOIL, EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD and EURJPY. Hourly bars from April 21, 2021 to the day of the download.
- Who: every idea on the forward watch on November 20, 2026 (13 ideas). Their parts are frozen.
- Fees per side: forex 0.015%, indices 0.025%, oil 0.03%. Slippage, fills, exits and the cooldown are the same as everywhere else.
- One run per idea, on the new markets only. No second run, no changed parts, no dropped markets. A market whose download fails is left out and named in the journal.
- All must hold:
  1. At least 150 trades.
  2. Profit factor of 1.15 or more.
  3. Profit factor above 1.0 with costs doubled.
  4. Profitable in at least half of the new markets.
  5. Beats 95% of 1,000 random-entry runs with the same trade count, sides and exits.
  6. t-stat of 2.67 or more (the normal quantile at 1 - 0.05 / 13, for 13 ideas tested). First written as 2.65 by a rounding slip; corrected to the formula's value before the run.
- An idea that passes is a CANDIDATE. It stays on the forward watch, which is still the last gate before the account-fit check.
- An idea that fails stays on the forward watch too, marked as failed here. Nothing is removed.
- The new markets are kept apart in `lab/data_new`. They do not join the screen until a new catalogue version says so.

## Catalogue version 3: fifteen markets (added November 20, 2026, before any trigger ran under it)
The new-market test showed that every watched idea lost money on markets it was not found on. From here a new idea has to work broadly to survive.

- Applies to every trigger registered from now on. The 4,320 ideas already screened are not re-run, and their results stand.
- Markets: the six lab markets plus NAS100, SPX500, USOIL, EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD and EURJPY (`lab/data_new`).
- Fees per side for the nine: forex 0.015%, indices 0.025%, oil 0.03%. Everything else about fills and exits is unchanged.
- The data split is unchanged: screen years before April 21, 2024; confirm years to April 20, 2026; quarantine after that.
- Screen and confirm thresholds are unchanged. "Half of the markets" now means 8 of 15.
- The survivor count carries on from 109, so the bar keeps rising.
- The nine added markets were used once, for the new-market test of 13 older ideas. No new trigger has touched them.
- Forward watch: every watched idea, old or new, is tracked on all fifteen markets from its start date.

## Paper track (added November 20, 2026, before any paper was tested under it)
A paper is a published study that states trading rules. The paper track finds them, writes each one down, and tests the ones the lab's data can test. Files: `lab/papers/`. Tool: `lab/tools/paper.py`.

### Finding and filtering
- Sources: new listings on arXiv (quantitative finance), SSRN and NBER.
- Every abstract looked at is logged in `papers/seen.csv` as kept or dropped, with a reason. A paper is looked at once.
- Kept: the abstract points to explicit buy and sell rules. Dropped: everything else.

### One file per paper
- Each kept paper gets `papers/ID.yaml`: formulas, variables, entry and exit rules, market, timeframe, the data it needs, and the results the authors report.
- The authors' results are copied as they state them and are never mixed with the lab's numbers.
- The file is written in the lab's own words. Formulas are facts and may be stated. Long passages are not copied.

### What can be tested
- The lab has 1-hour bars for fifteen markets since April 2021 (gold since 2009) and nothing else.
- A paper whose rule needs other data is marked `cant_test`, with the missing data named. It is not approximated with data the lab happens to have.
- A testable paper is tested on its own market if the lab holds it. If the paper claims the rule is general, it runs on all fifteen.

### How a paper is tested
- It becomes one idea in the main track and counts as one attempt against the rising bar. The seven checks apply unchanged.
- The idea is coded from the paper's rule as written. Its settings are the paper's settings. Nothing is tuned to the lab's data.
- Formula check: the idea file carries a second, slow, literal version of each formula. `tools/check_formula.py` compares the two on random price paths before the test. They must agree on every bar. This catches slips in the code. It cannot catch a misreading of the paper.

### Nearby settings (applies to every signal idea in the main track from attempt 104 on)
- An idea that passes the seven checks and the permutation test is re-run with each number in its settings moved 20% down and 20% up, one at a time.
- At least two thirds of those re-runs must keep a walk-forward profit factor above 1.0. If not, the idea is rejected before the quarantine run.
- This check can only reject an idea. It never rescues one.

### Before and after publication
- The walk-forward test years are split at the paper's publication date. Years that end before it are "before". Years that start on or after it are "after". A year that straddles the date is left out of the split.
- Both halves are reported when they exist. Most papers were published before the lab's data begins, so often only "after" exists.

### Verdict for a paper
- `holds_up`: the idea reached CANDIDATE.
- `decayed`: not a candidate; at least two "before" years with a positive total and at least 60% of them profitable; and at least one "after" year with a total at or below zero.
- `failed`: tested and rejected, and not `decayed`. It means the rule failed on the lab's markets and costs, not that the paper is wrong about its own.
- `cant_test`: the lab lacks the data.

### Morning brief
- Each run writes `lab/briefs/DATE.md`: papers scanned, kept and dropped; each verdict; which missing data blocks the most papers; and the screen and forward-watch totals.
- For a paper that holds up, the brief says in which market conditions the edge might stop working. That part is a theory and is labelled as one.

### Main-track markets (amended November 20, 2026)
- An idea may name any of the fifteen markets, or ask for all fifteen. An idea that names none still runs on the original six, so earlier results are unchanged.

## Intraday study 1: opening range breakout (written November 21, 2026, before any 1-minute data was downloaded)
A one-off study on 1-minute bars, which the rest of the lab does not have. Code: `lab/intraday/orb.py`. Data: `lab/data_1m/`.

### Where the rule comes from
- A YouTube video, "I Built a Trading Bot to Pass Prop Firm Challenges" (Jan - Algo Trader, October 29, 2026). It reports 296 trades since 2024 with a 93% win rate and a profit factor of 2.45 on Nasdaq futures, after its filters were adjusted on that same period.
- The video states the range (9:30 to 9:45 New York time), the direction rule, a 10-minute time exit and a relative-volume filter of 0.5 to 1.5. It does not state the entry time clearly, the stop and target sizes, or its volatility band.
- So this study tests the core of the rule, with the unstated parts fixed below before any data is seen. It is the lab's version, not a copy of the video's bot.

### The rule
- Market: Nasdaq 100 index, 1-minute bars, New York time with daylight saving handled.
- Range: the highest high and lowest low of the bars from 9:30 to 9:44.
- Decision: at the close of the 9:59 bar. Close above the range high: buy. Close below the range low: sell. Inside the range: no trade.
- Entry: the open of the 10:00 bar. Exit: the open of the 10:10 bar. No stop and no target, so the test measures the signal itself.
- Test A uses the video's volume filter: the 9:59 bar's volume divided by the average volume of the 14 bars before it must be between 0.5 and 1.5.
- Test B uses no filter.
- A day is skipped if fewer than 12 of the 15 range bars exist, or if the 9:59, 10:00 or 10:10 bar is missing.
- Cost: 0.005% of price per round trip, about 1 Nasdaq point, covering commission and slippage on a futures contract. The double-cost check uses 0.01%.

### The data split
- Unseen years: April 21, 2021 to December 31, 2023. The video's backtest starts in 2024, so its settings were never fitted to these years. The verdict comes from here.
- The video's years: January 1, 2024 to the download date. Reported for comparison only.

### Pass, on the unseen years (each test is judged on its own)
1. At least 150 trades.
2. Average net return per trade above zero, with a t-stat of 2.58 or more (the normal quantile at 1 - 0.01 / 2, for two tests).
3. Profit factor of 1.15 or more.
4. Average return still above zero at double cost.
5. A positive total in at least two of the three calendar years 2021, 2022 and 2023.

### Also reported, without changing the verdict
- The same two tests on the S&P 500 and the Dow, to show whether the effect is broad.
- Win rate, average win and average loss, so the result can be compared with the video's.

### What a result means
- PASS: the rule earns a forward watch on new 1-minute data and a second study with stops and targets. It is not a reason to trade or to buy a challenge.
- FAIL: the rule is rejected. It is not re-run with a different range, entry time, holding time or filter on this data.
- If the video's exact settings are obtained later, testing them is a new study with its own count.

## Intraday study 2: opening range variations (written November 21, 2026, before any 1-minute data reached the lab)
Study 1 tests one version of the opening range rule. This study tests a fixed family of 36, so that trying variations cannot turn into tuning. Code: `lab/intraday/orb2.py`. Data: full-session 1-minute bars in `lab/data_1m/`.

### The 36 versions
Every combination of four parts. Times are New York time.
- Range: the high and low of the first 5, 15 or 30 minutes from 9:30.
- Entry, one of:
  - Breakout: the first 1-minute bar after the range ends, and before 11:00, that closes outside the range. Enter at the next bar's open.
  - Fixed check: the bar that ends 15 minutes after the range ends (9:49, 9:59 or 10:14). If it closes outside the range, enter at the next bar's open. Inside the range: no trade.
- Exit: the open of the bar 10 minutes after entry, 60 minutes after entry, or at 15:55.
- Direction: with the break (buy above, sell below) or against it.
- One trade per market per day at most. No stops and no targets, so each version measures a signal and nothing else.
- A day is skipped for a market if more than a fifth of its range bars are missing, or if the entry or exit bar is missing.
- Cost: 0.005% of price per round trip. The double-cost check uses 0.01%.

### Markets and counting
- Nasdaq 100, S&P 500 and Dow, tested together.
- The three move together, so a day counts once: each day's result is the average of the markets that traded that day. All statistics below are on those daily averages.

### Data split
- Screen years: April 21, 2021 to December 31, 2023.
- Confirm years: January 1, 2024 to the download date. A version sees these only if it passes the screen.
- One version (15-minute range, fixed check, 10-minute exit, with the break) is close to the video's rule and to study 1, whose results on both periods will already have been seen. That is noted, not corrected for: the steps below are mechanical.

### Screen (all must hold)
1. At least 150 traded days.
2. Average above zero, with a t-stat of 1.65 or more.
3. Profit factor of 1.10 or more.
4. Average above zero on at least two of the three markets taken alone.
5. Average above zero at double cost.

### Confirm (one run per survivor; all must hold)
1. At least 150 traded days.
2. Average above zero, with a t-stat at or above the normal quantile at 1 - 0.05 / survivors, where survivors is counted as 5 if fewer than 5 pass the screen. So the bar is 2.33 or higher.
3. Profit factor of 1.15 or more.
4. Average above zero on at least two of the three markets taken alone.
5. Average above zero at double cost.
6. A positive total in at least two of the calendar years 2024, 2025 and 2026.

### What a result means
- CONFIRMED: the version earns a forward watch on new 1-minute data and a later study with stops and position sizing against prop-firm limits. It is not a reason to trade or to buy a challenge.
- Everything else is rejected. No version is re-run with other numbers on this data, and no version is added to the family after the data has been seen.
- All 36 results are logged, including the ones that fail.
