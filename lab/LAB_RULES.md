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

## Intraday study 3: the video's own settings (written November 21, 2026, before any 1-minute data reached the lab)
Study 1 said that if the video's exact settings turned up, testing them would be a new study. Jeff sent a screenshot of the settings panel after studies 1 and 2 were registered. Code: `lab/intraday/orb3.py`. Data: the same first-hour 1-minute files as study 1.

### The settings in the screenshot
Range 9:30 to 9:45. Entry time 9:59. One trade a day. ATR period 14. Stop 1 ATR. Target 2 ATR. Time exit 10 minutes. Relative volume: lookback 14, minimum 0.5, maximum 1.5. ATR regime: average length 14, minimum 1, maximum 3.

### The rule
- Range, decision bar, entry (open of the 10:00 bar) and volume filter: the same as study 1, test A.
- ATR: the average true range of the 14 one-minute bars ending with the 9:59 bar.
- Stop: 1 ATR against the trade from the entry price. Target: 2 ATR in favour.
- The bars from 10:00 to 10:09 are checked in order. Neither level reached: exit at the open of the 10:10 bar.
- A bar that opens beyond the stop exits at that open. A target is filled at the target price, never better.
- Test A adds the ATR regime filter: the ATR at 9:59 divided by the average of the last 14 ATR values must be between 1 and 3.
- Test B leaves the ATR regime filter out.
- Cost, skipped days, markets: the same as study 1. A day is also skipped if there are too few bars before 9:59 to work out the ATR figures.

### What is assumed, because the screenshot does not say
- That ATR is measured on 1-minute bars as a simple average of true range.
- That "ATR regime" means the ratio described above. Test B exists because this reading may be wrong.
- The volume is Dukascopy's index volume, not futures volume. The prices are bid prices.

### Stops inside a 1-minute bar
- A 1-minute bar can touch both the stop and the target. The bar does not say which came first. Tick data would.
- The verdict counts every such trade as a loss at the stop.
- The same trades counted as wins are reported next to it, with how many trades this affects. If the two differ enough to change the verdict, the answer needs tick data and the study says so.

### Pass, on the years before 2024 (each test is judged on its own)
The same five checks as study 1, including the t-stat of 2.58 for two tests. The years from 2024 are reported for comparison with the video's 93% win rate and 2.45 profit factor.

### What a result means
- PASS: a forward watch on new data and a tick-data check of the trades. It is not a reason to trade or to buy a challenge.
- FAIL: rejected. Not re-run with other settings on this data.

## Intraday study 4: hold to the close, as one group (written November 22, 2026, before these versions' results from 2024 on were computed)
One test, drawn from what study 2 showed. Code: `lab/intraday/orb4.py`. Data: the full-session files study 2 used.

### Where the idea comes from, and what has been seen
- In study 2's screen years, five of the six "with the break, exit at 15:55" versions had a positive average. None reached the screen bar, so all six were rejected one by one.
- This study asks a different question: do the six, taken together as one rule, make money in the years from 2024 on?
- The idea was picked after seeing the screen years. That is allowed here only because the test uses years in which none of the six has been computed.
- What has been seen from 2024 on: study 1 and study 3 (10-minute exits, with and without stops) and one study 2 version (5-minute range, 10-minute exit, against the break). None holds to the close.

### The rule
- The six versions: range of 5, 15 or 30 minutes; breakout or fixed check; with the break; exit at the open of the 15:55 bar. Entries, skipped days and cost exactly as in study 2.
- Markets: Nasdaq 100, S&P 500 and Dow.
- One number per day: for each version, the average across the markets it traded; then the average across the versions that traded. All statistics are on those daily numbers.
- Period: January 1, 2024 to November 20, 2026.

### Pass (all must hold)
1. At least 150 traded days.
2. Average above zero, with a t-stat of 2.58 or more.
3. Profit factor of 1.15 or more.
4. Average above zero on at least two of the three markets taken alone.
5. Average above zero at double cost.
6. A positive total in at least two of 2024, 2025 and 2026.
7. At least four of the six versions have an average above zero on their own.
8. The short trades taken alone have an average above zero, counting every short trade equally. Without this, a pass could be nothing more than the market rising.
   - The first draft of this check averaged short trades per day, like the group. A dry run on made-up prices showed that method is biased: on days when the versions disagree, the lone short is usually the one the price has already turned against, and it counted as a whole day. On random prices it made shorts look like losers. The check was changed to equal weight per trade before any real result was computed.

### Also reported, without changing the verdict
Each version alone, long trades alone (every trade counted equally), and win rate.

### What a result means
- PASS: a forward watch on new 1-minute data and a later study with stops and position sizing against prop-firm limits. It is not a reason to trade or to buy a challenge.
- FAIL: the opening range idea is closed on this data. No further versions, groups or filters are tried on these files.
- This study runs once.

## Intraday study 5: the video's 93% run, replayed on ticks (written November 22, 2026, before any tick data was downloaded)
Studies 1 and 3 could not reproduce the video's 93% win rate. Reading the video frame by frame showed why: the 93% run is not the settings the video shows being typed in. Code: `lab/intraday/orb5.py`. Data: Dukascopy tick quotes for the Nasdaq 100, a few minutes around 10:00 New York time each day.

### What the video shows on screen
- The settings in the panel (1 ATR stop, 2 ATR target, 10-minute exit, 17 parameters) produced, on the video's own screen: 77 trades, 40.3% win rate, profit factor 0.57, account down 98%. Study 3 found a 37% to 40% win rate for the same settings. The two agree.
- The 93% run has 21 parameters, 6 contracts on $10,000, and a cost of $0.80 a contract instead of $2.50. Its results panel shows an average win of $798 and an average loss of $5,021.
- Its trade list shows entries at 9:59:55 and most exits within seconds. Eight trades with stop and target prices visible give, against the lab's own 1-minute data: target 0.30 ATR and stop 2.29 ATR on average, with Wilder's 14-bar ATR at the 9:58 bar. One losing trade closed 8 minutes after entry.
- The on-screen assistant had just offered to optimise the stop, target and time exit. The video does not say this was done.
- Check of the entry rule: of 23 trades read off the screen, the lab's rule takes the same side on 22 and no trade on 1.

