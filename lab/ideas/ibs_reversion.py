"""Internal bar strength of the previous day, faded at the next day's first bar (inbox card, book section 4.4)."""
import numpy as np

IDEA = dict(
    name="ibs_reversion",
    source="Kakushadze and Serur, 151 Trading Strategies (2018), section 4.4, https://ssrn.com/abstract=3247865 "
           "(single-market adaptation; the book ranks many ETFs against each other)",
    reason="A close near the day's low is cheap and a close near the high is rich, and short-term extremes tend to revert.",
    loser="Traders who need to sell or buy urgently into the close and pay for immediacy.",
    grid=[{"threshold": 0.1}, {"threshold": 0.2}, {"threshold": 0.3}],
)


def signals(df, p):
    day = df.index.normalize()
    g = df.groupby(day)
    hi, lo, cl = g["high"].max(), g["low"].min(), g["close"].last()
    rng = (hi - lo).replace(0, np.nan)
    ibs = ((cl - lo) / rng).shift(1).reindex(day).to_numpy()     # previous UTC day's IBS
    first = np.r_[True, day[1:] != day[:-1]]                     # first bar of a new day
    ok = first & ~np.isnan(ibs)
    long_ = ok & (ibs < p["threshold"])
    short = ok & (ibs > 1 - p["threshold"])
    return np.where(long_, 1, np.where(short, -1, 0))
