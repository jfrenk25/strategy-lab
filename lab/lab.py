"""Strategy lab: every idea is rejected unless it passes every check in LAB_RULES.md.

Run from the repo root:
    python lab/lab.py            # test every idea in lab/ideas that has not been tested yet
    python lab/lab.py NAME       # test one idea by file name (still counts as an attempt)

An idea is a file in lab/ideas with:
    IDEA = dict(name=..., source=..., reason=..., loser=..., grid=[{...}, ...])   # at most 12 parameter sets
    def signals(df, p) -> integer array, +1 long / -1 short / 0 none, decided at each bar's close
"""
import sys, os, json, hashlib, importlib.util, datetime
from statistics import NormalDist
import numpy as np
import pandas as pd
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
FEES = {"BTCUSD": 0.0003, "ETHUSD": 0.0004, "XAUUSD": 0.0002, "GBPJPY": 0.00015, "USA30": 0.00025, "DEU30": 0.00025}   # per side
EXTRA_FEES = {"NAS100": 0.00025, "SPX500": 0.00025, "USOIL": 0.0003, "EURUSD": 0.00015, "GBPUSD": 0.00015,
              "USDJPY": 0.00015, "AUDUSD": 0.00015, "USDCAD": 0.00015, "EURJPY": 0.00015}    # the nine markets in lab/data_new
ALL_FEES = {**FEES, **EXTRA_FEES}
SLIP, COOLDOWN = 0.0002, 6
EXITS = [(2.0, 1.5), (2.0, 2.5), (3.0, 1.5), (3.0, 2.5)]       # (stop in ATRs, target as a multiple of the stop)
QUARANTINE = 2026                                             # block held back; an idea may touch it once
MIN_TRAIN_TRADES, MAX_GRID = 20, 12
T = dict(pf=1.15, trades=150, block_share=0.60, market_share=0.50, random_pct=95.0, q_trades=20, perm_p=0.01, neighbour_share=2 / 3)
N_PERM = 200


def _path(m):
    return os.path.join(HERE, "data_new" if m in EXTRA_FEES else "data", f"{m}_1h.csv.gz")


def load_market(m):
    df = pd.read_csv(_path(m), parse_dates=["time"]).set_index("time")
    idx = df.index
    block = np.where((idx.month > 4) | ((idx.month == 4) & (idx.day >= 21)), idx.year, idx.year - 1).astype(np.int64)
    pc = df["close"].shift(1)
    tr = pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)
    atrp = (tr.rolling(14, min_periods=14).mean() / df["close"]).fillna(0.01).to_numpy()
    return df, block, atrp


@njit(cache=True)
def _cooldown(d, n):
    rem = 0
    for i in range(len(d)):
        if rem > 0: d[i] = 0; rem -= 1
        elif d[i] != 0: rem = n
    return d


@njit(cache=True)
def _simulate(o, h, l, c, d, slf, rr, fee, slip):
    """Entry at the next bar's open. Stops and targets on highs and lows. Gaps fill at the open.
    Stop first if both fall in one bar. An opposite signal closes the trade at that bar's close."""
    n = len(c); ei = np.empty(n, np.int64); R = np.empty(n); sd = np.empty(n, np.int64); k = 0
    inpos = False; s = 0; e = 0.0; f = 0.0; st = 0.0; tp = 0.0; pi = 0; pend = 0; pf = 0.0
    for i in range(n):
        if pend != 0 and not inpos:
            s = pend; e = o[i]; f = pf; st = e * (1 - s * f); tp = e * (1 + s * f * rr); pi = i; inpos = True; pend = 0
        if inpos:
            ex = 0.0
            if (s == 1 and l[i] <= st) or (s == -1 and h[i] >= st):
                ex = (min(o[i], st) if s == 1 else max(o[i], st)) * (1 - s * slip)
            elif (s == 1 and h[i] >= tp) or (s == -1 and l[i] <= tp):
                ex = tp
            if ex != 0.0:
                ei[k] = pi; R[k] = (s * (ex / e - 1) - fee * (1 + ex / e)) / f; sd[k] = s; k += 1; inpos = False
        if d[i] != 0:
            if inpos and d[i] != s:
                ei[k] = pi; R[k] = (s * (c[i] / e - 1) - fee * (1 + c[i] / e)) / f; sd[k] = s; k += 1; inpos = False
            if not inpos and pend == 0:
                pend = d[i]; pf = slf[i]
    return ei[:k], R[:k], sd[:k]


