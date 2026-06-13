# M1W7 Opportunity Scoring Model

## Objective

This scoring model ranks SEO opportunities at the URL-query level by combining Google Search Console performance data with crawl-based page signals.

The goal is to identify pages that already have search demand and ranking visibility, but still have clear optimization gaps such as weak rankings, low CTR, missing metadata, thin content, missing structured data, or weak internal linking.

This model is designed for the M1 SEO data pipeline. It starts with practical SEO signals that are already available from Google Search Console and crawl results. Future AI Search and Google AIO readiness signals can be added later as an overlay, but they should not replace the core SEO opportunity model.

---

## Inputs

### Google Search Console Table

Source table:

```text
project-5d19c72c-351f-4c80-8fc.seo_diagnostic.gscqueries
```

Core fields:

- `date`
- `url`
- `query`
- `clicks`
- `impressions`
- `ctr`
- `positions`
- `country`
- `device`
- `isbranded`

Purpose:

- Measure search demand.
- Identify URL-query pairs with impressions.
- Detect rankings close to page one.
- Detect low CTR opportunities.
- Prioritize non-branded queries.
- Find pages that already show topical relevance.

### Crawl Results Table

Source table:

```text
seo_diagnostic.crawlresults
```

Core fields:

- `url`
- `statuscode`
- `title`
- `h1`
- `metadescription`
- `canonical`
- `wordcount`
- `schemafound`
- `crawledat`

Purpose:

- Detect crawl and indexability issues.
- Detect missing or weak on-page elements.
- Identify thin content.
- Identify missing structured data.
- Support content gap scoring.

---

## Scoring Overview

The opportunity score is built from three main SEO components in M1.

| Component | Purpose | Initial Weight |
|---|---:|---:|
| Striking Distance Score | Find non-branded URL-query pairs close to page one | 40% |
| CTR Gap Score | Find pages with weak click performance | 30% |
| Content Gap Score | Find on-page and technical weaknesses | 30% |

Initial formula:

```text
total_score_v1 =
  0.40 * striking_distance_score +
  0.30 * ctr_gap_score +
  0.30 * content_gap_score
```

The final score should be normalized to a 0-100 scale.

Google AIO readiness can be added later as a separate overlay, but the M1 production scoring model should remain based on measurable GSC and crawl signals.

---

## 1. Striking Distance Score

A striking distance opportunity is a non-branded URL-query pair where the page already ranks near page one but is not yet in the top results.

For the current `q09_striking_distance.sql` implementation, the model focuses on query-page pairs with meaningful impressions and weighted average position between 11 and 20.

### Current Criteria

A URL-query pair qualifies as a striking distance opportunity when all of the following criteria are met:

- `query` is not null.
- `query` is not empty after trimming whitespace.
- `url` is not null.
- `url` is not empty after trimming whitespace.
- `isbranded IS FALSE`.
- Total impressions are greater than or equal to 100.
- Weighted average position is between 11 and 20.
- The result is grouped at URL-query level.
- The output is ordered by opportunity score, impressions, and clicks.

### Why branded queries are excluded

Branded queries are excluded because they usually reflect existing brand demand rather than new SEO growth opportunity.

For this project, the scoring model should prioritize non-branded queries because they are more useful for identifying content, ranking, CTR, and acquisition opportunities.

The confirmed SQL filter is:

```sql
AND isbranded IS FALSE
```

This is intentionally stricter than using `COALESCE(isbranded, FALSE) = FALSE`.

If `isbranded` is null, the query is excluded from this specific scoring output because the model only wants confirmed non-branded queries.

### Weighted Average Position

Average position should be calculated using impression-weighted ranking, not a simple average.

Confirmed logic:

```sql
SAFE_DIVIDE(SUM(positions * impressions), SUM(impressions)) AS avg_position
```

This gives more weight to rows with higher impression volume.

For example, if a query-page pair has one row with 1,000 impressions at position 12 and another row with 5 impressions at position 20, the position 12 row should influence the final average much more strongly.

### SQL Qualification Logic

The confirmed striking distance filter is:

```sql
WHERE
  impressions >= 100
  AND avg_position BETWEEN 11 AND 20
```

This means the model only includes query-page pairs that have enough demand and are close enough to the first page to be actionable.

### Opportunity Score Formula

