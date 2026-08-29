from pathlib import Path
import joblib
import pandas as pd

def test_model_artifact_exists_and_predicts():
    """Verify that models/revenue_model.joblib exists and generates valid log-revenue predictions."""
    model_path = Path(__file__).resolve().parent.parent / "models" / "revenue_model.joblib"
    assert model_path.exists(), "Model artifact revenue_model.joblib does not exist."

    model = joblib.load(model_path)
    
    sample_input = pd.DataFrame([{
        "budget": 100000000,
        "runtime": 120.0,
        "release_year": 2024,
        "release_month": 6,
        "release_day_of_week": 5,
        "genre_count": 2,
        "director_prior_movies_count": 3,
        "director_historical_avg_revenue": 150000000.0,
        "top3_cast_historical_avg_revenue": 80000000.0,
        "original_language_code": "en"
    }])

    prediction = model.predict(sample_input)
    assert len(prediction) == 1
    assert prediction[0] > 0, "Predicted log revenue must be a positive scalar."