from pathlib import Path
import joblib
import numpy as np
import pandas as pd


def test_model_artifact_exists_and_predicts():
    """Verify that models/revenue_model.joblib exists and generates valid log-revenue predictions."""
    model_path = Path(__file__).resolve().parent.parent / "models" / "revenue_model.joblib"
    assert model_path.exists(), "Model artifact revenue_model.joblib does not exist."

    artifact = joblib.load(model_path)
    model = artifact["model"]
    mlb = artifact["mlb"]

    # Use the persisted MultiLabelBinarizer to build genre columns the same way
    # they were built at training time — no need to guess column names by hand.
    sample_genres = [["Action", "Adventure"]]
    genre_dummies = pd.DataFrame(
        mlb.transform(sample_genres),
        columns=[f"genre_{g}" for g in mlb.classes_]
    )

    sample_data = {
    "budget_log": np.log1p(100_000_000),
    "runtime": 120.0,
    "release_year": 2024,
    "release_month": 6,
    "release_day_of_week": 5,
    "genre_count": 2,
    "director_prior_movies_count": 3,
    "director_historical_avg_revenue": 150000000.0,
    "top3_cast_historical_avg_revenue": 80000000.0,
    "studio_historical_avg_revenue": 200000000.0,
    "studio_prior_movies_count": 5,
    "is_sequel": 0,
    "director_is_debut": 0,
    "cast_is_debut": 0,
    "studio_is_debut": 0,
    "original_language_code": "en",
}

    sample_input = pd.concat(
        [pd.DataFrame([sample_data]), genre_dummies],
        axis=1
    )

    prediction = model.predict(sample_input)
    assert len(prediction) == 1
    assert prediction[0] > 0, "Predicted log revenue must be a positive scalar."