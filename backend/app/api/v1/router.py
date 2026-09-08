from fastapi import APIRouter
from app.api.v1 import bi, ml

api_router = APIRouter()
api_router.include_router(bi.router)


api_router.include_router(ml.router)
