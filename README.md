# AI SEO Portfolio

A personal engineering portfolio for building AI-powered SEO and AI Search workflows.

This repository is used to document and build practical systems for SEO data diagnostics, BigQuery analysis, Python automation, LLM-assisted content audit, entity SEO, internal linking, AI visibility, RAG, and MCP-based SEO tooling.

## Project Goals

This project is designed to help me build hands-on capability in:

- SEO data engineering
- BigQuery SQL analysis
- Python automation for SEO workflows
- Google Search Console data processing
- Technical SEO crawling and diagnostics
- LLM-based content and compliance audit
- Entity SEO and internal linking systems
- AI Search / GEO visibility workflows
- RAG and MCP-based SEO tooling

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
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Environment Variables

This project uses `.env` for local secrets and configuration.

Create a local `.env` file based on `.env.example`:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_APPLICATION_CREDENTIALS=
GCP_PROJECT_ID=
BIGQUERY_DATASET=seo_diagnostic
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

## Current Stage

M0 W1: Project foundation

Current focus:
- Set up GitHub repository
- Create project folder structure
- Prepare BigQuery Sandbox workflow
- Configure Python environment