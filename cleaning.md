```python
import os
import pandas as pd
import numpy as np
from util import save_dataframes, load_dataframes
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
save_dataframes(df_games_sales[df_games_sales['Year'].isna()][['Name', 'Platform', 'Year']].sort_values('Name'), "nan_year_vgsales", compression=None)
```

```python
df_games_sales = load_dataframes("vgsales")
df_games_Year = load_dataframes("year_vgsales", compression=None)
m = {}
def add(row):
    m[f"{row['Name']} : {row['Platform']}"] = row['Year']
df_games_Year.apply(add, axis=1)


def pr(row):
    if(row['Name'] in m):
        row['Year'] = m[f"{row['Name']} : {row['Platform']}"]
    return row
df_games_sales = df_games_sales.apply(pr, axis=1)

#print(df_games_sales[df_games_sales['Year'].isna()][['Name','Year', 'Platform']].sort_values('Name').head(15))
#Year
df_games_sales['Year'] = np.nan_to_num(df_games_sales['Year']).astype(int)

save_dataframes(df_games_sales, "vgsales_cleand")
```

```python
#Names
df_games_vote = load_dataframes("games_of_all_time")
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

#Platform
df_games_vote['Platform']=df_games_vote.apply(lambda row : row['Platform'][1:][:-1].replace(' ', '').replace("'", '').split(','), axis=1)

save_dataframes(df_games_vote, "games_of_all_time_cleand")
```

```python

```

```python
df = df_games_vote.set_index('Name').join(df_games_sales.set_index('Name'), how='outer', lsuffix='_vote', rsuffix='_sales')
df_filtred = df[df['Platform_sales'].notna() & df['Platform_vote'].notna()]
```