### The rule tested
- Range: high and low of the 1-minute bars from 9:30 to 9:44.
- Signal: the last quote at or before 9:59:55. Bid above the range high: buy. Bid below the range low: sell. Otherwise no trade.
- Entry: the first quote after 9:59:55.
- ATR: Wilder's 14-bar average true range on 1-minute bars, read at the 9:58 bar.
- Target 0.3 ATR, stop 2.3 ATR, both measured from the entry price. Time exit 8 minutes after entry.
- No volume or ATR regime filter: neither can be reproduced here. The video's run took 296 trades; this rule will take more.
- A day is skipped if fewer than 12 of the 15 range bars exist, if there is no quote in the 10 seconds before 9:59:55, or if there is no quote in the 30 seconds before the time exit.

### Three ways of filling the same trades
- A, the video's way: every fill at the mid price with no spread. The target fills the moment the mid price touches it. Cost 0.0004% a round trip ($0.80 a contract each way).
- B, realistic futures: market orders (entry, stop, time exit) fill a quarter point worse than mid. The target is a resting order and fills only when the mid price is a quarter point beyond it. Cost 0.001% a round trip.
- C, the index as quoted: buy at the ask, sell at the bid, target and stop judged on the side being sold or bought back. No commission. This is closest to an FTMO-style account.

### Pass (fill B, years before 2024, which the video's settings were never fitted to)
1. At least 150 trades.
2. Average above zero, with a t-stat of 2.58 or more.
3. Profit factor of 1.15 or more.
4. Average above zero when stop and time-exit fills are another half point worse.
5. A positive total in at least two of 2021, 2022 and 2023.

### Also reported, without changing the verdict
- Fills A and C, and all three from 2024 on, next to the video's 93.9% and 2.45.
- The same rule on 1-minute candles (entry at the 10:00 open, a bar that touches both levels counted as a loss), on the same days. This is the tick-against-candle comparison.
- Win rate needed to break even at this stop and target, for reference: a target of 0.3 and a stop of 2.3 wins about 88% of the time with no edge at all.

### What a result means
- PASS: a forward watch on new tick data and an account-fit study. One loss here is about eight wins, so sizing against prop-firm daily limits decides whether it is usable at all. It is not a reason to trade or to buy a challenge.
- FAIL: rejected. Not re-run with other stops, targets or times on this data.
- This study runs once.

## Intraday study 6: Coil Reclaim, a first-hour breakout with a pullback entry (written November 22, 2026, before this rule was run on any lab data)
One rule from one outside source, at its default settings. Code: `lab/intraday/coil.py`. Data: the full-session 1-minute files in `lab/data_1m/` and the lab's 1-hour files for the same three markets.

### Where the rule comes from
- A public GitHub repo, `Allencake/coil-reclaim-indicator` (MIT licence), sent by Jeff on November 22, 2026. It holds a TradingView indicator in Pine Script and a prompt for an AI agent. It was created that same day by an anonymous account.
- The repo gives no backtest, win rate or profit figure, and says so. It credits the rules to "a publicly shared idea" without naming it. Its sample alert is a Bitcoin perpetual on 15-minute bars.
- The indicator has about 35 settings. This study uses the defaults and changes none of them.

### Why this is run although the opening range idea is closed
- Study 4 closed the opening range idea on these files: no further versions, groups or filters.
- This is a different rule from a different source. Its range is any 3 to 20 bar pause, not the first minutes after 9:30. It takes its direction from the daily and 4-hour candles, enters only after a pullback, and uses a stop, a part exit and a target.
- It is still a first-hour breakout on the same three markets and the same files, so it is the same family. Jeff was told this, and that the family had failed four studies, and asked for the test.

### What has been seen
- Studies 1 to 4 ran on these files. None computed this rule or any part of it.
- Before these rules were written, the session looked at file coverage only: the 1-minute files run from 8:00 to 16:14 New York time, and the 1-hour files end on November 20, 2026 at 05:00 UTC.

### The rule (the indicator's defaults)
Times are New York time. Chart bars are 5-minute bars built from the 1-minute files. Every decision is made at the close of a 5-minute bar.
- Direction, fixed at the close of the 9:30 bar for the day:
  - Two candles: the last finished daily candle and the 4-hour candle from 5:00 to 9:00. Both up: buy only. Both down: sell only.
  - If they disagree: price within a quarter of the daily ATR of an unbroken daily ceiling means sell only; near a daily floor means buy only; otherwise follow the weekly swing direction (daily if the weekly is not yet defined); otherwise follow the daily candle.
- Levels: a ceiling is an up candle followed by a down candle, drawn at the higher of the two bodies. A floor is the mirror image. A level is broken when a candle of its own timeframe closes beyond it. The two most recent unbroken ceilings and floors are kept on the daily, 4-hour and 1-hour timeframes.
- Blocked for the day: during the window, if the direction is buy and price is at a daily ceiling (or sell at a daily floor).
- Clean zone: a run of at least 3 same-colour 5-minute bars covering at least 1.5 ATR, ended by two opposite bars. The 8 most recent are kept. A zone is dropped when a new 4-hour or 1-hour level forms inside it.
- Wait for a pullback: if the 5:00 to 9:00 candle already ran in the trade direction (body at least 60% of its range, range at least one 4-hour ATR), the range must sit at least 38.2% back into that candle.
- Trigger, only on bars that open from 9:30 to 10:25:
  - A range of 3 to 20 earlier bars, measured on candle bodies, with at least 2 bars against the direction and a height of 0.5 to 4 ATR.
  - A breakout bar in the direction that closes beyond the range, with a body of at least half its own range and a range of no more than half the range height. Its far end must lie in a clean zone.
  - A stop order at the breakout bar's high (low for a sell). The protective stop is the other end of that bar.
  - The order fills only after a pullback bar: a wick of at least 0.1 ATR and 20% of that bar's range. It is cancelled if price reaches it with no pullback first, if a bar closes back inside the range, or after 6 bars.
- Exit: at 1R close half and move the stop to the entry price. The stop also moves to entry if a level is touched before 1R. The rest is held to the nearest unbroken level beyond 1R, capped at 3R. Close everything if the trade is at least 1.5R ahead after 3 straight bars in its direction, or 240 minutes after entry. A bar that reaches the stop is a stop, whatever else it reached.
- At most 2 trades a day for each market, one at a time.

