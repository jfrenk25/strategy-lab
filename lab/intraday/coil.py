"""Intraday study 6: Coil Reclaim, a first-hour breakout with a pullback entry. One run.

Run from the repo root:
    python lab/intraday/coil.py --dryrun    # same code on made-up prices with no cost; nothing is written
    python lab/intraday/coil.py             # the one real run; refuses to run a second time

The rules are in LAB_RULES.md under "Intraday study 6". They were written and pushed before this file existed.
Source of the rule: github.com/Allencake/coil-reclaim-indicator (MIT), `coil_reclaim.pine`, default settings.
The logic below is written from that script's rules in the lab's own code. Comments name the script's steps.
"""
import sys, os, json, datetime
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
RESULTS = os.path.join(HERE, "coil_results.json")
MARKETS = ["NAS100", "SPX500", "USA30"]
H1_DIR = {"NAS100": "data_new", "SPX500": "data_new", "USA30": "data"}
COST = 0.00005                                              # 0.005% of price per round trip
START, END = datetime.date(2021, 6, 1), datetime.date(2026, 11, 19)
WIN_OPEN, WIN_END = 9 * 60 + 30, 10 * 60 + 30               # bars that open from 9:30 to 10:25
PASS = dict(days=150, t=2.58, pf=1.15, markets_ok=2, years=(2021, 2022, 2023, 2024, 2025, 2026), years_ok=4)
P = dict(at_pad=0.25, clean_min_bars=3, clean_min_atr=1.5, clean_keep=8, ran_body=0.60, ran_atr=1.0, pull_depth=0.382,
         range_max=20, range_min=3, opp_min=2, range_min_atr=0.5, range_max_atr=4.0, bo_body=0.50, bo_max=0.50,
         wick_atr=0.10, wick_pct=0.20, expire=6, max_trades=2, partial=0.5, cap_r=3.0, fast_r=1.5, fast_bars=3, max_minutes=240)
NAN = float("nan")


# ---------------------------------------------------------------- data

def fake_minutes(seed):
    """Made-up 24-hour 1-minute prices, Sunday 18:00 to Friday 17:00 New York time, with the daily 17:00 break."""
    rng = np.random.default_rng(seed)
    t = pd.date_range("2021-04-20 22:00", "2026-11-20 21:14", freq="min", tz="UTC")
    ny = t.tz_convert("America/New_York")
    wd, hr = ny.dayofweek.to_numpy(), ny.hour.to_numpy()
    keep = ~((wd == 5) | ((wd == 6) & (hr < 18)) | ((wd == 4) & (hr >= 17)) | (hr == 17))
    t = t[keep]; n = len(t)
    steps = rng.normal(0, 0.0002, (n, 4)).cumsum(axis=1)
    base = np.r_[0.0, steps[:-1, -1].cumsum()]
    path = 15000 * np.exp(base[:, None] + steps)
    o = np.r_[15000.0, path[:-1, -1]]
    return pd.DataFrame({"time": t, "open": o, "high": np.maximum(o, path.max(axis=1)), "low": np.minimum(o, path.min(axis=1)), "close": path[:, -1]})


def load(m, fake_seed=None):
    """Returns (minute bars from 8:00 to 16:14 New York time, hourly bars for the whole day)."""
    if fake_seed is not None:
        mn = fake_minutes(fake_seed)
        hr = mn.set_index("time").resample("1h").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna().reset_index()
        ny = mn["time"].dt.tz_convert("America/New_York"); mod = ny.dt.hour * 60 + ny.dt.minute
        mn = mn[(mod >= 8 * 60) & (mod < 16 * 60 + 15)].reset_index(drop=True)
    else:
        mn = pd.read_csv(os.path.join(LAB, "data_1m", f"{m}_1m_full.csv.gz")); mn["time"] = pd.to_datetime(mn["time"], unit="s", utc=True)
        hr = pd.read_csv(os.path.join(LAB, H1_DIR[m], f"{m}_1h.csv.gz")); hr["time"] = pd.to_datetime(hr["time"], utc=True)
    return mn.sort_values("time").reset_index(drop=True), hr.sort_values("time").reset_index(drop=True)


