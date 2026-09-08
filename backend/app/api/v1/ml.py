from fastapi import APIRouter, Depends
from app.api.deps import get_ml_service
from app.services.ml_service import MLService
from app.schemas.ml import RevenuePredictionRequest, RevenuePredictionResponse

router = APIRouter(prefix="/ml", tags=["ML"])

@router.post("/predict-revenue", response_model=RevenuePredictionResponse)
def predict_revenue(request: RevenuePredictionRequest, service: MLService = Depends(get_ml_service)):
    revenue = service.predict_revenue(request)
    return RevenuePredictionResponse(predicted_revenue=revenue)