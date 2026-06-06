# Crawl Policy

This project uses a lightweight SEO diagnostic crawler for public webpages only.

## Rules

- Respect robots.txt where applicable.
- Crawl only public HTML pages.
- Do not crawl login, checkout, account, search-result, or API endpoints.
- Send a clear User-Agent.
- Use request timeout to avoid hanging.
- Add delay between requests.
- Store only SEO diagnostic fields, not full page content.

## Fields collected

- url
- status_code
- title
- h1
- meta_description
- canonical
- word_count
- schema_found
- crawled_at

## Purpose

The crawler supports SEO diagnostics by joining GSC performance data with on-page signals.