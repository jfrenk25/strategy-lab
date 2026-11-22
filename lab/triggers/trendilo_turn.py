"""Trendilo turn: a smoothed percent change leaves its own band.

Source: the open-source "Trendilo" indicator on TradingView. Jeff asked on 2026-11-22 for DaviddTech's "Trendhoo"
strategy, which a post by @DaviddDotTech on X named. Trendhoo is a paid, invite-only script and none of its rules are
public, so it cannot be coded. DaviddTech's own strategy list calls it "Trendhoo! v5 (Trendilo)", so this file codes
the public indicator it is named after. Whatever Trendhoo adds on top (confirmation, filters, stops, settings) is
withheld by the vendor and is not here.
How it was read: the indicator's page was not opened, in line with the lab's rule against collecting from
TradingView. The definition below is the indicator's public description as returned by a web search, and the default
settings are from recall.
Definition: pch = percent change of the close over `smooth` bars. avpch = ALMA of pch (Arnaud Legoux moving average:
weights exp(-(i - m)^2 / (2 s^2)) over the last n bars, i = n - 1 for the newest bar, m = offset x (n - 1),
s = n / sigma). rms = mult x square root of the mean of avpch squared over the last n bars. The trend is up while
avpch is above +rms, down while it is below -rms, neutral in between.
Defaults: smooth 1, n 50, offset 0.85, sigma 6, mult 1.
Kept: the indicator and its default settings.
Changed: 1-hour bars. The event is the bar on which the trend turns up (+1) or turns down (-1).
Caution: this is a trend indicator built from price alone, a class the lab's notes say to skip, and it is a cousin of
the built-in zmove (a move that is large against its own history). It was added because Jeff asked for it.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="trendilo_turn",
    source='Trendilo, open-source TradingView indicator (public description via web search, page not opened; defaults from recall); the base of DaviddTech\'s invite-only "Trendhoo" strategy, whose own rules are not public',
    summary="+1 when the smoothed percent change of the close rises above its own root-mean-square band; -1 when it falls below the band on the other side.",
    variants=[{"smooth": 1, "n": 50, "offset": 0.85, "sigma": 6, "mult": 1.0}],
    timed=False,
)


def event(df, p):
    c = df["close"]
    n = int(p["n"])
    pch = (c / c.shift(int(p["smooth"])) - 1.0) * 100.0
    i = np.arange(n); m = p["offset"] * (n - 1); s = n / p["sigma"]
    w = np.exp(-((i - m) ** 2) / (2.0 * s * s)); w /= w.sum()               # the last weight belongs to the newest bar
    avpch = pch.rolling(n).apply(lambda x: float(np.dot(x, w)), raw=True)
    rms = p["mult"] * np.sqrt((avpch ** 2).rolling(n).mean())
    state = np.where(avpch > rms, 1, np.where(avpch < -rms, -1, 0))
    state = np.where(rms.notna().to_numpy(), state, 0)
    prev = np.concatenate(([0], state[:-1]))
    return np.where((state == 1) & (prev != 1), 1, np.where((state == -1) & (prev != -1), -1, 0))
