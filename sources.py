"""RSS source collection for weekly AI news."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable

import feedparser


@dataclass(frozen=True)
class Source:
    name: str
    url: str


@dataclass(frozen=True)
class NewsItem:
    title: str
    link: str
    source: str
    published: datetime | None
    summary: str


DEFAULT_SOURCES: tuple[Source, ...] = (
    Source("OpenAI Blog", "https://openai.com/news/rss.xml"),
    Source("Google AI Blog", "https://blog.google/technology/ai/rss/"),
    Source("Anthropic News", "https://www.anthropic.com/news/rss.xml"),
    Source("Hugging Face Blog", "https://huggingface.co/blog/feed.xml"),
    Source("MIT Technology Review AI", "https://www.technologyreview.com/topic/artificial-intelligence/feed/"),
)


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def fetch_items(sources: Iterable[Source], limit: int = 12) -> list[NewsItem]:
    items: list[NewsItem] = []

    for source in sources:
        feed = feedparser.parse(source.url)
        for entry in feed.entries:
            published = _parse_date(
                getattr(entry, "published", None) or getattr(entry, "updated", None)
            )
            items.append(
                NewsItem(
                    title=getattr(entry, "title", "Untitled"),
                    link=getattr(entry, "link", ""),
                    source=source.name,
                    published=published,
                    summary=getattr(entry, "summary", "") or getattr(entry, "description", ""),
                )
            )

    return sorted(
        items,
        key=lambda item: item.published or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )[:limit]
