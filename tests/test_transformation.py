import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "movie_analysis")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


@pytest.fixture(scope="module")
def db_engine():
    """Provides a SQLAlchemy database engine fixture for transformation tests."""
    engine = create_engine(DATABASE_URL)
    yield engine
    engine.dispose()


def test_dim_movies_count_matches_staging(db_engine):
    """Verify dim_movies matches exact record count from raw_movies staging table."""
    with db_engine.connect() as conn:
        staging_count = conn.execute(text("SELECT COUNT(*) FROM raw_movies")).scalar()
        dim_count = conn.execute(text("SELECT COUNT(*) FROM dim_movies")).scalar()
        assert dim_count == 4803, f"Expected 4803 movies, got {dim_count}"
        assert dim_count == staging_count, "Mismatch between raw_movies and dim_movies count!"


def test_dimensions_not_empty(db_engine):
    """Ensure all core dimension tables contain populated catalog data."""
    dimensions = [
        "dim_genres",
        "dim_keywords",
        "dim_companies",
        "dim_countries",
        "dim_languages",
        "dim_people",
    ]
    with db_engine.connect() as conn:
        for dim in dimensions:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {dim}")).scalar()
            assert count > 0, f"Dimension table '{dim}' is unexpectedly empty!"


def test_no_orphan_bridge_records(db_engine):
    """Check for foreign key integrity across all bridge/junction tables."""
    bridges = [
        ("movie_genres", "movie_id", "dim_movies"),
        ("movie_keywords", "movie_id", "dim_movies"),
        ("movie_production_companies", "company_id", "dim_companies"),
        ("movie_cast", "person_id", "dim_people"),
        ("movie_crew", "person_id", "dim_people"),
    ]
    with db_engine.connect() as conn:
        for bridge, fk_column, target_table in bridges:
            orphan_query = text(f"""
                SELECT COUNT(*) 
                FROM {bridge} b
                LEFT JOIN {target_table} t ON b.{fk_column} = t.{fk_column}
                WHERE t.{fk_column} IS NULL
            """)
            orphans = conn.execute(orphan_query).scalar()
            assert orphans == 0, f"Found {orphans} orphan records in '{bridge}' referencing '{target_table}'!"