"""Input validation and normalization helpers."""

from __future__ import annotations

import re
from typing import List


_DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
_TOKEN_RE = re.compile(r"^[a-zA-Z0-9\-\._\s]+$")


def normalize_domain(value: str) -> str:
    value = value.strip().lower()
    value = value.removeprefix("https://").removeprefix("http://")
    value = value.rstrip("/")
    return value


def validate_domain(value: str) -> str:
    domain = normalize_domain(value)
    if not domain:
        return ""
    if not _DOMAIN_RE.match(domain):
        raise ValueError("Domain must look like example.com")
    return domain


def split_csv(value: str) -> List[str]:
    if not value.strip():
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def sanitize_token(value: str) -> str:
    token = value.strip()
    if not token:
        return ""
    if not _TOKEN_RE.match(token):
        raise ValueError(f"Unsupported characters in token: {value!r}")
    return token


def sanitize_many(values: List[str]) -> List[str]:
    return [token for token in (sanitize_token(value) for value in values) if token]

