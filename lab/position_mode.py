"""Position mode: for ideas that hold weights across markets day by day (trend, relative value, stat arb).

An idea file sets IDEA["mode"] = "position" and defines:
    def positions(data, p) -> DataFrame of target weights (days x markets), decided at each day's close

`data` is a dict of wide DataFrames (days x markets): data["open"], ["high"], ["low"], ["close"], ["volume"].
A cell is NaN when that market has no bar that day. A weight earns the NEXT day's return.
The engine caps total exposure at 1 (sum of absolute weights) and charges costs on every change.
"""
import os
from statistics import NormalDist
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FEES = {"BTCUSD": 0.0003, "ETHUSD": 0.0004, "XAUUSD": 0.0002, "GBPJPY": 0.00015, "USA30": 0.00025, "DEU30": 0.00025}   # per side
SLIP = 0.0002
QUARANTINE = 2026
MIN_TRAIN_DAYS, MAX_GRID, N_PERM, N_SHIFT = 250, 12, 200, 1000
T = dict(sharpe=0.8, days=500, block_share=0.60, market_share=0.50, shift_pct=95.0, perm_p=0.01, q_days=100)
FIELDS = ("open", "high", "low", "close", "volume")


def load_daily(markets="all"):
    """Daily bars per market. The day rolls at 22:00 UTC (5pm New York) so FX and index sessions stay whole."""
    wide = {f: {} for f in FIELDS}
    for m in FEES:
        path = os.path.join(HERE, "data", f"{m}_1h.csv.gz")
        if not os.path.exists(path) or (markets != "all" and m not in markets): continue
        h = pd.read_csv(path, parse_dates=["time"]).set_index("time")
        day = (h.index + pd.Timedelta(hours=2)).floor("D").tz_localize(None)
        d = h.groupby(day).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"), volume=("volume", "sum"), n=("close", "size"))
        d = d[d["n"] >= 6]                                   # drop stub days with only a few bars
        for f in FIELDS: wide[f][m] = d[f]
    data = {f: pd.DataFrame(wide[f]).sort_index() for f in FIELDS}
    idx = data["close"].index
    block = np.where((idx.month > 4) | ((idx.month == 4) & (idx.day >= 21)), idx.year, idx.year - 1).astype(np.int64)
    return data, block


def net_returns(data, w, cost_mult=1.0):
    """Daily portfolio return and per-market contribution, after costs."""
    close = data["close"]
    ret = close.ffill().pct_change().where(close.notna()).fillna(0.0)            # 0 on days a market does not trade
    w = w.reindex(index=close.index, columns=close.columns).astype(float)
    w = w.where(close.notna()).ffill().fillna(0.0)                               # hold through non-trading days
    w = w.where(close.ffill().notna(), 0.0)                                      # nothing before a market exists
    gross = w.abs().sum(axis=1)
    w = w.div(gross.where(gross > 1.0, 1.0), axis=0)                             # cap total exposure at 1
    cost = pd.Series({m: FEES[m] + SLIP for m in close.columns}) * cost_mult
    contrib = w.shift(1).fillna(0.0) * ret - w.diff().abs().fillna(w.abs()) * cost
    return contrib.sum(axis=1), contrib, w


def _t(r):
    r = np.asarray(r, dtype=float)
    return float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))) if len(r) > 2 and r.std(ddof=1) > 0 else float("nan")


def _walk_forward(mod, idea, data, block, cost_mult=1.0):
    """Per test block, choose the parameter set on earlier blocks only. Returns picks and the per-config results."""
    runs = [net_returns(data, mod.positions(data, p), cost_mult) for p in idea["grid"]]
    blocks = sorted(set(block.tolist())); picks, q_pick = [], None
    for Tb in blocks:
        prior = [b for b in blocks if b < Tb][-3:]
        if len(prior) < 2: continue
        msk = np.isin(block, prior); best, bt = None, -np.inf
        for gi, (r, _, _) in enumerate(runs):
            x = r.to_numpy()[msk]
            if (x != 0).sum() >= MIN_TRAIN_DAYS and _t(x) > bt: best, bt = gi, _t(x)
        if best is None: continue
        if Tb == QUARANTINE: q_pick = (int(Tb), best)
        else: picks.append((int(Tb), best))
    return runs, picks, q_pick


