"""CLI for generating Google dork queries."""

from __future__ import annotations

import argparse
import sys
from typing import List

from dorkgen.builder import DorkRequest, build_dorks
from dorkgen.catalog import compose_query, get_by_id, load_catalog
from dorkgen.console_ui import print_output_panel, prompt_home_choice, run_catalog_browser
from dorkgen.templates import TEMPLATES, objective_choices
from dorkgen.validators import split_csv, validate_domain

# Exit codes
EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USER_INPUT = 2
EXIT_INTERRUPT = 130


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="dorkgen",
        description="Generate copy-ready Google dork queries.",
    )
    parser.add_argument("--objective", choices=TEMPLATES.keys(), help="Objective key.")
    parser.add_argument("--domain", default="", help="Target domain like example.com")
    parser.add_argument("--keyword", default="", help="Keyword or phrase to prioritize")
    parser.add_argument("--filetypes", default="", help="CSV list: pdf,docx,sql")
    parser.add_argument("--exclude", default="", help="CSV list of exclusion terms")
    parser.add_argument("--menu", action="store_true", help="Use menu-based console UI.")
    parser.add_argument(
        "--include-file-hunter",
        action="store_true",
        help="Include FILE_HUNTER (media) catalog entries.",
    )
    parser.add_argument("--catalog-id", default="", help="Run a specific catalog item by id.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Force interactive prompts even when flags are provided.",
    )
    return parser.parse_args(argv)


def _print_objective_menu() -> None:
    print("What are you trying to find?")
    for number, key in objective_choices().items():
        print(f"{number}. {TEMPLATES[key].name} ({key})")


def _interactive_objective() -> str:
    mapping = objective_choices()
    while True:
        _print_objective_menu()
        selection = input("Choose objective number: ").strip()
        if selection in mapping:
            return mapping[selection]
        print("Invalid selection. Try again.\n")


def _interactive_prompt() -> DorkRequest:
    objective = _interactive_objective()
    domain = input("Domain (optional, e.g. example.com): ").strip()
    keyword = input("Keyword or phrase (optional): ").strip()
    filetypes_raw = input("Filetypes CSV (optional, e.g. pdf,docx): ").strip()
    exclude_raw = input("Exclude terms CSV (optional): ").strip()

    return DorkRequest(
        objective_key=objective,
        domain=validate_domain(domain),
        keyword=keyword,
        filetypes=split_csv(filetypes_raw),
        exclude_terms=split_csv(exclude_raw),
    )


def _from_flags(args: argparse.Namespace) -> DorkRequest:
    if not args.objective:
        raise ValueError("--objective is required in non-interactive mode.")
    return DorkRequest(
        objective_key=args.objective,
        domain=validate_domain(args.domain),
        keyword=args.keyword.strip(),
        filetypes=split_csv(args.filetypes),
        exclude_terms=split_csv(args.exclude),
    )


def _print_output(dorks: List[str]) -> None:
    print_output_panel(dorks)


def _run_catalog_from_id(args: argparse.Namespace) -> List[str]:
    items = load_catalog(include_file_hunter=args.include_file_hunter)
    item = get_by_id(items, args.catalog_id)
    if item is None:
        raise ValueError(
            f"Unknown catalog id: {args.catalog_id}. Use --menu to browse available IDs."
        )
    query = compose_query(
        item.dork,
        mode=item.mode,
        domain=validate_domain(args.domain),
        keyword=args.keyword.strip(),
    )
    return [query]


def _run_menu(args: argparse.Namespace) -> List[str]:
    choice = prompt_home_choice() if args.interactive else "catalog"
    if choice == "classic":
        request = _interactive_prompt()
        return build_dorks(request)
    items = load_catalog(include_file_hunter=args.include_file_hunter)
    query = run_catalog_browser(
        items,
        include_file_hunter=args.include_file_hunter,
        preset_domain=validate_domain(args.domain),
        preset_keyword=args.keyword.strip(),
    )
    return [query]


def _validate_flag_conflicts(args: argparse.Namespace) -> str | None:
    """Return an error message if flags conflict, else None."""
    if args.catalog_id and args.menu:
        return "--catalog-id and --menu cannot be used together."
    if args.catalog_id and args.objective:
        return "--catalog-id and --objective cannot be used together."
    if args.menu and args.objective:
        return "--menu and --objective cannot be used together."
    return None


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    conflict = _validate_flag_conflicts(args)
    if conflict:
        print(f"Error: {conflict}", file=sys.stderr)
        return EXIT_USER_INPUT

    try:
        if args.catalog_id:
            dorks = _run_catalog_from_id(args)
        elif args.menu:
            dorks = _run_menu(args)
        elif args.interactive:
            use_catalog = input("Use catalog browser? [y/N]: ").strip().lower() == "y"
            if use_catalog:
                dorks = _run_menu(args)
            else:
                dorks = build_dorks(_interactive_prompt())
        else:
            request = _from_flags(args)
            dorks = build_dorks(request)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_USER_INPUT
    except KeyboardInterrupt:
        print("\nCancelled by user.", file=sys.stderr)
        return EXIT_INTERRUPT

    _print_output(dorks)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())

