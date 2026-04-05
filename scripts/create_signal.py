# create_signal.py
import pandas as pd

def create_signal(prices):
    prices = prices.copy()
    
    # Step 1: 12-month rolling average of past returns
    prices['average_return_1y'] = (
        prices.groupby('ticker')['monthly_past_return']
        .rolling(12, min_periods=12)
        .mean()
        .reset_index(level=0, drop=True)
    )
    
    # Step 2: Rank companies by average_return_1y each month
    prices['rank'] = (
        prices.groupby(level='Date')['average_return_1y']
        .rank(method='first', ascending=False)
    )
    
    # Step 3: Signal is True for top 20 companies
    prices['signal'] = prices['rank'] <= 20
    
    return prices