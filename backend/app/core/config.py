from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "moviedb"

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()