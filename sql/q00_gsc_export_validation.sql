-- GSC export validation query
-- Replace project_id if needed.

SELECT
  COUNT(*) AS row_count,
  MIN(date) AS min_date,
  MAX(date) AS max_date,
  COUNT(DISTINCT query) AS unique_queries,
  COUNT(DISTINCT url) AS unique_urls,
  SUM(clicks) AS total_clicks,
  SUM(impressions) AS total_impressions,
  SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS weighted_ctr,
  AVG(position) AS avg_position
FROM `seodiagnostic.gscqueries`;
