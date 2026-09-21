# Movie Analysis: BI & ML Platform

A personal portfolio project that turns a raw dataset of 5,000 movies
into a full analytics platform — from SQL-based business intelligence
to a revenue prediction model served through a REST API.

## Why this project

Most "ML portfolio projects" jump straight to `model.fit()`. This one
doesn't. The interesting part of this project isn't the model itself —
it's what happens *before* the model ever sees the data.

Revenue in the movie industry is brutally skewed: a handful of
blockbusters earn billions while most films earn a fraction of that.
A naive model trained on raw budget/revenue numbers will overfit to
outliers and miss the signal entirely. So before any training
happened, most of the effort went into a SQL feature store designed
to reduce that dispersion and expose real, learnable signal:

- **Temporal leakage prevention**: historical averages (director,
  cast, studio) are computed with PostgreSQL window functions using
  `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING` — meaning each
  row only "knows" about movies released before it, never after.
- **Genre-relative budget normalization**: instead of comparing every
  movie's budget to a single global average, budgets are compared
  against the historical average *for that genre*, which is a more
  honest baseline.
- **Explicit cold-start handling**: first-time directors, actors, and
  studios don't get a missing value — they get a sensible global
  fallback *plus* a boolean flag (`is_debut`) so the model can treat
  uncertainty as a first-class signal, not noise.
- **Log-transformed target**: revenue is modeled in log-space to
  tame the extreme skew mentioned above.

The result is a Postgres view (`v_ml_movie_features`) that does most
of the real feature engineering work in SQL, before a single line of
Python touches the data.


## Data Pipeline

The project follows a staged, script-driven pipeline rather than
ad-hoc data wrangling: raw ingestion → staging → analytics
transformation → BI views → ML feature store → model training. Each
stage is a standalone Python script paired with its own SQL file
under `pipeline/` and `sql/`, and covered by its own test module
under `tests/` — so a failure in one stage can be caught without
needing the rest of the pipeline to run first.

The project is under active, continuous development — the pipeline
and test coverage grow alongside it.

## Architecture

The backend follows a layered architecture (router → service →
repository) designed around SOLID principles, particularly
Dependency Inversion — every layer depends on an abstraction it
receives via FastAPI's `Depends()`, not on a concrete implementation
it creates itself.
Request
  │
  ▼
Router (api/v1/*.py)        — HTTP only: parses input, returns response
  │
  ▼
Service (services/*.py)     — business logic: validation, orchestration
  │
  ▼
Repository (repositories/*.py) — the only layer that knows SQL exists
  │
  ▼
PostgreSQL
markdown
This separation means:
- **BI endpoints** are thin: each one queries a pre-aggregated SQL
  view, so heavy lifting (joins, `GROUP BY`, window functions)
  happens once in the database, not on every request.
- The **ML endpoint** resolves historical features (director, cast,
  studio track record) by calling PostgreSQL functions that mirror
  the same leakage-safe window function pattern used at training
  time — reused for live inference.
- Invalid input (e.g. a `director_id` that doesn't exist) is
  rejected with a `404` before any prediction is attempted, instead
  of silently defaulting to "debut" behavior.

The design leans on Dependency Inversion and Single Responsibility
in particular — every layer receives its dependencies through
FastAPI's `Depends()` rather than constructing them, and each class
has one clear reason to change. Other SOLID principles are applied
unevenly for now (e.g. `MLRepository` doesn't yet share a common
interface with `BIRepository`) — a known area for improvement as
the project evolves.

## How to Run It

### Prerequisites
- Python 3.11+
- Docker (for PostgreSQL)
- A Kaggle account with an API token (used to download the dataset)

### Setup

1. Clone the repo and create the environment:
```bash
   git clone https://github.com/sebasmadrizz/movie-analysis.git
   cd movie_analysis
   make venv
```

2. Create a `.env` file in the project root:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=moviedb
KAGGLE_API_TOKEN=your_kaggle_token


3. Start PostgreSQL:
```bash
   make db-up
```

### Run the pipeline

Each stage has its own command and test, and most are chained into a
single target so tests run right after their step:

```bash
make ingest                 # download + load raw data, then verify it
make transform-data         # build the analytics schema
make test-transformation

make analytics-all          # create BI views + run their tests
make ml-feature-store-all   # create the ML feature store view + tests
make train-model            # train the revenue model
make test-train-model
```

`models/revenue_model.joblib` is already committed to the repo, but
running `make train-model` regenerates it from scratch — recommended
so you see the full pipeline work end-to-end rather than relying on
a pre-baked artifact.

`make analyze-importance` is optional — it's an exploratory script
for inspecting feature importance, not required for the pipeline to
work.

### Run the API

```bash
make run-api
```

Then open `http://127.0.0.1:8000/docs` for interactive API docs.

Run the API's own test suites independently at any point:
```bash
make test-bi
make test-ml
```

### Stopping everything

```bash
make db-down     # stop and remove the database container
make clean        # remove .venv and Python cache files
```

## API Endpoints
 
Full interactive documentation (with request/response schemas and a
"try it out" button) is available at `/docs` once the API is
running. Below is a summary.
 
### BI Endpoints (`/api/v1/bi`)
 
All BI endpoints are `GET` requests that query a pre-aggregated SQL
view, with an optional `limit` query parameter (default: 10).
 
| Endpoint | Returns |
|---|---|
| `/top-profitable-movies` | Movies ranked by net profit (revenue - budget) |
| `/top-roi-movies` | Movies ranked by return on investment |
| `/genre-performance` | Aggregated budget, revenue, and ROI by genre |
| `/top-directors` | Directors ranked by total box office |
| `/top-lead-actors` | Lead actors (top 3 billing) ranked by box office |
| `/director-actor-duos` | Director/actor pairs with 2+ collaborations, ranked by box office |
| `/production-company-performance` | Studios ranked by revenue, with market share |
| `/critical-vs-commercial-matrix` | Movies classified by critical rating vs. commercial performance |
| `/top-financial-flops` | Movies with the largest real financial losses |
| `/worst-performing-directors` | Directors ranked by lowest average ROI |
| `/lowest-roi-lead-actors` | Lead actors ranked by lowest average ROI |
 
Example:
```bash
curl "http://127.0.0.1:8000/api/v1/bi/top-profitable-movies?limit=5"
```
 
### ML Endpoint (`/api/v1/ml`)
 
`POST /predict-revenue` — predicts a movie's revenue given its
budget, genres, release date, and the IDs of its director, top-3
cast, and production studio. Historical performance for those
IDs (prior movies, average revenue, debut status) is resolved
automatically from the database — not supplied by the caller.
 
Example request:
```json
{
  "budget": 100000000,
  "runtime": 120,
  "genres": ["Action", "Adventure"],
  "release_date": "2024-06-15",
  "director_id": 488,
  "cast_ids": [380, 62, 2231],
  "studio_id": 6194,
  "is_sequel": 0,
  "original_language_code": "en",
  "budget_vs_genre_historical_ratio": 1.2
}
```
 
Example response:
```json
{
  "predicted_revenue": 281279437.07
}
```
 
Returns `404` if `director_id`, any `cast_ids`, or `studio_id` do not
exist in the database.
 