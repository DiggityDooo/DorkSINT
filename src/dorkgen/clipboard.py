"""Cross-platform clipboard support using common terminal utilities.

No third-party dependencies: we shell out to whatever clipboard helper the
host already provides. This keeps DorkSINT terminal-only and dependency-free
while still letting users copy a generated dork with a single flag.
"""

from __future__ import annotations

import shutil
import subprocess
from typing import List, Optional, Tuple

# Ordered by preference. Wayland first, then X11, then macOS, then Windows.
_CLIPBOARD_COMMANDS: List[Tuple[str, List[str]]] = [
    ("wl-copy", ["wl-copy"]),
    ("xclip", ["xclip", "-selection", "clipboard"]),
    ("xsel", ["xsel", "--clipboard", "--input"]),
    ("pbcopy", ["pbcopy"]),
    ("clip", ["clip"]),
]


def detect_clipboard_command() -> Optional[List[str]]:
    """Return the argv for the first available clipboard helper, or None."""
    for _name, command in _CLIPBOARD_COMMANDS:
        if shutil.which(command[0]):
            return command
    return None


def copy_to_clipboard(text: str) -> Optional[str]:
    """Copy ``text`` to the system clipboard.

    Returns the name of the helper used on success, or ``None`` when no
    clipboard tool is available or the copy fails.
    """
    command = detect_clipboard_command()
    if command is None:
        return None
    try:
        subprocess.run(
            command,
            input=text.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return command[0]
