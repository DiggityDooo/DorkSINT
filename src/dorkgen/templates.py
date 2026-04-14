"""Intent templates for Google dork generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DorkTemplate:
    name: str
    terms: List[str]
    inurl: List[str]
    intitle: List[str]
    filetypes: List[str]
    include_index: bool = False
    include_open_directory_hint: bool = False


TEMPLATES: Dict[str, DorkTemplate] = {
    "public-documents": DorkTemplate(
        name="Public Documents",
        terms=["confidential", "internal use only", "do not distribute"],
        inurl=["docs", "uploads", "files"],
        intitle=["index of", "documents"],
        filetypes=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "txt"],
        include_index=True,
    ),
    "login-portals": DorkTemplate(
        name="Login Portals",
        terms=["login", "signin", "admin"],
        inurl=["login", "admin", "auth"],
        intitle=["login", "sign in", "admin panel"],
        filetypes=[],
    ),
    "public-backups": DorkTemplate(
        name="Public Backups",
        terms=["backup", "db dump", "archive"],
        inurl=["backup", "dump", "export"],
        intitle=["index of", "backup"],
        filetypes=["sql", "zip", "tar", "gz", "bak"],
        include_index=True,
        include_open_directory_hint=True,
    ),
    "configuration-files": DorkTemplate(
        name="Configuration Files",
        terms=["password", "apikey", "token"],
        inurl=["config", ".env", "settings"],
        intitle=["index of", "config"],
        filetypes=["env", "ini", "yml", "yaml", "json", "xml"],
        include_index=True,
    ),
}


def objective_choices() -> Dict[str, str]:
    """Map numeric prompt selection to template keys."""
    return {
        "1": "public-documents",
        "2": "login-portals",
        "3": "public-backups",
        "4": "configuration-files",
    }

