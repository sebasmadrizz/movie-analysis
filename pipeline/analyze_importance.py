from sklearn.inspection import permutation_importance
import pandas as pd

from train_model import load_feature_data, build_genre_dummies, train_revenue_model
import numpy as np
from sklearn.model_selection import train_test_split


def analyze_feature_importance():
    """Runs permutation importance on the trained model to see which
    features actually drive predictions, and which ones barely matter.
    """
    # Re-load and re-prepare the same data used in training
    df = load_feature_data()
    df["budget_log"] = np.log1p(df["budget"])
    genre_dummies, mlb = build_genre_dummies(df)
    df = pd.concat([df, genre_dummies], axis=1)

    num_features = [
            "budget_log", "runtime", "release_year", "release_month",
            "release_day_of_week", "genre_count",
            "director_prior_movies_count", "director_historical_avg_revenue",
            "top3_cast_historical_avg_revenue",
            "studio_historical_avg_revenue", "studio_prior_movies_count",
            "is_sequel", "director_is_debut", "cast_is_debut", "studio_is_debut",
            "budget_per_minute", "budget_vs_genre_historical_ratio" # <-- ¡Agregadas!
        ] + list(genre_dummies.columns)
    cat_features = ["original_language_code"]

    X = df[num_features + cat_features]
    y = df["target_log_revenue"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Load the already-trained model from disk instead of retraining
    import joblib
    from pathlib import Path
    model_path = Path(__file__).resolve().parent.parent / "models" / "revenue_model.joblib"
    artifact = joblib.load(model_path)
    model = artifact["model"]

    print("Running permutation importance (this may take a minute)...")
    result = permutation_importance(
        model, X_test, y_test,
        n_repeats=10, random_state=42, scoring="r2"
    )

    importances_df = pd.DataFrame({
        "feature": X_test.columns,
        "importance_mean": result.importances_mean,
        "importance_std": result.importances_std
    }).sort_values("importance_mean", ascending=False)

    print(importances_df.head(20).to_string(index=False))
    return importances_df


if __name__ == "__main__":
    analyze_feature_importance()