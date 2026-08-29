import os
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="module")
def db_connection():
    """Pytest fixture to establish and close PostgreSQL connection."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME") or os.getenv("POSTGRES_DB", "moviedb"),
        user=os.getenv("DB_USER") or os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    yield conn
    conn.close()

def test_feature_store_view_exists_and_returns_data(db_connection):
    """Verify that v_ml_movie_features exists and contains records."""
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM v_ml_movie_features;")
        count = cursor.fetchone()[0]
        assert count > 0, "Feature store view v_ml_movie_features is empty."

def test_feature_store_schema_columns(db_connection):
    """Verify that mandatory feature and target columns exist in the view."""
    expected_columns = {
        "movie_id", "title", "budget", "runtime", "original_language_code",
        "release_year", "release_month", "release_day_of_week",
        "genre_count", "genres", "director_name", "director_prior_movies_count",
        "director_historical_avg_revenue", "top3_cast_historical_avg_revenue",
        "target_revenue", "target_log_revenue", "target_is_profitable", "target_is_blockbuster"
    }
    with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM v_ml_movie_features LIMIT 1;")
        row = cursor.fetchone()
        assert row is not None, "No record returned from v_ml_movie_features."
        actual_columns = set(row.keys())
        assert expected_columns.issubset(actual_columns), f"Missing columns: {expected_columns - actual_columns}"

def test_feature_store_target_integrity(db_connection):
    """Validate data integrity for target variables and filtering rules."""
    with db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT budget, target_revenue, target_is_profitable, target_is_blockbuster "
            "FROM v_ml_movie_features LIMIT 100;"
        )
        rows = cursor.fetchall()
        for row in rows:
            assert row["target_is_profitable"] in (0, 1), "target_is_profitable must be binary (0 or 1)."
            assert row["target_is_blockbuster"] in (0, 1), "target_is_blockbuster must be binary (0 or 1)."
            assert row["budget"] > 0, "Budget feature must be greater than zero."
            assert row["target_revenue"] > 0, "Target revenue must be greater than zero."