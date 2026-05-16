# SEO Diagnostic Database Schema

This document defines the canonical database schema for the SEO diagnostic project.

The database connects Google Search Console performance data, crawl diagnostics, content metadata, and SEO opportunity scoring.

The five core canonical tables are:

1. `gscqueries`
2. `gscpages`
3. `crawlresults`
4. `opportunityscores`
5. `contentinventory`

These tables support the Month 1 SEO pipeline: GSC query/page analysis, URL crawling, striking-distance keyword discovery, CTR-gap analysis, content-gap analysis, and prioritized opportunity output.

---

## Legacy note: M0W1D3 gsc_daily_request

In M0W1D3, I created `gsc_daily_request` as an initial GSC query-level table.

For the canonical project schema, this table maps to `gscqueries`.

Legacy BigQuery target:

```text
project-5d19c72c-351f-4c80-8fc.seodiagnostic.gsc_daily_request
```

Canonical BigQuery target:

```text
project-5d19c72c-351f-4c80-8fc.seodiagnostic.gscqueries
```

Raw data location:

```text
data/raw/gsc_daily_request.csv
```

### Legacy field mapping

| Legacy field | Legacy type | Canonical field | Canonical type | Notes |
|---|---|---|---|---|
| `date` | DATE | `date` | DATE | GSC performance date. |
| `query` | STRING | `query` | STRING | Search query. |
| `is_branded` | BOOL | Optional derived field | BOOL | TRUE when the query contains a known brand term, such as `airwallex`. |
| `landing_page` | STRING | `url` | STRING | Landing page URL. |
| `gsc_clicks` | INT64 | `clicks` | INT64 | Organic clicks from Google Search. |
| `gsc_impressions` | INT64 | `impressions` | INT64 | Organic impressions from Google Search. |
| `gsc_ctr_pct` | FLOAT64 | `ctr` | FLOAT64 | Click-through rate. |
| `gsc_avg_position` | FLOAT64 | `position` | FLOAT64 | Average ranking position. |
| `gsc_reporting_region` | STRING | `country` | STRING | Searcher country or market. |
| `gsc_device_category` | STRING | `device` | STRING | Device type. |

### Naming decision

The initial table used explicit `gsc_` prefixes for metric fields:

- `gsc_clicks`
- `gsc_impressions`
- `gsc_ctr_pct`
- `gsc_avg_position`
- `gsc_reporting_region`
- `gsc_device_category`

This helped avoid confusion when joining the table with crawl, content audit, or AI visibility tables.

For the canonical project schema, I will use the standard table name `gscqueries` and the standard field names:

- `clicks`
- `impressions`
- `ctr`
- `position`
- `country`
- `device`

The legacy table remains useful as an earlier experiment, but future SQL, documentation, and pipeline work should use `gscqueries`.

### Partition and clustering

The canonical `gscqueries` table should be partitioned by `date` because most SEO diagnostics filter by reporting period.

The table should be clustered by `url` and `query` because most future analysis will group by landing page and search query.

### Optional branded field

`is_branded` is an optional derived field, not part of the core canonical schema.

If used later, it should be stored as `BOOL`.

Suggested definition:

```text
TRUE when the query contains a known brand term, such as airwallex.
```

---

## 1. gscqueries

### Purpose

`gscqueries` stores query-level Google Search Console performance data.

It answers: “For this search query, which URL appeared in Google Search, and how did it perform?”

This is the main table for keyword-level SEO analysis, including ranking opportunity, CTR opportunity, and query-to-page mapping.

### Grain

One row = one `date` + one `query` + one `url` + one `country` + one `device`.

Example:

| date | query | url | country | device |
|---|---|---|---|---|
| 2026-05-01 | what is bitcoin | /en/academy/articles/what-is-bitcoin | US | desktop |

### Source

Google Search Console export or Google Search Console Search Analytics API.

### Fields

| Field | Type | Definition |
|---|---|---|
| `date` | DATE | Date of the GSC performance record. |
| `query` | STRING | Search query typed by the user. |
| `url` | STRING | Landing page URL shown in Google Search. |
| `clicks` | INT64 | Organic clicks from Google Search for this query + URL. |
| `impressions` | INT64 | Number of times this query + URL appeared in search results. |
| `ctr` | FLOAT64 | Click-through rate, calculated as `clicks / impressions`. |
| `position` | FLOAT64 | Average Google ranking position for this query + URL. |
| `country` | STRING | Searcher country or market. |
| `device` | STRING | Device type, such as desktop, mobile, or tablet. |

