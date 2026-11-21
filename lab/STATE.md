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
- Fading the edge of a range on 1-hour bars loses before the idea gets going: channel bounce beat only 4% of random entries. Daily-level rules (pivot, IBS) coded on hourly bars trade thousands of times and costs eat them.
- Formula lists (Alpha158, 101 Alphas) turned into single-market events gave no confirmed idea out of 14 triggers. The few that passed the screen were mostly the follow side in quiet Asian hours, like the older survivors.

## Needs other data (not testable with price bars)
- Order flow and footprint ideas (delta, bid/ask volume).
- Funding and open-interest ideas (tested once outside the lab: rejected, best profit factor 0.99).

## Position mode
- Built 2026-11-19. Ideas that hold weights across markets now run with `mode="position"` (see `_TEMPLATE_POSITION.py`).
- Limit: six markets in three asset classes is a thin basket. Stat arb across 10 or more coins still needs more data.

## Book progress ("151 Trading Strategies")
- Full triage is in `BOOK_INDEX.md`. Use it instead of fetching the book.
- Tested 2026-11-20 from the inbox, all three rejected: 3.14 pivot cross (profit factor 0.88, 6,921 trades), 3.15 channel bounce (0.82, 5,055 trades), 4.4 IBS reversion (0.83, 1,994 trades). The inbox has no unprocessed cards.
- Dead on arrival: 3.11 to 3.13 (moving-average crossovers).
- Tested in position mode 2026-11-19, both rejected: 10.4 time-series momentum (Sharpe 0.05), 10.3 cross-market contrarian (Sharpe 0.13).
- Still open for position mode: 3.8 to 3.10 pairs and cluster reversion, 3.17 nearest neighbours, 3.18 stat arb, 3.20 alpha combination, 8.1 HP-filter trend.

## Screen track
- Built 2026-11-20. `screen.py` builds 4,000 ideas from parts, screens them on trades before April 21, 2024, and gives each survivor one run on April 2024 to April 2026.
- Rules: "Screen and confirm" in `LAB_RULES.md`. Progress: `screen/state.json`. Every screened idea: `screen/log.csv`.
- First batch 2026-11-20: 100 screened, 1 survivor, 0 confirmed. The survivor (24-bar extreme move, follow) had a t-stat of 3.81 on the screen years and -0.25 on the confirm years.
- Second batch 2026-11-20: 100 screened, 0 survivors. Running totals: 200 of 4,000 screened, 1 survivor, 0 confirmed.
- Full catalogue 2026-11-20: all 4,000 screened, 87 survivors, 0 confirmed. Catalogue version 1 is exhausted.
- 67 of the 87 survivors were "follow an extreme move" or "follow a big bar" rules. Treat them as one or two weak ideas, not 67. 67 of the 87 stayed above break-even on the confirm years, but none reached the bar.
- Nearest miss: `breakout_n168.follow.with_trend.asia.stop3_rr2.5` (survivor 3). Confirm years: 289 trades, profit factor 1.42, t-stat 2.78 against a bar of 2.81. Its 24 and 72 bar cousins scored 2.38 and 2.24. It is a REJECT. It passed every other confirm check.
- Do not re-test any survivor on the confirm years: those results have been seen. Only new data (a forward test) can judge them now.
- Growing catalogue built 2026-11-20: new triggers go in `triggers/`, one file each. First one, `open_distance` (levels at a set distance from the session open): 320 ideas, 22 survivors, 0 confirmed. Every survivor was the follow side; the reversal side the source describes passed nothing.
- Running totals 2026-11-20: 4,320 screened, 109 survivors, 0 confirmed. A new survivor now needs a confirm t-stat of about 3.3.
- Forward watch built 2026-11-20 (`forward.py`): 13 near misses registered, forward trades count from 2026-11-21. It shows 0 trades until fresh bars reach `data/`. GBPJPY, USA30 and DEU30 data end on 2026-04-21.
- Missing piece: a price refresh. This workspace cannot reach Binance, Bitstamp or Dukascopy, so new bars have to come from Jeff's PC.
- Data refreshed 2026-11-20 from Jeff's PC (`fetch_lab_data.py` in his `vectorbt research\data` folder): all six markets now run to 2026-11-20. BTC bars are Bitstamp's, ETH bars are Binance's, the rest are Dukascopy BID. The overlap matched the old bars exactly.
- New-market test 2026-11-20: the 13 watched ideas got one run each on nine unseen markets (`data_new/`). 0 of 13 passed. Every one lost money there; the nearest miss made a profit factor of 0.89 over 1,176 trades. The edge seen on the six lab markets did not carry over.
- Rule learned: a rule that only works on the markets it was found on is not an edge. Trend-following survivors here leaned on gold, crypto and DAX trends.
- The forward watch still starts 2026-11-21 and needs another data refresh to move.
- Catalogue version 3 from 2026-11-20: every trigger registered from now on is screened and confirmed on fifteen markets (the six plus `data_new/`). "Half the markets" means 8 of 15. Older ideas are not re-run.
- The forward watch now tracks every watched idea on all fifteen markets.
- Paper track built 2026-11-20: `papers/` holds one YAML file per paper and `papers/seen.csv` logs every abstract looked at. Tools: `tools/paper.py` (validate, verdict, brief) and `tools/check_formula.py`. No paper has been scanned yet.
- Main track from attempt 104: an idea may name any of the fifteen markets; a passing signal idea must also survive the nearby-settings check before quarantine.
- `briefs/DATE.md` is the daily summary.
- On shuffled prices 0 of 400 ideas passed the screen, so a survivor is rarely pure luck in the screen years. It can still fail to carry forward, as the first one did.
- Limit: 1-hour bars and single-market triggers only. Cross-market triggers and other timeframes would be a new catalogue version.

