import pandas as pd
import matplotlib.pyplot as plt
import os

def backtest(df, sp500):

    df["future_return"] = df.groupby("company")["return"].shift(-1)

    df["pnl"] = df["signal"] * df["future_return"]

    strategy = df.groupby("Date").agg({
        "pnl": "sum",
        "signal": "sum"
    })

    strategy["strategy_return"] = strategy["pnl"] / strategy["signal"].replace(0, 1)
    sp500["Date"] = pd.to_datetime(sp500["Date"])
    sp500 = sp500.sort_values("Date")

    sp500["return"] = sp500["Adjusted Close"].pct_change()

    sp500["pnl"] = 20 * sp500["return"]

    strategy["cum_pnl"] = strategy["pnl"].cumsum()
    sp500["cum_pnl"] = sp500["pnl"].cumsum()

    total_pnl = strategy["cum_pnl"].iloc[-1]

    print("Total PnL:", total_pnl)

    if total_pnl > 75:
        print("WARNING: PnL > 75 → check winsorizing")

    os.makedirs("results", exist_ok=True)

    with open("results/results.txt", "w") as f:
        f.write(f"Strategy Total PnL: {strategy['cum_pnl'].iloc[-1]}\n")
        f.write(f"SP500 Total PnL: {sp500['cum_pnl'].iloc[-1]}\n")

    plt.figure()

    plt.plot(strategy.index, strategy["cum_pnl"], label="Stock Picking 20")
    plt.plot(sp500["Date"], sp500["cum_pnl"], label="SP500 Benchmark")

    plt.title("Cumulative Performance")
    plt.xlabel("Date")
    plt.ylabel("PnL")
    plt.legend()

    plt.savefig("results/performance.png")

    print("Backtest done. Results saved.")