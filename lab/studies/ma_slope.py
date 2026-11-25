"""Study 16: MA slope + ATR trail on daily bars. Rules: claude/ma-slope-rules-2026-11-25.md (written before this ran).

Usage: python -I ma_slope.py MODE [LAB_DIR] [OUT_JSON]
  MODE  selftest   hand-built bars for the exit logic (no data read)
        dryrun     the same code on made-up prices with no trend
        lookahead  trades from a cut-off copy must match the full run up to the cut (reads prices, prints no results)
        run        the study (once)
"""
import json
import os
import sys

import numpy as np
import pandas as pd

NS, KS, ATR_N = (30, 50, 80, 100), (1.5, 2.0, 3.0), 14
START, END_UTC = "2021-04-21", "2026-04-20 21:00"        # last bar read ends 17:00 New York on April 20, 2026
FILES = {"BTCUSD": "data", "ETHUSD": "data", "XAUUSD": "data", "GBPJPY": "data", "USA30": "data", "DEU30": "data",
         "SPX500": "data_new", "NAS100": "data_new", "USOIL": "data_new", "EURUSD": "data_new", "GBPUSD": "data_new",
         "USDJPY": "data_new", "AUDUSD": "data_new", "USDCAD": "data_new", "EURJPY": "data_new"}
NEED = dict(days=150, t=2.58, pf=1.15, markets=8, years=4, versions=8, guard=95.0)
N_COPIES, FIN = 1000, 0.0002


def sessions(ts, o, h, l, c):
    """Group hourly bars into days that run 17:00 to 17:00 New York. Returns daily arrays and each day's bar range."""
    day = (pd.DatetimeIndex(ts) + pd.Timedelta(hours=7)).normalize()
    codes, uniq = pd.factorize(day)                    # bars are sorted, so codes rise
    first = np.r_[0, np.flatnonzero(np.diff(codes)) + 1]
    last = np.r_[first[1:], len(codes)]
    D = {"day": pd.DatetimeIndex(uniq), "o": o[first], "c": c[last - 1],
         "h": np.maximum.reduceat(h, first), "l": np.minimum.reduceat(l, first)}
    return D, first, last


def indicators(D, n):
    c, h, l = D["c"], D["h"], D["l"]
    sma = pd.Series(c).rolling(n).mean().to_numpy()
    pc = np.r_[np.nan, c[:-1]]
    tr = np.where(np.isnan(pc), h - l, np.maximum(h, pc) - np.minimum(l, pc))
    atr = pd.Series(tr).ewm(alpha=1.0 / ATR_N, adjust=False, min_periods=ATR_N).mean().to_numpy()
    return sma, atr


def simulate(D, first, last, bo, bl, n, k, cost):
    """Buy-side trades for one market and one version. Returns (trades, held) where held[d] is True if a trade is open at day d's close."""
    sma, atr = indicators(D, n)
    c, nd = D["c"], len(D["c"])
    held = np.zeros(nd, bool)
    trades, open_left = [], 0
    up = np.r_[False, sma[1:] > sma[:-1]]                # NaN compares False
    down = np.r_[False, sma[1:] < sma[:-1]]
    t = n + 1
    while t < nd - 1:
        if not (up[t] and not up[t - 1] and not np.isnan(sma[t - 2]) and not np.isnan(atr[t])):
            t += 1
            continue
        e = t + 1
        entry, stop = float(D["o"][e]), float(c[t] - k * atr[t])
        if entry <= stop:
            t += 1
            continue
        risk = (entry - stop) / entry
        d, px, kind = e, None, None
        while d < nd:
            lo, op = bl[first[d]:last[d]], bo[first[d]:last[d]]
            hit = np.flatnonzero(lo <= stop)
            if len(hit):
                px, kind = float(min(op[hit[0]], stop)), "stop"
                break
            held[d] = True
            if down[d]:
                if d + 1 < nd:
                    px, kind = float(D["o"][d + 1]), "slope"
                    d += 1                               # the exit day; not held at its close
                break
            stop = max(stop, float(c[d] - k * atr[d]))
            d += 1
        if px is None:
            open_left += 1                               # still open at the end of the data: dropped
            held[e:] = False
            break
        costs = 2 * cost + (cost if kind == "stop" else 0.0)
        ret = px / entry - 1 - costs
        trades.append({"e": e, "x": d, "day": D["day"][e], "ret": ret, "R": ret / risk, "risk": risk, "kind": kind, "nights": int(d - e)})
        t = d if kind == "stop" else d - 1               # flat from here; the next signal needs a fresh turn at a later close
        t = max(t, e)
    return trades, held, open_left


