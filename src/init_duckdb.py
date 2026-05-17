from pathlib import Path
import duckdb

DB_PATH = Path("data/seo_diagnostic.duckdb")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(DB_PATH))

con.execute("""
CREATE TABLE IF NOT EXISTS gsc_daily_request (
  date DATE,
  query VARCHAR,
  is_branded BOOLEAN,
  landing_page VARCHAR,
  gsc_clicks BIGINT,
  gsc_impressions BIGINT,
  gsc_ctr_pct DOUBLE,
  gsc_avg_position DOUBLE,
  gsc_reporting_region VARCHAR,
  gsc_device_category VARCHAR
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS gsc_pages (
  date DATE,
  landing_page VARCHAR,
  gsc_clicks BIGINT,
  gsc_impressions BIGINT,
  gsc_ctr_pct DOUBLE,
  gsc_avg_position DOUBLE,
  gsc_reporting_region VARCHAR,
  gsc_device_category VARCHAR
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS crawl_results (
  crawl_date DATE,
  landing_page VARCHAR,
  final_url VARCHAR,
  status_code BIGINT,
  title VARCHAR,
  title_length BIGINT,
  meta_description VARCHAR,
  meta_description_length BIGINT,
  h1 VARCHAR,
  h1_count BIGINT,
  canonical_url VARCHAR,
  canonical_matches_landing_page BOOLEAN,
  word_count BIGINT,
  publish_date DATE,
  update_date DATE,
  has_schema BOOLEAN,
  schema_types VARCHAR,
  internal_links_count BIGINT,
  external_links_count BIGINT,
  crawl_source VARCHAR
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS opportunity_scores (
  score_date DATE,
  landing_page VARCHAR,
  query VARCHAR,
  opportunity_score DOUBLE,
  opportunity_type VARCHAR,
  issue_summary VARCHAR,
  recommended_action VARCHAR,
  priority VARCHAR
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS content_inventory (
  landing_page VARCHAR,
  language VARCHAR,
  market VARCHAR,
  content_type VARCHAR,
  primary_topic VARCHAR,
  publish_date DATE,
  update_date DATE,
  content_status VARCHAR
);
""")

tables = con.execute("SHOW TABLES").fetchall()
print("DuckDB initialized:", DB_PATH)
print("Tables:")
for table in tables:
    print("-", table[0])

con.close()