from google.cloud import bigquery
from datetime import datetime, timezone
import uuid

PROJECT_ID = "project-5d19c72c-351f-4c80-8fc"
DATASET_ID = "seo_diagnostic"
TABLE_ID = "roundtrip_test"

client = bigquery.Client(project=PROJECT_ID)

table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

schema = [
    bigquery.SchemaField("test_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("note", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
]

table = bigquery.Table(table_ref, schema=schema)
client.create_table(table, exists_ok=True)

test_id = str(uuid.uuid4())

rows = [
    {
        "test_id": test_id,
        "note": "M0W4D2 BigQuery Python roundtrip test",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
]

errors = client.insert_rows_json(table_ref, rows)

if errors:
    raise RuntimeError(f"Insert failed: {errors}")

query = f"""
SELECT
  test_id,
  note,
  created_at
FROM `{table_ref}`
WHERE test_id = @test_id
LIMIT 1
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("test_id", "STRING", test_id)
    ]
)

result = client.query(query, job_config=job_config).result()

for row in result:
    print("Roundtrip OK")
    print(f"test_id: {row.test_id}")
    print(f"note: {row.note}")
    print(f"created_at: {row.created_at}")