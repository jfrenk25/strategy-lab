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