### Main use cases

- Find top queries by clicks.
- Find high-impression queries with weak CTR.
- Find striking-distance queries ranking in positions 11 to 20.
- Map each query to the URL currently ranking for it.
- Identify query + URL pairs for `opportunityscores`.

### Priority rules

A query + URL pair is worth reviewing if it meets one or more of these conditions over the selected date range:

- `impressions >= 100`
- `clicks > 0`
- `position BETWEEN 11 AND 20`
- `ctr` is lower than expected for its position

---

## 2. gscpages

### Purpose

`gscpages` stores page-level Google Search Console performance data.

It answers: “How much organic search visibility does this URL already have, regardless of the individual queries?”

This table is used to decide whether a page has enough search demand to justify SEO work.

### Grain

One row = one `date` + one `url` + one `country` + one `device`.

Example:

| date | url | country | device |
|---|---|---|---|
| 2026-05-01 | /en/academy/articles/what-is-bitcoin | US | desktop |

### Source

Google Search Console export or Google Search Console Search Analytics API.

### Fields

| Field | Type | Definition |
|---|---|---|
| `date` | DATE | Date of the GSC performance record. |
| `url` | STRING | Page URL. |
| `clicks` | INT64 | Organic clicks received by this URL. |
| `impressions` | INT64 | Organic impressions received by this URL. |
| `ctr` | FLOAT64 | Page-level click-through rate, calculated as `clicks / impressions`. |
| `position` | FLOAT64 | Average ranking position for the page. |
| `country` | STRING | Searcher country or market. |
| `device` | STRING | Device type, such as desktop, mobile, or tablet. |

### Page-level demand definition

A URL has measurable page-level demand when it already receives meaningful visibility in Google Search.

For this project, a URL is treated as a priority page if it meets one or more of these conditions over the selected date range, usually the last 90 days:

- `impressions >= 100`
- `clicks > 0`
- `position <= 30`
- `ctr` is lower than expected for its average position

### Why this matters

This prevents the project from prioritizing pages only because they have technical issues.

For example, a page with missing metadata but zero impressions is usually lower priority than a page with 2,000 impressions, average position 12, and weak CTR.

### Main use cases

- Identify URLs with existing organic search demand.
- Prioritize high-impression pages for technical checks.
- Find pages with clicks declining over time.
- Select URLs for crawling, content audit, internal linking, and AI visibility testing.
- Join with `crawlresults` to detect technical issues on pages that already matter.

---

## 3. crawlresults

### Purpose

`crawlresults` stores technical and on-page SEO data collected from a crawler.

It answers: “Is this URL technically healthy, indexable, and properly structured for SEO?”

This table connects search performance data with crawl diagnostics.

### Grain

One row = one crawled `url` at one `crawledat` timestamp.

Example:

| url | crawledat |
|---|---|
| /en/academy/articles/what-is-bitcoin | 2026-05-01 10:30:00 UTC |

### Source

Python crawler using `requests` and `BeautifulSoup`, or a crawler export such as Screaming Frog.

### Fields

| Field | Type | Definition |
|---|---|---|
| `url` | STRING | Crawled page URL. |
| `statuscode` | INT64 | HTTP status code, such as 200, 301, 404, or 500. |
| `title` | STRING | Page title tag. |
| `metadescription` | STRING | Meta description tag. |
| `h1` | STRING | Main H1 heading found on the page. |
| `canonical` | STRING | Canonical URL declared by the page. |
| `wordcount` | INT64 | Estimated body word count. |
| `schemafound` | BOOL | Whether structured data or JSON-LD was found. |
| `crawledat` | TIMESTAMP | Timestamp when the page was crawled. |

### Diagnostic flags

The table should be used to create clear technical flags:

| Flag | Rule |
|---|---|
| `non_200_status` | `statuscode != 200` |
| `missing_title` | `title IS NULL OR title = ''` |
| `missing_metadescription` | `metadescription IS NULL OR metadescription = ''` |
| `missing_h1` | `h1 IS NULL OR h1 = ''` |
| `missing_canonical` | `canonical IS NULL OR canonical = ''` |
| `thin_content` | `wordcount < 600` by project default; adjust by template type |
| `missing_schema` | `schemafound = FALSE` |

### Main use cases

