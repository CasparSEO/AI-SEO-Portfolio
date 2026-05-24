import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from pathlib import Path

seed_file = Path("data/raw/crawlseed.csv")
output_file = Path("data/raw/crawlresults.csv")

seed = pd.read_csv(seed_file)
rows = []

for url in seed["url"].dropna().head(30):
    try:
        r = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (compatible; AI-SEO-Portfolio/1.0)"}
        )

        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        h1_tag = soup.find("h1")
        h1 = h1_tag.get_text(" ", strip=True) if h1_tag else ""

        canonical_tag = soup.find("link", rel="canonical")
        canonical = canonical_tag.get("href", "") if canonical_tag else ""

        meta_desc_tag = soup.find("meta", attrs={"name": "description"})
        metadescription = meta_desc_tag.get("content", "").strip() if meta_desc_tag else ""

        schemafound = bool(soup.find("script", type="application/ld+json"))
        wordcount = len(soup.get_text(" ", strip=True).split())

        rows.append({
            "url": url,
            "statuscode": r.status_code,
            "title": title,
            "metadescription": metadescription,
            "h1": h1,
            "canonical": canonical,
            "wordcount": wordcount,
            "schemafound": schemafound,
            "crawledat": datetime.now(timezone.utc).isoformat()
        })

        print(f"OK {r.status_code} {url}")

    except Exception as e:
        rows.append({
            "url": url,
            "statuscode": 0,
            "title": "",
            "metadescription": "",
            "h1": "",
            "canonical": "",
            "wordcount": 0,
            "schemafound": False,
            "crawledat": datetime.now(timezone.utc).isoformat()
        })

        print(f"FAIL {url} {e}")

output_file.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"Wrote {output_file} with {len(rows)} rows")
