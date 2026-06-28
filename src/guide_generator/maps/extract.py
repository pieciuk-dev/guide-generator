"""Extract placemark fields from traveler-facing guide notes."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

_WIKI_LINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
_MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_FRONTMATTER = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)

# (56.552667, 16.639778) or (56.552667, 16.639778) with spaces
_DECIMAL_IN_PARENS = re.compile(r"\(\s*(-?\d{1,2}\.\d+)\s*,\s*(\d{1,3}\.\d+)\s*\)")
# 56.52804, 16.51992 or ~57.22247, 16.95231
_DECIMAL_PAIR = re.compile(r"~?\s*(-?\d{1,2}\.\d+)\s*,\s*(\d{1,3}\.\d+)")
# 56°23′9.16″N, 16°25′59.0″E
# Decimal with degree symbol: 56.48°N, 16.52°E
_DEC_DEG = re.compile(
    r"(-?\d{1,2}\.\d+)\s*°\s*([NS])\s*,?\s*(\d{1,3}\.\d+)\s*°\s*([EW])",
    re.I,
)
_DMS = re.compile(
    r"(\d{1,2})°\s*(\d{1,2})[′']\s*([\d.]+)\s*[″\"]\s*([NS])\s*,\s*"
    r"(\d{1,3})°\s*(\d{1,2})[′']\s*([\d.]+)\s*[″\"]\s*([EW])",
    re.I,
)

_CONTENTS = re.compile(r"^## Contents\s*$", re.MULTILINE)
_SECTION = re.compile(r"^### (.+)$", re.MULTILINE)
_TABLE_ROW = re.compile(r"^\|\s*\[\[([^\]|]+)(?:\|[^\]]+)?\]\]\s*\|", re.MULTILINE)


@dataclass
class Placemark:
    slug: str
    name: str
    description: str
    latitude: float
    longitude: float
    layer: str
    priority: str
    site_type: str
    coords_note: str = ""


def strip_frontmatter(text: str) -> str:
    return _FRONTMATTER.sub("", text, count=1)


def section(text: str, *names: str) -> str:
    for name in names:
        m = re.search(rf"## {re.escape(name)}.*?\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""


def plain_text(text: str) -> str:
    text = _WIKI_LINK.sub(lambda m: m.group(2) or m.group(1).replace("-", " "), text)
    text = _MD_LINK.sub(r"\1", text)
    text = _BOLD.sub(r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_title(text: str) -> str:
    fm = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if fm:
        return fm.group(1).strip()
    m = re.search(r"^# (.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def parse_priority_type(text: str) -> tuple[str, str]:
    m = re.search(r"\*\*Priority:\*\*\s*(\w+)\s*·\s*\*\*Type:\*\*\s*(.+)", text)
    if m:
        return m.group(1).strip(), plain_text(m.group(2))
    return "", ""


def parse_overview(text: str, max_len: int = 240) -> str:
    block = section(text, "Overview")
    if not block:
        return ""
    first = block.split("\n\n")[0].strip()
    first = plain_text(first)
    if len(first) > max_len:
        cut = first[: max_len - 1].rsplit(" ", 1)[0]
        return cut + "…"
    return first


def _dms_to_decimal(deg: float, minutes: float, seconds: float, hemi: str) -> float:
    val = deg + minutes / 60 + seconds / 3600
    if hemi.upper() in ("S", "W"):
        val = -val
    return round(val, 6)


def parse_coordinates(text: str) -> tuple[float, float, str] | None:
    """Return (lat, lng, note) from Location, Facts, or full text."""
    for block in (
        section(text, "Location & access", "Location"),
        section(text, "Facts (sourced)", "Facts"),
        text,
    ):
        if not block:
            continue
        result = _coords_from_text(block)
        if result:
            return result
    return None


def _coords_from_text(haystack: str) -> tuple[float, float, str] | None:
    coord_parts: list[str] = []
    for line in haystack.splitlines():
        if re.search(r"Coordinates", line, re.I):
            m = re.search(r"Coordinates[^:]*:\s*(.+)", line, re.I)
            if m:
                coord_parts.append(m.group(1).strip())
    search = " ".join(coord_parts) if coord_parts else haystack

    m = _DECIMAL_IN_PARENS.search(search)
    if m:
        lat, lng = float(m.group(1)), float(m.group(2))
        if _valid_wgs84(lat, lng):
            note = "representative" if "representative" in search.lower() else ""
            return lat, lng, note

    for m in _DECIMAL_PAIR.finditer(search):
        lat, lng = float(m.group(1)), float(m.group(2))
        if _valid_wgs84(lat, lng):
            note = "representative" if "representative" in search.lower() else ""
            return lat, lng, note

    m = _DEC_DEG.search(search)
    if m:
        lat = float(m.group(1))
        if m.group(2).upper() == "S":
            lat = -lat
        lng = float(m.group(3))
        if m.group(4).upper() == "W":
            lng = -lng
        if _valid_wgs84(lat, lng):
            note = "representative" if "representative" in search.lower() or "approx" in search.lower() else ""
            return lat, lng, note

    m = _DMS.search(search)
    if m:
        lat = _dms_to_decimal(float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4))
        lng = _dms_to_decimal(float(m.group(5)), float(m.group(6)), float(m.group(7)), m.group(8))
        if _valid_wgs84(lat, lng):
            note = "representative" if "representative" in search.lower() else ""
            return lat, lng, note

    return None


def _valid_wgs84(lat: float, lng: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lng <= 180 and not (math.isclose(lat, 0) and math.isclose(lng, 0))


def parse_layers_from_index(index_text: str) -> dict[str, str]:
    """Map slug → Layer name from ### headings under ## Contents."""
    m = _CONTENTS.search(index_text)
    if not m:
        return {}
    tail = index_text[m.end() :]
    stop = re.search(r"^## (?:Suggested|routes|Further reading|Island-wide)", tail, re.MULTILINE | re.I)
    if stop:
        tail = tail[: stop.start()]

    layers: dict[str, str] = {}
    current = "Sites"
    pos = 0
    for match in re.finditer(r"^### (.+)$", tail, re.MULTILINE):
        if match.start() > pos:
            chunk = tail[pos : match.start()]
            for row in _TABLE_ROW.finditer(chunk):
                layers[row.group(1).strip()] = current
        current = match.group(1).strip()
        pos = match.end()
    chunk = tail[pos:]
    for row in _TABLE_ROW.finditer(chunk):
        layers[row.group(1).strip()] = current
    return layers


