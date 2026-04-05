import pandas as pd

def create_signal(path):
    df = pd.read_csv(path)
    return df

