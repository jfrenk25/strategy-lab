"""Study 17, part 2: the nine members in one account. Rules: claude/book-rules-2026-11-25.md (written before this ran). One run.

Usage: python book.py selftest
       python book.py run MEMBERS_DIR OUT_JSON
MEMBERS_DIR holds the files written by book_members.py.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

NAMES = ["1_cutler_D", "2_cmo_B", "3_rsi_ema_vwap_C", "4_third_friday_E", "5_gapline_orb", "6_ma_slope", "7_gtja118", "8_streak_k5", "9_a158_rsqr"]
BOOKS = {"ALL": list(range(9)), "PUBLIC": list(range(6))}
VOLS = (4.0, 6.0, 8.0, 10.0, 12.0, 15.0)                # yearly swing targets, % of the account
REPLAY_FROM, EARLY_END, LATE_FROM = "2021-08-02", "2023-12-31", "2024-01-01"
CAP, YEAR = 500, 260
FIRMS = {
    "FTMO 1-Step": dict(target=10.0, daily=3.0, ref="balance", maxloss=10.0, trailing=True, need=0, best=0.5),
    "The5ers 1-step": dict(target=10.0, daily=3.0, ref="higher", maxloss=6.0, trailing=False, need=3, best=None),
}
N_SLIDES, SEED = 500, 17


def replay(E, R, L, G, S, k0):
    """Every start from day k0 with CAP days after it. E, R, L: account value at each day's end, closed profit to date, lowest value in the day.
    G[row, j]: open profit, as marked at the start, of trades open at the start and still open at the end of day start+j."""
    n = len(E)
    starts = np.arange(k0, n - CAP)
    idx = starts[:, None] + np.arange(CAP)[None, :]
    B0, R0 = E[starts - 1], R[starts - 1]
    F0 = B0 - R0
    eq, low = E[idx] - B0[:, None], L[idx] - B0[:, None]
    bal = R[idx] - R0[:, None] - F0[:, None] + G
    z = np.zeros((len(starts), 1))
    bal0, eq0 = np.hstack([z, bal[:, :-1]]), np.hstack([z, eq[:, :-1]])
    dreal = bal - bal0
    ref = bal0 if S["ref"] == "balance" else np.maximum(bal0, eq0)
    daily = low <= ref - S["daily"] + 1e-9
    floor = (np.maximum.accumulate(np.maximum(bal0, 0.0), axis=1) - S["maxloss"]) if S["trailing"] else -S["maxloss"]
    mx = low <= floor + 1e-9
    ok = (eq >= S["target"] - 1e-9) & (np.cumsum(dreal >= 0.5 - 1e-9, axis=1) >= S["need"])
    if S["best"] is not None:
        ok &= np.maximum.accumulate(dreal, axis=1) <= S["best"] * eq + 1e-9
    br = daily | mx
    fb = np.where(br.any(1), br.argmax(1), CAP)
    fp = np.where(ok.any(1), ok.argmax(1), CAP)
    out = np.full(len(starts), "dropped", dtype=object)
    out[fp < fb] = "passed"
    hit = (fb <= fp) & (fb < CAP)
    rows = np.flatnonzero(hit)
    out[rows] = np.where(daily[rows, fb[rows]], "breach_daily", "breach_max")
    return out, np.where(fp < fb, fp + 1, -1), starts


def replay_loop(E, R, L, G, S, k0):
    """The same rules as a plain day-by-day loop, written separately, to check replay()."""
    res = []
    for row, s in enumerate(range(k0, len(E) - CAP)):
        B0, R0 = E[s - 1], R[s - 1]
        F0 = B0 - R0
        bal_mid = eq_mid = hwm = 0.0
        best, pdays, o, took = -1e18, 0, "dropped", -1
        for j in range(CAP):
            k = s + j
            low = L[k] - B0
            hwm = max(hwm, bal_mid)
            ref = bal_mid if S["ref"] == "balance" else max(bal_mid, eq_mid)
            if low <= ref - S["daily"] + 1e-9:
                o = "breach_daily"; break
            if low <= (hwm - S["maxloss"] if S["trailing"] else -S["maxloss"]) + 1e-9:
                o = "breach_max"; break
            bal = R[k] - R0 - F0 + G[row, j]
            eq = E[k] - B0
            d = bal - bal_mid
            best = max(best, d)
            pdays += d >= 0.5 - 1e-9
            good = eq >= S["target"] - 1e-9 and pdays >= S["need"]
            if S["best"] is not None:
                good = good and best <= S["best"] * eq + 1e-9
            if good:
                o, took = "passed", j + 1; break
            bal_mid, eq_mid = bal, eq
        res.append((o, took))
    return np.array([r[0] for r in res], dtype=object), np.array([r[1] for r in res])


def summarise(out, took):
    sh = lambda k: round(100 * float((out == k).mean()), 1)
    r = {"starts": int(len(out)), "passed_pct": sh("passed"), "breach_daily_pct": sh("breach_daily"), "breach_max_pct": sh("breach_max"),
         "dropped_pct": sh("dropped"), "median_days_to_pass": float(np.median(took[took > 0])) if (took > 0).any() else None}
    r["fits"] = bool(r["passed_pct"] >= 50 and r["breach_daily_pct"] + r["breach_max_pct"] <= 10
                     and r["median_days_to_pass"] is not None and r["median_days_to_pass"] <= 250)
    return r


def carried(v, k0, n):
    """G for one member at unit size, from its (day, last day open, open profit) rows."""
    S = n - CAP - k0
    Gd = np.zeros((S, CAP + 1))
    s = v[:, 0].astype(int) + 1
    dl = v[:, 1].astype(int)
    keep = (s >= k0) & (s < n - CAP) & (dl >= s)
    s, dl, f = s[keep], dl[keep], v[keep, 2]
    np.add.at(Gd, (s - k0, np.zeros(len(s), int)), f)
    np.add.at(Gd, (s - k0, np.minimum(dl - s + 1, CAP)), -f)
    return np.cumsum(Gd, axis=1)[:, :CAP]


def path_stats(p):
    """p: daily account changes in %. Yearly return, Sharpe, worst day, deepest drawdown at the day's close."""
    eq = np.cumsum(p)
    dd = eq - np.maximum.accumulate(np.r_[0.0, eq])[1:]
    sd = p.std(ddof=1)
    return {"total_pct": round(float(p.sum()), 1), "per_year_pct": round(float(p.mean() * YEAR), 1),
            "sharpe": round(float(p.mean() / sd * np.sqrt(YEAR)), 2) if sd > 0 else None,
            "swing_per_year_pct": round(float(sd * np.sqrt(YEAR)), 1), "worst_day_pct": round(float(p.min()), 2),
            "deepest_drawdown_pct": round(float(dd.min()), 1)}


