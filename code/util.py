import os
import pandas as pd
import numpy as np

ENCODING = 'utf-8'
COMPRESSION = 'bz2'
SPLIT = '\\' if '\\' in os.getcwd() else '/'

DATA_PATH = f'..{SPLIT}data'


def save_dataframes(df, filename, path=DATA_PATH, compression=COMPRESSION, encoding=ENCODING):
    path = "" if path == "" else (path.replace('/', SPLIT)+SPLIT).replace(SPLIT+SPLIT, SPLIT)
    df.to_csv(f"{path}{filename}.csv{'.'+compression if compression != None else ''}",
              compression=compression, encoding=encoding, index=False)


def load_dataframes(filename, path=DATA_PATH, compression=COMPRESSION, encoding=ENCODING):
    path = "" if path == "" else (path.replace('/', SPLIT)+SPLIT).replace(SPLIT+SPLIT, SPLIT)
    return pd.read_csv(f"{path}{filename}.csv{'.'+compression if compression != None else ''}",
                       compression=compression, encoding=encoding)
