-- ============================================================================
-- SQL Script: 02_create_analytics_tables.sql
-- Description: Analytics schema DDL, JSON parsing transformation, and FK indexes
-- ============================================================================

-- 1. CLEANUP PREVIOUS TABLES (IDEMPOTENCY)
DROP TABLE IF EXISTS movie_crew CASCADE;
DROP TABLE IF EXISTS movie_cast CASCADE;
DROP TABLE IF EXISTS movie_spoken_languages CASCADE;
DROP TABLE IF EXISTS movie_production_countries CASCADE;
DROP TABLE IF EXISTS movie_production_companies CASCADE;
DROP TABLE IF EXISTS movie_keywords CASCADE;
DROP TABLE IF EXISTS movie_genres CASCADE;

DROP TABLE IF EXISTS dim_people CASCADE;
DROP TABLE IF EXISTS dim_languages CASCADE;
DROP TABLE IF EXISTS dim_countries CASCADE;
DROP TABLE IF EXISTS dim_companies CASCADE;
DROP TABLE IF EXISTS dim_keywords CASCADE;
DROP TABLE IF EXISTS dim_genres CASCADE;
DROP TABLE IF EXISTS dim_movies CASCADE;

-- 2. DDL: DIMENSIONAL TABLES
CREATE TABLE dim_languages (
    language_code VARCHAR(10) PRIMARY KEY,
    language_name TEXT NOT NULL
);

CREATE TABLE dim_countries (
    country_code VARCHAR(10) PRIMARY KEY,
    country_name TEXT NOT NULL
);

CREATE TABLE dim_movies (
    movie_id INT PRIMARY KEY,
    title TEXT NOT NULL,
    original_title TEXT,
    budget BIGINT,
    revenue BIGINT,
    release_date DATE,
    runtime NUMERIC(6, 2),
    popularity NUMERIC(10, 4),
    vote_average NUMERIC(4, 2),
    vote_count INT,
    status VARCHAR(50),
    homepage TEXT,
    tagline TEXT,
    overview TEXT,
    original_language_code VARCHAR(10) REFERENCES dim_languages(language_code)
);

CREATE TABLE dim_genres (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);

CREATE TABLE dim_keywords (
    keyword_id INT PRIMARY KEY,
    keyword_name TEXT NOT NULL
);

CREATE TABLE dim_companies (
    company_id INT PRIMARY KEY,
    company_name TEXT NOT NULL
);

CREATE TABLE dim_people (
    person_id INT PRIMARY KEY,
    name TEXT NOT NULL
);

-- 3. DDL: JUNCTION / BRIDGE TABLES
CREATE TABLE movie_genres (
    movie_id INT REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    genre_id INT REFERENCES dim_genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE movie_keywords (
    movie_id INT REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    keyword_id INT REFERENCES dim_keywords(keyword_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, keyword_id)
);

CREATE TABLE movie_production_companies (
    movie_id INT REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    company_id INT REFERENCES dim_companies(company_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, company_id)
);

CREATE TABLE movie_production_countries (
    movie_id INT REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    country_code VARCHAR(10) REFERENCES dim_countries(country_code) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, country_code)
);

CREATE TABLE movie_spoken_languages (
    movie_id INT REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    language_code VARCHAR(10) REFERENCES dim_languages(language_code) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, language_code)
);

CREATE TABLE movie_cast (
    movie_id INT REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    person_id INT REFERENCES dim_people(person_id) ON DELETE CASCADE,
    character_name TEXT NOT NULL DEFAULT '',
    cast_order INT NOT NULL DEFAULT 0,
    PRIMARY KEY (movie_id, person_id, cast_order, character_name)
);

CREATE TABLE movie_crew (
    movie_id INT REFERENCES dim_movies(movie_id) ON DELETE CASCADE,
    person_id INT REFERENCES dim_people(person_id) ON DELETE CASCADE,
    department TEXT NOT NULL,
    job TEXT NOT NULL,
    PRIMARY KEY (movie_id, person_id, department, job)
);

-- 4. DML: POPULATE TABLES BY PARSING JSON FROM STAGING

-- A. Languages (Dimension)
INSERT INTO dim_languages (language_code, language_name)
SELECT DISTINCT
    l->>'iso_639_1' AS language_code,
    COALESCE(NULLIF(l->>'name', ''), l->>'iso_639_1') AS language_name
FROM raw_movies,
LATERAL json_array_elements(NULLIF(spoken_languages, '')::json) AS l
WHERE l->>'iso_639_1' IS NOT NULL AND l->>'iso_639_1' != ''
ON CONFLICT (language_code) DO NOTHING;

INSERT INTO dim_languages (language_code, language_name)
SELECT DISTINCT original_language, original_language
FROM raw_movies
WHERE original_language IS NOT NULL AND original_language != ''
ON CONFLICT (language_code) DO NOTHING;

-- B. Movies (Core Dimension)
INSERT INTO dim_movies (
    movie_id, title, original_title, budget, revenue, release_date,
    runtime, popularity, vote_average, vote_count, status,
    homepage, tagline, overview, original_language_code
)
SELECT
    id AS movie_id,
    title,
    original_title,
    budget,
    revenue,
    NULLIF(release_date, '')::DATE,
    runtime,
    popularity,
    vote_average,
    vote_count,
    status,
    homepage,
    tagline,
    overview,
    original_language AS original_language_code
FROM raw_movies;

