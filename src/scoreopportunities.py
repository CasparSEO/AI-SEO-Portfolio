from pathlib import Path
from google.cloud import bigquery

PROJECT_ID = "project-5d19c72c-351f-4c80-8fc"
TABLE_ID = "`project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries`"
OUTPUT_PATH = Path("outputs/top50opportunities.csv")

QUERY = f"""
WITH params AS (
  SELECT
    MAX(date) AS max_date,
    DATE_SUB(MAX(date), INTERVAL 14 DAY) AS start_date
  FROM {TABLE_ID}
),

base AS (
  SELECT
    url,
    query,
    SUM(clicks) AS clicks,
    SUM(impressions) AS impressions,
    SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS ctr,
    SAFE_DIVIDE(SUM(positions * impressions), SUM(impressions)) AS avg_position
  FROM {TABLE_ID}, params
  WHERE
    date BETWEEN params.start_date AND params.max_date
    AND query IS NOT NULL
    AND TRIM(query) != ''
    AND url IS NOT NULL
    AND TRIM(url) != ''
    AND is_branded IS FALSE
  GROUP BY
    url,
    query
),

scored AS (
  SELECT
    url,
    query,
    clicks,
    impressions,
    ctr,
    avg_position,
    ROUND(
      impressions * (31 - avg_position) / 20,
      2
    ) AS opportunity_score,
    CASE
      WHEN avg_position BETWEEN 11 AND 15 THEN 'High striking-distance opportunity'
      WHEN avg_position BETWEEN 16 AND 20 THEN 'Medium striking-distance opportunity'
      WHEN avg_position BETWEEN 21 AND 30 THEN 'Lower ranking opportunity'
      ELSE 'Other'
    END AS reason,
    CASE
      WHEN avg_position BETWEEN 11 AND 20 AND ctr < 0.02 THEN 'Refresh content and rewrite title/meta'
      WHEN avg_position BETWEEN 11 AND 20 THEN 'Improve content depth and internal links'
      WHEN avg_position BETWEEN 21 AND 30 THEN 'Strengthen topical relevance and supporting sections'
      ELSE 'Review manually'
    END AS recommended_action
  FROM base
  WHERE
    impressions > 10
    AND avg_position BETWEEN 11 AND 30
)

SELECT
  url,
  query,
  clicks,
  impressions,
  ROUND(ctr * 100, 2) AS ctr_percent,
  ROUND(avg_position, 2) AS avg_position,
  opportunity_score,
  reason,
  recommended_action
FROM scored
ORDER BY
  opportunity_score DESC,
  impressions DESC,
  clicks DESC
LIMIT 50
"""

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    client = bigquery.Client(project=PROJECT_ID)
    df = client.query(
        QUERY,
        location="asia-east2"
    ).to_dataframe()

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} rows to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()