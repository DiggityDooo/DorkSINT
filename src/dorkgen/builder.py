"""Build Google dork query strings from intent and user input."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from dorkgen.templates import DorkTemplate, TEMPLATES
from dorkgen.validators import sanitize_many


@dataclass
class DorkRequest:
    objective_key: str
    domain: str = ""
    keyword: str = ""
    filetypes: List[str] | None = None
    exclude_terms: List[str] | None = None


def _q(term: str) -> str:
    return f"\"{term}\"" if " " in term else term


def _unique_ordered(tokens: Iterable[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for token in tokens:
        if token and token not in seen:
            seen.add(token)
            result.append(token)
    return result


def build_dorks(request: DorkRequest) -> List[str]:
    if request.objective_key not in TEMPLATES:
        raise ValueError("Unknown objective key.")

    template = TEMPLATES[request.objective_key]
    keyword = request.keyword.strip()
    user_filetypes = sanitize_many(request.filetypes or [])
    exclusions = sanitize_many(request.exclude_terms or [])

    dorks = [
        _build_primary(template, request.domain, keyword, user_filetypes, exclusions),
        _build_title_variant(template, request.domain, keyword, exclusions),
        _build_inurl_variant(template, request.domain, keyword, user_filetypes, exclusions),
    ]

    if template.include_open_directory_hint:
        dorks.append(_build_open_directory_variant(template, request.domain, exclusions))

    return _unique_ordered(dorks)


def _build_primary(
    template: DorkTemplate,
    domain: str,
    keyword: str,
    user_filetypes: List[str],
    exclusions: List[str],
) -> str:
    parts: List[str] = []
    if domain:
        parts.append(f"site:{domain}")

    focus_terms = _unique_ordered([keyword] if keyword else template.terms[:2])
    parts.extend(_q(term) for term in focus_terms if term)

    filetypes = _unique_ordered(user_filetypes or template.filetypes[:2])
    if filetypes:
        ft_block = " OR ".join(f"filetype:{ft}" for ft in filetypes)
        parts.append(f"({ft_block})")

    if template.include_index:
        parts.append("intitle:\"index of\"")

    parts.extend(f"-{_q(term)}" for term in exclusions)
    return " ".join(parts).strip()


def _build_title_variant(
    template: DorkTemplate,
    domain: str,
    keyword: str,
    exclusions: List[str],
) -> str:
    parts: List[str] = []
    if domain:
        parts.append(f"site:{domain}")

    title_term = keyword or template.intitle[0]
    parts.append(f"intitle:{_q(title_term)}")

    if template.terms:
        parts.append(_q(template.terms[0]))
    parts.extend(f"-{_q(term)}" for term in exclusions)
    return " ".join(parts).strip()


def _build_inurl_variant(
    template: DorkTemplate,
    domain: str,
    keyword: str,
    user_filetypes: List[str],
    exclusions: List[str],
) -> str:
    parts: List[str] = []
    if domain:
        parts.append(f"site:{domain}")

    url_term = keyword or template.inurl[0]
    parts.append(f"inurl:{_q(url_term)}")
    if keyword:
        parts.append(_q(keyword))

    filetypes = _unique_ordered(user_filetypes[:1] or template.filetypes[:1])
    if filetypes:
        parts.append(f"filetype:{filetypes[0]}")

    parts.extend(f"-{_q(term)}" for term in exclusions)
    return " ".join(parts).strip()


def _build_open_directory_variant(
    template: DorkTemplate,
    domain: str,
    exclusions: List[str],
) -> str:
    parts: List[str] = []
    if domain:
        parts.append(f"site:{domain}")
    parts.append("intitle:\"index of\"")
    parts.append("\"parent directory\"")
    if template.terms:
        parts.append(_q(template.terms[0]))
    parts.extend(f"-{_q(term)}" for term in exclusions)
    return " ".join(parts).strip()