The current striking distance opportunity score is:

```text
opportunity_score = impressions * (21 - avg_position) / 10
```

Score direction:

- Higher impressions increase the opportunity score.
- Position 11 receives a higher score than position 20.
- Position 20 still qualifies but receives a lower score.
- Queries outside positions 11-20 are excluded from this specific SQL output.
- Queries with fewer than 100 impressions are excluded from this specific SQL output.

### Current Criteria Table

| Criteria | Current Setting |
|---|---|
| Data source | `seo_diagnostic.gscqueries` |
| Output level | URL-query pair |
| Query cleanup | Query must not be null or empty |
| URL cleanup | URL must not be null or empty |
| Brand filter | `isbranded IS FALSE` |
| Impression threshold | `impressions >= 100` |
| Position band | `avg_position BETWEEN 11 AND 20` |
| Position method | Impression-weighted average position |
| CTR method | `SAFE_DIVIDE(SUM(clicks), SUM(impressions))` |
| Opportunity formula | `impressions * (21 - avg_position) / 10` |
| Output limit | Top 200 opportunities |

### Rationale

The URL already has topical relevance because it is receiving impressions for the query.

The query already has search demand because it has at least 100 impressions.

The page is close enough to page one that content, metadata, internal linking, or technical improvements may help move it into stronger ranking positions.

These opportunities are usually more actionable than pages with no impressions or queries ranking far outside the top results.

### Recommended Actions

Possible actions for striking distance opportunities:

- Refresh or expand the target page content.
- Improve the page title.
- Improve the meta description.
- Add internal links from relevant supporting pages.
- Add FAQ content where the query has informational intent.
- Add comparison content where the query has comparison intent.
- Add structured data where relevant.
- Improve above-the-fold answer clarity.
- Strengthen topical depth around the query intent.

---

## 2. CTR Gap Score

CTR gap estimates whether a page is underperforming relative to its ranking position.

A query-page pair can have strong impressions and reasonable rankings but still receive weak clicks if the title, meta description, intent match, or SERP positioning is poor.

### CTR Gap Criteria

A URL-query pair may qualify as a CTR gap opportunity when:

- The query is non-branded.
- The URL and query are valid.
- Impressions are meaningful.
- Average position is strong enough for CTR to matter.
- CTR is lower than expected for the ranking range.

### Initial Rules

High CTR gap:

```text
impressions >= 100
avg_position <= 10
ctr < 0.02
```

Medium CTR gap:

```text
impressions >= 100
avg_position BETWEEN 11 AND 20
ctr < 0.01
```

Low CTR gap:

```text
impressions < 100
or avg_position is too low to estimate CTR reliably
```

### Example SQL Pattern

```sql
CASE
  WHEN impressions >= 100 AND avg_position <= 10 AND ctr < 0.02 THEN 100
  WHEN impressions >= 100 AND avg_position BETWEEN 11 AND 20 AND ctr < 0.01 THEN 70
  WHEN impressions >= 100 THEN 40
  ELSE 10
END AS ctr_gap_score
```

### Rationale

A page ranking in positions 1-10 with weak CTR may be a quick-win title and meta description opportunity.

A page ranking in positions 11-20 with very low CTR may need both ranking improvement and stronger snippet relevance.

CTR gap should be interpreted carefully because CTR varies by query intent, SERP features, brand familiarity, and ranking position.

### Recommended Actions

Possible actions for CTR gap opportunities:

- Rewrite the title tag.
- Rewrite the meta description.
- Add stronger intent alignment.
- Add clearer value proposition.
- Add pricing, feature, or trust signals where relevant.
- Improve snippet clarity.
- Add FAQ or structured data where relevant.
- Check whether the page matches the search intent behind the query.

---

## 3. Content Gap Score

Content gap score uses crawl signals to estimate whether a page has on-page or technical weaknesses.

This component helps explain why a URL-query pair may be underperforming despite having impressions.

### Content Gap Signals

Content gap signals include:

- Missing H1.
- Weak or empty H1.
- Missing meta description.
- Weak or empty meta description.
- Low word count.
- Missing structured data.
- Non-200 status code.
- Canonical issue.
- Weak title.
- Duplicate or unclear page purpose.
- Page not crawled.

### Initial Rules

Example content gap checks:

