# Strategy lab

A strict test bench for trading ideas. It does not find strategies. It rejects them and logs why.

## Quick start

```
pip install -r requirements.txt
python lab/lab.py
```

That tests every idea in `lab/ideas` that has not been tested yet and appends the verdicts to `lab/JOURNAL.md`.

```
python lab/screen.py
```

That registers any new trigger files in `lab/triggers`, screens every untested machine-built idea on older years and gives each survivor one run on years the screen never saw. See "Screen and confirm" and "Growing catalogue" in `lab/LAB_RULES.md`.

```
python lab/forward.py
```

That tracks candidates and near misses on price bars newer than their registration date. It needs fresh bars in `lab/data`. See "Forward watch" in `lab/LAB_RULES.md`.

## How it fits together

| Step | Who | Where |
|---|---|---|
| Collect ideas from X | Grok Bot scout | `lab/GROK_SCOUT_PROMPT.md` |
| Collect ideas from research | `idea-scout` agent | `.claude/agents/idea-scout.md` |
| Hold raw idea cards | you or a bot | `lab/ideas/inbox/` |
| Code one card | `idea-builder` agent | `lab/ideas/` |
| Check for look-ahead, then test once | `lab-verifier` agent | `lab/tools/check_idea.py`, `lab/lab.py` |
| Screen machine-built ideas, confirm survivors | `lab/screen.py` | `lab/screen/log.csv`, `lab/screen/confirm/` |
| Add a trigger to the screen's catalogue | you or an agent | `lab/triggers/`, `lab/tools/check_trigger.py` |
| Watch candidates and near misses on new prices | `lab/forward.py` | `lab/forward/` |
| Watch the three-leg book as one paper prop account | `lab/book/forward_book.py` | `lab/book/` |
| Find papers, write one file each, test what can be tested | paper track | `lab/papers/`, `lab/tools/paper.py`, `lab/tools/check_formula.py` |
| Read the day's summary | you | `lab/briefs/` |
| Remember between sessions | everyone | `lab/STATE.md`, `lab/JOURNAL.md` |

- The rules every idea must pass are in `lab/LAB_RULES.md`. They are fixed.
- To run the agent team, open Claude Code in this folder and paste the brief from `lab/ORCHESTRATOR_BRIEF.md`.
- To add an idea by hand, copy `lab/ideas/_TEMPLATE.py`.

## What a verdict means
- `REJECT`: failed at least one check. This is the expected result.
- `CANDIDATE`: passed every check and one run on held-back data. Worth watching on new data. Not proven.

## Data
`lab/data` holds 1-hour bars for BTCUSD, ETHUSD, XAUUSD, GBPJPY, USA30 and DEU30. Crypto bars come from Binance and Bitstamp public data, the rest from Dukascopy. Check each source's terms before reusing the data elsewhere.

Nothing here is investment advice, and nothing in this project places trades.
