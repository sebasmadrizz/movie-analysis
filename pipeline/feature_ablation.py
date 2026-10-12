import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import RepeatedKFold, cross_val_score

from train_model import load_feature_data, build_genre_dummies

df = load_feature_data()
df["budget_log"] = np.log1p(df["budget"])
genre_dummies, _ = build_genre_dummies(df)
lang_dummies = pd.get_dummies(df["original_language_code"], prefix="lang")
df = pd.concat([df, genre_dummies, lang_dummies], axis=1)
y = df["target_log_revenue"]

# Feature groups, added cumulatively
steps = [
    ("budget only", ["budget_log"]),
    ("+ runtime, date, genres",
     ["runtime", "release_year", "release_month", "release_day_of_week", "genre_count"]
     + list(genre_dummies.columns)),
    ("+ studio track record",
     ["studio_historical_avg_revenue", "studio_prior_movies_count", "studio_is_debut"]),
    ("+ director and cast track record",
     ["director_prior_movies_count", "director_historical_avg_revenue", "director_is_debut",
      "top3_cast_historical_avg_revenue", "cast_is_debut"]),
    ("+ budget ratios, sequel, language",
     ["budget_per_minute", "budget_vs_genre_historical_ratio", "is_sequel"]
     + list(lang_dummies.columns)),
]

model = HistGradientBoostingRegressor(
    max_iter=200, learning_rate=0.03, max_depth=4,
    min_samples_leaf=20, l2_regularization=1.0, random_state=42,
)
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)

features = []
for name, cols in steps:
    features += cols
    scores = cross_val_score(model, df[features], y, cv=cv, scoring="r2", n_jobs=-1)
    print(f"{name:36s} R2 = {scores.mean():.3f} ± {scores.std():.3f}")