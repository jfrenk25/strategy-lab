"""Study 17, part 1: rebuild each member's trades, check them against the member's own study, and mark them hour by hour.
Rules: claude/book-rules-2026-11-25.md (written before this ran). No combined number is computed here.

Usage: python book_members.py selftest
       python book_members.py build LAB_DIR ETF_DIR OUT_DIR
Each member is saved as OUT_DIR/<name>.npz with three hourly arrays in % of the account at the member's own unit:
  real  closed profit booked in that hour
  fc    open profit of every open trade at the end of that hour
  lo    the sum of every trade's worst point in that hour (a trade closed in the hour counts its worst point before the close)
Units: 1 unit = a position worth 1x the account (members 1 to 4) or 1% of the account risked per trade (members 5 to 9).
"""
import json
import os
import sys

import numpy as np
import pandas as pd

T0 = pd.Timestamp("2021-04-21", tz="UTC")
T1 = pd.Timestamp("2026-04-21", tz="UTC")              # hours from T1 on are the lab's quarantine: never marked
NG = int((T1 - T0) / pd.Timedelta(hours=1))
HOUR = pd.Timedelta(hours=1)
FIN = 0.0002                                           # estimated financing per night held, as a fraction of price
SIX = ("BTCUSD", "ETHUSD", "XAUUSD", "GBPJPY", "USA30", "DEU30")
FIFTEEN = SIX + ("SPX500", "NAS100", "USOIL", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "EURJPY")
ICOST = 0.00005                                        # indices, per side (checked against costs.py in build)


def gidx(ts):
    """Grid hour of a UTC timestamp (or series of them)."""
    return (ts - T0) // HOUR


def firm_days():
    """Firm day of every grid hour: midnight to midnight Prague, Saturday with Friday, Sunday with Monday."""
    loc = pd.date_range(T0, periods=NG, freq="h").tz_convert("Europe/Prague")
    wd = loc.weekday.to_numpy()
    day = loc.tz_localize(None).normalize() + pd.to_timedelta((wd == 6).astype(int) - (wd == 5).astype(int), unit="D")
    codes, uniq = pd.factorize(day)
    assert (np.diff(codes) >= 0).all()
    first = np.r_[0, np.flatnonzero(np.diff(codes)) + 1]
    return pd.DatetimeIndex(uniq), first, np.r_[first[1:], NG] - 1


DAYS, DAY_FIRST, DAY_END = firm_days()


class Arr:
    def __init__(self):
        self.real, self.fc, self.lo, self.n = np.zeros(NG), np.zeros(NG), np.zeros(NG), 0
        self.v = []                                    # (firm day, last firm day the trade is still open at the end of, open profit at the end of that firm day)


def mark(A, B, g_in, g_out, side, entry, units, cost_in, realized, exit_is_worst):
    """Add one trade to a member's hourly arrays. B holds the market's hourly bars: g (grid hour), l, h, c.
    Returns False (and adds nothing) if the trade is not wholly inside the grid."""
    if g_in < 0 or g_out >= NG or g_out < g_in:
        return False
    bh = B["g"]
    A.real[g_out] += realized
    j = int(np.searchsorted(bh, g_out))
    if exit_is_worst or j >= len(bh) or bh[j] != g_out:
        A.lo[g_out] += realized
    else:
        adv = B["l"][j] if side == 1 else B["h"][j]
        A.lo[g_out] += min(units * (side * (adv / entry - 1) - cost_in), realized)
    if g_out > g_in:
        gs = np.arange(g_in, g_out)
        i0 = int(np.searchsorted(bh, g_in))
        pos = np.searchsorted(bh, gs, "right") - 1
        ok = pos >= i0
        p = np.clip(pos, 0, len(bh) - 1)
        fl = np.where(ok, units * (side * (B["c"][p] / entry - 1) - cost_in), -units * cost_in)
        adv = B["l"][p] if side == 1 else B["h"][p]
        lw = np.where(ok & (bh[p] == gs), units * (side * (adv / entry - 1) - cost_in), fl)
        A.fc[gs] += fl
        A.lo[gs] += np.minimum(lw, fl)
        i_lo, i_hi = int(np.searchsorted(DAY_END, g_in)), int(np.searchsorted(DAY_END, g_out - 1, "right")) - 1
        for d in range(i_lo, i_hi + 1):
            A.v.append((d, i_hi, float(fl[DAY_END[d] - g_in])))
    A.n += 1
    return True


