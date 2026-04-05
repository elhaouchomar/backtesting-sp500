import pandas as pd
import matplotlib.pyplot as plt
import os

def backtest(df, sp500):
    df = df.copy()
    os.makedirs("results/plots", exist_ok=True)
    
    if df.empty or sp500.empty:
        raise ValueError("DataFrames are empty")
    
    df["future_return"] = df.groupby("ticker")["monthly_future_return"].shift(-1)
    df = df.dropna(subset=["future_return"])
    df["pnl"] = df["signal"].astype(int) * df["future_return"]
    
    strategy = df.groupby(level='Date').agg({"pnl": "sum", "signal": "sum"})
    strategy["strategy_return"] = strategy["pnl"] / strategy["signal"].replace(0, 1)
    
    sp500 = sp500.copy()
    sp500["pnl"] = 20 * sp500["return"]
    
    common = strategy.index.intersection(sp500.index)
    if len(common) == 0:
        raise ValueError("No common dates")
    
    strategy, sp500 = strategy.loc[common], sp500.loc[common]
    strategy["cum_pnl"] = strategy["pnl"].cumsum()
    sp500["cum_pnl"] = sp500["pnl"].cumsum()
    
    total_pnl = strategy["cum_pnl"].iloc[-1]
    
    print(f"Strategy PnL: ${total_pnl:.2f} | SP500: ${sp500['cum_pnl'].iloc[-1]:.2f}")
    if total_pnl > 75:
        print("WARNING: PnL > 75")
    
    with open("results/results.txt", "w") as f:
        f.write(f"Strategy PnL: ${strategy['cum_pnl'].iloc[-1]:.2f}\n")
        f.write(f"SP500 PnL: ${sp500['cum_pnl'].iloc[-1]:.2f}\n")
        f.write(f"Trading months: {len(strategy)}\n")
        f.write(f"Avg monthly PnL: ${strategy['pnl'].mean():.4f}\n")
        f.write(f"Avg positions: {strategy['signal'].mean():.1f}")
    
    plt.figure(figsize=(12, 6))
    plt.plot(strategy.index, strategy["cum_pnl"], label="Strategy", linewidth=2)
    plt.plot(sp500.index, sp500["cum_pnl"], label="SP500", linewidth=2, linestyle='--')
    plt.fill_between(strategy.index, strategy["cum_pnl"], sp500["cum_pnl"], alpha=0.3)
    plt.title("Cumulative Performance")
    plt.xlabel("Date")
    plt.ylabel("PnL ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("results/plots/performance.png", dpi=150)
    plt.close()
    
    
    print("Backtest complete. Results in results/")
    return strategy, sp500