- Find important GSC pages with non-200 status codes.
- Find high-impression pages missing titles, meta descriptions, H1s, canonicals, or schema.
- Detect thin pages using `wordcount`.
- Feed technical and content-quality signals into `contentgapscore`.
- Support later content audit, entity mapping, schema, and internal linking modules.

---

## 4. opportunityscores

### Purpose

`opportunityscores` stores ranked SEO opportunities at the URL + query level.

It answers: “Which query + URL pair should we work on first, and why?”

This is a derived table, not a raw input table.

It combines GSC performance, ranking upside, CTR gap, content gap, and crawl diagnostics into a prioritized SEO work queue.

### Grain

One row = one `url` + one `query` opportunity.

Example:

| url | query |
|---|---|
| /en/academy/articles/what-is-bitcoin | what is bitcoin |

### Source

Generated by SQL and Python from:

- `gscqueries`
- `gscpages`
- `crawlresults`
- `contentinventory`

### Fields

| Field | Type | Definition |
|---|---|---|
| `url` | STRING | Landing page connected to the opportunity. |
| `query` | STRING | Search query connected to the landing page. |
| `strikingdistancescore` | FLOAT64 | Normalized 0–1 score measuring ranking upside when a query ranks close to page one. |
| `ctrgapscore` | FLOAT64 | Normalized 0–1 score measuring how far actual CTR is below expected CTR for the ranking position. |
| `contentgapscore` | FLOAT64 | Normalized 0–1 score measuring whether the page has content, technical, or topical weaknesses. |
| `totalscore` | FLOAT64 | Final weighted opportunity score. |
| `recommendation` | STRING | Recommended SEO action based on the dominant opportunity signal. |

### strikingdistancescore definition

`strikingdistancescore` measures how close a query + URL pair is to page-one rankings.

A high score means the URL is already ranking near the top 10, but has not yet reached the first page.

Project rule:

- Eligible if `impressions >= 100`
- Main striking-distance band is `position BETWEEN 11 AND 20`
- Score range is 0 to 1
- Higher score = closer to position 10

Formula:

```sql
CASE
  WHEN impressions >= 100 AND position BETWEEN 11 AND 20
    THEN (21 - position) / 10
  ELSE 0
END AS strikingdistancescore
```

Example:

| Position | Impressions | Score |
|---:|---:|---:|
| 11 | 500 | 1.0 |
| 15 | 500 | 0.6 |
| 20 | 500 | 0.1 |
| 25 | 500 | 0.0 |
| 12 | 50 | 0.0 |

### ctrgapscore definition

`ctrgapscore` measures whether the query + URL gets fewer clicks than expected for its ranking position.

It compares actual CTR against an expected CTR benchmark.

Simple formula:

```sql
ctrgapscore =
  GREATEST(expected_ctr - actual_ctr, 0) / expected_ctr
```

Project rule:

- Eligible if `impressions >= 100`
- Score range is 0 to 1
- Higher score = bigger CTR underperformance
- Score should be 0 if actual CTR is equal to or higher than expected CTR

Example:

| Position | Expected CTR | Actual CTR | Score |
|---:|---:|---:|---:|
| 5 | 0.08 | 0.04 | 0.50 |
| 8 | 0.04 | 0.01 | 0.75 |
| 12 | 0.02 | 0.02 | 0.00 |

Use this signal when the page is already visible but the title, meta description, or SERP positioning may be weak.

### contentgapscore definition

`contentgapscore` measures whether the page has content, technical, or topical weaknesses that may limit ranking growth.

It uses signals from `crawlresults` and `contentinventory`.

Recommended project default:

| Issue | Points |
|---|---:|
| Missing H1 | 1 |
| Missing title | 1 |
| Missing meta description | 1 |
| Missing canonical | 1 |
| Missing schema | 1 |
| Thin content, default `wordcount < 600` | 1 |
| Stale content, default `lastupdated > 365 days ago` | 1 |
| Weak topic match between `query` and `primarytopic` | 1 |

Formula:

```sql
contentgapscore = issue_points / total_possible_points
```

Example:

| Issue points | Total possible points | Score |
|---:|---:|---:|
| 2 | 8 | 0.25 |
| 4 | 8 | 0.50 |
| 7 | 8 | 0.875 |

### totalscore definition

`totalscore` is the final weighted SEO opportunity score.

Formula:

```sql
totalscore =
  0.4 * strikingdistancescore +
  0.3 * ctrgapscore +
  0.3 * contentgapscore
```

The score ranges from 0 to 1.

Higher scores mean the URL + query pair is more attractive for SEO action.

