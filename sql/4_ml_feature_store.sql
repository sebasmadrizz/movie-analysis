
CREATE OR REPLACE VIEW v_ml_movie_features AS
WITH director_metrics AS (
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
    ROUND(COALESCE(dm.director_historical_avg_revenue, 0), 2) AS director_historical_avg_revenue,
    ROUND(COALESCE(t3.top3_cast_historical_avg_revenue, 0), 2) AS top3_cast_historical_avg_revenue,
    
    -- TARGET VARIABLES (OBJECTIVES TO PREDICT)
    m.revenue AS target_revenue,
    ROUND(LN(NULLIF(m.revenue, 0))::NUMERIC, 4) AS target_log_revenue,
    CASE WHEN m.revenue > m.budget THEN 1 ELSE 0 END AS target_is_profitable,
    CASE WHEN m.revenue >= (m.budget * 2.5) THEN 1 ELSE 0 END AS target_is_blockbuster

FROM dim_movies m
LEFT JOIN movie_genres_agg ga ON m.movie_id = ga.movie_id
LEFT JOIN director_metrics dm ON m.movie_id = dm.movie_id
LEFT JOIN top3_cast_agg t3 ON m.movie_id = t3.movie_id
WHERE m.budget > 0 
  AND m.revenue > 0 
  AND m.release_date IS NOT NULL;