def wilder_atr(h, l, c, n=14, prev_close=True):
    tr = h - l
    if prev_close and len(h) > 1:
        tr = np.r_[tr[0], np.maximum(tr[1:], np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))]
    out = np.full(len(h), NAN)
    if len(h) >= n:
        out[n - 1] = tr[:n].mean()
        for i in range(n, len(h)):
            out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def level_states(o, c):
    """Ceiling: an up candle then a down candle, at the higher body. Floor: the mirror. Broken by a close beyond it.
    Returns the two most recent unbroken ceilings and floors as they stand after each bar."""
    n = len(o); out = np.full((n, 4), NAN); c1 = c2 = f1 = f2 = NAN
    for i in range(n):
        if i > 0:
            if c[i - 1] > o[i - 1] and c[i] < o[i]:
                c2 = c1; c1 = max(o[i], c[i], o[i - 1], c[i - 1])
            if c[i - 1] < o[i - 1] and c[i] > o[i]:
                f2 = f1; f1 = min(o[i], c[i], o[i - 1], c[i - 1])
        if c1 == c1 and c[i] > c1: c1 = NAN
        if c2 == c2 and c[i] > c2: c2 = NAN
        if f1 == f1 and c[i] < f1: f1 = NAN
        if f2 == f2 and c[i] < f2: f2 = NAN
        out[i] = (c1, c2, f1, f2)
    return out


def stair_codes(h, l, n=2):
    """Last two swing highs and lows (a swing needs n lower/higher bars each side). 1 up, -1 down, 2 sideways, 0 unknown."""
    out = np.zeros(len(h), dtype=int); h0 = h1 = l0 = l1 = NAN
    for i in range(len(h)):
        j = i - n
        if j - n >= 0:
            wh = h[j - n:j + n + 1]; wl = l[j - n:j + n + 1]
            if h[j] == wh.max() and (wh == h[j]).sum() == 1: h1, h0 = h0, h[j]
            if l[j] == wl.min() and (wl == l[j]).sum() == 1: l1, l0 = l0, l[j]
        if h1 != h1 or l1 != l1: out[i] = 0
        elif h0 > h1 and l0 > l1: out[i] = 1
        elif h0 < h1 and l0 < l1: out[i] = -1
        else: out[i] = 2
    return out


