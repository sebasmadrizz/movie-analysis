import os

import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import RepeatedKFold, cross_val_score

from train_model import load_feature_data, build_genre_dummies

load_dotenv()
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "moviedb"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
)
cur = conn.cursor()
cur.execute(
    "SELECT mk.movie_id, k.keyword_name "
    "FROM movie_keywords mk JOIN dim_keywords k ON mk.keyword_id = k.keyword_id"
)
kw = pd.DataFrame(cur.fetchall(), columns=["movie_id", "keyword_name"])
conn.close()

df = load_feature_data()
df["budget_log"] = np.log1p(df["budget"])
genre_dummies, _ = build_genre_dummies(df)
lang_dummies = pd.get_dummies(df["original_language_code"], prefix="lang")
df = pd.concat([df, genre_dummies, lang_dummies], axis=1)

base_features = [
    "budget_log", "runtime", "release_year", "release_month",
    "release_day_of_week", "genre_count",
    "studio_historical_avg_revenue", "studio_prior_movies_count", "studio_is_debut",
    "director_prior_movies_count", "director_historical_avg_revenue", "director_is_debut",
    "top3_cast_historical_avg_revenue", "cast_is_debut",
    "budget_per_minute", "budget_vs_genre_historical_ratio", "is_sequel",
] + list(genre_dummies.columns) + list(lang_dummies.columns)

# 'sequel' is already captured by is_sequel
kw = kw[(kw["keyword_name"] != "sequel") & kw["movie_id"].isin(df["movie_id"])]
counts = kw["keyword_name"].value_counts()


def keyword_matrix(n):
    top = counts.head(n).index
    sub = kw[kw["keyword_name"].isin(top)]
    m = pd.crosstab(sub["movie_id"], sub["keyword_name"]).clip(upper=1)
    m = m.reindex(df["movie_id"]).fillna(0).astype(int)
    m.index = df.index
    m.columns = [f"kw_{c}" for c in m.columns]
    return m


y = df["target_log_revenue"]
model = HistGradientBoostingRegressor(
    max_iter=200, learning_rate=0.03, max_depth=4,
    min_samples_leaf=20, l2_regularization=1.0, random_state=42,
)
# Same folds every call, so scores are paired fold by fold
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)

baseline = cross_val_score(model, df[base_features], y, cv=cv, scoring="r2", n_jobs=-1)
print(f"no keywords        R2 = {baseline.mean():.3f} ± {baseline.std():.3f}")

for n in (25, 75):
    X = pd.concat([df[base_features], keyword_matrix(n)], axis=1)
    scores = cross_val_score(model, X, y, cv=cv, scoring="r2", n_jobs=-1)
    diff = scores - baseline
    print(f"top {n:<3d} keywords   R2 = {scores.mean():.3f} ± {scores.std():.3f}   "
          f"diff {diff.mean():+.3f} ± {diff.std():.3f}  "
          f"(better in {(diff > 0).sum()} of {len(diff)} folds)")


print("\nTop 25 keywords:")
print(counts.head(25).to_string())

per_movie = kw.groupby("movie_id").size().reindex(df["movie_id"]).fillna(0)
print(f"\nkeywords per training movie: median {per_movie.median():.0f}, "
      f"share with none {(per_movie == 0).mean():.0%}")