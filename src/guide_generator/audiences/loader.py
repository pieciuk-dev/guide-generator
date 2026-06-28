from __future__ import annotations

from pathlib import Path

import yaml

from guide_generator.audiences.models import AudienceDefinition

_DEFAULT_AUDIENCES_DIR = Path(__file__).resolve().parents[3] / "audiences"


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return meta, body


def load_audience(audience_id: str, audiences_dir: Path | None = None) -> AudienceDefinition:
    base = audiences_dir or _DEFAULT_AUDIENCES_DIR
    path = base / f"{audience_id}.md"
    if not path.is_file():
        raise FileNotFoundError(f"Audience not found: {audience_id} ({path})")

    meta, body = _split_frontmatter(path.read_text(encoding="utf-8"))
    copy_from = meta.get("copy_from") or []
    parent = meta.get("parent")
    if parent in ("", "null", None):
        parent = None

    return AudienceDefinition(
        id=str(meta.get("id", audience_id)),
        parent=parent,
        copy_from=tuple(copy_from),
        body=body,
        path=str(path.resolve()),
    )


def load_all_audiences(audiences_dir: Path | None = None) -> dict[str, AudienceDefinition]:
    base = audiences_dir or _DEFAULT_AUDIENCES_DIR
    audiences: dict[str, AudienceDefinition] = {}
    for path in sorted(base.glob("*.md")):
        if path.name.startswith("_"):
            continue
        audience = load_audience(path.stem, base)
        if audience.id in audiences:
            raise ValueError(f"duplicate audience id {audience.id!r}")
        audiences[audience.id] = audience
    return audiences
