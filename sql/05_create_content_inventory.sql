CREATE TABLE IF NOT EXISTS `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.content_inventory` (
  landing_page STRING,
  language STRING,
  market STRING,
  content_type STRING,
  primary_topic STRING,
  publish_date DATE,
  update_date DATE,
  content_status STRING
)
CLUSTER BY landing_page, primary_topics;