### Where the lab's version differs from the indicator on a TradingView chart
These were fixed before any result was computed. Each is forced by the data.
- New York session only. The lab has no 1-minute bars for the Asia or London hours.
- 5-minute bars only. On 15-minute bars the files hold too little of the morning before 9:30.
- Markets: Nasdaq 100, S&P 500 and Dow. The repo's sample is Bitcoin, which the lab does not hold below 1-hour bars.
- The 5-minute ATR (Wilder, 14 bars) restarts each day at 8:00, so the overnight gap does not inflate it. The range may only use bars from the same day.
- Clean zones can only form from bars between 8:00 and 16:14, because that is all the files hold. On a 24-hour chart there would be more zones, so the lab's version takes fewer trades than the indicator would.
- Daily candles run from 17:00 to 17:00 and 4-hour candles start at 17:00, 21:00, 1:00, 5:00, 9:00 and 13:00. A broker with another day boundary would give other candles.
- The first trades are on June 1, 2021, to let the daily and weekly measures fill in. The last possible day is November 19, 2026, where the 1-hour files end.
- A day is skipped for a market if fewer than 135 of the 150 one-minute bars from 8:00 to 10:29 exist, if any 5-minute bar in that stretch is missing, or if the 5:00 to 9:00 candle is incomplete. A trade still open when the day's bars end is closed at the last price, and such trades are counted in the report.

### Two ways of filling the same signals
- A, the indicator's own bookkeeping. A bar that both forms the pullback wick and touches the order counts as filled at the order price. On the fill bar, the stop counts only if the bar closes beyond it. This is what the chart labels would show.
- B, as it could be traded. The verdict is on B.
  - If the pullback wick and the touch come in the same bar, nobody can know it is a pullback bar until it closes. So the entry is at that bar's close, if the close is at or beyond the order price. If it is not, the order stays live as a resting stop order.
  - A resting order fills at the order price, or at the bar's open if that is worse. Inside the fill bar the 1-minute bars decide the stop: stopped if the fill minute closes beyond the stop, or if any later minute trades through it.
  - Everything after the fill bar is the same as A.
- Cost for both: 0.005% of price per round trip, charged once per trade whatever the part exits. The double-cost check uses 0.01%.

### Counting
- Results are in R: profit or loss divided by the distance from entry to the first stop.
- The three markets move together, so a day counts once: each market's trades for the day are added up, and the day's result is the average across the markets that traded. All statistics are on those daily numbers unless stated.
- Period: June 1, 2021 to November 19, 2026, as one test. The rule has no fitted period to keep apart, and it is run once.

### Pass, on fill B (all must hold)
1. At least 150 traded days.
2. Average above zero, with a t-stat of 2.58 or more.
3. Profit factor of 1.15 or more.
4. Average above zero at double cost.
5. Average above zero on at least two of the three markets taken alone.
6. A positive total in at least four of the six calendar years 2021 to 2026.
7. Long trades alone and short trades alone each have an average above zero, counting every trade equally.

### Also reported, without changing the verdict
- Fill A, next to B.
- Win rate, trades per market, how trades ended (stop, break-even, target, too fast, time), and how many orders were cancelled and why.
- A dry run of the same code on made-up prices with no cost. Made-up prices have no edge, so B should average about zero there. If A does not, the gap is how much the indicator's own bookkeeping flatters it.

### What a result means
- PASS: a forward watch on new 1-minute data, and the prop-rules calculator before any challenge. It is not a reason to trade or to buy a challenge.
- FAIL: the rule is rejected. It is not re-run with other settings, sessions, timeframes or filters on these files.
- Fewer than 150 traded days is a FAIL marked "too few trades": the rule was not shown to work, and loosening it to get more trades would be tuning.
- Testing it on the market it was written for (Bitcoin, 15-minute bars) would be a new study with new data and its own count.
- This study runs once.

## Study 7: the "7H Profile · Fractal Model" script on 1-hour bars (written November 23, 2026, before this rule was run on any lab data)
One rule from one outside source, at its default settings, on the lab's fifteen markets. Code: `lab/intraday/fractal7h.py`. Data: the lab's 1-hour files.

### Where the rule comes from
- An anonymous paste, pastebin.com/9AMMivPh, sent by Jeff on November 23, 2026. It is a TradingView indicator in Pine Script, 1,155 lines, titled "7H Profile · Fractal Model Pro". It was posted on November 22, 2026 by a user called "ajiim" with no author, licence or credits in the code. Where it came from before that is unknown.
- It gives no backtest. Its on-chart panel counts wins and losses for the few setups on screen, which is not evidence.
- It has about 90 settings, most of them drawing options. This study uses the defaults and changes none.
- The script says it works on charts of 1 hour or lower and recommends 15, 5 or 3 minutes. The lab holds 24-hour data on 1-hour bars only, so this is the script's slowest allowed chart, not its recommended one. On 1-hour bars the script picks its "method A" by itself.

### What has been seen
- These 1-hour files have been used for the whole screen track. None of that computed this rule. The built-in `sweep` trigger is a simpler relative and confirmed nothing.
- Before these rules were written, the session read the script in full and checked file coverage in New York time, by market and by season: every market has the hours from 1:00 to 11:00 on at least 99% of weekdays, summer and winter. No result of any kind was computed.

### The rule (the script's defaults)
Times are New York time. Every decision is made at the close of a 1-hour bar.
- The day starts at 18:00 and is cut into blocks of 7 hours: 18:00 to 1:00 (Asia), 1:00 to 8:00 (London), 8:00 to 15:00 (New York), and the rest to 18:00. A gap of 7 hours or more in the bars also starts a new day.
- Daily direction, set when a day ends:
  - A swing low is a day whose low is below the day before and not above the day after. A swing high is the mirror. One of each is kept as the "relevant" swing. A newer swing replaces it if it is more extreme, or if it stands at least half a daily ATR (14 days) away and the pullback to it was no more than 50% of the move since.
  - A day that dips below the relevant swing low and closes back above it turns the direction up, and that day's low becomes the new relevant low. The mirror turns it down.
  - A day that closes below the relevant swing low turns the direction down. A close above the relevant swing high turns it up.
  - No trading for a day if the day before left a wick against the direction of more than 40% of its range.
  - No trading for the rest of a day once a bar closes beyond the midpoint between the previous day's close and the relevant swing on the other side.
