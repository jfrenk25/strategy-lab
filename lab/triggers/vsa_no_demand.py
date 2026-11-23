"""No-demand and no-supply bars (Volume Spread Analysis, Tom Williams).

Source: Tom Williams, "Master the Markets" (TradeGuider). The definition was read on 2026-11-23 from two public
descriptions (luxalgo.com/library/concept/no-demand-no-supply-bars and therighttrader.com/learn/volume-and-order-flow/
no-demand-bar), not from the book.
    No demand: the bar closes above the previous close, its range is narrow against recent bars, and its volume is
               below the volume of each of the two bars before it. Read as weakness: -1.
    No supply: the bar closes below the previous close, narrow range, volume below each of the two bars before. +1.
Kept: the three conditions. Changed: "narrow" is not given a number by the sources (one says thresholds vary by
author; the other compares with the last 10 to 20 bars and shows a bar a quarter of the average). Here it means a
range below k times the average range of the 20 bars before it, with k = 1 and k = 0.5.
Left out: the sources say the bar only counts against the right background (after a rally, into resistance) and is
confirmed by the next bar. The screen's own regime filters stand in for the background; no confirmation bar is used.
Not a repeat: vol_spike and high_volume_premium fire on high volume; this fires on low volume with a small bar.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="vsa_no_demand",
    source="Tom Williams, Master the Markets (TradeGuider), no-demand and no-supply bars, as described at https://www.luxalgo.com/library/concept/no-demand-no-supply-bars/ and https://therighttrader.com/learn/volume-and-order-flow/no-demand-bar",
    summary="-1 on an up-close bar with a narrow range and volume below each of the two bars before it (no demand); +1 on the down-close mirror (no supply).",
    variants=[{"k": 1.0}, {"k": 0.5}],
    timed=False,
)


def event(df, p):
    c, v = df["close"], df["volume"]
    rng = df["high"] - df["low"]
    narrow = rng < float(p["k"]) * rng.rolling(20).mean().shift(1)
    quiet = (v < v.shift(1)) & (v < v.shift(2))
    return np.where(narrow & quiet & (c > c.shift(1)), -1, np.where(narrow & quiet & (c < c.shift(1)), 1, 0))
