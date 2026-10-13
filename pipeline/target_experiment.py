import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import RepeatedKFold

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

X = df[features]
y = df["target_log_revenue"]
budget_log = df["budget_log"]

model = HistGradientBoostingRegressor(
    max_iter=200, learning_rate=0.03, max_depth=4,
    min_samples_leaf=20, l2_regularization=1.0, random_state=42,
)
# Same folds as the ablation, so numbers are comparable
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)

linear, direct, residual = [], [], []

for train_idx, test_idx in cv.split(X):
    X_tr, X_te = X.iloc[train_idx], X.iloc[test_idx]
    y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]
    b_tr, b_te = budget_log.iloc[train_idx], budget_log.iloc[test_idx]

    # 1) Straight line on budget only
    lin = LinearRegression().fit(b_tr.to_frame(), y_tr)
    linear.append(r2_score(y_te, lin.predict(b_te.to_frame())))

    # 2) Current approach: predict log revenue directly
    m = clone(model).fit(X_tr, y_tr)
    direct.append(r2_score(y_te, m.predict(X_te)))

    # 3) Predict log revenue minus log budget, then add the budget back.
    #    R2 is still measured against the original log revenue.
    m = clone(model).fit(X_tr, y_tr - b_tr)
    residual.append(r2_score(y_te, m.predict(X_te) + b_te))

linear, direct, residual = map(np.array, (linear, direct, residual))
diff = residual - direct

print(f"linear on budget only            R2 = {linear.mean():.3f} ± {linear.std():.3f}")
print(f"boosting, direct target          R2 = {direct.mean():.3f} ± {direct.std():.3f}")
print(f"boosting, target minus budget    R2 = {residual.mean():.3f} ± {residual.std():.3f}")
print(f"difference (residual - direct)   {diff.mean():+.3f} ± {diff.std():.3f}  "
      f"(better in {(diff > 0).sum()} of {len(diff)} folds)")