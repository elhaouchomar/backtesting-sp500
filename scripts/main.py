# main.py
import pandas as pd
from memory_reducer import memory_reducer       # your function to load CSVs
from create_signal import create_signal     # your signal creation function
from backtester import backtest              # backtester we just wrote

paths = {
    "prices": "../data/stock_prices.csv",
    "sp500": "../data/sp500.csv"
}

prices, sp500 = memory_reducer(paths)

# prices, sp500 = preprocessing(prices, sp500)

# prices = create_signal(prices)

# backtest(prices, sp500)
