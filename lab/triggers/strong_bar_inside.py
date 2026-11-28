"""A strong one-way bar followed by a small bar that stays inside it.

Source: S. Ermolov, "TEST #002 Inside Bar", MQL5 traders' blog, 11 June 2026, https://www.mql5.com/en/blogs/post/771362
(read on 2026-11-28 through the page-reading helper). The post tests a continuation idea on 1-hour and 15-minute bars
of EURUSD, gold and the S&P 500: a "main bar" that moves strongly one way, then a "signal bar" that forms inside the
main bar's range, then a pending order to trade a break of the main bar in the direction of its close.
Kept: the two-bar shape and the numbers the post reports as its best: main bar body about 80% of its range, main bar
range at least about 0.6 ATR, signal bar range about 50% of the main bar's range or less, and the direction (the way
the main bar closed).
Changed: the event is marked at the close of the signal bar, so the screen enters at the next open; the post waits for
a break of the main bar with a pending order that lives 1 to 15 bars. The post's own stop and target (fractions of the
main bar's range, mostly not stated) are not used; the screen applies the lab's exits. The ATR length is not given in
the text read, so the 24-bar average true range of the bars before the main bar is the lab's choice. The post's numbers
are its author's optimised values on 2020 to 2026 data, so this screens the event and is not a test of the post.
Not `big_bar` (one wide bar closing near its end, no second bar), not `crabel_idnr` (an inside bar that is the
narrowest of n, direction from the later break) and not `hikkake` (a failed break of an inside bar).
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="strong_bar_inside",
    source='S. Ermolov, "TEST #002 Inside Bar", MQL5 traders\' blog, 11 June 2026, https://www.mql5.com/en/blogs/post/771362',
    summary="The previous bar had a body of at least 80% of its range and a range of at least 0.6 ATR, and this bar stays inside it with half its range or less: +1 if the previous bar closed up, -1 if it closed down.",
    variants=[{"body": 0.8, "inside": 0.5, "atr": 0.6}],
    timed=False,
)


def event(df, p):
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    rng = h - l
    prev_close = c.shift(1)
    true_range = pd.concat([rng, (h - prev_close).abs(), (l - prev_close).abs()], axis=1).max(axis=1)
    atr = true_range.rolling(24).mean()

    # the main bar is the bar before this one; its ATR uses only bars before it
    m_rng = rng.shift(1)
    m_body = (c - o).shift(1)
    m_atr = atr.shift(2)
    strong = (m_rng > 0) & (m_body.abs() >= p["body"] * m_rng) & (m_rng >= p["atr"] * m_atr)

    # this bar is the signal bar: inside the main bar and small
    inside = (h <= h.shift(1)) & (l >= l.shift(1)) & (rng <= p["inside"] * m_rng)

    setup = strong & inside
    return np.where(setup & (m_body > 0), 1, np.where(setup & (m_body < 0), -1, 0))
