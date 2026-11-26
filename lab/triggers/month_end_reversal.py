"""Month-end cash cycle: the move made while institutions sell for month-end cash, turned around.

Source: E. Etula, K. Rinne, M. Suominen and L. Vaittinen, "Dash for Cash: Monthly Market Impact of Institutional
Liquidity Needs", Review of Financial Studies 33(1), 2020. The first half of the paper was read on 2026-11-26 through a
helper (open copy at acris.aalto.fi); the later tables only as the helper's summary.
As read: T is the last trading day of the month. Institutions that need cash at the month end must sell by T-4, so
T-8 to T-4 is a selling window and T-3 to T-1 a rebound: the market's return over T-8 to T-4 and its return over
T-3 to T-1 move opposite ways (correlation -0.54 in 2003 to 2013, on the US market index). From the summary only:
T to T+3 is a buying window, and T+4 to T+8 moves against it, more weakly.
Kept: the paper's windows and the opposite sign.
  leg 1: on day T-3, -1 times the sign of the move over T-8 to T-4.
  leg 2: on day T+4, -1 times the sign of the move over T to T+3.
Changed: the paper reports a correlation, not a trade; the yes-or-no event is the lab's. Trading days are weekdays
(Monday to Friday), so a holiday shifts the count by a day. The move is measured from close to close at the event's
own UTC hour: the last close at or before that hour on T-3 against the one a week (five weekdays) earlier, and for
leg 2 the last close on T+4 against the one at the same hour on day T. The paper covers stock markets; here the same
calendar is applied to all fifteen markets. One event a month for each leg, at a fixed UTC hour.
Not turn_of_month (always +1 on fixed days, whatever came before) and not the built-in clock (weekdays and hours).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="month_end_reversal",
    source='Etula, Rinne, Suominen and Vaittinen, "Dash for Cash: Monthly Market Impact of Institutional Liquidity Needs", Review of Financial Studies 33(1), 2020, https://doi.org/10.1093/rfs/hhz054',
    summary="At 00:00 UTC on the fourth-last weekday of a month: +1 if the five weekdays before it fell, -1 if they rose (leg 1). At 00:00 UTC on the fourth weekday of a month: +1 if the four weekdays before it fell, -1 if they rose (leg 2).",
    variants=[{"leg": 1, "hour": 0}, {"leg": 2, "hour": 0}],
    timed=True,
)


def event(df, p):
    idx = df.index
    leg, hour = int(p["leg"]), int(p["hour"])
    out = np.zeros(len(idx), dtype=int)
    days = idx.normalize()
    if days.tz is not None:
        days = days.tz_localize(None)
    d = days.values.astype("datetime64[D]")
    m0 = d.astype("datetime64[M]")
    first = m0.astype("datetime64[D]")                         # first calendar day of this month
    nxt = (m0 + 1).astype("datetime64[D]")                     # first calendar day of the next month
    weekday = np.is_busday(d)
    if leg == 1:
        left = np.busday_count(d + 1, nxt)                     # weekdays after this day in the month
        on = weekday & (left == 3)                             # T-3
        ref = d - 7                                            # the same weekday a week earlier: start of T-8
    else:
        rank = np.busday_count(first, d) + 1                   # 1 for the first weekday of the month
        on = weekday & (rank == 4)                             # T+4
        ref = np.busday_offset(first, -1, roll="forward")      # last weekday of the month before: day T
    here = np.where(on & (idx.hour == hour))[0]
    if len(here) == 0:
        return out
    close = pd.Series(df["close"].to_numpy(), index=idx)
    close = close[~close.index.duplicated(keep="last")]
    t_ref = pd.DatetimeIndex(ref[here].astype("datetime64[ns]"), tz=idx.tz) + pd.Timedelta(hours=hour)
    now = close.asof(idx[here]).to_numpy()
    then = close.asof(t_ref).to_numpy()
    r = now / then - 1.0
    out[here] = (-np.sign(np.nan_to_num(r))).astype(int)
    return out
