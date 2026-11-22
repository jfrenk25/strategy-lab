"""SuperTrend flip.

Source: the SuperTrend indicator, credited to Olivier Seban, as it is commonly published. Jeff supplied a link to a
public TradingView script (tradingview.com/script/4UaDaKOX-SuperTrend) on 2026-11-21. That page was not opened, in
line with the lab's rule against collecting from TradingView; the rule below is the indicator's standard public
definition, written from recall, with its usual default settings (ATR over 10 bars, multiplier 3).
Definition: mid = (high + low) / 2. Basic bands: mid + m x ATR and mid - m x ATR. The upper band may only move down
while the previous close is at or below it, and the lower band may only move up while the previous close is at or
above it. The trend turns up when the close moves above the upper band and down when it moves below the lower band.
Kept: the bands, the ratchet and the flip. ATR is Wilder's smoothed average of the true range.
Changed: 1-hour bars. Only the flip is an event (+1 up, -1 down); the indicator's use as a trailing stop is not coded
because the lab has its own exits.
Caution: this is an indicator rule of the kind the lab's notes call a dead class, and it is close to the registered
alexander_filter trigger (a turn of k ATRs from a running extreme). It was added because Jeff asked for it.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="supertrend_flip",
    source="SuperTrend indicator (credited to Olivier Seban), standard public definition; link supplied by Jeff: tradingview.com/script/4UaDaKOX-SuperTrend (not opened)",
    summary="+1 when the close moves above the trailing upper band (bar midpoint plus 3 average true ranges, only allowed to fall); -1 when it moves below the trailing lower band.",
    variants=[{"period": 10, "mult": 3}],
    timed=False,
)


def event(df, p):
    h = df["high"].to_numpy(dtype=float); l = df["low"].to_numpy(dtype=float); c = df["close"].to_numpy(dtype=float)
    n = int(p["period"]); m = float(p["mult"])
    out = np.zeros(len(c), dtype=int)
    atr = np.nan; tr_sum = 0.0; up = dn = np.nan; trend = 0
    for i in range(1, len(c)):
        tr = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
        if i <= n:
            tr_sum += tr
            if i < n:
                continue
            atr = tr_sum / n                                    # the first value is a plain average of n true ranges
        else:
            atr = (atr * (n - 1) + tr) / n                      # Wilder's smoothing
        mid = (h[i] + l[i]) / 2.0
        b_up, b_dn = mid + m * atr, mid - m * atr
        new_up = b_up if not up == up or b_up < up or c[i - 1] > up else up
        new_dn = b_dn if not dn == dn or b_dn > dn or c[i - 1] < dn else dn
        if up == up:
            if trend <= 0 and c[i] > up:                        # judged against the band as it stood before this bar
                out[i] = 1 if trend != 0 else 0; trend = 1
            elif trend >= 0 and c[i] < dn:
                out[i] = -1 if trend != 0 else 0; trend = -1
        up, dn = new_up, new_dn
    return out
