"""Generate a weekly AI news Medium draft."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from sources import DEFAULT_SOURCES, fetch_items
from summarizer import build_markdown_draft, summarize_items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect AI news and generate a Medium-ready Markdown draft."
    )
    parser.add_argument(
        "--output-dir",
        default="drafts",
        help="Directory where the generated draft will be saved.",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=12,
        help="Maximum number of source items to include.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now(timezone.utc).date()
    items = fetch_items(DEFAULT_SOURCES, limit=args.max_items)
    summaries = summarize_items(items)
    draft = build_markdown_draft(summaries, published_on=today)

    output_path = output_dir / f"ai-weekly-{today.isoformat()}.md"
    output_path.write_text(draft, encoding="utf-8")
    print(f"Generated Medium draft: {output_path}")


if __name__ == "__main__":
    main()
