import pandas as pd

import numpy as np

def reducer(path):
 
    df = pd.read_csv(path, index_col=0, low_memory=False)

  
    float_cols = df.select_dtypes(include=['floating']).columns
    df[float_cols] = df[float_cols].astype(np.float32)


    int_cols = df.select_dtypes(include=['integer']).columns
    df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast='integer')


    obj_cols = df.select_dtypes(include=['object']).columns
    df[obj_cols] = df[obj_cols].astype('category')
    

    if df.index.dtype == 'object':
        df.index = df.index.astype('category')

    return df

def memory_reducer(paths):
    # paths[0] = stock_prices.csv, paths[1] = sp500.csv
    prices = reducer(paths[0])
    sp500 = reducer(paths[1])
    return prices, sp500