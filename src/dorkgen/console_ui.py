"""Prompt-based console UI for DorkSINT catalog browsing."""

from __future__ import annotations

import shutil
import textwrap
import webbrowser
from typing import Iterable, List, Sequence

from dorkgen.catalog import CatalogItem, build_google_url, compose_query
from dorkgen.templates import TEMPLATES


def _supports_unicode() -> bool:
    import sys
    try:
        encoding = sys.stdout.encoding or ""
        if encoding.lower().replace("-", "") not in ("utf8", "utf16", "utf32"):
            return False
    except Exception:
        return False
    return shutil.get_terminal_size((80, 24)).columns >= 70


def _frame_lines(title: str, lines: Sequence[str]) -> str:
    width = max(72, min(110, shutil.get_terminal_size((80, 24)).columns))
    inner = width - 4
    if _supports_unicode():
        top_left, top_right, bottom_left, bottom_right, horizontal, vertical = "┌", "┐", "└", "┘", "─", "│"
    else:
        top_left = top_right = bottom_left = bottom_right = "+"
        horizontal = "-"
        vertical = "|"

    wrapped: List[str] = []
    for line in lines:
        chunks = textwrap.wrap(line, width=inner) or [""]
        wrapped.extend(chunks)

    result = [
        f"{top_left}{horizontal * (width - 2)}{top_right}",
        f"{vertical} {title[:inner].ljust(inner)} {vertical}",
        f"{vertical}{horizontal * (width - 2)}{vertical}",
    ]
    result.extend(f"{vertical} {line.ljust(inner)} {vertical}" for line in wrapped)
    result.append(f"{bottom_left}{horizontal * (width - 2)}{bottom_right}")
    return "\n".join(result)


def _choose_from_list(prompt: str, options: Sequence[str]) -> int:
    while True:
        print(prompt)
        for idx, value in enumerate(options, start=1):
            print(f"{idx}. {value}")
        raw = input("Select number: ").strip()
        if raw.isdigit():
            index = int(raw)
            if 1 <= index <= len(options):
                return index - 1
        print("Invalid selection. Try again.\n")


def prompt_home_choice() -> str:
    """Prompt for experience mode."""
    options = ["Classic templates", "Catalog browser"]
    idx = _choose_from_list("How would you like to generate dorks?", options)
    return "classic" if idx == 0 else "catalog"


def run_catalog_browser(
    items: Iterable[CatalogItem],
    include_file_hunter: bool,
    preset_domain: str = "",
    preset_keyword: str = "",
) -> str:
    """Run interactive catalog browser and return selected query."""
    all_items = list(items)
    if not all_items:
        raise ValueError("Catalog is empty.")

    modes = ["sec"] + (["media"] if include_file_hunter else [])
    chosen_mode = modes[_choose_from_list("Select catalog mode:", ["CYBER_INTEL (sec)"] + (["FILE_HUNTER (media)"] if include_file_hunter else []))]
    categories = []
    for item in all_items:
        if item.mode == chosen_mode and item.category not in categories:
            categories.append(item.category)

    category = categories[_choose_from_list("Select category:", categories)]
    category_items = [item for item in all_items if item.mode == chosen_mode and item.category == category]
    item_labels = [f"{item.label} [{item.id}]" for item in category_items]
    selected = category_items[_choose_from_list("Select dork:", item_labels)]

    domain = preset_domain.strip() or input("Domain (optional, ex: example.com): ").strip()
    keyword = preset_keyword.strip() or input("Keyword (optional): ").strip()
    query = compose_query(selected.dork, selected.mode, domain=domain, keyword=keyword)
    url = build_google_url(query)
    print()
    print(_frame_lines("DorkSINT Query Preview", [f"Catalog ID: {selected.id}", f"Category: {selected.category}", f"Label: {selected.label}", "", "Query:", query, "", "Google URL:", url]))
    open_answer = input("Open this search in your browser now? [y/N]: ").strip().lower()
    if open_answer == "y":
        webbrowser.open(url)
    return query


def print_output_panel(dorks: Sequence[str]) -> None:
    lines = ["Generated dorks (copy and paste into Google):", ""]
    lines.extend(f"{idx}. {dork}" for idx, dork in enumerate(dorks, start=1))
    print()
    print(_frame_lines("DorkSINT Output", lines))


def print_supported_objectives() -> None:
    lines = [f"- {key}: {template.name}" for key, template in TEMPLATES.items()]
    print(_frame_lines("Objectives", lines))
