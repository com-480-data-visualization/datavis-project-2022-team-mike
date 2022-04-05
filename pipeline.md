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
              compression=compression, encoding=encoding, index=False)
```

```python
def load_dataframes(filename, path=DATA_PATH, compression=COMPRESSION, encoding=ENCODING):
    path = "" if path == "" else (path.replace('/', SPLIT)+SPLIT).replace(SPLIT+SPLIT, SPLIT)
    return pd.read_csv(f"{path}{filename}.csv{'.'+compression if compression != None else ''}",
                       compression=compression, encoding=encoding)
```

```python
# compresses data
df = load_dataframes("vgsales", compression=None)
save_dataframes(df, "vgsales")
df = load_dataframes("games_of_all_time", compression=None)
save_dataframes(df, "games_of_all_time")
```

```python
# get missing year game name
df_games_sales = load_dataframes("vgsales")
save_dataframes(df_games_sales[df_games_sales['Year'].isna()][['Name','Year']].drop_duplicates().sort_values('Name'), "nan_year_vgsales", compression=None)
```

```python
df_games_sales = load_dataframes("vgsales")
df_games_Year = load_dataframes("year_vgsales", compression=None)
m = {}
def add(row):
    m[row['Name']] = row['Year']
df_games_Year.apply(add, axis=1)


def pr(row):
    if(row['Name'] in m):
        row['Year'] = int(m[row['Name']])
    return row
df_games_sales = df_games_sales.apply(pr, axis=1)

df_games_sales = load_dataframes("vgsales_completed")
```

```python
df_games_sales = load_dataframes("vgsales")
df_games_sales.head(10)
```

```python
df_games_vote = load_dataframes("games_of_all_time")
df_games_vote.head(10)
```

```python
#name
df_games_vote = df_games_vote.rename(columns={'game_name': 'Name', 
                                              'meta_score': 'Meta_score',
                                              'user_score': 'User_score',
                                              'platform': 'Platform',
                                              'description': 'Description',
                                              'url': 'URL',
                                              'developer': 'Developer',
                                              'genre': 'Genre',
                                              'type': 'Type',
                                              'rating': 'Rating'})
print(df_games_sales)

#platform
df_games_vote['Platform']=df_games_vote.apply(lambda row : row['Platform'][1:][:-1].replace(' ', '').replace("'", '').split(','), axis=1)
df_games_sales['Platform']=df_games_sales.apply(lambda row : [row['Platform']], axis=1)

#Year
df_games_sales['Year'] = np.nan_to_num(df_games_sales['Year']).astype(int)

```

```python
df = df_games_vote.set_index('Name').join(df_games_sales.set_index('Name'), how='outer', lsuffix='_vote', rsuffix='_sales')
```

```python
df_filtred = df[df['Platform_sales'].notna() & df['Platform_vote'].notna()]
df_filtred[['Platform_sales', 'Platform_vote']].head(15)
```

```python

```

```python

```