@njit(cache=True)
def _random(o, h, l, lo, hi, sides, slf, rr, fee, slip, nruns, seed):
    np.random.seed(seed); out = np.empty(nruns); n = len(o)
    for r in range(nruns):
        tot = 0.0
        for t in range(len(sides)):
            i = lo + np.random.randint(max(hi - lo - 1, 1)); s = sides[t]; e = o[i]; f = slf[i]; st = e * (1 - s * f); tp = e * (1 + s * f * rr); ex = 0.0
            for m in range(i, n):
                if (s == 1 and l[m] <= st) or (s == -1 and h[m] >= st):
                    ex = (min(o[m], st) if s == 1 else max(o[m], st)) * (1 - s * slip); break
                if (s == 1 and h[m] >= tp) or (s == -1 and l[m] <= tp):
                    ex = tp; break
            if ex == 0.0: ex = o[n - 1]
            tot += (s * (ex / e - 1) - fee * (1 + ex / e)) / f
        out[r] = tot
    return out


def _pf(r):
    w, ls = r[r > 0].sum(), -r[r < 0].sum()
    return float(w / ls) if ls > 0 else (float("inf") if w > 0 else float("nan"))


def _tstat(r):
    return float(r.mean() / (r.std(ddof=1) / np.sqrt(len(r)))) if len(r) > 2 and r.std(ddof=1) > 0 else float("nan")


def permute(df, rng):
    """A random price path with the same bars in a different order: gaps and in-bar moves are shuffled separately.
    Real patterns are destroyed; volatility and overall drift are kept."""
    o, h, l, c = (np.log(df[x].to_numpy(np.float64)) for x in ("open", "high", "low", "close"))
    gap = o[1:] - c[:-1]; hi = h[1:] - o[1:]; lo = l[1:] - o[1:]; cl = c[1:] - o[1:]
    p1 = rng.permutation(len(gap)); p2 = rng.permutation(len(gap))
    gap, hi, lo, cl = gap[p1], hi[p2], lo[p2], cl[p2]
    no = np.empty(len(o)); nc = np.empty(len(o)); nh = np.empty(len(o)); nl = np.empty(len(o))
    no[0], nh[0], nl[0], nc[0] = o[0], h[0], l[0], c[0]
    steps = gap + cl
    nc_prev = c[0] + np.concatenate([[0.0], np.cumsum(steps)[:-1]])          # previous close before each bar
    no[1:] = nc_prev + gap; nh[1:] = no[1:] + hi; nl[1:] = no[1:] + lo; nc[1:] = no[1:] + cl
    out = pd.DataFrame({"open": np.exp(no), "high": np.exp(nh), "low": np.exp(nl), "close": np.exp(nc)}, index=df.index)
    out["volume"] = np.concatenate([[df["volume"].iloc[0]], df["volume"].to_numpy()[1:][p2]])
    return out


def _frames(idea):
    """Markets for an idea: the original six by default, all fifteen on request, or the ones it names."""
    mk = idea.get("markets", "all")
    pool = FEES if mk == "all" else ALL_FEES
    return {m: load_market(m) for m in pool if os.path.exists(_path(m)) and (mk in ("all", "fifteen") or m in mk)}


def _collect(mod, idea, frames, costs=(1, 2)):
    """Simulate every config on every market and make the walk-forward picks (train data only)."""
    store, picks_all, q_picks = {}, [], []
    for m, (df, block, atrp) in frames.items():
        o, h, l, c = (np.ascontiguousarray(df[x].to_numpy(np.float64)) for x in ("open", "high", "low", "close"))
        cfgs = {}
        for gi, p in enumerate(idea["grid"]):
            d = _cooldown(np.ascontiguousarray(np.nan_to_num(np.asarray(mod.signals(df, p), dtype=np.float64)).astype(np.int64)), COOLDOWN)
            for xi, (am, rr) in enumerate(EXITS):
                slf = np.clip(am * atrp, 0.001, 0.20)
                cfgs[(gi, xi)] = tuple(_simulate(o, h, l, c, d, slf, rr, ALL_FEES[m] * k, SLIP * k) for k in costs)
        store[m] = dict(cfgs=cfgs, block=block, ohlc=(o, h, l, c), atrp=atrp)
        blocks = sorted(set(block.tolist()))
        for Tb in blocks:
            prior = [b for b in blocks if b < Tb][-3:]
            if len(prior) < 2: continue
            best, bt = None, -np.inf
            for key, runs in cfgs.items():
                ei, R, sd = runs[0]
                r = R[np.isin(block[ei], prior)]
                if len(r) >= MIN_TRAIN_TRADES and _tstat(r) > bt: best, bt = key, _tstat(r)
            if best is None: continue
            (q_picks if Tb == QUARANTINE else picks_all).append(dict(market=m, block=int(Tb), cfg=best, train_t=float(bt)))
    return store, picks_all, q_picks


