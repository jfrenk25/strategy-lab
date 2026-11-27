"""Price leaves the band of its usual move for this time of day.

Source: Zarattini, Aziz and Barbon, "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)",
first version 10 May 2024 (read on 2026-11-27 from the University of St. Gallen repository; paper file `ssrn_4824172`).
The paper's band: for each time of day, take the average over the last 14 days of the absolute move from that day's
open to that time. Draw the upper band that far above the higher of today's open and yesterday's close, and the lower
band that far below the lower of the two. A price outside the band is a move larger than the usual noise for that hour.
Kept: the band formula, the 14 days and the multiplier of 1.
Changed: 1-hour bars instead of half-hour checks on 1-minute data. The lab's markets have no common session, so the
"day" starts at a fixed UTC hour, `anchor` (0 = the UTC day, 13 = the bar in which New York stocks open for most of the
year); both anchors are the lab's choice, not the paper's. The open is the first bar's open at or after the anchor and
the previous close is the last close before it. "The last 14 days" means the last 14 days on which that hour traded.
The event is the bar on which the close first moves outside the band (it was inside on the bar before, or the day has
just begun): +1 above, -1 below. The paper's own exits (a VWAP trailing stop and the session close) are not used; the
screen applies the lab's exits, so this screens the event and is not a test of the paper.
Not `open_distance` (one fixed share of the average daily range for every hour) nor `opening_range_break` (the high
and low of the first bars): here the distance from the open grows through the day with what is usual for each hour.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="noise_band_break",
    source='Zarattini, Aziz and Barbon, "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)", 2024, SSRN 4824172, https://alexandria.unisg.ch/server/api/core/bitstreams/a99aba00-f967-49b3-aceb-f544dc386e0b/content',
    summary="+1 when the close first rises above the day's open (or previous close, if higher) by more than the average move from the open at this hour over the last 14 days; -1 for the mirror below.",
    variants=[{"anchor": 0, "days": 14}, {"anchor": 13, "days": 14}],
    timed=False,
)


def event(df, p):
    idx = df.index
    sess = pd.Series((idx - pd.Timedelta(hours=int(p["anchor"]))).normalize(), index=idx)   # the day runs from the anchor hour
    c = df["close"]
    o = df["open"].groupby(sess).transform("first")                      # today's open
    last = c.groupby(sess).last().shift(1)                                # the close of the day before (a finished day)
    pc = pd.Series(last.reindex(sess.to_numpy()).to_numpy(), index=idx)
    move = (c / o - 1.0).abs()
    hour = pd.Series(idx.hour, index=idx)
    n = int(p["days"])
    sigma = move.groupby(hour).transform(lambda s: s.rolling(n).mean().shift(1))   # earlier days only, same hour
    ub = np.maximum(o, pc) * (1.0 + sigma)
    lb = np.minimum(o, pc) * (1.0 - sigma)
    above = (c > ub).fillna(False)
    below = (c < lb).fillna(False)
    new_day = sess.ne(sess.shift(1))
    was_above = above.shift(1, fill_value=False) & ~new_day
    was_below = below.shift(1, fill_value=False) & ~new_day
    return np.where(above & ~was_above, 1, np.where(below & ~was_below, -1, 0))