```sql
CASE WHEN h1 IS NULL OR TRIM(h1) = '' THEN 1 ELSE 0 END AS missing_h1

CASE WHEN metadescription IS NULL OR TRIM(metadescription) = '' THEN 1 ELSE 0 END AS missing_meta_description

CASE WHEN wordcount < 500 THEN 1 ELSE 0 END AS thin_content

CASE WHEN schemafound IS FALSE THEN 1 ELSE 0 END AS missing_schema

CASE WHEN statuscode != 200 THEN 1 ELSE 0 END AS technical_issue
```

### Example Scoring Logic

```text
content_gap_score =
  20 * missing_h1 +
  20 * missing_meta_description +
  20 * thin_content +
  20 * missing_schema +
  20 * technical_issue
```

This produces a simple 0-100 content gap score.

A higher score means the page has more visible on-page or technical weaknesses.

### Recommended Actions

Possible actions for content gap opportunities:

- Add or improve the H1.
- Rewrite the meta description.
- Improve thin content.
- Add relevant structured data.
- Fix non-200 status issues.
- Fix canonical issues.
- Improve content structure.
- Add supporting sections for related subtopics.
- Add internal links to and from relevant pages.

---

## 4. Final Opportunity Score

The M1 opportunity score combines striking distance, CTR gap, and content gap.

### Version 1: M1 Basic SEO Score

Use this version for the first working opportunity scoring model.

```text
total_score_v1 =
  0.40 * striking_distance_score +
  0.30 * ctr_gap_score +
  0.30 * content_gap_score
```

Use this version when AIO or AI visibility signals are not yet available.

### Version 2: SEO + AIO Readiness Overlay

Use this version later when basic crawl data and AIO readiness checks are available.

```text
total_score_v2 =
  0.35 * striking_distance_score +
  0.25 * ctr_gap_score +
  0.25 * content_gap_score +
  0.15 * aio_readiness_score
```

This should be treated as an overlay, not as a replacement for the M1 production score.

### Version 3: AI Search / GEO Score

Use this in later modules when AI visibility tracking exists.

```text
total_score_v3 =
  0.25 * striking_distance_score +
  0.20 * ctr_gap_score +
  0.20 * content_gap_score +
  0.20 * aio_readiness_score +
  0.15 * ai_visibility_gap_score
```

Future AI visibility signals may include:

- Brand mentioned in AI answer.
- URL cited by AI answer.
- Competitor cited instead of the target brand.
- Citation count.
- Source quality.
- Market and language visibility.
- Query intent coverage.

---

## 5. Google AIO Readiness Overlay

Google AIO readiness estimates whether a page is suitable for AI Overview-style retrieval, summarization, and citation.

This is not a guarantee of inclusion in Google AI Overviews.

It is a practical readiness layer for checking whether the page has clear structure, entity clarity, direct answers, trust signals, and supporting content.

### Important Limitation

The current M1 model does not measure actual Google AI Overview citations.

The current model does not confirm whether Google AI Overviews cite a URL.

AIO readiness should therefore be treated as a future-facing content quality and structure overlay, not as observed AIO performance data.

### AIO Readiness Signals

Potential AIO readiness signals:

- Clear direct answer near the top of the page.
- Strong entity coverage.
- Clear topic definition.
- FAQ or QA structure.
- Source-backed factual claims.
- Updated date or last reviewed date.
- Clear author, reviewer, or editorial signals.
- Structured data.
- Internal links to supporting pages.
- Consistent terminology across related pages.
- Canonical and indexable URL.
- No major technical crawl issue.

### Practical AIO Checks

For each URL, check:

```text
Does the page answer the main query clearly in the first section?
Does the page define the main entity?
Does the page cover related subtopics?
Does the page include FAQ or QA style content?
Does the page include factual claims with sources?
Does the page include structured data?
Does the page have a clear author, reviewer, or editorial signal?
Does the page internally link to related supporting content?
Does the page have enough content depth?
Is the page crawlable and indexable?
```

### Initial AIO Readiness Scoring

Example scoring logic:

```text
aio_readiness_score =
  15 * has_direct_answer_block +
  15 * has_entity_definition +
  15 * has_faq_or_qa_structure +
  15 * has_structured_data +
  15 * has_source_backed_claims +
  10 * has_author_or_reviewer_signal +
  10 * has_supporting_internal_links +
  5  * has_recent_update_signal
```

