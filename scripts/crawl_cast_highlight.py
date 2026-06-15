#!/usr/bin/env python3
"""
crawl_cast_highlight.py — Polite web crawler for CAST Highlight documentation.

Crawls the "Indicators & Methodology" category from https://doc.casthighlight.com/
and converts content to a structured markdown knowledgebase.

Usage:
    python scripts/crawl_cast_highlight.py [options]

Options:
    --discover-only     Only run Phase 1: URL discovery (no content fetch)
    --limit N           Only crawl the first N URLs (for testing)
    --force             Re-crawl and overwrite already-written pages
    --output-dir DIR    Output directory (default: docs/research/cast-highlight)
    --cache-dir DIR     Cache directory for raw HTML (default: <output-dir>/_cache)
    --dry-run           Show what would be done without fetching
    -v, --verbose       Verbose logging

Dependencies:
    pip install requests beautifulsoup4 lxml markdownify
    (markdownify is optional; falls back to hand-rolled conversion)

Output layout (under docs/research/cast-highlight/):
    README.md               — Overview, source URL, crawl date, stats
    methodology/            — One .md per methodology page
    rules/<lang>/           — One .md per rule page, grouped by primary language
    _index/urls.json        — Discovered URL list with metadata
    _index/catalog.json     — Machine-queryable catalog (no body text)
    _index/stats.md         — Summary counts by type/language/category

Contact: robert.matsuoka@duettoresearch.com
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from random import uniform
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag

try:
    from markdownify import markdownify as _markdownify_lib

    def html_to_markdown(html: str) -> str:
        """Convert HTML to markdown using markdownify."""
        return _markdownify_lib(
            html,
            heading_style="ATX",
            bullets="-",
            code_language="",
            strip=["script", "style", "nav", "footer"],
        ).strip()

except ImportError:

    def html_to_markdown(html: str) -> str:
        """Fallback hand-rolled HTML-to-markdown conversion."""
        soup = BeautifulSoup(html, "lxml")
        for tag in soup.find_all(["script", "style", "nav", "footer"]):
            tag.decompose()
        lines: list[str] = []
        for elem in soup.find_all(True):
            name = elem.name
            text = elem.get_text(strip=True)
            if not text:
                continue
            if name in ("h1",):
                lines.append(f"# {text}\n")
            elif name in ("h2",):
                lines.append(f"## {text}\n")
            elif name in ("h3",):
                lines.append(f"### {text}\n")
            elif name in ("h4",):
                lines.append(f"#### {text}\n")
            elif name == "pre":
                lines.append(f"```\n{text}\n```\n")
            elif name == "li":
                lines.append(f"- {text}")
            elif name == "p":
                lines.append(f"{text}\n")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_URL = "https://doc.casthighlight.com"
CATEGORY_URL = f"{BASE_URL}/category/product/indicators-methodology/"
ROBOTS_TXT_URL = f"{BASE_URL}/robots.txt"
SITEMAP_INDEX_URL = f"{BASE_URL}/wp-sitemap.xml"
POSTS_SITEMAP_URL = f"{BASE_URL}/wp-sitemap-posts-post-1.xml"

USER_AGENT = (
    "claude-mpm-skills-kb-crawler/1.0 "
    "(+research; contact: robert.matsuoka@duettoresearch.com)"
)

REQUEST_DELAY_MIN = 0.8  # seconds between requests
REQUEST_DELAY_MAX = 1.4
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2.0  # seconds

# Language detection keywords mapped to directory names.
# Order matters: more specific/distinctive keywords are checked first within each lang.
# The primary language (first detected) determines the output directory.
LANGUAGE_KEYWORDS: dict[str, list[str]] = {
    "scala": ["scala", "akka", "sbt", " val ", " def ", "option["],
    "kotlin": ["kotlin", ".kt ", "coroutine", "suspend fun"],
    "swift": ["swift", "ios", "xcode", "nsuserdefaults", "uikit"],
    "cobol": ["cobol", "identification division", "procedure division"],
    "abap": ["abap", " sap ", "report z"],
    "php": ["php", ".php", "laravel", "symfony", "drupal", "phpinfo", "<?php"],
    "python": ["python", ".py", "django", "flask", "fastapi", "pypi"],
    "ruby": ["ruby", ".rb", "rails", "gem ", "bundler"],
    "go": ["golang", "goroutine", "go routine", " gofmt"],
    "dotnet": ["c#", "csharp", "asp.net", "vb.net", ".net framework", ".net core"],
    "java": ["java", ".java", "spring boot", "hibernate", "maven", "gradle", "jvm"],
    "javascript": [
        "javascript",
        "node.js",
        "typescript",
        "angular",
        "react",
        "vue",
        "npm ",
        "webpack",
    ],
    "sql": ["sql", "plsql", "t-sql", "oracle sql", "ansi sql"],
    "cpp": ["c++", "cpp", "c/c++"],
    "vba": ["vba", "visual basic", "vb6"],
}

# Category/family detection
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Robustness": [
        "robustness",
        "crash",
        "null pointer",
        "exception",
        "error handling",
        "stability",
    ],
    "Efficiency": [
        "efficiency",
        "performance",
        "memory",
        "cpu",
        "throughput",
        "resource",
    ],
    "Security": [
        "security",
        "vulnerability",
        "injection",
        "xss",
        "csrf",
        "authentication",
        "sql injection",
        "owasp",
    ],
    "Transferability": [
        "transferability",
        "maintainability",
        "complexity",
        "coupling",
        "duplication",
    ],
    "Changeability": ["changeability", "readability", "dead code", "comment"],
    "CloudReady": [
        "cloud",
        "cloud readiness",
        "containerization",
        "microservice",
        "kubernetes",
        "docker",
    ],
    "Green": ["green", "energy", "sustainability", "carbon", "power consumption"],
    "AI_Readiness": [
        "agentic",
        "ai readiness",
        "llm",
        "artificial intelligence",
        "machine learning",
    ],
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

log = logging.getLogger("cast_crawler")


def setup_logging(verbose: bool = False) -> None:
    """Configure logging to stdout."""
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    )
    log.setLevel(level)
    log.addHandler(handler)


# ---------------------------------------------------------------------------
# HTTP layer — polite with retry/backoff
# ---------------------------------------------------------------------------


class PoliteCrawler:
    """HTTP client with rate-limiting, retry/backoff, caching, and robots.txt compliance.

    Why: Encapsulates all politeness concerns so callers don't need to think about
    rate limits, retries, or cache hits.
    What: Fetches URLs with delay, retries on 5xx, caches raw HTML to disk, respects robots.txt.
    Test: Mock requests.Session; assert delay called, retry on 503, cache hit skips network.
    """

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self._disallowed_prefixes: list[str] = []
        self._last_request_time: float = 0.0

    def _cache_path(self, url: str) -> Path:
        """Return deterministic cache file path for a URL."""
        key = hashlib.sha256(url.encode()).hexdigest()[:16]
        slug = re.sub(r"[^\w-]", "_", urlparse(url).path.strip("/"))[:60]
        return self.cache_dir / f"{slug}_{key}.html"

    def _sleep(self) -> None:
        """Sleep to maintain polite rate limiting with jitter."""
        elapsed = time.monotonic() - self._last_request_time
        target_delay = uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
        remaining = target_delay - elapsed
        if remaining > 0:
            time.sleep(remaining)
        self._last_request_time = time.monotonic()

    def fetch(
        self, url: str, use_cache: bool = True, force: bool = False
    ) -> str | None:
        """Fetch URL, returning HTML string or None on permanent failure.

        Why: Single entry point for all HTTP fetches with consistent politeness.
        What: Checks cache, sleeps, fetches, retries 5xx, caches success, logs errors.
        Test: Give cached file path; assert no HTTP call made. Remove cache; assert HTTP called.
        """
        cache_path = self._cache_path(url)
        if use_cache and not force and cache_path.exists():
            log.debug("Cache hit: %s", url)
            return cache_path.read_text(encoding="utf-8", errors="replace")

        # Check robots.txt compliance
        path = urlparse(url).path
        for prefix in self._disallowed_prefixes:
            if path.startswith(prefix):
                log.error("robots.txt disallows path: %s (matched %s)", path, prefix)
                return None

        self._sleep()
        last_error: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    html = response.text
                    if use_cache:
                        cache_path.write_text(html, encoding="utf-8")
                    return html
                elif response.status_code in (301, 302, 303, 307, 308):
                    # Follow redirects (requests does this automatically, but log it)
                    log.debug(
                        "Redirect %s -> %s", url, response.headers.get("Location", "?")
                    )
                    html = response.text
                    if use_cache:
                        cache_path.write_text(html, encoding="utf-8")
                    return html
                elif response.status_code in (404, 410):
                    log.warning("SKIP %s status=%d", url, response.status_code)
                    return None
                elif response.status_code >= 500:
                    wait = RETRY_BACKOFF_BASE**attempt
                    log.warning(
                        "Server error %d for %s (attempt %d/%d); retrying in %.1fs",
                        response.status_code,
                        url,
                        attempt + 1,
                        MAX_RETRIES,
                        wait,
                    )
                    time.sleep(wait)
                    last_error = RuntimeError(f"HTTP {response.status_code}")
                else:
                    log.warning(
                        "Unexpected status %d for %s", response.status_code, url
                    )
                    return None
            except requests.exceptions.Timeout as e:
                wait = RETRY_BACKOFF_BASE**attempt
                log.warning(
                    "Timeout fetching %s (attempt %d/%d); retrying in %.1fs",
                    url,
                    attempt + 1,
                    MAX_RETRIES,
                    wait,
                )
                time.sleep(wait)
                last_error = e
            except requests.exceptions.RequestException as e:
                log.error("Request failed for %s: %s", url, e)
                return None

        log.error("All %d retries failed for %s: %s", MAX_RETRIES, url, last_error)
        return None

    def check_robots_txt(self) -> bool:
        """Fetch and parse robots.txt; return True if our paths are allowed.

        Why: Robots.txt compliance is mandatory before any crawling.
        What: Parses Disallow rules for our user-agent and * wildcard.
        Test: Set robots content to block /category/; assert returns False.
        """
        log.info("Checking robots.txt: %s", ROBOTS_TXT_URL)
        self._sleep()
        try:
            response = self.session.get(ROBOTS_TXT_URL, timeout=15)
        except requests.exceptions.RequestException as e:
            log.warning("Could not fetch robots.txt (%s) — proceeding with caution", e)
            return True

        if response.status_code != 200:
            log.warning("robots.txt returned %d — proceeding", response.status_code)
            return True

        log.info("robots.txt content:\n%s", response.text[:2000])

        # Parse robots.txt
        current_agent_applies = False
        disallowed: list[str] = []
        for line in response.text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            field, _, value = line.partition(":")
            field = field.strip().lower()
            value = value.strip()
            if field == "user-agent":
                current_agent_applies = value in ("*", "claude-mpm-skills-kb-crawler")
            elif field == "disallow" and current_agent_applies:
                if value:
                    disallowed.append(value)

        self._disallowed_prefixes = disallowed
        log.info("Disallowed prefixes from robots.txt: %s", disallowed)

        # Check if our target paths are disallowed
        target_paths = [
            "/category/product/indicators-methodology/",
            "/wp-sitemap.xml",
        ]
        for target in target_paths:
            for prefix in disallowed:
                if target.startswith(prefix):
                    log.error(
                        "robots.txt DISALLOWS our target path: %s (rule: Disallow: %s)",
                        target,
                        prefix,
                    )
                    return False

        log.info("robots.txt check PASSED — all target paths are allowed")
        return True


# ---------------------------------------------------------------------------
# Phase 1 — URL Discovery
# ---------------------------------------------------------------------------


def discover_urls(crawler: PoliteCrawler) -> list[dict[str, Any]]:
    """Scrape paginated category listing and cross-reference with sitemap.

    Why: Category membership (not sitemap) is the authoritative source for which pages to include.
    What: Scrapes all paginated category pages, extracts article links+titles, cross-refs sitemap.
    Test: Mock listing HTML with 3 articles; assert 3 entries returned with correct URLs/titles.
    """
    # Step 1: Fetch sitemap for lastmod dates
    sitemap_data: dict[str, str] = {}
    log.info("Fetching sitemap: %s", POSTS_SITEMAP_URL)
    sitemap_html = crawler.fetch(POSTS_SITEMAP_URL, use_cache=True)
    if sitemap_html:
        sitemap_data = _parse_sitemap(sitemap_html)
        log.info("Sitemap: %d URLs with lastmod", len(sitemap_data))

    # Step 2: Scrape paginated category listing
    discovered: dict[str, dict[str, Any]] = {}  # url -> entry
    page = 1
    consecutive_empty = 0

    while True:
        if page == 1:
            page_url = CATEGORY_URL
        else:
            page_url = f"{CATEGORY_URL}page/{page}/"

        log.info("Discovering: page %d — %s", page, page_url)
        html = crawler.fetch(page_url, use_cache=True)
        if not html:
            log.warning("No content for page %d — stopping discovery", page)
            break

        soup = BeautifulSoup(html, "lxml")

        # Find article links — WordPress typically uses article or h2.entry-title > a
        entries = _extract_listing_entries(soup, page_url, page)
        if not entries:
            consecutive_empty += 1
            log.info(
                "Page %d returned no entries (consecutive empty: %d)",
                page,
                consecutive_empty,
            )
            if consecutive_empty >= 2:
                log.info("Two consecutive empty pages — discovery complete")
                break
        else:
            consecutive_empty = 0
            new_count = 0
            for entry in entries:
                url = entry["url"]
                if url not in discovered:
                    discovered[url] = entry
                    new_count += 1
            log.info(
                "Page %d: found %d entries (%d new)", page, len(entries), new_count
            )

        # Check for "next page" link
        next_link = soup.find("a", class_=re.compile(r"next|page-numbers.*next", re.I))
        if not next_link:
            # Also check for standard WordPress pagination
            nav = soup.find("nav", class_=re.compile(r"paginat|nav-links", re.I))
            if nav:
                next_link = nav.find("a", class_=re.compile(r"next", re.I))

        if not next_link:
            log.info(
                "No 'next' link found on page %d — checking if more pages exist", page
            )
            # Try next page anyway up to 40
            if page >= 40:
                log.info("Reached page limit 40 — stopping")
                break
        else:
            log.debug("Next page link found: %s", next_link.get("href", "?"))

        page += 1
        if page > 40:
            log.warning("Stopping at page 40 (safety limit)")
            break

    # Cross-reference with sitemap
    result: list[dict[str, Any]] = []
    for url, entry in discovered.items():
        entry["lastmod"] = sitemap_data.get(
            url, sitemap_data.get(url.rstrip("/") + "/", None)
        )
        result.append(entry)

    log.info("Total discovered URLs: %d", len(result))
    if len(result) < 150 or len(result) > 600:
        log.warning(
            "URL count %d is outside expected range 150–600 — verify pagination handling!",
            len(result),
        )

    return result


def _parse_sitemap(xml_content: str) -> dict[str, str]:
    """Parse WordPress sitemap XML; return {url: lastmod} mapping."""
    data: dict[str, str] = {}
    try:
        root = ET.fromstring(xml_content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url_elem in root.findall("sm:url", ns):
            loc = url_elem.find("sm:loc", ns)
            lastmod = url_elem.find("sm:lastmod", ns)
            if loc is not None and loc.text:
                data[loc.text.strip()] = (
                    lastmod.text.strip() if lastmod is not None and lastmod.text else ""
                )
    except ET.ParseError as e:
        log.warning("Could not parse sitemap XML: %s", e)
    return data


def _extract_listing_entries(
    soup: BeautifulSoup, page_url: str, page_num: int
) -> list[dict[str, Any]]:
    """Extract article entries from a category listing page.

    Why: Different WordPress themes use different markup; tries multiple selectors.
    What: Returns list of {url, title, discovered_page} dicts.
    Test: Parse sample WordPress category HTML; assert correct URLs and titles extracted.
    """
    entries: list[dict[str, Any]] = []
    seen_urls: set[str] = set()

    # Strategy 1: article elements with links
    articles = soup.find_all("article")
    if articles:
        for article in articles:
            link = article.find("a", href=True)
            title_elem = article.find(re.compile(r"h[1-4]"))
            if link:
                href = _normalize_url(link["href"])
                title = (
                    title_elem.get_text(strip=True)
                    if title_elem
                    else link.get_text(strip=True)
                )
                if href and href not in seen_urls and _is_article_url(href):
                    entries.append(
                        {"url": href, "title": title, "discovered_page": page_num}
                    )
                    seen_urls.add(href)

    # Strategy 2: h2.entry-title > a (common WordPress pattern)
    if not entries:
        for h2 in soup.find_all(
            ["h2", "h3"], class_=re.compile(r"entry-title|post-title", re.I)
        ):
            link = h2.find("a", href=True)
            if link:
                href = _normalize_url(link["href"])
                title = link.get_text(strip=True)
                if href and href not in seen_urls and _is_article_url(href):
                    entries.append(
                        {"url": href, "title": title, "discovered_page": page_num}
                    )
                    seen_urls.add(href)

    # Strategy 3: main content area links (broader fallback)
    if not entries:
        main = soup.find(["main", "div"], id=re.compile(r"main|content|primary", re.I))
        if main:
            for link in main.find_all("a", href=True):
                href = _normalize_url(link["href"])
                text = link.get_text(strip=True)
                if href and href not in seen_urls and _is_article_url(href) and text:
                    entries.append(
                        {"url": href, "title": text, "discovered_page": page_num}
                    )
                    seen_urls.add(href)

    return entries


def _normalize_url(url: str) -> str:
    """Normalize URL: ensure it's absolute and on the target domain."""
    if not url:
        return ""
    url = urljoin(BASE_URL, url.strip())
    parsed = urlparse(url)
    # Remove fragment and query params for cleanliness
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def _is_article_url(url: str) -> bool:
    """Check if URL looks like a CAST Highlight article (not navigation/category/tag)."""
    parsed = urlparse(url)
    if parsed.netloc and "casthighlight.com" not in parsed.netloc:
        return False
    path = parsed.path
    # Exclude category listings, tags, authors, pages that aren't articles
    exclude_patterns = [
        r"^/category/",
        r"^/tag/",
        r"^/author/",
        r"^/page/",
        r"^/wp-",
        r"^\s*$",
        r"^/$",
        r"^/feed/",
    ]
    for pattern in exclude_patterns:
        if re.match(pattern, path):
            return False
    # Must have some path component
    return bool(path and path != "/")


