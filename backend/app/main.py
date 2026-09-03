from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Movie Analysis API")
app.include_router(api_router, prefix="/api/v1")