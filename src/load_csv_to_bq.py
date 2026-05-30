from google.cloud import bigquery
from pathlib import Path

PROJECT_ID = "project-5d19c72c-351f-4c80-8fc"
DATASET_ID = "seo_diagnostic"
TABLE_ID = "gscqueries_python_load_test"

csv_path = Path("data/raw/gscqueriesraw20260101.csv")
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

client = bigquery.Client(project=PROJECT_ID)

schema = [
    bigquery.SchemaField("date", "DATE"),
    bigquery.SchemaField("url", "STRING"),
    bigquery.SchemaField("query", "STRING"),
    bigquery.SchemaField("clicks", "INT64"),
    bigquery.SchemaField("impressions", "INT64"),
    bigquery.SchemaField("ctr", "FLOAT64"),
    bigquery.SchemaField("position", "FLOAT64"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("device", "STRING"),
    bigquery.SchemaField("is_branded", "BOOL"),
]

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    schema=schema,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

print(f"Loading CSV: {csv_path}")
print(f"Destination table: {table_ref}")

with open(csv_path, "rb") as source_file:
    load_job = client.load_table_from_file(
        source_file,
        table_ref,
        job_config=job_config,
    )

load_job.result()

table = client.get_table(table_ref)

print("Load complete")
print(f"Rows loaded: {table.num_rows}")
print(f"Columns: {[field.name for field in table.schema]}")