Normalize to a 0-100 scale.

### AIO Weakness Examples

High AIO weakness:

- The page ranks but does not directly answer the query.
- The page has no clear entity definition.
- The page has no FAQ or question-answer structure.
- The page makes factual claims without sources.
- The page has no structured data.
- The page has weak internal links.
- The page has no author, reviewer, or update signal.

Medium AIO weakness:

- The page has useful content but poor structure.
- The page has entities but no clear definitions.
- The page has some internal links but weak topical support.
- The page has schema but missing recommended fields.

Low AIO weakness:

- The page has a clear answer.
- The page has strong entity coverage.
- The page has structured data.
- The page has sources.
- The page has strong internal links.
- The page is technically clean.

---

## 6. Query Intent Layer

Different query intents should receive different scoring treatment.

| Intent | Example | SEO Focus | AIO Focus |
|---|---|---|---|
| Informational | what is a multi-currency business account | Clear answer and entity definition | High |
| Comparison | Airwallex vs Wise for business | Structured comparison | High |
| How-to | how to open an Airwallex business account | Step-by-step content | High |
| Commercial | best global business account for startups | Trust, pricing, compliance, comparison | Medium |
| Branded | Airwallex pricing | Accuracy and freshness | Medium |
| Navigational | Airwallex login | Technical and UX | Low |

AIO readiness should be more important for informational, comparison, and how-to queries because these queries often need summarization, explanation, or multi-step reasoning.

Suggested intent adjustment:

```text
if intent in informational, comparison, how-to:
  aio_weight = 0.20

if intent in commercial, branded:
  aio_weight = 0.10

if intent is navigational:
  aio_weight = 0.05
```

For the confirmed M1 non-branded scoring model, branded and navigational terms should generally be excluded from the main opportunity shortlist.

---

## 7. Recommended Actions

Each opportunity should map to one main recommended action.

### SEO Recommendations

- Refresh content.
- Rewrite title and meta description.
- Add internal links.
- Add FAQ content.
- Add structured data.
- Fix canonical issue.
- Improve thin content.
- Fix crawl or indexing issue.
- Improve page intent match.

### Google AIO Recommendations

- Add direct answer block.
- Add FAQ section.
- Add entity definition.
- Add comparison table.
- Add step-by-step explanation.
- Add source citations.
- Add author or reviewer signal.
- Add Article or FAQPage schema.
- Add supporting internal links.
- Update outdated factual claims.
- Improve topical completeness.

### Airwallex B2B Fintech Content Recommendations

- Clarify product positioning for global business accounts.
- Explain multi-currency account use cases.
- Add transparent pricing and fee explanation where relevant.
- Add comparison sections against common alternatives.
- Add trust, compliance, and security context.
- Add regional relevance for Hong Kong, Singapore, Australia, the UK, and the US where relevant.
- Add examples for startups, ecommerce, SaaS, and cross-border businesses.
- Add internal links between business account, payments, FX, cards, and expense management pages.

### Technical Recommendations

- Fix non-200 status.
- Fix canonical mismatch.
- Improve crawlability.
- Add structured data.
- Improve sitemap coverage.
- Check robots directives.
- Check meta robots directives.
- Check indexability.

---

## 8. Output Table

Target BigQuery table:

```text
seo_diagnostic.opportunityscores
```

Initial proposed fields:

- `url`
- `query`
- `striking_distance_score`
- `ctr_gap_score`
- `content_gap_score`
- `aio_readiness_score`
- `total_score`
- `recommendation`
- `recommendation_type`
- `reason`
- `priority`

Recommended `recommendation_type` values:

- `content_refresh`
- `title_meta_rewrite`
- `internal_linking`
- `schema_addition`
- `aio_readiness`
- `technical_fix`
- `canonical_fix`
- `thin_content_fix`
- `indexing_review`
- `b2b_fintech_trust`
- `pricing_clarity`
- `comparison_content`

---

## 9. Example Cases

### Example 1: Striking Distance Opportunity

A URL-query pair may become a high-priority SEO opportunity if:

- It is non-branded.
- It has at least 100 impressions.
- Weighted average position is between 11 and 20.
- CTR is low.
- The page has weak metadata or missing schema.

