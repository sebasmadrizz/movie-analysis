CREATE OR REPLACE FUNCTION get_director_inference_metrics(target_director_id INT, target_date DATE)
RETURNS TABLE (
    director_prior_movies_count INT,
    director_historical_avg_revenue NUMERIC,
    director_is_debut INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(DISTINCT m.movie_id)::INT AS director_prior_movies_count,
        COALESCE(ROUND(AVG(m.revenue)::NUMERIC, 2), (SELECT ROUND(AVG(g.revenue)::NUMERIC, 2) FROM dim_movies g WHERE g.revenue > 10000)) AS director_historical_avg_revenue,
        CASE WHEN COUNT(DISTINCT m.movie_id) = 0 THEN 1 ELSE 0 END AS director_is_debut
    FROM movie_crew mc
    JOIN dim_movies m ON mc.movie_id = m.movie_id
    WHERE mc.person_id = target_director_id
      AND mc.job = 'Director'
      AND m.release_date < target_date
      AND m.revenue > 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_cast_inference_metrics(target_cast_ids INT[], target_date DATE)
RETURNS TABLE (
    top3_cast_historical_avg_revenue NUMERIC,
    cast_is_debut INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COALESCE(ROUND(AVG(m.revenue)::NUMERIC, 2), (SELECT ROUND(AVG(g.revenue)::NUMERIC, 2) FROM dim_movies g WHERE g.revenue > 10000)) AS top3_cast_historical_avg_revenue,
        CASE WHEN COUNT(DISTINCT m.movie_id) = 0 THEN 1 ELSE 0 END AS cast_is_debut
    FROM movie_cast mc
    JOIN dim_movies m ON mc.movie_id = m.movie_id
    WHERE mc.person_id = ANY(target_cast_ids)
      AND mc.cast_order <= 3
      AND m.release_date < target_date
      AND m.revenue > 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_studio_inference_metrics(target_company_id INT, target_date DATE)
RETURNS TABLE (
    studio_prior_movies_count INT,
    studio_historical_avg_revenue NUMERIC,
    studio_is_debut INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(DISTINCT m.movie_id)::INT AS studio_prior_movies_count,
        COALESCE(ROUND(AVG(m.revenue)::NUMERIC, 2), (SELECT ROUND(AVG(g.revenue)::NUMERIC, 2) FROM dim_movies g WHERE g.revenue > 10000)) AS studio_historical_avg_revenue,
        CASE WHEN COUNT(DISTINCT m.movie_id) = 0 THEN 1 ELSE 0 END AS studio_is_debut
    FROM movie_production_companies mpc
    JOIN dim_movies m ON mpc.movie_id = m.movie_id
    WHERE mpc.company_id = target_company_id
      AND m.release_date < target_date
      AND m.revenue > 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_genre_budget_ratio(target_genres TEXT[], target_budget NUMERIC, target_date DATE)
RETURNS NUMERIC AS $$
DECLARE
    baseline NUMERIC;
BEGIN
    -- Average past budget per genre, then averaged across the movie's genres
    SELECT AVG(genre_avg) INTO baseline
    FROM (
        SELECT AVG(m.budget) AS genre_avg
        FROM dim_genres g
        JOIN movie_genres mg ON g.genre_id = mg.genre_id
        JOIN dim_movies m ON mg.movie_id = m.movie_id
        WHERE g.genre_name = ANY(target_genres)
          AND m.budget > 10000
          AND m.release_date < target_date
        GROUP BY g.genre_id
    ) t;

    -- Fallback to the global average budget, same as the feature store
    IF baseline IS NULL THEN
        SELECT AVG(budget) INTO baseline FROM dim_movies WHERE budget > 10000;
    END IF;

    RETURN ROUND((target_budget / baseline)::NUMERIC, 4);
END;
$$ LANGUAGE plpgsql;
