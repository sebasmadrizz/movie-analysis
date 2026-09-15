from fastapi import HTTPException
import numpy as np
from app.ml.predictor import RevenuePredictor
from app.repositories.ml_repository import MLRepository
from app.schemas.ml import RevenuePredictionRequest

class MLService:
    def __init__(self, predictor: RevenuePredictor, repo: MLRepository):
        self.predictor = predictor
        self.repo = repo

    def predict_revenue(self, request: RevenuePredictionRequest) -> float:
        if not self.repo.person_exists(request.director_id):
            raise HTTPException(status_code=404, detail=f"Director with id {request.director_id} not found")

        for cast_id in request.cast_ids:
            if not self.repo.person_exists(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast member with id {cast_id} not found")

        if not self.repo.company_exists(request.studio_id):
            raise HTTPException(status_code=404, detail=f"Studio with id {request.studio_id} not found")

        director_metrics = self.repo.get_director_metrics(request.director_id, request.release_date)
        cast_metrics = self.repo.get_cast_metrics(request.cast_ids, request.release_date)
        studio_metrics = self.repo.get_studio_metrics(request.studio_id, request.release_date)

    

        features = {
            "budget_log": np.log1p(request.budget),
            "runtime": request.runtime,
            "budget_per_minute": request.budget / request.runtime,
            "budget_vs_genre_historical_ratio": request.budget_vs_genre_historical_ratio,
            "release_year": request.release_date.year,
            "release_month": request.release_date.month,
            "release_day_of_week": request.release_date.weekday(),
            "genre_count": len(request.genres),
            "director_prior_movies_count": director_metrics["director_prior_movies_count"],
            "director_historical_avg_revenue": float(director_metrics["director_historical_avg_revenue"]),
            "top3_cast_historical_avg_revenue": float(cast_metrics["top3_cast_historical_avg_revenue"]),
            "studio_historical_avg_revenue": float(studio_metrics["studio_historical_avg_revenue"]),
            "studio_prior_movies_count": studio_metrics["studio_prior_movies_count"],
            "is_sequel": request.is_sequel,
            "director_is_debut": director_metrics["director_is_debut"],
            "cast_is_debut": cast_metrics["cast_is_debut"],
            "studio_is_debut": studio_metrics["studio_is_debut"],
            "original_language_code": request.original_language_code,
        }
        return self.predictor.predict(features, request.genres)