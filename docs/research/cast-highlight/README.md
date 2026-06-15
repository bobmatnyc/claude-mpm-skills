# CAST Highlight — Indicators & Methodology Knowledgebase

**Source:** https://doc.casthighlight.com/category/product/indicators-methodology/
**Crawl date:** 2026-06-15
**Total pages:** 335 (322 rules + 13 methodology pages)
**Languages covered:** abap, cobol, cpp, dotnet, java, javascript, kotlin, php, python, ruby, scala, sql, swift

## What Is This?

This knowledgebase is a structured, git-tracked extraction of CAST Highlight's
"Indicators & Methodology" documentation. CAST Highlight is a static analysis platform
that measures software health, cloud readiness, green IT, and AI readiness using
hundreds of code-quality rules and scoring methodologies.

This data is used to enrich the `claude-mpm-skills` coding skills with concrete,
language-specific quality rules that can guide developers during code review.

## Directory Layout

```
docs/research/cast-highlight/
├── README.md               # This file
├── methodology/            # Conceptual scoring framework pages
├── rules/                  # Code quality rules organized by language
│   ├── php/
│   ├── java/
│   ├── python/
│   ├── javascript/
│   ├── _multi/             # Language-agnostic rules
│   └── ...
└── _index/
    ├── urls.json           # Discovered URL list with metadata
    ├── catalog.json        # Machine-queryable catalog (no body text)
    └── stats.md            # Summary counts by type/language/category
```

## Regenerating

```bash
# Full re-crawl (uses cache for already-fetched pages):
python scripts/crawl_cast_highlight.py

# Force re-fetch everything:
python scripts/crawl_cast_highlight.py --force

# Discovery only (Phase 1):
python scripts/crawl_cast_highlight.py --discover-only

# Test run (5 pages):
python scripts/crawl_cast_highlight.py --limit 5
```

**Dependencies:** `requests`, `beautifulsoup4`, `lxml`, `markdownify`
Install via: `uv pip install requests beautifulsoup4 lxml markdownify`

## Source Notes

- CAST Highlight WordPress site at `doc.casthighlight.com`
- Crawled with `claude-mpm-skills-kb-crawler/1.0 (+research; contact: robert.matsuoka@duettoresearch.com)`
- Robots.txt verified before crawling
- Rate-limited to ~1 req/sec
