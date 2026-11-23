"""One cost table for every track (rules version 4, November 23, 2026). The rules are in LAB_RULES.md under "Rules version 4".

COST is charged per side, as a fraction of price: once on entry and once on exit. It stands for commission plus half the spread.
A stopped exit pays STOP_SLIP on top (the same amount again). The double-cost check doubles both.

Where the numbers come from (read on November 23, 2026):
- FTMO US (with OANDA) publishes commission of 5 USD per forex lot round trip, and 0.0025% per side on index, commodity and metal
  contracts that expire. Its rolling index and oil contracts carry no commission.
- FTMO publishes 0.0325% per side on crypto.
- FTMO publishes no typical spreads. The spread part below is an estimate from third-party listings (Nasdaq about 1.7 points,
  forex majors under 1 pip, gold about 0.30 USD, Bitcoin about 60 USD). It is the weakest part of this table.
- To correct a number, read the spread and commission for the symbol off the trading platform. A changed table is a new rules version.

In price terms at November 2026 prices, per round trip: Nasdaq 2.8 points, S&P 500 0.8 points, Dow 5.2 points, EURUSD 1.3 pips,
gold 0.48 USD, oil 3.5 cents, Bitcoin about 97 USD.
"""
SIX = ("BTCUSD", "ETHUSD", "XAUUSD", "GBPJPY", "USA30", "DEU30")           # the lab's first six markets (lab/data)
COST = {
    "BTCUSD": 0.00065, "ETHUSD": 0.00075,                                 # crypto: 0.0325% commission plus half a wide spread
    "XAUUSD": 0.00006,                                                    # gold: 0.0025% commission plus half of about 0.30 USD
    "USA30": 0.00005, "DEU30": 0.00005, "NAS100": 0.00005, "SPX500": 0.00005,   # indices: about 0.01% per round trip, all in
    "USOIL": 0.0002,                                                      # oil: spread only, about 3.5 cents per round trip
    "EURUSD": 0.00006, "GBPUSD": 0.00006, "USDJPY": 0.00006, "AUDUSD": 0.00006, "USDCAD": 0.00006,   # majors: 2.5 USD a side plus half of about 0.8 pips
    "EURJPY": 0.00008, "GBPJPY": 0.00008,                                 # yen crosses: wider spread
}
STOP_SLIP = dict(COST)                                                    # extra on a stopped exit: the per-side cost again
POSITION_MULT = 2.0                                                       # position mode trades at the daily close, when spreads are wide: each change pays twice the per-side cost
DATA_START = "2021-04-21"                                                 # every market is read from this day on, gold too