### Recommendation logic

| Dominant signal | Condition | Recommendation |
|---|---|---|
| Striking distance | High `strikingdistancescore` | Add internal links, improve headings, refresh query targeting. |
| CTR gap | High `ctrgapscore` | Rewrite title tag and meta description. |
| Content gap | High `contentgapscore` | Refresh content, add missing sections, improve structure. |
| Technical issue | Non-200 status, missing canonical, missing H1 | Fix technical/on-page issue first. |
| Schema gap | `schemafound = FALSE` | Add suitable structured data. |
| Intent mismatch | Query does not match `primarytopic` | Create a new page or remap the query to a better page. |
| YMYL/compliance risk | Crypto or financial claim needs review | Send to compliance review before publishing. |

### Example output

| url | query | strikingdistancescore | ctrgapscore | contentgapscore | totalscore | recommendation |
|---|---|---:|---:|---:|---:|---|
| /en/academy/articles/what-is-bitcoin | what is bitcoin | 1.00 | 0.20 | 0.25 | 0.535 | Add internal links and improve query targeting. |
| /en/academy/articles/crypto-wallet | best crypto wallet | 0.60 | 0.75 | 0.50 | 0.615 | Rewrite title/meta and refresh content. |
| /en/academy/articles/proof-of-reserves | proof of reserves | 0.20 | 0.10 | 0.875 | 0.3725 | Refresh content and add schema. |

---

## 5. contentinventory

### Purpose

`contentinventory` stores manual content metadata for each URL.

It answers: “What is this page about, who is it for, and how should it be grouped?”

This table gives the SEO system context that is not available from GSC or crawler data alone.

### Grain

One row = one canonical `url`.

Example:

| url |
|---|
| /en/academy/articles/what-is-bitcoin |

### Source

Manual CSV seed, enriched over time by content audit, entity mapping, and internal linking workflows.

### Fields

| Field | Type | Definition |
|---|---|---|
| `url` | STRING | Canonical page URL. |
| `language` | STRING | Page language, such as `en`, `zh-Hant`, or `zh-Hans`. |
| `market` | STRING | Target market, such as HK, SG, AU, UK, US, or Global. |
| `contenttype` | STRING | Page type, such as guide, glossary, blog, product page, academy article, or landing page. |
| `primarytopic` | STRING | Main topic, entity, or keyword theme of the page. |
| `lastupdated` | DATE | Date when the content was last updated. |

### Controlled values

Recommended controlled values:

| Field | Example values |
|---|---|
| `language` | `en`, `zh-Hant`, `zh-Hans` |
| `market` | `HK`, `SG`, `AU`, `UK`, `US`, `Global` |
| `contenttype` | `guide`, `glossary`, `blog`, `product`, `academy`, `landing_page` |
| `primarytopic` | `bitcoin`, `ethereum`, `crypto wallet`, `proof of reserves`, `trading fees` |

### Main use cases

- Group URLs by market and language.
- Segment content by page type.
- Map URLs to topics and entities.
- Check whether a query matches the page’s `primarytopic`.
- Support `contentgapscore`, internal linking, entity SEO, AI visibility testing, and RAG retrieval.

---

# Table relationships

The five canonical tables connect through shared `url` and `query` fields.

## Main joins

| Join | Purpose |
|---|---|
| `gscqueries.url = gscpages.url` | Connect query-level and page-level performance. |
| `gscqueries.url = crawlresults.url` | Check technical issues for ranking query + URL pairs. |
| `gscpages.url = crawlresults.url` | Check technical issues for important pages. |
| `gscqueries.url = contentinventory.url` | Add language, market, content type, and topic to query data. |
| `gscpages.url = contentinventory.url` | Add content metadata to page-level performance. |
| `opportunityscores.url = gscqueries.url` | Tie final opportunity score back to GSC performance. |
| `opportunityscores.query = gscqueries.query` | Tie final opportunity score back to the search query. |

## Analysis workflow

1. Use `gscqueries` to find high-impression query + URL pairs.
2. Use `gscqueries` to identify striking-distance rankings where `position BETWEEN 11 AND 20` and `impressions >= 100`.
3. Use `gscpages` to confirm the URL has page-level search demand, such as `impressions >= 100`, `clicks > 0`, or `position <= 30`.
4. Use `crawlresults` to check for technical or on-page problems.
5. Use `contentinventory` to add market, language, content type, and topic context.
6. Write the final ranked URL + query opportunity into `opportunityscores`.

---