def _oos(runs, picks, block):
    parts, contribs = [], []
    for Tb, gi in picks:
        r, c, _ = runs[gi]; m = block == Tb
        parts.append(r[m]); contribs.append(c[m])
    if not parts: return pd.Series(dtype=float), pd.DataFrame()
    return pd.concat(parts), pd.concat(contribs)


def permute_joint(data, rng):
    """Shuffle days jointly across markets, among days on which the same set of markets trades.
    Cross-market links on a given day survive; patterns through time do not."""
    close = data["close"]; avail = close.notna()
    key = avail.astype(int).astype(str).agg("".join, axis=1).to_numpy()
    lo = {f: np.log(data[f].where(data[f] > 0)) for f in ("open", "high", "low", "close")}
    prev_c = lo["close"].ffill().shift(1)
    gap = (lo["open"] - prev_c).fillna(0.0).to_numpy()
    hi = (lo["high"] - lo["open"]).fillna(0.0).to_numpy(); low = (lo["low"] - lo["open"]).fillna(0.0).to_numpy(); cl = (lo["close"] - lo["open"]).fillna(0.0).to_numpy()
    vol = data["volume"].to_numpy(dtype=float)
    o1 = np.arange(len(close)); o2 = np.arange(len(close))
    for k in np.unique(key):
        ix = np.where(key == k)[0]; ix = ix[ix > 0]              # the first day stays where it is
        if len(ix) > 2:
            o1[ix] = rng.permutation(ix); o2[ix] = rng.permutation(ix)
    gap, hi, low, cl, vol = gap[o1], hi[o2], low[o2], cl[o2], vol[o2]
    gap[0] = 0.0; cl[0] = 0.0
    first = lo["close"].bfill().iloc[0].to_numpy()
    c = first + np.cumsum(gap + cl, axis=0)
    c_prev = np.vstack([first, c[:-1]]); o = c_prev + gap
    mask = avail.to_numpy(); out = {}
    for f, arr in (("open", o), ("high", o + hi), ("low", o + low), ("close", c)):
        out[f] = pd.DataFrame(np.where(mask, np.exp(arr), np.nan), index=close.index, columns=close.columns)
    out["volume"] = pd.DataFrame(np.where(mask, vol, np.nan), index=close.index, columns=close.columns)
    return out


def permutation_p(mod, idea, data, block, actual, n=N_PERM, seed=7):
    rng = np.random.default_rng(seed); beat = 0
    for _ in range(n):
        pdata = permute_joint(data, rng)
        runs, picks, _ = _walk_forward(mod, idea, pdata, block)
        r, _ = _oos(runs, picks, block)
        beat += float(r.sum()) >= actual
    return (beat + 1) / (n + 1)