def load(lab, market, fake_seed=None):
    if fake_seed is not None:
        rng = np.random.default_rng(fake_seed)
        ts = pd.date_range("2021-04-21", "2026-04-20 16:00", freq="h")
        ts = ts[ts.dayofweek < 5]
        cl = 100 * np.exp(np.cumsum(rng.normal(-0.000002, 0.002, len(ts)))); op = np.r_[cl[0], cl[:-1]]   # the mean is minus half the variance, so the price itself has no drift
        return ts.to_numpy(), op, np.maximum(op, cl) * 1.0005, np.minimum(op, cl) * 0.9995, cl
    df = pd.read_csv(os.path.join(lab, FILES[market], f"{market}_1h.csv.gz"))
    t = pd.to_datetime(df["time"], utc=True)
    df = df[(t >= pd.Timestamp(START, tz="UTC")) & (t < pd.Timestamp(END_UTC, tz="UTC"))]
    ts = pd.to_datetime(df["time"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None).to_numpy()
    return (ts,) + tuple(df[k].to_numpy(float) for k in ("open", "high", "low", "close"))


def flip(ts, o, h, l, c):
    """One divided by price: a buy here is close to a sell on the real series."""
    return ts, 1 / o, 1 / l, 1 / h, 1 / c


def run_all(data, costs, cost_mult=1.0):
    rows, holds, left = [], [], 0
    for mk, (ts, o, h, l, c) in data.items():
        D, first, last = sessions(ts, o, h, l, c)
        r1 = np.r_[D["c"][1:] / D["c"][:-1] - 1, 0.0]    # move from this close to the next
        for n in NS:
            for k in KS:
                tr, held, ol = simulate(D, first, last, o, l, n, k, costs[mk] * cost_mult)
                left += ol
                for x in tr:
                    x.update(market=mk, n=n, k=k)
                rows += tr
                holds.append((held, r1))
    return pd.DataFrame(rows), holds, left


def day_stats(tr):
    d = tr.groupby("day")["R"].mean()
    v = d.to_numpy()
    wins, losses = v[v > 0].sum(), -v[v < 0].sum()
    return {"entry_days": int(len(v)), "trades": int(len(tr)), "avg_R": round(float(v.mean()), 4),
            "profit_factor": round(float(wins / losses), 2) if losses > 0 else None,
            "t_stat": round(float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))), 2) if len(v) > 2 else None,
            "win_trade_pct": round(100 * float((tr["R"] > 0).mean()), 1), "avg_R_per_trade": round(float(tr["R"].mean()), 4)}, d


def guard(holds, rng):
    real = sum(float((h * r).sum()) for h, r in holds)
    beat = 0
    for _ in range(N_COPIES):
        u = rng.random()
        tot = 0.0
        for h, r in holds:
            s = 20 + int(u * (len(h) - 40))
            tot += float((np.roll(h, s) * r).sum())
        beat += real > tot
    return real, 100.0 * beat / N_COPIES


def selftest():
    # 8 days of 2 hourly bars each; n=2 average; stop logic checked by hand
    days = pd.date_range("2026-01-05", periods=8, freq="D")
    c = np.array([10.0, 9.0, 9.5, 10.5, 11.0, 12.0, 10.8, 10.0])
    D = {"day": days, "o": np.r_[10.0, c[:-1]], "c": c, "h": c + 0.3, "l": c - 0.3}
    first, last = np.arange(0, 16, 2), np.arange(2, 18, 2)
    bo = np.repeat(D["o"], 2).astype(float); bl = np.repeat(np.minimum(D["o"], c) - 0.1, 2)
    global ATR_N
    keep, ATR_N = ATR_N, 2
    try:
        sma, atr = indicators(D, 2)
        assert abs(sma[3] - 10.0) < 1e-12 and sma[2] < sma[1]                       # turn up at day 3 (9.25 -> 10.0)
        tr, held, left = simulate(D, first, last, bo, bl, 2, 5.0, 0.0)              # stop far away: slope exit
        assert len(tr) == 1 and tr[0]["e"] == 4 and tr[0]["kind"] == "slope"        # in at day 4's open (10.5)
        assert tr[0]["x"] == 7 and abs(tr[0]["ret"] - (10.8 / 10.5 - 1)) < 1e-12    # average falls at day 6's close: out at day 7's open
        assert list(np.flatnonzero(held)) == [4, 5, 6] and left == 0
        bl2 = bl.copy(); bl2[11] = 5.0                                               # day 5, second bar trades far down
        tr2, held2, _ = simulate(D, first, last, bo, bl2, 2, 5.0, 0.0)
        s0 = c[3] - 5.0 * atr[3]; s1 = max(s0, c[4] - 5.0 * atr[4])
        assert tr2[0]["kind"] == "stop" and abs(tr2[0]["ret"] - (s1 / 10.5 - 1)) < 1e-12 and s1 > s0   # the stop had moved up; fill at the stop
        assert len(tr2) == 1 and list(np.flatnonzero(held2)) == [4]                 # no re-entry without a fresh turn
        bo3, bl3 = bo.copy(), bl.copy(); bo3[10] = 4.0; bl3[10] = 3.9               # day 5 opens below the stop
        tr3, _, _ = simulate(D, first, last, bo3, bl3, 2, 5.0, 0.0)
        assert tr3[0]["kind"] == "stop" and abs(tr3[0]["ret"] - (4.0 / 10.5 - 1)) < 1e-12              # fill at the open
    finally:
        ATR_N = keep
    print("selftest OK")