def _total(store, picks):
    tot = 0.0
    for pk in picks:
        s = store[pk["market"]]; ei, R, sd = s["cfgs"][pk["cfg"]][0]
        tot += float(R[s["block"][ei] == pk["block"]].sum())
    return tot


def permutation_p(mod, idea, frames, actual, n=N_PERM, seed=7):
    """Re-run the whole walk-forward on shuffled price paths. p = share of shuffled paths that do at least as well."""
    rng = np.random.default_rng(seed); beat = 0
    for _ in range(n):
        fr = {}
        for m, (df, block, _) in frames.items():
            pdf = permute(df, rng); pc = pdf["close"].shift(1)
            tr = pd.concat([pdf["high"] - pdf["low"], (pdf["high"] - pc).abs(), (pdf["low"] - pc).abs()], axis=1).max(axis=1)
            fr[m] = (pdf, block, (tr.rolling(14, min_periods=14).mean() / pdf["close"]).fillna(0.01).to_numpy())
        store, picks, _ = _collect(mod, idea, fr, costs=(1,))
        beat += _total(store, picks) >= actual
    return (beat + 1) / (n + 1)


def neighbour_test(mod, idea, frames):
    """Move each number in the idea's settings 20% down and 20% up, one at a time, and re-run the walk-forward.
    An edge that only exists at one exact setting is a lucky number, not an edge."""
    names = sorted({k for p in idea["grid"] for k, v in p.items() if isinstance(v, (int, float)) and not isinstance(v, bool)})
    runs = []
    for name in names:
        for factor in (0.8, 1.2):
            grid = []
            for p in idea["grid"]:
                q = dict(p)
                if name in q and isinstance(q[name], (int, float)) and not isinstance(q[name], bool):
                    if isinstance(q[name], int):                      # whole numbers stay whole and always move by at least 1
                        moved = int(round(q[name] * factor))
                        q[name] = max(1, moved if moved != q[name] else q[name] + (1 if factor > 1 else -1))
                    else:
                        q[name] = q[name] * factor
                grid.append(q)
            if grid == idea["grid"]:
                continue
            store, picks, _ = _collect(mod, {**idea, "grid": grid}, frames, costs=(1,))
            R = [store[pk["market"]]["cfgs"][pk["cfg"]][0][1][store[pk["market"]]["block"][store[pk["market"]]["cfgs"][pk["cfg"]][0][0]] == pk["block"]] for pk in picks]
            R = np.concatenate(R) if R else np.array([])
            runs.append(dict(setting=name, factor=factor, trades=int(len(R)), pf=_pf(R) if len(R) else float("nan"), totalR=float(R.sum()) if len(R) else 0.0))
    good = int(sum(r["pf"] > 1.0 for r in runs))
    return dict(runs=runs, profitable=good, total=len(runs), passed=bool(not runs or good / len(runs) >= T["neighbour_share"]))


