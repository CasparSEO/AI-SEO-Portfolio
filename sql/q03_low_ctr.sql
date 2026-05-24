SELECT
  query,
  url,
  SUM(clicks) AS clicks,
  SUM(impressions) AS impressions,
  SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS ctr,
  SAFE_DIVIDE(SUM(positions * impressions), SUM(impressions)) AS avg_position
FROM `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries`
WHERE query IS NOT NULL
  AND TRIM(query) != ''
  AND LOWER(CAST(is_branded AS STRING)) = 'false'
GROUP BY query, url
HAVING impressions >= 100
   AND avg_position <= 10
   AND ctr < 0.02
ORDER BY impressions DESC
LIMIT 50;