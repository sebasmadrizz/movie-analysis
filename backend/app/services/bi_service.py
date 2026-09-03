from app.repositories.bi_repository import BIRepository

class BIService:
    def __init__(self, repo: BIRepository):
        self.repo = repo

    def get_top_profitable_movies(self, limit: int) -> list[dict]:
        return self.repo.top_profitable_movies(limit)