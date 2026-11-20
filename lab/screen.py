"""Screen-and-confirm track: test many machine-built ideas cheaply, then check the survivors on years the screen never saw.

Run from the repo root:
    python lab/screen.py              # screen the next 100 untested ideas from the catalogue
    python lab/screen.py --n 50       # screen the next 50
    python lab/screen.py --selftest 300   # run 300 ideas on shuffled prices to measure the luck rate (nothing is logged)

The rules are in LAB_RULES.md under "Screen and confirm". Thresholds here must match that section.
An idea is built from parts: trigger x direction x regime filter x session filter x exit. It has no stated reason.
Fresh data replaces the reason: a survivor gets exactly one run on the confirm years, against a bar that rises with
the number of survivors ever confirmed.
"""
import sys, os, json, csv, hashlib, random, datetime, argparse
from statistics import NormalDist
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab

CATALOGUE_VERSION = 1
SEED = 20261120                    # fixes the order in which the catalogue is screened
SCREEN_LAST_BLOCK = 2023           # the screen sees trades entered before April 21, 2024
CONFIRM_BLOCKS = (2024, 2025)      # April 21, 2024 to April 20, 2026: one run per survivor
S = dict(trades=150, pf=1.10, t=1.65, market_share=0.5)             # screen: loose on purpose
C = dict(trades=60, pf=1.15, market_share=0.5, random_pct=95.0)     # confirm: strict, plus the rising bar
SURVIVOR_FLOOR = 20                # the survivor bar is never easier than the bar for 20 survivors (t of about 2.81)
SESSIONS = {"any": None, "asia": (0, 6), "london": (7, 12), "ny": (13, 20)}     # UTC hours of the signal bar
REGIMES = ["none", "with_trend", "against_trend", "high_vol", "low_vol"]
OUT = os.path.join(HERE, "screen")
LOG_COLS = ["date", "id", "name", "trades", "pf", "t", "double_cost_pf", "markets_profitable", "screen"]


# ---------------------------------------------------------------- catalogue

def catalogue():
    """Every idea the screen can build, in a fixed shuffled order."""
    trig = []
    for n in (24, 72, 168):
        trig.append(("breakout", {"n": n})); trig.append(("sweep", {"n": n}))
    trig.append(("prev_day_break", {}))
    for k in (2, 3):
        trig.append(("big_bar", {"k": k})); trig.append(("vol_spike", {"k": k}))
    for n in (24, 72):
        trig.append(("squeeze_break", {"n": n}))
    for k in (3, 4, 5):
        trig.append(("streak", {"k": k}))
    trig.append(("gap", {}))
    for n in (24, 72):
        for z in (2.0, 2.5):
            trig.append(("zmove", {"n": n, "z": z}))
    timed = [("session_open", {"hour": hr}) for hr in (0, 7, 13)]
    timed += [("clock", {"weekday": d, "hour": 0}) for d in range(7)]
    timed += [("clock", {"weekday": -1, "hour": hr}) for hr in (0, 4, 8, 12, 16, 20)]
    specs = []
    for group, sessions in ((trig, list(SESSIONS)), (timed, ["any"])):
        for t, p in group:
            for direction in ("follow", "fade"):
                for regime in REGIMES:
                    for session in sessions:
                        for x in range(len(lab.EXITS)):
                            specs.append(dict(trigger=t, params=p, direction=direction, regime=regime, session=session, exit=x))
    for s in specs:
        s["id"] = hashlib.sha1(json.dumps(s, sort_keys=True).encode()).hexdigest()[:10]
        am, rr = lab.EXITS[s["exit"]]
        ptxt = "".join(f"_{k}{v:g}" for k, v in sorted(s["params"].items()))
        s["name"] = f"{s['trigger']}{ptxt}.{s['direction']}.{s['regime']}.{s['session']}.stop{am:g}_rr{rr:g}"
    assert len({s["id"] for s in specs}) == len(specs)
    specs.sort(key=lambda s: s["id"])
    random.Random(SEED).shuffle(specs)
    return specs