# ---------------------------------------------------------------------------
# Phase 2 — Content Extraction
# ---------------------------------------------------------------------------


def extract_page(url: str, html: str) -> dict[str, Any]:
    """Extract structured metadata and markdown content from a CAST Highlight page.

    Why: Different page types (rule vs methodology) need different extraction logic.
    What: Parses HTML, classifies type, extracts fields, converts body to markdown.
    Test: Parse a fixture rule HTML; assert content_type=="rule", languages extracted, body non-empty.
    """
    soup = BeautifulSoup(html, "lxml")
    slug = urlparse(url).path.strip("/").split("/")[-1] or urlparse(url).path.strip("/")

    # Extract title
    title = _extract_title(soup, slug)

    # Extract languages from raw HTML before article stripping (CSS classes are reliable)
    soup_for_lang = BeautifulSoup(html, "lxml")
    languages_from_html = _extract_languages_from_html(soup_for_lang)

    # Extract main article body
    article_html, article_text = _extract_article(soup)

    # Convert to markdown
    body_markdown = html_to_markdown(article_html) if article_html else article_text

    # Classify content type
    content_type = _classify_content_type(slug, title, article_text)

    # Extract structured metadata: combine HTML-detected languages with text-based
    languages_from_text = _extract_languages(title, article_text, slug)
    # HTML class detection is highest priority
    all_langs: list[str] = list(languages_from_html)
    for lang in languages_from_text:
        if lang not in all_langs:
            all_langs.append(lang)
    languages = all_langs
    category = _extract_category(title, article_text)
    severity = _extract_severity(article_text, soup)
    description, remediation = _extract_description_remediation(soup, article_text)
    has_code_examples = bool(soup.find(["pre", "code"]))

    return {
        "url": url,
        "slug": slug,
        "title": title,
        "content_type": content_type,
        "languages": languages,
        "category": category,
        "severity": severity,
        "description": description,
        "remediation": remediation,
        "has_code_examples": has_code_examples,
        "body_markdown": body_markdown,
    }