- The 7-hour profile, which must agree with the daily direction:
  - Asia or London: the block dips below the previous block's low and closes back above it (up), or the mirror (down).
  - New York: a bar in the New York block closes back above the low of the Asia and London blocks after the block has dipped below it, on an up bar (up), or the mirror (down). Only if no earlier profile formed that day.
  - The profile is dead once price trades beyond its extreme. An Asia or London profile is also dead once price, in the New York block, trades beyond the midpoint between its extreme and the close of its block (for an Asia profile, the close of the London block).
- Entry, from 1:00 to 11:59 only, one a day for each market, at least 4 bars after the last one:
  - A swing low on 1-hour bars is a bar with a low below the 3 bars on each side.
  - A sweep: a bar trades below the latest swing low not yet used. The lowest low from there on is the sweep low. It is dropped after 20 bars.
  - The trigger: an up bar closes above the open of the most recent run of down bars, as it stood at the sweep low.
  - Buy if the daily direction is up and an up profile is alive. Selling is the mirror in every part.
- Stop at the sweep low (the bar's own low if that is not below the close). Target at twice the risk. Everything is closed at the open of the 15:00 bar.
- A bar that opens beyond the stop or target is closed at its open. A bar that reaches both stop and target counts as a stop.

### Where the lab's version differs from the script on a TradingView chart
Fixed before any result was computed.
- 1-hour bars, for the reason above. A sweep followed by a trigger within 20 bars means within 20 hours here and within 5 hours on a 15-minute chart.
- Entry at the open of the bar after the trigger, as everywhere else in the lab. The script books the trigger bar's close. The stop and target stay where the script put them, and R is measured against the risk the script set.
- A tie between two equal lows or highs does not make a swing. TradingView's own tie rule is not documented, and ties are rare.
- Cost as in the rest of the lab: the market's fee on entry and exit, and 0.02% slippage on a stop. The double-cost check doubles both.
- Gold is read from April 21, 2021, like the other markets, although its file starts earlier.

### Counting
- Results are in R, after costs.
- One number per day: the average across the markets that traded that day. All statistics are on those daily numbers unless stated.
- Period: trades entered from June 1, 2021 to April 20, 2026, as one test. Later bars are the lab's quarantine and are not touched.

### Pass (all must hold)
1. At least 150 traded days.
2. Average above zero, with a t-stat of 2.58 or more.
3. Profit factor of 1.15 or more.
4. Average above zero at double cost.
5. Average above zero on at least 8 of the 15 markets taken alone.
6. A positive total in at least four of the six calendar years 2021 to 2026.
7. Long trades alone and short trades alone each have an average above zero, counting every trade equally.

### Also reported, without changing the verdict
- The same figures before costs, so that a rule killed only by costs can be told from a rule with nothing in it.
- Trades by market group (crypto, forex, indices, gold and oil), by profile (Asia, London, New York), and how trades ended.
- A dry run of the same code on made-up prices with no cost, which should average about zero.

### What a result means
- PASS: one run on the quarantine bars, then the forward watch, then the prop-rules calculator. It is not a reason to trade or to buy a challenge.
- FAIL: the rule is rejected on 1-hour bars. It is not re-run here with other settings, hours or markets.
- A fail here says nothing certain about 15-minute or 5-minute charts. Testing those needs 24-hour data on those bars, which the lab does not hold, and would be a new study.
- This study runs once.

## Study 8: sweep, fair value gap, return to the gap, on 1-minute bars (written November 23, 2026, before this rule was run on any lab data)
One setup from one outside source, in 96 fixed scenarios, so that trying variations cannot turn into tuning. Code: `lab/intraday/sweep_fvg.py`. Data: `lab/data_1m/*_1m_full.csv.gz` and the 1-hour files.

### Where the rule comes from
- A post by @L2WTrades on X, x.com/L2WTrades/status/2124841683896406023, November 23, 2026, sent by Jeff the same day.
- The post's steps: mark a significant high or low on the 4-hour or daily chart; wait for price to trade through it; wait for a fair value gap to form after that; enter when price returns to the gap; stop on the far side of the gap; target the liquidity on the other side, at least 3R away. Trade 9:30 to 12:00 New York time and stop for the day at 12:00.
- It gives no backtest. The author says he makes over $100,000 a month and shows no record. His profile sells a paid community and carries a prop-firm affiliate code.
- The post does not say what makes a high "significant", when the sweep has to happen, which chart the gap is on, where in the gap to enter, or what the target is. Each scenario part below is one reading of one of those.

### Why this is run although sweep rules on 1-hour bars are a dead class
- The built-in `sweep` trigger (480 ideas), the `fair_value_gap` trigger (320 ideas) and study 7 all showed nothing on 1-hour bars.
- The post trades the New York morning on small charts. The lab has 1-minute bars for three index markets in exactly those hours, and none of the three earlier tests could use them. That is different information.
- Jeff approved the 96 scenarios on November 23, 2026, before any of this was computed.

### What has been seen
- The 1-minute files have been used by intraday studies 1 to 6, in both the years before 2024 and the years from 2024. None of that computed this rule.
- Before these rules were written, the session counted bars: every market has at least 27 of the 30 minutes from 9:00 to 9:29 and at least 140 of the 150 minutes from 9:30 to 11:59 on about 99% of days, summer and winter, and 15 hourly bars from 18:00 to 8:59 on about 99% of days. The 1-hour and 1-minute files agree on the high and low of every full hour they share.
- The code was checked on made-up prices only: against a plain bar-by-bar version of the same rule (0 mismatches in 6,250 trades), and in a dry run with no cost.
- The first dry run showed a mistake in a draft rule: an order was cancelled if its 2R or 3R target traded before the fill. With a stop as small as the gap, that target often sits where price already is, so nearly every order was cancelled. The cancel rule now applies only to the opposite-level target. This was fixed on made-up prices, before any lab data was read by the rule.
- No result of any kind was computed on lab data.

### The 96 scenarios
Every combination of six parts. Times are New York time. The high side is described; the low side is the mirror in every part.
- Level, fixed at 17:00 the day before:
  - `pdhl`: the previous trading day's high and low. A trading day runs from 17:00 to 17:00. If the previous day has fewer than 18 hourly bars, there is no level.
  - `swing4h`: the latest 4-hour swing high and low. 4-hour candles start at 17:00, 21:00, 1:00, 5:00, 9:00 and 13:00. A swing high is a candle whose high is above the highs of the 2 candles on each side. It counts only if no later candle up to 17:00 traded above it. The most recent one among the last 30 candles is used. If there is none, there is no level on that side.
- Sweep: the first bar since 18:00 the evening before that trades above the level, by any amount. A touch is not a sweep.
  - `window`: the sweep must come between 9:30 and 11:59. If price traded above the level before 9:30, there is no setup on that side that day.
  - `overnight`: the sweep may come at any time from 18:00 the evening before to 11:59.
- Gap chart: `m1`, 1-minute bars, or `m5`, 5-minute bars counted from 9:00.
  - A down gap is three bars in a row where the low of the first is above the high of the third. The gap is the space between those two prices.
  - It must be at least 0.25 times the average range of the bars before it on the same chart: up to 24 bars, counted from 9:00, at least 6. This is the same floor as the lab's `fair_value_gap` trigger, and it keeps out gaps of a tick or two.
  - The first of the three bars is the bar that holds the sweep, or a later one, and opens at 9:30 or later. The third bar ends by 11:58. A bar with a missing minute cannot be part of a gap.
  - Only the first such gap of the day on each side is used. If its order does not lead to a trade, that side is finished for the day.
- Entry: a sell order placed when the third bar closes. `edge`: at the bottom of the gap (the third bar's high). `mid`: at the middle of the gap.
- Stop: `gapstop`: at the top of the gap (the first bar's low). `sweepstop`: at the highest price since 18:00 the evening before, as it stands when the order is placed.
- Target: `2r` or `3r`: twice or three times the risk below the entry. `opp`: the level of the same kind on the other side (the previous day's low, or the latest 4-hour swing low). With `opp` there is no trade if that level does not exist, has already been touched since 18:00, or is closer than 3 times the risk.
- Names read `level.timing.chart.entry.stop.target`, for example `pdhl.window.m5.edge.gapstop.3r`.

### Fills and exits, the same for every scenario
- The order fills in the first minute, up to 11:59, whose high reaches the order price. It fills at the order price. Not filled by 12:00: cancelled.
- With the `opp` target only: if the target level trades before the fill, or in the fill minute, the order is cancelled.
- If the fill minute's high reaches the stop, the trade is stopped for a loss of 1R. A target cannot be hit in the fill minute.
- After that, minute by minute: a bar that opens beyond the stop or the target is closed at its open. A bar that reaches both counts as a stop. Anything still open is closed at the open of the 15:55 bar, or at the last price before it if that bar is missing.
- One trade per market per day: the first order to fill. If both sides fill in the same minute, the order placed first counts. If they were also placed in the same minute, the day is skipped.
- Cost: 0.005% of price per round trip, as in the other studies on these files. The double-cost check uses 0.01%. In R, the cost is that amount divided by the risk, so a small stop makes it large.
- A day is skipped for a market if it has fewer than 27 of the 30 minutes from 9:00 to 9:29, fewer than 140 of the 150 minutes from 9:30 to 11:59, or fewer than 13 hourly bars from 18:00 to 8:59.
- Minute bars before 9:00 are not used, because the files only have them in winter. Sweeps before 9:00 are read from the 1-hour bars.

### Markets and counting
- Nasdaq 100, S&P 500 and Dow, tested together.
- Results are in R: profit or loss divided by the distance from entry to stop, after costs.
- The three markets move together, so a day counts once: the day's result is the average of the markets that traded that day. All statistics are on those daily averages unless stated.

### Data split
- Screen years: June 1, 2021 to December 31, 2023.
- Confirm years: January 1, 2024 to November 19, 2026, where the 1-hour files end. A scenario sees these only if it passes the screen.

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
7. Long trades alone and short trades alone each have an average above zero, counting every trade equally.

### Also reported, without changing the verdict
- The family in the screen years: how many of the 96 scenarios have an average above zero, after costs and before costs, and the median average, profit factor and cost in R. A real edge shows up across most of the family, not in one scenario.
- For each scenario: the average before costs, the average cost in R, win rate, results by market and year, longs and shorts, and how trades ended.
- The dry run on made-up prices with no cost. With no edge in the prices, every scenario should average about zero.

### What a result means
- CONFIRMED: a forward watch on new 1-minute data, then the prop-rules calculator before any challenge. It is not a reason to trade or to buy a challenge.
- Everything else is rejected. No scenario is re-run with other numbers on these files, and no scenario is added to the family after the data has been seen.
- Fewer than 150 traded days is a reject marked "too few trades". The `window` scenarios need the level untouched all night, so some of them may end this way. That is not evidence for or against them, and loosening the rule to get more trades would be tuning.
- With `m1` gaps and `gapstop`, the risk is about the size of one minute's range. The files cannot show what happened inside a minute, and the fill rules count the unclear minutes against the trade. A reject there is a reject on 1-minute data, not proof about tick data.
- The study covers three index markets in the New York morning. It says nothing about forex, gold or crypto on small charts, which the lab cannot test.
- All 96 results are logged, including the ones that fail. This study runs once.

## Rules version 4: fixes from the audit (written November 23, 2026, before anything was run under it)
An audit on November 23, 2026 checked the lab against an outside backtesting library, planted known edges in shuffled prices, and had an independent reviewer read the code. The arithmetic held up. Four things in the rules made passing much harder than intended, and two checks were weak. This section replaces the parts named below. Everything else in this file stands. Jeff asked for the fixes and a re-run on November 23, 2026.

Version 3 results are kept as they were: `lab/screen/v3/` and `lab/results/v3/`. The version 3 code is commit 413dae0.

### 1. One cost table for every track
The 1-hour tracks charged about five to ten times what the intraday studies charged for the same index, and several times a prop firm's published commission. A no-edge idea started about 3 standard errors below zero on fifteen markets. From version 4 there is one table, in `lab/costs.py`.

| Market | Per side | Round trip at November 2026 prices |
|---|---|---|
| Nasdaq 100, S&P 500, Dow, DAX | 0.005% | Nasdaq 2.8 points, S&P 0.8, Dow 5.2 |
| EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD | 0.006% | EURUSD 1.3 pips |
| EURJPY, GBPJPY | 0.008% | GBPJPY 3.4 pips |
| Gold | 0.006% | 0.48 USD |
| Oil | 0.02% | 3.5 cents |
| Bitcoin | 0.065% | about 97 USD |
| Ether | 0.075% | about 2.90 USD |

- The cost is charged on entry and on exit. A stopped exit pays the per-side cost once more. The double-cost check doubles all of it.
- Position mode trades at the daily close, when spreads are wide, so each change of weight pays twice the per-side cost.
- Where the numbers come from: FTMO US publishes 5 USD per forex lot round trip and 0.0025% per side on expiring index, commodity and metal contracts; its rolling index and oil contracts carry no commission. FTMO publishes 0.0325% per side on crypto. FTMO publishes no typical spreads, so the spread part is an estimate from third-party listings. It is the weakest part of the table.
- Crypto is now dearer than before (0.03% and 0.04% per side under version 3). Everything else is cheaper.
- To correct a number, read the spread and commission off the trading platform. A changed table is a new rules version.
- Intraday studies from here on use this table too. Studies 1 to 8 ran at 0.005% per round trip, which is about half of it for an index. They all failed at the lower cost, so no verdict changes.
- A third-party page says FTMO US offers three US indices, gold, oil, Bitcoin and forex. The DAX and Ether may not be tradable there. They stay in the lab as markets, and this is noted where it matters.

### 2. Every market is read from April 21, 2021
- Gold's file starts in 2009. Under version 3 that made gold 47% of the screen sample for six-market ideas, and 13 of the main track's 16 test years were gold alone.
- From version 4 every track drops bars before April 21, 2021, for gold as for the rest. The main track then has three test years (the blocks starting April 2023, 2024 and 2025).
- Everything from April 21, 2026 on is one quarantine block, including later years.

### 3. Every screened idea runs on all fifteen markets
- Version 3 did this only for triggers registered after November 20, 2026. From version 4 it holds for the whole catalogue.
- "Profitable in at least half of the markets" counts the markets that traded in the window. A market that is closed whenever the idea fires is left out, as in the forward watch.

### 4. Checks repaired
- Position mode, "beats 95% of time-shifted copies": the old copies wrapped weights from the end of a year to its start, so they had already seen the days they were applied to. On no-edge prices trend ideas passed 0% to 3% of the time and contrarian ideas up to 97%. The copies now use weights from 20 or more days earlier, and the real run is scored the same way. Measured on 60 no-edge datasets: 3% to 15% pass, rising with the lookback, the same for trend and contrarian. It should be 5%. The check is now a little easy for slow ideas, which the other checks cover.
- Position mode Sharpe is annualised with the idea's own number of rows a year, not 365.
- Look-ahead checks (`check_trigger.py`, `check_idea.py`, `check_screen.py`): the old ones cut the data at two points and missed a one-bar peek most of the time (17 of 40 and 4 of 40 in the audit). They now also cut right after 20 to 40 bars on which the signal fires. Test files that peek one bar ahead, fire rarely, or use a centred window were caught on every market. All 60 registered triggers, the built-in parts and the eight ideas pass.
- Signals are reduced to -1, 0 or +1 before they are used.
- `lab.py --permtest NAME` works only for an idea that has already been tested, so it cannot give a free look.
- The quarantine block is read once per idea whatever the version: `quarantine_used` is now enforced.
- `screen.py --selftest` draws a sample of the whole catalogue and uses all fifteen markets.

### 5. What the code has always done, now written down
- A gap through the target fills at the target price, not at the better open.
- An opposite signal closes the trade at that bar's close and opens the other way at the next open.
- The six-bar cooldown counts from every signal, including one that was ignored because a trade was open.
- A trade is counted in the window in which it was entered, even if it exits later.
- The random-entry baseline has no cooldown and no opposite-signal exit. On no-edge prices the check passes 2% to 3% of the time, not 5%. It is slightly strict.
- The t-stat treats trades in different markets as independent. Markets that move together make it slightly lenient.

### 6. The bar does not change
- Screen and confirm thresholds are as before. The survivor bar carries on from the 155 ideas sent to confirm under versions 1 to 3, so the first version 4 survivor needs a t-stat of 3.41 and the bar only rises.
- The main track's attempt counter stays at 104. A re-run of an idea tested under version 3 is judged at the bar for attempt 104 and is not a new attempt.
- What the audit found about power still holds: with about 300 trades in the two confirm years, a true profit factor near 1.25 is not caught, and one near 1.45 is caught about half the time. Two unseen years cannot show a small edge. The fixes are more history or a longer forward watch, not a lower bar.

### 7. The re-run
- Main track: the eight ideas tested under version 3 are run once more. The journal marks each "version 4 re-run".
- Screen track: all 17,200 catalogue ideas are screened again into a new log, `lab/screen/log.csv`. A survivor gets its one confirm run.
- 155 ideas had their confirm years read under version 3. If one of them survives the version 4 screen, its confirm run is not a first look. The journal and its confirm file say so.
- The screen years were seen under version 3 by every idea. That is what a screen is for: it only picks who goes to confirm.
- Forward watch: candidates and near misses from version 4 are added. The 20 ideas already watched stay. No forward trade had been counted before this version, so all forward results use the version 4 costs.
- The new-market test and the intraday studies ran once under their own rules and are not re-run.

### What a version 4 result means
- A CANDIDATE is worth watching on new data and nothing more, as before.
- A REJECT now says "not shown to work at roughly real costs", which is a stronger statement than under version 3.
- The cost table is an estimate. A result that depends on it being exactly right is not a result.

## Study 9: the pull to the midnight open (written November 23, 2026, before this rule was run on any lab data)
One claim from one outside source, tested as a claim first and as a trade second. Code: `lab/intraday/midnight_open.py`. Data: `lab/data_1m/*_1m_full.csv.gz` and the 1-hour files. Costs from `costs.py` (rules version 4).

### Where the claim comes from
- A post by @RHerman on X, x.com/rherman/status/2124971266839076991, November 23, 2026, sent by Jeff the same day.
- The claim: on Nasdaq futures, when regular hours open below the midnight open but above the previous day's close, price gets back to the midnight open in 82.5% of sessions. "Almost 300 sessions", 2015 to 2025, the author's own study, not published.
- The post says this is a filter and not an entry signal. It gives no stop, no target and no distances. Its profile sells TradingView indicators.
- The post says "one specific configuration", so other configurations were looked at and this one was picked.

### Why a touch rate is not enough
- How often price reaches a level depends mostly on how near the level is. A market with no pull at all reaches a level 82.5% of the time when it sits about 0.22 of a typical session move away.
- So the study asks a second question the post does not: is the midnight open reached sooner than a made-up level the same distance on the other side of the open? With no pull that is a coin flip.

### What has been seen
- The 1-minute files were used by intraday studies 1 to 8. None of them computed this.
- Before these rules were written, the session counted bars only: of 1,444 days in each index file, about 1,393 have at least 370 of the 390 regular-hours minutes, 1,440 have a 9:30 bar and 1,443 have a midnight hourly bar. No setup was counted and no price was compared.
- The code ran on made-up prices only: 400 days matched a plain second calculation with 0 mismatches. Across 24 made-up markets with no pull, the setup came up on 11% of days, the level was touched on 64% of them, and it was reached before the phantom level on 50.2% of decided days.
- A draft counted a minute that reached both levels as a loss for the claim. That is right for a trade and unfair to the claim, so such a minute now decides nothing in the first-touch count. Changed on made-up prices, before any lab data was read.

### Definitions (New York time)
- Midnight open: the open of the 1-hour bar that starts at 00:00.
- Previous close: the close of the last 1-minute bar from 15:45 to 15:59 on the previous day that has bars.
- Open: the open of the 9:30 one-minute bar.
- The post's setup: previous close below the open, and the open below the midnight open.
- Distance: the midnight open minus the open. The phantom level is the open minus the same distance.
- A day needs a 9:30 bar, at least 370 of the 390 minutes from 9:30 to 15:59, a midnight bar and a previous close. Days run from April 22, 2021 to November 19, 2026.
- There is no screen and confirm split. About 150 setup days are expected and that is too few to cut in two.

### What is measured, on Nasdaq 100
1. Touch rate: the share of setup days on which a bar from 9:30 to 15:59 reaches the midnight open. Set beside the post's 82.5%.
2. First touch: on each setup day, which is reached first, the midnight open or the phantom level. A minute that reaches both, and a day that reaches neither, decide nothing.
3. The trade: buy at the 9:30 open, target the midnight open, stop at the phantom level, so risk and reward are equal. Taken only when the distance is at least 0.04% of price, so that costs are at most a quarter of the risk. A bar that reaches both counts as a stop. A bar that opens beyond the stop or target is closed at its open. Anything still open is closed at the open of the 15:55 bar. Costs: 0.005% of price per side, and once more on a stopped exit. Results in R.

### Verdict (all must hold for SUPPORTED)
1. At least 100 setup days.
2. The midnight open is reached first on more than half of the decided days, with a one-sided binomial p of 0.05 or less.
3. The trade's average is above zero after costs, with a t-stat of 1.65 or more.
4. The trade's average is above zero at double cost.

### Also reported, without changing the verdict
- The same three measures on three other groups of days: open below the midnight open with no gap up; the mirror setup (previous close above the open, open above the midnight open, with everything turned upside down); and open above the midnight open with no gap down. If the setup does no better than "open below the midnight open" alone, the gap adds nothing.
- The setup days split into thirds by distance.
- S&P 500 and Dow. The post is about the Nasdaq, and the three move together, so these are not extra evidence.

### What a result means
- SUPPORTED means the pull showed up in about 150 days of one market, with no unseen data behind it. It earns a forward watch on new 1-minute data. It is not a reason to trade.
- NOT SUPPORTED means the pull did not show on this data. With about 150 days the study can tell 50% from about 60%, not 50% from 55%.
- The lab's data starts in 2021 and is an index price, not the futures contract. The post covers 2015 to 2025. A different touch rate here does not show the post's count is wrong.
- This study runs once. No other distance floor, target or session is tried on these files afterwards.

## Study 10: thirteen claims from one account (written November 23, 2026, before this code was run on any lab data)
Jeff asked for a scan of the whole @RHerman account on X and a test of what can be tested. Code: `lab/intraday/herman_claims.py`. Data: the 1-hour files and `lab/data_1m/*_1m_full.csv.gz`. Costs from `costs.py` (rules version 4).

### What the scan found
- About 1,400 of the account's own posts were read as headlines, back to August 2025. 565 carry a percentage. 29 were opened in full.
- Roughly half the percentage posts are readings from the author's paid indicators ("74% SHORTS today"). The rule behind the number is not published, so they cannot be tested.
- Most of the rest are rates for a price level being reached or left alone, from the author's own unpublished studies of futures from 2015. Since October 2026 these posts add a "distance alone predicts" rate and say "a frequency, not a trade signal. No entries, stops or costs modelled".
- A few are strategy backtests of three weeks to one year. The author calls several of them overfitted or says they fail on a longer chart. One says a plain opening range breakout is break-even (profit factor 1.03 on 2,629 trades), which matches the lab's own opening range studies.
- The rest is arithmetic about win rates and losing streaks. It is correct and it is not a trading rule.
- Not tested, and why: indicator readings (rule not published); posts whose setup uses an unnamed "08:00 overnight filter"; volume profile and VWAP posts (no volume data); news-minute posts (no 8:30 minute data in summer); seasonal posts (5 years is too few); the Russell (no data); a Bollinger band rule on 3 weeks (needs minute bars before 9:00); the midnight open (study 9); the 11:00 candle (the lab's screen already holds inside-bar breakouts).

### What has been seen
- The minute and hourly files were used by studies 1 to 9 and the screen. None of them computed any of the thirteen claims.
- Before these rules were written, the session counted bars per hour of the day in four hourly files and the first and last minute of each day in one minute file. No setup was counted and no price was compared.
- The code ran on made-up prices only. A mixed path (hourly bars before the minute bars start) was compared with a pure minute path on 10,324 setups: 0 mismatches, 609 left undecided by an hourly bar. Over 12 to 24 made-up markets every claim came out near a coin flip (48% to 53% for the claim's side) with trade averages near zero.
- A draft counted an hourly bar that reaches both sides as a loss. On made-up prices that made a no-edge rule lose 0.03R to 0.18R. Such a bar now counts as no trade. For the two claims that only have hourly bars the trade has no target, so the order inside a bar does not matter. Changed on made-up prices, before any lab data was read.

### The one test used for every level claim
- At the check time the price is P and the claim names a level L. The phantom level is the same distance on the other side of P.
- Level reached: the share of setup events where a bar in the window reaches L. Set beside the post's rate.
- First touch: which is reached first, L or the phantom level. A claim that L is taken points to L. A claim that L survives points to the phantom level. A bar that reaches both, and a window that reaches neither, decide nothing. With no edge this is a coin flip.
- The trade: enter at P on the claim's side, target and stop at the two levels, so risk and reward are equal. A bar that opens beyond a level is closed at its open. Anything still open is closed at the last close of the window. Taken only when the distance is at least 0.04% of price. An hourly bar that reaches both sides counts as no trade.
- Claims 5 and 12 only have hourly bars. Their trade is: enter away from the level, stop at the level, no target, out at the last close of the window.
- Costs: the per-side cost in `costs.py`, twice, and once more on a stopped exit. Results in R (the distance to the level).
- Minute bars are used from the first minute bar of the day (8:00 in winter, 9:00 in summer) to 15:59. Hourly bars are used before that and for the 16:00 hour.

### Definitions (New York time)
- Trading day: 18:00 the evening before to 17:00. A day needs at least 20 hourly bars, 5 of the 6 London bars and 6 of the 8 Asia bars. Claims that use minute bars need a 9:30 bar and at least 370 of the 390 minutes from 9:30 to 15:59. Days run from May 3, 2021 to November 19, 2026.
- Asia: 18:00 to 01:59. London: 02:00 to 07:59. Overnight: both. New York session: 08:00 to 15:59. The posts do not give the Asia hours; these are the lab's.
- Yesterday's high, low, open and range: from the previous trading day. Daily open: the 18:00 open. Midnight open: the open of the 00:00 hourly bar. 9:30 open: the open of the 9:30 minute bar.
- "Sweeps": trades beyond. "Hour N" is the hourly candle that starts at N:00.

### The thirteen claims
1. `c01_sweep_reclaim_0800`, Nasdaq. The 8:00 candle trades below the 7:00 low, not above the 7:00 high, and closes above the 7:00 low. Level: the 8:00 high. Check time 9:00, window to 9:59. Claim: taken (post: 85.9%).
2. `c02_hour_sweep_reclaim`, Nasdaq. An hourly candle from 9:00 to 14:00 trades below the prior candle's low (not above its high) and closes back above that low. Level: the candle's high. Window: the next hour. Claim: taken. The same upside down for a swept high (post: 62.2% and 58.6%).
3. `c03_hour_sweep_continue`, Nasdaq. Same candles, but the close is beyond the swept level. Level: the candle's own low (high). Claim: taken again in the next hour (post: 65.5% and 69.5%).
4. `c04_wide_breakout_holds`, Nasdaq. An hourly candle from 9:00 to 14:00 trades above the prior high and closes above it, and its range is more than 1.3 times the median range of that hour on the previous 20 days. Level: the candle's low. Window: the next hour. Claim: survives. The same upside down (post: taken 12.2% and 14.2%).
5. `c05_friday_last_hour`, Nasdaq, Fridays. Level: the 15:00 candle's high. Window: the 16:00 hourly candle. Left out when the 16:00 open is within 0.10 of the median range of the last 24 hourly candles of the level, or beyond it. Claim: survives (post: 84.9%).
6. `c06_red_morning`, Nasdaq. The 11:59 close is below the 9:30 open. Level: the high from 9:30 to 11:59. Check time 13:30, window to 15:59. Claim: survives (post: 85.5%).
7. `c07_asia_low_taken_below_opens`, Nasdaq. London traded below the Asia low, and the 9:30 open is below the midnight open and below the 18:00 open. Level: the Asia high. Check time 9:30, window to 15:59. Claim: survives (post: 74.4%).
8. `c08_dow_expansion_below_pdl`, Dow. London took an Asia side and its last close is beyond that side, and the 9:30 open is below yesterday's low. Level: the overnight high. Check time 9:30. Claim: survives (post: 83.3%).
9. `c09_quiet_london_above_pdh`, Nasdaq. London's range is under 0.7 times the median of the previous 20 London ranges, and the 9:30 open is above yesterday's high. Level: yesterday's New York session low. Check time 9:30. Claim: survives (post: 96.8%).
10. `c10_prior_low_only_bearish_london`, Nasdaq. Yesterday traded below the low of the day before and not above its high, and London closed below its open. Level: the overnight low. Check time 8:00, window to 15:59. Claim: taken (post: 88.8%).
11. `c11_wide_day_untouched`, Nasdaq. Yesterday's range is more than 1.3 times the median range of the 24 days before it, and the overnight session stayed inside yesterday's high and low. Level: the overnight high. Check time 8:00. Claim: taken (post: 86.6%).
12. `c12_gold_below_two_opens`, gold. The 8:00 open is below yesterday's open and below the midnight open, each by more than 0.25 of the median range of the previous 24 days. Level: the overnight high. Window 8:00 to 16:59. Claim: survives (post: 86.8%).
13. `c13_weekday_direction`, Nasdaq. Buy the 9:30 open on Monday, Tuesday and Friday, sell it on Wednesday and Thursday, out at the 15:59 close. The post gives a 1-year backtest and no stop, so none is used. Measured in percent of price after two cost sides.
- Events that share the claim's level but not its setup are reported next to each claim as "other days".

### Verdict, per claim
- First touch supports the claim: the claim's side comes first on more than half of decided events, with a one-sided binomial p of 0.05 / 13 = 0.0038 or less.
- The trade passes: at least 50 trades, average above zero after costs, t-stat of 2.67 or more (5% shared over 13 tests), and average above zero at double cost.
- There is no screen and confirm split. Most claims have 60 to 200 events.

### What a result means
- A trade that passes showed up once on data the claim's author may also have seen (2021 to 2026 is inside the posts' 2015 to 2026). It earns a forward watch on new data. It is not a reason to trade.
- No pass means the lab's translation of the claim made no money here. The posts themselves say they are not trade signals.
- The lab's prices are index and spot prices from 2021, not futures from 2015, and the Asia hours and the "recent median" windows are the lab's guesses. A different rate here does not show a post's count is wrong.
- This study runs once. No other target, stop, window or session definition is tried on these files afterwards.
