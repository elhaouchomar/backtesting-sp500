import pandas as pd
import numpy as np


def preprocessing(prices, sp500):
    """
    Preprocess stock prices and S&P500 data.

    Parameters:
        prices (pd.DataFrame): Wide-format price data (Date + tickers as columns)
        sp500 (pd.DataFrame): S&P500 OHLC data

    Returns:
        prices (pd.DataFrame): Cleaned panel data with returns
        sp500_returns (pd.Series): Monthly S&P500 returns
    """

    # ---------------------------
    # 1. CLEAN & RESHAPE PRICES
    # ---------------------------
    prices['Date'] = pd.to_datetime(prices['Date'])

    # Wide → long
    prices = prices.melt(id_vars='Date', var_name='Ticker', value_name='Price')

    # Convert to numeric (remove garbage like "4.23M", "ADP", etc.)
    prices['Price'] = pd.to_numeric(prices['Price'], errors='coerce')

    # Drop invalid values
    prices = prices.dropna(subset=['Price'])

    # Remove unrealistic prices
    prices = prices[(prices['Price'] >= 0.1) & (prices['Price'] <= 10000)]

    # Sort properly
    prices = prices.sort_values(['Ticker', 'Date'])

    # ---------------------------
    # 2. MONTHLY RESAMPLING
    # ---------------------------
    prices = (
        prices.set_index('Date')
        .groupby('Ticker')
        .resample('ME')
        .last()
        .reset_index()
    )

    # ---------------------------
    # 3. RETURNS CALCULATION
    # ---------------------------
    prices['monthly_past_return'] = prices.groupby('Ticker')['Price'].pct_change()

    prices['monthly_future_return'] = (
        prices.groupby('Ticker')['Price'].shift(-1) / prices['Price'] - 1
    )

    # ---------------------------
    # 4. OUTLIER HANDLING
    # ---------------------------
    mask_crisis = prices['Date'].dt.year.isin([2008, 2009])

    mask_outlier_past = (
        (prices['monthly_past_return'] > 1) |
        (prices['monthly_past_return'] < -0.5)
    )

    mask_outlier_future = (
        (prices['monthly_future_return'] > 1) |
        (prices['monthly_future_return'] < -0.5)
    )

    prices.loc[~mask_crisis & mask_outlier_past, 'monthly_past_return'] = np.nan
    prices.loc[~mask_crisis & mask_outlier_future, 'monthly_future_return'] = np.nan

    # Forward fill returns per ticker
    prices[['monthly_past_return', 'monthly_future_return']] = (
        prices.groupby('Ticker')[['monthly_past_return', 'monthly_future_return']]
        .ffill()
    )

    # Drop remaining NaNs
    prices = prices.dropna()

    # Final integrity check
    assert prices.isnull().sum().sum() == 0, "Missing values still exist!"

    # Set multi-index
    prices = prices.set_index(['Date', 'Ticker'])

    # ---------------------------
    # 5. S&P 500 PROCESSING
    # ---------------------------
    sp500['Date'] = pd.to_datetime(sp500['Date'])
    sp500 = sp500.sort_values('Date').set_index('Date')

    # Use correct column name from your dataset
    sp500_monthly = sp500['Adjusted Close'].resample('ME').last()

    sp500_returns = sp500_monthly.pct_change().dropna()
    sp500_returns.name = 'sp500_past_return'

    # ---------------------------
    # DONE
    # ---------------------------
    return prices, sp500_returns