def _extract_title(soup: BeautifulSoup, slug: str = "") -> str:
    """Extract page title from various WordPress markup locations.

    Why: WordPress rule pages often use generic h1 like 'Why you should care';
         the real title is in og:title or <title> tag.
    What: Prefers og:title > <title> tag > entry-title h1, skipping generic h1s.
    Test: Page with og:title 'phpinfo() not used in production' -> returns that string.
    """
    # Generic h1 phrases that are NOT the page title
    generic_h1 = {
        "why you should care",
        "about",
        "overview",
        "introduction",
        "description",
    }

    # Try og:title first (most reliable for WordPress)
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = str(og_title["content"]).strip()
        # Strip site name suffix
        title = re.sub(
            r"\s*[|–—-]\s*(CAST Highlight|Cast Highlight).*$", "", title, flags=re.I
        ).strip()
        if title and title.lower() not in generic_h1:
            return title

    # <title> tag (reliable)
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)
        title = re.sub(
            r"\s*[|–—-]\s*(CAST Highlight|Cast Highlight).*$", "", title, flags=re.I
        ).strip()
        if title and title.lower() not in generic_h1:
            return title

    # Try h1.entry-title (WordPress standard)
    h1 = soup.find("h1", class_=re.compile(r"entry-title|page-title|post-title", re.I))
    if h1:
        title = h1.get_text(strip=True)
        if title.lower() not in generic_h1:
            return title

    # Any h1 that isn't generic
    for h1 in soup.find_all("h1"):
        title = h1.get_text(strip=True)
        if title and title.lower() not in generic_h1:
            return title

    # Fall back to slug-derived title
    if slug:
        return slug.replace("-", " ").replace("_", " ").title()

    return "Untitled"


