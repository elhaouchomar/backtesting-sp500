import pandas as pd
import numpy as np
import os

def preprocessing(prices, sp500):
    # Clean and prepare prices
    prices.columns = [c.strip() for c in prices.columns]
    sp500.columns = [c.strip() for c in sp500.columns]
    
    prices['Date'] = pd.to_datetime(prices['Date'])
    sp500['Date'] = pd.to_datetime(sp500['Date'])
    
    # Convert wide to long format if needed
    if 'Ticker' not in prices.columns:
        prices = prices.melt(id_vars='Date', var_name='ticker', value_name='price')
    
    prices = prices.sort_values(['ticker', 'Date'])
    
    # Resample to month end (keep last value)
    prices = prices.set_index('Date').groupby('ticker').resample('ME', include_groups=False).last().reset_index()
    
    # Filter price outliers
    prices = prices[(prices['price'] >= 0.1) & (prices['price'] <= 10000)]
    
    # Compute monthly returns
    prices['monthly_past_return'] = prices.groupby('ticker')['price'].pct_change()
    prices['monthly_future_return'] = prices.groupby('ticker')['price'].shift(-1) / prices['price'] - 1
    
    # Handle outliers (exclude 2008-2009 crisis)
    crisis = prices['Date'].dt.year.isin([2008, 2009])
    outlier_past = (prices['monthly_past_return'] > 1) | (prices['monthly_past_return'] < -0.5)
    outlier_future = (prices['monthly_future_return'] > 1) | (prices['monthly_future_return'] < -0.5)
    
    prices.loc[~crisis & outlier_past, 'monthly_past_return'] = np.nan
    prices.loc[~crisis & outlier_future, 'monthly_future_return'] = np.nan
    
    # Fill missing values using last available value per company
    prices[['monthly_past_return', 'monthly_future_return']] = prices.groupby('ticker')[['monthly_past_return', 'monthly_future_return']].ffill()
    
    # Drop rows where future_return is NaN (end of series)
    prices = prices.dropna(subset=['monthly_future_return'])
    prices = prices.dropna(subset=['monthly_past_return'])
    
    # Verify no missing values
    assert prices.isnull().sum().sum() == 0, "Missing values still exist!"
    
    # Process SP500
    sp500 = sp500.sort_values('Date').set_index('Date').resample('ME').last()
    sp500['return'] = sp500['Adjusted Close'].pct_change()
    sp500 = sp500.dropna()[['return']]
    
    # Save outliers.txt with actual data outliers
    os.makedirs("results", exist_ok=True)
    
    # Find actual outliers in the data
    outliers = []
    
    # Find extreme price outliers
    extreme_prices = prices.nlargest(10, 'price')[['ticker', 'Date', 'price']]
    for _, row in extreme_prices.iterrows():
        outliers.append({
            'ticker': row['ticker'],
            'date': row['Date'],
            'price': row['price'],
            'type': 'price',
            'reason': f'Extreme high price: ${row["price"]:.2f}'
        })
    
    # Find extreme return outliers
    extreme_returns = prices.nlargest(10, 'monthly_past_return')[['ticker', 'Date', 'monthly_past_return']]
    for _, row in extreme_returns.iterrows():
        if row['monthly_past_return'] > 0.5:
            outliers.append({
                'ticker': row['ticker'],
                'date': row['Date'],
                'price': row['monthly_past_return'],
                'type': 'return',
                'reason': f'Extreme monthly return: {row["monthly_past_return"]:.1%}'
            })
    
    # Save first 5 outliers
    with open("results/outliers.txt", "w") as f:
        f.write("STOCK PRICE OUTLIERS - IDENTIFIED FROM DATASET\n")
        f.write("=" * 60 + "\n\n")
        f.write("These outliers were found by scanning the actual data:\n\n")
        
        for i, o in enumerate(outliers[:5], 1):
            f.write(f"OUTLIER {i}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Ticker: {o['ticker']}\n")
            f.write(f"Date: {o['date'].strftime('%Y-%m-%d')}\n")
            if o['type'] == 'price':
                f.write(f"Price: ${o['price']:.2f}\n")
            else:
                f.write(f"Return: {o['price']:.1%}\n")
            f.write(f"Reason: {o['reason']}\n")
            f.write(f"Source: Original stock_prices.csv dataset\n\n")
        
        f.write("\nNOTE: These outliers were identified by analyzing extreme values\n")
        f.write("in the dataset. During 2008-2009 crisis, return outliers were preserved.\n")
    
    return prices.set_index(['Date', 'ticker']), sp500