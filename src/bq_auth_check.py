from google.cloud import bigquery

PROJECT_ID = "project-5d19c72c-351f-4c80-8fc"
DATASET_ID = "seo_diagnostic"

client = bigquery.Client(project=PROJECT_ID)

query = f"""
SELECT COUNT(*) AS row_count
FROM `{PROJECT_ID}.{DATASET_ID}.gscqueries`
"""

result = client.query(query).result()

for row in result:
    print(f"gscqueries row_count: {row.row_count}")