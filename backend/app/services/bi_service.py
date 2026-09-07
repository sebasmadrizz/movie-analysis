from app.repositories.bi_repository import BIRepository

class BIService:
    def __init__(self, repo: BIRepository):
        self.repo = repo

    def get_top_profitable_movies(self, limit: int) -> list[dict]:
        return self.repo.top_profitable_movies(limit)

    def get_genre_performance(self, limit: int) -> list[dict]:
            return self.repo.v_genre_performance(limit)

    def get_top_roi_movies(self, limit: int) -> list[dict]:
                return self.repo.v_top_roi_movies(limit)

    def get_top_directors(self, limit: int) -> list[dict]:
                return self.repo.v_top_directors(limit)

    def get_top_lead_actors(self, limit: int) -> list[dict]:
                    return self.repo.v_top_lead_actors(limit)

    def get_top_director_actor_duos(self, limit: int) -> list[dict]:
                    return self.repo.v_top_director_actor_duos(limit)

    def get_production_company_performance(self, limit: int) -> list[dict]:
                        return self.repo.v_production_company_performance(limit)

    def get_critical_vs_commercial_matrix(self, limit: int) -> list[dict]:
                            return self.repo.v_critical_vs_commercial_matrix(limit)

    def get_top_financial_flops(self, limit: int) -> list[dict]:
                                return self.repo.v_top_financial_flops(limit)
    
    def get_worst_performing_directors(self, limit: int) -> list[dict]:
                                        return self.repo.v_worst_performing_directors(limit)

    def get_lowest_roi_lead_actors(self, limit: int) -> list[dict]:
                                        return self.repo.v_lowest_roi_lead_actors(limit)