def _extract_article(soup: BeautifulSoup) -> tuple[str, str]:
    """Find and return the main article body HTML and text, stripped of chrome.

    Why: WordPress pages have nav/header/footer/sidebar chrome we must exclude.
    What: Tries multiple selectors to locate article content; strips unwanted elements.
    Test: Parse page HTML with sidebar; assert sidebar text not in output.
    """
    # Remove chrome elements first
    for tag in soup.find_all(
        [
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
        ]
    ):
        tag.decompose()
    for tag in soup.find_all(
        class_=re.compile(
            r"sidebar|widget|breadcrumb|related|comment|share|social|nav|header|footer"
            r"|author-bio|post-nav|entry-meta.*footer|tags|categories",
            re.I,
        )
    ):
        tag.decompose()
    for tag in soup.find_all(
        id=re.compile(
            r"sidebar|comments|respond|breadcrumb|related|share|nav",
            re.I,
        )
    ):
        tag.decompose()

    # Strip CAST Highlight site-wide boilerplate sections (appear on every rule page)
    # Target ONLY the specific container that holds the "About CAST" promo.
    # We look for headings with that exact text, then remove their parent container.
    boilerplate_phrases = [
        "about cast and highlight",
        "about cast highlight",
        "over the last 25 years, cast has leveraged",
    ]
    for heading in soup.find_all(re.compile(r"^(h[2-5]|strong)$")):
        heading_text = heading.get_text(strip=True).lower()
        if any(phrase in heading_text for phrase in boilerplate_phrases):
            # Remove the nearest sectioning ancestor (div/section) or just the heading
            parent = heading.parent
            # Walk up to find a meaningful container to remove
            for _ in range(4):
                if parent and parent.name in ("div", "section", "article"):
                    # Only remove if this container is NOT the main article content
                    cls = " ".join(parent.get("class", []))
                    if not re.search(
                        r"entry-content|post-content|article-content|main", cls, re.I
                    ):
                        parent.decompose()
                        break
                    break
                parent = parent.parent if parent else None
            else:
                # Couldn't find safe container; just remove the heading
                heading.decompose()

    # Try to find the article body
    candidates = [
        soup.find(
            "div",
            class_=re.compile(r"entry-content|post-content|article-content", re.I),
        ),
        soup.find("article"),
        soup.find("main"),
        soup.find("div", id=re.compile(r"content|main", re.I)),
        soup.find("div", class_=re.compile(r"content", re.I)),
    ]

    for candidate in candidates:
        if candidate and len(candidate.get_text(strip=True)) > 100:
            return str(candidate), candidate.get_text(separator="\n", strip=True)

    # Fallback: body
    body = soup.find("body")
    if body:
        return str(body), body.get_text(separator="\n", strip=True)

    return str(soup), soup.get_text(separator="\n", strip=True)


