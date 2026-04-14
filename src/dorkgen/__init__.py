"""Public package API for google-dork-cli."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from dorkgen.builder import DorkRequest, build_dorks

try:
    __version__ = version("google-dork-cli")
except PackageNotFoundError:
    # Editable/local execution without installed package metadata.
    __version__ = "0.0.0"

__all__ = ["DorkRequest", "build_dorks", "__version__"]

