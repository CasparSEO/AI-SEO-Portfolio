# M1 Diagnostic Report

## Overview

This report summarizes a sample set of SEO opportunities identified from the Airwallex query-level opportunity scoring workflow.

The analysis is based on non-branded URL-query combinations that already have search impressions, rank in the striking-distance range, and show clear optimisation potential. The goal is to move from raw Google Search Console performance data into a practical action list for SEO execution.

This first version focuses on traditional SEO opportunities such as CTR improvement, content expansion, and internal linking. In later modules, this framework can be extended with Google AIO readiness, entity signals, and AI visibility layers.

## Method

The opportunity list was generated from the Month 1 scoring workflow using query-level Google Search Console data.

The filtering logic focused on:
- Non-branded queries
- Non-empty query and URL fields
- Recent 14-day performance window
- Impressions greater than 10
- Average position between 11 and 30

This means the final list is not a full SEO audit of every page. It is a prioritised shortlist of URL-query pairs that are already close enough to page-one visibility to justify action.

## Top sample opportunities

### 1. Remittance to mainland China content

**URL**  
https://www.airwallex.com/hk-zh/blog/remittance-to-mainland-china

**Query**  
大陸匯款到香港限制

**Performance snapshot**
- Clicks: 1
- Impressions: 64
- CTR: 1.56%
- Average position: 11.78
- Opportunity score: 61.5
- Reason: High striking-distance opportunity
- Recommended action: Refresh content and rewrite title/meta

**Why this matters**

This query already has meaningful impressions and is ranking just outside page one. That usually means Google already sees the page as relevant, but the result is still underperforming in either ranking strength or search snippet appeal.

The keyword intent is highly practical and regulation-oriented. Users searching for remittance restrictions likely want a fast, trustworthy answer about limitations, process, compliance considerations, and transfer options.

**Recommended SEO action**
- Rewrite the title and meta description so the page more clearly addresses “大陸匯款到香港限制”.
- Add a dedicated section answering common restrictions, requirements, timelines, and compliance considerations.
- Improve internal links from related cross-border payment or remittance pages.
- Add clearer summary boxes or FAQ-style sections to make the answer easier to extract.

### 2. Business registration content

**URL**  
https://www.airwallex.com/hk-zh/blog/business-registration-certificate

**Query**  
商業登記處派籌時間

**Performance snapshot**
- Clicks: 1
- Impressions: 35
- CTR: 2.86%
- Average position: 11.0
- Opportunity score: 35.0
- Reason: High striking-distance opportunity
- Recommended action: Improve content depth and internal links

**Why this matters**

This page is already sitting almost exactly at page-one threshold. That makes it a strong candidate for content-depth improvements rather than a full rewrite.

The query suggests operational intent. Users likely want practical and timely information about appointment flow, queueing, timing, and required preparation.

**Recommended SEO action**
- Add a short section specifically about 派籌時間, appointment flow, and what users should prepare before visiting.
- Expand the article so it answers adjacent questions that searchers may also have.
- Strengthen internal links from business account setup, company incorporation, and related SME onboarding pages.
- Review whether the article structure can better surface the answer near the top of the page.

### 3. DBS business account comparison content

**URL**  
https://www.airwallex.com/hk/blog/dbs-open-account

**Query**  
dbs business account

**Performance snapshot**
- Clicks: 0
- Impressions: 36
- CTR: 0.0%
- Average position: 11.75
- Opportunity score: 34.64
- Reason: High striking-distance opportunity
- Recommended action: Refresh content and rewrite title/meta

**Why this matters**

This page has clear visibility but no clicks in the sample window. That usually indicates a strong CTR opportunity, especially when average position is already close to page one.

The query is competitor-oriented and commercial. Users may be comparing account opening requirements, fees, speed, and suitability across providers.

**Recommended SEO action**
- Reframe the title and meta description to better match comparison intent around DBS business account queries.
- Make the page’s comparison angle clearer in headings and intro copy.
- Add more explicit decision-support content such as eligibility, cost differences, processing speed, and use-case comparison.
- Link from related account comparison and SME finance content to strengthen relevance.

## Pattern summary

Across these examples, the strongest opportunities share three traits:
- Existing impressions
- Average positions just outside page one
- A clear on-page action that can be taken quickly

This is useful because it creates a practical SEO prioritisation model. Instead of trying to improve every page at once, the workflow identifies pages that already have demand and partial relevance, then recommends the most likely next move.

## Recommended next steps

1. Prioritise the top 10 URL-query pairs from `top50opportunities.csv`.
2. Group them by action type: title/meta refresh, content expansion, internal linking, or comparison-page improvement.
3. Implement changes on a small batch first, then monitor clicks, impressions, CTR, and average position in the next reporting window.
4. In the next iteration, connect this scoring layer with crawl-based page signals and future Google AIO readiness metrics.

## Portfolio value

This project demonstrates a full mini-pipeline:
- Query-level SEO opportunity scoring
- BigQuery-based filtering and ranking
- Python export to CSV
- Markdown reporting for decision-making

That makes the work more valuable than a static dashboard. It shows the ability to turn search data into prioritised recommendations, content actions, and portfolio-ready business communication.