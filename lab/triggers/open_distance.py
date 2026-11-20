"""Fixed levels around the session open.

Idea only, from a page Jeff sent: an indicator that maps reversal levels at set distances from the session open.
The page gives no formula and keeps its code private, so the levels here are our own simple version:
a fraction of the average daily range of the last 14 completed sessions, measured from the 22:00 UTC open.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="open_distance",
    source="https://stopgettingscammed.vercel.app/indicators/vexel-plus/ (concept only: levels at set distances from the session open; formula is ours)",
    summary="+1 when the close first reaches a level a set fraction of the average daily range above the session open, -1 for the level below.",
    variants=[{"frac": 0.5}, {"frac": 1.0}],
    timed=False,
)


def event(df, p):
    idx = df.index
    sess = pd.Series((idx - pd.Timedelta(hours=22)).normalize(), index=idx)       # a session runs 22:00 to 22:00 UTC
    o = df["open"].groupby(sess).transform("first")                                # the session's opening price
    rng = df["high"].groupby(sess).max() - df["low"].groupby(sess).min()           # one range per session
    adr = rng.rolling(14).mean().shift(1)                                          # completed sessions only
    dist = p["frac"] * pd.Series(adr.reindex(sess.to_numpy()).to_numpy(), index=idx)
    up, dn = o + dist, o - dist
    c = df["close"]; pc = c.shift(1); new_sess = (sess != sess.shift(1)).to_numpy()
    hit_up = (c >= up) & ((pc < up) | new_sess)
    hit_dn = (c <= dn) & ((pc > dn) | new_sess)
    return np.where(hit_up, 1, np.where(hit_dn, -1, 0))