def run_idea(mod, attempts):
    idea = mod.IDEA
    assert len(idea["grid"]) <= MAX_GRID, "grid too large"
    assert idea.get("reason") and idea.get("loser"), "an idea must state why the edge exists and who loses"
    frames = _frames(idea); markets = list(frames)
    store, picks_all, q_picks = _collect(mod, idea, frames)
    # pooled out-of-sample result (quarantine block excluded)
    R_all, R_dbl, by_block, by_market, rnd, actual = [], [], {}, {}, np.zeros(1000), 0.0
    for pk in picks_all:
        s = store[pk["market"]]; (ei, R, sd), (ei2, R2, _) = s["cfgs"][pk["cfg"]]
        msk = s["block"][ei] == pk["block"]; r = R[msk]; r2 = R2[s["block"][ei2] == pk["block"]]
        R_all.append(r); R_dbl.append(r2); pk["n"] = int(len(r)); pk["R"] = float(r.sum())
        by_block[pk["block"]] = by_block.get(pk["block"], 0.0) + float(r.sum()); by_market[pk["market"]] = by_market.get(pk["market"], 0.0) + float(r.sum())
        if len(r):
            w = np.where(s["block"] == pk["block"])[0]; am, rr = EXITS[pk["cfg"][1]]
            rnd += _random(*s["ohlc"][:3], int(w[0]), int(w[-1]), sd[msk].astype(np.int64), np.clip(am * s["atrp"], 0.001, 0.20), rr, ALL_FEES[pk["market"]], SLIP, 1000, 11)
            actual += float(r.sum())
    R_all = np.concatenate(R_all) if R_all else np.array([]); R_dbl = np.concatenate(R_dbl) if R_dbl else np.array([])
    need_t = NormalDist().inv_cdf(1 - 0.05 / attempts)
    res = dict(name=idea["name"], markets=markets, trades=int(len(R_all)), pf=_pf(R_all) if len(R_all) else float("nan"), totalR=float(R_all.sum()) if len(R_all) else 0.0,
               t=_tstat(R_all), need_t=float(need_t), attempts=attempts, dbl_pf=_pf(R_dbl) if len(R_dbl) else float("nan"),
               beats_random=float((rnd < actual).mean() * 100) if len(R_all) else float("nan"),
               blocks_profitable=[int(sum(v > 0 for v in by_block.values())), len(by_block)], markets_profitable=[int(sum(v > 0 for v in by_market.values())), len(by_market)],
               by_block={int(k): round(v, 1) for k, v in sorted(by_block.items())}, by_market={k: round(v, 1) for k, v in by_market.items()})
    nb, nm = res["blocks_profitable"], res["markets_profitable"]
    res["checks"] = {
        f"profit factor >= {T['pf']}": bool(res["pf"] >= T["pf"]),
        f"trades >= {T['trades']}": bool(res["trades"] >= T["trades"]),
        "profitable in 60% of test years": bool(nb[1] and nb[0] / nb[1] >= T["block_share"]),
        "profitable in half the markets": bool(nm[1] and nm[0] / nm[1] >= T["market_share"]),
        "profit factor > 1 at double costs": bool(res["dbl_pf"] > 1.0),
        "beats 95% of random entries": bool(res["beats_random"] >= T["random_pct"]),
        f"t-stat >= {need_t:.2f} (bar for attempt {attempts})": bool(res["t"] >= need_t),
    }
    res["verdict"] = "REJECT"
    if all(res["checks"].values()):
        res["perm_p"] = float(permutation_p(mod, idea, frames, res["totalR"]))
        res["checks"][f"permutation test p <= {T['perm_p']}"] = bool(res["perm_p"] <= T["perm_p"])
    if all(res["checks"].values()):
        res["neighbours"] = neighbour_test(mod, idea, frames)
        res["checks"]["nearby settings stay profitable (two thirds or more)"] = res["neighbours"]["passed"]
    if all(res["checks"].values()):
        qr = []
        for pk in q_picks:
            s = store[pk["market"]]; (ei, R, sd), _ = s["cfgs"][pk["cfg"]]; qr.append(R[s["block"][ei] == QUARANTINE])
        qr = np.concatenate(qr) if qr else np.array([])
        res["quarantine"] = dict(trades=int(len(qr)), pf=_pf(qr) if len(qr) else float("nan"), totalR=float(qr.sum()) if len(qr) else 0.0)
        res["verdict"] = "CANDIDATE" if len(qr) >= T["q_trades"] and res["quarantine"]["pf"] > 1.0 else "REJECT (failed quarantine)"
    return res


