```python
import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from util import save_dataframes, load_dataframes
```

```python
df_games_sales = load_dataframes("vgsales_cleand")
df_games_vote = load_dataframes("games_of_all_time_cleand")
```

# Sales

```python
df_games_sales.head(10)
```

```python
def Top_Sales_Per(df_games_sales, value, head = 20, sales_type = 'Global_Sales'):
    plt.figure(figsize=(20,10))
    
    df = df_games_sales if (value != 'Year') else df_games_sales[df_games_sales['Year'] > 0]
    df = df.groupby(value).sum().sort_values(sales_type, ascending=False)
    df = df.head(head) if (value != 'Year') else df
    df = pd.DataFrame({value: df.index, sales_type: df[sales_type]}).reset_index(drop=True)

    g = sns.barplot(x=sales_type, y=value, orient='h', data=df)
    for item in g.get_xticklabels():
        item.set_rotation(45)
    plt.xlabel("Count (in millions)", size=20)
    plt.ylabel(value, size=20)
    plt.title(f"Top Sales Per {value}", size=24)
    plt.show()
```

```python
Top_Sales_Per(df_games_sales, 'Platform')
```

```python
Top_Sales_Per(df_games_sales, 'Genre')
```

```python
Top_Sales_Per(df_games_sales, 'Publisher', head = 11)
```

```python
Top_Sales_Per(df_games_sales, 'Year')
```

```python

```
