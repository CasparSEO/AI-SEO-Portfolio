# GSC Export to BigQuery Notes — Airwallex

## Current setup

This project uses manual Google Search Console export data, not the GSC API.

Domain:

```text
airwallex.com
```

Main URL-prefix:

```text
https://www.airwallex.com/
```

## Data source

Data was exported from Google Search Console and uploaded into Google BigQuery.

Approximate row count:

```text
100,000 rows
```

## BigQuery tables

Expected table pattern:

```text
seodiagnostic.gscqueries
```

Recommended columns:

```text
date
query
url
clicks
impressions
ctr
position
country
device
```

If the uploaded export only has query/page/clicks/impressions/ctr/position, country and device can be added later.

## Why no API script

No GSC API or OAuth setup is needed for this version.

Instead of:

```text
src/gsc_hello.py
src/gsc_import.py
```

This project continues from the uploaded BigQuery table and uses SQL analysis directly.

## Next step

Validate the uploaded GSC table in BigQuery, then create SEO analysis SQL files for:

- Top queries
- Top pages
- Striking-distance keywords
- Low CTR opportunities
- Click trend analysis
