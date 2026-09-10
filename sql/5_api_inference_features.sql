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
        COALESCE(ROUND(AVG(m.revenue)::NUMERIC, 2), 0) AS director_historical_avg_revenue,
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
        COALESCE(ROUND(AVG(m.revenue)::NUMERIC, 2), 0) AS top3_cast_historical_avg_revenue,
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
        COALESCE(ROUND(AVG(m.revenue)::NUMERIC, 2), 0) AS studio_historical_avg_revenue,
        CASE WHEN COUNT(DISTINCT m.movie_id) = 0 THEN 1 ELSE 0 END AS studio_is_debut
    FROM movie_production_companies mpc
    JOIN dim_movies m ON mpc.movie_id = m.movie_id
    WHERE mpc.company_id = target_company_id
      AND m.release_date < target_date
      AND m.revenue > 0;
END;
$$ LANGUAGE plpgsql;

