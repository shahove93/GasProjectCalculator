"""Filesystem helpers for resolving bundled application resources.

In a PyInstaller build the frontend static files live inside the bundle
directory exposed as ``sys._MEIPASS``.  In development they live in the
repository next to the ``app`` package.  Keeping the lookup in one place lets
``app.main`` serve ``frontend/index.html`` unchanged in both modes.
"""

from __future__ import annotations

import sys
from pathlib import Path


def app_base_dir() -> Path:
    """Return the directory that contains bundled/static resources."""

    bundle_dir = getattr(sys, "_MEIPASS", None)
    if bundle_dir:
        return Path(bundle_dir)
    return Path(__file__).resolve().parent.parent


def frontend_index_path() -> Path:
    """Return the absolute path to ``frontend/index.html``.

    Raises ``FileNotFoundError`` with a readable message if the file is
    missing, so a broken package fails loudly instead of serving a 500.
    """

    path = app_base_dir() / "frontend" / "index.html"
    if not path.is_file():
        raise FileNotFoundError(
            f"Frontend file not found: {path}. "
            "Rebuild the packaged application with packaging/build.ps1."
        )
    return path
