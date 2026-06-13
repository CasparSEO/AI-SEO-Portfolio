# SEO Opportunity Scoring Model v2

This document defines a practical SEO opportunity scoring model for the AI SEO Portfolio project. It is designed to rank page-query opportunities using currently available data sources in the repository: Google Search Console performance data, lightweight crawl diagnostics, and manually reviewed content signals.[1]

The model is intentionally split into a production scoring layer and an experimental AI-readiness layer. This keeps the workflow usable today while making room for future AI visibility and Google AI Overview measurement work in later modules.[1][2][3]

## Purpose

The goal of this model is to prioritize SEO opportunities that are both actionable and measurable. In the current project phase, the most reliable inputs are GSC query-page performance data, crawl-based page diagnostics, and a small amount of manual review.[1]

This model supports three portfolio needs:

- Ranking opportunities into a short list for execution.[1]
- Showing a clear logic for why one URL-query pair matters more than another.[1]
- Demonstrating how traditional SEO scoring can evolve toward AI Search / GEO thinking without overstating current measurement capabilities.[1][4]

## Data sources

The current repository and workflow already use a BigQuery-backed SEO diagnostic setup with core tables such as `gscqueries`, `gscpages`, `crawlresults`, and `opportunityscores`.[1]

The scoring model draws from the following inputs:

| Input | What it provides | Current status |
|---|---|---|
| `seodiagnostic.gscqueries` | Query, URL, clicks, impressions, CTR, average position, branded vs non-branded | Production-ready.[1] |
| `crawlresults` | Status code, title, meta description, H1, canonical, word count, schema presence | Available from lightweight crawl workflow.[1] |
| Manual content review | Answer-first structure, FAQ presence, source-backed claims, update freshness | Small-sample only.[1] |
| SERP / AI Overview observation | Whether a query triggers AIO and whether the domain is cited | Not yet integrated programmatically.[2][5][4] |

## Model layers

The model is divided into three layers so that current implementation and future expansion remain separate and transparent.[1]

### Layer 1: Base opportunity score

This is the main production scoring layer. It uses data that already exists in the portfolio workflow and can be refreshed with SQL and Python today.[1]

The base score combines three components:

- Striking distance score: high-impression query-URL pairs ranking around positions 11-20.[1]
- CTR gap score: query-URL pairs with strong impressions and acceptable rank but weak click-through rate.[1]
- Content gap score: pages that show weaker on-page support signals such as thin copy, missing schema, weak title/H1 alignment, or missing FAQ-like structure.[1]

A practical base formula is:

$$
\text{Base Opportunity Score} = 0.40 \times \text{Striking Distance Score} + 0.35 \times \text{CTR Gap Score} + 0.25 \times \text{Content Gap Score}
$$

This base model is the recommended scoring logic for current portfolio outputs such as `top50_opportunities.csv`, SQL shortlist tables, and diagnostic reporting.[1]

### Layer 2: AIO readiness overlay

This layer does not measure real Google AI Overview citation visibility. Instead, it estimates whether a page is structurally likely to be easier for AI systems to interpret, summarize, and potentially cite in the future.[6][7][3]

This distinction matters because crawling a website can reveal on-page structure, but it cannot reveal whether Google actually cited that page inside AI Overviews. Real citation visibility requires SERP-level observation or specialized monitoring workflows.[2][5][4]

The AIO readiness overlay can use signals such as:

- Presence of a direct answer block near the top of the page.
- Clear entity definition or category explanation.
- FAQ or Q-and-A structure.
- Structured data presence.
- Source-backed factual claims.
- Author, reviewer, or editorial trust signals.
- Helpful internal links to supporting pages.
- Freshness or visible update indicators.[1]

A simple readiness formula is:

$$
\text{AIO Readiness Score} = 15a + 15b + 15c + 15d + 15e + 10f + 10g + 5h
$$

Where:

- `a` = has direct answer block (0 or 1)
- `b` = has entity definition (0 or 1)
- `c` = has FAQ or Q-and-A structure (0 or 1)
- `d` = has structured data (0 or 1)
- `e` = has source-backed claims (0 or 1)
- `f` = has author or reviewer signal (0 or 1)
- `g` = has supporting internal links (0 or 1)
- `h` = has recent update signal (0 or 1)[1]

This produces a 0-100 score when all components are summed directly.[1]

At the current stage of the portfolio, this layer should be treated as a qualitative overlay or small-sample enhancement, not as the primary ranking engine.[2][4]

### Layer 3: Future AI visibility measurement

A later version of this project can add real AI visibility inputs, such as whether a query triggers AI Overviews, whether the brand is cited, what citation format appears, and which competitor domains are also shown.[1][8][3]

This layer belongs more naturally to the AI visibility / GEO phase of the roadmap rather than the current scoring workflow.[1]

## Component definitions

### Striking distance score

This score captures ranking upside. It focuses on query-URL pairs that already have meaningful impressions and sit just outside the top positions, especially positions 11-20.[1]

Example logic:

- Require impressions above a minimum threshold such as 100.[1]
- Focus on non-branded terms where possible using `isbranded`.[1]
- Give higher scores to URLs closer to position 11 than 20.[1]

A simple scaled version:

$$
\text{Striking Distance Score} = \min\left(100, \frac{\text{impressions}}{10}\right) \times \frac{21 - \text{avg position}}{10}
$$

### CTR gap score

