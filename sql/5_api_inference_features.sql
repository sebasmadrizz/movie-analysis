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