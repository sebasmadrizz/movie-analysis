import numpy as np
from app.ml.predictor import RevenuePredictor
from app.schemas.ml import RevenuePredictionRequest

class MLService:
    def __init__(self, predictor: RevenuePredictor):
        self.predictor = predictor

    def predict_revenue(self, request: RevenuePredictionRequest) -> float:
        features = {
            "budget_log": np.log1p(request.budget),
            "runtime": request.runtime,
            "budget_per_minute": request.budget / request.runtime,
            "budget_vs_genre_historical_ratio": request.budget_vs_genre_historical_ratio,
            "release_year": request.release_year,
            "release_month": request.release_month,
            "release_day_of_week": request.release_day_of_week,
            "genre_count": len(request.genres),
            "director_prior_movies_count": request.director_prior_movies_count,
            "director_historical_avg_revenue": request.director_historical_avg_revenue,
            "top3_cast_historical_avg_revenue": request.top3_cast_historical_avg_revenue,
            "studio_historical_avg_revenue": request.studio_historical_avg_revenue,
            "studio_prior_movies_count": request.studio_prior_movies_count,
            "is_sequel": request.is_sequel,
            "director_is_debut": request.director_is_debut,
            "cast_is_debut": request.cast_is_debut,
            "studio_is_debut": request.studio_is_debut,
            "original_language_code": request.original_language_code,
        }
        return self.predictor.predict(features, request.genres)