"""SuperCycle Surge: three indicators that have to agree.

Source: "SuperCycle Surge Strategy" by DaviddTech, a paid, invite-only TradingView script. Jeff asked for it on
2026-11-22 after a post by @DaviddDotTech on X named it. The code is not public. The vendor's public description
names the parts and says how they combine, and that is all this file uses:
  - baseline: Ehlers' 2-pole Super Smoother filter. Up when the price is above it, down when below.
  - confirmation: Schaff Trend Cycle. Trade only when it points the same way as the baseline.
  - filter: Choppiness Index. No trade while the market is going sideways.
  - risk: a stop 1.5 ATR from the entry, exit when the price or the Schaff cycle turns, or a trailing stop.
How it was read: a web search returned the description, and the script's TradingView page was then opened once. That
page read goes against the lab's rule not to collect from TradingView. It happened before the session had opened the
lab's rules. Nothing else was taken from the page.
Withheld by the vendor: every length, the Choppiness level, what "up" means for the Schaff cycle, the timeframe and
the markets. Each one below is the indicator's own customary default, written from recall, not the vendor's setting:
  - Super Smoother (Ehlers, "Cycle Analytics for Traders", 2013), period 10:
    a = exp(-1.414 pi / N), b = 2 a cos(1.414 pi / N), c2 = b, c3 = -a^2, c1 = 1 - c2 - c3,
    filt = c1 (x + x[1]) / 2 + c2 filt[1] + c3 filt[2].
  - Schaff Trend Cycle (Doug Schaff), 23 / 50 / 10: the MACD line (EMA 23 minus EMA 50) is put through a 10-bar
    stochastic, smoothed with a factor of 0.5, then through a second 10-bar stochastic, smoothed again.
    "Up" is read as: higher than on the previous bar.
  - Choppiness Index (E. W. Dreiss), 14 bars: 100 log10(sum of true ranges / (highest high - lowest low)) / log10(14).
    Its two customary lines are 61.8 (above: sideways) and 38.2 (below: trending). One setting for each reading of
    the vendor's words: "not sideways" (below 61.8) and "trending" (below 38.2).
Kept: the three parts and the rule that all three must agree.
Changed: 1-hour bars. The event is the first bar on which all three agree after a bar on which they did not (+1 for
up, -1 for down). The vendor's stop and exits are not coded because the lab has its own exits.
Caution: this is an indicator mix that follows the trend, a class the lab's notes say to skip (supertrend_flip lost
on both sides). It was added because Jeff asked for it.
"""
import numpy as np
import pandas as pd

TRIGGER = dict(
    name="supercycle_surge",
    source='DaviddTech, "SuperCycle Surge Strategy" (invite-only TradingView script; public description only, settings withheld); parts: Ehlers 2013 Super Smoother, Schaff Trend Cycle, Dreiss Choppiness Index, at their customary defaults',
    summary="+1 on the first bar where the close is above the Super Smoother, the Schaff Trend Cycle is rising and the Choppiness Index is below its line; -1 for the mirror image.",
    variants=[{"ss": 10, "fast": 23, "slow": 50, "cycle": 10, "chop_n": 14, "chop_max": 61.8},
              {"ss": 10, "fast": 23, "slow": 50, "cycle": 10, "chop_n": 14, "chop_max": 38.2}],
    timed=False,
)


def _super_smoother(x, n):
    a = np.exp(-np.sqrt(2.0) * np.pi / n); b = 2.0 * a * np.cos(np.sqrt(2.0) * np.pi / n)
    c2, c3 = b, -a * a; c1 = 1.0 - c2 - c3
    out = np.array(x, dtype=float)
    for i in range(2, len(x)):
        out[i] = c1 * (x[i] + x[i - 1]) / 2.0 + c2 * out[i - 1] + c3 * out[i - 2]
    return out


def _stoch_smooth(x, n, factor=0.5):
    """A stochastic of x over n bars, then the Schaff smoothing: s = s[1] + factor x (k - s[1])."""
    s = pd.Series(x)
    lo = s.rolling(n).min().to_numpy(); rng = s.rolling(n).max().to_numpy() - lo
    out = np.full(len(x), np.nan); prev_k = prev = np.nan
    for i in range(len(x)):
        if not rng[i] == rng[i]:
            continue
        k = 100.0 * (x[i] - lo[i]) / rng[i] if rng[i] > 0 else prev_k      # a flat window keeps the last reading
        if not k == k:
            continue
        prev = k if not prev == prev else prev + factor * (k - prev)
        out[i] = prev; prev_k = k
    return out


def event(df, p):
    h, l, c = df["high"], df["low"], df["close"]
    cv = c.to_numpy(dtype=float)
    base = _super_smoother(cv, int(p["ss"]))
    macd = np.array(c.ewm(span=int(p["fast"]), adjust=False).mean() - c.ewm(span=int(p["slow"]), adjust=False).mean(), dtype=float)
    macd[: int(p["slow"])] = np.nan                                         # let the slow average settle first
    stc = pd.Series(_stoch_smooth(_stoch_smooth(macd, int(p["cycle"])), int(p["cycle"])), index=df.index)
    n = int(p["chop_n"]); pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    span = h.rolling(n).max() - l.rolling(n).min()
    chop = 100.0 * np.log10(tr.rolling(n).sum() / span.where(span > 0)) / np.log10(n)
    calm = (chop < p["chop_max"]).to_numpy()
    rising = (stc > stc.shift(1)).to_numpy(); falling = (stc < stc.shift(1)).to_numpy()
    up = (cv > base) & rising & calm
    dn = (cv < base) & falling & calm
    up_prev = np.concatenate(([False], up[:-1])); dn_prev = np.concatenate(([False], dn[:-1]))
    return np.where(up & ~up_prev, 1, np.where(dn & ~dn_prev, -1, 0))
