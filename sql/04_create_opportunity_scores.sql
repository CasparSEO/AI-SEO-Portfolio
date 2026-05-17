CREATE TABLE IF NOT EXISTS `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.opportunity_scores` (
  score_date DATE,
  landing_page STRING,
  query STRING,
  striking_distance_score FLOAT64,
  ctr_gap_score FLOAT64,
  content_gap_score FLOAT64,
  total_score FLOAT64,
  recommendation STRING
)
PARTITION BY score_date
CLUSTER BY landing_page, query;