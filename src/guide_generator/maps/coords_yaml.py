"""Load optional coordinate overrides from _ai/map_coords.yaml."""
from __future__ import annotations

from pathlib import Path

import yaml


def load_coord_overrides(topic_dir: Path) -> dict[str, dict]:
    path = topic_dir / "_ai" / "map_coords.yaml"
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    sites = data.get("sites", data)
    if not isinstance(sites, dict):
        return {}
    out: dict[str, dict] = {}
    for slug, entry in sites.items():
        if isinstance(entry, dict) and "latitude" in entry and "longitude" in entry:
            out[str(slug)] = entry
    return out
