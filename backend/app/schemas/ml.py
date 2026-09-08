from pydantic import BaseModel

class RevenuePredictionRequest(BaseModel):
    budget: float
    runtime: float
    genres: list[str]
    release_year: int
    release_month: int
    release_day_of_week: int
    director_prior_movies_count: int
    director_historical_avg_revenue: float
    top3_cast_historical_avg_revenue: float
    studio_historical_avg_revenue: float
    studio_prior_movies_count: int
    is_sequel: int
    director_is_debut: int
    cast_is_debut: int
    studio_is_debut: int
    original_language_code: str
    budget_vs_genre_historical_ratio: float

class RevenuePredictionResponse(BaseModel):
    predicted_revenue: float