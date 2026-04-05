# main.py

# import data
prices, sp500 = memory_reducer(paths)

# preprocessing
prices, sp500 = preprocessing(prices, sp500)

# create signal
prices = create_signal(prices)

# backtest
backtest(prices, sp500)