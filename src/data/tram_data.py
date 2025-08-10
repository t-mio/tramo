"""Shared loader for `storage/data/tram.json`.

Provides cached access to tram data from anywhere in the app.

Usage:
    from data.tram_data import get_tram_data, reload_tram_data
    data = get_tram_data()

Environment override:
    Set `TRAM_JSON_PATH` to point to a custom json file if needed.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any


def _default_tram_json_path() -> Path:
    """Resolve the default path to `storage/data/tram.json`.

    This resolves relative to the project root assuming this file lives in
    `src/data/tram_data.py`.
    """
    # `.../my-app/src/data/tram_data.py` → project root is parents[2]
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "storage" / "data" / "tram.json"


def _resolve_tram_json_path() -> Path:
    """Resolve the tram json path with environment override.

    TRAM_JSON_PATH can be an absolute or relative path. Relative paths are
    resolved against the current working directory.
    """
    env_path = os.environ.get("TRAM_JSON_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return _default_tram_json_path().resolve()


@lru_cache(maxsize=1)
def get_tram_data() -> Any:
    """Load and cache the tram json data.

    Returns the parsed JSON (dict or list depending on file contents).
    Subsequent calls return the cached object. Use `reload_tram_data()` to
    refresh.
    """
    file_path = _resolve_tram_json_path()
    if not file_path.exists():
        raise FileNotFoundError(
            f"tram.json not found at '{file_path}'. "
            "Set TRAM_JSON_PATH to override the location if needed."
        )
    with file_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def reload_tram_data() -> Any:
    """Clear the cache and reload the tram data.

    Returns the freshly loaded data.
    """
    get_tram_data.cache_clear()  # type: ignore[attr-defined]
    return get_tram_data()


__all__ = [
    "get_tram_data",
    "reload_tram_data",
]


