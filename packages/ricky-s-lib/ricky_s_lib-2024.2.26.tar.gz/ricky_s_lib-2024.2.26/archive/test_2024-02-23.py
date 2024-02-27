# cspell:ignore talib, openai, backtesting

import talib as ta
from openai import OpenAI

from ricky_s_lib.trading.analyze import analyze
from ricky_s_lib.trading.data import load_data
from ricky_s_lib.trading.sim import ENTER, EXIT, sim

ai = OpenAI(api_key="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")
path = r"D:\data\crypto\USDT_5m_2022-08-01_2023-08-01.pkl"
data = load_data(path, 0, 1)

# loop

trials = []


code = """
# import talib as ta

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

for i in range(10):
    trade_algo = None
    conf = None
    exec(code)
    conf["n_slot"] = 5
    conf["leverage"] = 2
    conf["fee"] = 0.0005

    hist, trades = sim(data, trade_algo, conf)
    max_worth, min_dd = hist[:, 2].max(), hist[:, 3].min()
    result = f"num trades: {len(trades)}, max worth: {max_worth:.2f}, largest drawdown: lost {min_dd*100:.0f}%"
    if best is None or max_worth > best:
        best = max_worth
        analyze(hist, trades)

    trials.append([code, result])

    lines = ["The following are codes and their results"]
    for i, (code, result) in enumerate(trials):
        lines.append(
            f"""
code {i+1}:

{code}

result {i+1}:
{result}
"""
        )
    lines.append(
        """
help me improve the code gradually by comparing the codes and results
(adding ta indicators and conditions, changing parameters etc.)
return me the code string without any explanations, don't say things like "here is the code", don't add missing definitions!
if the conditions are too stringent, there will be no trades, I don't want that! so let's improve a little bit at a time!
"""
    )
    msg = "\n".join(lines)
    print(msg)

    res = ai.chat.completions.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": msg}],
        # temperature=0.7,
        # top_p=1,
    )
    code = res.choices[0].message.content
    print(code)

    with open("msg.txt", "w+") as f:
        print(msg, file=f)