def bars(lab, m):
    df = pd.read_csv(os.path.join(lab, "data" if m in SIX else "data_new", f"{m}_1h.csv.gz"))
    t = pd.to_datetime(df["time"], utc=True)
    k = ((t >= T0) & (t < T1)).to_numpy()
    df, t = df[k].reset_index(drop=True), t[k].reset_index(drop=True)
    return {"g": gidx(t).to_numpy(), "t": t, **{x[0]: df[x].to_numpy(float) for x in ("open", "high", "low", "close")}}


def pf(v):
    v = np.asarray(v, float)
    w, ls = v[v > 0].sum(), -v[v < 0].sum()
    return round(float(w / ls), 2) if ls > 0 else None


def tstat(v):
    v = np.asarray(v, float)
    return round(float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))), 2) if len(v) > 2 else None


# ------------------------------------------------------------------ members 1 to 4: Study 12 rules (copied from claude/qs_study.py)
def wilder_rsi(close, n):
    c = np.asarray(close, float)
    d = np.diff(c, prepend=np.nan)
    up, dn = np.where(d > 0, d, 0.0), np.where(d < 0, -d, 0.0)
    out = np.full(len(c), np.nan)
    if len(c) <= n:
        return out
    au, ad = up[1:n + 1].mean(), dn[1:n + 1].mean()
    out[n] = 100.0 if ad == 0 and au > 0 else (50.0 if au + ad == 0 else 100 * au / (au + ad))
    for i in range(n + 1, len(c)):
        au = (au * (n - 1) + up[i]) / n
        ad = (ad * (n - 1) + dn[i]) / n
        out[i] = 50.0 if au + ad == 0 else 100 * au / (au + ad)
    return out


def cutler_rsi(close, n):
    c = pd.Series(np.asarray(close, float))
    d = c.diff()
    up, dn = d.clip(lower=0).rolling(n).sum(), (-d.clip(upper=0)).rolling(n).sum()
    tot = up + dn
    return np.where(tot > 0, 100 * up / tot, 50.0) + np.where(tot.isna(), np.nan, 0.0)


def cmo(close, n):
    c = pd.Series(np.asarray(close, float))
    d = c.diff()
    up, dn = d.clip(lower=0).rolling(n).sum(), (-d.clip(upper=0)).rolling(n).sum()
    tot = up + dn
    return (100 * (up - dn) / tot).where(tot > 0, 0.0).where(tot.notna()).to_numpy()


def run_B(o, h, c):
    m = cmo(c, 11)
    trades, t, n = [], 12, len(c)
    while t < n - 1:
        if m[t] < -45:
            e = t + 1
            u = e
            while u < n and not (c[u] > h[u - 1]):
                u += 1
            if u + 1 >= n:
                break
            trades.append((e, u + 1, o[e], o[u + 1], "o", "o"))
            t = u + 1
            continue
        t += 1
    return trades


def run_C(c, typical, vol, o):
    r = wilder_rsi(c, 3)
    ema = pd.Series(c).ewm(span=100, adjust=False).mean().to_numpy()
    vwap = pd.Series(typical * vol).rolling(10).sum().to_numpy() / pd.Series(vol).rolling(10).sum().to_numpy()
    s = np.zeros(len(c), bool)
    for t in range(105, len(c)):
        s[t] = (r[t] < 22 and ema[t] > ema[t - 5] and c[t] <= 0.99 * vwap[t])
    trades, t, n = [], 0, len(c)
    while t < n - 2:
        if s[t]:
            u = t + 2
            while u < n and not (r[u] > 55):
                u += 1
            if u >= n:
                break
            trades.append((t + 1, u, o[t + 1], c[u], "o", "c"))
            t = u
        t += 1
    return trades


