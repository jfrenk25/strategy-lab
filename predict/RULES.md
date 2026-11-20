# Prediction lab rules

A second lab, kept apart from the trading lab in `lab/`. It asks whether prices on Kalshi's yes/no markets are fair, and whether any unfairness is large enough to trade after fees. Nothing here places trades.

Same habits as the trading lab: the rule is written before the data exists, each rule gets one run, every attempt is counted, and results are never tuned afterwards.

## Study 1: back the favourite (written November 20, 2026, before any Kalshi data was downloaded)

### Question
When a market is one day from closing and one side is priced between 80 and 95 cents, does buying that side make money after fees?

### Why it might
Research on betting markets often finds that favourites are slightly underpriced and long shots overpriced. If that holds on Kalshi, the favourite at 80 to 95 cents wins a little more often than its price says.

### Who would be losing
Buyers of cheap long-shot contracts, who pay too much for a small chance of a big payout.

### Sample
- Source: Kalshi's public API (`/markets` with status settled, and `/markets/candlesticks`).
- Markets settled in the most recent whole days that fit the download budget, at most 180 days back and not before Kalshi's historical cutoff.
- Yes/no markets only. Combination ("multivariate") markets are left out.
- The market was open for at least 48 hours and traded at least 500 contracts in total.
- It settled yes or no.

### The snapshot
- Taken from the last hourly candle that ends at or before 24 hours ahead of the market's close, and no earlier than 27 hours ahead.
- Uses that candle's closing bid and ask for YES. A market with no such candle, or with a missing bid or ask, is left out.

### The bet
- The favourite is the side whose mid price is 50 cents or more.
- Buying YES costs the YES ask. Buying NO costs one dollar minus the YES bid.
- A bet is placed only if the favourite's cost is between 0.80 and 0.95 and the bid-ask spread is 5 cents or less.
- One bet per event: the qualifying market with the highest total volume. This stops ten strike prices of one event counting as ten bets.
- The contract is held to settlement. It pays 1 dollar if the favourite wins and 0 if not.
- Fee per contract: 0.07 x cost x (1 - cost), charged on every bet. Kalshi waives or lowers this on some markets, so this is the cautious figure.

### Pass (all must hold)
1. At least 300 bets, spread over at least 60 different closing days.
2. Average profit per contract above zero, with a t-stat of 2.33 or more. The t-stat is computed on daily averages, one number per closing day, so that bets settling together count once.
3. Average profit above zero in the first half of the days and in the second half.
4. Average profit still above zero when every cost is made 1 cent worse.
5. Average profit still above zero after removing the single most profitable series.

### What a result means
- PASS: the rule goes to a forward watch on markets that settle after the download date. It is not a reason to trade yet.
- FAIL: the rule is rejected. It is not re-run with a different price band, horizon or filter on this data.

### The calibration table
- Alongside the test, the lab reports ten price buckets (0 to 10 cents, 10 to 20, and so on) with how often YES won in each.
- The table is a description only. Any new rule suggested by it counts as a new attempt and needs data from after the download date.

## Counting
- Attempts in the prediction lab start at 1 with Study 1. Every later rule raises the bar: required t-stat = the normal quantile at 1 - 0.01 / attempts.
- Every run is logged in `predict/JOURNAL.md`. Entries are never edited or deleted.
