# Chat studies and their forward watch

Studies 12 to 18 were run in chat sessions, outside the daily run. Their rules, code and results are in the Trading Lab project docs. This folder holds the code for four of them and one forward watch.

| Study | Rule | Verdict | Code here |
|---|---|---|---|
| 12, 13 | Cutler RSI dip-buy on NAS100 (3 ATR stop) | passed as an edge, too slow for a challenge alone | `pair_study.py` (rebuilt, matches Study 13's 118 trades) |
| 14 | Gapline ORB on NAS100 | FAIL (t-stat 2.17, lost money from 2025) | `gapline_orb.py` |
| 16 | MA slope + ATR trail, 15 markets | FAIL (timing guard: beat 63% of slid copies) | `ma_slope.py` |
| 17 | RTH open ATR breakout on NAS100 | PASS, versions A and B | `rth_breakout.py` |
| 18 | Breakout plus dip-buy as a pair | helps a little (about 210 to 162 days to pass) | `pair_study.py` |

Each script has a `selftest` mode. Run them with `python -I`, for example `python -I lab/studies/rth_breakout.py selftest`.

## Forward watch for the three that passed (written November 25, 2026, before any forward bar existed)
Code: `forward_studies.py`. Output: `lab/forward/studies_status.json`. This is separate from `lab/forward.py`, which tracks screen ideas on 1-hour bars and cannot run these rules.

### Who is watched
- `breakout_A`: Study 17 as posted. `breakout_B`: the same with no new entries after two stops in a day.
- `dipbuy`: the Cutler RSI rule with a 3 ATR stop.
- The pair at 0.25% risk a trade on the breakout and 1.5% on the dip-buy rule. It is reported next to the legs and has no verdict of its own.
- The rules are frozen. Nothing in the study scripts may change after the first forward bar.

### What counts
- Only trades entered on or after November 21, 2026, the day after the last bar these studies read.
- Fills and costs are the same as in the studies.

### Verdict (given once per rule)
- The breakout versions: at the first run with 200 or more forward trades. The dip-buy rule: at 40 forward trades, which is about two years.
- **FAILED:** the average is not above zero, or the profit factor is under 1.15, or (breakout only) the profit factor at double cost is not above 1.0.
- **HOLDING UP:** all of those hold, but the t-stat is under the bar.
- **FORWARD PASS:** all of those hold and the t-stat is at or above the normal quantile at 1 - 0.05 / 3, which is 2.13.
- The t-stat is on one number per traded day for the breakout and one per trade for the dip-buy rule.
- Before the count is reached the status is WATCHING and nothing is concluded.

### What to expect
- An edge of the size seen in the studies will probably not reach the t-stat bar in 200 trades. HOLDING UP is the likely best case. The watch is better at showing that a rule has stopped working than at proving it works.
- The watch only moves when `lab/data_1m/NAS100_1m_full.csv.gz` and `lab/data_new/NAS100_1h.csv.gz` are refreshed. The daily run does not refresh the 1-minute file.
- The daily run calls `forward_studies.py` right after `forward.py` (step 7 in `lab/AGENT.md`).
