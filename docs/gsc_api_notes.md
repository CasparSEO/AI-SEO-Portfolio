# GSC API Notes — Airwallex

## Property

Domain property:

```text
sc-domain:airwallex.com
```

URL-prefix property:

```text
https://www.airwallex.com/
```

Use the exact property that exists in Google Search Console.

## Search Analytics API

Endpoint/method:

```text
searchanalytics.query
```

Core request fields:

```json
{
  "startDate": "2026-03-01",
  "endDate": "2026-05-31",
  "dimensions": ["query", "page", "date"],
  "rowLimit": 25000,
  "startRow": 0
}
```

## Notes

- `query` = keyword searched in Google
- `page` = landing page URL
- `date` = daily trend dimension
- `clicks` = organic search clicks
- `impressions` = search result impressions
- `ctr` = clicks divided by impressions
- `position` = average Google ranking position
- Use pagination with `startRow` when exporting more than 25,000 rows
- Store query-level data in `gscqueries`
- Store page-level data in `gscpages`
