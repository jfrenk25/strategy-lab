"""Study 18: the breakout (Study 17) and the dip-buy rule (Study 13, 3 ATR stop) as a pair.
Rules: claude/pair-breakout-dipbuy-rules-2026-11-25.md (written before this ran).

Usage: python -I pair_study.py MODE LAB_DIR STUDY17_OUT_DIR [OUT_JSON]
  MODE  check   rebuild the dip-buy leg and compare it with Study 13 (prints trade count and total only)
        run     the study (once)
Needs gapline_orb.py in the same folder (challenge replay) and the pandas_market_calendars package (exchange sessions).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

import gapline_orb as g14

COST, SWAP, K, ATR_N = 0.00005, 0.0002, 3.0, 10
B_RISKS, C_RISKS = (0.25, 0.375, 0.5), (0.0, 0.5, 1.0, 1.5)
H = lambda h, m=0: pd.Timedelta(hours=h, minutes=m)


def cutler_rsi(c, n=3):
    d = np.diff(c, prepend=np.nan)
    up = pd.Series(np.where(d > 0, d, 0.0)).rolling(n).sum().to_numpy()
    dn = pd.Series(np.where(d < 0, -d, 0.0)).rolling(n).sum().to_numpy()
    out = np.where(up + dn > 0, 100 * up / np.where(up + dn > 0, up + dn, 1), 50.0)
    out[:n] = np.nan
    return out


def load(lab):
    m = pd.read_csv(os.path.join(lab, "data_1m", "NAS100_1m_full.csv.gz"))
    m["ts"] = pd.to_datetime(m["time"], unit="s", utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    h = pd.read_csv(os.path.join(lab, "data_new", "NAS100_1h.csv.gz"))
    h["ts"] = pd.to_datetime(h["time"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    return m.sort_values("ts").reset_index(drop=True), h.sort_values("ts").reset_index(drop=True)


def daily(m):
    sess = mcal.get_calendar("NYSE").schedule("2021-04-21", str(m["ts"].max().date())).index   # to the last bar on file, so new bars are picked up
    mn = m["ts"].dt.hour * 60 + m["ts"].dt.minute
    r = m[(mn >= 570) & (mn <= 959)]
    d = r.groupby(r["ts"].dt.normalize()).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"))
    return d[d.index.isin(sess)]


def cut(src, a, b):
    i, j = np.searchsorted(src["ts"], np.datetime64(a)), np.searchsorted(src["ts"], np.datetime64(b))
    return [src[k][i:j] for k in ("ts", "open", "low", "close")]


def dipbuy(m, h):
    d = daily(m)
    dates = list(d.index)
    o, hi, lo, c = (d[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    pc = np.r_[np.nan, c[:-1]]
    tr = np.where(np.isnan(pc), hi - lo, np.maximum(hi, pc) - np.minimum(lo, pc))
    atr = pd.Series(tr).rolling(ATR_N).mean().to_numpy()
    rsi = cutler_rsi(c)
    M = {k: m[k].to_numpy() for k in ("ts", "open", "low", "close")}
    Hh = {k: h[k].to_numpy() for k in ("ts", "open", "low", "close")}
    close_time = np.array([np.datetime64(x + H(16)) for x in dates])
    trades, t, n = [], 4, len(c)
    while t < n - 2:
        if not (rsi[t] < 10 and not np.isnan(atr[t])):
            t += 1
            continue
        e = t + 1
        u = e
        while u < n and not (c[u] > c[u - 1]):
            u += 1
        x = u + 1
        if x >= n:
            break
        entry, stop = o[e], o[e] - K * atr[t]
        parts = [cut(M, dates[e] + H(9, 30), dates[e] + H(10)), cut(Hh, dates[e] + H(10), dates[x] + H(9))]
        tail = cut(M, dates[x] + H(9), dates[x] + H(9, 30))
        parts.append(tail if len(tail[0]) else cut(Hh, dates[x] + H(9), dates[x] + H(10)))
        ts, bo, bl, bc = (np.concatenate([p[k] for p in parts]) for k in range(4))
        hit = np.flatnonzero(bl <= stop)
        t_in = dates[e] + H(9, 30)
        if len(hit):
            j = int(hit[0]); px, t_out, stopped = float(min(bo[j], stop)), pd.Timestamp(ts[j]), True
            ts, bl, bc = ts[:j + 1], bl[:j + 1].copy(), bc[:j + 1].copy(); bl[j] = px; bc[j] = px
        else:
            px, t_out, stopped = o[x], dates[x] + H(9, 30), False
        nights = int(((t_out - H(17)).normalize() - (t_in - H(17)).normalize()).days)
        risk = (entry - stop) / entry
        net = px / entry - 1 - 2 * COST - (COST if stopped else 0.0) - SWAP * nights
        trades.append({"e": e, "x": x, "t_out": t_out, "stopped": stopped, "R": net / risk, "ts": ts,
                       "lowR": (bl / entry - 1) / risk, "closeR": (bc / entry - 1) / risk})
        t = x if not stopped else int(np.searchsorted(close_time, np.datetime64(t_out), side="right"))
    return trades, dates


def day_table(trades, dates):
    n = len(dates)
    darr = np.array([np.datetime64(x) for x in dates])
    a = np.zeros(n); dmin = np.zeros(n); dbal = np.zeros(n); flat0 = np.ones(n, bool); flat1 = np.ones(n, bool)
    for tr in trades:
        fd = np.searchsorted(darr, (pd.DatetimeIndex(tr["ts"]) + H(6)).normalize().to_numpy())
        i0 = tr["e"]
        i1 = int(np.searchsorted(darr, np.datetime64((tr["t_out"] + H(6)).normalize())))
        carry = 0.0
        for i in range(i0, i1 + 1):
            sel = fd == i
            a[i] = carry
            lows = [tr["lowR"][sel].min() - carry] if sel.any() else []
            if i == i1:
                dbal[i] += tr["R"]
                lows.append(tr["R"] - carry)
            dmin[i] = min([0.0] + lows)
            flat0[i] = i == i0
            flat1[i] = i == i1
            if sel.any():
                carry = tr["closeR"][sel][-1]
    return pd.DataFrame({"day": dates, "a": a, "dmin": dmin, "dbal": dbal, "flat0": flat0, "flat1": flat1})


def max_dd(pnl):
    eq = np.cumsum(pnl)
    return float((eq - np.maximum.accumulate(np.r_[0.0, eq])[1:]).min())


def main():
    mode, lab, s17 = sys.argv[1:4]
    m, h = load(lab)
    trades, dates = dipbuy(m, h)
    R = np.array([t["R"] for t in trades])
    yr = pd.Series(R, index=[dates[t["e"]].year for t in trades]).groupby(level=0).sum()
    rebuilt = {"trades": int(len(R)), "stopped": int(sum(t["stopped"] for t in trades)), "sum_R": round(float(R.sum()), 1),
               "by_year": {int(y): round(float(v), 1) for y, v in yr.items()}, "sessions": int(len(dates))}
    if mode == "check":
        print(json.dumps(rebuilt))
        return
    out = {"dipbuy_rebuilt": rebuilt, "study13": {"trades": 118, "stopped_pct": 1, "sum_R": 8.2,
                                                  "by_year": {2021: 1.2, 2022: 1.2, 2023: 1.8, 2024: -0.3, 2025: 4.1, 2026: 0.2}}}
    C = day_table(trades, dates)
    a_next = np.r_[C["a"].to_numpy()[1:], 0.0]
    C["pnl"] = C["dbal"] + a_next - C["a"]                       # day's change in closed plus open result, in R
    for name in ("A_as_posted", "B_daily_cap"):
        B = pd.read_csv(os.path.join(s17, f"rth_{name}_days.csv"), parse_dates=["day"]).set_index("day")
        T = C.set_index("day").join(B[["dbal", "dmin", "n"]], rsuffix="_b").fillna({"dbal_b": 0.0, "dmin_b": 0.0, "n": 0})
        T = T[T.index >= B.index[0]]
        res = {"days": int(len(T))}
        if name == "A_as_posted":
            b, c = T["dbal_b"].to_numpy(), T["pnl"].to_numpy()
            inpos = (T["a"].to_numpy() != 0) | (c != 0)
            res["corr_all_days"] = round(float(np.corrcoef(b, c)[0, 1]), 3)
            res["corr_days_dipbuy_in_trade"] = round(float(np.corrcoef(b[inpos], c[inpos])[0, 1]), 3)
            res["dipbuy_days_in_trade"] = int(inpos.sum())
            res["breakout_sum_R_on_those_days"] = round(float(b[inpos].sum()), 1)
            res["breakout_avg_R_on_those_days"] = round(float(b[inpos & (T["n"].to_numpy() > 0)].mean()), 3)
            worst = np.argsort(b)[:20]
            res["breakout_20_worst_days"] = {"sum_R": round(float(b[worst].sum()), 1), "dipbuy_in_trade": int(inpos[worst].sum()),
                                             "dipbuy_sum_R": round(float(c[worst].sum()), 2)}
            res["drawdown_pct"] = {}
            for rb in B_RISKS:
                for rc in C_RISKS:
                    res["drawdown_pct"][f"{rb}+{rc}"] = {"deepest": round(max_dd(rb * b + rc * c), 1), "total": round(float((rb * b + rc * c).sum()), 1)}
        cells = {}
        for firm, S in g14.FIRMS.items():
            cells[firm] = {}
            for rb in B_RISKS:
                for rc in C_RISKS:
                    tab = pd.DataFrame({"a": rc * T["a"].to_numpy(), "dmin": rb * T["dmin_b"].to_numpy() + rc * T["dmin"].to_numpy(),
                                        "dbal": rb * T["dbal_b"].to_numpy() + rc * T["dbal"].to_numpy(),
                                        "flat0": T["flat0"].to_numpy(), "flat1": T["flat1"].to_numpy()})
                    r = g14.challenge(tab, S, 1.0)
                    r["fits"] = bool(r["passed_pct"] >= 50 and r["breach_daily_pct"] + r["breach_max_pct"] <= 10
                                     and r["median_days_to_pass"] is not None and r["median_days_to_pass"] <= 250)
                    cells[firm][f"{rb}+{rc}"] = r
        res["challenge"] = cells
        out[name] = res
    json.dump(out, open(sys.argv[4], "w"), indent=1)
    print("done")


if __name__ == "__main__":
    main()
