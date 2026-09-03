from fastapi import APIRouter, Depends
from app.api.deps import get_bi_service
from app.services.bi_service import BIService
from app.schemas.bi import MovieProfitOut

router = APIRouter(prefix="/bi", tags=["BI"])

@router.get("/top-profitable-movies", response_model=list[MovieProfitOut])
def top_profitable_movies(limit: int = 10, service: BIService = Depends(get_bi_service)):
    return service.get_top_profitable_movies(limit)