# ---------------------------------------------------------------- signals (current bar and earlier bars only)

class Feats:
    """Per-market features, cached. Everything is computed from the current bar and earlier bars."""

    def __init__(self, df):
        self.df = df; self._ev = {}; self._rg = {}
        pc = df["close"].shift(1)
        tr = pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)
        self.atr24 = tr.rolling(24).mean()
        self.hour = df.index.hour.to_numpy()

    def event(self, trigger, p):
        key = (trigger, json.dumps(p, sort_keys=True))
        if key not in self._ev:
            self._ev[key] = np.asarray(_event(self, trigger, p), dtype=np.int64)
        return self._ev[key]

    def regime(self, name):
        if name not in self._rg:
            c = self.df["close"]
            if name in ("with_trend", "against_trend"):
                self._rg[name] = np.nan_to_num(np.sign((c - c.rolling(500).mean()).to_numpy())).astype(np.int64)
            else:
                a = self.atr24 / c
                med = a.rolling(500).median().shift(1)
                self._rg[name] = ((a > med) if name == "high_vol" else (a <= med)).to_numpy()
        return self._rg[name]


def _event(f, trigger, p):
    df = f.df; o, h, l, c, v = df["open"], df["high"], df["low"], df["close"], df["volume"]; idx = df.index
    if trigger in ("breakout", "sweep", "squeeze_break"):
        n = p["n"]; hi = h.rolling(n).max().shift(1); lo = l.rolling(n).min().shift(1)
        if trigger == "sweep":          # pokes through the old range and closes back inside: the event points back inside
            return np.where((h > hi) & (c < hi), -1, np.where((l < lo) & (c > lo), 1, 0))
        brk = np.where(c > hi, 1, np.where(c < lo, -1, 0))
        if trigger == "breakout":
            return brk
        width = ((hi - lo) / c.shift(1))                       # range of the n bars before this one
        narrow = (width <= width.rolling(500).quantile(0.2)).to_numpy()
        return np.where(narrow, brk, 0)
    if trigger == "prev_day_break":
        day = idx.normalize()
        ph = pd.Series(h.groupby(day).max().shift(1).reindex(day).to_numpy(), index=idx)
        pl = pd.Series(l.groupby(day).min().shift(1).reindex(day).to_numpy(), index=idx)
        pc = c.shift(1)
        return np.where((c > ph) & (pc <= ph), 1, np.where((c < pl) & (pc >= pl), -1, 0))
    if trigger == "big_bar":
        rng = h - l; pos = (c - l) / rng.where(rng > 0); big = rng > p["k"] * f.atr24.shift(1)
        return np.where(big & (pos >= 0.75), 1, np.where(big & (pos <= 0.25), -1, 0))
    if trigger == "vol_spike":
        spike = v > p["k"] * v.rolling(168).mean().shift(1)
        return np.where(spike & (c > o), 1, np.where(spike & (c < o), -1, 0))
    if trigger == "streak":
        k = p["k"]; up = (c > c.shift(1)).astype(float); dn = (c < c.shift(1)).astype(float)
        return np.where(up.rolling(k).sum() == k, 1, np.where(dn.rolling(k).sum() == k, -1, 0))
    if trigger == "gap":
        g = o - c.shift(1); thr = 0.5 * f.atr24.shift(1)
        return np.where(g > thr, 1, np.where(g < -thr, -1, 0))
    if trigger == "zmove":
        n, z = p["n"], p["z"]; r = np.log(c / c.shift(n)); zc = r / r.rolling(500).std().shift(1); zp = zc.shift(1)
        return np.where((zc > z) & (zp <= z), 1, np.where((zc < -z) & (zp >= -z), -1, 0))
    if trigger == "session_open":       # the bar that closes at the session open, pointing the way the last 6 bars went
        at = f.hour == (p["hour"] - 1) % 24; mom = (c / c.shift(6) - 1).to_numpy()
        return np.where(at & (mom > 0), 1, np.where(at & (mom < 0), -1, 0))
    if trigger == "clock":              # a fixed time of day or week; follow = buy, fade = sell
        at = f.hour == p["hour"]
        if p["weekday"] >= 0:
            at = at & (idx.dayofweek.to_numpy() == p["weekday"])
        return np.where(at, 1, 0)
    raise ValueError(trigger)


