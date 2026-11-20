# Strategy lab

A strict test bench for trading ideas. It does not find strategies. It rejects them and logs why.

## Quick start

```
pip install -r requirements.txt
python lab/lab.py
```

That tests every idea in `lab/ideas` that has not been tested yet and appends the verdicts to `lab/JOURNAL.md`.

## How it fits together

| Step | Who | Where |
|---|---|---|
| Collect ideas from X | Grok Bot scout | `lab/GROK_SCOUT_PROMPT.md` |
| Collect ideas from research | `idea-scout` agent | `.claude/agents/idea-scout.md` |
| Hold raw idea cards | you or a bot | `lab/ideas/inbox/` |
| Code one card | `idea-builder` agent | `lab/ideas/` |
| Check for look-ahead, then test once | `lab-verifier` agent | `lab/tools/check_idea.py`, `lab/lab.py` |
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
