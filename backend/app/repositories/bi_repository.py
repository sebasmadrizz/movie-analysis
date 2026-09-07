from sqlalchemy import text
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository

class BIRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def fetch_all(self, query: str, params: dict | None = None) -> list[dict]:
        result = self.db.execute(text(query), params or {})
        return [dict(row._mapping) for row in result]

    def top_profitable_movies(self, limit: int = 10) -> list[dict]:
        return self.fetch_all(
            "SELECT * FROM v_top_profitable_movies LIMIT :limit",
            {"limit": limit},
        )


    def v_genre_performance(self, limit: int = 10) -> list[dict]:
            return self.fetch_all(
                "SELECT * FROM v_genre_performance LIMIT :limit",
                {"limit": limit},
            )


    def v_top_roi_movies(self, limit: int = 10) -> list[dict]:
            return self.fetch_all(
                "SELECT * FROM v_top_roi_movies LIMIT :limit",
                {"limit": limit},
            )

    def v_top_directors(self, limit: int = 10) -> list[dict]:
            return self.fetch_all(
                "SELECT * FROM v_top_directors LIMIT :limit",
                {"limit": limit},
            )

    def v_top_lead_actors(self, limit: int = 10) -> list[dict]:
                return self.fetch_all(
                    "SELECT * FROM v_top_lead_actors LIMIT :limit",
                    {"limit": limit},
                )

    def v_top_director_actor_duos(self, limit: int = 10) -> list[dict]:
                return self.fetch_all(
                    "SELECT * FROM v_top_director_actor_duos LIMIT :limit",
                    {"limit": limit},
                )

    def v_production_company_performance(self, limit: int = 10) -> list[dict]:
                    return self.fetch_all(
                        "SELECT * FROM v_production_company_performance LIMIT :limit",
                        {"limit": limit},
                    )

    def v_critical_vs_commercial_matrix(self, limit: int = 10) -> list[dict]:
                        return self.fetch_all(
                            "SELECT * FROM v_critical_vs_commercial_matrix LIMIT :limit",
                            {"limit": limit},
                        )

    def v_top_financial_flops(self, limit: int = 10) -> list[dict]:
                            return self.fetch_all(
                                "SELECT * FROM v_top_financial_flops LIMIT :limit",
                                {"limit": limit},
                            )

    def v_worst_performing_directors(self, limit: int = 10) -> list[dict]:
                                return self.fetch_all(
                                    "SELECT * FROM v_worst_performing_directors LIMIT :limit",
                                    {"limit": limit},
                                )

    def v_lowest_roi_lead_actors(self, limit: int = 10) -> list[dict]:
                                    return self.fetch_all(
                                        "SELECT * FROM v_lowest_roi_lead_actors LIMIT :limit",
                                        {"limit": limit},
                                    )