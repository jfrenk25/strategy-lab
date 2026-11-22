"""The way the coming 12-hour session went a day earlier.

Source: Z. Wu and E. Pinsky, "On the Performance of Lagged Momentum and Reversal Strategies Across Daytime and
Overnight Sessions in Bitcoin and Ethereum Cryptocurrencies", Journal of Risk and Financial Management 19(9), 692,
2026 (read on 2026-11-22; lab paper file jrfm_19_9_692). The paper cuts each day into two 12-hour sessions and sets
the position for a session from the sign of the return of the same session one day earlier: with it ("Momentum") or
against it ("Reversal"). Its picks were sessions starting at 08:00 and 20:00 UTC for bitcoin and 05:00 for ether.
Kept: the 12-hour session, the one-day lag, the sign as the whole signal, and the paper's three start hours.
Changed: this is an event for the screen, so the trade leaves by the lab's stop or target and not at the session's
end. That makes it the lab's own screen of the signal, not a test of the paper. On a market that was closed for the
whole of the lagged window (a Monday morning in forex, for example) nothing fires.
The event points the way the lagged session went: the follow side is the paper's Momentum, the fade side its Reversal.
Not the built-in session_open, which reads the six bars just before the open, nor same_hour_seasonality, which needs
one clock hour to repeat for k days.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="lagged_session_sign",
    source='Wu and Pinsky, "On the Performance of Lagged Momentum and Reversal Strategies Across Daytime and Overnight Sessions in Bitcoin and Ethereum Cryptocurrencies", J. Risk Financial Manag. 19(9), 692, 2026, https://www.mdpi.com/1911-8074/19/9/692',
    summary="At the bar that closes at hour h UTC: +1 if the 12 hours starting at h rose a day earlier, -1 if they fell.",
    variants=[{"h": 8}, {"h": 20}, {"h": 5}],
    timed=True,
)

H1, H12, H24 = pd.Timedelta(hours=1), pd.Timedelta(hours=12), pd.Timedelta(hours=24)


def event(df, p):
    idx = df.index
    close = pd.Series(df["close"].to_numpy(), index=idx)
    close = close[~close.index.duplicated(keep="last")]
    stamp = pd.Series(close.index, index=close.index)
    out = np.zeros(len(idx), dtype=int)
    here = np.where(idx.hour == (int(p["h"]) - 1) % 24)[0]            # this bar closes at hour h; the entry is the open of hour h
    if len(here) == 0:
        return out
    t = idx[here] + H1                                                 # the session about to start
    last = t - H24 + H12 - H1                                          # last bar of the same session a day earlier
    before = t - H24 - H1                                              # last bar before that session began
    p_end = close.asof(last).to_numpy(); p_start = close.asof(before).to_numpy()
    seen = stamp.asof(last).to_numpy()                                 # the bar actually found for the session's end
    traded = pd.notna(seen) & (pd.DatetimeIndex(seen) >= (t - H24))    # it must lie inside the lagged session
    r = np.where(traded, p_end / p_start - 1.0, 0.0)
    out[here] = np.nan_to_num(np.sign(r)).astype(int)
    return out
