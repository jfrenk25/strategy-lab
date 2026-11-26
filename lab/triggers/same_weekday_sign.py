"""Same-weekday momentum on one market: how this weekday has gone over the past year.

Source: Z. Da and X. Zhang, "Same-Weekday Momentum" (working paper, draft of 30 October 2025; first 18 pages read on
2026-11-26 through a helper at afajof.org, the rest as the helper's summary). Related: M. Keloharju, J. Linnainmaa and
P. Nyberg, "Return Seasonalities", Journal of Finance 71(4), 2016 (from recall, not opened).
As read: a stock's average return on one weekday (say Mondays) over months t-12 to t-2 predicts its return on that
same weekday in month t. The paper ranks US stocks against each other each day, buys the top tenth and sells the
bottom tenth; that made 2.05% a month before costs, and the other weekdays' average predicted nothing.
Kept: the signal (the average return of the same weekday over about eleven months, skipping the latest month) and
its sign.
Changed: one market against its own past, not a ranking across stocks, so this is the time-series cousin of the
paper's rule and not a test of it. The day is the 24 hours from `hour` UTC. The average runs over the same weekday
5 to 52 weeks back (48 weeks, skipping the latest 4); at least 30 of them must have traded. The event fires once a
day at `hour` UTC, on every weekday the market trades: +1 if that average is above zero, -1 if below.
Not the built-in clock (a fixed weekday with no condition) and not same_hour_seasonality (one clock hour over the
last k days): the sign here changes with each weekday's own record over the past year.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="same_weekday_sign",
    source='Z. Da and X. Zhang, "Same-Weekday Momentum", working paper, 2025, https://papers.ssrn.com/abstract=4806275; Keloharju, Linnainmaa and Nyberg, "Return Seasonalities", Journal of Finance 71(4), 2016',
    summary="Once a day at `hour` UTC: +1 if the 24 hours from this hour rose on average on the same weekday 5 to 52 weeks ago, -1 if they fell on average.",
    variants=[{"hour": 0}, {"hour": 13}],
    timed=True,
)

FIRST_WEEK, LAST_WEEK, MIN_WEEKS = 5, 52, 30
D1 = pd.Timedelta(hours=24)


def event(df, p):
    idx = df.index
    out = np.zeros(len(idx), dtype=int)
    here = np.where(idx.hour == int(p["hour"]))[0]
    if len(here) == 0:
        return out
    close = pd.Series(df["close"].to_numpy(), index=idx)
    close = close[~close.index.duplicated(keep="last")]
    stamp = pd.Series(close.index, index=close.index)
    t0 = idx[here]
    total = np.zeros(len(here)); count = np.zeros(len(here))
    for w in range(FIRST_WEEK, LAST_WEEK + 1):
        a = t0 - pd.Timedelta(days=7 * w)                      # the same weekday and hour, w weeks ago
        b = a + D1                                             # 24 hours later: still more than 4 weeks ago
        pa = close.asof(a).to_numpy(); pb = close.asof(b).to_numpy()
        sb = stamp.asof(b)
        traded = (sb.notna() & (sb > a)).to_numpy() & np.isfinite(pa) & np.isfinite(pb)
        r = np.where(traded, pb / np.where(traded, pa, 1.0) - 1.0, 0.0)
        total += r; count += traded
    mean = np.where(count >= MIN_WEEKS, total / np.maximum(count, 1), 0.0)
    out[here] = np.sign(mean).astype(int)
    return out
