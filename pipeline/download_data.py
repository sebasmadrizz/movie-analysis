import shutil
import kagglehub
from pathlib import Path
from dotenv import load_dotenv

#include .env file with KAGGLE_API_TOKEN
load_dotenv()

def download_tmdb_dataset():
    print("downloading tmdb dataset...")
    cache_path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")

    target_dir = Path("data/raw")
    target_dir.mkdir(parents=True, exist_ok=True)

    files_to_copy = ["tmdb_5000_movies.csv", "tmdb_5000_credits.csv"]

    for file_name in files_to_copy:
        source_file = Path(cache_path) / file_name
        destination_file = target_dir / file_name

        if source_file.exists():
            shutil.copy(source_file, destination_file)
            print(f" success: {destination_file}")
        else:
            print(f" File not found: {file_name}")

if __name__ == "__main__":
    download_tmdb_dataset()