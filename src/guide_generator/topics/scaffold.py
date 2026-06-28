from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import yaml

from guide_generator.audiences.resolve import write_resolved_profile

_REPO_ROOT = Path(__file__).resolve().parents[3]
_TOPICS_DIR = _REPO_ROOT / "topics"
_TRIPS_DIR = _REPO_ROOT / "data" / "trips"


@dataclass(frozen=True)
class TripInput:
    id: str
    region: dict
    audience: str
    dates: dict | None = None
    notes: list | None = None
    raw: dict | None = None


def load_trip(path: Path) -> TripInput:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    trip_id = str(data.get("id", path.stem))
    region = data.get("region")
    if not region or not region.get("name"):
        raise ValueError(f"{path}: region.name is required")
    audience = data.get("audience")
    if not audience:
        raise ValueError(f"{path}: audience is required")
    return TripInput(
        id=trip_id,
        region=region,
        audience=str(audience),
        dates=data.get("dates"),
        notes=data.get("notes") or [],
        raw=data,
    )


def init_topic(trip_path: Path, topics_dir: Path | None = None) -> Path:
    """Create topic folder structure and write _ai/input.yaml + audience_profile.md."""
    trip = load_trip(trip_path)
    base = topics_dir or _TOPICS_DIR
    topic_dir = base / trip.id

    if topic_dir.exists() and any(topic_dir.iterdir()):
        raise FileExistsError(
            f"Topic folder already exists and is not empty: {topic_dir}. "
            "Use a new trip id or remove the folder manually."
        )

    ai_dir = topic_dir / "_ai"
    attachments = topic_dir / "attachments" / "images"
    audio_dir = topic_dir / "attachments" / "audio"
    for d in (ai_dir, attachments, audio_dir, ai_dir / "research"):
        d.mkdir(parents=True, exist_ok=True)

    shutil.copy2(trip_path, ai_dir / "input.yaml")
    write_resolved_profile(trip.audience, ai_dir / "audience_profile.md")

    att_path = attachments / "ATTRIBUTION.md"
    if not att_path.exists():
        att_path.write_text(
            "\n".join(
                [
                    f"# Image attribution — {trip.id}",
                    "",
                    "Running manifest for CC/public-domain downloads (Phase 2).",
                    "",
                    "| Slug | File | Author | License | Commons | Local path |",
                    "|------|------|--------|---------|---------|------------|",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    research_template = ai_dir / "research" / "_TEMPLATE.md"
    repo_template = _REPO_ROOT / "topics" / "_template" / "_ai" / "research" / "_TEMPLATE.md"
    if repo_template.is_file() and not research_template.exists():
        shutil.copy2(repo_template, research_template)

    map_coords = ai_dir / "map_coords.yaml"
    if not map_coords.exists():
        map_coords.write_text(
            "\n".join(
                [
                    "# Optional WGS84 fallbacks when guide notes lack parseable coordinates.",
                    "# Used by: python -m guide_generator.maps <topic_id>",
                    "",
                    "sites: {}",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    site_list = ai_dir / "site_list.md"
    site_list.write_text(
        "\n".join(
            [
                f"# Site list: {trip.id}",
                "",
                "Status: draft",
                "",
                "| # | Site / subject | Slug | Priority | Why include | Phase 2 |",
                "|---|----------------|------|----------|-------------|---------|",
                "",
            ]
        ),
        encoding="utf-8",
    )

    worklog = ai_dir / "worklog.md"
    region_name = trip.region.get("name", trip.id)
    worklog.write_text(
        "\n".join(
            [
                f"# Worklog: {trip.id}",
                "",
                f"- **Region:** {region_name}",
                f"- **Audience:** {trip.audience}",
                f"- **Initialized:** from `{trip_path.name}`",
                f"- **Build process:** [GUIDE_BUILD_PROCESS.md](../../../docs/GUIDE_BUILD_PROCESS.md)",
                "",
                "## Phase 1 — Discovery",
                "",
                "Status: not started",
                "",
                "- _Initial research and `site_list.md`._",
                "",
                "## Phase 2 — Deep dive",
                "",
                "Status: not started",
                "",
                "## Phase 3 — Compile",
                "",
                "Status: not started",
                "",
                "## Sources",
                "",
                "| Date | Source | Phase | Used for |",
                "|------|--------|-------|----------|",
                "",
            ]
        ),
        encoding="utf-8",
    )

    index = topic_dir / "index.md"
    index.write_text(
        "\n".join(
            [
                "---",
                f"title: {region_name}",
                f"topic: {trip.id}",
                f"audience: {trip.audience}",
                "tags:",
                "  - guide",
                "---",
                "",
                f"# {region_name}",
                "",
                f"Travel guide for **{trip.audience}** audience.",
                "",
                "## Contents",
                "",
                "_Sections will be linked here as notes are created._",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return topic_dir


def refresh_topic_profile(topic_id: str, topics_dir: Path | None = None) -> Path:
    """Regenerate topics/<id>/_ai/audience_profile.md from current audience definitions."""
    base = topics_dir or _TOPICS_DIR
    topic_dir = base / topic_id
    input_yaml = topic_dir / "_ai" / "input.yaml"
    profile_path = topic_dir / "_ai" / "audience_profile.md"

    if not input_yaml.is_file():
        raise FileNotFoundError(f"Topic not found or missing _ai/input.yaml: {topic_dir}")

    data = yaml.safe_load(input_yaml.read_text(encoding="utf-8")) or {}
    audience = data.get("audience")
    if not audience:
        raise ValueError(f"{input_yaml}: audience field is required")

    write_resolved_profile(str(audience), profile_path)
    return profile_path
