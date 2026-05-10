## M0W1D3: gsc_daily_request

BigQuery target:

```text
project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gsc_daily_request
```

Raw data location:

```text
data/raw/gsc_daily_request.csv
```

### Field Naming Decision

This table uses explicit `gsc_` prefixes for metric fields:

- `gsc_clicks`
- `gsc_impressions`
- `gsc_ctr_pct`
- `gsc_avg_position`
- `gsc_reporting_region`
- `gsc_device_category`


### Initial Fields

| Field | Type | Purpose |
|---|---|---|
| date | DATE | GSC performance date |
| query | STRING | Search query |
|is_branded| BOOL | Branded Terms|
| landing_page | STRING | Landing page URL |
| gsc_clicks | INT64 | Organic clicks |
| gsc_impressions | INT64 | Organic impressions |
| gsc_ctr_pct | FLOAT64 | Click-through rate |
| gsc_avg_position | FLOAT64 | Average ranking position |
| gsc_reporting_region | STRING | Search country |
| gsc_device_category | STRING | Device type |

Reason:

- Avoids confusion when this table is joined with crawl, content audit, or AI visibility tables.
- Makes it clear that these metrics come from Google Search Console.
- Keeps future reporting fields easier to understand.

### Partition and Clustering

The table is partitioned by `date` because most SEO diagnostics will filter by reporting period.

The table is clustered by `landing_page` and `query` because most future analysis will group by URL and search query.

Metric columns use the `gsc_` prefix to avoid confusion when joined with crawl data, content audit data, or AI visibility data.

`is_branded` is stored as `BOOL` because it is a binary query classification field, where the braned terms is containing `airwallex`