def higher_timeframes(hr):
    """Daily (17:00 to 17:00 New York), 4-hour (from 17:00), 1-hour and weekly candles from the hourly bars."""
    ny = hr["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    shifted = ny - pd.Timedelta(hours=17)
    keys = {"h1": ny.dt.floor("h"), "h4": shifted.dt.floor("4h") + pd.Timedelta(hours=17), "d": (ny + pd.Timedelta(hours=7)).dt.normalize()}
    keys["w"] = keys["d"] - pd.to_timedelta(keys["d"].dt.dayofweek, unit="D")
    out = {}
    for tf, k in keys.items():
        g = hr.assign(k=k.to_numpy()).groupby("k", sort=True).agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"), n=("open", "size"))
        o, h, l, c = (g[x].to_numpy(dtype=float) for x in ("open", "high", "low", "close"))
        d = dict(key=g.index.to_numpy(), o=o, h=h, l=l, c=c, n=g["n"].to_numpy())
        if tf in ("d", "h4"): d["atr"] = wilder_atr(h, l, c)
        if tf in ("d", "h4", "h1"): d["lv"] = level_states(o, c)
        if tf in ("d", "w"): d["stair"] = stair_codes(h, l)
        out[tf] = d
    return out


def five_minute_days(mn):
    """Per New York day: 5-minute bars from the minute bars, each with the rows of its minutes."""
    ny = mn["time"].dt.tz_convert("America/New_York").dt.tz_localize(None)
    mod = (ny.dt.hour * 60 + ny.dt.minute).to_numpy(); day = ny.dt.normalize().to_numpy(); slot = mod // 5 * 5
    o, h, l, c = (mn[x].to_numpy(dtype=float) for x in ("open", "high", "low", "close"))
    days = []
    bounds = np.r_[0, np.flatnonzero(day[1:] != day[:-1]) + 1, len(day)]
    for a, b in zip(bounds[:-1], bounds[1:]):
        s = slot[a:b]; cut = np.r_[0, np.flatnonzero(s[1:] != s[:-1]) + 1, b - a] + a
        lo, hi = cut[:-1], cut[1:]
        days.append(dict(day=pd.Timestamp(day[a]), slot=slot[lo], o=o[lo], h=np.array([h[x:y].max() for x, y in zip(lo, hi)]),
                         l=np.array([l[x:y].min() for x, y in zip(lo, hi)]), c=c[hi - 1], lo=lo, hi=hi,
                         minutes_early=int(((mod[a:b] >= 480) & (mod[a:b] < 630)).sum())))
    return days, (o, h, l, c)


# ---------------------------------------------------------------- the rule

def find_range(o, c, i, direction, atr):
    """The script's findRange: the longest look-back (3 to 20 bars, same day) whose bodies form a range the bar closes beyond."""
    if direction == 0 or atr != atr:
        return None
    top = bot = None; opp = 0; best = None
    for k in range(1, P["range_max"] + 1):
        j = i - k
        if j < 0:
            break
        bt, bb = max(o[j], c[j]), min(o[j], c[j])
        top = bt if top is None else max(top, bt); bot = bb if bot is None else min(bot, bb)
        if (direction == 1 and c[j] < o[j]) or (direction == -1 and c[j] > o[j]):
            opp += 1
        if top - bot > P["range_max_atr"] * atr:
            break
        beyond = c[i] > top if direction == 1 else c[i] < bot
        if k >= P["range_min"] and opp >= P["opp_min"] and top - bot >= P["range_min_atr"] * atr and beyond:
            best = (k, top, bot)
    return best


def straight_run(o, c, i, direction, n):
    if i - n < 0:
        return False
    for k in range(n):
        up = c[i - k] > c[i - k - 1] and c[i - k] > o[i - k]; dn = c[i - k] < c[i - k - 1] and c[i - k] < o[i - k]
        if not (up if direction == 1 else dn):
            return False
    return True


def nearest_level(side, from_px, levels):
    """Nearest unbroken ceiling at or above from_px (side 1) or floor at or below it (side -1), over daily, 4-hour and 1-hour."""
    best = NAN
    for lv in levels:
        for x in ((lv[0], lv[1]) if side == 1 else (lv[2], lv[3])):
            if x == x and (x >= from_px if side == 1 else x <= from_px):
                if best != best or (x < best if side == 1 else x > best):
                    best = x
    return best


def simulate(mn, hr, fill):
    """fill 'A': the indicator's own bookkeeping. fill 'B': as it could be traded. Returns (trades, counts)."""
    days, (m_o, m_h, m_l, m_c) = five_minute_days(mn)
    tf = higher_timeframes(hr)
    trades = []; counts = dict(orders=0, no_pullback=0, back_inside=0, expired=0, day_end_order=0, skipped_days=0, used_days=0,
                               skip_blocked=0, skip_big_bar=0, skip_wait_pullback=0, skip_not_clean=0, forced_close=0)
    bias = 0; zones = []; prev_h4c1 = prev_h4f1 = prev_h1c1 = prev_h1f1 = NAN
    tick = 1e-9
    for D in days:
        o, h, l, c, slot = D["o"], D["h"], D["l"], D["c"], D["slot"]; n = len(o)
        atr_all = wilder_atr(h, l, c)
        t_open = D["day"].to_datetime64() + slot.astype("timedelta64[m]")
        # the last finished candle of each timeframe, as seen from each bar's open time
        i_d = np.searchsorted(tf["d"]["key"], (D["day"] + pd.Timedelta(0)).to_datetime64(), "left") - 1       # 8:00 to 16:14 lies in one trading day
        i_w = np.searchsorted(tf["w"]["key"], (D["day"] - pd.Timedelta(days=D["day"].dayofweek)).to_datetime64(), "left") - 1
        b4 = (pd.DatetimeIndex(t_open) - pd.Timedelta(hours=17)).floor("4h") + pd.Timedelta(hours=17)
        i_h4 = np.searchsorted(tf["h4"]["key"], b4.to_numpy(), "left") - 1
        i_h1 = np.searchsorted(tf["h1"]["key"], pd.DatetimeIndex(t_open).floor("h").to_numpy(), "left") - 1
        pre_key = D["day"].to_datetime64() + np.timedelta64(5, "h")
        k_pre = np.searchsorted(tf["h4"]["key"], pre_key, "left")
        pre_ok = k_pre < len(tf["h4"]["key"]) and tf["h4"]["key"][k_pre] == pre_key and tf["h4"]["n"][k_pre] == 4
        early = set(slot[(slot >= 480) & (slot < 630)].tolist())
        usable = (START <= D["day"].date() <= END and i_d >= 14 and pre_ok and D["minutes_early"] >= 135 and len(early) == 30)
        if START <= D["day"].date() <= END:
            counts["used_days" if usable else "skipped_days"] += 1
        lv_d = tf["d"]["lv"][i_d] if i_d >= 0 else (NAN,) * 4
        d_atr = tf["d"]["atr"][i_d] if i_d >= 0 else NAN
        d_dir = 0 if i_d < 0 else int(np.sign(tf["d"]["c"][i_d] - tf["d"]["o"][i_d]))
        sw = tf["w"]["stair"][i_w] if i_w >= 0 else 0
        stair = sw if sw != 0 else (tf["d"]["stair"][i_d] if i_d >= 0 else 0)
        pad = (d_atr if d_atr == d_atr else 0.0) * P["at_pad"]
        blocked = False; run_dir = 0; run_cnt = opp_run = 0; run_start = run_ext = NAN
        state = 0; sess_trades = 0; started = False; mode = "BREAKOUT"; pre = None
        T = {}
        for i in range(n):
            atr = atr_all[i]
            lv_h4 = tf["h4"]["lv"][i_h4[i]] if i_h4[i] >= 0 else (NAN,) * 4
            lv_h1 = tf["h1"]["lv"][i_h1[i]] if i_h1[i] >= 0 else (NAN,) * 4
            levels = (lv_d, lv_h4, lv_h1)
            cdir = 1 if c[i] > o[i] else -1 if c[i] < o[i] else 0
            crng = h[i] - l[i]; cbody = abs(c[i] - o[i])
            at_ceil = (lv_d[0] == lv_d[0] and c[i] >= lv_d[0] - pad) or (lv_d[1] == lv_d[1] and c[i] >= lv_d[1] - pad)
            at_floor = (lv_d[2] == lv_d[2] and c[i] <= lv_d[2] + pad) or (lv_d[3] == lv_d[3] and c[i] <= lv_d[3] + pad)
            in_win = WIN_OPEN <= slot[i] < WIN_END
            win_start = in_win and not started
            rng = find_range(o, c, i, bias, atr)                 # the script computes this before the bar's own updates
            straight = {1: straight_run(o, c, i, 1, P["fast_bars"]), -1: straight_run(o, c, i, -1, P["fast_bars"])}

            # clean zones: a run of same-colour bars; one opposite bar is a pause, two end it
            if cdir != 0:
                if run_dir == 0:
                    run_dir, run_cnt, run_start, run_ext, opp_run = cdir, 1, o[i], c[i], 0
                elif cdir == run_dir:
                    run_cnt += 1; run_ext = max(run_ext, c[i]) if run_dir == 1 else min(run_ext, c[i]); opp_run = 0
                else:
                    opp_run += 1
                    if opp_run >= 2:
                        if run_cnt >= P["clean_min_bars"] and atr == atr and abs(run_ext - run_start) >= P["clean_min_atr"] * atr:
                            zones.append((max(run_start, run_ext), min(run_start, run_ext)))
                            if len(zones) > P["clean_keep"]:
                                zones.pop(0)
                        run_dir, run_cnt, run_start, run_ext, opp_run = cdir, 2, o[i - 1], c[i], 0
            for now, before in ((lv_h4[0], prev_h4c1), (lv_h4[2], prev_h4f1), (lv_h1[0], prev_h1c1), (lv_h1[2], prev_h1f1)):
                if now == now and before == before and now != before:      # a new level inside a zone (8% margin) drops the zone
                    zones = [(t, b) for (t, b) in zones if not (b + (t - b) * 0.08 < now < t - (t - b) * 0.08)]
            prev_h4c1, prev_h4f1, prev_h1c1, prev_h1f1 = lv_h4[0], lv_h4[2], lv_h1[0], lv_h1[2]

            def in_clean(px):
                return any(b <= px <= t for (t, b) in zones)

            # direction, fixed on the window's first bar
            if win_start:
                started = True; sess_trades = 0
                k4 = i_h4[i]
                h4_dir = 0 if k4 < 0 else int(np.sign(tf["h4"]["c"][k4] - tf["h4"]["o"][k4]))
                pre = None if k4 < 0 else (tf["h4"]["o"][k4], tf["h4"]["h"][k4], tf["h4"]["l"][k4], tf["h4"]["c"][k4], tf["h4"]["atr"][k4])
                if d_dir != 0 and d_dir == h4_dir: bias = d_dir
                elif at_ceil and not at_floor: bias = -1
                elif at_floor and not at_ceil: bias = 1
                elif stair == 1: bias = 1
                elif stair == -1: bias = -1
                else: bias = d_dir if d_dir != 0 else h4_dir
                mode = "BREAKOUT"
                if pre is not None and bias != 0:
                    po, ph, pl, pc, patr = pre; pr = ph - pl
                    ran = pr > 0 and abs(pc - po) >= P["ran_body"] * pr and pr >= P["ran_atr"] * (patr if patr == patr else 0.0)
                    if ran and int(np.sign(pc - po)) == bias:
                        mode = "PULLBACK"
            if in_win and ((bias == 1 and at_ceil) or (bias == -1 and at_floor)):
                blocked = True

            # a working order: pullback first, then the fill
            just_filled = False
            if state == 1 and i > T["ord_bar"]:
                s = T["side"]
                wick = (min(o[i], c[i]) - l[i]) if s == 1 else (h[i] - max(o[i], c[i]))
                wick_ok = atr == atr and wick >= P["wick_atr"] * atr and crng > 0 and wick >= P["wick_pct"] * crng
                hit = h[i] >= T["ord_px"] if s == 1 else l[i] <= T["ord_px"]
                same_bar = wick_ok and (o[i] < T["ord_px"] if s == 1 else o[i] > T["ord_px"])
                entry = None; stopped_in_bar = False
                if hit:
                    if T["dip"]:                                 # a resting order: both fills agree on the price
                        entry = max(o[i], T["ord_px"]) if s == 1 else min(o[i], T["ord_px"])
                        if fill == "B":                          # the 1-minute bars decide whether the stop went in the same bar
                            filled = False
                            for q in range(D["lo"][i], D["hi"][i]):
                                if not filled:
                                    if (m_h[q] >= T["ord_px"]) if s == 1 else (m_l[q] <= T["ord_px"]):
                                        filled = True
                                        if (m_c[q] <= T["ord_sl"]) if s == 1 else (m_c[q] >= T["ord_sl"]):
                                            stopped_in_bar = True; break
                                elif (m_l[q] <= T["ord_sl"]) if s == 1 else (m_h[q] >= T["ord_sl"]):
                                    stopped_in_bar = True; break
                    elif same_bar:
                        if fill == "A":
                            entry = max(o[i], T["ord_px"]) if s == 1 else min(o[i], T["ord_px"])
                        elif (c[i] >= T["ord_px"]) if s == 1 else (c[i] <= T["ord_px"]):
                            entry = c[i]                         # known only at the close, so that is the price
                        else:
                            T["dip"] = True                      # touched and fell back: the order rests from here
                    else:
                        state = 0; counts["no_pullback"] += 1
                else:
                    if wick_ok:
                        T["dip"] = True
                    elif (c[i] < T["r_top"]) if s == 1 else (c[i] > T["r_bot"]):
                        state = 0; counts["back_inside"] += 1
                    elif i - T["ord_bar"] >= P["expire"]:
                        state = 0; counts["expired"] += 1
                if entry is not None:
                    risk = abs(entry - T["ord_sl"]); tp1 = entry + s * risk
                    tg = nearest_level(s, tp1, levels); cap = entry + s * P["cap_r"] * risk
                    target = cap if (tg != tg or (tg > cap if s == 1 else tg < cap)) else tg
                    pl_ = nearest_level(s, entry + s * tick, levels)
                    T.update(entry=entry, stop=T["ord_sl"], risk=risk, tp1=tp1, target=target, be=False, hit1r=False, banked=0.0,
                             pre_lvl=pl_ if (pl_ == pl_ and (pl_ < tp1 if s == 1 else pl_ > tp1)) else NAN, entry_slot=int(slot[i]), entry_i=i)
                    state = 2; sess_trades += 1; just_filled = True

            # an open trade
            if state == 2:
                s = T["side"]; ex = None; why = ""
                if just_filled:
                    if fill == "A":
                        if (c[i] <= T["stop"]) if s == 1 else (c[i] >= T["stop"]):
                            ex, why = T["stop"], "stop"
                    elif stopped_in_bar:
                        ex, why = T["stop"], "stop"
                else:
                    if (l[i] <= T["stop"]) if s == 1 else (h[i] >= T["stop"]):
                        ex = min(o[i], T["stop"]) if s == 1 else max(o[i], T["stop"]); why = "breakeven" if T["be"] else "stop"
                    else:
                        if not T["hit1r"] and ((h[i] >= T["tp1"]) if s == 1 else (l[i] <= T["tp1"])):
                            T["hit1r"] = True; T["banked"] = P["partial"]; T["stop"] = T["entry"]; T["be"] = True
                        if not T["be"] and T["pre_lvl"] == T["pre_lvl"] and ((h[i] >= T["pre_lvl"]) if s == 1 else (l[i] <= T["pre_lvl"])):
                            T["stop"] = T["entry"]; T["be"] = True
                        if (h[i] >= T["target"]) if s == 1 else (l[i] <= T["target"]):
                            ex, why = T["target"], "target"
                        if ex is None and T["risk"] > 0 and s * (c[i] - T["entry"]) / T["risk"] >= P["fast_r"] and straight[s]:
                            ex, why = c[i], "too_fast"
                        if ex is None and int(slot[i]) - T["entry_slot"] >= P["max_minutes"]:
                            ex, why = c[i], "time"
                if ex is None and i == n - 1:
                    ex, why = c[i], "day_end"; counts["forced_close"] += 1
                if ex is not None:
                    r = T["banked"] + (1 - T["banked"]) * s * (ex - T["entry"]) / T["risk"] if T["risk"] > 0 else 0.0
                    trades.append(dict(day=D["day"].date(), side=s, r=float(r), cost_r=float(T["entry"] / T["risk"]) if T["risk"] > 0 else 0.0,
                                       why=why, hit1r=bool(T["hit1r"]), entry_slot=T["entry_slot"]))
                    state = 0
            if state == 1 and i == n - 1:
                state = 0; counts["day_end_order"] += 1

            # look for the breakout bar
            if (state == 0 and not just_filled and usable and in_win and bias != 0 and sess_trades < P["max_trades"] and rng is not None
                    and cdir == bias and crng > 0 and cbody >= P["bo_body"] * crng):
                k, top, bot = rng; height = top - bot
                pull_ok = True
                if mode == "PULLBACK" and pre is not None:
                    _, ph, pl, _, _ = pre
                    pull_ok = (bot <= ph - P["pull_depth"] * (ph - pl)) if bias == 1 else (top >= pl + P["pull_depth"] * (ph - pl))
                if blocked: counts["skip_blocked"] += 1
                elif crng > P["bo_max"] * height: counts["skip_big_bar"] += 1
                elif not pull_ok: counts["skip_wait_pullback"] += 1
                elif not in_clean(h[i] if bias == 1 else l[i]): counts["skip_not_clean"] += 1
                else:
                    T = dict(side=bias, r_top=top, r_bot=bot, ord_px=h[i] if bias == 1 else l[i], ord_sl=l[i] if bias == 1 else h[i], ord_bar=i, dip=False)
                    state = 1; counts["orders"] += 1
    return trades, counts


# ---------------------------------------------------------------- statistics

def daily(tr, mult=1.0, cost=COST):
    """One number per day: each market's trades added up, then the average across the markets that traded."""
    if tr.empty:
        return pd.Series(dtype=float)
    net = tr["r"] - mult * cost * tr["cost_r"]
    return net.groupby([tr["day"], tr["market"]]).sum().groupby(level=0).mean()


def stats(x):
    x = np.asarray(x, dtype=float); n = len(x)
    if n == 0:
        return dict(n=0, mean=0.0, t=0.0, pf=0.0, win=0.0, total=0.0)
    sd = x.std(ddof=1) if n > 1 else 0.0; pos = x[x > 0].sum(); neg = -x[x < 0].sum()
    return dict(n=n, mean=float(x.mean()), t=float(x.mean() / (sd / np.sqrt(n))) if sd > 0 else 0.0,
                pf=float(pos / neg) if neg > 0 else float("inf"), win=float((x > 0).mean()), total=float(x.sum()))


def report(tr, cost=COST):
    d = daily(tr, 1.0, cost); s = stats(d)
    d2 = daily(tr, 2.0, cost)
    net = tr["r"] - cost * tr["cost_r"] if not tr.empty else pd.Series(dtype=float)
    yr = {y: float(d[[k.year == y for k in d.index]].sum()) for y in PASS["years"]} if len(d) else {}
    mk = {m: stats(daily(tr[tr["market"] == m], 1.0, cost)) for m in MARKETS} if not tr.empty else {}
    long_s = stats(net[tr["side"] == 1]) if not tr.empty else stats([]); short_s = stats(net[tr["side"] == -1]) if not tr.empty else stats([])
    checks = {
        "at least 150 traded days": s["n"] >= PASS["days"],
        "average above zero with t-stat >= 2.58": s["mean"] > 0 and s["t"] >= PASS["t"],
        "profit factor >= 1.15": s["pf"] >= PASS["pf"],
        "average above zero at double cost": len(d2) > 0 and d2.mean() > 0,
        "positive on two of three markets": sum(1 for m in mk.values() if m["mean"] > 0) >= PASS["markets_ok"],
        "positive in four of six years": sum(1 for v in yr.values() if v > 0) >= PASS["years_ok"],
        "longs and shorts each above zero": long_s["n"] > 0 and short_s["n"] > 0 and long_s["mean"] > 0 and short_s["mean"] > 0,
    }
    return dict(days=s, double_cost_mean=float(d2.mean()) if len(d2) else 0.0, by_year=yr, by_market=mk, longs=long_s, shorts=short_s,
                trades=int(len(tr)), trade_stats=stats(net), gross_trade_mean=float(tr["r"].mean()) if not tr.empty else 0.0,
                avg_cost_r=float((cost * tr["cost_r"]).mean()) if not tr.empty else 0.0,
                endings=tr["why"].value_counts().to_dict() if not tr.empty else {}, reached_1r=float(tr["hit1r"].mean()) if not tr.empty else 0.0,
                checks=checks, passed=bool(all(checks.values())))


def main():
    dry = "--dryrun" in sys.argv
    if not dry and os.path.exists(RESULTS):
        sys.exit("This study has already run. Its result is in lab/intraday/coil_results.json and the journal. It runs once.")
    cost = 0.0 if dry else COST
    out = {}
    for fill in ("A", "B"):
        rows = []; cnt = {}
        for k, m in enumerate(MARKETS):
            mn, hr = load(m, fake_seed=100 + k if dry else None)
            tr, c = simulate(mn, hr, fill)
            for t in tr:
                t["market"] = m
            rows += tr; cnt[m] = c
        tr = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["day", "side", "r", "cost_r", "why", "hit1r", "entry_slot", "market"])
        out[fill] = report(tr, cost); out[fill]["counts"] = cnt
        r = out[fill]; s = r["days"]
        print(f"fill {fill}: {r['trades']} trades on {s['n']} days · day average {s['mean']:+.4f}R · t-stat {s['t']:.2f} · profit factor {s['pf']:.2f} · "
              f"trade win rate {r['trade_stats']['win']:.0%} · gross per trade {r['gross_trade_mean']:+.4f}R · cost per trade {r['avg_cost_r']:.4f}R")
        print(f"   by year {{{', '.join(f'{y}: {v:+.1f}' for y, v in r['by_year'].items())}}} · by market {{{', '.join(f'{m}: {v['mean']:+.4f} ({v['n']} days)' for m, v in r['by_market'].items())}}}")
        print(f"   longs {r['longs']['n']} avg {r['longs']['mean']:+.4f} · shorts {r['shorts']['n']} avg {r['shorts']['mean']:+.4f} · double cost {r['double_cost_mean']:+.4f} · endings {r['endings']} · reached 1R {r['reached_1r']:.0%}")
        tot = {k: sum(c[k] for c in cnt.values()) for k in next(iter(cnt.values()))}
        print(f"   counts {tot}")
    v = out["B"]
    verdict = "PASS" if v["passed"] else ("FAIL (too few trades)" if not v["checks"]["at least 150 traded days"] else "FAIL")
    out["verdict"] = verdict
    failed = [k for k, ok in v["checks"].items() if not ok]
    print(("DRY RUN on made-up prices, no cost. " if dry else "") + f"Verdict on fill B: {verdict}" + (f" · failed: {'; '.join(failed)}" if failed else ""))
    if not dry:
        out["run_date"] = datetime.date.today().isoformat()
        json.dump(out, open(RESULTS, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
