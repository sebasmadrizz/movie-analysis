from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.bi_repository import BIRepository
from app.services.bi_service import BIService
from app.ml.predictor import RevenuePredictor
from app.services.ml_service import MLService


_predictor = RevenuePredictor() 

def get_bi_service(db: Session = Depends(get_db)) -> BIService:
    return BIService(BIRepository(db))


def get_ml_service() -> MLService:
    return MLService(_predictor)