def main():
    state_path = os.path.join(HERE, "state.json"); state = json.load(open(state_path))
    want = sys.argv[1:]
    if want and want[0] == "--permtest":
        f = want[1] + ".py"; spec = importlib.util.spec_from_file_location(want[1], os.path.join(HERE, "ideas", f)); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        frames = _frames(mod.IDEA); store, picks, _ = _collect(mod, mod.IDEA, frames, costs=(1,)); actual = _total(store, picks)
        n = int(want[2]) if len(want) > 2 else N_PERM
        print(f"{want[1]}: real walk-forward total {actual:+.1f}R, permutation p = {permutation_p(mod, mod.IDEA, frames, actual, n=n):.3f} over {n} shuffled paths (diagnostic only, nothing logged)")
        return
    files = sorted(f for f in os.listdir(os.path.join(HERE, "ideas")) if f.endswith(".py") and not f.startswith("_"))
    for f in files:
        path = os.path.join(HERE, "ideas", f); digest = hashlib.sha1(open(path, "rb").read()).hexdigest()[:12]
        if want and f[:-3] not in want: continue
        if not want and state["tested"].get(f) == digest: continue
        spec = importlib.util.spec_from_file_location(f[:-3], path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        sys.path.insert(0, os.path.join(HERE, "tools")); sys.path.insert(0, HERE)
        from check_idea import check
        problems = check(f[:-3])
        if problems:                       # a broken idea is not a test: it is not counted and not marked as tested
            print(f"INVALID    {f[:-3]}: " + "; ".join(problems)); continue
        state["attempts"] += 1
        is_pos = mod.IDEA.get("mode") == "position"
        if is_pos:
            import position_mode
            res = position_mode.run_idea(mod, state["attempts"])
        else:
            res = run_idea(mod, state["attempts"])
        res["file"], res["hash"], res["date"] = f, digest, datetime.date.today().isoformat()
        if "quarantine" in res: state["quarantine_used"].append(f)
        state["tested"][f] = digest
        json.dump(res, open(os.path.join(HERE, "results", f"{f[:-3]}_{digest}.json"), "w"), indent=1, default=float)
        fails = [k for k, v in res["checks"].items() if not v]
        with open(os.path.join(HERE, "JOURNAL.md"), "a") as j:
            j.write(f"\n### {res['date']} · attempt {res['attempts']} · `{mod.IDEA['name']}` · {res['verdict']}\n"
                    f"- Source: {mod.IDEA['source']}\n- Reason claimed: {mod.IDEA['reason']}\n- Who loses: {mod.IDEA['loser']}\n"
                    + (position_mode.journal_lines(res) if is_pos else
                       f"- Out-of-sample: {res['trades']} trades, profit factor {res['pf']:.2f}, {res['totalR']:+.1f}R, t-stat {res['t']:.2f} (needed {res['need_t']:.2f})\n"
                       f"- Profitable test years {res['blocks_profitable'][0]} of {res['blocks_profitable'][1]}; markets {res['markets_profitable'][0]} of {res['markets_profitable'][1]}; "
                       f"double-cost profit factor {res['dbl_pf']:.2f}; beats {res['beats_random']:.0f}% of random entries\n")
                    + (f"- Permutation test: p = {res['perm_p']:.3f}\n" if "perm_p" in res else "")
                    + (f"- Nearby settings: {res['neighbours']['profitable']} of {res['neighbours']['total']} stayed profitable\n" if "neighbours" in res else "")
                    + ((f"- Quarantine run: {res['quarantine']['days']} days, total {res['quarantine']['total']*100:+.1f}%\n" if is_pos else f"- Quarantine run: {res['quarantine']['trades']} trades, profit factor {res['quarantine']['pf']:.2f}\n") if "quarantine" in res else "")
                    + (f"- Failed: {'; '.join(fails)}\n" if fails else "- Passed every pre-quarantine check\n"))
        json.dump(state, open(state_path, "w"), indent=1)
        if is_pos:
            print(position_mode.summary_line(res)); continue
        print(f"{res['verdict']:10s} {mod.IDEA['name']:28s} trades {res['trades']:5d}  PF {res['pf']:.2f}  {res['totalR']:+7.1f}R  t {res['t']:.2f}/{res['need_t']:.2f}  double-cost PF {res['dbl_pf']:.2f}  beats random {res['beats_random']:.0f}%  years {res['blocks_profitable']}  markets {res['markets_profitable']}")


if __name__ == "__main__":
    main()
