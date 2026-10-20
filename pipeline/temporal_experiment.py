import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from train_model import load_feature_data, build_genre_dummies

CUTOFF_YEAR = 2012

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


def make_model():
    return HistGradientBoostingRegressor(
        max_iter=200, learning_rate=0.03, max_depth=4,
        min_samples_leaf=20, l2_regularization=1.0, random_state=42,
    )


def report(label, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    print(f"{label:38s} R2 = {r2_score(y_true, y_pred):.3f}   "
          f"MAE = {mae:.3f} (about x{np.exp(mae):.1f} off)")


train = df["release_year"] < CUTOFF_YEAR
test = ~train
print(f"train: {train.sum()} movies (before {CUTOFF_YEAR}), test: {test.sum()} movies\n")

# 1) Temporal split, all features
model = make_model().fit(df.loc[train, features], y[train])
pred = model.predict(df.loc[test, features])
report("temporal split, all features", y[test], pred)

# 2) Temporal split without release_year
no_year = [f for f in features if f != "release_year"]
model_ny = make_model().fit(df.loc[train, no_year], y[train])
report("temporal split, no release_year", y[test], model_ny.predict(df.loc[test, no_year]))

# 3) Straight line on budget only (reference)
lin = LinearRegression().fit(df.loc[train, ["budget_log"]], y[train])
report("temporal split, budget-only line", y[test], lin.predict(df.loc[test, ["budget_log"]]))

# 4) Random split with the same test size (what we measured so far)
X_tr, X_te, y_tr, y_te = train_test_split(
    df[features], y, test_size=test.mean(), random_state=42
)
report("random split, all features", y_te, make_model().fit(X_tr, y_tr).predict(X_te))

# Bias by year: negative = the model predicts too low
bias = (pd.Series(pred, index=y[test].index) - y[test]).groupby(df.loc[test, "release_year"])
print("\nMean error by year (log scale, negative = under-predicts):")
print(pd.DataFrame({"mean_error": bias.mean().round(3), "movies": bias.size()}).to_string())