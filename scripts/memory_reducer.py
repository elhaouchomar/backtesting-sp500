import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
def reducer(path):
    df = pd.read_csv(path)
    for label, content in df.items():
        if is_numeric_dtype(content) :
            c_min = content.min()
            c_max = content.max()
            print(content.dtype.kind)
            if content.dtype.kind in 'iu':
                print('hello')
                if c_min >= np.iinfo(np.int8).min and c_max <= np.iinfo(np.int8).max:
                    df[label] = content.astype(np.int8)
                elif c_min >= np.iinfo(np.int16).min and c_max <= np.iinfo(np.int16).max:
                    df[label] = content.astype(np.int16)
                elif c_min >= np.iinfo(np.int32).min and c_max <= np.iinfo(np.int32).max:
                    df[label] = content.astype(np.int32)
                else:
                    df[label] = content.astype(np.int64)
            else:
                if c_min >= np.finfo(np.float32).min and c_max <= np.finfo(np.float32).max:
                    df[label] = content.astype(np.float32)
                else:
                    df[label] = content.astype(np.float64)
        else :
            df[label] = content.astype('category')

    return df

def memory_reducer(paths):
    reduced_dataframes = []
    for path in paths:
        reduced_df = reducer(path)
        reduced_dataframes.append(reduced_df)
    return reduced_dataframes
    

