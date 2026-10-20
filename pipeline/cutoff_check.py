import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score

from train_model import load_feature_data, build_genre_dummies

df = load_feature_data()
df["budget_log"] = np.log1p(df["budget"])
genre_dummies, _ = build_genre_dummies(df)
lang_dummies = pd.get_dummies(df["original_language_code"], prefix="lang")
df = pd.concat([df, genre_dummies, lang_dummies], axis=1)

features = [
    "budget_log", "runtime", "release_year", "release_month",
    "release_day_of_week", "genre_count",
    "studio_historical_avg_revenue", "studio_prior_movies_count", "studio_is_debut",
    "director_prior_movies_count", "director_historical_avg_revenue", "director_is_debut",
    "top3_cast_historical_avg_revenue", "cast_is_debut",
    "budget_per_minute", "budget_vs_genre_historical_ratio", "is_sequel",
] + list(genre_dummies.columns) + list(lang_dummies.columns)
no_year = [f for f in features if f != "release_year"]
y = df["target_log_revenue"]

print("cutoff  test_n  with_year  no_year   diff")
for cutoff in range(2008, 2014):
    train = df["release_year"] < cutoff
    test = ~train
    scores = []
    for cols in (features, no_year):
        model = HistGradientBoostingRegressor(
            max_iter=200, learning_rate=0.03, max_depth=4,
            min_samples_leaf=20, l2_regularization=1.0, random_state=42,
        ).fit(df.loc[train, cols], y[train])
        scores.append(r2_score(y[test], model.predict(df.loc[test, cols])))
    print(f"{cutoff}    {test.sum():5d}    {scores[0]:.3f}     {scores[1]:.3f}   {scores[1] - scores[0]:+.3f}")