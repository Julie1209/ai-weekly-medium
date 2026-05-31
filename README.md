# AI Weekly Medium Draft Generator

Collect AI news from RSS feeds and turn it into a Medium-ready Markdown draft every week.

## Features

- Collects AI news from curated RSS feeds.
- Sorts articles by publish date.
- Generates a Markdown draft under `drafts/`.
- Runs locally or on a weekly GitHub Actions schedule.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Output

Drafts are written to:

```text
drafts/ai-weekly-YYYY-MM-DD.md
```

## Customize Sources

Edit `DEFAULT_SOURCES` in `sources.py` to add or remove RSS feeds.

## GitHub Actions

The workflow runs every Monday at 09:00 UTC and can also be started manually from the Actions tab.
