"""CLI for generating Google dork queries."""

from __future__ import annotations

import argparse
import sys
from typing import List

from dorkgen.builder import DorkRequest, build_dorks
from dorkgen.templates import TEMPLATES, objective_choices
from dorkgen.validators import split_csv, validate_domain


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
    print("\nGenerated dorks (copy and paste into Google):")
    for idx, dork in enumerate(dorks, start=1):
        print(f"{idx}. {dork}")


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)
    try:
        request = _interactive_prompt() if args.interactive or not args.objective else _from_flags(args)
        dorks = build_dorks(request)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    _print_output(dorks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

