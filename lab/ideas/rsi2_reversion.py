"""Short-term pullback in the direction of the long trend (seed idea, used to prove the lab runs)."""
import numpy as np

IDEA = dict(
    name="rsi2_reversion",
    source="Textbook short-term mean-reversion rule (2-period RSI with a trend filter)",
    reason="Short, sharp pullbacks inside a longer trend tend to snap back.",
    loser="Traders who sell in panic on a short pullback, and stop orders placed too close.",
    grid=[{"lo": 5, "ma": 200}, {"lo": 10, "ma": 200}, {"lo": 10, "ma": 100}],
)


def signals(df, p):
    d = df["close"].diff()
    up = d.clip(lower=0).ewm(alpha=0.5, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=0.5, adjust=False).mean()
    rsi = 100 - 100 / (1 + up / dn.replace(0, np.nan))
    ma = df["close"].rolling(p["ma"]).mean()
    long_ = (rsi < p["lo"]) & (df["close"] > ma)
    short = (rsi > 100 - p["lo"]) & (df["close"] < ma)
    return np.where(long_, 1, np.where(short, -1, 0))
