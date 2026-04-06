import pandas as pd
import numpy as np

def reducer(path):
    df = pd.read_csv(path, low_memory=False)

    df = df.convert_dtypes()

    float_cols = df.select_dtypes(include=['float']).columns
    df[float_cols] = df[float_cols].astype(np.float32)

    int_cols = df.select_dtypes(include=['integer']).columns
    df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast='integer')

    obj_cols = df.select_dtypes(include=['object']).columns
    df[obj_cols] = df[obj_cols].astype('category')

    return df

def memory_reducer(paths):
    prices = reducer(paths[0])
    sp500  = reducer(paths[1])

    prices_mb = prices.memory_usage(deep=False).sum() / 1024 ** 2
    sp500_mb  = sp500.memory_usage(deep=False).sum() / 1024 ** 2

    print(f"Memory usage — prices: {prices_mb:.2f} MB, sp500: {sp500_mb:.3f} MB")
    return prices, sp500