CREATE TABLE IF NOT EXISTS `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gsc_daily_request` (
  date DATE,
  query STRING,
  is_branded BOOL,
  landing_page STRING,
  gsc_clicks INT64,
  gsc_impressions INT64,
  gsc_ctr_pct FLOAT64,
  gsc_avg_position FLOAT64,
  gsc_reporting_region STRING,
  gsc_device_category STRING
)
PARTITION BY date
CLUSTER BY url, query;