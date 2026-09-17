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