"""Three-line break reversal.

Source: S. Nison, "Beyond Candlesticks: New Japanese Charting Techniques Revealed" (Wiley, 1994), the chapter on
three-line break charts. A line chart is built from closes only: a new rising line is drawn when the close exceeds
the top of the last line; a new falling line when it drops below the bottom of the last line; but to turn a run of
rising lines the close must fall below the lowest point of the last three lines (and the mirror for a run of falling
lines). The turning line is the signal.
Note: the book was not opened in the session that wrote this file, so the rule is written from the published
description as recalled.
Kept: the line-building rule and the three-line reversal. The event is the bar whose close draws a reversal line.
Changed: 1-hour bars. Nothing else: the rule has no price scale and no time window, so it is the same on every market.
This is not the built-in breakout (a fixed number of bars): one line can cover one bar or a hundred.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="three_line_break",
    source='S. Nison, "Beyond Candlesticks: New Japanese Charting Techniques Revealed", Wiley, 1994 (three-line break charts)',
    summary="+1 when, during a run of falling lines, the close rises above the highest point of the last three lines; -1 when, during a run of rising lines, it falls below their lowest point.",
    variants=[{"lines": 3}],
    timed=False,
)


def event(df, p):
    cv = df["close"].to_numpy(dtype=float); n = int(p["lines"])
    out = np.zeros(len(cv), dtype=int)
    lo, hi, d = [], [], 0                       # bottoms and tops of the lines so far, and the direction of the last one
    base = np.nan
    for i in range(len(cv)):
        px = cv[i]
        if not px == px:
            continue
        if d == 0:
            if not base == base:
                base = px
            elif px != base:
                lo.append(min(base, px)); hi.append(max(base, px)); d = 1 if px > base else -1
            continue
        if d == 1:
            if px > hi[-1]:
                lo.append(hi[-1]); hi.append(px)
            elif px < min(lo[-n:]):
                hi.append(lo[-1]); lo.append(px); d = -1; out[i] = -1
        else:
            if px < lo[-1]:
                hi.append(lo[-1]); lo.append(px)
            elif px > max(hi[-n:]):
                lo.append(hi[-1]); hi.append(px); d = 1; out[i] = 1
        if len(lo) > 4 * n:
            del lo[:-n], hi[:-n]
    return out
