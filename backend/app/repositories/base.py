from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def fetch_all(self, query: str, params: dict | None = None) -> list[dict]:
        ...