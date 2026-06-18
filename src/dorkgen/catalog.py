"""Catalog helpers for curated dork entries."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.parse import quote_plus

CATALOG_PATH = Path(__file__).parent / "data" / "catalog.json"


@dataclass(frozen=True)
class CatalogItem:
    id: str
    mode: str
    category: str
    label: str
    dork: str


def load_catalog(include_file_hunter: bool = False) -> List[CatalogItem]:
    """Load catalog items from JSON data."""
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    items = [CatalogItem(**entry) for entry in raw]
    if include_file_hunter:
        return items
    return [item for item in items if item.mode == "sec"]


def list_categories(items: Iterable[CatalogItem], mode: str | None = None) -> List[str]:
    """List distinct category names preserving order of first appearance."""
    seen: Dict[str, None] = {}
    for item in items:
        if mode and item.mode != mode:
            continue
        if item.category not in seen:
            seen[item.category] = None
    return list(seen.keys())


def items_for_category(
    items: Iterable[CatalogItem],
    category: str,
    mode: str | None = None,
) -> List[CatalogItem]:
    """Return catalog items for a category, optionally mode-filtered."""
    matches = [item for item in items if item.category == category]
    if mode:
        matches = [item for item in matches if item.mode == mode]
    return matches


def search_catalog(items: Iterable[CatalogItem], term: str) -> List[CatalogItem]:
    """Return catalog items whose id, category, label, or dork matches ``term``.

    Matching is case-insensitive and substring-based for fast terminal lookups.
    An empty term returns all items unchanged.
    """
    needle = term.strip().lower()
    if not needle:
        return list(items)
    matches: List[CatalogItem] = []
    for item in items:
        haystack = " ".join(
            (item.id, item.category, item.label, item.dork)
        ).lower()
        if needle in haystack:
            matches.append(item)
    return matches


def get_by_id(items: Iterable[CatalogItem], item_id: str) -> CatalogItem | None:
    """Return catalog item by stable id."""
    for item in items:
        if item.id == item_id:
            return item
    return None


def compose_query(
    dork_code: str,
    mode: str,
    domain: str = "",
    keyword: str = "",
) -> str:
    """Compose query text mirroring upstream dork assembly semantics."""
    query_parts: List[str] = []
    clean_domain = domain.strip()
    clean_keyword = keyword.strip()

    if mode == "sec" and clean_domain and "site:" not in dork_code:
        query_parts.append(f"site:{clean_domain}")
    if clean_keyword:
        query_parts.append(f"\"{clean_keyword}\"")
    query_parts.append(dork_code.strip())
    return " ".join(part for part in query_parts if part).strip()


def build_google_url(query: str) -> str:
    """Build executable Google search URL for a query."""
    return f"https://www.google.com/search?q={quote_plus(query)}"
