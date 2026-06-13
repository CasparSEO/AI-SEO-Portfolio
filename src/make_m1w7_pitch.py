from pathlib import Path
import pandas as pd

INPUT_PATH = Path("outputs/top50opportunities.csv")
OUTPUT_PATH = Path("outputs/m1w7pitch.md")

def fmt(value):
    if pd.isna(value):
        return ""
    return str(value)

def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "Missing outputs/top50opportunities.csv. Run src/scoreopportunities.py first."
        )

    df = pd.read_csv(INPUT_PATH)
    top3 = df.head(3).copy()

    lines = [
        "# M1W7 Opportunity Score Pitch",
        "",
        "## Executive pitch",
        "",
        "This module turns Google Search Console query-level data into a prioritized SEO opportunity list.",
        "",
        "The scoring logic focuses on non-branded URL-query combinations with existing search demand, striking-distance rankings, and clear optimization actions.",
        "",
        "The output is designed for SEO prioritization: which page to improve, which query to target, why it matters, and what action should be taken next.",
        "",
        "## Top 3 opportunities",
        "",
        "| Rank | URL | Query | Impressions | Avg Position | Opportunity Score | Recommended Action |",
        "|---:|---|---|---:|---:|---:|---|",
    ]

    for idx, row in top3.iterrows():
        lines.append(
            "| {rank} | {url} | {query} | {impressions} | {avg_position} | {score} | {action} |".format(
                rank=idx + 1,
                url=fmt(row.get("url")),
                query=fmt(row.get("query")),
                impressions=fmt(row.get("impressions")),
                avg_position=fmt(row.get("avg_position")),
                score=fmt(row.get("opportunity_score")),
                action=fmt(row.get("recommended_action")),
            )
        )

    lines.extend([
        "",
        "## How to read this output",
        "",
        "- High opportunity scores indicate URL-query pairs with meaningful impressions and rankings close enough to improve.",
        "- Queries in positions 11-30 are treated as striking-distance or lower-page opportunities.",
        "- Recommended actions translate the score into practical SEO next steps, such as content refreshes, title/meta improvements, internal linking, or topical expansion.",
        "",
        "## Portfolio value",
        "",
        "This is a practical SEO data product rather than a static report.",
        "",
        "It combines BigQuery, Python, pandas, and GSC-derived metrics to move from raw search data to prioritised recommendations.",
        "",
        "In later modules, this output can feed content audits, internal linking, AI visibility checks, and Google AIO readiness analysis.",
        "",
    ])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved pitch to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()