def _classify_content_type(slug: str, title: str, text: str) -> str:
    """Classify page as 'rule' or 'methodology'.

    Why: The two types have different extraction needs and go to different output dirs.
    What: Uses slug patterns, title keywords, and content signals to classify.
    Test: slug='alt_debug-phpinfo' -> 'rule'; slug='cloud-maturity' -> 'methodology'.
    """
    text_lower = text.lower()
    title_lower = title.lower()

    # Strong rule indicators: alt_ prefix is used for code-quality rules
    if slug.startswith("alt_") or slug.startswith("alt-"):
        return "rule"

    # Methodology indicators: conceptual framework pages
    methodology_keywords = [
        "maturity",
        "scoring",
        "weighting",
        "framework",
        "software health",
        "green it",
        "sustainability score",
        "cloud readiness score",
        "agentic",
        "ai readiness",
        "how cast highlight",
        "methodology",
        "indicators overview",
        "measurement",
        "model",
        "approach",
    ]
    for kw in methodology_keywords:
        if kw in title_lower or kw in text_lower[:1000]:
            return "methodology"

    # Rule indicators: has remediation, code patterns, "what to do", technology tags
    rule_signals = [
        "what to do",
        "compliant",
        "non-compliant",
        "remediation",
        "this rule",
        "this indicator",
        "violation",
        "detected when",
        "code example",
        "bad practice",
        "good practice",
    ]
    rule_score = sum(1 for kw in rule_signals if kw in text_lower)
    if rule_score >= 2:
        return "rule"

    # Default: if has language mentions and short content, likely a rule
    lang_count = sum(
        1
        for lang_kwds in LANGUAGE_KEYWORDS.values()
        for kw in lang_kwds
        if kw.lower() in text_lower
    )
    if lang_count >= 2 and len(text) < 5000:
        return "rule"

    return "methodology"  # Safe default for unknown


def _extract_languages_from_html(soup: BeautifulSoup) -> list[str]:
    """Extract languages from HTML CSS class names (highest confidence signal).

    Why: CAST Highlight uses 'language-<lang>' CSS classes on code blocks, which
         are the most reliable indicator of what language a rule applies to.
    What: Finds all elements with 'language-*' classes; maps to canonical lang names.
    Test: HTML with class='language-scala' -> ['scala']. No such class -> [].
    """
    # Map of CSS class names to our canonical language keys
    css_to_lang: dict[str, str] = {
        "scala": "scala",
        "java": "java",
        "python": "python",
        "ruby": "ruby",
        "php": "php",
        "javascript": "javascript",
        "typescript": "javascript",
        "csharp": "dotnet",
        "cs": "dotnet",
        "vb": "dotnet",
        "kotlin": "kotlin",
        "swift": "swift",
        "go": "go",
        "golang": "go",
        "sql": "sql",
        "cobol": "cobol",
        "abap": "abap",
        "cpp": "cpp",
        "c": "c",
        "c++": "cpp",
        "vba": "vba",
        "groovy": "java",
        "jsx": "javascript",
        "tsx": "javascript",
    }
    found: list[str] = []
    seen: set[str] = set()

    for elem in soup.find_all(class_=re.compile(r"language-\w+", re.I)):
        for cls in elem.get("class", []):
            if cls.startswith("language-"):
                lang_css = cls[len("language-") :].lower()
                canonical = css_to_lang.get(lang_css)
                if canonical and canonical not in seen:
                    found.append(canonical)
                    seen.add(canonical)

    # Also check WordPress post tags with language names
    for tag_link in soup.find_all("a", rel=re.compile(r"tag", re.I)):
        tag_text = tag_link.get_text(strip=True).lower()
        for lang_name, canonical in css_to_lang.items():
            if tag_text == lang_name and canonical not in seen:
                found.append(canonical)
                seen.add(canonical)

    return found