def signals(spec, f):
    d = f.event(spec["trigger"], spec["params"]) * (1 if spec["direction"] == "follow" else -1)
    rg = spec["regime"]
    if rg == "with_trend":
        d = np.where(d == f.regime(rg), d, 0)
    elif rg == "against_trend":
        d = np.where(d == -f.regime(rg), d, 0)
    elif rg != "none":
        d = np.where(f.regime(rg), d, 0)
    hrs = SESSIONS[spec["session"]]
    if hrs is not None:
        d = np.where((f.hour >= hrs[0]) & (f.hour <= hrs[1]), d, 0)
    return d.astype(np.int64)


# ---------------------------------------------------------------- testing

def load(frames=None):
    data = {}
    for m in lab.FEES:
        if frames is None and not os.path.exists(os.path.join(HERE, "data", f"{m}_1h.csv.gz")):
            continue
        df, block, atrp = lab.load_market(m) if frames is None else frames[m]
        o, h, l, c = (np.ascontiguousarray(df[x].to_numpy(np.float64)) for x in ("open", "high", "low", "close"))
        data[m] = dict(df=df, block=block, atrp=atrp, ohlc=(o, h, l, c), feats=Feats(df))
    return data


def run_spec(spec, data):
    am, rr = lab.EXITS[spec["exit"]]; runs = {}
    for m, D in data.items():
        d = lab._cooldown(np.ascontiguousarray(signals(spec, D["feats"])), lab.COOLDOWN)
        slf = np.clip(am * D["atrp"], 0.001, 0.20)
        runs[m] = dict(slf=slf, rr=rr, x1=lab._simulate(*D["ohlc"], d, slf, rr, lab.FEES[m], lab.SLIP),
                       x2=lab._simulate(*D["ohlc"], d, slf, rr, lab.FEES[m] * 2, lab.SLIP * 2))
    return runs


def window_stats(runs, data, in_window, random_baseline=False):
    """Pooled result for trades entered in the window. in_window maps an array of block numbers to a mask."""
    R, R2, by_market, rnd, actual = [], [], {}, np.zeros(1000), 0.0
    for m, run in runs.items():
        blk = data[m]["block"]; ei, r, sd = run["x1"]; ei2, r2, _ = run["x2"]
        k = in_window(blk[ei]); R.append(r[k]); R2.append(r2[in_window(blk[ei2])]); by_market[m] = float(r[k].sum())
        if random_baseline and k.any():
            w = np.where(in_window(blk))[0]
            rnd += lab._random(*data[m]["ohlc"][:3], int(w[0]), int(w[-1]), sd[k].astype(np.int64), run["slf"], run["rr"], lab.FEES[m], lab.SLIP, 1000, 11)
            actual += float(r[k].sum())
    R = np.concatenate(R); R2 = np.concatenate(R2)
    out = dict(trades=int(len(R)), pf=lab._pf(R) if len(R) else float("nan"), totalR=float(R.sum()) if len(R) else 0.0, t=lab._tstat(R),
               dbl_pf=lab._pf(R2) if len(R2) else float("nan"), markets_profitable=[int(sum(v > 0 for v in by_market.values())), len(by_market)],
               by_market={k: round(v, 1) for k, v in by_market.items()})
    if random_baseline:
        out["beats_random"] = float((rnd < actual).mean() * 100) if len(R) else float("nan")
    return out


