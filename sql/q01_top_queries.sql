SELECT
  query,
  SUM(clicks) AS clicks,
  SUM(impressions) AS impressions,
  ROUND(SAFE_DIVIDE(SUM(clicks), SUM(impressions)) * 100, 2) AS ctr_percent,
  ROUND(AVG(positions), 2) AS avg_position
FROM `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries`
GROUP BY query
ORDER BY clicks DESC
LIMIT 20;