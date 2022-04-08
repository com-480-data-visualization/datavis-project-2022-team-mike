# Milestone 1

## Dataset
Our work focuses on two datasets [Video Game Sales | Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales) and [Metacritic Ratings | Kaggle](https://www.kaggle.com/datasets/xcherry/games-of-all-time-from-metacritic). It’s data on sales and ratings of video games.

The first one, [Video Game Sales | Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales), comes from a scrape of the [vgchartz.com](https://vgchartz.com) website. It contains 16 598 records with the name, platform, publisher, year, genre and the related sales in europe, north-america, japan and others.

The second, [Metacritic Ratings | Kaggle](https://www.kaggle.com/datasets/xcherry/games-of-all-time-from-metacritic), includes all games from [Metacritics](https://www.metacritic.com/browse/games/score/metascore/all/all/filtered) at the time of publication. It contains records for 8831 games, scrapped from the website, with details about the score assigned by critics and users, platform, genre, developer, and link to the review of the game.

The first dataset is clean, there is some data missing as the `Year` and `Publisher` that we can easily complete manually.

The second dataset is less clean: for most columns, it is very similar to the first one: there are a few missing values for the ‘developer’ and ‘genre’ that we can complete by hand. However, there is about a quarter of the column ‘type’ (singleplayer, multiplayer, …) with no values, which is problematic; we will try to scrape the Metacritic page again for those entries to fix this. (There is also a lot of missing values for the age rating, but we don’t plan to use this column)

We want to merge those two datasets, such that we can work on one unified basis. That way, the two dataset will complement each other on the different categories (e.g. some platforms are missing on one but not the other, so merging smartly means we can have a more complete list of platforms), and we can make sure we have complete data points for analysis. We plan to do that by joining on the name of the video games; most names are the same in both datasets, but we will implement strategies to match names with slight variations between the datasets.

## Problematic
In this project, we want to explore the different relationships between a video game’s sales success and its reception by players and critics, and how it evolved over time.

Are the user ratings correlated to the sales success of a video game ? How did the market evolve over time, in terms of genre and market sales, in different countries ?

Video games are still widely considered to be a new form of entertainment, despite existing for more than 50 years, and only recently has it been popularized to a larger and larger extent. For instance, in 2020, the video game market exceeded 300 billion in revenue, up from 8 billion in 2000. 

With the advent of the internet, it has also become a rapidly changing and unpredictable market, with many trends coming and going, and many different opinions on the state of the industry. We are currently in a social world and studies about the reasons for success show a high unpredictability and dependency on the opinions of users in a cultural market.[1](#bibliography)

Therefore, it is useful and interesting to analyze how that all evolved, and what was successful throughout the years in terms of sales and critical reception.

We plan to visualize our data based on the different main markets (Europe, North America and Japan), and use different interactive visualizations to show how these markets developed over time. The goal is to clearly see trends in genre, popularity and sales for the different years, and how they unfolded or went away.

## Exploratory Data Analysis

For our exploratory data analysis, we made a [notebook](data_exploration.ipynb) containing basic statistics and simple visualizations.

!["Top Count Per Year"](img/Top_Count_Per_Year.png "Top Count Per Year")

!["Top Count Per Platform"](img/Top_Count_Per_Platform.png "Top Count Per Platform")

![Density Of Meta And User Score](img/Density_Of_Meta_And_User_Score.png "Density Of Meta And User Score")

## Related Work
A full exploratory data analysis and a data visualization is already done on the first dataset [Video Game Sales EDA, Visualizations, ML Models](https://www.kaggle.com/code/vikasukani/video-game-sales-eda-visualizations-ml-models/notebook).

Our approach takes both data sets together to answer the problematic, which has not yet been done on any of these datasets.

We will be inspired by the visualization already done on the first dataset for our own visualization

## Bibliography
1. Experimental Study of Inequality and Unpredictability in an Artificial Cultural Market.
<br>&nbsp;&nbsp;&nbsp;
SCIENCE • 10 Feb 2006 • Vol 311, Issue 5762
<br>&nbsp;&nbsp;&nbsp;
MATTHEW J. SALGANIKPETER SHERIDAN DODDSAND DUNCAN J. WATTS
