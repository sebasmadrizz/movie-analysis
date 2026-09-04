from datetime import date
from pydantic import BaseModel

class MovieProfitOut(BaseModel):
    movie_id: int
    title: str
    release_date: date | None
    budget: float
    revenue: float
    net_profit: float
    roi: float | None

class GenrePerformanceOut(BaseModel):
    genre_name: str
    total_movies: int
    total_budget: float
    total_revenue: float
    total_profit: float
    avg_roi: float | None
    