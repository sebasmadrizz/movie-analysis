from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_ml_service

client = TestClient(app)


class MockMLService:
    # Fake service that mimics MLService's interface without touching
    # the real model or the database.
    def predict_revenue(self, request):
        return 281279437.07


# Override the real get_ml_service dependency with the mock for all tests
# in this file — this is what makes the test fast and isolated.
app.dependency_overrides[get_ml_service] = lambda: MockMLService()


def test_predict_revenue():
    payload = {
        "budget": 100000000,
        "runtime": 120,
        "genres": ["Action", "Adventure"],
        "release_date": "2024-06-15",
        "director_id": 488,
        "cast_ids": [380, 62, 2231],
        "studio_id": 6194,
        "is_sequel": 0,
        "original_language_code": "en",
        "budget_vs_genre_historical_ratio": 1.2
    }
    response = client.post("/api/v1/ml/predict-revenue", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_revenue" in data
    assert data["predicted_revenue"] > 0


def test_predict_revenue_missing_field():
    # Intentionally incomplete payload to confirm Pydantic rejects it
    # before it ever reaches the service layer.
    payload = {
        "budget": 100000000,
        "runtime": 120,
        "genres": ["Action"],
    }
    response = client.post("/api/v1/ml/predict-revenue", json=payload)
    assert response.status_code == 422