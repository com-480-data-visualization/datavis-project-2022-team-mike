# %%
import os
import pandas as pd
import numpy as np

# %%
ENCODING = 'utf-8'
COMPRESSION = 'bz2'
SPLIT = '\\' if '\\' in os.getcwd() else '/'

# %%
DATA_PATH = f'data'


# %%
def save_dataframes(df, filename, path=DATA_PATH, compression=COMPRESSION, encoding=ENCODING):
    path = "" if path == "" else (path.replace('/', SPLIT)+SPLIT).replace(SPLIT+SPLIT, SPLIT)
    df.to_csv(f"{path}{filename}.csv{'.'+compression if compression != None else ''}",
              compression=compression, encoding=encoding)


# %%
def load_dataframes(filename, path=DATA_PATH, compression=COMPRESSION, encoding=ENCODING):
    path = "" if path == "" else (path.replace('/', SPLIT)+SPLIT).replace(SPLIT+SPLIT, SPLIT)
    return pd.read_csv(f"{path}{filename}.csv{'.'+compression if compression != None else ''}",
                       compression=compression, encoding=encoding)


# %%
df_games_sales = load_dataframes("vgsales")
df_games_vote = load_dataframes("games_of_all_time")

# %%
#name
df_games_sales['name'] = df_games_sales['Name']
df_games_vote['name'] = df_games_vote['game_name']

#platform
df_games_vote['platform_list']=df_games_vote.apply(lambda row : row['platform'][1:][:-1].replace(' ', '').replace("'", '').split(','), axis=1)
df_games_sales['platform_list']=df_games_sales.apply(lambda row : [row['Platform']], axis=1)



# %%
df = df_games_vote.set_index('name').join(df_games_sales.set_index('name'), how='outer', lsuffix='_vote', rsuffix='_sales')

# %%
df_filtred = df[df['game_name_sales'].notna() & df['game_name_vote'].notna()]
df_filtred[['platform_list_sales', 'platform_list_vote']].head(15)

# %%
