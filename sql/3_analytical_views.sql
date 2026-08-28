CREATE OR REPLACE VIEW v_top_profitable_movies AS
SELECT 
    movie_id,
    title,
    release_date,
    budget,
    revenue,
    (revenue - budget) AS net_profit,
    ROUND((revenue::NUMERIC / NULLIF(budget, 0)), 2) AS roi
FROM dim_movies
WHERE budget > 0 AND revenue > 0
ORDER BY net_profit DESC;

-- ----------------------------------------------------------------------------
-- 2. TOP MOVIES BY ROI (>= $100k BUDGET)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_top_roi_movies AS
SELECT 
    movie_id,
    title,
    release_date,
    budget,
    revenue,
    (revenue - budget) AS net_profit,
    ROUND((revenue::NUMERIC / NULLIF(budget, 0)), 2) AS roi
FROM dim_movies
WHERE budget >= 100000 AND revenue > 0
ORDER BY roi DESC;

-- ----------------------------------------------------------------------------
-- 3. GENRE PERFORMANCE METRICS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_genre_performance AS
SELECT 
    g.genre_name,
    COUNT(DISTINCT m.movie_id) AS total_movies,
    SUM(m.budget) AS total_budget,
    SUM(m.revenue) AS total_revenue,
    SUM(m.revenue - m.budget) AS total_profit,
    ROUND(AVG(m.revenue::NUMERIC / NULLIF(m.budget, 0)), 2) AS avg_roi
FROM dim_genres g
JOIN movie_genres mg ON g.genre_id = mg.genre_id
JOIN dim_movies m ON mg.movie_id = m.movie_id
WHERE m.budget > 0 AND m.revenue > 0
GROUP BY g.genre_name
ORDER BY total_profit DESC;

-- ----------------------------------------------------------------------------
-- 4. TOP GROSSING DIRECTORS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_top_directors AS
SELECT 
    p.person_id,
    p.name AS director_name,
    COUNT(DISTINCT m.movie_id) AS total_movies_directed,
    SUM(m.revenue) AS total_box_office,
    SUM(m.revenue - m.budget) AS total_profit
FROM dim_people p
JOIN movie_crew mc ON p.person_id = mc.person_id
JOIN dim_movies m ON mc.movie_id = m.movie_id
WHERE mc.job = 'Director' 
  AND m.budget > 0 
  AND m.revenue > 0
GROUP BY p.person_id, p.name
ORDER BY total_box_office DESC;

-- ----------------------------------------------------------------------------
-- 5. TOP BANKABLE LEAD ACTORS (Top 3 Cast Order, Min 3 Movies)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_top_lead_actors AS
SELECT 
    p.person_id,
    p.name AS actor_name,
    COUNT(DISTINCT m.movie_id) AS lead_roles_count,
    SUM(m.revenue) AS total_box_office,
    ROUND(AVG(m.revenue), 2) AS avg_box_office_per_movie
FROM dim_people p
JOIN movie_cast mc ON p.person_id = mc.person_id
JOIN dim_movies m ON mc.movie_id = m.movie_id
WHERE mc.cast_order <= 3 
  AND m.budget > 0 
  AND m.revenue > 0
GROUP BY p.person_id, p.name
HAVING COUNT(DISTINCT m.movie_id) >= 3
ORDER BY total_box_office DESC;

-- ----------------------------------------------------------------------------
-- 6. DIRECTOR & ACTOR SYNERGY (DUOS)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_top_director_actor_duos AS
SELECT 
    p_dir.name AS director_name,
    p_act.name AS actor_name,
    COUNT(DISTINCT m.movie_id) AS collaborations,
    SUM(m.revenue) AS total_box_office,
    ROUND(AVG(m.revenue::NUMERIC / NULLIF(m.budget, 0)), 2) AS avg_roi
FROM dim_movies m
JOIN movie_crew mc ON m.movie_id = mc.movie_id AND mc.job = 'Director'
JOIN dim_people p_dir ON mc.person_id = p_dir.person_id
JOIN movie_cast ma ON m.movie_id = ma.movie_id AND ma.cast_order <= 3
JOIN dim_people p_act ON ma.person_id = p_act.person_id
WHERE m.budget > 0 
  AND m.revenue > 0 
  AND p_dir.person_id != p_act.person_id
GROUP BY p_dir.person_id, p_dir.name, p_act.person_id, p_act.name
HAVING COUNT(DISTINCT m.movie_id) >= 2
ORDER BY total_box_office DESC;

