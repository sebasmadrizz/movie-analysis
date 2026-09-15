from datetime import date
from sqlalchemy import text
from sqlalchemy.orm import Session


class MLRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_director_metrics(self, director_id: int, target_date: date) -> dict:
        result = self.db.execute(
            text("SELECT * FROM get_director_inference_metrics(:director_id, :target_date)"),
            {"director_id": director_id, "target_date": target_date},
        )
        return dict(result.mappings().one())

    def get_cast_metrics(self, cast_ids: list[int], target_date: date) -> dict:
        result = self.db.execute(
            text("SELECT * FROM get_cast_inference_metrics(:cast_ids, :target_date)"),
            {"cast_ids": cast_ids, "target_date": target_date},
        )
        return dict(result.mappings().one())

    def get_studio_metrics(self, company_id: int, target_date: date) -> dict:
        result = self.db.execute(
            text("SELECT * FROM get_studio_inference_metrics(:company_id, :target_date)"),
            {"company_id": company_id, "target_date": target_date},
        )
        return dict(result.mappings().one())

    def person_exists(self, person_id: int) -> bool:
        result = self.db.execute(
            text("SELECT 1 FROM dim_people WHERE person_id = :person_id"),
            {"person_id": person_id},
        )
        return result.first() is not None

    def company_exists(self, company_id: int) -> bool:
        result = self.db.execute(
            text("SELECT 1 FROM dim_companies WHERE company_id = :company_id"),
            {"company_id": company_id},
        )
        return result.first() is not None