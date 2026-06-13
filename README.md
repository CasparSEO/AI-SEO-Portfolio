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

### M1W7 - URL-query Opportunity Scoring

Built a scoring layer that ranks non-branded URL-query opportunities using Google Search Console data.

Key outputs:
- `docs/scoringmodel.md`
- `src/scoreopportunities.py`
- `outputs/top50opportunities.csv`
- `outputs/m1w7pitch.md`

This workflow turns raw GSC data into a practical SEO action list: which URL to improve, which query to target, why it matters, and what action to take next.

## Status

Current phase: `M1 - SEO Data Pipeline`

Completed:
- M0W1 Project Foundation
- M0W2 Diagnostic Schema
- M0W3 GSC + Crawl SQL Diagnostics
- M0W4 Python + BigQuery Automation
- M1W6 Crawl + GSC Join
- M1W7 URL-query Opportunity Scoring

In progress:
- M1W8 Diagnostic Report

This repository is in active development.

## No-API GSC Workflow

This project uses Google Search Console CSV exports and BigQuery SQL instead of the Search Console API.

Current pipeline:
1. Export query/page data from GSC
2. Load CSV into BigQuery table `seo_diagnostic.gscqueries`
3. Run SQL diagnostics from `sql/`
4. Generate prioritised opportunity outputs in `outputs/`
5. Convert scored opportunities into a short diagnostic report

## M1 Diagnostic Layer

This module turns Google Search Console query-level data and crawl signals into prioritised SEO opportunities.

The workflow focuses on non-branded queries with real search demand, recent impressions, and striking-distance rankings. Instead of only reporting performance, it ranks URL-query pairs by opportunity score and converts them into specific SEO actions such as title/meta refreshes, content expansion, and internal linking improvements.

### Key outputs

- `docs/scoringmodel.md`  
  Scoring logic for striking-distance opportunities, CTR improvement potential, and future Google AIO readiness extension

- `src/scoreopportunities.py`  
  Python script that queries BigQuery and exports prioritised SEO opportunities

- `outputs/top50opportunities.csv`  
  Top 50 URL-query opportunities ranked by score, reason, and recommended action

- `docs/diagnosticreport.md`  
  Short markdown report that translates scored opportunities into practical next steps

### Example opportunities

Sample opportunities from the current output include:
- `https://www.airwallex.com/hk-zh/blog/remittance-to-mainland-china` → `大陸匯款到香港限制`
- `https://www.airwallex.com/hk-zh/blog/business-registration-certificate` → `商業登記處派籌時間`
- `https://www.airwallex.com/hk/blog/dbs-open-account` → `dbs business account`

These examples show the kind of opportunity this project is designed to identify: pages already ranking near page one but still underperforming in CTR, content depth, or internal linking support.