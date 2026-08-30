import os
import numpy as np
import logging
from pathlib import Path
import joblib
import pandas as pd
import psycopg2
from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def load_feature_data() -> pd.DataFrame:
    """Connects to PostgreSQL and retrieves records from v_ml_movie_features."""
    load_dotenv()

    db_name = os.getenv("DB_NAME") or os.getenv("POSTGRES_DB", "moviedb")
    db_user = os.getenv("DB_USER") or os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")

    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    
    query = "SELECT * FROM v_ml_movie_features;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def build_genre_dummies(df: pd.DataFrame) -> tuple[pd.DataFrame, MultiLabelBinarizer]:
    """Converts the 'genres' column (string 'Action, Adventure') into multi-label dummies.

    Returns both the dummy DataFrame and the fitted MultiLabelBinarizer,
    so the binarizer can be persisted alongside the model for future inference.
    """
    genre_lists = df["genres"].apply(
        lambda x: [g.strip() for g in x.split(",")] if x != "Unknown" else []
    )
    mlb = MultiLabelBinarizer()
    genre_dummies = pd.DataFrame(
        mlb.fit_transform(genre_lists),
        columns=[f"genre_{g}" for g in mlb.classes_],
        index=df.index
    )
    return genre_dummies, mlb


def train_revenue_model():
    """Preprocesses features, trains a Random Forest model,

    evaluates performance metrics, and serializes the trained model pipeline artifact.
    """
    logger.info("Loading feature dataset from v_ml_movie_features...")
    df = load_feature_data()

    if df.empty:
        raise ValueError("No feature data found in v_ml_movie_features.")

    logger.info(f"Loaded {len(df)} records for training.")

    df["budget_log"] = np.log1p(df["budget"])

    genre_dummies, mlb = build_genre_dummies(df)
    df = pd.concat([df, genre_dummies], axis=1)

    num_features = [
    "budget_log", "runtime", "release_year", "release_month",
    "release_day_of_week", "genre_count",
    "director_prior_movies_count", "director_historical_avg_revenue",
    "top3_cast_historical_avg_revenue",
    "studio_historical_avg_revenue", "studio_prior_movies_count",
    "is_sequel"
] + list(genre_dummies.columns)
    cat_features = ["original_language_code"]
    target_col = "target_log_revenue"

    X = df[num_features + cat_features]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
        ]
    )

    model_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", HistGradientBoostingRegressor(
    max_iter=300,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
))
    ])

    logger.info("Training HistGradientBoostingRegressor pipeline...")
    model_pipeline.fit(X_train, y_train)

    predictions = model_pipeline.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    logger.info("=== Model Performance Metrics ===")
    logger.info(f"RMSE (Log Scale): {rmse:.4f}")
    logger.info(f"MAE  (Log Scale): {mae:.4f}")
    logger.info(f"R^2 Score       : {r2:.4f}")

    models_dir = Path(__file__).resolve().parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    model_path = models_dir / "revenue_model.joblib"

    joblib.dump({"model": model_pipeline, "mlb": mlb}, model_path)
    logger.info(f"Model artifact successfully saved to: {model_path}")

    return model_pipeline, {"rmse": rmse, "mae": mae, "r2": r2}

if __name__ == "__main__":
    train_revenue_model()