def _extract_languages(title: str, text: str, slug: str) -> list[str]:
    """Extract programming languages applicable to a rule.

    Why: Rules are language-specific; we need this to organize output directories.
    What: Scans title, slug for strong signals first; text for secondary signals.
         Returns languages in order of confidence (strongest first).
    Test: slug='alt_debug-phpinfo-not-used-production' title='phpinfo()...' -> ['php'].
    """
    # Primary signal: slug and title (high confidence)
    primary_source = f"{slug} {title}".lower()
    # Secondary signal: article text excerpt (lower confidence; use word boundaries)
    secondary_source = text[:4000].lower()

    found_primary: list[str] = []
    found_secondary: list[str] = []

    for lang, keywords in LANGUAGE_KEYWORDS.items():
        in_primary = any(kw.lower() in primary_source for kw in keywords)
        in_secondary = any(kw.lower() in secondary_source for kw in keywords)
        if in_primary and lang not in found_primary:
            found_primary.append(lang)
        elif in_secondary and lang not in found_secondary:
            found_secondary.append(lang)

    # Combine: primary detections first, then secondary
    result: list[str] = []
    for lang in found_primary:
        if lang not in result:
            result.append(lang)
    for lang in found_secondary:
        if lang not in result:
            result.append(lang)

    return result


def _extract_category(title: str, text: str) -> str | None:
    """Detect the quality category/family for a rule.

    Why: Rules belong to families (Security, Robustness, etc.) useful for filtering.
    What: Scores each category by keyword count; returns highest-scoring category.
    Test: Text with 'sql injection', 'xss', 'vulnerability' -> 'Security'.
    """
    combined = f"{title} {text[:2000]}".lower()
    scores: dict[str, int] = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        scores[cat] = sum(1 for kw in keywords if kw in combined)
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else None


def _extract_severity(text: str, soup: BeautifulSoup) -> str | None:
    """Extract severity/criticality level if shown on page.

    Why: Some rule pages expose a severity level helpful for prioritization.
    What: Scans for severity/criticality text patterns or structured data.
    Test: Text with 'Critical' near 'severity' -> 'critical'.
    """
    # Try structured spans/labels
    for elem in soup.find_all(
        class_=re.compile(r"severity|criticality|priority", re.I)
    ):
        val = elem.get_text(strip=True).lower()
        if val in ("critical", "high", "medium", "low"):
            return val

    # Text pattern match
    match = re.search(
        r"(?:severity|criticality|priority)[:\s]+([a-z]+)",
        text.lower(),
    )
    if match:
        val = match.group(1)
        if val in ("critical", "high", "medium", "low"):
            return val

    return None


def _extract_description_remediation(
    soup: BeautifulSoup, text: str
) -> tuple[str | None, str | None]:
    """Extract description/rationale and remediation guidance.

    Why: These are the most actionable parts of a rule page for developers.
    What: Looks for labeled sections; falls back to first/later paragraphs.
    Test: HTML with 'What to do' h2 -> remediation contains following paragraph text.
    """
    description: str | None = None
    remediation: str | None = None

    # Try to find labeled sections
    for heading in soup.find_all(re.compile(r"h[2-4]")):
        heading_text = heading.get_text(strip=True).lower()
        # Collect sibling text until next heading
        siblings: list[str] = []
        for sib in heading.find_next_siblings():
            if sib.name and re.match(r"h[2-4]", sib.name):
                break
            if isinstance(sib, Tag):
                t = sib.get_text(strip=True)
                if t:
                    siblings.append(t)
        combined_text = " ".join(siblings).strip()
        if not combined_text:
            continue

        if re.search(r"what to do|remediat|fix|solution|how to", heading_text):
            remediation = combined_text[:1000]
        elif re.search(
            r"descri|why|rationale|overview|about|issue|problem", heading_text
        ):
            description = combined_text[:1000]

    # Fallback: first paragraph as description
    if not description:
        first_p = soup.find("p")
        if first_p:
            description = first_p.get_text(strip=True)[:500] or None

    return description, remediation


# ---------------------------------------------------------------------------
# File output helpers
# ---------------------------------------------------------------------------


def slugify(text: str) -> str:
    """Convert text to a safe filename slug.

    Why: Page titles may contain characters unsafe for filenames.
    What: Normalizes unicode, lowercases, replaces non-alphanumeric with hyphens.
    Test: 'C++ Security Issues!' -> 'c--security-issues'.
    """
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")[:80]


def write_rule_page(page_data: dict[str, Any], output_dir: Path) -> Path:
    """Write a rule page to the rules/<lang>/ directory with YAML frontmatter.

    Why: Rules are organized by language for easy lookup by coding-skill agents.
    What: Writes frontmatter + body markdown to rules/<primary_lang>/<slug>.md.
    Test: Pass rule data; assert file created at expected path with correct frontmatter.
    """
    languages = page_data.get("languages") or []
    primary_lang = languages[0] if languages else "_multi"
    lang_dir = output_dir / "rules" / primary_lang
    lang_dir.mkdir(parents=True, exist_ok=True)

    slug = page_data["slug"] or slugify(page_data["title"])
    filename = f"{slugify(slug)}.md"
    filepath = lang_dir / filename

    frontmatter_lines = [
        "---",
        f"title: {_yaml_str(page_data['title'])}",
        f"url: {page_data['url']}",
        f"slug: {page_data['slug']}",
        "content_type: rule",
    ]
    if languages:
        frontmatter_lines.append(f"languages: [{', '.join(languages)}]")
    if page_data.get("category"):
        frontmatter_lines.append(f"category: {page_data['category']}")
    if page_data.get("severity"):
        frontmatter_lines.append(f"severity: {page_data['severity']}")
    frontmatter_lines.append(
        f"has_code_examples: {str(page_data.get('has_code_examples', False)).lower()}"
    )
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)

    body = page_data.get("body_markdown", "")
    content = f"{frontmatter}\n\n{body}\n"
    filepath.write_text(content, encoding="utf-8")
    return filepath