def selftest():
    rng = np.random.default_rng(1)
    n, k0 = 900, 30
    for S in FIRMS.values():
        for trial in range(6):
            d = rng.normal(0.05, 0.9, n)
            R = np.cumsum(d)
            F = rng.normal(0, 0.8, n)
            E = R + F
            L = np.r_[0.0, E[:-1]] - np.abs(rng.normal(0, 1.0, n))
            L = np.minimum(L, E)
            G = rng.normal(0, 0.5, (n - CAP - k0, 1)) * (np.arange(CAP)[None, :] < rng.integers(1, 30, (n - CAP - k0, 1)))
            o1, t1, _ = replay(E, R, L, G, S, k0)
            o2, t2 = replay_loop(E, R, L, G, S, k0)
            assert (o1 == o2).all() and (t1 == t2).all()
            assert len(set(o1)) >= 2
    v = np.array([[40.0, 43.0, 1.5], [10.0, 12.0, 9.0]])
    G = carried(v, 30, 900)
    assert G.shape == (370, CAP) and np.allclose(G[11, :3], 1.5) and G[11, 3] == 0 and G.sum() == 4.5
    print("selftest OK")


def main():
    if sys.argv[1] == "selftest":
        return selftest()
    mdir, out_path = sys.argv[2:4]
    dz = np.load(os.path.join(mdir, "days.npz"), allow_pickle=True)
    days, first, end = pd.DatetimeIndex(dz["days"]), dz["first"], dz["end"]
    n = len(days)
    k0 = int(np.searchsorted(days, pd.Timestamp(REPLAY_FROM)))
    early = (days >= REPLAY_FROM) & (days <= EARLY_END)
    late = days >= LATE_FROM
    win = days >= REPLAY_FROM
    Eh, Rh, Lh, V = [], [], [], []
    for nm in NAMES:
        z = np.load(os.path.join(mdir, nm + ".npz"))
        r = np.cumsum(z["real"])
        Eh.append(r + z["fc"]); Rh.append(r); Lh.append(np.r_[0.0, r[:-1]] + z["lo"]); V.append(z["v"])
    Eh, Rh, Lh = np.array(Eh), np.array(Rh), np.array(Lh)
    Ed = Eh[:, end]                                                    # each member's value at every day end, unit size
    P = np.diff(np.c_[np.zeros(len(NAMES)), Ed], axis=1)               # daily change
    sig = P[:, early].std(axis=1, ddof=1)
    Gm = [carried(v, k0, n) for v in V]
    out = {"settings": {"vols": VOLS, "replay_from": REPLAY_FROM, "early_end": EARLY_END, "cap_days": CAP, "firm_days": n,
                        "starts": n - CAP - k0, "first_start": str(days[k0].date()), "last_start": str(days[n - CAP - 1].date()),
                        "last_day": str(days[-1].date())}}

    def weights(members, vol):
        w = np.zeros(len(NAMES))
        w[members] = 1.0 / (len(members) * sig[members])
        return w * (vol / np.sqrt(YEAR)) / (w @ P)[early].std(ddof=1)

    def tables(w):
        e, r = w @ Ed, w @ Rh[:, end]
        low = np.minimum.reduceat(w @ Lh, first)
        return e, r, low, sum(wi * g for wi, g in zip(w, Gm) if wi != 0)

    configs = {nm: [i] for i, nm in enumerate(NAMES)}
    configs.update({"BOOK_" + k: v for k, v in BOOKS.items()})

    # ---- test 1: each member and each book alone, at a 10% yearly swing set on the early window
    t1 = {}
    for nm, mem in configs.items():
        w = weights(mem, 10.0)
        p = (w @ P)
        e, r, low, _ = tables(w)
        dip = (low - np.r_[0.0, e[:-1]])[win]
        s = path_stats(p[win])
        s["worst_dip_inside_a_day_pct"] = round(float(dip.min()), 2)
        s["early"], s["late"] = path_stats(p[early]), path_stats(p[late])
        s["by_year_pct"] = {int(y): round(float(p[win & (days.year == y)].sum()), 1) for y in sorted(set(days.year[win]))}
        s["days_with_a_change_pct"] = round(100 * float((p[win] != 0).mean()), 0)
        t1[nm] = s
    out["test1_alone_at_10pct"] = t1

    # ---- test 2: do they move together?
    Z = P[:, win] / sig[:, None]
    C = np.corrcoef(Z)
    iu = lambda m: np.array([C[a, b] for a in m for b in m if a < b])
    t2 = {"correlation": {NAMES[a]: {NAMES[b]: round(float(C[a, b]), 2) for b in range(len(NAMES))} for a in range(len(NAMES))},
          "average_pair": {k: round(float(iu(m).mean()), 3) for k, m in BOOKS.items()},
          "highest_pair": {k: round(float(iu(m).max()), 2) for k, m in BOOKS.items()}}
    rng = np.random.default_rng(SEED)
    for bk, mem in BOOKS.items():
        w = weights(mem, 10.0)
        X = (w[mem, None] * P[mem][:, win])
        real = path_stats(X.sum(0))
        nd = X.shape[1]
        wd, dd, sh = [], [], []
        for _ in range(N_SLIDES):
            sl = rng.integers(20, nd - 20, len(mem))
            ps = path_stats(sum(np.roll(X[i], sl[i]) for i in range(len(mem))))
            wd.append(ps["worst_day_pct"]); dd.append(ps["deepest_drawdown_pct"]); sh.append(ps["swing_per_year_pct"])
        t2["tail_" + bk] = {"real_worst_day_pct": real["worst_day_pct"], "slid_median_worst_day_pct": round(float(np.median(wd)), 2),
                            "real_worse_than_pct_of_slid": round(100 * float((np.array(wd) > real["worst_day_pct"]).mean()), 1),
                            "real_deepest_drawdown_pct": real["deepest_drawdown_pct"], "slid_median_drawdown_pct": round(float(np.median(dd)), 1),
                            "drawdown_worse_than_pct_of_slid": round(100 * float((np.array(dd) > real["deepest_drawdown_pct"]).mean()), 1),
                            "real_swing_per_year_pct": real["swing_per_year_pct"], "slid_median_swing_pct": round(float(np.median(sh)), 1)}
        tot = X.sum(0)
        worst = np.argsort(tot)[:5]
        t2["worst_days_" + bk] = [{"day": str(days[win][i].date()), "book_pct": round(float(tot[i]), 2),
                                   "members_pct": {NAMES[m]: round(float(X[q, i]), 2) for q, m in enumerate(mem) if abs(X[q, i]) > 0.005}} for i in worst]
    out["test2_together"] = t2

    # ---- tests 3 and 4: challenge replay, and the same with each config's average daily gain removed
    t3, t4, check = {}, {}, {}
    jan = int(np.searchsorted(days, pd.Timestamp(LATE_FROM)))
    t5 = {}
    for nm, mem in configs.items():
        t3[nm], t4[nm] = {}, {}
        for vol in VOLS:
            w = weights(mem, vol)
            e, r, low, G = tables(w)
            m = float((w @ P)[win].mean())
            drift = np.where(np.arange(n) >= k0, m * (np.arange(n) - k0 + 1), 0.0)
            e0, r0, low0 = e - drift, r - drift, low - np.r_[0.0, drift[:-1]]
            for firm, S in FIRMS.items():
                o, took, starts = replay(e, r, low, G, S, k0)
                t3[nm].setdefault(firm, {})[str(vol)] = summarise(o, took)
                o0, took0, _ = replay(e0, r0, low0, G, S, k0)
                t4[nm].setdefault(firm, {})[str(vol)] = summarise(o0, took0)
                if nm.startswith("BOOK"):
                    row = jan - k0
                    t5.setdefault(nm, {}).setdefault(firm, {})[str(vol)] = {"outcome": str(o[row]), "days": int(took[row]) if took[row] > 0 else None}
                    if vol in (8.0, 12.0):
                        o2, took2 = replay_loop(e, r, low, G, S, k0)
                        check[f"{nm} {firm} {vol}"] = bool((o == o2).all() and (took == took2).all())
    out["test3_challenge"], out["test4_no_edge"] = t3, t4
    out["test5_started_first_day_of_2024"] = {"start_day": str(days[jan].date()), "books": t5}
    out["plain_loop_matches"] = check
    # ---- how each book is put together and what it looks like at each size
    out["weights_at_10pct"] = {bk: {NAMES[i]: round(float(weights(mem, 10.0)[i]), 3) for i in mem} for bk, mem in BOOKS.items()}
    out["book_by_size"] = {}
    for bk, mem in BOOKS.items():
        out["book_by_size"][bk] = {}
        for vol in VOLS:
            w = weights(mem, vol)
            e, r, low, _ = tables(w)
            s = path_stats((w @ P)[win])
            s["worst_dip_inside_a_day_pct"] = round(float((low - np.r_[0.0, e[:-1]])[win].min()), 2)
            out["book_by_size"][bk][str(vol)] = s
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
