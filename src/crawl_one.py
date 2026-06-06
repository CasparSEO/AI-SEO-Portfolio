import argparse
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "AI-SEO-Portfolio-Crawler/0.1 (+https://github.com/your-username/AI-SEO-Portfolio)"
}


def clean_text(value):
    if not value:
        return ""
    return " ".join(value.strip().split())


def get_title(soup):
    if soup.title and soup.title.string:
        return clean_text(soup.title.string)
    return ""


def get_h1(soup):
    h1 = soup.find("h1")
    return clean_text(h1.get_text(" ", strip=True)) if h1 else ""


def get_meta_description(soup):
    tag = soup.find("meta", attrs={"name": "description"})
    if tag and tag.get("content"):
        return clean_text(tag["content"])
    return ""


def get_canonical(soup):
    tag = soup.find("link", rel=lambda value: value and "canonical" in value)
    if tag and tag.get("href"):
        return tag["href"].strip()
    return ""


def has_json_ld(soup):
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    return len(scripts) > 0


def get_word_count(soup):
    body = soup.find("body")
    if not body:
        return 0
    text = body.get_text(" ", strip=True)
    return len(text.split())


def crawl_one(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    return {
        "url": url,
        "final_url": response.url,
        "status_code": response.status_code,
        "title": get_title(soup),
        "h1": get_h1(soup),
        "meta_description": get_meta_description(soup),
        "canonical": get_canonical(soup),
        "word_count": get_word_count(soup),
        "schema_found": has_json_ld(soup),
        "crawled_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Crawl one URL for SEO fields")
    parser.add_argument("url", help="URL to crawl")
    args = parser.parse_args()

    result = crawl_one(args.url)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()