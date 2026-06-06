WITH params AS (
  SELECT
    MAX(date) AS max_date,
    DATE_SUB(MAX(date), INTERVAL 90 DAY) AS start_date
  FROM `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries`
),

filtered_gsc AS (
  SELECT
    date,
    query,
    url,
    clicks,
    impressions,
    positions,
    is_branded
  FROM `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries`, params
  WHERE date BETWEEN params.start_date AND params.max_date
    AND query IS NOT NULL
    AND url IS NOT NULL
    AND is_branded = FALSE
),

weekly_url_query_metrics AS (
  SELECT
    DATE_TRUNC(date, WEEK(MONDAY)) AS week_start,
    url,
    query,
    SUM(clicks) AS clicks,
    SUM(impressions) AS impressions,
    ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2) AS ctr_percent,
    ROUND(AVG(positions), 2) AS avg_position
  FROM filtered_gsc
  GROUP BY week_start, url, query
),

trend AS (
  SELECT
    week_start,
    url,
    query,
    clicks,
    impressions,
    ctr_percent,
    avg_position,
    LAG(clicks) OVER (
      PARTITION BY url, query
      ORDER BY week_start
    ) AS previous_week_clicks,
    clicks - LAG(clicks) OVER (
      PARTITION BY url, query
      ORDER BY week_start
    ) AS click_change
  FROM weekly_url_query_metrics
)

SELECT
  week_start,
  url,
  query,
  clicks,
  previous_week_clicks,
  click_change,
  impressions,
  ctr_percent,
  avg_position
FROM trend
WHERE previous_week_clicks IS NOT NULL
ORDER BY ABS(click_change) DESC, clicks DESC
LIMIT 100;