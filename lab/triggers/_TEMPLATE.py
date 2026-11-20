"""Template for a screen trigger. Copy to lab/triggers/NAME.py (lower-case letters, digits, underscores).

A trigger marks bars where something happened: +1 for an event pointing up, -1 for an event pointing down, 0 otherwise.
The screen then tries it both ways (follow and fade), under every regime filter, session filter and exit.

Rules
- Use the current bar and earlier bars only. Never use .shift(-1), centred windows, or whole-series statistics.
- At most 3 parameter sets, numbers only.
- Cite an outside source. Do not design a trigger from this lab's own confirm results.
- Once screen.py has registered the file it must never change. A changed idea is a new file with a new name.
- Set timed=True only if the trigger fires at fixed clock times (then the session filter is skipped).

df has a UTC time index and the columns open, high, low, close, volume (1-hour bars).
Check before running the screen:  python lab/tools/check_trigger.py NAME
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="_TEMPLATE",
    source="Author, title, link",
    summary="One plain sentence: what has to happen for +1 and for -1.",
    variants=[{"n": 24}],
    timed=False,
)


def event(df, p):
    c = df["close"]
    hi = df["high"].rolling(p["n"]).max().shift(1)      # the range of the n bars before this one
    lo = df["low"].rolling(p["n"]).min().shift(1)
    return np.where(c > hi, 1, np.where(c < lo, -1, 0))
