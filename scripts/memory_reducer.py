import pandas as pd
import numpy as np

def reducer(path):
    # index_col=0 is vital. It stops Pandas from creating a new 64-bit ID column.
    df = pd.read_csv(path, index_col=0, low_memory=False)

    # 1. Optimize Floats (Minimum float32 as per your rule)
    float_cols = df.select_dtypes(include=['floating']).columns
    df[float_cols] = df[float_cols].astype(np.float32)

    # 2. Optimize Integers (Vectorized downcasting)
    int_cols = df.select_dtypes(include=['integer']).columns
    df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast='integer')

    # 3. Optimize Objects/Strings -> This is the key for the 0.15MB target!
    obj_cols = df.select_dtypes(include=['object']).columns
    df[obj_cols] = df[obj_cols].astype('category')
    
    # 4. Final Secret: Optimize the Index itself
    if df.index.dtype == 'object':
        df.index = df.index.astype('category')

    return df
def memory_reducer(paths):
    reduced_dataframes = []
    for path in paths:
        reduced_df = reducer(path)
        reduced_dataframes.append(reduced_df)
    return reduced_dataframes
    

