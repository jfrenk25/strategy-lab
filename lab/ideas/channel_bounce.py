"""Bounce off the floor and ceiling of a closing-price channel (inbox card, book section 3.15)."""
import numpy as np

IDEA = dict(
    name="channel_bounce",
    source="Kakushadze and Serur, 151 Trading Strategies (2018), section 3.15, https://ssrn.com/abstract=3247865",
    reason="Price inside a range tends to bounce off its edges.",
    loser="Breakout traders who enter at the edge of a range that holds.",
    grid=[{"T": 20}, {"T": 55}, {"T": 100}],
)


def signals(df, p):
    c = df["close"]
    floor = c.rolling(p["T"]).min().shift(1)      # lowest close of the previous T bars
    ceil = c.rolling(p["T"]).max().shift(1)       # highest close of the previous T bars
    long_ = c <= floor
    short = c >= ceil
    return np.where(long_, 1, np.where(short, -1, 0))
