-- q09_striking_distance.sql
-- M0W7D2 – Striking distance opportunities (GSC only)

WITH base AS (
  SELECT
    url,
    query,
    SUM(clicks) AS clicks,
    SUM(impressions) AS impressions,
    SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS ctr,
    AVG(positions) AS avg_position
  FROM
    `project-5d19c72c-351f-4c80-8fc.seodiagnostic.gscqueries`
  WHERE
    query IS NOT NULL
    AND url IS NOT NULL
       -- AND isbranded IS FALSE
  GROUP BY
    url,
    query
),

striking_distance AS (
  SELECT
    url,
    query,
    clicks,
    impressions,
    ctr,
    avg_position
  FROM
    base
  WHERE
    impressions >= 100
    AND avg_position BETWEEN 11 AND 20
)

SELECT
  url,
  query,
  clicks,
  impressions,
  ROUND(ctr * 100, 2) AS ctr_percent,
  ROUND(avg_position, 2) AS avg_position,
  ROUND(
    impressions * (21 - LEAST(GREATEST(avg_position, 11), 20)) / 10,
    2
  ) AS opportunity_score
FROM
  striking_distance
ORDER BY
  opportunity_score DESC,
  impressions DESC
LIMIT 200;