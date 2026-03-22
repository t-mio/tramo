from __future__ import annotations
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

def _default_tram_json_path() -> Path:
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "storage" / "data" / "tram.json"

def _resolve_tram_json_path() -> Path:
    env_path = os.environ.get("TRAM_JSON_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return _default_tram_json_path().resolve()

@lru_cache(maxsize=1)
def get_tram_data() -> Any:
    file_path = _resolve_tram_json_path()
    if not file_path.exists():
        raise FileNotFoundError(
            f"tram.json not found at '{file_path}'. "
            "Set TRAM_JSON_PATH to override the location if needed."
        )
    with file_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)

def reload_tram_data() -> Any:
    get_tram_data.cache_clear()
    return get_tram_data()

__all__ = ["get_tram_data", "reload_tram_data"]