def main():
    mode = sys.argv[1]
    if mode == "selftest":
        return selftest()
    if mode == "dryrun":
        data = {f"FAKE{i}": load(None, None, fake_seed=160 + i) for i in range(15)}
        tr, holds, left = run_all(data, {k: 0.00005 for k in data})
        s, _ = day_stats(tr)
        print(json.dumps(s), "left open:", left)
        return
    lab = sys.argv[2]
    sys.path.insert(0, lab)
    import costs
    data = {mk: load(lab, mk) for mk in FILES}
    if mode == "lookahead":
        ok = True
        for mk in ("XAUUSD", "NAS100", "EURUSD"):
            ts, o, h, l, c = data[mk]
            cut = len(ts) * 2 // 3
            D, f, la = sessions(ts, o, h, l, c)
            D2, f2, la2 = sessions(ts[:cut], o[:cut], h[:cut], l[:cut], c[:cut])
            full, _, _ = simulate(D, f, la, o, l, 50, 2.0, 0.0)
            part, _, _ = simulate(D2, f2, la2, o[:cut], l[:cut], 50, 2.0, 0.0)
            a = [(x["e"], x["x"], x["kind"], round(x["ret"], 10)) for x in part if x["x"] < len(D2["c"]) - 2]
            b = [(x["e"], x["x"], x["kind"], round(x["ret"], 10)) for x in full][:len(a)]
            ok = ok and a == b and len(a) > 0
        print("look-ahead check:", "OK" if ok else "MISMATCH")
        return
    out_path = sys.argv[3]
    tr, holds, left = run_all(data, costs.COST)
    s, daily = day_stats(tr)
    tr2, _, _ = run_all(data, costs.COST, cost_mult=2.0)
    s["avg_R_double_cost"] = day_stats(tr2)[0]["avg_R"]
    yr = daily.groupby(daily.index.year).sum()
    s["by_year_sum"] = {int(y): round(float(v), 1) for y, v in yr.items()}
    s["years_positive"] = int((yr > 0).sum())
    bym = tr.groupby("market")["R"].agg(["mean", "count"])
    s["markets_positive"] = int((bym["mean"] > 0).sum())
    byv = tr.groupby(["n", "k"])["R"].agg(["mean", "count"])
    s["versions_positive"] = int((byv["mean"] > 0).sum())
    real, beat = guard(holds, np.random.default_rng(16))
    s["guard_beats_pct"] = round(beat, 1)
    s["left_open"] = int(left)
    s["verdict"] = "PASS" if (s["entry_days"] >= NEED["days"] and s["avg_R"] > 0 and s["t_stat"] >= NEED["t"] and (s["profit_factor"] or 0) >= NEED["pf"]
                              and s["avg_R_double_cost"] > 0 and s["markets_positive"] >= NEED["markets"] and s["years_positive"] >= NEED["years"]
                              and s["guard_beats_pct"] >= NEED["guard"] and s["versions_positive"] >= NEED["versions"]) else "FAIL"
    s["exits_pct"] = {k: round(100 * float(v), 1) for k, v in tr["kind"].value_counts(normalize=True).items()}
    s["median_days_held"] = float(tr["nights"].median()); s["avg_days_held"] = round(float(tr["nights"].mean()), 1)
    s["avg_R_per_trade_after_financing"] = round(float(((tr["ret"] - FIN * tr["nights"]) / tr["risk"]).mean()), 4)
    s["avg_trade_pct_of_price"] = round(100 * float(tr["ret"].mean()), 3)
    out = {"group": s}
    out["by_version"] = {f"{n}d_{k:g}atr": {"trades": int(r["count"]), "avg_R": round(float(r["mean"]), 3)} for (n, k), r in byv.iterrows()}
    mk_change = {mk: float(d[4][-1] / d[1][0] - 1) for mk, d in data.items()}
    tot = tr.groupby("market")["ret"].sum() / len(byv)
    out["by_market"] = {mk: {"trades": int(r["count"]), "avg_R": round(float(r["mean"]), 3), "rule_total_pct_avg_version": round(100 * float(tot[mk]), 1),
                             "market_change_pct": round(100 * mk_change[mk], 1)} for mk, r in bym.iterrows()}
    d50 = tr[(tr["n"] == 50) & (tr["k"] == 2.0)]
    out["default_50d_2atr"] = day_stats(d50)[0]
    trs, _, _ = run_all({mk: flip(*d) for mk, d in data.items()}, costs.COST)
    out["sell_side_mirror"] = day_stats(trs)[0]
    tr.assign(day=tr["day"].dt.strftime("%Y-%m-%d")).drop(columns=["e", "x"]).to_csv(out_path.replace(".json", "_trades.csv"), index=False)
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
