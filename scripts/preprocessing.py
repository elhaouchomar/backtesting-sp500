import pandas as pd
import numpy as np

def preprocessing(prices, sp500):
   
    prices['Date'] = pd.to_datetime(prices['Date'])
    prices = prices.sort_values(['Ticker', 'Date'])

   
    prices = (
        prices.set_index('Date')
        .groupby('Ticker')
        .resample('M')
        .last()
        .drop(columns='ticker')
        .reset_index()
    )

   
    prices = prices[(prices['price'] >= 0.1) & (prices['price'] <= 10000)]

    prices['monthly_past_return'] = prices.groupby('ticker')['price'].pct_change()

    prices['monthly_future_return'] = prices.groupby('ticker')['price'].shift(-1) / prices['price'] - 1


    mask_crisis = prices['date'].dt.year.isin([2008, 2009])
    mask_outlier_past = (prices['monthly_past_return'] > 1) | (prices['monthly_past_return'] < -0.5)
    mask_outlier_future = (prices['monthly_future_return'] > 1) | (prices['monthly_future_return'] < -0.5)

    prices.loc[~mask_crisis & mask_outlier_past, 'monthly_past_return'] = np.nan
    prices.loc[~mask_crisis & mask_outlier_future, 'monthly_future_return'] = np.nan

   
    prices[['monthly_past_return', 'monthly_future_return']] = (
        prices.groupby('ticker')[['monthly_past_return', 'monthly_future_return']]
        .ffill()
    )

    prices = prices.dropna()
    assert prices.isnull().sum().sum() == 0, "Missing values still exist!"

  
    prices = prices.set_index(['date', 'ticker'])

    sp500['Date'] = pd.to_datetime(sp500['Date'])
    sp500 = sp500.sort_values('Date').set_index('Date')
    
   
    sp500_monthly = sp500['Adj Close'].resample('M').last()
    sp500_returns = sp500_monthly.pct_change().dropna()
    
    
    sp500_returns.name = 'sp500_past_return'

    return prices, sp500_returns