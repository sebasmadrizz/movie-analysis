DROP TABLE IF EXISTS raw_movies CASCADE;
CREATE TABLE raw_movies (
    budget BIGINT,
    genres TEXT,
    homepage TEXT,
    id INT PRIMARY KEY,
    keywords TEXT,
    original_language VARCHAR(10),
    original_title TEXT,
    overview TEXT,
    popularity NUMERIC(10, 4),
    production_companies TEXT,
    production_countries TEXT,
    release_date TEXT,
    revenue BIGINT,
    runtime NUMERIC(6, 2),
    spoken_languages TEXT,
    status VARCHAR(50),
    tagline TEXT,
    title TEXT,
    vote_average NUMERIC(4, 2),
    vote_count INT
);

DROP TABLE IF EXISTS raw_credits CASCADE;
CREATE TABLE raw_credits (
    movie_id INT,
    title TEXT,
    "cast" TEXT,
    crew TEXT
);