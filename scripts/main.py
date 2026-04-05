# main.py
import pandas as pd
from memory_reducer import memory_reducer 
from preprocessing import preprocessing      # your function to load CSVs
from create_signal import create_signal     # your signal creation function
from backtester import backtest              # backtester we just wrote

paths = [
    "./data/stock_prices.csv",
    "./data/sp500.csv"
]

prices, sp500 = memory_reducer(paths)
# Calculate size in MB
prices_size = prices.memory_usage(deep=True).sum() / (1024**2)
sp500_size = sp500.memory_usage(deep=True).sum() / (1024**2)

print(f"Prices Size: {prices_size:.2f} MB")
print(f"SP500 Size: {sp500_size:.4f} MB")

# Boolean checks for your targets
print(f"Prices under 8MB? {prices_size < 8}")
print(f"SP500 under 0.15MB? {sp500_size < 0.15}")



# prices = create_signal(prices)

# backtest(prices, sp500)