def run_D(c, o):
    k = cutler_rsi(c, 3)
    trades, t, n = [], 4, len(c)
    while t < n - 2:
        if k[t] < 10:
            u = t + 1
            while u < n and not (c[u] > c[u - 1]):
                u += 1
            if u + 1 >= n:
                break
            trades.append((t + 1, u + 1, o[t + 1], o[u + 1], "o", "o"))
            t = u + 1
            continue
        t += 1
    return trades


def run_E(dates, o, c):
    return [(i, i, o[i], c[i], "o", "c") for i, d in enumerate(dates) if d.weekday() == 4 and 15 <= d.day <= 21]


def load_etf(path, last="2026-11-20"):
    d = pd.read_csv(path)
    d.columns = [x.strip().lower() for x in d.columns]
    d["date"] = pd.to_datetime(d["date"])
    d = d.dropna(subset=["close"]).sort_values("date").drop_duplicates("date")
    return d[d["date"] <= last].reset_index(drop=True)


def lab_daily(path, etf_dates):
    d = pd.read_csv(path)
    t = pd.to_datetime(d["time"], unit="s", utc=True).dt.tz_convert("America/New_York")
    mins = t.dt.hour * 60 + t.dt.minute
    d = d[(mins >= 570) & (mins < 960)].copy()
    d["date"] = t[d.index].dt.tz_localize(None).dt.normalize()
    d["min"] = mins[d.index]
    g = d.groupby("date")
    day = pd.DataFrame({"open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(), "close": g["close"].last(),
                        "n": g["close"].size(), "first_min": g["min"].min()})
    ok = day[(day["n"] >= 200) & (day["first_min"] <= 574)]
    return ok[ok.index.isin(set(etf_dates))].reset_index()


def qs_member(trades, dates, side, B):
    """Stats as in Study 12 (after costs and financing, whole file), then the hourly arrays for trades inside the grid."""
    r = np.array([side * (px / pe - 1) - 2 * ICOST - FIN * (dates[x] - dates[e]).days for e, x, pe, px, _, _ in trades])
    st = {"trades_whole_file": int(len(r)), "profit_factor": pf(r), "t_stat": tstat(r), "avg_pct": round(100 * float(r.mean()), 3),
          "win_pct": round(100 * float((r > 0).mean()), 1)}
    A = Arr()
    for (e, x, pe, px, _, xk), ri in zip(trades, r):
        t_in = (dates[e] + pd.Timedelta(hours=9, minutes=30)).tz_localize("America/New_York").tz_convert("UTC")
        t_out = (dates[x] + (pd.Timedelta(hours=9, minutes=30) if xk == "o" else pd.Timedelta(hours=15, minutes=59))).tz_localize("America/New_York").tz_convert("UTC")
        mark(A, B, int(gidx(t_in)), int(gidx(t_out)), side, pe, 100.0, ICOST, 100 * ri, False)
    st["trades_in_grid"] = A.n
    return A, st


