from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.bi_repository import BIRepository
from app.services.bi_service import BIService

def get_bi_service(db: Session = Depends(get_db)) -> BIService:
    return BIService(BIRepository(db))