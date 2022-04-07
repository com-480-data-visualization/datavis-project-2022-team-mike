```python
import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from util import save_dataframes, load_dataframes
```

```python
df_games_sales = load_dataframes("vgsales_cleand")
df_games_vote = load_dataframes("games_of_all_time_cleand")
```

```python
def Top_Per(df, value, top='Sales', head = 20, sales_type = 'Global_Sales'):
    plt.figure(figsize=(20,10))
    
    df = df if (value != 'Year') else df[df_games_sales['Year'] > 0]
    df = df.groupby(value).sum().sort_values(sales_type, ascending=False)
    df = df.head(head) if (value != 'Year') else df
    df = pd.DataFrame({value: df.index, sales_type: df[sales_type]}).reset_index(drop=True)

    ax = sns.barplot(x=sales_type, y=value, orient='h', data=df)
    ax.tick_params(axis='both'if (value != 'Year')else'x', labelsize=20)
    
    plt.xlabel('Count (in millions)', size=20)
    plt.ylabel(value, size=20)
    plt.title(f'Top {top} Per {value}', size=24)
    plt.savefig(f'Top {top} Per {value}')
    plt.show()
```

# Sales

```python
df_games_sales.head(10)
```

```python
df_games_sales.info()
```

```python
df_games_sales.isnull().sum()
```

```python
Top_Per(df_games_sales, 'Platform', top='Sales')
```

```python
Top_Per(df_games_sales, 'Genre', top='Sales')
```

```python
Top_Per(df_games_sales, 'Publisher', top='Sales', head = 11)
```

```python
Top_Per(df_games_sales, 'Year', top='Sales')
```

# Votes

```python
df_games_vote.head(10)
```

```python
df_games_vote.info()
```

```python
df_games_vote.isnull().sum()
```

```python
df_games_vote['Name'].nunique()
```

```python
platforms = df_games_vote['Platform'].apply(lambda x : ast.literal_eval(x)).explode().value_counts()
print(f'Number of different platforms: {len(platforms)}')
platforms
```

```python
genres = df_games_vote['Genre'].apply(lambda x : ast.literal_eval(x)).explode().value_counts()
print(f'Number of different platforms: {len(genres)}')
genres
```

```python
df_games_vote['Type'].dropna().value_counts()
```

```python
df_games_vote['Rating'].dropna().value_counts()
```

```python
plt.figure(figsize=(20,10))
ax = sns.kdeplot(data = df_games_vote[['Meta_score', 'User_score']]
                 .rename(columns={'Meta_score': 'Meta Score', 'User_score': 'User Score'}),
                 fill=True,  palette='colorblind')

sns.move_legend(ax, 'upper left')
plt.setp(ax.get_legend().get_texts(), fontsize=24)
ax.tick_params(axis='both', labelsize=20)

plt.xlabel(f'Score', size=20)
plt.ylabel(f'Density', size=20)
plt.title(f'Density Of Meta And User Score', size=24)
plt.savefig('Density Of Meta And User Score')
plt.show()
```

```python

```
