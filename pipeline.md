```python
import os
import pandas as pd
import numpy as np
```

```python
ENCODING = 'utf-8'
COMPRESSION = 'bz2'
SPLIT = '\\' if '\\' in os.getcwd() else '/'
```

```python
DATA_PATH = f'data'
```

```python
def save_dataframes(df, filename, path=DATA_PATH, compression=COMPRESSION, encoding=ENCODING):
    path = "" if path == "" else (path.replace('/', SPLIT)+SPLIT).replace(SPLIT+SPLIT, SPLIT)
    df.to_csv(f"{path}{filename}.csv{'.'+compression if compression != None else ''}",
              compression=compression, encoding=encoding)
```

```python
def load_dataframes(filename, path=DATA_PATH, compression=COMPRESSION, encoding=ENCODING):
    path = "" if path == "" else (path.replace('/', SPLIT)+SPLIT).replace(SPLIT+SPLIT, SPLIT)
    return pd.read_csv(f"{path}{filename}.csv{'.'+compression if compression != None else ''}",
                       compression=compression, encoding=encoding)
```

```python
df_games_sales = load_dataframes("vgsales")
df_games_vote = load_dataframes("games_of_all_time")
df_games_sales.head(10)
```

```python
#name
df_games_sales['game_name'] = df_games_sales['Name']
df_games_vote['name'] = df_games_vote['game_name']
df_games_sales['name'] = df_games_sales['game_name']

#platform
df_games_vote['platform_list']=df_games_vote.apply(lambda row : row['platform'][1:][:-1].replace(' ', '').replace("'", '').split(','), axis=1)
df_games_sales['platform_list']=df_games_sales.apply(lambda row : [row['Platform']], axis=1)


```

```python
df = df_games_vote.set_index('name').join(df_games_sales.set_index('name'), how='outer', lsuffix='_vote', rsuffix='_sales')
```

```python
df_filtred = df[df['game_name_sales'].notna() & df['game_name_vote'].notna()]
df_filtred[['game_name_sales', 'game_name_vote', 'platform_list_sales', 'platform_list_vote']].head(10)
```

```python

```