def run_idea(mod, attempts):
    idea = mod.IDEA
    assert len(idea["grid"]) <= MAX_GRID, "grid too large"
    assert idea.get("reason") and idea.get("loser"), "an idea must state why the edge exists and who loses"
    data, block = load_daily(idea.get("markets", "all"))
    runs, picks, q_pick = _walk_forward(mod, idea, data, block)
    r, contrib = _oos(runs, picks, block)
    runs2, _, _ = _walk_forward(mod, idea, data, block, cost_mult=2.0)
    r2, _ = _oos(runs2, picks, block)                          # same picks, double costs
    x = r.to_numpy(); active = int((x != 0).sum())
    sharpe = float(x.mean() / x.std(ddof=1) * np.sqrt(365)) if len(x) > 2 and x.std(ddof=1) > 0 else float("nan")
    eq = np.cumprod(1 + x) if len(x) else np.array([1.0]); peak = np.maximum.accumulate(eq)
    by_block = {int(b): float(r[block[np.isin(data["close"].index, r.index)] == b].sum()) for b, _ in picks} if len(x) else {}
    by_market = contrib.sum().to_dict() if len(contrib) else {}
    traded = {m: v for m, v in by_market.items() if abs(v) > 1e-12}
    # timing baseline: the same positions, shifted in time inside each test block
    rng = np.random.default_rng(11); shifted = np.zeros(N_SHIFT); close = data["close"]
    ret = close.ffill().pct_change().where(close.notna()).fillna(0.0)
    cost = pd.Series({m: FEES[m] + SLIP for m in close.columns})
    for Tb, gi in picks:
        m = block == Tb; w = runs[gi][2][m].to_numpy(); rr = ret[m].to_numpy(); n = len(w)
        if n < 60: continue
        for k in range(N_SHIFT):
            ws = np.roll(w, rng.integers(20, n - 20), axis=0)
            shifted[k] += float((ws[:-1] * rr[1:]).sum() - (np.abs(np.diff(ws, axis=0)) * cost.to_numpy()).sum())
    need_t = NormalDist().inv_cdf(1 - 0.05 / attempts)
    nb = [int(sum(v > 0 for v in by_block.values())), len(by_block)]; nm = [int(sum(v > 0 for v in traded.values())), len(traded)]
    res = dict(name=idea["name"], mode="position", markets=list(close.columns), days=active, sharpe=sharpe, total=float(x.sum()) if len(x) else 0.0,
               maxdd=float(((eq - peak) / peak).min()), t=_t(x[x != 0]) if active > 2 else float("nan"), need_t=float(need_t), attempts=attempts,
               dbl_total=float(r2.sum()) if len(r2) else 0.0, beats_shifted=float((shifted < x.sum()).mean() * 100) if len(x) else float("nan"),
               blocks_profitable=nb, markets_profitable=nm, by_block={k: round(v, 4) for k, v in sorted(by_block.items())},
               by_market={k: round(float(v), 4) for k, v in by_market.items()}, picks=[[b, idea["grid"][g]] for b, g in picks])
    res["checks"] = {
        f"Sharpe >= {T['sharpe']}": bool(res["sharpe"] >= T["sharpe"]),
        f"days in the market >= {T['days']}": bool(active >= T["days"]),
        "profitable in 60% of test years": bool(nb[1] and nb[0] / nb[1] >= T["block_share"]),
        "half the markets contribute a profit": bool(nm[1] and nm[0] / nm[1] >= T["market_share"]),
        "still profitable at double costs": bool(res["dbl_total"] > 0),
        "beats 95% of time-shifted copies of itself": bool(res["beats_shifted"] >= T["shift_pct"]),
        f"t-stat >= {need_t:.2f} (bar for attempt {attempts})": bool(res["t"] >= need_t),
    }
    res["verdict"] = "REJECT"
    if all(res["checks"].values()):
        res["perm_p"] = float(permutation_p(mod, idea, data, block, res["total"]))
        res["checks"][f"permutation test p <= {T['perm_p']}"] = bool(res["perm_p"] <= T["perm_p"])
    if all(res["checks"].values()) and q_pick is not None:
        q = runs[q_pick[1]][0][block == QUARANTINE].to_numpy()
        res["quarantine"] = dict(days=int((q != 0).sum()), total=float(q.sum()))
        res["verdict"] = "CANDIDATE" if res["quarantine"]["days"] >= T["q_days"] and res["quarantine"]["total"] > 0 else "REJECT (failed quarantine)"
    return res


def journal_lines(res):
    return (f"- Mode: position (daily weights across {len(res['markets'])} markets)\n"
            f"- Out-of-sample: {res['days']} days in the market, Sharpe {res['sharpe']:.2f}, total {res['total']*100:+.1f}%, max drawdown {res['maxdd']*100:.1f}%, t-stat {res['t']:.2f} (needed {res['need_t']:.2f})\n"
            f"- Profitable test years {res['blocks_profitable'][0]} of {res['blocks_profitable'][1]}; markets contributing {res['markets_profitable'][0]} of {res['markets_profitable'][1]}; "
            f"double-cost total {res['dbl_total']*100:+.1f}%; beats {res['beats_shifted']:.0f}% of time-shifted copies\n")


def summary_line(res):
    return (f"{res['verdict']:10s} {res['name']:28s} days {res['days']:5d}  Sharpe {res['sharpe']:.2f}  total {res['total']*100:+6.1f}%  maxDD {res['maxdd']*100:.1f}%  "
            f"t {res['t']:.2f}/{res['need_t']:.2f}  double-cost {res['dbl_total']*100:+.1f}%  beats shifted {res['beats_shifted']:.0f}%  years {res['blocks_profitable']}  markets {res['markets_profitable']}")