def screen_checks(st):
    nm = st["markets_profitable"]
    return {
        f"trades >= {S['trades']}": bool(st["trades"] >= S["trades"]),
        f"profit factor >= {S['pf']}": bool(st["pf"] >= S["pf"]),
        f"t-stat >= {S['t']}": bool(st["t"] >= S["t"]),
        "profitable in half the markets": bool(nm[1] and nm[0] / nm[1] >= S["market_share"]),
        "profit factor > 1 at double costs": bool(st["dbl_pf"] > 1.0),
    }


def confirm_checks(st, need_t, k):
    nm = st["markets_profitable"]
    return {
        f"trades >= {C['trades']}": bool(st["trades"] >= C["trades"]),
        f"profit factor >= {C['pf']}": bool(st["pf"] >= C["pf"]),
        "profitable in half the markets": bool(nm[1] and nm[0] / nm[1] >= C["market_share"]),
        "profit factor > 1 at double costs": bool(st["dbl_pf"] > 1.0),
        "beats 95% of random entries": bool(st["beats_random"] >= C["random_pct"]),
        f"t-stat >= {need_t:.2f} (bar for survivor {k})": bool(st["t"] >= need_t),
    }


def in_screen(b): return b <= SCREEN_LAST_BLOCK
def in_confirm(b): return np.isin(b, CONFIRM_BLOCKS)
def in_quarantine(b): return b == lab.QUARANTINE


