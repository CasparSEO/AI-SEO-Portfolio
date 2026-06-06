WITH g AS (
  SELECT
    REGEXP_REPLACE(
      REGEXP_REPLACE(LOWER(TRIM(url)), r'[?#].*$', ''),
      r'/$',
      ''
    ) AS join_url,
    ANY_VALUE(url) AS gsc_url,
    SUM(clicks) AS total_clicks,
    SUM(impressions) AS total_impressions,
    SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS weighted_ctr,
    AVG(positions) AS avg_position,
    COUNT(DISTINCT query) AS query_count
  FROM `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries`
  GROUP BY join_url
),
c AS (
  SELECT
    REGEXP_REPLACE(
      REGEXP_REPLACE(LOWER(TRIM(url)), r'[?#].*$', ''),
      r'/$',
      ''
    ) AS join_url,
    ANY_VALUE(url) AS crawled_url,
    ANY_VALUE(statuscode) AS statuscode,
    ANY_VALUE(title) AS title,
    ANY_VALUE(metadescription) AS metadescription,
    ANY_VALUE(h1) AS h1,
    ANY_VALUE(canonical) AS canonical,
    ANY_VALUE(wordcount) AS wordcount,
    ANY_VALUE(schemafound) AS schemafound
  FROM `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.crawl_results`
  GROUP BY join_url
)
SELECT
  g.gsc_url,
  c.crawled_url,
  g.total_clicks,
  g.total_impressions,
  g.weighted_ctr,
  g.avg_position,
  g.query_count,
  c.statuscode,
  c.title,
  c.h1,
  c.canonical,
  c.wordcount,
  c.schemafound,
  CASE
    WHEN c.crawled_url IS NULL THEN 'not crawled'
    WHEN c.statuscode != 200 THEN 'status issue'
    WHEN c.h1 IS NULL OR c.h1 = '' THEN 'missing h1'
    WHEN c.canonical IS NULL OR c.canonical = '' THEN 'missing canonical'
    WHEN c.wordcount < 300 THEN 'thin content'
    WHEN c.schemafound = FALSE THEN 'missing schema'
    ELSE 'ok'
  END AS onpage_issue
FROM g
LEFT JOIN c
  ON g.join_url = c.join_url
ORDER BY g.total_impressions DESC
LIMIT 50;