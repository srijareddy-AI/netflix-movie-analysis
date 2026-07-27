"""
Netflix Movies Analysis (1990s focus)
--------------------------------------
Analyzes the public "Netflix Movies and TV Shows" dataset (netflix_titles.csv,
originally published on Kaggle by Shivam Bansal) to explore runtime trends
across genres in the 1990s, and to compare genre-wise title distribution.

Author: Srija Reddy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------
# Download netflix_titles.csv from:
# https://www.kaggle.com/datasets/shivamb/netflix-shows
# and place it in the same folder as this script.
df = pd.read_csv("netflix_titles.csv")

# ---------------------------------------------------------
# 2. Clean and filter
# ---------------------------------------------------------
# Keep only Movies (TV Shows use "seasons" instead of minutes for duration)
movies = df[df["type"] == "Movie"].copy()

# Extract numeric minutes from "90 min" style strings
movies["duration_min"] = (
    movies["duration"].str.extract(r"(\d+)").astype(float)
)

# Filter to 1990s releases
movies_90s = movies[(movies["release_year"] >= 1990) & (movies["release_year"] <= 1999)]

# A title can have multiple genres in "listed_in" (comma-separated) —
# split them out so each genre is counted properly instead of as one long string
movies_90s = movies_90s.assign(genre=movies_90s["listed_in"].str.split(", ")).explode("genre")

# Drop rows with missing runtime — can't analyze what we don't have
movies_90s = movies_90s.dropna(subset=["duration_min"])

print(f"Movies from the 1990s in dataset: {movies_90s['title'].nunique()}")

# ---------------------------------------------------------
# 3. Genre-wise average runtime
# ---------------------------------------------------------
avg_runtime_by_genre = (
    movies_90s.groupby("genre")["duration_min"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
sns.barplot(x=avg_runtime_by_genre.values, y=avg_runtime_by_genre.index, hue=avg_runtime_by_genre.index, palette="viridis", legend=False)
plt.xlabel("Average Runtime (minutes)")
plt.title("Average Movie Runtime by Genre — 1990s Netflix Titles")
plt.tight_layout()
plt.savefig("avg_runtime_by_genre.png")
plt.close()

# ---------------------------------------------------------
# 4. Genre-wise title count (distribution)
# ---------------------------------------------------------
genre_counts = movies_90s["genre"].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, hue=genre_counts.index, palette="magma", legend=False)
plt.xlabel("Number of Titles")
plt.title("Genre Distribution — 1990s Netflix Movies")
plt.tight_layout()
plt.savefig("genre_distribution.png")
plt.close()

# ---------------------------------------------------------
# 5. Short-duration Action films
# ---------------------------------------------------------
short_action = movies_90s[
    (movies_90s["genre"].str.contains("Action", na=False)) & (movies_90s["duration_min"] < 90)
][["title", "release_year", "duration_min"]].drop_duplicates().sort_values("duration_min")

print("\nShort-duration (<90 min) Action films from the 1990s:")
print(short_action.to_string(index=False))

short_action.to_csv("short_action_films_1990s.csv", index=False)

print("\nDone. Charts saved as avg_runtime_by_genre.png and genre_distribution.png")
