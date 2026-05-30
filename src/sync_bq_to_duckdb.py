from google.cloud import bigquery
from pathlib import Path
import duckdb

PROJECT_ID = "project-5d19c72c-351f-4c80-8fc"
DATASET_ID = "seo_diagnostic"
SOURCE_TABLE = "gscqueries_python_load_test"

duckdb_path = Path("data/seodiagnostic.duckdb")
parquet_path = Path("data/processed/gscqueries.parquet")

duckdb_path.parent.mkdir(parents=True, exist_ok=True)
parquet_path.parent.mkdir(parents=True, exist_ok=True)

client = bigquery.Client(project=PROJECT_ID)

query = f"""
SELECT
  date,
  url,
  query,
  clicks,
  impressions,
  ctr,
  position,
  country,
  device,
  is_branded
FROM `{PROJECT_ID}.{DATASET_ID}.{SOURCE_TABLE}`
"""

print("Querying BigQuery...")
df = client.query(query).to_dataframe()

print(f"Rows downloaded: {len(df)}")

print("Writing Parquet...")
df.to_parquet(parquet_path, index=False)

print("Writing DuckDB...")
con = duckdb.connect(str(duckdb_path))
con.execute("CREATE OR REPLACE TABLE gscqueries AS SELECT * FROM df")

row_count = con.execute("SELECT COUNT(*) FROM gscqueries").fetchone()[0]
sample = con.execute("""
    SELECT query, url, impressions, clicks
    FROM gscqueries
    ORDER BY impressions DESC
    LIMIT 5
""").fetchdf()

con.close()

print(f"DuckDB rows: {row_count}")
print(sample)
print(f"Parquet written: {parquet_path}")
print(f"DuckDB written: {duckdb_path}")