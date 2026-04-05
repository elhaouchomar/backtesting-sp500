# main.py

from memory_reducer import memory_reducer
from create_signal import create_signal
from backtester import backtest
from preprocessing import preprocessing

paths = ["./data/stock_prices.csv", "./data/sp500.csv"]

print("Loading data with memory optimization...")
prices, sp500 = memory_reducer(paths)
print("prices" + "="*100)
print(prices)
print("sp500" + "="*100)
print(sp500)

print("Preprocessing data...")
prices, sp500 = preprocessing(prices, sp500)
print("prices" + "="*100)
print(prices)

print("sp500" + "="*100)
print(sp500)

print("Creating trading signal...")
prices = create_signal(prices)
print("prices" + "="*100)
print(prices)


print("Running backtest...")
backtest(prices, sp500)
print("prices" + "="*100)
print(prices)

print("sp500" + "="*100)
print(sp500)

print("Pipeline completed successfully!")
