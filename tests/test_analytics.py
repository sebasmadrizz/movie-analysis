import os
import pytest
import psycopg2
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "movies_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )
    yield conn
    conn.close()

EXPECTED_VIEWS = [
    "v_top_profitable_movies",
    "v_top_roi_movies",
    "v_genre_performance",
    "v_top_directors",
    "v_top_lead_actors",
    "v_top_director_actor_duos",
    "v_production_company_performance",
    "v_critical_vs_commercial_matrix",
    "v_top_financial_flops",
    "v_worst_performing_directors",
    "v_lowest_roi_lead_actors"
]

@pytest.mark.parametrize("view_name", EXPECTED_VIEWS)
def test_analytical_views_exist_and_queryable(db_connection, view_name):
    """Validates that each analytical view exists in PostgreSQL and returns data without errors."""
    cursor = db_connection.cursor()
    query = f"SELECT * FROM {view_name} LIMIT 1;"
    
    try:
        cursor.execute(query)
        cursor.fetchone()
        assert True
    except Exception as e:
        pytest.fail(f"Querying view '{view_name}' failed with error: {e}")
    finally:
        cursor.close()