# cspell:ignore talib
import talib as ta

from ricky_s_lib.code_optimizer.CodeOptimizer import CodeOptimizer
from ricky_s_lib.trading.analyze import analyze
from ricky_s_lib.trading.data import load_data
from ricky_s_lib.trading.sim import ENTER, EXIT, sim

ai = CodeOptimizer(
    api_key="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",
    model="gpt-3.5-turbo",
)

path = r"D:\data\crypto\USDT_5m_2022-08-01_2023-08-01.pkl"
data = load_data(path, 0, 1)

code = """
# import talib as ta
# improve the code by adding ta indicators, conditions, and adjusting parameters

def trade_algo(o, h, l, c, v, long, short):
    ma = ta.KAMA(c, 30)
    long[c < ma * 0.97] = ENTER
    long[c > ma * 1.01] = EXIT
    short[c > ma * 1.03] = ENTER
    short[c < ma * 0.99] = EXIT

conf = {
    "take_profit": 0.02,
    "stop_loss": -0.2,
    "timeout": 360,
}
"""

best = None

for i in range(50):
    try:
        trade_algo = None
        conf = None
        exec(code)
        conf["n_slot"] = 5
        conf["leverage"] = 2
        conf["fee"] = 0.0005

        hist, trades = sim(data, trade_algo, conf)
        max_profit, min_dd = hist[:, 2].max() - 1000, hist[:, 3].min()
        result = f"# {len(trades)} trades, max profit {max_profit:.2e} ({max_profit:.2f}) USD, worst drawdown: lost {min_dd*100:.0f}%"
        if best is None or max_profit > best:
            best = max_profit
            analyze(hist, trades)
            with open("best_code.py", "w+") as f:
                f.write("\n\n".join([result, code]))
    except Exception as e:
        result = e

    if i == 0:
        code = ai.set_baseline(code, result)
    else:
        code = ai.feedback(result)
