"""The coming hour moved the same way on each of the last k days.

Source: Heston, Korajczyk and Sadka, "Intraday Patterns in the Cross-Section of Stock Returns", Journal of Finance
65(4), 2010. A stock's return in a given half-hour tends to repeat in the same half-hour on later days.
Kept: the idea that the same clock interval on earlier days predicts the coming one. Changed: one market, 1-hour bars,
and a yes-or-no rule: the event fires when the clock hour that comes next had the same open-to-close direction on each
of the last k days on which that hour traded, so weekends and closed hours are handled without assumptions.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="same_hour_seasonality",
    source='Heston, Korajczyk and Sadka, "Intraday Patterns in the Cross-Section of Stock Returns", Journal of Finance 65(4), 2010',
    summary="+1 when the clock hour that follows this bar rose on each of the last k days, -1 when it fell on each of them.",
    variants=[{"k": 5}, {"k": 8}],
    timed=False,
)


def event(df, p):
    k = int(p["k"]); idx = df.index; hour = idx.hour
    sgn = pd.Series(np.sign((df["close"] - df["open"]).to_numpy()), index=idx)
    sgn = sgn[~sgn.index.duplicated(keep="last")]
    out = np.zeros(len(idx), dtype=int)
    for target in range(24):
        past = sgn[sgn.index.hour == target]                  # every earlier bar at the clock hour that comes next
        here = np.where(hour == (target - 1) % 24)[0]
        if len(past) < k or len(here) == 0:
            continue
        ups = (past > 0).astype(float).rolling(k).sum() == k
        dns = (past < 0).astype(float).rolling(k).sum() == k
        run = pd.Series(np.where(ups, 1, np.where(dns, -1, 0)), index=past.index)
        out[here] = np.nan_to_num(run.asof(idx[here]).to_numpy()).astype(int)     # last value at or before this bar
    return out
