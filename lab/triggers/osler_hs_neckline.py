"""Head-and-shoulders neckline break (Osler).

Source: C. L. Osler, "Identifying Noise Traders: The Head-and-Shoulders Pattern in U.S. Equities", Federal Reserve Bank
of New York Staff Report 42, February 1998; the same rule on currencies is in Chang and Osler, "Methodical Madness:
Technical Analysis and the Irrationality of Exchange-Rate Forecasts", Economic Journal 109, 1999.
The opening sections of Staff Report 42 were read in the session that wrote this file: three peaks with the middle
one (the head) above the other two; the neckline is the line through the two troughs between them, extended to the
right; the position is taken when the price closes through the neckline after the third peak. Bottoms are the mirror
image. The paper finds the rule loses money on US stocks and treats its users as noise traders.
Not read word for word: the appendix with the full identification rules (symmetry and spacing conditions) and the
size of the zigzag cut-off, which a summary gave as 1.5 to 6 daily standard deviations. Those extra conditions are
not coded, so this trigger accepts more patterns than the paper does.
Kept: peaks and troughs from a zigzag whose cut-off is a multiple of the market's own typical move; head above both
shoulders; neckline through the two troughs; event on the first close through the extended neckline.
Changed: 1-hour bars. The typical move is the standard deviation of the last 500 close-to-close changes. A pattern
is dropped once the zigzag confirms the next turning point. The paper's exit rules are not used (the lab has its own).
This differs from lmw_head_shoulders, which fires when the fifth turning point is confirmed and needs level shoulders.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="osler_hs_neckline",
    source='C. L. Osler, "Identifying Noise Traders: The Head-and-Shoulders Pattern in U.S. Equities", Federal Reserve Bank of New York Staff Report 42, 1998',
    summary="-1 on the first close below the line through the two troughs of a three-peak pattern whose middle peak is highest; +1 for the mirror image.",
    variants=[{"k": 2}, {"k": 4}],
    timed=False,
)


def event(df, p):
    c = df["close"]; cv = c.to_numpy(dtype=float)
    cut = (p["k"] * c.diff().rolling(500).std()).to_numpy(dtype=float)
    out = np.zeros(len(cv), dtype=int)
    T, E, K = [], [], []                        # confirmed turning points: position, price, kind (+1 peak, -1 trough)
    leg, ext, ext_i = 0, np.nan, -1             # current leg (+1 rising, -1 falling) and its running extreme
    armed, t2, e2, slope = 0, 0, 0.0, 0.0       # a live pattern: side, and the neckline through its second trough/peak
    for i in range(len(cv)):
        x = cut[i]
        if not x > 0:
            continue
        px = cv[i]; new = 0
        if leg == 0:
            leg, ext, ext_i = 1, px, i
        elif leg == 1:
            if px >= ext:
                ext, ext_i = px, i
            elif ext - px >= x:
                T.append(ext_i); E.append(ext); K.append(1); new = 1
                leg, ext, ext_i = -1, px, i
        else:
            if px <= ext:
                ext, ext_i = px, i
            elif px - ext >= x:
                T.append(ext_i); E.append(ext); K.append(-1); new = -1
                leg, ext, ext_i = 1, px, i
        if new:
            armed = 0
            if len(E) >= 5:
                a1, b1, a2, b2, a3 = E[-5:]
                if (a2 - a1) * new > 0 and (a2 - a3) * new > 0 and T[-2] > T[-4]:
                    armed, t2, e2 = -new, T[-2], b2
                    slope = (b2 - b1) / (T[-2] - T[-4])
        if armed:
            line = e2 + slope * (i - t2)
            if (px - line) * armed > 0:
                out[i] = armed; armed = 0
    return out
