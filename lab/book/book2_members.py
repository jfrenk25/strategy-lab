"""Study 20, part 1: rebuild copy v3 (gold) and the RTH breakout (version A), check each against its own study, mark them hour by hour.
Rules: claude/book2-rules-2026-11-25.md (written before this ran). No combined number is computed here.

Usage: python book2_members.py selftest
       python book2_members.py build LAB_DIR GOLD_DIR OUT_DIR
GOLD_DIR holds the six files *XAUUSD_1m_<year>.csv.gz. OUT_DIR is the folder book_members.py wrote to.
Units: 1 unit = 1% of the account risked per position (copy v3, three positions a fill) or per trade (breakout).
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import book_members as bm

NG, DAY_END, T0, T1 = bm.NG, bm.DAY_END, bm.T0, bm.T1


def mark_minutes(A, gm, C, W, a, b, side, px, scale, cost_in, realized, exit_worst):
    """One trade from minute bars. gm: grid hour of each bar. The trade is open at the close of bars a..b-1 and closes inside bar b.
    C: closes. W: each bar's adverse price (low for a buy, high for a sell). scale turns a fraction of price into % of the account.
    exit_worst: the adverse price inside the exit bar, or None when the exit itself is the worst point (a stop)."""
    g_in, g_out = int(gm[a]), int(gm[b])
    if g_in < 0 or g_out >= NG:
        return False
    A.real[g_out] += realized
    lows_exit = [realized]
    if exit_worst is not None:
        lows_exit.append(scale * (side * (exit_worst / px - 1) - cost_in))
    if b > a:
        g = gm[a:b]
        fl_m = scale * (side * (C[a:b] / px - 1) - cost_in)
        lw_m = scale * (side * (W[a:b] / px - 1) - cost_in)
        inx = g == g_out
        if inx.any():
            lows_exit.append(float(lw_m[inx].min()))
        if g_out > g_in:
            hours = np.arange(g_in, g_out)
            fl = fl_m[np.searchsorted(g, hours, "right") - 1]         # the last mark at or before the end of each hour
            cut = np.flatnonzero(np.r_[True, g[1:] != g[:-1]])
            run_h, run_min = g[cut], np.minimum.reduceat(lw_m, cut)
            k = run_h < g_out
            lw = fl.copy()
            lw[run_h[k] - g_in] = np.minimum(run_min[k], fl[run_h[k] - g_in])
            A.fc[hours] += fl
            A.lo[hours] += lw
            i_lo, i_hi = int(np.searchsorted(DAY_END, g_in)), int(np.searchsorted(DAY_END, g_out - 1, "right")) - 1
            for d in range(i_lo, i_hi + 1):
                A.v.append((d, i_hi, float(fl[DAY_END[d] - g_in])))
    A.lo[g_out] += min(lows_exit)
    A.n += 1
    return True


# ------------------------------------------------------------------ member 10: copy v3 (logic copied from claude/copy_v2.py, copy_v3.py, prop_build.py)
REF = 4150.0
K, MAX_AGE_H, BUF, MAX_HOLD_MIN = 5, 240, 1.5 / REF, 5 * 1440
P = lambda p: p / 100.0 / REF
BOTS = {"Q800": dict(tp=P(800), sl=P(2250), trig=P(300), lock=P(80)),
        "Q900": dict(tp=P(900), sl=P(2250), trig=P(300), lock=P(80)),
        "Q1450": dict(tp=P(1450), sl=P(2250), trig=P(300), lock=P(30))}
FIRM = dict(spread=0.0075, comm=0.0025, slip=0.005, swl=0.0175, sws=0.005)          # the "realistic" cost case, % of price
SL_PCT = 100 * P(2250)


def load_gold(folder, years):
    fr = []
    for y in years:
        f = glob.glob(f"{folder}/*XAUUSD_1m_{y}.csv.gz")
        assert len(f) == 1, (y, f)
        fr.append(pd.read_csv(f[0]))
    return pd.concat(fr, ignore_index=True).drop_duplicates("time").sort_values("time").reset_index(drop=True)


def h4_bars(d):
    ny = pd.to_datetime(d.time, unit="s", utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    key = (ny + pd.Timedelta(hours=7)).dt.floor("4h")
    g = d.assign(i=np.arange(len(d))).groupby(key.values)
    b = g.agg(high=("high", "max"), low=("low", "min"), n=("high", "size"), end_i=("i", "last"))
    return b[b.n >= 30]


def pivots(b, k=K):
    hi, lo, end = b.high.values, b.low.values, b.end_i.values
    out = []
    for i in range(k, len(b) - k):
        if lo[i] < lo[i - k:i].min() and lo[i] <= lo[i + 1:i + k + 1].min():
            out.append((int(end[i + k]), -1, float(lo[i]), int(end[i])))
        if hi[i] > hi[i - k:i].max() and hi[i] >= hi[i + 1:i + k + 1].max():
            out.append((int(end[i + k]), 1, float(hi[i]), int(end[i])))
    return sorted(out)


def entries(d, k=K, max_age_h=MAX_AGE_H, buf=BUF):
    """(bar, side, fill price, level, age in hours). The same walk as copy_v2.entries; the two reach values only skip bars that cannot trigger."""
    O, H, L, T = d.open.tolist(), d.high.tolist(), d.low.tolist(), d.time.tolist()
    piv = pivots(h4_bars(d), k)
    pi, lows, highs, out = 0, [], [], []
    lo_reach, hi_reach = -1e18, 1e18
    for j in range(len(O)):
        while pi < len(piv) and piv[pi][0] < j:
            if piv[pi][1] == -1:
                lows.append((piv[pi][2], piv[pi][3])); lo_reach = max(lo_reach, piv[pi][2] * (1 + buf))
            else:
                highs.append((piv[pi][2], piv[pi][3])); hi_reach = min(hi_reach, piv[pi][2] * (1 - buf))
            pi += 1
        if L[j] <= lo_reach:
            trig = [x for x in lows if L[j] <= x[0] * (1 + buf)]
            if trig:
                lows = [x for x in lows if x not in trig]
                lo_reach = max((x[0] * (1 + buf) for x in lows), default=-1e18)
                live = [x for x in trig if (T[j] - T[x[1]]) / 3600.0 <= max_age_h]
                if live:
                    lv = max(live)
                    out.append((j, -1, min(O[j], lv[0] * (1 + buf)), lv[0], (T[j] - T[lv[1]]) / 3600.0))
        if H[j] >= hi_reach:
            trig = [x for x in highs if H[j] >= x[0] * (1 - buf)]
            if trig:
                highs = [x for x in highs if x not in trig]
                hi_reach = min((x[0] * (1 - buf) for x in highs), default=1e18)
                live = [x for x in trig if (T[j] - T[x[1]]) / 3600.0 <= max_age_h]
                if live:
                    lv = min(live)
                    out.append((j, 1, max(O[j], lv[0] * (1 - buf)), lv[0], (T[j] - T[lv[1]]) / 3600.0))
    return out


def run_leg(O, H, L, C, j, end, side, px, tp, sl, trig, lock):
    """Copied from copy_v2.run_leg."""
    stop, tgt, armed = px - side * sl * px, px + side * tp * px, False
    if (side == 1 and L[j] <= stop) or (side == -1 and H[j] >= stop):
        return j, stop, "stop"
    if (side == 1 and C[j] >= tgt) or (side == -1 and C[j] <= tgt):
        return j, tgt, "target"
    if (C[j] - px) * side >= trig * px:
        stop, armed = px + side * lock * px, True
    for i in range(j + 1, end + 1):
        o, h, l = O[i], H[i], L[i]
        if side == 1:
            if o <= stop: return i, o, "lock" if armed else "stop"
            if o >= tgt: return i, o, "target"
            if l <= stop: return i, stop, "lock" if armed else "stop"
            if h >= tgt: return i, tgt, "target"
        else:
            if o >= stop: return i, o, "lock" if armed else "stop"
            if o <= tgt: return i, o, "target"
            if h >= stop: return i, stop, "lock" if armed else "stop"
            if l <= tgt: return i, tgt, "target"
        if not armed and (C[i] - px) * side >= trig * px:
            stop, armed = px + side * lock * px, True
    return end, C[end], "time"


def nights(e, x):
    """17:00 New York rollovers in (entry, exit], Wednesday counted three times. Copied from prop_build.nights."""
    e, x = e.tz_localize("UTC").tz_convert("America/New_York"), x.tz_localize("UTC").tz_convert("America/New_York")
    r = e.normalize() + pd.Timedelta(hours=17)
    if r <= e:
        r += pd.Timedelta(days=1)
    n = 0
    while r <= x:
        if r.weekday() < 5:
            n += 3 if r.weekday() == 2 else 1
        r += pd.Timedelta(days=1)
    return n


def copy_v3_positions(d):
    O, H, L, C = d.open.tolist(), d.high.tolist(), d.low.tolist(), d.close.tolist()
    utc = pd.to_datetime(d.time, unit="s")
    rows = []
    for f, (j, side, px, lvl, age) in enumerate(entries(d)):
        end = min(j + MAX_HOLD_MIN, len(O) - 1)
        for name, b in BOTS.items():
            i, xp, how = run_leg(O, H, L, C, j, end, side, px, b["tp"], b["sl"], b["trig"], b["lock"])
            rows.append((f, name, j, i, side, px, xp, how))
    t = pd.DataFrame(rows, columns=["fill", "bot", "j", "i", "side", "entry", "exit", "how"])
    t["entry_utc"], t["exit_utc"] = utc.values[t.j.values], utc.values[t.i.values]
    ny = t.entry_utc.dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    mn = ny.dt.hour * 60 + ny.dt.minute
    bad = np.zeros(len(t), bool)
    for c in (510, 600, 840, 870):                                  # 8:30, 10:00, 14:00, 14:30 New York, two minutes either side
        bad |= ((mn >= c - 2) & (mn <= c + 2)).to_numpy()
    t = t[~bad & (t.entry_utc >= "2021-06-01")].reset_index(drop=True)
    nn = np.array([nights(a, b) for a, b in zip(t.entry_utc, t.exit_utc)])
    stopfill = t.how.isin(["stop", "lock"]).to_numpy(float)
    t["ec"] = FIRM["spread"] + FIRM["comm"] + FIRM["slip"]
    gross = 100 * (t.exit - t.entry) * t.side / t.entry
    t["net"] = gross - t.ec - (FIRM["comm"] + FIRM["slip"] * stopfill + nn * np.where(t.side == 1, FIRM["swl"], FIRM["sws"]))
    t["R"] = t.net / SL_PCT
    return t


def v3_by_year(t):
    y = t.entry_utc.dt.year
    return {int(k): {"signals": int(g.fill.nunique()), "usd_at_0.35pct": int(round(350 * g.R.sum()))} for k, g in t.groupby(y)}


def copy_v3_member(d, t, A):
    gm = ((d.time.values - int(T0.timestamp())) // 3600).astype(np.int64)
    C, H, L = d.close.values, d.high.values, d.low.values
    for r in t.itertuples():
        W = L if r.side == 1 else H
        mark_minutes(A, gm, C, W, r.j, r.i, r.side, r.entry, 100.0 / SL_PCT, r.ec / 100.0, r.R,
                     None if r.how in ("stop", "lock") else float(W[r.i]))


# ------------------------------------------------------------------ member 11: RTH open ATR breakout, version A (logic copied from claude/rth_breakout.py)
def rth(lab, A):
    COST, ENTRY_ATR, STOP_ATR, FILTER_MULT, ATR_DAYS = bm.ICOST, 0.2, 0.25, 1.2, 5
    CHECKS = tuple(range(600, 931, 30))
    m = pd.read_csv(os.path.join(lab, "data_1m", "NAS100_1m_full.csv.gz"))
    tu = pd.to_datetime(m["time"], unit="s", utc=True)
    m = m[(tu < T1).to_numpy()].copy()
    m["g"] = bm.gidx(tu[m.index]).to_numpy()
    m["ts"] = tu[m.index].dt.tz_convert("America/New_York").dt.tz_localize(None)
    m = m.sort_values("ts").reset_index(drop=True)
    m["mm"] = m["ts"].dt.hour * 60 + m["ts"].dt.minute
    r = m[(m["mm"] >= 570) & (m["mm"] <= 959)]
    d = r.groupby(r["ts"].dt.normalize()).agg(h=("high", "max"), l=("low", "min"), c=("close", "last"), m0=("mm", "min"), m1=("mm", "max"))
    d = d[(d["m0"] == 570) & (d["m1"] == 959)]
    pc = d["c"].shift()
    tr = np.maximum(d["h"], pc.fillna(d["h"])) - np.minimum(d["l"], pc.fillna(d["l"]))
    prev_atr, prev_range = tr.rolling(ATR_DAYS).mean().shift(), (d["h"] - d["l"]).shift()
    m = m[m["mm"] >= 570]
    rows = []
    for day, g in m.groupby(m["ts"].dt.normalize(), sort=True):
        if day not in d.index or np.isnan(prev_atr.get(day, np.nan)):
            continue
        atr = float(prev_atr[day])
        if not (float(prev_range[day]) < FILTER_MULT * atr):
            rows.append((day, 0.0, 0))
            continue
        mins, gm = g["mm"].to_numpy(), g["g"].to_numpy()
        o, h, l, c = (g[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        pos = {int(x): k for k, x in enumerate(mins)}
        if 570 not in pos or 959 not in pos:
            continue
        last, ref = pos[959], float(o[pos[570]])
        up, dn, dist = ref + ENTRY_ATR * atr, ref - ENTRY_ATR * atr, STOP_ATR * atr
        dayR, ntr, free_from = 0.0, 0, 0
        for cm in CHECKS:
            if cm < free_from or cm - 1 not in pos or cm not in pos:
                continue
            px0 = float(c[pos[cm - 1]])
            side = 1 if px0 > up else (-1 if px0 < dn else 0)
            if side == 0:
                continue
            i = pos[cm]
            entry = float(o[i])
            stop = entry - side * dist
            j, px, kind = last, float(c[last]), "close"
            for q in range(i, last + 1):
                if side == 1 and l[q] <= stop:
                    j, px, kind = q, float(min(o[q], stop)), "stop"; break
                if side == -1 and h[q] >= stop:
                    j, px, kind = q, float(max(o[q], stop)), "stop"; break
            denom = dist / entry
            R = (side * (px / entry - 1) - 2 * COST - (COST if kind == "stop" else 0.0)) / denom
            W = l if side == 1 else h
            mark_minutes(A, gm, c, W, i, j, side, entry, 1.0 / denom, COST, R, None if kind == "stop" else float(W[j]))
            dayR += R
            ntr += 1
            if kind == "close":
                break
            free_from = int(mins[j]) + 1
        rows.append((day, dayR, ntr))
    tab = pd.DataFrame(rows, columns=["day", "R", "n"])
    t = tab[tab["n"] > 0]
    e = t[t["day"] < "2024-01-01"]
    return {"by_year_sum_R": {int(y): round(float(v), 1) for y, v in tab.groupby(tab["day"].dt.year)["R"].sum().items()},
            "2021_2023": {"traded_days": int(len(e)), "sum_R": round(float(e["R"].sum()), 1), "t_stat": bm.tstat(e["R"])},
            "trades_in_grid": A.n, "trades": int(tab["n"].sum())}


def selftest():
    gm = np.array([10, 10, 11, 11, 13, 13])                              # minute bars in hours 10, 11 and 13 (hour 12 has none)
    C = np.array([100.0, 101.0, 99.0, 102.0, 103.0, 104.0])
    W = np.array([99.5, 100.0, 98.0, 99.0, 102.0, 103.0])
    A = bm.Arr()
    assert mark_minutes(A, gm, C, W, 0, 5, 1, 100.0, 100.0, 0.0, 4.0, 103.0)   # buy at 100 in bar 0, closed +4% inside bar 5
    assert np.allclose(A.fc[10:14], [1.0, 2.0, 2.0, 0.0])                # hour 12 carries hour 11's mark; nothing is open after hour 13
    assert np.allclose(A.lo[10:14], [-0.5, -2.0, 2.0, 2.0])              # exit hour: min(bar 4 low +2%, exit bar low +3%, closed +4%)
    assert A.real[13] == 4.0 and A.real.sum() == 4.0
    A2 = bm.Arr()
    assert mark_minutes(A2, gm, C, np.array([100.5, 101.5, 100.0, 102.5, 103.5, 104.5]), 2, 3, -1, 100.0, 50.0, 0.001, -1.3, None)   # a sell stopped in the next bar
    assert np.allclose(A2.lo[11], min(50 * (0.0 - 0.001), -1.3)) and A2.fc[11] == 0.0 and A2.real[11] == -1.3
    A3 = bm.Arr()
    assert mark_minutes(A3, gm, C, W, 4, 4, 1, 103.0, 100.0, 0.0, -0.2, None) and A3.lo[13] == -0.2 and A3.fc.sum() == 0.0   # in and out in one bar
    O = [10, 10, 10, 10, 10]
    assert run_leg(O, [10, 10.2, 10, 10, 10], [10, 9.9, 9.9, 10, 10], [10, 10.1, 10, 10, 10], 0, 4, 1, 10.0, 0.02, 0.05, 0.005, 0.001)[1:] == (10.2, "target")
    i, xp, how = run_leg([10, 10, 10.05, 10, 10], [10, 10.1, 10.05, 10, 10], [10, 10, 9.9, 10, 10], [10, 10.08, 10, 10, 10], 0, 4, 1, 10.0, 0.02, 0.05, 0.005, 0.001)
    assert (i, how) == (2, "lock") and abs(xp - 10.01) < 1e-12           # armed by the close of bar 1, stopped at entry plus the lock in bar 2
    i, xp, how = run_leg(O, [10, 10.1, 10, 10, 10], [10, 10, 9.9, 10, 10], [10, 10.08, 10, 10, 10], 0, 4, 1, 10.0, 0.02, 0.05, 0.005, 0.001)
    assert (i, xp, how) == (2, 10, "lock")                               # bar 2 opens under the moved stop: out at its open
    assert nights(pd.Timestamp("2026-01-07 15:00"), pd.Timestamp("2026-01-08 15:00")) == 3     # one Wednesday rollover counts three times
    print("selftest OK")


def main():
    if sys.argv[1] == "selftest":
        return selftest()
    lab, gold, out = sys.argv[2:5]
    stats = {}

    def save(name, A, st):
        v = np.array(A.v, float).reshape(-1, 3)
        carried = np.zeros(len(bm.DAYS)); np.add.at(carried, v[:, 0].astype(int), v[:, 2])
        assert np.allclose(carried, A.fc[DAY_END], atol=1e-9), name
        np.savez_compressed(os.path.join(out, name + ".npz"), real=A.real, fc=A.fc, lo=A.lo, v=v)
        stats[name] = st
        print(name, json.dumps(st), flush=True)

    d5 = load_gold(gold, [2021, 2022, 2023, 2024, 2025])
    study = v3_by_year(copy_v3_positions(d5))                            # as the copy v3 study ran it: 2021 to 2025 only
    d = load_gold(gold, [2021, 2022, 2023, 2024, 2025, 2026])
    d = d[d.time < int(T1.timestamp())].reset_index(drop=True)           # nothing after April 20, 2026 is read into the book
    t = copy_v3_positions(d)
    A = bm.Arr()
    copy_v3_member(d, t, A)
    save("10_copy_v3", A, {"rebuilt_2021_2025": study, "study_says": {"signals": [69, 114, 107, 114, 109], "usd_at_0.35pct": [2287, 5984, 10293, 6015, 8455]},
                           "continuous_run_to_apr_2026": v3_by_year(t), "positions_in_grid": A.n})
    A = bm.Arr()
    st = rth(lab, A)
    st["study_says_by_year"] = {"2021": 24.9, "2022": 70.2, "2023": 26.6, "2024": 42.6, "2025": 10.7, "2021_2023": "537 days, +121.8R, t 3.10"}
    save("11_rth_breakout_A", A, st)
    json.dump(stats, open(os.path.join(out, "members2.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
