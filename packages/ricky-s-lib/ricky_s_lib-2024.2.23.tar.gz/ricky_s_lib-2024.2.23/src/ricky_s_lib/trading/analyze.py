import matplotlib.pyplot as plt
import numba
import numpy as np


@numba.njit
def drawdown(worth):
    max_w = 0
    dd = np.zeros_like(worth)
    for i, w in enumerate(worth):
        max_w = max(max_w, w)
        dd[i] = w / max_w
    return dd


def analyze(hist: np.ndarray, trades: np.ndarray):
    n_trades = len(trades)
    n_days = (hist[-1, 0] - hist[0, 0]) / (24 * 60 * 60e3)
    title = f"{n_trades} trades in {n_days:.0f} days"

    date = hist[:, 0].astype("datetime64[ms]")
    cash_left = hist[:, 1]
    worth = hist[:, 2]
    dd = drawdown(worth)

    plt.figure(figsize=(8, 10))
    plt.subplot(3, 1, 1)
    plt.title("cash left")
    plt.plot(date, cash_left)

    plt.subplot(3, 1, 2)
    plt.title("worth")
    plt.plot(date, worth)

    plt.subplot(3, 1, 3)
    plt.title("drawdown")
    plt.plot(date, dd)
    plt.axhline(0.5)

    plt.suptitle(title)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig("part1.png")

    date = trades[:, 0].astype("datetime64[ms]")
    duration = trades[:, 2]
    profit = trades[:, 3]
    pos_map = {1: "long", -1: "short"}
    pos = [pos_map[x] for x in trades[:, 4]]
    # pair = trades[:, 5]
    reason_map = {1: "signal", 2: "take profit", 3: "stop loss", 4: "timeout"}
    reason = [reason_map[x] for x in trades[:, -1]]

    plt.figure(figsize=(8, 12))
    plt.subplot(4, 1, 1)
    plt.title("duration")
    plt.hist(duration, 100)

    plt.subplot(4, 1, 2)
    plt.title("profit")
    plt.hist(profit, 100)

    plt.subplot(4, 1, 3)
    plt.title("position")
    plt.hist(pos)

    plt.subplot(4, 1, 4)
    plt.title("exit reason")
    plt.hist(reason)

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig("part2.png")
