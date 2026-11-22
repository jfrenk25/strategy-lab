"""What does a strategy with no edge take home from an FTMO 2-Step challenge?

A calculator for the lab, not a gate: the account-fit check named in LAB_RULES.md is not defined yet. It uses
made-up trades, not lab data, so it tests the firm's rules and nothing else. A losing trade loses one unit of risk (R); a winner makes a set multiple of R. The win rate sets the edge.
The RIAG-like case copies the win rate (40.86%) and payoff ratio (1.71) Darwinex publishes for ZenomTrader's index.

Rules modelled (FTMO 2-Step, $100,000, as published in November 2026):
  - Challenge: reach +10%. Verification: reach +5%. No time limit, at least 4 trading days in each.
  - Fail if the day's loss reaches 5% of the starting balance, or the balance falls 10% below the start (fixed line).
  - Funded account: same two loss limits. A payout of 80% of the profit every 14 days (10 trading days here),
    after which the balance goes back to the start. The fee comes back with the first payout.
Assumptions that are ours:
  - Fee of $600 (EUR 540 as recalled, not checked against FTMO's price list).
  - Limits are checked after each closed trade. Open-trade swings, swaps and news rules are ignored.
  - An unfinished challenge is abandoned after 250 trading days. A funded account is followed for 250 trading days.
  - FTMO's right to refuse a payout for "gambling" style trading is not modelled.

Usage (from the repo root): python lab/tools/prop_rules_sim.py
"""
import numpy as np

SIZE = 100_000.0
FEE = 600.0
SPLIT = 0.80
DAILY, MAXLOSS = 0.05, 0.10
TARGETS = (0.10, 0.05)
MIN_DAYS = 4
PAY_EVERY = 10          # trading days
EVAL_CAP = 250
FUNDED_DAYS = 250


EPS = 1e-9             # guards the limit checks against rounding in sums of floats


def run(risk, trades_per_day, cost_r, win_prob=0.5, payoff=1.0, n=40_000, seed=1):
    """risk: share of the starting balance lost on a losing trade (1R). A winner makes payoff x R.
    cost_r: cost per trade in units of R."""
    rng = np.random.default_rng(seed)
    phase = np.zeros(n, dtype=int)                 # 0 challenge, 1 verification, 2 funded, 3 failed, 4 abandoned, 5 done
    bal = np.zeros(n)                              # profit or loss as a share of the starting balance
    days_in = np.zeros(n, dtype=int)
    eval_days = np.zeros(n, dtype=int)
    paid = np.zeros(n); n_pay = np.zeros(n, dtype=int)
    funded_at = np.full(n, -1)
    for day in range(EVAL_CAP * 2 + FUNDED_DAYS + 10):
        live = phase <= 2
        if not live.any():
            break
        start = bal.copy()
        traded = np.zeros(n, dtype=bool)
        for _ in range(trades_per_day):
            act = (phase <= 2) & ~((phase < 2) & (bal >= np.where(phase == 0, TARGETS[0], TARGETS[1]) - EPS))
            if not act.any():
                break
            win = rng.random(n) < win_prob
            bal = np.where(act, bal + np.where(win, payoff * risk, -risk) - cost_r * risk, bal)
            traded |= act
            breach = act & ((bal - start <= -DAILY + EPS) | (bal <= -MAXLOSS + EPS))
            phase[breach] = 3
        days_in[traded] += 1
        waiting = (phase < 2) & ~traded & (bal >= np.where(phase == 0, TARGETS[0], TARGETS[1]) - EPS)
        days_in[waiting] += 1                      # target reached early: a token trade a day fills the minimum days
        ev = (phase < 2)
        eval_days[ev & traded] += 1
        for ph in (0, 1):                          # a target is banked once the minimum days are done
            hit = (phase == ph) & (bal >= TARGETS[ph] - EPS) & (days_in >= MIN_DAYS)
            if ph == 0:
                phase[hit] = 1
            else:
                phase[hit] = 2; funded_at[hit] = day
            bal[hit] = 0.0; days_in[hit] = 0
        phase[(phase < 2) & (eval_days >= EVAL_CAP)] = 4
        fd = phase == 2
        due = fd & (days_in > 0) & (days_in % PAY_EVERY == 0) & traded & (bal > EPS)
        paid[due] += SPLIT * bal[due] * SIZE; n_pay[due] += 1; bal[due] = 0.0
        phase[fd & (days_in >= FUNDED_DAYS)] = 5
    net = paid - FEE + np.where(n_pay > 0, FEE, 0.0)
    return dict(passed=(funded_at >= 0).mean(), abandoned=(phase == 4).mean(), any_payout=(n_pay > 0).mean(),
                mean_net=net.mean(), median_net=np.median(net), mean_paid_if_funded=paid[funded_at >= 0].mean() if (funded_at >= 0).any() else 0.0,
                eval_days=np.median(eval_days[funded_at >= 0]) if (funded_at >= 0).any() else np.nan, net=net)


def campaign(net, attempts, rng, sims=20_000):
    tot = rng.choice(net, size=(sims, attempts)).sum(axis=1)
    return (tot > 0).mean(), np.median(tot), np.percentile(tot, 10)


if __name__ == "__main__":
    rng = np.random.default_rng(7)
    print("FTMO 2-Step $100K, fee $%d, split %d%%, 2 trades a day. Net = payouts in the first funded year, less the fee." % (FEE, SPLIT * 100))
    print("%-34s %6s %7s %8s %9s %9s %8s | %s" % ("case", "pass", "payout", "quit", "mean net", "median", "days", "10 tries: P(profit), median, worst 10%"))
    cases = [                                   # name, risk per trade, trades a day, cost in R, win rate, payoff
        ("no edge, no costs, risk 0.5%", 0.005, 2, 0.0, 0.5, 1.0),
        ("no edge, no costs, risk 1%", 0.010, 2, 0.0, 0.5, 1.0),
        ("no edge, no costs, risk 2%", 0.020, 2, 0.0, 0.5, 1.0),
        ("profit factor 0.9, risk 1%", 0.010, 2, 0.0, 0.9 / 1.9, 1.0),
        ("profit factor 0.8, risk 1%", 0.010, 2, 0.0, 0.8 / 1.8, 1.0),
        ("profit factor 0.8, risk 2%", 0.020, 2, 0.0, 0.8 / 1.8, 1.0),
        ("RIAG-like (PF 1.18), risk 0.26%", 0.0026, 2, 0.0, 0.4086, 1.71),
        ("RIAG-like (PF 1.18), risk 0.5%", 0.005, 2, 0.0, 0.4086, 1.71),
        ("RIAG-like (PF 1.18), risk 1%", 0.010, 2, 0.0, 0.4086, 1.71),
    ]
    for name, risk, tpd, cost, wp, po in cases:
        r = run(risk, tpd, cost, wp, po)
        c = campaign(r["net"], 10, rng)
        print("%-34s %5.1f%% %6.1f%% %7.1f%% %9.0f %9.0f %8.0f | %4.0f%%, %7.0f, %7.0f" % (
            name, 100 * r["passed"], 100 * r["any_payout"], 100 * r["abandoned"], r["mean_net"], r["median_net"], r["eval_days"], 100 * c[0], c[1], c[2]))
