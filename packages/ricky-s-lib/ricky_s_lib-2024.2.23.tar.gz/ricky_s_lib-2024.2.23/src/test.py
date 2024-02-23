import talib as ta

from ricky_s_lib.trading.analyze import analyze
from ricky_s_lib.trading.data import load_data
from ricky_s_lib.trading.sim import ENTER, EXIT, sim

path = r"D:\data\crypto\USDT_5m_2022-08-01_2023-08-01.pkl"
data = load_data(path, 0, 0.1)


def sample_algo(o, h, l, c, v, long, short):
    sma = ta.SMA(c, 20)
    long[c < sma * 0.97] = ENTER
    long[c > sma * 1.01] = EXIT


hist, trades = sim(
    data,
    sample_algo,
    {
        "n_slot": 5,
        "leverage": 2,
        "take_profit": 0.02,
        "stop_loss": -0.2,
        "timeout": 300,
        "fee": 0.0005,
    },
)
analyze(hist, trades)
