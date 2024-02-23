import pickle
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

DATA_TYPE = Dict[str, Dict[str, np.ndarray]]


def load_data(path, start, stop, plot=False, plot_path="data.png"):
    with open(path, "rb") as f:
        data: DATA_TYPE = pickle.load(f)
    L = len(data["BTCUSDT"]["date"])
    a, b = int(L * start), int(L * stop)
    data2 = {
        k: {k2: v2[a:b] for k2, v2 in v.items()}
        for k, v in data.items()
        if len(v["date"]) == L
    }
    if plot:
        num = 3
        for i, (k, v) in enumerate(data2.items()):
            date = v["date"].astype("datetime64[ms]")
            plt.subplot(num, 1, i + 1)
            plt.plot(date, v["close"])
            plt.title(k)
            if i + 1 == num:
                break
        plt.tight_layout()
        plt.gcf().autofmt_xdate()
        plt.savefig(plot_path)
    return data2
