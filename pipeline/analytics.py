import os
import sys
import logging
import psycopg2
from dotenv import load_dotenv

# Load environment variables from a .env file for local execution
load_dotenv()

# Configure logging format and severity level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Database connection parameters with local default fallbacks
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "movies_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

SQL_FILE_PATH = "sql/3_analytical_views.sql"

def execute_sql_file():
    """Reads and executes the analytical views SQL script in PostgreSQL."""
    if not os.path.exists(SQL_FILE_PATH):
        logging.error(f"The SQL file '{SQL_FILE_PATH}' was not found.")
        sys.exit(1)

    try:
        logging.info(f"Connecting to PostgreSQL database '{DB_NAME}' at {DB_HOST}:{DB_PORT}...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        logging.info(f"Reading SQL script: {SQL_FILE_PATH}...")
        with open(SQL_FILE_PATH, "r", encoding="utf-8") as file:
            sql_script = file.read()

        logging.info("Executing analytical views script (BI / EDA)...")
        cursor.execute(sql_script)
        conn.commit()

        # Validation: Retrieve all created views starting with 'v_' in the public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public' AND table_name LIKE 'v_%'
            ORDER BY table_name;
        """)
        created_views = cursor.fetchall()

        logging.info(f"Success! {len(created_views)} views created/updated in the database:")
        for view in created_views:
            logging.info(f"  - {view[0]}")

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error executing SQL script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    execute_sql_file()