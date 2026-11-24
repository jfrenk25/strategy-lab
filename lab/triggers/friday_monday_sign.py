"""The weekend effect by sign: the way Friday went, read at the start of Monday.

Source: F. Cross, "The Behavior of Stock Prices on Fridays and Mondays" (Financial Analysts Journal, 1973) and
A. Abraham and D. Ikenberry, "The Individual Investor and the Weekend Effect" (Journal of Financial and Quantitative
Analysis, 1994): Monday's return tends to take the sign of the Friday before it, and weak Mondays mostly follow weak
Fridays. Written from the published finding as recalled; the papers were not opened in the session that wrote this file.
Kept: Friday's sign as the whole signal for Monday.
Changed: the papers measure Friday close to Monday close on stocks, which includes a weekend gap nobody can trade. Here
Friday's move is the close of the bar starting at 20:00 UTC on Friday against the last close at or before the same hour
on Thursday, and the event fires on a Monday bar at a fixed UTC hour (00:00, when every lab market is open again, or
13:00, the start of the New York day). The trade leaves by the lab's stop or target.
The event points the way Friday went: follow is the papers' pattern, fade is its opposite.
Not the built-in clock (every Monday, no condition) and not turnaround_tuesday (Monday's own move, read a day later).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="friday_monday_sign",
    source='F. Cross, "The Behavior of Stock Prices on Fridays and Mondays", Financial Analysts Journal 29(6), 1973; A. Abraham and D. Ikenberry, "The Individual Investor and the Weekend Effect", JFQA 29(2), 1994',
    summary="On the Monday bar that starts at `hour` UTC: +1 if Friday rose (20:00 UTC Thursday to 20:00 UTC Friday), -1 if it fell.",
    variants=[{"hour": 0}, {"hour": 13}],
    timed=True,
)

D1 = pd.Timedelta(hours=24)


def event(df, p):
    idx = df.index
    close = pd.Series(df["close"].to_numpy(), index=idx)
    close = close[~close.index.duplicated(keep="last")]
    stamp = pd.Series(close.index, index=close.index)
    out = np.zeros(len(idx), dtype=int)
    here = np.where((idx.dayofweek == 0) & (idx.hour == int(p["hour"])))[0]
    if len(here) == 0:
        return out
    monday = idx[here].normalize()
    fri = monday - 3 * D1 + pd.Timedelta(hours=20)                    # the Friday bar that starts at 20:00 UTC
    thu = fri - D1
    p_fri = close.asof(fri).to_numpy(); p_thu = close.asof(thu).to_numpy()
    s_fri = stamp.asof(fri).to_numpy()
    traded = pd.notna(s_fri) & (pd.DatetimeIndex(s_fri) > thu)        # the market must have traded on Friday
    r = np.where(traded, p_fri / p_thu - 1.0, 0.0)
    out[here] = np.nan_to_num(np.sign(r)).astype(int)
    return out
