# M1W7 Opportunity Score Pitch

## Executive pitch

This module turns Google Search Console query-level data into a prioritized SEO opportunity list.

The scoring logic focuses on non-branded URL-query combinations with existing search demand, striking-distance rankings, and clear optimization actions.

The output is designed for SEO prioritization: which page to improve, which query to target, why it matters, and what action should be taken next.

## Top 3 opportunities

| Rank | URL | Query | Impressions | Avg Position | Opportunity Score | Recommended Action |
|---:|---|---|---:|---:|---:|---|
| 1 | https://www.airwallex.com/hk-zh/blog/remittance-to-mainland-china | 大陸匯款到香港限制 | 64 | 11.78 | 61.5 | Refresh content and rewrite title/meta |
| 2 | https://www.airwallex.com/hk-zh/blog/business-registration-certificate | 商業登記處派籌時間 | 35 | 11.0 | 35.0 | Improve content depth and internal links |
| 3 | https://www.airwallex.com/hk/blog/dbs-open-account | dbs business account | 36 | 11.75 | 34.64 | Refresh content and rewrite title/meta |

## How to read this output

- High opportunity scores indicate URL-query pairs with meaningful impressions and rankings close enough to improve.
- Queries in positions 11-30 are treated as striking-distance or lower-page opportunities.
- Recommended actions translate the score into practical SEO next steps, such as content refreshes, title/meta improvements, internal linking, or topical expansion.

## Portfolio value

This is a practical SEO data product rather than a static report.

It combines BigQuery, Python, pandas, and GSC-derived metrics to move from raw search data to prioritised recommendations.

In later modules, this output can feed content audits, internal linking, AI visibility checks, and Google AIO readiness analysis.