-- ----------------------------------------------------------------------------
-- 7. PRODUCTION COMPANY MARKET SHARE
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_production_company_performance AS
WITH company_totals AS (
    SELECT 
        c.company_id,
        c.company_name,
        COUNT(DISTINCT m.movie_id) AS movies_produced,
        SUM(m.budget) AS total_budget,
        SUM(m.revenue) AS total_revenue,
        SUM(m.revenue - m.budget) AS total_profit
    FROM dim_companies c
    JOIN movie_production_companies mpc ON c.company_id = mpc.company_id
    JOIN dim_movies m ON mpc.movie_id = m.movie_id
    WHERE m.budget > 0 AND m.revenue > 0
    GROUP BY c.company_id, c.company_name
)
SELECT 
    company_id,
    company_name,
    movies_produced,
    total_budget,
    total_revenue,
    total_profit,
    ROUND((total_revenue / NULLIF(SUM(total_revenue) OVER(), 0)) * 100, 2) AS market_share_pct
FROM company_totals
WHERE movies_produced >= 3
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- 8. CRITICAL VS. COMMERCIAL MATRIX
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_critical_vs_commercial_matrix AS
SELECT 
    movie_id,
    title,
    vote_average,
    vote_count,
    ROUND((revenue::NUMERIC / NULLIF(budget, 0)), 2) AS roi,
    CASE 
        WHEN vote_average >= 7.0 AND (revenue::NUMERIC / NULLIF(budget, 0)) >= 2.0 THEN 'Blockbuster & Critical Acclaim'
        WHEN vote_average < 7.0 AND (revenue::NUMERIC / NULLIF(budget, 0)) >= 2.0 THEN 'Commercial Hit (Low Rating)'
        WHEN vote_average >= 7.0 AND (revenue::NUMERIC / NULLIF(budget, 0)) < 2.0 THEN 'Cult Classic / Critical Darling'
        ELSE 'Commercial & Critical Flop'
    END AS performance_segment
FROM dim_movies
WHERE budget >= 100000 AND revenue > 0 AND vote_count >= 50;

-- ----------------------------------------------------------------------------
-- 9. TOP FINANCIAL FLOPS (REAL LOSSES ONLY)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_top_financial_flops AS
SELECT 
    movie_id,
    title,
    release_date,
    budget,
    revenue,
    (budget - revenue) AS net_loss,
    ROUND((revenue::NUMERIC / NULLIF(budget, 0)), 2) AS roi
FROM dim_movies
WHERE budget > 0 
  AND revenue > 0 
  AND budget > revenue
ORDER BY net_loss DESC;

-- ----------------------------------------------------------------------------
-- 10. WORST PERFORMING DIRECTORS BY AVG ROI (MIN 3 MOVIES, BUDGET >= $1M)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_worst_performing_directors AS
SELECT 
    p.person_id,
    p.name AS director_name,
    COUNT(DISTINCT m.movie_id) AS total_movies_directed,
    SUM(m.budget) AS total_budget,
    SUM(m.revenue) AS total_revenue,
    SUM(m.revenue - m.budget) AS total_net_profit,
    ROUND(AVG(m.revenue::NUMERIC / NULLIF(m.budget, 0)), 2) AS avg_roi
FROM dim_people p
JOIN movie_crew mc ON p.person_id = mc.person_id
JOIN dim_movies m ON mc.movie_id = m.movie_id
WHERE mc.job = 'Director' 
  AND m.budget >= 1000000 
  AND m.revenue > 0
GROUP BY p.person_id, p.name
HAVING COUNT(DISTINCT m.movie_id) >= 3
ORDER BY avg_roi ASC;

-- ----------------------------------------------------------------------------
-- 11. LOWEST ROI LEAD ACTORS (MIN 3 MOVIES, BUDGET >= $1M)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_lowest_roi_lead_actors AS
SELECT 
    p.person_id,
    p.name AS actor_name,
    COUNT(DISTINCT m.movie_id) AS lead_roles_count,
    SUM(m.budget) AS total_budget_spent,
    SUM(m.revenue) AS total_box_office,
    SUM(m.revenue - m.budget) AS total_net_profit,
    ROUND(AVG(m.revenue::NUMERIC / NULLIF(m.budget, 0)), 2) AS avg_roi
FROM dim_people p
JOIN movie_cast mc ON p.person_id = mc.person_id
JOIN dim_movies m ON mc.movie_id = m.movie_id
WHERE mc.cast_order <= 3 
  AND m.budget >= 1000000 
  AND m.revenue > 0
GROUP BY p.person_id, p.name
HAVING COUNT(DISTINCT m.movie_id) >= 3
ORDER BY total_net_profit ASC;