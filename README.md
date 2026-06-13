## Milestones

### M0W1 - Project Foundation

Set up the AI SEO portfolio repository and established the initial BigQuery-backed SEO data foundation.

Completed:
- Created the GitHub repository and local project structure
- Set up Python virtual environment and `requirements.txt`
- Prepared BigQuery Sandbox workflow
- Created the SEO diagnostic dataset
- Designed the first GSC query schema
- Added `is_branded` for branded vs non-branded query analysis

Key outputs:
- `README.md`
- `requirements.txt`
- `data/`
- `sql/`
- `src/`

---

### M0W2 - SEO Diagnostic Database Schema

Built the first version of the SEO diagnostic database model.

Completed:
- Designed a 5-table SEO diagnostic schema
- Created BigQuery DDL files
- Added a local DuckDB fallback setup
- Created an ER diagram for the diagnostic data model
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

### M0W3 - GSC + Crawl SQL Diagnostic

Built a reusable workflow that combines Google Search Console data, lightweight crawl data, and BigQuery SQL analysis to identify early SEO opportunities.

Completed:
- Exported GSC query/page data
- Loaded GSC data into BigQuery
- Generated a 30-URL crawl seed from GSC landing pages
- Crawled on-page SEO fields such as status code, title, meta description, H1, canonical, word count, and schema presence
- Created and tested 3 BigQuery opportunity queries

SQL analysis:
- `sql/q01_top_queries.sql` - Top queries by impressions and clicks
- `sql/q02_striking_distance.sql` - Non-branded query/page pairs ranking 11-20
- `sql/q03_low_ctr.sql` - Non-branded top-10 query/page pairs with low CTR

Data policy:
- Raw GSC and crawl CSV files are stored locally in `data/raw/`
- Raw private data is not committed to GitHub

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
- BigQuery remains the cloud warehouse
- DuckDB and Parquet are used as local fallback analysis layers
- Processed local data is stored in `data/processed/` and not committed to GitHub

Key outputs:
- `src/load_csv_to_bq.py`
- `src/sync_bq_to_duckdb.py`
- `requirements.txt`

## Status

Current phase: `M0 - Database, Schema, GSC Diagnostics, and Python Automation`

Completed:
- M0W1 Project Foundation
- M0W2 SEO Diagnostic Database Schema
- M0W3 GSC + Crawl SQL Diagnostic
- M0W4 Python + BigQuery Automation in progress
This repository is in active development.

## No-API GSC workflow

This project uses Google Search Console CSV exports and BigQuery SQL instead of the Search Console API.

Current pipeline:
1. Export query/page data from GSC.
2. Load CSV into BigQuery table `seo_diagnostic.gscqueries`.
3. Run SQL diagnostics in `/sql`.
4. Save selected query outputs into `/outputs`.


## M1W6 Crawl + GSC Join

- URLs attempted: 30
- URLs crawled successfully: 30
- URLs failed: 0
- BigQuery table: `seo_diagnostic.crawl_results`
- Join SQL: `sql/q05_gsc_crawl_join_page_level.sql`
- Notes: Joined GSC query/page performance with crawl signals including status code, title, H1, canonical, word count, and schema found.


## M1W7: URL-query opportunity scoring

This module ranks non-branded URL-query opportunities using Google Search Console performance data.

Key outputs:
- `docs/scoringmodel.md`: scoring model for SEO opportunity prioritization and future Google AIO readiness
- `src/scoreopportunities.py`: Python script that queries BigQuery and exports the top opportunities
- `outputs/top50opportunities.csv`: top 50 prioritized URL-query opportunities
- `outputs/m1w7pitch.md`: portfolio pitch explaining the top 3 opportunities and recommended actions

The workflow turns raw GSC data into a practical SEO action list: which URL to improve, which query to target, why it matters, and what action to take next.