Recommended action:

```text
Refresh content, improve title and meta description, and add internal links to help push the page from page two to page one.
```

### Example 2: CTR Gap Opportunity

A URL-query pair may become a high-priority CTR opportunity if:

- It is non-branded.
- It ranks in positions 1-10.
- It has strong impressions.
- CTR is lower than expected.
- The title does not match query intent.

Recommended action:

```text
Rewrite title and meta description to better match user intent and improve snippet appeal.
```

### Example 3: Google AIO Readiness Opportunity

A URL-query pair may become a high-priority AIO readiness opportunity if:

- It has strong impressions.
- It targets an informational, comparison, or how-to query.
- It lacks a direct answer block.
- It lacks FAQ or QA structure.
- It has weak entity definitions.
- It has no supporting sources.
- It has missing structured data.

Recommended action:

```text
Add a concise answer block, entity definition, FAQ section, supporting citations, and relevant structured data.
```

### Example 4: Airwallex B2B Fintech Opportunity

A URL-query pair may become a high-priority Airwallex-style opportunity if:

- It targets global business account, international payment, FX, or expense management intent.
- It has impressions but ranks outside the top 10.
- It lacks a clear comparison against alternatives.
- It does not explain pricing, fees, trust, compliance, or regional availability clearly.
- It has weak internal links to related product pages.

Recommended action:

```text
Improve the page with clearer product positioning, pricing context, comparison content, trust signals, and internal links to related Airwallex product pages.
```

### Example 5: Technical SEO Opportunity

A URL-query pair may become a technical priority if:

- It has impressions.
- It has ranking potential.
- It has non-200 status.
- It has canonical mismatch.
- It is missing from important internal links.

Recommended action:

```text
Fix crawl and indexability issues before investing in content optimization.
```

---

## 10. Implementation Plan

### M1W7D1: Create scoring model document

Expected file:

```text
docs/scoringmodel.md
```

Purpose:

- Define scoring components.
- Define criteria.
- Define opportunity output fields.
- Document how SQL and Python scoring should work.

### M1W7D2: Create BigQuery striking distance SQL

Expected file:

```text
sql/q09_striking_distance.sql
```

Current implementation criteria:

- Group by URL and query.
- Exclude null query values.
- Exclude empty query values.
- Exclude null URL values.
- Exclude empty URL values.
- Exclude branded queries with `isbranded IS FALSE`.
- Use total impressions.
- Use total clicks.
- Calculate CTR with `SAFE_DIVIDE`.
- Calculate weighted average position with `SAFE_DIVIDE(SUM(positions * impressions), SUM(impressions))`.
- Keep query-page pairs with `impressions >= 100`.
- Keep query-page pairs with weighted average position between 11 and 20.
- Calculate opportunity score with `impressions * (21 - avg_position) / 10`.
- Order by opportunity score, impressions, and clicks.
- Limit output to 200 rows.

Expected output fields:

- `url`
- `query`
- `clicks`
- `impressions`
- `ctr_percent`
- `avg_position`
- `opportunity_score`

### M1W7D3: Create Python scoring script

Expected file:

```text
src/scoreopportunities.py
```

Purpose:

- Load GSC data.
- Load crawl data.
- Merge by URL.
- Calculate scoring components.
- Output opportunity scores.
- Prepare top opportunities for reporting.

### M1W7D4: Export top opportunities

Expected file:

```text
outputs/top50opportunities.csv
```

Expected fields:

- `url`
- `query`
- `score`
- `reason`
- `recommended_action`
- `priority`

### M1W7D5: Update README and pitch section

Purpose:

- Explain the scoring logic.
- Show top opportunity examples.
- Document how the model works.
- Commit and tag the milestone.

---

## 11. Notes

This model starts with practical SEO signals because GSC and crawl data are already available.

The confirmed M1 striking distance SQL should only include non-branded queries.

Google AIO readiness is included as a future-facing overlay so that the system does not become a traditional SEO-only workflow.

However, AIO readiness should not be treated as observed Google AI Overview citation data unless a future module collects SERP-level or AI Overview citation evidence.

The first production version should remain simple, explainable, and easy to validate:

```text
non-branded query + meaningful impressions + position 11-20 + crawl-based issue = actionable SEO opportunity
```