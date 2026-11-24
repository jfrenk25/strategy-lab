"""Turnaround Tuesday: the way Monday went, read at Monday's close.

Source: Larry Williams' "Turnaround Tuesday", as tested in "Turnaround Tuesday: The One-Day Edge That Still Works"
(Alpha Algo Trading Research, algotr.substack.com, 15 April 2026; the free part was read on 2026-11-24). The rule there,
on S&P 500 futures: buy at Monday's close if Monday closed below Friday's close, and sell at Tuesday's close.
Kept: the comparison of Monday's close with Friday's close, read at Monday's close.
Changed: "the close" is one fixed clock hour for every market, the bar that starts at `hour` UTC (20:00, which ends at
the New York stock close in winter), because the lab's markets have no common session. Friday's close is the last bar
at or before the same hour three days earlier. The event is signed the way Monday went (+1 up, -1 down), so the fade
side is the source's rule and its mirror, and the follow side is the opposite bet. The trade leaves by the lab's stop
or target, not at Tuesday's close, so this screens the signal and is not a test of the write-up. The paid part of the
write-up (a filter and a second market) was not seen.
Not the built-in clock (every Monday, no condition) nor session_open (the six bars before a session).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="turnaround_tuesday",
    source='L. Williams, "Turnaround Tuesday"; rule read in "Turnaround Tuesday: The One-Day Edge That Still Works", Alpha Algo Trading Research, https://algotr.substack.com/p/turnaround-tuesday-the-one-day-edge (2026)',
    summary="On the Monday bar that starts at `hour` UTC: +1 if its close is above the close at the same hour on Friday, -1 if below.",
    variants=[{"hour": 20}],
    timed=True,
)


def event(df, p):
    idx = df.index
    close = pd.Series(df["close"].to_numpy(), index=idx)
    close = close[~close.index.duplicated(keep="last")]
    out = np.zeros(len(idx), dtype=int)
    here = np.where((idx.dayofweek == 0) & (idx.hour == int(p["hour"])))[0]
    if len(here) == 0:
        return out
    t = idx[here]
    fri = close.asof(t - pd.Timedelta(hours=72)).to_numpy()          # last close at or before the same hour on Friday
    stamp = pd.Series(close.index, index=close.index).asof(t - pd.Timedelta(hours=72)).to_numpy()
    fresh = pd.notna(stamp) & (pd.DatetimeIndex(stamp) >= (t - pd.Timedelta(hours=96)))   # that bar must be from Friday itself
    r = np.where(fresh, df["close"].to_numpy()[here] / fri - 1.0, 0.0)
    out[here] = np.nan_to_num(np.sign(r)).astype(int)
    return out