def write_methodology_page(page_data: dict[str, Any], output_dir: Path) -> Path:
    """Write a methodology page to the methodology/ directory.

    Why: Methodology pages are conceptual overviews, not language-specific rules.
    What: Writes frontmatter + body markdown to methodology/<slug>.md.
    Test: Pass methodology data; assert file at methodology/<slug>.md with correct title.
    """
    method_dir = output_dir / "methodology"
    method_dir.mkdir(parents=True, exist_ok=True)

    slug = page_data["slug"] or slugify(page_data["title"])
    filename = f"{slugify(slug)}.md"
    filepath = method_dir / filename

    frontmatter_lines = [
        "---",
        f"title: {_yaml_str(page_data['title'])}",
        f"url: {page_data['url']}",
        f"slug: {page_data['slug']}",
        "content_type: methodology",
    ]
    if page_data.get("category"):
        frontmatter_lines.append(f"category: {page_data['category']}")
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)

    body = page_data.get("body_markdown", "")
    content = f"{frontmatter}\n\n{body}\n"
    filepath.write_text(content, encoding="utf-8")
    return filepath


def _yaml_str(value: str) -> str:
    """Quote a string for YAML frontmatter if it contains special characters."""
    if any(c in value for c in ('"', "'", ":", "#", "[", "]", "{", "}", ",")):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return value


# ---------------------------------------------------------------------------
# Catalog and stats
# ---------------------------------------------------------------------------


def build_catalog_entry(
    page_data: dict[str, Any], file_path: Path, output_dir: Path
) -> dict[str, Any]:
    """Build a catalog entry (no body text) for catalog.json.

    Why: catalog.json is machine-queryable without loading large bodies.
    What: Returns all metadata fields plus relative file path, excluding body_markdown.
    Test: Pass page data + path; assert 'body_markdown' not in result, 'file_path' in result.
    """
    rel_path = str(file_path.relative_to(output_dir))
    return {
        "url": page_data["url"],
        "slug": page_data["slug"],
        "title": page_data["title"],
        "content_type": page_data["content_type"],
        "languages": page_data.get("languages") or [],
        "category": page_data.get("category"),
        "severity": page_data.get("severity"),
        "description": page_data.get("description"),
        "remediation": page_data.get("remediation"),
        "has_code_examples": page_data.get("has_code_examples", False),
        "file_path": rel_path,
    }


def write_stats(
    catalog: list[dict[str, Any]], output_dir: Path, crawl_date: str
) -> None:
    """Write _index/stats.md with summary counts.

    Why: Quick human-readable overview of the knowledgebase contents.
    What: Counts by content_type, language, and category; writes stats.md.
    Test: Pass catalog with mixed types; assert counts match input distribution.
    """
    total = len(catalog)
    by_type: dict[str, int] = {}
    by_lang: dict[str, int] = {}
    by_cat: dict[str, int] = {}

    for entry in catalog:
        ct = entry.get("content_type", "unknown")
        by_type[ct] = by_type.get(ct, 0) + 1

        for lang in entry.get("languages") or []:
            by_lang[lang] = by_lang.get(lang, 0) + 1
        if not entry.get("languages"):
            by_lang["_multi"] = by_lang.get("_multi", 0) + 1

        cat = entry.get("category") or "unknown"
        by_cat[cat] = by_cat.get(cat, 0) + 1

    lines = [
        "# CAST Highlight Knowledgebase — Statistics",
        "",
        f"**Crawl date:** {crawl_date}",
        f"**Source:** {CATEGORY_URL}",
        "",
        f"## Total Pages: {total}",
        "",
        "## By Content Type",
        "",
    ]
    for ct, count in sorted(by_type.items()):
        lines.append(f"| {ct} | {count} |")

    lines += [
        "",
        "## By Primary Language",
        "",
        "| Language | Rule Count |",
        "|----------|-----------|",
    ]
    for lang, count in sorted(by_lang.items(), key=lambda x: -x[1]):
        lines.append(f"| {lang} | {count} |")

    lines += [
        "",
        "## By Quality Category",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ]
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {count} |")

    stats_path = output_dir / "_index" / "stats.md"
    stats_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log.info("Wrote stats: %s", stats_path)


def write_readme(
    catalog: list[dict[str, Any]], output_dir: Path, crawl_date: str
) -> None:
    """Write top-level README.md for the knowledgebase.

    Why: Provides orientation for anyone exploring the knowledgebase directory.
    What: Describes source, structure, counts, and how to regenerate.
    Test: Assert README.md created and contains source URL.
    """
    total = len(catalog)
    rule_count = sum(1 for e in catalog if e.get("content_type") == "rule")
    method_count = sum(1 for e in catalog if e.get("content_type") == "methodology")
    langs = sorted({lang for e in catalog for lang in (e.get("languages") or [])})

    content = f"""# CAST Highlight — Indicators & Methodology Knowledgebase

**Source:** {CATEGORY_URL}
**Crawl date:** {crawl_date}
**Total pages:** {total} ({rule_count} rules + {method_count} methodology pages)
**Languages covered:** {', '.join(langs) or 'various'}

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
- Crawled with `{USER_AGENT}`
- Robots.txt verified before crawling
- Rate-limited to ~1 req/sec
"""
    (output_dir / "README.md").write_text(content, encoding="utf-8")
    log.info("Wrote README.md")


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Polite crawler for CAST Highlight Indicators & Methodology docs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--discover-only",
        action="store_true",
        help="Only run Phase 1: URL discovery",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Only crawl first N URLs (for testing)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-crawl and overwrite already-written pages",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/research/cast-highlight"),
        help="Output directory (default: docs/research/cast-highlight)",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Cache directory for raw HTML (default: <output-dir>/_cache)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose logging",
    )
    return parser.parse_args()