This score captures underperformance in snippet appeal or mismatch between intent and page presentation. A query can rank reasonably well and still deserve action if the click-through rate is weaker than expected for its position band.[1]

Example inputs:

- Impressions.
- Current CTR.
- Average position.
- Position bucket benchmark CTR, whether estimated manually or calculated from your own data.[1]

One workable concept is:

$$
\text{CTR Gap Score} = \text{impressions weight} \times (\text{expected CTR} - \text{actual CTR})
$$

Where negative values are floored at zero.[1]

### Content gap score

This score reflects whether the page appears weak or incomplete relative to the query opportunity. It can use crawl-based signals first, then later expand to LLM-assisted audits.[1]

Useful signals include:

- Thin or low-depth content proxy such as low word count.[1]
- Missing schema.[1]
- Weak title and H1 relevance.[1]
- Missing FAQ-style support content.[1]
- Weak internal linking support.[1]

An example rule-based model:

| Signal | Condition | Score effect |
|---|---|---|
| Thin content | Low word count or shallow template page | +25 [1] |
| Missing schema | No schema found | +20 [1] |
| Weak title/H1 alignment | Title or H1 missing query theme | +20 [1] |
| Missing FAQ support | No FAQ or answer-style support | +20 [1] |
| Weak internal support | Few related internal links | +15 [1] |

The score can then be capped at 100.[1]

## Recommended production formula

For the current repo stage, the safest production formula is:

$$
\text{Total Score v1} = 0.40 \times \text{Striking Distance Score} + 0.35 \times \text{CTR Gap Score} + 0.25 \times \text{Content Gap Score}
$$

This version is fully aligned with the data model already present in the repository and with the workflow built around GSC exports, crawl results, SQL analysis, and opportunity ranking.[1]

## Experimental formula with AIO readiness

A future-ready but currently non-production formula can be documented as:

$$
\text{Total Score v2} = 0.35 \times \text{Striking Distance Score} + 0.25 \times \text{CTR Gap Score} + 0.25 \times \text{Content Gap Score} + 0.15 \times \text{AIO Readiness Score}
$$

This should be used only when the AIO readiness score has been manually reviewed or generated consistently for the evaluated sample.[1][2]

For now, the project should avoid presenting this as a fully automated production score because the model does not yet include observed AI Overview citation data from SERP monitoring.[2][5][4]

## Query intent adjustment

The model can become more realistic by adjusting weights based on query intent.[1]

| Intent type | Suggested use of AIO readiness | Reason |
|---|---|---|
| Informational / how-to | Higher | AI systems often favor concise explainers, structured answers, and source-backed educational content.[6][7] |
| Comparison / alternative | Medium to high | Comparative queries may surface synthesized answers and source cards.[7][3] |
| Commercial | Medium | Snippet and conversion intent still matter, but AIO influence may vary.[7] |
| Navigational / login | Low | These terms are usually not strong candidates for AIO-driven opportunity scoring.[1] |

This means the AIO readiness overlay is most useful for non-branded informational and comparison queries.[1][3]

## Output design

The `opportunityscores` output should remain simple and auditable. A recommended table or CSV structure is:[1]

| Column | Description |
|---|---|
| `url` | Landing page URL.[1] |
| `query` | Search query.[1] |
| `clicks` | Aggregated clicks.[1] |
| `impressions` | Aggregated impressions.[1] |
| `ctr` | Aggregated CTR.[1] |
| `avg_position` | Aggregated average position.[1] |
| `striking_distance_score` | Ranking upside component.[1] |
| `ctr_gap_score` | Snippet underperformance component.[1] |
| `content_gap_score` | On-page weakness component.[1] |
| `base_opportunity_score` | Main production score.[1] |
| `aio_readiness_score` | Optional overlay score, only when available.[1] |
| `notes` | Manual explanation or reason for prioritization.[1] |

## Limitations

The current model has clear limitations, and documenting them improves credibility rather than weakening the project.[4]

- The current crawl workflow can assess page structure and SEO signals, but it cannot reveal whether Google AI Overviews actually cited the page.[2][5]
- No production SERP-level AIO citation dataset is currently connected to the model.[2][3][4]
- AIO readiness is therefore a proxy layer, not a visibility measurement layer.[6][7]
- Some content quality signals are still manual or heuristic rather than fully automated.[1]
- Position, CTR, and impression thresholds should be tuned to the specific site and market rather than treated as universal constants.[1]

## Recommended implementation path

The scoring workflow should be implemented in phases:[1]

1. Use BigQuery SQL to generate striking distance and CTR gap candidates from `gscqueries`.[1]
2. Join crawl diagnostics to generate a rule-based content gap score.[1]
3. Export a ranked shortlist as `top50_opportunities.csv` using `Total Score v1`.[1]
4. Add small-sample manual AIO readiness review only for top shortlisted URLs.[1]
5. In a later GEO / AI visibility module, add SERP observation and citation tracking before promoting AIO into the main scoring pipeline.[1][3]

## Interpretation

This model is intentionally practical. It prioritizes what can be measured now, while still showing a credible path toward AI Search-aware opportunity scoring.[1][4]

For the current portfolio phase, the correct positioning is:

- `Total Score v1` is the real, production-ready ranking logic.[1]
- `AIO Readiness Score` is an experimental overlay that helps prioritize which shortlisted pages may deserve AI Search-oriented improvement work.[1][2]
- True AI Overview citation visibility belongs to a later monitoring layer and should not be overstated in current reporting.[2][5][4]