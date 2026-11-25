"""Forward watch for the chat studies: the breakout (Study 17), the dip-buy rule (Studies 12 and 13) and the pair (Study 18).

Run from the repo root:
    python lab/studies/forward_studies.py

It re-runs the frozen rules on the NAS100 files and keeps only what was entered on or after START.
The rules and the verdict are in lab/studies/README.md. Nothing here may be changed after the first forward bar.
It only moves when lab/data_1m/NAS100_1m_full.csv.gz and lab/data_new/NAS100_1h.csv.gz are refreshed.
"""
import json
import os
import sys
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

import numpy as np
import pandas as pd

import gapline_orb as g14
import pair_study as ps
import rth_breakout as rth

START = pd.Timestamp("2026-11-21")                      # the day after the last bar any of these studies read
STATUS = os.path.join(LAB, "forward", "studies_status.json")
NEED = {"breakout_A": 200, "breakout_B": 200, "dipbuy": 40}       # forward trades before a verdict is given
NEED_T = NormalDist().inv_cdf(1 - 0.05 / 3)             # three watched rules
PAIR = (0.25, 1.5)                                      # % of account risked per trade: breakout, dip-buy


def pf(v):
    wins, losses = v[v > 0].sum(), -v[v < 0].sum()
    return round(float(wins / losses), 2) if losses > 0 else None


def summarize(v, v2, trades, need):
    """v: one number per traded day (breakout) or per trade (dip-buy), in R. v2: the same at double cost, or None."""
    v = np.asarray(v, float)
    s = {"forward_trades": int(trades), "needed_for_verdict": need, "sum_R": round(float(v.sum()), 2) if len(v) else 0.0,
         "profit_factor": pf(v) if len(v) else None, "status": "WATCHING"}
    if trades < need or len(v) < 3:
        return s
    t = float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v))))
    s["t_stat"], s["t_bar"] = round(t, 2), round(NEED_T, 2)
    ok = v.mean() > 0 and (s["profit_factor"] or 0) >= 1.15
    if v2 is not None:
        s["profit_factor_double_cost"] = pf(np.asarray(v2, float))
        ok = ok and (s["profit_factor_double_cost"] or 0) > 1.0
    s["status"] = "FAILED" if not ok else ("FORWARD PASS" if t >= NEED_T else "HOLDING UP")
    return s


def main():
    m, _ = g14.load(LAB, "NAS100")
    out = {"start": str(START.date()), "last_1m_bar": str(m["ts"].max()), "items": {}}
    fwd_tab = {}
    for name, cap in (("breakout_A", None), ("breakout_B", 2)):
        tab, _ = rth.run_market(m, cap)
        tab2, _ = rth.run_market(m, cap, cost=2 * rth.COST)
        f, f2 = tab[tab["day"] >= START], tab2[tab2["day"] >= START]
        fwd_tab[name] = f
        out["items"][name] = summarize(f[f["n"] > 0]["dbal"], f2[f2["n"] > 0]["dbal"], int(f["n"].sum()), NEED[name])
    m2, h = ps.load(LAB)
    out["last_1h_bar"] = str(h["ts"].max())
    trades, dates = ps.dipbuy(m2, h)
    fwd = [t for t in trades if dates[t["e"]] >= START]
    out["items"]["dipbuy"] = summarize([t["R"] for t in fwd], None, len(fwd), NEED["dipbuy"])
    # the pair: breakout version A plus the dip-buy rule, in % of account. Reported next to the legs; no verdict of its own.
    C = ps.day_table(fwd, dates)
    C["pnl"] = C["dbal"] + np.r_[C["a"].to_numpy()[1:], 0.0] - C["a"]
    T = C.set_index("day").join(fwd_tab["breakout_A"].set_index("day")[["dbal"]], rsuffix="_b").fillna({"dbal_b": 0.0})
    T = T[T.index >= START]
    p = PAIR[0] * T["dbal_b"].to_numpy() + PAIR[1] * T["pnl"].to_numpy()
    out["items"]["pair_0.25_plus_1.5"] = {"days": int(len(p)), "total_pct": round(float(p.sum()), 2),
                                          "deepest_drawdown_pct": round(ps.max_dd(p), 2) if len(p) else 0.0,
                                          "worst_day_pct": round(float(p.min()), 2) if len(p) else 0.0}
    json.dump(out, open(STATUS, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
