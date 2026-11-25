"""Study 20, part 2: the book with copy v3 (gold) and the RTH breakout added. Rules: claude/book2-rules-2026-11-25.md. One run.

Usage: python book2.py MEMBERS_DIR OUT_JSON
Runs book.py's tests unchanged on the new member list and books, then adds the breach days and each book's worst point under its midnight balance.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import book as bk

bk.NAMES = bk.NAMES + ["10_copy_v3", "11_rth_breakout_A"]
bk.BOOKS = {"ALL11": list(range(11)), "PASSED3": [0, 9, 10], "PAIR": [0, 10]}


def extras(mdir):
    dz = np.load(os.path.join(mdir, "days.npz"), allow_pickle=True)
    days, first, end = pd.DatetimeIndex(dz["days"]), dz["first"], dz["end"]
    n = len(days)
    k0 = int(np.searchsorted(days, pd.Timestamp(bk.REPLAY_FROM)))
    early = (days >= bk.REPLAY_FROM) & (days <= bk.EARLY_END)
    Eh, Rh, Lh, V = [], [], [], []
    for nm in bk.NAMES:
        z = np.load(os.path.join(mdir, nm + ".npz"))
        r = np.cumsum(z["real"])
        Eh.append(r + z["fc"]); Rh.append(r); Lh.append(np.r_[0.0, r[:-1]] + z["lo"]); V.append(z["v"])
    Eh, Rh, Lh = np.array(Eh), np.array(Rh), np.array(Lh)
    Ed = Eh[:, end]
    P = np.diff(np.c_[np.zeros(len(bk.NAMES)), Ed], axis=1)
    sig = P[:, early].std(axis=1, ddof=1)
    Gm = [bk.carried(v, k0, n) for v in V]
    out = {}
    for name, mem in bk.BOOKS.items():
        out[name] = {"breach_days": {}}
        for vol in bk.VOLS:
            w = np.zeros(len(bk.NAMES))
            w[mem] = 1.0 / (len(mem) * sig[mem])
            w = w * (vol / np.sqrt(bk.YEAR)) / (w @ P)[early].std(ddof=1)
            e, r = w @ Ed, w @ Rh[:, end]
            low = np.minimum.reduceat(w @ Lh, first)
            G = sum(wi * g for wi, g in zip(w, Gm) if wi != 0)
            if vol == 10.0:                                               # worst point under the midnight balance, one unbroken run of the book
                under = (np.r_[0.0, (e - r)[:-1]] + low - np.r_[0.0, e[:-1]])[k0:]
                order = np.argsort(under)[:5]
                out[name]["worst_under_midnight_balance_at_10pct"] = [
                    {"day": str(days[k0 + i].date()), "pct": round(float(under[i]), 2),
                     "open_loss_carried_in_pct": round(float((e - r)[k0 + i - 1]), 2),
                     "by_member_carried_in": {bk.NAMES[m]: round(float(w[m] * (Ed[m] - Rh[m, end])[k0 + i - 1]), 2) for m in mem
                                              if abs(w[m] * (Ed[m] - Rh[m, end])[k0 + i - 1]) > 0.05}} for i in order]
                out[name]["largest_size_that_never_goes_3pct_under"] = round(10.0 * 3.0 / -float(under.min()), 1)
            for firm, S in bk.FIRMS.items():
                o, took, starts = bk.replay(e, r, low, G, S, k0)
                idx = starts[:, None] + np.arange(bk.CAP)[None, :]
                B0, R0 = e[starts - 1], r[starts - 1]
                bal = r[idx] - R0[:, None] - (B0 - R0)[:, None] + G
                z = np.zeros((len(starts), 1))
                bal0, eq0 = np.hstack([z, bal[:, :-1]]), np.hstack([z, (e[idx] - B0[:, None])[:, :-1]])
                lw = low[idx] - B0[:, None]
                ref = bal0 if S["ref"] == "balance" else np.maximum(bal0, eq0)
                floor = (np.maximum.accumulate(np.maximum(bal0, 0.0), axis=1) - S["maxloss"]) if S["trailing"] else -S["maxloss"]
                br = (lw <= ref - S["daily"] + 1e-9) | (lw <= floor + 1e-9)
                hit = np.isin(o, ["breach_daily", "breach_max"])
                cnt = pd.Series(days[starts[hit] + br.argmax(1)[hit]]).value_counts().sort_index()
                out[name]["breach_days"].setdefault(firm, {})[str(vol)] = {str(k.date()): int(v) for k, v in cnt.items()}
    return out


if __name__ == "__main__":
    mdir, out_path = sys.argv[1:3]
    sys.argv = [sys.argv[0], "run", mdir, out_path]
    bk.main()
    res = json.load(open(out_path))
    res["extras"] = extras(mdir)
    json.dump(res, open(out_path, "w"), indent=1)
