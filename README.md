## Milestones

### M0W1 - Project Foundation

Set up the AI SEO portfolio repository and the first BigQuery-backed SEO data foundation.

Completed:
- Created the GitHub repository and local project structure
- Set up Python virtual environment and `requirements.txt`
- Prepared the BigQuery Sandbox workflow
- Created the SEO diagnostic dataset
- Designed the first GSC query schema
- Added `is_branded` for branded vs non-branded analysis

Key outputs:
- `README.md`
- `requirements.txt`
- `data/`
- `sql/`
- `src/`

---

### M0W2 - Diagnostic Schema

Built the first version of the SEO diagnostic database model.

Completed:
- Designed a 5-table SEO diagnostic schema
- Created BigQuery DDL files
- Added a local DuckDB fallback setup
- Created an ER diagram
- Documented the schema and release milestone

Core tables:
- `gscqueries`
- `gsc_pages`
- `crawl_results`
- `opportunity_scores`
- `content_inventory`

Key outputs:
- `sql/`
- `src/init_duckdb.py`
- `docs/er-diagram.md`
- `release-log.md`

---

### M0W3 - GSC + Crawl SQL Diagnostics

Built a reusable workflow that combines Google Search Console data, lightweight crawl data, and BigQuery SQL analysis to identify early SEO opportunities.

Completed:
- Exported GSC query/page data
- Loaded GSC data into BigQuery
- Generated a 30-URL crawl seed from GSC landing pages
- Crawled key on-page SEO fields including status code, title, meta description, H1, canonical, word count, and schema presence
- Created and tested 3 BigQuery opportunity queries

SQL outputs:
- `sql/q01_top_queries.sql`
- `sql/q02_striking_distance.sql`
- `sql/q03_low_ctr.sql`

Data policy:
- Raw GSC and crawl CSV files stay in `data/raw/`
- Private raw data is not committed to GitHub

Key outputs:
- `src/make_crawlseed.py`
- `src/crawl_urls.py`
- `sql/q01_top_queries.sql`
- `sql/q02_striking_distance.sql`
- `sql/q03_low_ctr.sql`

---

### M0W4 - Python + BigQuery Automation

Started converting manual BigQuery and CSV workflows into repeatable Python automation.

Completed:
- Set up Python BigQuery client authentication
- Created a BigQuery roundtrip test script
- Loaded local GSC CSV data into BigQuery using Python
- Started BigQuery-to-local sync workflow using DuckDB and Parquet

Automation scripts:
- `src/bq_auth_check.py`
- `src/00_roundtrip_test.py`
- `src/load_csv_to_bq.py`
- `src/sync_bq_to_duckdb.py`

Local analytics layer:
- BigQuery is the main cloud warehouse
- DuckDB and Parquet are local fallback analysis layers
- Processed local data in `data/processed/` is not committed to GitHub

Key outputs:
- `src/load_csv_to_bq.py`
- `src/sync_bq_to_duckdb.py`
- `requirements.txt`

---

### M1W6 - Crawl + GSC Join

Joined crawl results with GSC performance data to create a page-level SEO diagnostic layer.

Completed:
- Crawled 30 URLs successfully
- Loaded crawl data into BigQuery table `seo_diagnostic.crawl_results`
- Joined GSC page/query performance with crawl signals including status code, title, H1, canonical, word count, and schema presence

Key output:
- `sql/q05_gsc_crawl_join_page_level.sql`

---

### 