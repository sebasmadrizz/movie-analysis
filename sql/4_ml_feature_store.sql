DROP VIEW IF EXISTS v_ml_movie_features CASCADE;
CREATE OR REPLACE VIEW v_ml_movie_features AS
WITH global_avg_revenue AS (
    SELECT AVG(revenue) AS avg_rev FROM dim_movies WHERE revenue > 10000
),
director_metrics AS (
    SELECT 
        mc.movie_id,
        p.name AS director_name,
        AVG(m_past.revenue) OVER (
            PARTITION BY p.person_id 
            ORDER BY m_past.release_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
        ) AS director_historical_avg_revenue,
        COUNT(m_past.movie_id) OVER (
            PARTITION BY p.person_id 
            ORDER BY m_past.release_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
        ) AS director_prior_movies_count
    FROM movie_crew mc
    JOIN dim_people p ON mc.person_id = p.person_id
    JOIN dim_movies m_past ON mc.movie_id = m_past.movie_id
    WHERE mc.job = 'Director' AND m_past.revenue > 0
),
top3_cast_metrics AS (
    SELECT 
        mc.movie_id,
        AVG(m_past.revenue) OVER (
            PARTITION BY p.person_id 
            ORDER BY m_past.release_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
        ) AS actor_past_revenue,
        mc.cast_order
    FROM movie_cast mc
    JOIN dim_people p ON mc.person_id = p.person_id
    JOIN dim_movies m_past ON mc.movie_id = m_past.movie_id
    WHERE mc.cast_order <= 3 AND m_past.revenue > 0
),
top3_cast_agg AS (
    SELECT 
        movie_id,
        AVG(actor_past_revenue) AS top3_cast_historical_avg_revenue
    FROM top3_cast_metrics
    GROUP BY movie_id
),

movie_primary_studio AS (
    SELECT DISTINCT ON (mpc.movie_id)
        mpc.movie_id,
        mpc.company_id
    FROM movie_production_companies mpc
    ORDER BY mpc.movie_id, mpc.company_id
),
studio_metrics AS (
    SELECT 
        mps.movie_id,
        AVG(m_past.revenue) OVER (
            PARTITION BY mps.company_id 
            ORDER BY m_past.release_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
        ) AS studio_historical_avg_revenue,
        COUNT(m_past.movie_id) OVER (
            PARTITION BY mps.company_id 
            ORDER BY m_past.release_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
        ) AS studio_prior_movies_count
    FROM movie_primary_studio mps
    JOIN dim_movies m_past ON mps.movie_id = m_past.movie_id
    WHERE m_past.revenue > 0
),
sequel_flag AS (
    SELECT DISTINCT mk.movie_id, 1 AS is_sequel
    FROM movie_keywords mk
    JOIN dim_keywords k ON mk.keyword_id = k.keyword_id
    WHERE k.keyword_name = 'sequel'
),
movie_genres_agg AS (
    SELECT 
        mg.movie_id,
        STRING_AGG(g.genre_name, ', ' ORDER BY g.genre_name) AS genre_list,
        COUNT(g.genre_id) AS genre_count
    FROM movie_genres mg
    JOIN dim_genres g ON mg.genre_id = g.genre_id
    GROUP BY mg.movie_id
)
SELECT 
    m.movie_id,
    m.title,
    
    -- INPUT FEATURES (PRODUCTIONS & METADATA)
    m.budget,
    m.runtime,
    COALESCE(m.original_language_code, 'en') AS original_language_code,
    
    -- SEASONALITY
    EXTRACT(YEAR FROM m.release_date)::INT AS release_year,
    EXTRACT(MONTH FROM m.release_date)::INT AS release_month,
    EXTRACT(ISODOW FROM m.release_date)::INT AS release_day_of_week,
    
    -- CONTENT & TALENT ATTRIBUTES
    COALESCE(ga.genre_count, 0) AS genre_count,
    COALESCE(ga.genre_list, 'Unknown') AS genres,
    COALESCE(dm.director_name, 'Unknown') AS director_name,
    COALESCE(dm.director_prior_movies_count, 0) AS director_prior_movies_count,
   ROUND(COALESCE(dm.director_historical_avg_revenue, (SELECT avg_rev FROM global_avg_revenue)), 2) AS director_historical_avg_revenue,
ROUND(COALESCE(t3.top3_cast_historical_avg_revenue, (SELECT avg_rev FROM global_avg_revenue)), 2) AS top3_cast_historical_avg_revenue,
ROUND(COALESCE(sm.studio_historical_avg_revenue, (SELECT avg_rev FROM global_avg_revenue)), 2) AS studio_historical_avg_revenue,
CASE WHEN dm.director_historical_avg_revenue IS NULL THEN 1 ELSE 0 END AS director_is_debut,
CASE WHEN t3.top3_cast_historical_avg_revenue IS NULL THEN 1 ELSE 0 END AS cast_is_debut,
CASE WHEN sm.studio_historical_avg_revenue IS NULL THEN 1 ELSE 0 END AS studio_is_debut,
COALESCE(sm.studio_prior_movies_count, 0) AS studio_prior_movies_count,
COALESCE(sf.is_sequel, 0) AS is_sequel,
    
    -- TARGET VARIABLES (OBJECTIVES TO PREDICT)
    m.revenue AS target_revenue,
    ROUND(LN(NULLIF(m.revenue, 0))::NUMERIC, 4) AS target_log_revenue,
    CASE WHEN m.revenue > m.budget THEN 1 ELSE 0 END AS target_is_profitable,
    CASE WHEN m.revenue >= (m.budget * 2.5) THEN 1 ELSE 0 END AS target_is_blockbuster

FROM dim_movies m
LEFT JOIN movie_genres_agg ga ON m.movie_id = ga.movie_id
LEFT JOIN director_metrics dm ON m.movie_id = dm.movie_id
LEFT JOIN top3_cast_agg t3 ON m.movie_id = t3.movie_id
LEFT JOIN studio_metrics sm ON m.movie_id = sm.movie_id
LEFT JOIN sequel_flag sf ON m.movie_id = sf.movie_id
WHERE m.budget > 10000 
  AND m.revenue > 10000 
  AND m.release_date IS NOT NULL;