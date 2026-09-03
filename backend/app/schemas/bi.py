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