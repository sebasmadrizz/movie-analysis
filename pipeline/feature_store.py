import os
import logging
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Configure logging format and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def run_feature_store_script():
    """Reads sql/04_ml_feature_store.sql and executes the creation

    of the v_ml_movie_features view in PostgreSQL.
    """
    load_dotenv()
    
    # Retrieve database credentials supporting both DB_* and POSTGRES_* environment variables
    db_name = os.getenv("DB_NAME") or os.getenv("POSTGRES_DB", "moviedb")
    db_user = os.getenv("DB_USER") or os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")

    # Resolve absolute path to the SQL file (checking both file naming formats)
    sql_file_path = Path(__file__).resolve().parent.parent / "sql" / "4_ml_feature_store.sql"

    logger.info(f"Loading SQL script from: {sql_file_path}")
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            logger.info("Executing Feature Store SQL script on PostgreSQL...")
            cursor.execute(sql_script)
            logger.info("View 'v_ml_movie_features' successfully created/updated.")
            
        conn.close()
    except Exception as e:
        logger.error(f"Failed to execute Feature Store script: {e}")
        raise

if __name__ == "__main__":
    run_feature_store_script()