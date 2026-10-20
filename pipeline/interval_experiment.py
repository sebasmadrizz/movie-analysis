import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split

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
y = df["target_log_revenue"]


def fit_quantile(X, target, q):
    return HistGradientBoostingRegressor(
        loss="quantile", quantile=q, max_iter=200, learning_rate=0.03,
        max_depth=4, min_samples_leaf=20, l2_regularization=1.0, random_state=42,
    ).fit(X, target)


def evaluate(label, X_tr, y_tr, X_te, y_te):
    lo = fit_quantile(X_tr, y_tr, 0.1).predict(X_te)
    hi = fit_quantile(X_tr, y_tr, 0.9).predict(X_te)
    inside = ((y_te.values >= lo) & (y_te.values <= hi)).mean()
    ratio = np.median(np.exp(hi - lo))
    print(f"{label:22s} 80% interval contains the real value in {inside:.0%} of movies; "
          f"upper bound is about x{ratio:.1f} the lower bound")


X_tr, X_te, y_tr, y_te = train_test_split(df[features], y, test_size=0.2, random_state=42)
evaluate("random split", X_tr, y_tr, X_te, y_te)

train = df["release_year"] < 2012
evaluate("temporal split (2012+)", df.loc[train, features], y[train],
         df.loc[~train, features], y[~train])