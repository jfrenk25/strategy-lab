# Strategy lab

A small, strict test bench. It does not find strategies. It rejects them, and logs why.

- `LAB_RULES.md`: the fixed checks every idea must pass.
- `lab.py`: the test runner (walk-forward, realistic fills, random-entry baseline, rising bar, quarantine).
- `position_mode.py`: the second engine, for ideas that hold weights across markets day by day.
- `ideas/`: one file per idea. Copy `_TEMPLATE.py` to add one. `ideas/inbox/` holds raw idea cards.
- `JOURNAL.md`: append-only log of every attempt.
- `state.json`: attempt counter and which ideas have been tested.
- `results/`: full numbers for each run.
- `data/`: 1-hour bars for six markets.
- `AGENT.md`: instructions for an automated agent that feeds the lab.
- `STATE.md`: memory between sessions. `ORCHESTRATOR_BRIEF.md`: opening message for an agent-team session.
- `GROK_SCOUT_PROMPT.md`: prompt for collecting idea cards from X.
- `tools/check_idea.py`: blocks ideas with look-ahead before they are tested.

## Run

```
pip install numpy pandas numba
python lab/lab.py
```

It tests every idea that has not been tested yet and appends the verdicts to the journal.

`python lab/lab.py --permtest NAME 50` runs the permutation test alone as a diagnostic. It logs nothing and does not count as an attempt.

## Reading a verdict
- `REJECT`: failed at least one check. This is the expected result.
- `CANDIDATE`: passed all seven checks and one run on held-back data. Worth watching on new data. Not proven.

Nothing here is investment advice, and nothing in the lab places trades.
