# AI SEO Portfolio

A personal engineering portfolio for building AI-powered SEO and AI Search workflows.

This repository documents and builds practical systems for SEO data diagnostics, BigQuery analysis, Python automation, LLM-assisted content audit, entity SEO, internal linking, AI visibility, RAG, and MCP-based SEO tooling.

## TL;DR

This project is a hands-on AI SEO engineering portfolio.

It starts with a BigQuery-backed SEO data model, then expands into Python data pipelines, crawl diagnostics, opportunity scoring, LLM content audits, semantic clustering, internal linking, AI visibility monitoring, and stakeholder-ready reporting.

## Project Goals

This project is designed to build hands-on capability in:

- SEO data engineering
- BigQuery SQL analysis
- Python automation for SEO workflows
- Google Search Console data processing
- Technical SEO crawling and diagnostics
- LLM-based content and compliance audit
- Entity SEO and internal linking systems
- AI Search / GEO visibility workflows
- RAG and MCP-based SEO tooling

## Current Milestone (10-May-2026)

M0 W1: Project foundation

Completed:

- Created GitHub repository
- Created project folder structure
- Prepared BigQuery Sandbox workflow
- Created BigQuery dataset: `seodiagnostic`
- Created first GSC query schema
- Added `is_branded` field for branded vs non-branded query analysis
- Configured Python virtual environment
- Added Python dependencies in `requirements.txt`

## Repository Structure

```text
AI-SEO-Portfolio/
├── data/
│   ├── raw/              # Raw exports such as GSC CSV files
│   └── processed/        # Cleaned or transformed datasets
├── docs/                 # Technical notes, schema design, release logs
├── notebooks/            # Exploratory analysis and experiments
├── notes/                # Daily learning notes
├── outputs/              # Final reports, CSV outputs, playbooks
├── prompts/              # LLM prompt templates
├── schemas/              # BigQuery schemas and JSON schemas
├── scripts/              # Helper scripts and automation runners
├── sql/                  # BigQuery SQL files
├── src/                  # Python source code
├── .env.example          # Example environment variables
├── .gitignore            # Files and folders excluded from Git
├── requirements.txt      # Python package dependencies
└── README.md
```

## Setup

Clone the repository:

```powershell
git clone https://github.com/CasparSEO/AI-SEO-Portfolio.git
cd AI-SEO-Portfolio
```

Create a Python virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Environment Variables

This project uses `.env` for local secrets and configuration.

Create a local `.env` file based on `.env.example`:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_APPLICATION_CREDENTIALS=
GCP_PROJECT_ID=
BIGQUERY_DATASET=seodiagnostic
```

Do not commit `.env`, API keys, service account JSON files, or raw private data to GitHub.

## Data Policy

Raw data should be stored in:

```text
data/raw/
```

Processed data should be stored in:

```text
data/processed/
```

These folders are ignored by Git except for `.gitkeep` files, so the folder structure is preserved without exposing private data.

## Architecture

```text
GSC exports / crawl data / content data
        |
        v
BigQuery dataset: seodiagnostic
        |
        v
SQL + Python diagnostics
        |
        v
Reports, CSV outputs, audits, and recommendations
```

## Roadmap

- M0: Database, repo, schemas, Python foundation
- M1: GSC and crawl pipeline with diagnostic report
- M2: LLM content and compliance audit layer
- M3: Embeddings and keyword cannibalization analysis
- M4: Entity map, JSON-LD, and internal linking system
- M5: AI visibility and GEO monitoring
- M6: MCP-style SEO assistant tools
- M7: International AI visibility workflows
- M8: Lead-level playbook, ROI framework, and portfolio packaging

## Status

Current version: `v0.1.0`

This repository is in active development.

## Current Milestone (17-May-2026)

### v0.1.5 - M0W2 SEO Diagnostic Database Schema

The project now includes a 5-table SEO diagnostic data model, BigQuery DDL files, a DuckDB local fallback, and an ER diagram created with dbdiagram.io.

Key files:

- `sql/`
- `src/init_duckdb.py`
- `docs/er-diagram.md`
- `release-log.md`

## GSC CSV Export (18-May-2026)

- Source: Google Search Console export
- File: `data/raw/gscqueriesraw.csv`
- Schema: aligned with previous `gscqueries` schema
- Header: `date,url,query,clicks,impressions,ctr,position,country,device,is_branded`
- Clean CSV: not generated, because raw file already matches schema
- Next: load CSV into BigQuery `gscqueries` table

### Load GSC CSV to BigQuery  (18-May-2026)

Loaded `data/raw/gscqueriesraw.csv` into BigQuery table `seodiagnostic.gscqueries`.
Validation query: `SELECT COUNT(*) FROM seodiagnostic.gscqueries`.