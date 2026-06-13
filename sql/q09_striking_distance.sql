WITH params AS (
  SELECT
    MAX(date) AS max_date,
    DATE_SUB(MAX(date), INTERVAL 13 DAY) AS start_date_14d
  FROM
    `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries`
),

recent_14d AS (
  SELECT
    g.url,
    g.query,
    SUM(g.clicks) AS clicks_14d,
    SUM(g.impressions) AS impressions_14d,
    SAFE_DIVIDE(SUM(g.clicks), SUM(g.impressions)) AS ctr_14d,
    SAFE_DIVIDE(SUM(g.positions * g.impressions), SUM(g.impressions)) AS avg_position_14d
  FROM
    `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries` AS g,
    params
  WHERE
    g.date BETWEEN params.start_date_14d AND params.max_date
    AND g.query IS NOT NULL
    AND TRIM(g.query) != ''
    AND g.url IS NOT NULL
    AND TRIM(g.url) != ''
    AND g.is_branded IS FALSE
    AND REGEXP_CONTAINS(
      LOWER(g.query),
      r'(payment|payments|online payment|business account|merchant account|virtual card|expense card|expense management|multi[- ]currency|fx|foreign exchange|global transfer|international transfer|cross[- ]border|payout|payouts|remittance|remit|wallet|checkout|gateway|收款|支付|付款|匯款|轉賬|轉帳|外匯|外幣|多幣種|虛擬卡|商戶帳戶|商戶賬戶|開戶|開戶口|企業戶口|公司戶口|business banking|corporate card|公司卡|企業卡)'
    )
  GROUP BY
    g.url,
    g.query
),

scored AS (
  SELECT
    url,
    query,
    clicks_14d,
    impressions_14d,
    ctr_14d,
    avg_position_14d
  FROM
    recent_14d
  WHERE
    impressions_14d > 10
    AND avg_position_14d BETWEEN 11 AND 30
)

SELECT
  url,
  query,
  clicks_14d,
  impressions_14d,
  ROUND(ctr_14d * 100, 2) AS ctr_14d_percent,
  ROUND(avg_position_14d, 2) AS avg_position_14d,
  ROUND(
    impressions_14d * (31 - avg_position_14d) / 20,
    2
  ) AS opportunity_score
FROM
  scored
ORDER BY
  opportunity_score DESC,
  impressions_14d DESC,
  clicks_14d DESC
LIMIT 200;