"""One-EMA trend following, equal treatment of markets (Valeyre, "Breaking the Trend", the naive 1/N version).

The paper's rule, per market i and day t (r: daily log return):
    sigma2[t] = (1 - eta) * sigma2[t-1] + eta * r[t]^2                      (Eq. 5)
    phi[t]    = (1 - eta) * phi[t-1] + sqrt(eta) * r[t] / sigma[t-1]        (Eq. 6)
    hat[t+1]  = (1 - rho) * hat[t] + rho * phi[t] / s[t]                    (Eq. 9 with the correlation matrix set to identity)
    position  = hat / sqrt(sum over markets of (hat * s)^2)                 (Eq. 10 with the same simplification)
s is the standard deviation from a 40-day exponential average of squared daily returns; rho = 1/20; eta = 1/120 or 1/100.
The paper's main version replaces the identity by a cleaned correlation matrix ("agnostic risk parity"). That
cleaning step was not read, so this file codes the naive version, which the paper also runs and describes as
"exactly the same computation" with the matrix set to identity.
Lab choices where the paper is silent: the recursions start after 40 returns (sigma2 and s^2 start at the mean of
those 40 squared returns, phi and hat at zero); a market gets no position until it has 250 returns; the constant
volatility target is 2% a year, small enough that the lab's cap on total exposure does not bind (the Sharpe ratio
does not depend on the target).
"""
import numpy as np
import pandas as pd
from scipy.signal import lfilter

IDEA = dict(
    name="valeyre_ema_trend",
    mode="position",
    paper="arxiv_2504_10914",
    source='S. Valeyre, "Breaking the Trend: How to Avoid Cherry-Picked Signals", arXiv:2504.10914 (naive 1/N version, Eqs. 5, 6, 9, 10)',
    reason="The paper's model: prices carry a slow hidden trend that fades at one time scale, which it puts down to investors herding; one exponential average of volatility-scaled returns estimates that trend.",
    loser="The paper names traders who pull prices back towards a fair value while a trend is still running. It does not show that they lose.",
    grid=[{"span": 120}, {"span": 100}],
    markets="fifteen",
)

INIT, WARM, RHO, VOL_SPAN, TARGET = 40, 250, 1.0 / 20, 40, 0.02 / np.sqrt(252)


def _ema(x, alpha, gain, start):
    """y[t] = (1 - alpha) * y[t-1] + gain * x[t], with y before the first x equal to start."""
    y, _ = lfilter([gain], [1.0, -(1.0 - alpha)], x, zi=[(1.0 - alpha) * start])
    return y


def _one_market(close, eta):
    """hat and s for one market on its own trading days."""
    c = close.dropna()
    r = np.log(c / c.shift(1)).to_numpy()[1:]
    hat = np.zeros(len(c)); s = np.full(len(c), np.nan)
    if len(r) > INIT:
        base = float(np.mean(r[:INIT] ** 2)); x = r[INIT:]
        sig2 = np.r_[base, _ema(x ** 2, eta, eta, base)]                    # sig2[j] is known after return INIT + j - 1
        s2 = np.r_[base, _ema(x ** 2, 1.0 / VOL_SPAN, 1.0 / VOL_SPAN, base)]
        prev = np.sqrt(sig2[:-1])
        z = np.divide(x, prev, out=np.zeros_like(x), where=prev > 0)
        phi = _ema(z, eta, np.sqrt(eta), 0.0)
        sd = np.sqrt(s2[1:])
        raw = np.divide(phi, sd, out=np.zeros_like(phi), where=sd > 0)
        h = _ema(raw, RHO, RHO, 0.0)
        h[: max(WARM - INIT, 0)] = 0.0
        hat[1 + INIT:] = h; s[1 + INIT:] = sd
    return pd.Series(hat, index=c.index), pd.Series(s, index=c.index)


def positions(data, p):
    close = data["close"]; eta = 1.0 / p["span"]
    hat, s = {}, {}
    for m in close.columns:
        hat[m], s[m] = _one_market(close[m], eta)
    hat = pd.DataFrame(hat).reindex(close.index).ffill().fillna(0.0)
    s = pd.DataFrame(s).reindex(close.index).ffill()
    risk = np.sqrt(((hat * s) ** 2).sum(axis=1))
    return hat.div(risk.where(risk > 0), axis=0).fillna(0.0) * TARGET


def reference(data, p):
    close = data["close"]; eta = 1.0 / p["span"]
    hat = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    sd = pd.DataFrame(np.nan, index=close.index, columns=close.columns)
    for m in close.columns:
        days = [d for d in close.index if close.at[d, m] == close.at[d, m]]
        rets = [np.log(close.at[days[k], m] / close.at[days[k - 1], m]) for k in range(1, len(days))]
        if len(rets) <= INIT:
            continue
        sigma2 = s2 = sum(x * x for x in rets[:INIT]) / INIT
        phi = h = 0.0
        for k in range(INIT, len(rets)):
            r = rets[k]
            phi = (1 - eta) * phi + (np.sqrt(eta) * r / np.sqrt(sigma2) if sigma2 > 0 else 0.0)     # uses sigma from the day before
            sigma2 = (1 - eta) * sigma2 + eta * r * r
            s2 = (1 - 1.0 / VOL_SPAN) * s2 + (1.0 / VOL_SPAN) * r * r
            h = (1 - RHO) * h + RHO * (phi / np.sqrt(s2) if s2 > 0 else 0.0)
            if k < WARM:
                continue
            hat.at[days[k + 1], m] = h; sd.at[days[k + 1], m] = np.sqrt(s2)
    out = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    last_h = {m: 0.0 for m in close.columns}; last_s = {m: np.nan for m in close.columns}
    for d in close.index:
        for m in close.columns:
            if close.at[d, m] == close.at[d, m]:
                last_h[m] = hat.at[d, m]
                if sd.at[d, m] == sd.at[d, m]:
                    last_s[m] = sd.at[d, m]
        risk = np.sqrt(sum((last_h[m] * last_s[m]) ** 2 for m in close.columns if last_s[m] == last_s[m]))
        if risk > 0:
            for m in close.columns:
                out.at[d, m] = TARGET * last_h[m] / risk
    return out
