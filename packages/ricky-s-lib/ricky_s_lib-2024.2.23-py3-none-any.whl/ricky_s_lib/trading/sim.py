from typing import Callable

import numba
import numpy as np

from ricky_s_lib.trading.data import DATA_TYPE

ENTER, EXIT = 1, 2


def sim(data: DATA_TYPE, algo: Callable, conf):
    data2 = []
    for k, x in data.items():
        long = x["long"] = np.zeros_like(x["date"])
        short = x["short"] = np.zeros_like(x["date"])
        o, h, l, c, v = [x[k] for k in ["open", "high", "low", "close", "volume"]]
        algo(o, h, l, c, v, long, short)
        data2.append([x[k] for k in ["date", "close", "long", "short"]])
    data2 = np.array(data2)
    return [
        np.array(x)
        for x in _sim_(
            data2,
            n_slot=conf["n_slot"],
            lev=conf["leverage"],
            take_profit=conf["take_profit"],
            stop_loss=conf["stop_loss"],
            timeout=conf["timeout"],
            fee=conf["fee"],
        )
    ]


@numba.njit
def _sim_(
    data: np.ndarray,
    n_slot: int,
    lev: int,
    take_profit: float,
    stop_loss: float,
    timeout: int,
    fee: float,
):
    cash0 = 1e3
    cash_left = cash0
    worth = cash_left
    open_trades = {}
    trades = []
    hist = []
    n_pair, _, n_time = data.shape
    for t in range(n_time):
        for pair in range(n_pair):
            date, close, long, short = data[pair, :, t]
            for pos in [-1, 1]:
                id = pos * (pair + 1)
                signal = long if pos == 1 else short
                if id not in open_trades:
                    if signal == ENTER and len(open_trades) < n_slot:
                        cash = min(cash_left, worth)
                        open_trades[id] = np.array(
                            [date, close, 0, 0, pos, pair, cash, 0]
                        )
                        cash_left -= cash
                else:
                    x = open_trades[id]
                    duration = x[2] = (date - x[0]) / 60e3
                    # profit
                    p1, p2 = x[1], close
                    diff = pos * (p2 - p1) / p1
                    profit = x[3] = (diff - fee * 2) * lev
                    reason = 0
                    if signal == EXIT:
                        reason = 1
                    elif profit > take_profit:
                        reason = 2
                    elif profit < stop_loss:
                        reason = 3
                    elif duration > timeout:
                        reason = 4
                    if reason:
                        x[0] = date
                        x[-1] = reason
                        del open_trades[id]
                        trades.append(x)
                        cash_left += x[-2] * (1 + profit)
                        worth += x[-2] * profit
        hist.append([date, cash_left, worth])
        if worth < cash0 * 0.1:
            print("you lost 90% of your money :(")
            break
    return hist, trades
