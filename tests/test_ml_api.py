from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_ml_service

client = TestClient(app)


class MockMLService:
    # Fake service that mimics MLService's interface without touching
    # the real model or the database.
    def predict_revenue(self, request):
        return {
            "predicted_revenue": 281279437.07,
            "director_is_debut": False,
            "cast_is_debut": False,
            "studio_is_debut": False,
        }


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
        "original_language_code": "en"
    }
    response = client.post("/api/v1/ml/predict-revenue", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_revenue" in data
    assert data["predicted_revenue"] > 0
    assert data["director_is_debut"] is False
    assert data["cast_is_debut"] is False
    assert data["studio_is_debut"] is False


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

def test_predict_revenue_rejects_zero_budget():
    # Budget must be > 0 — schema validation should reject it before the service runs
    payload = {
        "budget": 0,
        "runtime": 120,
        "genres": ["Action"],
        "release_date": "2024-06-15",
        "director_id": 488,
        "cast_ids": [380, 62, 2231],
        "studio_id": 6194,
        "is_sequel": 0,
        "original_language_code": "en",
    }
    response = client.post("/api/v1/ml/predict-revenue", json=payload)
    assert response.status_code == 422