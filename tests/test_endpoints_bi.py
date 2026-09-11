from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_bi_service

client = TestClient(app)

class MockBIService:
    def get_top_profitable_movies(self, limit: int):
        return [{
            "movie_id": 1,
            "title": "Test Movie",
            "release_date": "2023-01-01",
            "budget": 50000000.0,
            "revenue": 200000000.0,
            "net_profit": 150000000.0,
            "roi": 3.0
        }]
    
    def get_genre_performance(self, limit: int):
        return [{
            "genre_name": "Action",
            "total_movies": 45,
            "total_budget": 2000000000.0,
            "total_revenue": 9000000000.0,
            "total_profit": 7000000000.0,
            "avg_roi": 3.5,
            "avg_revenue": 200000000.0
        }]
    
    def get_top_roi_movies(self, limit: int):
        return [{
            "movie_id": 1,
            "title": "Test Movie",
            "release_date": "2023-01-01",
            "budget": 50000000.0,
            "revenue": 200000000.0,
            "net_profit": 150000000.0,
            "roi": 3.0
        }]

    def get_top_directors(self, limit: int):
        return [{
            "person_id": 10,
            "director_name": "Christopher Nolan",
            "total_movies_directed": 10,
            "total_box_office": 5000000000.0,
            "total_profit": 3000000000.0,
            "avg_revenue": 500000000.0
        }]

    def get_top_lead_actors(self, limit: int):
        return [{
            "person_id": 20,
            "actor_name": "Tom Cruise",
            "lead_roles_count": 15,
            "total_box_office": 7000000000.0,
            "avg_box_office_per_movie": 466666666.67,
            "avg_revenue": 500000000.0
        }]

    def get_top_director_actor_duos(self, limit: int):
        return [{"director_name": "Director X", "actor_name": "Actor Y", "collaboration_count": 3}]

    def get_production_company_performance(self, limit: int):
        return [{"company_id": 100, "company_name": "Warner Bros", "total_movies": 120}]

    def get_critical_vs_commercial_matrix(self, limit: int):
        return [{"movie_id": 1, "title": "Matrix Test", "vote_average": 8.1, "revenue": 300000000}]

    def get_top_financial_flops(self, limit: int):
        return [{
            "movie_id": 99,
            "title": "Flop Movie",
            "release_date": "2023-01-01",
            "budget": 100000000.0,
            "revenue": 50000000.0,
            "net_loss": -50000000.0,
            "roi": 0.5
        }]

    def get_worst_performing_directors(self, limit: int):
        return [{"person_id": 50, "name": "Bad Director", "avg_revenue": 10000.00}]

    def get_lowest_roi_lead_actors(self, limit: int):
        return [{"person_id": 60, "name": "Unprofitable Actor", "avg_roi": 0.2}]

app.dependency_overrides[get_bi_service] = lambda: MockBIService()


def test_top_profitable_movies():
    response = client.get("/api/v1/bi/top-profitable-movies?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["title"] == "Test Movie"
    assert data[0]["net_profit"] == 150000000.0


def test_genre_performance():
    response = client.get("/api/v1/bi/genre-performance?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["genre_name"] == "Action"


def test_top_financial_flops():
    response = client.get("/api/v1/bi/top-financial-flops?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["net_loss"] == -50000000.0


def test_top_directors():
    response = client.get("/api/v1/bi/top-directors?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["director_name"] == "Christopher Nolan"


def test_top_lead_actors():
    response = client.get("/api/v1/bi/top-lead-actors?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["actor_name"] == "Tom Cruise"