"""The start of the day predicts its last stretch.

Source: Gao, Han, Li and Zhou, "Market Intraday Momentum", Journal of Financial Economics 129(2), 2018. The return from
the previous close to the end of the first half-hour predicts the return of the last half-hour of the same day.
Kept: the first-part return measured from the previous close, acted on shortly before the close. Changed: 1-hour bars
and fixed UTC hours. Variant one uses New York hours (first part ends with the 14:00 bar, event on the 18:00 bar),
variant two London hours (08:00 bar, event on the 14:00 bar). Every market is given the same clock; a day with a
missing bar gives no event. The previous close is the last close at or before the bar two hours after the event hour
on the day before.
Note: the source could not be opened in the session that wrote this file, so the rule is written from the published description as recalled.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="intraday_momentum",
    source='Gao, Han, Li and Zhou, "Market Intraday Momentum", Journal of Financial Economics 129(2), 2018',
    summary="Late in the session, +1 if price rose from the previous close to the end of the session's first hour, -1 if it fell.",
    variants=[{"first": 14, "last": 18}, {"first": 8, "last": 14}],
    timed=True,
)


def event(df, p):
    idx = df.index; c = df["close"]; c = c[~c.index.duplicated(keep="last")]
    out = np.zeros(len(idx), dtype=int)
    at = np.where(idx.hour == int(p["last"]))[0]
    if len(at) == 0:
        return out
    day = idx[at].normalize()
    first_close = c.reindex(day + pd.Timedelta(hours=int(p["first"]))).to_numpy()
    prev_close = c.asof(day - pd.Timedelta(days=1) + pd.Timedelta(hours=int(p["last"]) + 2)).to_numpy()
    with np.errstate(invalid="ignore"):
        out[at] = np.nan_to_num(np.sign(first_close / prev_close - 1)).astype(int)
    return out
