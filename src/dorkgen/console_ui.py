"""Prompt-based console UI for DorkSINT catalog browsing."""

from __future__ import annotations

import os
import shutil
import sys
import textwrap
import webbrowser
from typing import Iterable, List, Optional, Sequence, TextIO

from dorkgen.catalog import CatalogItem, build_google_url, compose_query
from dorkgen.templates import TEMPLATES

# ANSI color codes used for terminal styling.
_RESET = "\x1b[0m"
_BORDER = "1;36"   # bold cyan
_TITLE = "1;37"    # bold white
_ACCENT = "1;32"   # bold green
_DIM = "2"         # dim

# Color override: None means auto-detect, True/False forces the behavior.
_COLOR_OVERRIDE: Optional[bool] = None


def set_color_override(value: Optional[bool]) -> None:
    """Force color on/off (True/False) or restore auto-detection (None)."""
    global _COLOR_OVERRIDE
    _COLOR_OVERRIDE = value


def _use_color(stream: Optional[TextIO] = None) -> bool:
    """Return True when ANSI color should be emitted to ``stream``."""
    stream = stream or sys.stdout
    if _COLOR_OVERRIDE is not None:
        if not _COLOR_OVERRIDE:
            return False
    else:
        if os.environ.get("NO_COLOR"):
            return False
        if os.environ.get("TERM", "") == "dumb":
            return False
    try:
        return bool(stream.isatty())
    except Exception:
        return False


def _colorize(text: str, code: str, stream: Optional[TextIO] = None) -> str:
    """Wrap ``text`` in an ANSI color code when color is enabled."""
    if not _use_color(stream):
        return text
    return f"\x1b[{code}m{text}{_RESET}"


def _supports_unicode() -> bool:
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

    if _use_color():
        # Color whole lines so the visible width math above stays correct
        # (ANSI escape codes are zero-width on screen).
        result[0] = _colorize(result[0], _BORDER)
        result[1] = _colorize(result[1], _TITLE)
        result[2] = _colorize(result[2], _BORDER)
        result[-1] = _colorize(result[-1], _BORDER)
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


_BANNER_UNICODE = r"""
 ____             _    ____ ___ _   _ _____
|  _ \  ___  _ __| | _/ ___|_ _| \ | |_   _|
| | | |/ _ \| '__| |/ \___ \| ||  \| | | |
| |_| | (_) | |  |   < ___) | || |\  | | |
|____/ \___/|_|  |_|\_\____/___|_| \_| |_|
"""

_BANNER_ASCII = r"""
 ___          _   ___ ___ _  _ _____
|   \ ___ _ _| |_/ __|_ _| \| |_   _|
| |) / _ \ '_| / \__ \| || .` | | |
|___/\___/_| |_\_\___/___|_|\_| |_|
"""

_TAGLINE = "Terminal-first Google dork generator  -  authorized recon only"


def print_banner(stream: Optional[TextIO] = None) -> None:
    """Print the DorkSINT banner. Defaults to stderr to keep stdout clean."""
    stream = stream or sys.stderr
    art = _BANNER_UNICODE if _supports_unicode() else _BANNER_ASCII
    print(_colorize(art, _BORDER, stream), file=stream)
    print(_colorize("  " + _TAGLINE, _DIM, stream), file=stream)
    print(file=stream)


def print_plain(dorks: Sequence[str], stream: Optional[TextIO] = None) -> None:
    """Print dorks one per line with no framing, ideal for piping/scripting."""
    stream = stream or sys.stdout
    for dork in dorks:
        print(dork, file=stream)


def format_catalog_lines(items: Sequence[CatalogItem]) -> List[str]:
    """Build one greppable line per catalog item: id, taxonomy, and dork."""
    if not items:
        return []
    id_width = max(len(item.id) for item in items)
    lines: List[str] = []
    for item in items:
        ident = _colorize(item.id.ljust(id_width), _ACCENT)
        taxonomy = f"{item.category} / {item.label}"
        sep = _colorize("::", _DIM)
        lines.append(f"{ident}  {taxonomy}  {sep}  {item.dork}")
    return lines


def print_catalog_list(
    items: Sequence[CatalogItem],
    stream: Optional[TextIO] = None,
) -> None:
    """Print catalog entries as greppable lines to stdout.

    Designed for fast terminal discovery, e.g. ``dorkgen --list | grep s3``.
    A short summary is written to stderr so it never pollutes a pipe.
    """
    stream = stream or sys.stdout
    for line in format_catalog_lines(items):
        print(line, file=stream)
    modes = sorted({item.mode for item in items})
    noun = "entry" if len(items) == 1 else "entries"
    summary = f"{len(items)} catalog {noun}  (modes: {', '.join(modes) or 'none'})"
    print(_colorize(summary, _DIM, sys.stderr), file=sys.stderr)
