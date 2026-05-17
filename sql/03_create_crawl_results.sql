CREATE TABLE IF NOT EXISTS `project-5d19c72c-351f-4c80-8fc.seo_diagnostic.crawl_results` (
  crawl_date DATE,
  landing_page STRING,
  final_url STRING,
  status_code INT64,

  title STRING,
  title_length INT64,

  meta_description STRING,
  meta_description_length INT64,

  h1 STRING,
  h1_count INT64,

  canonical_url STRING,
  canonical_matches_landing_page BOOL,

  word_count INT64,

  publish_date DATE,
  update_date DATE,

  has_schema BOOL,
  schema_types STRING,

  internal_links_count INT64,
  external_links_count INT64,

  crawl_source STRING
)
PARTITION BY crawl_date
CLUSTER BY landing_page;