def selftest(n):
    """Run n catalogue ideas on shuffled prices. Any pass there is luck by construction. Nothing is logged."""
    rng = np.random.default_rng(3); frames = {}
    for m in lab.FEES:
        df, block, _ = lab.load_market(m); pdf = lab.permute(df, rng); pc = pdf["close"].shift(1)
        tr = pd.concat([pdf["high"] - pdf["low"], (pdf["high"] - pc).abs(), (pdf["low"] - pc).abs()], axis=1).max(axis=1)
        frames[m] = (pdf, block, (tr.rolling(14, min_periods=14).mean() / pdf["close"]).fillna(0.01).to_numpy())
    data = load(frames); specs = catalogue()[-n:]; passed = 0
    for spec in specs:
        st = window_stats(run_spec(spec, data), data, in_screen)
        passed += all(screen_checks(st).values())
    print(f"selftest on shuffled prices: {passed} of {len(specs)} ideas passed the screen by luck ({100 * passed / len(specs):.1f}%)")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=100); ap.add_argument("--selftest", type=int, default=0)
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.selftest)
    os.makedirs(os.path.join(OUT, "confirm"), exist_ok=True)
    state_path = os.path.join(OUT, "state.json"); log_path = os.path.join(OUT, "log.csv")
    state = json.load(open(state_path)) if os.path.exists(state_path) else dict(catalogue_version=CATALOGUE_VERSION, screened=0, survivors=0, confirmed=0, candidates=0)
    assert state["catalogue_version"] == CATALOGUE_VERSION, "catalogue changed: bump the version and start a new log"
    done = set()
    if os.path.exists(log_path):
        done = {row["id"] for row in csv.DictReader(open(log_path, newline=""))}
    else:
        csv.writer(open(log_path, "w", newline="")).writerow(LOG_COLS)
    specs = catalogue(); todo = [s for s in specs if s["id"] not in done][: a.n]
    today = datetime.date.today().isoformat()
    if not todo:
        print(f"catalogue exhausted: all {len(specs)} ideas screened"); return
    data = load(); day = dict(screened=0, survivors=[], confirmed=[], candidates=[])
    for spec in todo:
        runs = run_spec(spec, data)
        st = window_stats(runs, data, in_screen); ok = all(screen_checks(st).values())
        with open(log_path, "a", newline="") as fh:        # logged before anything else: an idea is screened once
            csv.writer(fh).writerow([today, spec["id"], spec["name"], st["trades"], f"{st['pf']:.3f}", f"{st['t']:.2f}", f"{st['dbl_pf']:.3f}",
                                     f"{st['markets_profitable'][0]}/{st['markets_profitable'][1]}", "PASS" if ok else "fail"])
        state["screened"] += 1; day["screened"] += 1
        if not ok:
            json.dump(state, open(state_path, "w"), indent=1); continue
        # survivor: exactly one run on the confirm years
        state["survivors"] += 1; k = state["survivors"]; need_t = NormalDist().inv_cdf(1 - 0.05 / max(k, SURVIVOR_FLOOR))
        cf = window_stats(runs, data, in_confirm, random_baseline=True); checks = confirm_checks(cf, need_t, k)
        res = dict(id=spec["id"], name=spec["name"], spec={x: spec[x] for x in ("trigger", "params", "direction", "regime", "session", "exit")},
                   date=today, survivor=k, need_t=float(need_t), screen=st, confirm=cf, checks=checks, verdict="REJECT")
        day["survivors"].append(spec["name"])
        if all(checks.values()):
            state["confirmed"] += 1; day["confirmed"].append(spec["name"])
            q = window_stats(runs, data, in_quarantine); res["quarantine"] = dict(trades=q["trades"], pf=q["pf"], totalR=q["totalR"])
            if q["trades"] >= lab.T["q_trades"] and q["pf"] > 1.0:
                res["verdict"] = "CANDIDATE"; state["candidates"] += 1; day["candidates"].append(spec["name"])
            else:
                res["verdict"] = "REJECT (failed quarantine)"
        json.dump(res, open(os.path.join(OUT, "confirm", f"{spec['id']}.json"), "w"), indent=1, default=float)
        fails = [c for c, v in checks.items() if not v]
        with open(os.path.join(HERE, "JOURNAL.md"), "a") as j:
            j.write(f"\n### {today} · screen survivor {k} · `{spec['name']}` · {res['verdict']}\n"
                    f"- Source: machine-built from parts (screen catalogue v{CATALOGUE_VERSION}, id {spec['id']}). No stated reason.\n"
                    f"- Screen years: {st['trades']} trades, profit factor {st['pf']:.2f}, t-stat {st['t']:.2f}\n"
                    f"- Confirm years: {cf['trades']} trades, profit factor {cf['pf']:.2f}, {cf['totalR']:+.1f}R, t-stat {cf['t']:.2f} (needed {need_t:.2f}); "
                    f"markets {cf['markets_profitable'][0]} of {cf['markets_profitable'][1]}; double-cost profit factor {cf['dbl_pf']:.2f}; beats {cf['beats_random']:.0f}% of random entries\n"
                    + (f"- Quarantine run: {res['quarantine']['trades']} trades, profit factor {res['quarantine']['pf']:.2f}\n" if "quarantine" in res else "")
                    + (f"- Failed: {'; '.join(fails)}\n" if fails else "- Passed every confirm check\n"))
        json.dump(state, open(state_path, "w"), indent=1)
        print(f"{res['verdict']:10s} {spec['name']}  screen t {st['t']:.2f}  confirm: {cf['trades']} trades  PF {cf['pf']:.2f}  t {cf['t']:.2f}/{need_t:.2f}")
    with open(os.path.join(HERE, "JOURNAL.md"), "a") as j:
        j.write(f"\n### {today} · screen batch · {day['screened']} ideas\n"
                f"- Passed the screen: {len(day['survivors'])}. Confirmed on unseen years: {len(day['confirmed'])}. Candidates: {len(day['candidates'])}.\n"
                f"- Totals: {state['screened']} of {len(specs)} catalogue ideas screened, {state['survivors']} survivors, {state['confirmed']} confirmed, {state['candidates']} candidates.\n"
                f"- Every screened idea is in `lab/screen/log.csv`.\n")
    json.dump(state, open(state_path, "w"), indent=1)
    print(f"screened {day['screened']}: {len(day['survivors'])} passed the screen, {len(day['confirmed'])} confirmed, {len(day['candidates'])} candidates. "
          f"Totals: {state['screened']}/{len(specs)} screened, {state['survivors']} survivors, {state['confirmed']} confirmed, {state['candidates']} candidates.")


if __name__ == "__main__":
    main()