def parse_table_meta(index_text: str) -> dict[str, tuple[str, str]]:
    """slug → (priority, note/type from index table)."""
    meta: dict[str, tuple[str, str]] = {}
    for line in index_text.splitlines():
        if not line.startswith("| [[") or "---" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        wiki = re.match(r"\[\[([^\]|]+)", parts[0])
        if wiki:
            meta[wiki.group(1).strip()] = (parts[1], parts[2])
    return meta


def extract_placemark(
    slug: str,
    topic_dir: Path,
    *,
    layer: str,
    table_priority: str = "",
    table_type: str = "",
) -> Placemark | None:
    path = topic_dir / f"{slug}.md"
    research_path = topic_dir / "_ai" / "research" / f"{slug}.md"
    if not path.is_file() and not research_path.is_file():
        return None
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    research_text = (
        research_path.read_text(encoding="utf-8") if research_path.is_file() else ""
    )
    coords = parse_coordinates(text) if text else None
    if not coords and research_text:
        coords = parse_coordinates(research_text)
    if not coords:
        return None
    lat, lng, coords_note = coords
    priority, site_type = parse_priority_type(text)
    if table_priority:
        priority = table_priority
    if table_type:
        site_type = table_type
    name = parse_title(text) or parse_title(research_text) or slug.replace("-", " ").title()
    desc = parse_overview(text) or parse_overview(research_text)
    if coords_note:
        desc = f"{desc} (representative point)".strip() if desc else "Representative map point"
    return Placemark(
        slug=slug,
        name=name,
        description=desc,
        latitude=lat,
        longitude=lng,
        layer=layer,
        priority=priority,
        site_type=site_type,
        coords_note=coords_note,
    )


def ordered_slugs(index_text: str) -> list[str]:
    m = _CONTENTS.search(index_text)
    if not m:
        return []
    tail = index_text[m.end() :]
    stop = re.search(r"^## (?:Suggested|routes|Further reading|Island-wide)", tail, re.MULTILINE | re.I)
    if stop:
        tail = tail[: stop.start()]
    slugs: list[str] = []
    seen: set[str] = set()
    for hit in re.finditer(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]", tail):
        slug = hit.group(1).strip()
        if slug not in seen:
            seen.add(slug)
            slugs.append(slug)
    return slugs
