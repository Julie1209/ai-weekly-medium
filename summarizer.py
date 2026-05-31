"""Small deterministic summarizer for Medium draft generation."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import date

from sources import NewsItem


@dataclass(frozen=True)
class Summary:
    title: str
    link: str
    source: str
    published: str
    takeaway: str


def _clean_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _first_sentence(value: str, fallback: str) -> str:
    cleaned = _clean_text(value)
    if not cleaned:
        return fallback

    match = re.search(r"(.+?[.!?])\s", cleaned)
    sentence = match.group(1) if match else cleaned
    return sentence[:280].rstrip()


def summarize_items(items: list[NewsItem]) -> list[Summary]:
    summaries: list[Summary] = []
    for item in items:
        summaries.append(
            Summary(
                title=item.title,
                link=item.link,
                source=item.source,
                published=item.published.date().isoformat() if item.published else "Date unavailable",
                takeaway=_first_sentence(item.summary, fallback="Read the source for details."),
            )
        )
    return summaries


def build_markdown_draft(summaries: list[Summary], published_on: date) -> str:
    lines = [
        f"# AI Weekly: {published_on.isoformat()}",
        "",
        "A weekly roundup of AI news, formatted as a Medium draft starter.",
        "",
        "## Highlights",
        "",
    ]

    for index, summary in enumerate(summaries, start=1):
        lines.extend(
            [
                f"### {index}. {summary.title}",
                "",
                f"- Source: {summary.source}",
                f"- Published: {summary.published}",
                f"- Link: [{summary.link}]({summary.link})",
                f"- Takeaway: {summary.takeaway}",
                "",
            ]
        )

    lines.extend(
        [
            "## Draft Angle",
            "",
            "Add analysis around product updates, model capabilities, open-source tools, and industry adoption before publishing.",
            "",
            "## Notes",
            "",
            "- Verify each source before publishing.",
            "- Add personal analysis and examples for readers.",
        ]
    )
    return "\n".join(lines) + "\n"
