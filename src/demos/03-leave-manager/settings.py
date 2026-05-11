"""Load demo configuration from JSON (shared by server and client)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_CONFIG_PATH = Path(__file__).resolve().parent / "config" / "settings.json"


def load_config() -> dict[str, Any]:
    """Return settings from ``config/settings.json`` next to this package."""
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