def update_gitignore(repo_root: Path) -> None:
    """Ensure _cache/ under docs/research/cast-highlight/ is in .gitignore.

    Why: Raw HTML cache is large/ephemeral; only markdown output should be committed.
    What: Appends gitignore rule if not already present.
    Test: Run twice; assert rule appears exactly once in .gitignore.
    """
    gitignore_path = repo_root / ".gitignore"
    cache_pattern = "docs/research/cast-highlight/_cache/"
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
        if cache_pattern not in content:
            with gitignore_path.open("a", encoding="utf-8") as f:
                f.write(
                    f"\n# CAST Highlight raw HTML cache (not committed)\n{cache_pattern}\n"
                )
            log.info("Added %s to .gitignore", cache_pattern)
        else:
            log.debug("%s already in .gitignore", cache_pattern)
    else:
        log.warning(".gitignore not found at %s", gitignore_path)


def main() -> None:
    """Main entry point for the CAST Highlight crawler."""
    args = parse_args()
    setup_logging(args.verbose)

    output_dir = args.output_dir.resolve()
    cache_dir = (args.cache_dir or output_dir / "_cache").resolve()
    index_dir = output_dir / "_index"

    log.info("Output dir: %s", output_dir)
    log.info("Cache dir: %s", cache_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)

    # Update .gitignore for cache
    repo_root = Path(__file__).resolve().parent.parent
    update_gitignore(repo_root)

    crawler = PoliteCrawler(cache_dir)

    # ---- robots.txt check ----
    if not args.dry_run:
        allowed = crawler.check_robots_txt()
        if not allowed:
            log.error("robots.txt DISALLOWS crawling — STOPPING as required")
            sys.exit(1)
    else:
        log.info("[DRY RUN] Skipping robots.txt check")

    # ---- Phase 1: URL Discovery ----
    urls_json_path = index_dir / "urls.json"

    if urls_json_path.exists() and not args.force and not args.dry_run:
        log.info("Loading cached URL list from %s", urls_json_path)
        with urls_json_path.open(encoding="utf-8") as f:
            url_list: list[dict[str, Any]] = json.load(f)
        log.info("Loaded %d URLs from cache", len(url_list))
    else:
        log.info("=== Phase 1: URL Discovery ===")
        if args.dry_run:
            log.info("[DRY RUN] Would discover URLs from %s", CATEGORY_URL)
            return
        url_list = discover_urls(crawler)
        log.info("Discovery complete: %d URLs found", len(url_list))

        with urls_json_path.open("w", encoding="utf-8") as f:
            json.dump(url_list, f, indent=2, ensure_ascii=False)
        log.info("Saved URL list to %s", urls_json_path)

    log.info("Total URLs discovered: %d", len(url_list))

    if args.discover_only:
        log.info("--discover-only flag set — stopping after Phase 1")
        print(f"\nDiscovery complete: {len(url_list)} URLs found")
        print(f"URL list saved to: {urls_json_path}")
        return

    # ---- Phase 2: Crawl & Extract ----
    log.info("=== Phase 2: Crawl & Extract ===")

    crawl_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    catalog: list[dict[str, Any]] = []
    failed_urls: list[dict[str, str]] = []
    files_written = 0

    to_crawl = url_list
    if args.limit:
        to_crawl = url_list[: args.limit]
        log.info("Limiting crawl to %d URLs (--limit %d)", len(to_crawl), args.limit)

    total = len(to_crawl)
    for i, url_entry in enumerate(to_crawl, 1):
        url = url_entry["url"]
        log.info("[%d/%d] Crawling: %s", i, total, url)

        # Check if already extracted (skip unless --force)
        # We check by looking for the file in methodology/ or rules/
        if not args.force:
            # Quick check: does catalog already have this URL?
            # (We'll skip proper skip-detection and rely on cache hits)
            pass

        html = crawler.fetch(url, use_cache=True, force=args.force)
        if not html:
            reason = "fetch_failed"
            failed_urls.append({"url": url, "reason": reason})
            log.warning("FAILED: %s (%s)", url, reason)
            continue

        try:
            page_data = extract_page(url, html)
        except Exception as exc:
            failed_urls.append({"url": url, "reason": f"extract_error: {exc}"})
            log.error("Extraction error for %s: %s", url, exc)
            continue

        # Write output file
        try:
            if page_data["content_type"] == "methodology":
                file_path = write_methodology_page(page_data, output_dir)
            else:
                file_path = write_rule_page(page_data, output_dir)
        except Exception as exc:
            failed_urls.append({"url": url, "reason": f"write_error: {exc}"})
            log.error("Write error for %s: %s", url, exc)
            continue

        catalog.append(build_catalog_entry(page_data, file_path, output_dir))
        files_written += 1
        log.debug(
            "Wrote: %s (type=%s, langs=%s)",
            file_path,
            page_data["content_type"],
            page_data.get("languages"),
        )

    # ---- Write index files ----
    log.info("=== Writing index files ===")
    catalog_path = index_dir / "catalog.json"
    with catalog_path.open("w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    log.info("Wrote catalog: %d entries → %s", len(catalog), catalog_path)

    write_stats(catalog, output_dir, crawl_date)
    write_readme(catalog, output_dir, crawl_date)

    # ---- Summary ----
    log.info("=== Crawl Complete ===")
    log.info("Files written: %d", files_written)
    log.info("Failed URLs: %d", len(failed_urls))
    if failed_urls:
        log.warning("Failed URLs:")
        for f_entry in failed_urls:
            log.warning("  %s — %s", f_entry["url"], f_entry["reason"])

    print(f"\n{'='*60}")
    print("CAST Highlight Crawler — Done")
    print(f"{'='*60}")
    print(f"URLs discovered:  {len(url_list)}")
    print(f"URLs crawled:     {len(to_crawl)}")
    print(f"Files written:    {files_written}")
    print(f"Failed:           {len(failed_urls)}")
    print(f"Output dir:       {output_dir}")
    print(f"Catalog:          {catalog_path}")
    if failed_urls:
        print("\nFailed URLs:")
        for f_entry in failed_urls:
            print(f"  [{f_entry['reason']}] {f_entry['url']}")


if __name__ == "__main__":
    main()
