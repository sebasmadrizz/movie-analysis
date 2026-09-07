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

class TopDirectorOut(BaseModel):
    person_id: int
    director_name: str
    total_movies_directed: int
    total_box_office: float
    total_profit: float


class TopLeadActorOut(BaseModel):
    person_id: int
    actor_name: str
    lead_roles_count: int
    total_box_office: float
    avg_box_office_per_movie: float


class DirectorActorDuoOut(BaseModel):
    director_name: str
    actor_name: str
    collaborations: int
    total_box_office: float
    avg_roi: float | None

class ProductionCompanyOut(BaseModel):
    company_id: int
    company_name: str
    movies_produced: int
    total_budget: float
    total_revenue: float
    total_profit: float
    market_share_pct: float | None

class CriticalCommercialOut(BaseModel):
    movie_id: int
    title: str
    vote_average: float
    vote_count: int
    roi: float | None
    performance_segment: str


class FinancialFlopOut(BaseModel):
    movie_id: int
    title: str
    release_date: date | None
    budget: float
    revenue: float
    net_loss: float
    roi: float | None

class WorstDirectorOut(BaseModel):
    person_id: int
    director_name: str
    total_movies_directed: int
    total_budget: float
    total_revenue: float
    total_net_profit: float
    avg_roi: float | None

class LowestRoiActorOut(BaseModel):
    person_id: int
    actor_name: str
    lead_roles_count: int
    total_budget_spent: float
    total_box_office: float
    total_net_profit: float
    avg_roi: float | None