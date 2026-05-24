import pandas as pd
from pathlib import Path

input_file = Path("data/raw/gscqueriesraw20260101.csv")
output_file = Path("data/raw/crawlseed.csv")

df = pd.read_csv(input_file)

df.columns = [c.strip() for c in df.columns]

if "url" not in df.columns and "landing_page" in df.columns:
    df = df.rename(columns={"landing_page": "url"})

if "impressions" not in df.columns and "gsc_impressions" in df.columns:
    df = df.rename(columns={"gsc_impressions": "impressions"})

if "clicks" not in df.columns and "gsc_clicks" in df.columns:
    df = df.rename(columns={"gsc_clicks": "clicks"})

required = ["url", "impressions", "clicks"]
missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}. Actual columns: {df.columns.tolist()}")

seed = (
    df.groupby("url", as_index=False)
      .agg({"impressions": "sum", "clicks": "sum"})
      .sort_values("impressions", ascending=False)
      .head(30)
)

output_file.parent.mkdir(parents=True, exist_ok=True)
seed[["url"]].to_csv(output_file, index=False)

print(f"Wrote {output_file} with {len(seed)} URLs")
