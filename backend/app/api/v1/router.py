from fastapi import APIRouter
from app.api.v1 import bi

api_router = APIRouter()
api_router.include_router(bi.router)