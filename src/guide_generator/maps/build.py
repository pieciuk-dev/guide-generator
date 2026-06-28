"""Build Google My Maps CSV from a topic folder."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from guide_generator.maps.coords_yaml import load_coord_overrides
from guide_generator.maps.extract import (
    Placemark,
    extract_placemark,
    ordered_slugs,
    parse_layers_from_index,
    parse_overview,
    parse_table_meta,
    parse_title,
)

# Column order tuned for Google My Maps import wizard:
# - Name → title markers
# - Description → info window
# - Latitude / Longitude → position
# - Layer → "Style by data column" for icons / colours per group
CSV_COLUMNS = [
    "Name",
    "Description",
    "Latitude",
    "Longitude",
    "Layer",
    "Priority",
    "Type",
    "Slug",
]


@dataclass
class BuildResult:
    csv_path: Path
    placemarks: list[Placemark]
    skipped: list[tuple[str, str]]


def build_map_csv(topic_dir: Path, output: Path | None = None) -> BuildResult:
    """Write a single My Maps-ready CSV. Returns path and any skipped slugs."""
    topic_dir = topic_dir.resolve()
    index_path = topic_dir / "index.md"
    if not index_path.is_file():
        raise FileNotFoundError(f"Not a topic folder (no index.md): {topic_dir}")

    index_text = index_path.read_text(encoding="utf-8")
    layers = parse_layers_from_index(index_text)
    table_meta = parse_table_meta(index_text)
    slugs = ordered_slugs(index_text)
    if not slugs:
        slugs = sorted(
            p.stem for p in topic_dir.glob("*.md") if p.stem != "index"
        )

    placemarks: list[Placemark] = []
    skipped: list[tuple[str, str]] = []
    overrides = load_coord_overrides(topic_dir)

    for slug in slugs:
        layer = layers.get(slug, "Other")
        tp, tt = table_meta.get(slug, ("", ""))
        pm = extract_placemark(
            slug, topic_dir, layer=layer, table_priority=tp, table_type=tt
        )
        if not pm and slug in overrides:
            o = overrides[slug]
            path = topic_dir / f"{slug}.md"
            research_path = topic_dir / "_ai" / "research" / f"{slug}.md"
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            research_text = (
                research_path.read_text(encoding="utf-8")
                if research_path.is_file()
                else ""
            )
            name = (
                o.get("name")
                or parse_title(text)
                or parse_title(research_text)
                or slug.replace("-", " ").title()
            )
            desc = o.get("description") or parse_overview(text) or parse_overview(research_text)
            note = o.get("note", "override")
            if note == "override" and o.get("note"):
                note = str(o["note"])
            if note and note != "override" and desc:
                desc = f"{desc} ({note})"
            elif note and note != "override":
                desc = note
            pm = Placemark(
                slug=slug,
                name=name,
                description=desc or name,
                latitude=float(o["latitude"]),
                longitude=float(o["longitude"]),
                layer=layer,
                priority=tp or str(o.get("priority", "")),
                site_type=tt or str(o.get("type", "")),
                coords_note=note if note != "override" else "override",
            )
        if pm:
            placemarks.append(pm)
        else:
            skipped.append((slug, "no parseable coordinates"))

    out = output or (topic_dir / "guide_map.csv")
    out = out.resolve()
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for pm in placemarks:
            writer.writerow(
                {
                    "Name": pm.name,
                    "Description": pm.description,
                    "Latitude": f"{pm.latitude:.6f}",
                    "Longitude": f"{pm.longitude:.6f}",
                    "Layer": pm.layer,
                    "Priority": pm.priority,
                    "Type": pm.site_type,
                    "Slug": pm.slug,
                }
            )

    return BuildResult(csv_path=out, placemarks=placemarks, skipped=skipped)
