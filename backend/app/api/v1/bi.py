from fastapi import APIRouter, Depends
from app.api.deps import get_bi_service
from app.services.bi_service import BIService
from app.schemas.bi import DirectorActorDuoOut, GenrePerformanceOut, MovieProfitOut, TopDirectorOut, TopLeadActorOut

router = APIRouter(prefix="/bi", tags=["BI"])

@router.get("/top-profitable-movies", response_model=list[MovieProfitOut])
def top_profitable_movies(limit: int = 10, service: BIService = Depends(get_bi_service)):
    return service.get_top_profitable_movies(limit)

@router.get("/genre-performance", response_model=list[GenrePerformanceOut])
def genre_performance(limit: int = 10, service: BIService = Depends(get_bi_service)):
    return service.get_genre_performance(limit)

@router.get("/top-roi-movies", response_model=list[MovieProfitOut])
def top_roi_movies(limit: int = 10, service: BIService = Depends(get_bi_service)):
    return service.get_top_roi_movies(limit)

@router.get("/top-directors", response_model=list[TopDirectorOut])
def top_directors(limit: int = 10, service: BIService = Depends(get_bi_service)):
    return service.get_top_directors(limit)

@router.get("/top-lead-actors", response_model=list[TopLeadActorOut])
def top_lead_actors(limit: int = 10, service: BIService = Depends(get_bi_service)):
    return service.get_top_lead_actors(limit)

@router.get("/director-actor-duos", response_model=list[DirectorActorDuoOut])
def director_actor_duos(limit: int = 10, service: BIService = Depends(get_bi_service)):
    return service.get_top_director_actor_duos(limit)