-- C. Genres & Movie-Genres Junction
INSERT INTO dim_genres (genre_id, genre_name)
SELECT DISTINCT
    (g->>'id')::INT AS genre_id,
    g->>'name' AS genre_name
FROM raw_movies,
LATERAL json_array_elements(NULLIF(genres, '')::json) AS g
ON CONFLICT (genre_id) DO NOTHING;

INSERT INTO movie_genres (movie_id, genre_id)
SELECT DISTINCT
    id AS movie_id,
    (g->>'id')::INT AS genre_id
FROM raw_movies,
LATERAL json_array_elements(NULLIF(genres, '')::json) AS g
ON CONFLICT DO NOTHING;

-- D. Keywords & Movie-Keywords Junction
INSERT INTO dim_keywords (keyword_id, keyword_name)
SELECT DISTINCT
    (k->>'id')::INT AS keyword_id,
    k->>'name' AS keyword_name
FROM raw_movies,
LATERAL json_array_elements(NULLIF(keywords, '')::json) AS k
ON CONFLICT (keyword_id) DO NOTHING;

INSERT INTO movie_keywords (movie_id, keyword_id)
SELECT DISTINCT
    id AS movie_id,
    (k->>'id')::INT AS keyword_id
FROM raw_movies,
LATERAL json_array_elements(NULLIF(keywords, '')::json) AS k
ON CONFLICT DO NOTHING;

-- E. Production Companies & Junction
INSERT INTO dim_companies (company_id, company_name)
SELECT DISTINCT
    (c->>'id')::INT AS company_id,
    c->>'name' AS company_name
FROM raw_movies,
LATERAL json_array_elements(NULLIF(production_companies, '')::json) AS c
ON CONFLICT (company_id) DO NOTHING;

INSERT INTO movie_production_companies (movie_id, company_id)
SELECT DISTINCT
    id AS movie_id,
    (c->>'id')::INT AS company_id
FROM raw_movies,
LATERAL json_array_elements(NULLIF(production_companies, '')::json) AS c
ON CONFLICT DO NOTHING;

-- F. Production Countries & Junction
INSERT INTO dim_countries (country_code, country_name)
SELECT DISTINCT
    c->>'iso_3166_1' AS country_code,
    c->>'name' AS country_name
FROM raw_movies,
LATERAL json_array_elements(NULLIF(production_countries, '')::json) AS c
WHERE c->>'iso_3166_1' IS NOT NULL AND c->>'iso_3166_1' != ''
ON CONFLICT (country_code) DO NOTHING;

INSERT INTO movie_production_countries (movie_id, country_code)
SELECT DISTINCT
    id AS movie_id,
    c->>'iso_3166_1' AS country_code
FROM raw_movies,
LATERAL json_array_elements(NULLIF(production_countries, '')::json) AS c
WHERE c->>'iso_3166_1' IS NOT NULL AND c->>'iso_3166_1' != ''
ON CONFLICT DO NOTHING;

-- G. Spoken Languages Junction
INSERT INTO movie_spoken_languages (movie_id, language_code)
SELECT DISTINCT
    id AS movie_id,
    l->>'iso_639_1' AS language_code
FROM raw_movies,
LATERAL json_array_elements(NULLIF(spoken_languages, '')::json) AS l
WHERE l->>'iso_639_1' IS NOT NULL AND l->>'iso_639_1' != ''
ON CONFLICT DO NOTHING;

-- H. People Dimension (Union of Cast and Crew)
INSERT INTO dim_people (person_id, name)
SELECT DISTINCT
    (p->>'id')::INT AS person_id,
    p->>'name' AS name
FROM (
    SELECT json_array_elements(NULLIF("cast", '')::json) AS p FROM raw_credits
    UNION ALL
    SELECT json_array_elements(NULLIF(crew, '')::json) AS p FROM raw_credits
) combined
WHERE p->>'id' IS NOT NULL
ON CONFLICT (person_id) DO NOTHING;

-- I. Movie Cast Junction
INSERT INTO movie_cast (movie_id, person_id, character_name, cast_order)
SELECT DISTINCT
    movie_id,
    (c->>'id')::INT AS person_id,
    COALESCE(c->>'character', '') AS character_name,
    COALESCE((c->>'order')::INT, 0) AS cast_order
FROM raw_credits,
LATERAL json_array_elements(NULLIF("cast", '')::json) AS c
ON CONFLICT DO NOTHING;

-- J. Movie Crew Junction
INSERT INTO movie_crew (movie_id, person_id, department, job)
SELECT DISTINCT
    movie_id,
    (c->>'id')::INT AS person_id,
    c->>'department' AS department,
    c->>'job' AS job
FROM raw_credits,
LATERAL json_array_elements(NULLIF(crew, '')::json) AS c
ON CONFLICT DO NOTHING;

-- 5. PERFORMANCE INDEXES ON BRIDGE TABLES (FOREIGN KEYS)
CREATE INDEX idx_movie_genres_genre ON movie_genres(genre_id);
CREATE INDEX idx_movie_keywords_keyword ON movie_keywords(keyword_id);
CREATE INDEX idx_movie_companies_company ON movie_production_companies(company_id);
CREATE INDEX idx_movie_countries_country ON movie_production_countries(country_code);
CREATE INDEX idx_movie_spoken_languages_lang ON movie_spoken_languages(language_code);
CREATE INDEX idx_movie_cast_person ON movie_cast(person_id);
CREATE INDEX idx_movie_crew_person ON movie_crew(person_id);