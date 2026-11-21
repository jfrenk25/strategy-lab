"""Alexander's filter rule.

Source: Alexander, "Price Movements in Speculative Markets: Trends or Random Walks", Industrial Management Review 2(2),
1961; tested again in Fama and Blume, "Filter Rules and Stock-Market Trading", Journal of Business 39(1), 1966, and in
the rule set of Sullivan, Timmermann and White, "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap",
Journal of Finance 54(5), 1999.
The rule: buy when the price has risen x percent from a low; hold until it has fallen x percent from a later high,
then sell and go short; cover when it has risen x percent from a later low. Moves smaller than x are ignored.
Note: none of the three sources was opened in the session that wrote this file, so the rule is written from the
published description as recalled.
Kept: the rule's two states and its turning levels measured from the running high or low of the close.
Changed: 1-hour bars. The filter size x is not a fixed percentage: it is k times the market's own average true range
of the last 24 bars, read on the bar that tests it, so one setting fits every market. The event is the bar on which
the state flips: +1 for a rise of x from the low, -1 for a fall of x from the high.
This is not the built-in breakout (a new n-bar high or low): the level here trails the latest swing, with no window.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="alexander_filter",
    source='Alexander, "Price Movements in Speculative Markets: Trends or Random Walks", Industrial Management Review 2(2), 1961; Fama and Blume, "Filter Rules and Stock-Market Trading", Journal of Business 39(1), 1966',
    summary="+1 when the close has risen k average true ranges above its low since the last down signal; -1 when it has fallen k average true ranges below its high since the last up signal.",
    variants=[{"k": 4}, {"k": 8}],
    timed=False,
)


def event(df, p):
    h, l, c = df["high"], df["low"], df["close"]
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    x = (p["k"] * tr.rolling(24).mean()).to_numpy(dtype=float)
    cv = c.to_numpy(dtype=float)
    out = np.zeros(len(cv), dtype=int)
    state, ext = 0, np.nan                                  # state: +1 after an up signal, -1 after a down signal
    lo = hi = np.nan
    for i in range(len(cv)):
        if not x[i] > 0:
            continue
        px = cv[i]
        if state == 0:                                      # before the first signal: track both
            lo = px if not lo == lo else min(lo, px); hi = px if not hi == hi else max(hi, px)
            if px - lo >= x[i]:
                state, ext, out[i] = 1, px, 1
            elif hi - px >= x[i]:
                state, ext, out[i] = -1, px, -1
        elif state == 1:
            ext = max(ext, px)
            if ext - px >= x[i]:
                state, ext, out[i] = -1, px, -1
        else:
            ext = min(ext, px)
            if px - ext >= x[i]:
                state, ext, out[i] = 1, px, 1
    return out