# ------------------------------------------------------------------ member 5: Gapline ORB (logic copied from claude/gapline_orb.py)
def gapline(lab, A):
    MIN_DIST, TARGET_R, EMA5, EMA_H, GAP_PTS = 0.0003, 1.5, 200, 17, 0.5
    m = pd.read_csv(os.path.join(lab, "data_1m", "NAS100_1m_full.csv.gz"))
    tu = pd.to_datetime(m["time"], unit="s", utc=True)
    m = m[(tu < T1).to_numpy()].copy()
    m["g"] = gidx(tu[m.index]).to_numpy()
    m["ts"] = tu[m.index].dt.tz_convert("America/New_York").dt.tz_localize(None)
    m = m.sort_values("ts").reset_index(drop=True)
    hh = pd.read_csv(os.path.join(lab, "data_new", "NAS100_1h.csv.gz"))
    hu = pd.to_datetime(hh["time"], utc=True)
    hh = hh[(hu < T1).to_numpy()].copy()
    hh["ts"] = hu[hh.index].dt.tz_convert("America/New_York").dt.tz_localize(None)
    hh = hh.sort_values("ts").reset_index(drop=True)
    hh["ema"] = hh["close"].ewm(span=EMA_H, adjust=False).mean()
    h_ts, h_ema = hh["ts"].to_numpy(), hh["ema"].to_numpy()
    m = m[m["ts"].dt.hour * 60 + m["ts"].dt.minute >= 540]
    rows, prev_close, a5 = [], None, 2.0 / (EMA5 + 1)
    for day, g in m.groupby(m["ts"].dt.normalize(), sort=True):
        mins = (g["ts"].dt.hour * 60 + g["ts"].dt.minute).to_numpy()
        o, h, l, c = (g[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        gm = g["g"].to_numpy()
        has_close = (mins == 959).any()
        k = np.searchsorted(h_ts, np.datetime64(day + pd.Timedelta(hours=9)), side="left") - 1
        fresh = k >= EMA_H and (day + pd.Timedelta(hours=9) - pd.Timestamp(h_ts[k])) <= pd.Timedelta(hours=1)
        pos = {int(x): i for i, x in enumerate(mins)}
        if prev_close is not None and fresh and 959 in pos and 570 in pos:
            rb = [pos[x] for x in range(570, 585) if x in pos]
            if len(rb) >= 12:
                last = pos[959]
                r_hi, r_lo = float(max(h[i] for i in rb)), float(min(l[i] for i in rb))
                ema, bars5 = float(h_ema[k]), {}
                for b in range(540, 960, 5):
                    ks = [pos[x] for x in range(b, b + 5) if x in pos]
                    if ks:
                        ema = ema + a5 * (c[ks[-1]] - ema)
                        bars5[b] = (float(c[ks[-1]]), ema)
                dayR, ntr, free_after = 0.0, 0, -1
                if float(o[pos[570]]) - prev_close >= GAP_PTS:
                    for b in range(585, 950, 5):
                        if b not in bars5 or b + 5 < free_after:
                            continue
                        close5, ema_b = bars5[b]
                        if not (close5 > r_hi and close5 > ema_b) or b + 5 not in pos:
                            continue
                        i = pos[b + 5]
                        if i > last:
                            continue
                        entry = float(o[i])
                        dist = entry - r_lo
                        if dist <= 0:
                            continue
                        denom = max(dist, MIN_DIST * entry) / entry
                        target = entry + TARGET_R * dist
                        j, px, kind = last, float(c[last]), "close"
                        for q in range(i, last + 1):
                            if l[q] <= r_lo:
                                j, px, kind = q, float(min(o[q], r_lo)), "stop"
                                break
                            if h[q] >= target:
                                j, px, kind = q, float(target), "target"
                                break
                        R = (px / entry - 1 - 2 * ICOST - (ICOST if kind == "stop" else 0.0)) / denom
                        if gm[j] < NG:                                   # hourly marking from the 1-minute bars
                            for u in np.unique(gm[i:j + 1]):
                                seg = np.arange(i, j + 1)[gm[i:j + 1] == u]
                                low = (float(l[seg].min()) / entry - 1 - ICOST) / denom
                                if u == gm[j]:
                                    A.real[u] += R
                                    A.lo[u] += R if kind == "stop" else min(low, R)
                                else:
                                    fl = (float(c[seg[-1]]) / entry - 1 - ICOST) / denom
                                    A.fc[u] += fl
                                    A.lo[u] += min(low, fl)
                            A.n += 1
                        dayR += R
                        ntr += 1
                        free_after = int(mins[j]) + 1 if kind != "close" else 10 ** 6
                rows.append((day, dayR, ntr))
        prev_close = float(c[mins == 959][-1]) if has_close else None
    tab = pd.DataFrame(rows, columns=["day", "R", "n"])
    d = tab[tab["n"] > 0]
    by = tab.groupby(tab["day"].dt.year)["R"].sum()
    return {"by_year_sum_R": {int(y): round(float(v), 1) for y, v in by.items()},
            "to_2024": {"traded_days": int((d["day"] < "2025-01-01").sum()), "sum_R": round(float(d[d["day"] < "2025-01-01"]["R"].sum()), 1),
                        "t_stat": tstat(d[d["day"] < "2025-01-01"]["R"])},
            "trades_in_grid": A.n, "traded_days": int(len(d)), "sum_R": round(float(d["R"].sum()), 1), "profit_factor": pf(d["R"]), "t_stat": tstat(d["R"])}


# ------------------------------------------------------------------ member 6: MA slope, 50 days, 2 ATR (logic copied from claude/ma_slope.py)
def ma_slope(lab, costs, A):
    N, K, ATR_N, END = 50, 2.0, 14, pd.Timestamp("2026-04-20 21:00", tz="UTC")
    rows, left = [], 0
    for mk in FIFTEEN:
        B = bars(lab, mk)
        keep = (B["t"] < END).to_numpy()
        ts = B["t"][keep].dt.tz_convert("America/New_York").dt.tz_localize(None).to_numpy()
        bo, bh_, bl, bc = (B[x][keep] for x in "ohlc")
        bg = B["g"][keep]
        day = (pd.DatetimeIndex(ts) + pd.Timedelta(hours=7)).normalize()
        codes, uniq = pd.factorize(day)
        first = np.r_[0, np.flatnonzero(np.diff(codes)) + 1]
        last = np.r_[first[1:], len(codes)]
        Do, Dc = bo[first], bc[last - 1]
        Dh, Dl = np.maximum.reduceat(bh_, first), np.minimum.reduceat(bl, first)
        Dday = pd.DatetimeIndex(uniq)
        sma = pd.Series(Dc).rolling(N).mean().to_numpy()
        pc = np.r_[np.nan, Dc[:-1]]
        tr = np.where(np.isnan(pc), Dh - Dl, np.maximum(Dh, pc) - np.minimum(Dl, pc))
        atr = pd.Series(tr).ewm(alpha=1.0 / ATR_N, adjust=False, min_periods=ATR_N).mean().to_numpy()
        up = np.r_[False, sma[1:] > sma[:-1]]
        down = np.r_[False, sma[1:] < sma[:-1]]
        nd, t, cost = len(Dc), N + 1, costs[mk]
        while t < nd - 1:
            if not (up[t] and not up[t - 1] and not np.isnan(sma[t - 2]) and not np.isnan(atr[t])):
                t += 1
                continue
            e = t + 1
            entry, stop = float(Do[e]), float(Dc[t] - K * atr[t])
            if entry <= stop:
                t += 1
                continue
            risk = (entry - stop) / entry
            d, px, kind, xb = e, None, None, None
            while d < nd:
                lo, op = bl[first[d]:last[d]], bo[first[d]:last[d]]
                hit = np.flatnonzero(lo <= stop)
                if len(hit):
                    px, kind, xb = float(min(op[hit[0]], stop)), "stop", first[d] + hit[0]
                    break
                if down[d]:
                    if d + 1 < nd:
                        px, kind, xb = float(Do[d + 1]), "slope", first[d + 1]
                        d += 1
                    break
                stop = max(stop, float(Dc[d] - K * atr[d]))
                d += 1
            if px is None:
                left += 1
                break
            ret = px / entry - 1 - 2 * cost - (cost if kind == "stop" else 0.0)
            nights = int(d - e)
            rows.append({"day": Dday[e], "R": ret / risk, "market": mk, "kind": kind})
            mark(A, B, int(bg[first[e]]), int(bg[xb]), 1, entry, 1.0 / risk, cost, (ret - FIN * nights) / risk, True)
            t = max(d if kind == "stop" else d - 1, e)
    tr = pd.DataFrame(rows)
    v = tr.groupby("day")["R"].mean().to_numpy()
    return {"trades": int(len(tr)), "trades_in_grid": A.n, "left_open": left, "avg_R_per_entry_day": round(float(v.mean()), 4),
            "profit_factor": pf(v), "t_stat": tstat(v)}


# ------------------------------------------------------------------ members 7 to 9: screen-track ideas, on the lab's own engine
def walk(o, h, l, c, d, slf, rr, slip):
    """lab._simulate again in plain Python, keeping the exit bar, exit price and kind of every trade."""
    out, inpos, pend, s, e, f, st, tp, pi, pfv = [], False, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0.0
    for i in range(len(c)):
        if pend != 0 and not inpos:
            s, e, f = pend, o[i], pfv
            st, tp, pi, inpos, pend = e * (1 - s * f), e * (1 + s * f * rr), i, True, 0
        if inpos:
            ex, kind = 0.0, None
            if (s == 1 and l[i] <= st) or (s == -1 and h[i] >= st):
                ex, kind = (min(o[i], st) if s == 1 else max(o[i], st)) * (1 - s * slip), "stop"
            elif (s == 1 and h[i] >= tp) or (s == -1 and l[i] <= tp):
                ex, kind = tp, "target"
            if kind:
                out.append((pi, i, s, e, ex, f, kind))
                inpos = False
        if d[i] != 0:
            if inpos and d[i] != s:
                out.append((pi, i, s, e, c[i], f, "flip"))
                inpos = False
            if not inpos and pend == 0:
                pend, pfv = d[i], slf[i]
    return out


def screen_member(spec, want, screen, lab_mod, data, A):
    am, rr = lab_mod.EXITS[spec["exit"]]
    runs = screen.run_spec(spec, data)
    conf = screen.window_stats(runs, data, screen.in_confirm)
    worst, n_all = 0.0, 0
    for mk, run in runs.items():
        D = data[mk]
        o, h, l, c = D["ohlc"]
        dsig = lab_mod._cooldown(np.ascontiguousarray(screen.signals(spec, D["feats"])), lab_mod.COOLDOWN)
        slf = np.clip(am * D["atrp"], 0.001, 0.20)
        fee, slip = screen.FEES_ALL[mk], lab_mod.SLIPS[mk]
        tr = walk(o.tolist(), h.tolist(), l.tolist(), c.tolist(), dsig.tolist(), slf.tolist(), rr, slip)
        ei, R, sd = run["x1"]
        assert len(tr) == len(ei), (mk, len(tr), len(ei))
        idx = D["df"].index
        g = gidx(idx).to_numpy()
        B = {"g": g, "l": l, "h": h, "c": c}
        dates = idx.normalize()
        for k, (pi, xi, s, e, ex, f, kind) in enumerate(tr):
            r = (s * (ex / e - 1) - fee * (1 + ex / e)) / f
            assert pi == ei[k] and s == sd[k]
            worst = max(worst, abs(r - R[k]))
            nights = (dates[xi] - dates[pi]).days
            mark(A, B, int(g[pi]), int(g[xi]), s, e, 1.0 / f, fee, r - FIN * nights / f, kind == "stop")
        n_all += len(tr)
    return {"trades_all_bars": n_all, "trades_in_grid": A.n, "largest_R_gap_vs_lab_engine": float(worst),
            "confirm_window": {"trades": conf["trades"], "pf": round(conf["pf"], 3), "t": round(conf["t"], 2)}, "watchlist_says": want}


def selftest():
    B = {"g": np.array([10, 11, 12, 14]), "l": np.array([99.0, 97.0, 101.0, 100.0]), "h": np.array([101.0, 100.0, 104.0, 103.0]),
         "c": np.array([100.0, 98.0, 103.0, 102.0])}
    A = Arr()
    assert mark(A, B, 10, 14, 1, 100.0, 100.0, 0.0, 2.0, False)       # long 1x from hour 10 to hour 14, closed +2%
    assert np.allclose(A.fc[10:15], [0.0, -2.0, 3.0, 3.0, 0.0])       # hour 13 has no bar: the last mark carries
    assert np.allclose(A.lo[10:15], [-1.0, -3.0, 1.0, 3.0, 0.0])      # exit hour: min(low 100 -> 0%, closed +2%) = 0
    assert A.real[14] == 2.0 and A.real.sum() == 2.0
    A2 = Arr()
    assert mark(A2, B, 11, 12, -1, 100.0, 50.0, 0.001, -1.5, True)    # short, half size, stopped in hour 12
    assert np.allclose(A2.fc[11:13], [50 * (0.02 - 0.001), 0.0]) and np.allclose(A2.lo[11:13], [50 * (0.0 - 0.001), -1.5])
    assert not mark(Arr(), B, 10, NG, 1, 100.0, 1.0, 0.0, 0.0, False)  # runs past the grid: dropped
    assert str(DAYS[0].date()) == "2021-04-21" and all(d.weekday() < 5 for d in DAYS) and DAY_END[-1] == NG - 1
    A3 = Arr(); g0 = int(DAY_END[3]) - 1                                # a trade open across two firm-day ends
    B3 = {"g": np.arange(g0, g0 + 60), "l": np.full(60, 99.0), "h": np.full(60, 102.0), "c": np.full(60, 101.0)}
    assert mark(A3, B3, g0, int(DAY_END[5]) - 2, 1, 100.0, 100.0, 0.0, 1.0, False)
    assert [(a, b) for a, b, _ in A3.v] == [(3, 4), (4, 4)] and all(abs(f - 1.0) < 1e-9 for _, _, f in A3.v)
    tr = walk([10, 10, 10, 10, 10], [10, 10.1, 13, 10, 10], [10, 9.9, 9.95, 10, 10], [10, 10, 12, 10, 10], [1, 0, 0, 0, 0], [0.1] * 5, 2.0, 0.0)
    assert tr == [(1, 2, 1, 10, 12.0, 0.1, "target")]
    print("selftest OK")


def main():
    if sys.argv[1] == "selftest":
        return selftest()
    lab, etf_dir, out = sys.argv[2:5]
    sys.path.insert(0, lab)
    import costs
    import lab as lab_mod
    import screen
    assert all(costs.COST[k] == ICOST for k in ("NAS100", "SPX500", "USA30"))
    stats = {}

    def save(name, A, st):
        v = np.array(A.v, float).reshape(-1, 3)
        carried = np.zeros(len(DAYS)); np.add.at(carried, v[:, 0].astype(int), v[:, 2])
        assert np.allclose(carried, A.fc[DAY_END], atol=1e-9), name      # open profit at each day end equals the sum over the trades open then
        np.savez_compressed(os.path.join(out, name + ".npz"), real=A.real, fc=A.fc, lo=A.lo, v=v)
        stats[name] = st
        print(name, json.dumps(st), flush=True)

    spy, qqq = load_etf(f"{etf_dir}/SPY.csv"), load_etf(f"{etf_dir}/QQQ.csv")
    spx = lab_daily(f"{lab}/data_1m/SPX500_1m_full.csv.gz", spy["date"])
    nas = lab_daily(f"{lab}/data_1m/NAS100_1m_full.csv.gz", qqq["date"]).merge(qqq[["date", "volume"]], on="date", how="left")
    xd, xo, xh, xc = list(spx["date"]), *(spx[k].to_numpy(float) for k in ("open", "high", "close"))
    nd, no, nh, nl, nc, nv = list(nas["date"]), *(nas[k].to_numpy(float) for k in ("open", "high", "low", "close", "volume"))
    Bn, Bs = bars(lab, "NAS100"), bars(lab, "SPX500")
    save("1_cutler_D", *qs_member(run_D(nc, no), nd, 1, Bn))
    save("2_cmo_B", *qs_member(run_B(xo, xh, xc), xd, 1, Bs))
    save("3_rsi_ema_vwap_C", *qs_member(run_C(nc, (nh + nl + nc) / 3, nv, no), nd, 1, Bn))
    save("4_third_friday_E", *qs_member(run_E(nd, no, nc), nd, -1, Bn))
    A = Arr(); st = gapline(lab, A); save("5_gapline_orb", A, st)
    A = Arr(); st = ma_slope(lab, costs.COST, A); save("6_ma_slope", A, st)
    screen.load_registry()
    data = screen.load()
    watch = {w["id"]: w for w in json.load(open(os.path.join(lab, "forward", "watchlist.json")))}
    for name, wid in (("7_gtja118", "c9e430d9cc"), ("8_streak_k5", "b120889724"), ("9_a158_rsqr", "35a2c2e4a1")):
        A = Arr()
        st = screen_member(watch[wid]["spec"], watch[wid]["confirm"], screen, lab_mod, data, A)
        st["idea"] = watch[wid]["name"]
        save(name, A, st)
    np.savez(os.path.join(out, "days.npz"), days=DAYS.strftime("%Y-%m-%d").to_numpy(), first=DAY_FIRST, end=DAY_END)
    json.dump(stats, open(os.path.join(out, "members.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