- Trigger batch 2026-11-20 (second run of the day): 25 triggers added, 5,920 ideas screened on fifteen markets, 29 passed the screen, 0 confirmed, 0 candidates.
- Survivors by trigger: a158_vsumd 7, a158_rsqr 4, alpha007 4, realized_skew 3, a158_resi 2, alpha035 2, same_hour_seasonality 2, and 1 each for a158_cntd, a158_shadow, cmf_extreme, td_setup, turn_of_month. The other 13 triggers passed nothing.
- Four near misses (passed every confirm check except the survivor bar) went on the forward watch: `turn_of_month_hour13.follow.against_trend.any.stop3_rr2.5` (confirm t 2.47 against 3.38), `a158_cntd_n20.follow.high_vol.asia.stop3_rr1.5` (2.36), `alpha007_rank0.9.follow.low_vol.asia.stop3_rr2.5` (1.89), `a158_vsumd_n20.follow.low_vol.asia.stop3_rr2.5` (1.89). All four are REJECTs.
- Running totals 2026-11-20 (from `screen/state.json`): catalogue version 3, 10,240 screened, 138 survivors, 0 confirmed, 0 candidates. The next survivor needs a confirm t-stat of about 3.38.
- Forward watch 2026-11-20: 17 ideas watched, 0 forward trades. Price data ends 2026-11-20 05:00 UTC (ETHUSD 2026-11-19 23:00) and the watch starts 2026-11-21, so nothing can move until the next data refresh.
- Second trigger batch 2026-11-20 (run on Jeff's request, on top of the daily 25): 8 triggers added, 1,280 ideas screened, 4 passed the screen (all `cl_three_soldiers`), 0 confirmed, 0 candidates. No new near miss, so the forward watch stays at 17 ideas with 0 forward trades.
- Running totals after it (from `screen/state.json`): 11,520 screened, 142 survivors, 0 confirmed, 0 candidates. The next survivor needs a confirm t-stat of about 3.39.

## Trigger sources (where each list stands)
Caution for all 25 triggers of 2026-11-20: the session could not open any web page (page reads needed an approval nobody was there to give). Every formula was written from the published definition as recalled, and each file says so. The files are registered and must not be edited: a correction is a new trigger with a new name.
Spot check done later on 2026-11-20, when pages could be opened:
  - 101 Formulaic Alphas: #7, #12, #21, #23, #35, #46 and #54 were compared with the paper's appendix (arXiv 1601.00991v1). All seven match.
  - Alpha158: KUP, KLOW, BETA, RSQR, RESI, CORR, CORD, CNTD and VSUMD were compared with a third-party listing of the factor formulas (bigquant.com wiki). All match. Qlib's own file still could not be opened.
  - `td_setup` differs from the freqtrade file: the strategy buys only when the count is 9 or more AND the bar's low is below the lows of the bars at counts 6 and 7, and its sell side is looser. Our trigger uses the plain count of nine on both sides. It is DeMark's basic setup, not the strategy's exact rule.
  - Not yet checked against a source: `cmf_extreme` and the nine research triggers.
  - Page reads only work for links that a web search returned in the same session. Search first, then open the result.
- Qlib Alpha158: list worked through once, 7 triggers taken. Taken: KUP and KLOW (`a158_shadow`), RSQR with BETA's sign (`a158_rsqr`), RESI (`a158_resi`), CORR (`a158_corr`), CORD (`a158_cord`), CNTD (`a158_cntd`), VSUMD (`a158_vsumd`). Skipped as repeats of built-ins or dead classes: KMID, KLEN, KMID2, KSFT, KSFT2 (big_bar), ROC and BETA alone (zmove), MA (moving-average crossover), STD (squeeze), MAX, MIN, QTLU, QTLD, RANK, RSV, IMAX, IMIN, IMXD (breakout family), CNTP, CNTN (halves of CNTD), SUMP, SUMN, SUMD (RSI), VMA, VSTD, WVMA, VSUMP, VSUMN (vol_spike family or no direction). KUP2 and KLOW2 are the same shadows on a different scale. The list is used up.
- 101 Formulaic Alphas: list worked through once, 7 triggers taken: Alpha#7, #12, #21, #23, #35, #46 (also covers #49 and #51), #54. Skipped: every alpha that needs vwap, market cap or industry groups; every alpha whose core is a rank across stocks; #9 and #10 (streak), #19 and #24 (zmove), #20 (gap), #33 and #101 (bar body, big_bar family), #6, #14, #22, #26, #40, #44 (price-volume correlation, same idea as a158_corr), #43 and #39 (same parts as #7). Still open if wanted: #8, #30, #52, #53. Otherwise the list is used up.
- freqtrade-strategies: 2 triggers taken: TDSequentialStrategy (`td_setup`), TechnicalExampleStrategy's Chaikin Money Flow (`cmf_extreme`). Skipped: everything built on EMA, MACD, RSI, stochastic, CCI, MFI, ADX and DI crossings, Supertrend, parabolic SAR, heikin-ashi or Bollinger-plus-RSI mixes (indicator crossovers, a dead class); HourBasedStrategy (clock); strategies with fixed percent thresholds (BinHV45, ClucMay72018, Low_BB). The folder listing could not be read, so files added to the collection recently have not been looked at. Start there next time.
- Published research and books, 9 triggers taken: Gervais, Kaniel and Mingelgrin 2001 (`high_volume_premium`); Heston, Korajczyk and Sadka 2010 (`same_hour_seasonality`); Amaya and others 2015 (`realized_skew`); Osler 2003 (`round_number_cross`); Gao, Han, Li and Zhou 2018 (`intraday_momentum`); Crabel 1990 and Zarattini and Aziz 2023 (`opening_range_break`); Crabel 1990 (`crabel_idnr`); Williams 1999 (`smash_day`); Lakonishok and Smidt 1988, McConnell and Xu 2008 (`turn_of_month`).
- Second batch 2026-11-20, 8 triggers: Caginalp and Laurent 1998 (`cl_three_inside`, `cl_three_outside`, `cl_morning_star`, `cl_three_soldiers`; definitions read from the paper), Chesler 2004 (`hikkake`; rules read from Wikipedia), Amihud 2002 (`amihud_illiq`; from recall), LeBaron 1992 (`serial_corr`; from recall, and the trading rule is ours), 101 Alphas #8 (`alpha008`; read from the paper). Alpha#53 was left out: it is the close-location idea of #54 again. That leaves #30 and #52 in the 101 list.
- Considered and left out: outside bars and engulfing bars (close to big_bar), pin bars (same as a158_shadow), turtle soup and springs (sweep), VWAP cross and OBV cross (crossovers), Kaufman efficiency ratio (same idea as a158_rsqr), pocket pivots (vol_spike family), pivot levels (the class failed in the main track today). The book in `BOOK_INDEX.md` has no single-market events left.
- `same_hour_seasonality` needed one fix before registration: the first version counted calendar days, so it never fired on markets that close at weekends. It now counts the last k days on which that hour traded.
- Ideas for next time, not yet used: Lo, Mamaysky and Wang 2000 chart patterns, fair value gaps, variance-ratio regimes, overnight against intraday returns (needs session times per market).

## Next
- The inbox is empty. Fill `ideas/inbox/` from "151 Trading Strategies" (see `AGENT.md`) and from the X scout prompt in `GROK_SCOUT_PROMPT.md`.

## Last session
2026-11-20 (two runs) · 3 inbox ideas tested in the main track, 3 rejected (attempts now 103) · 33 triggers added (25 + 8), 7,200 ideas screened, 33 passed the screen, 0 confirmed, 0 candidates · forward watch 17 ideas, 0 forward trades
