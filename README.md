# Netflix Movies Analysis (1990s Genre & Runtime Trends)

Analyzes the public [Netflix Movies and TV Shows dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) (Kaggle) to explore how movie runtime and genre popularity looked in the 1990s, and to identify short-duration Action films.

## What this does

- Filters the dataset to 1990s movie releases
- Computes average runtime per genre
- Visualizes genre distribution (which genres had the most 1990s titles)
- Flags short-duration (<90 min) Action films specifically

## Setup

```bash
pip install -r requirements.txt
```

Download `netflix_titles.csv` from the [Kaggle dataset page](https://www.kaggle.com/datasets/shivamb/netflix-shows) and place it in this folder.

## Run

```bash
python netflix_analysis.py
```

## Output

- `avg_runtime_by_genre.png` — bar chart of average runtime per genre
- `genre_distribution.png` — bar chart of title count per genre
- `short_action_films_1990s.csv` — list of short Action films found

## Key design decisions

- **Genres are split, not left as one string.** The raw data lists genres like `"Action & Adventure, Dramas"` in a single field — I split (`explode`) these so each genre gets counted correctly, instead of "Action, Dramas" being treated as one unique category.
- **Only Movies are analyzed, not TV Shows.** TV Shows use "3 Seasons" instead of a minute count in the `duration` column, so mixing them would break the runtime math.
- **Missing runtime values are dropped, not filled in.** Guessing a runtime would distort the averages — better to analyze only complete data and be transparent about it.
