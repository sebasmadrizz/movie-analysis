from pathlib import Path
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "revenue_model.joblib"

class RevenuePredictor:
    def __init__(self):
        artifact = joblib.load(MODEL_PATH)
        self.model = artifact["model"]
        self.mlb = artifact["mlb"]

    def predict(self, features: dict, genres: list[str]) -> float:
        genre_dummies = pd.DataFrame(
            self.mlb.transform([genres]),
            columns=[f"genre_{g}" for g in self.mlb.classes_]
        )
        input_df = pd.concat([pd.DataFrame([features]), genre_dummies], axis=1)
        log_prediction = self.model.predict(input_df)
        revenue = np.expm1(log_prediction[0])
        return float(revenue)