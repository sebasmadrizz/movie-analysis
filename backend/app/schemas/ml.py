from datetime import date
from pydantic import BaseModel, Field

class RevenuePredictionRequest(BaseModel):
    budget: float = Field(gt=0)
    runtime: float = Field(gt=0)
    genres: list[str]
    release_date: date
    director_id: int
    cast_ids: list[int]
    studio_id: int
    is_sequel: int
    original_language_code: str

class RevenuePredictionResponse(BaseModel):
    predicted_revenue: float
    director_is_debut: bool
    cast_is_debut: bool
    studio_is_debut: bool