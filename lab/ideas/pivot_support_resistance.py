"""Cross of the previous day's pivot point (inbox card, book section 3.14)."""
import numpy as np

IDEA = dict(
    name="pivot_support_resistance",
    source="Kakushadze and Serur, 151 Trading Strategies (2018), section 3.14, https://ssrn.com/abstract=3247865",
    reason="Not stated in the book. Common explanation: many traders watch the same daily levels, so price reacts around them.",
    loser="Traders who fade a move through a widely watched level.",
    grid=[{"levels": "prev_utc_day"}],
)


def signals(df, p):
    day = df.index.normalize()
    g = df.groupby(day)
    daily = (g["high"].max() + g["low"].min() + g["close"].last()) / 3.0
    pivot = daily.shift(1).reindex(day).to_numpy()          # previous UTC day's (H + L + C) / 3
    c = df["close"].to_numpy()
    pc = np.roll(c, 1); pc[0] = np.nan
    ok = ~np.isnan(pivot) & ~np.isnan(pc)
    long_ = ok & (c > pivot) & (pc <= pivot)
    short = ok & (c < pivot) & (pc >= pivot)
    return np.where(long_, 1, np.where(short, -1, 0))
