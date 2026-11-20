"""Classic channel breakout (seed idea, used to prove the lab runs)."""
import numpy as np

IDEA = dict(
    name="donchian_breakout",
    source="Textbook trend-following rule (Donchian channel)",
    reason="Large moves start with a break of the recent range, and trends persist longer than chance.",
    loser="Traders fading new highs and lows, and hedgers who must trade regardless of price.",
    grid=[{"n": 20}, {"n": 55}, {"n": 100}],
)


def signals(df, p):
    hi = df["high"].rolling(p["n"]).max().shift(1)
    lo = df["low"].rolling(p["n"]).min().shift(1)
    return np.where(df["close"] > hi, 1, np.where(df["close"] < lo, -1, 0))
