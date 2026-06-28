"""Merge topic guide notes in reading order."""
from __future__ import annotations

import re
from pathlib import Path

from guide_generator.pdf.preprocess import obsidian_to_pandoc, slug_to_title

_CONTENTS_START = re.compile(r"^## Contents\s*$", re.MULTILINE)
_WIKI_IN_INDEX = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")


def _ordered_slugs(index_text: str) -> list[str]:
    m = _CONTENTS_START.search(index_text)
    if not m:
        return []
    tail = index_text[m.end() :]
    # Stop before suggested routes / further reading (wikilinks there are not site order)
    stop = re.search(r"^## (?:Suggested|routes|Further reading)", tail, re.MULTILINE | re.I)
    if stop:
        tail = tail[: stop.start()]
    slugs: list[str] = []
    seen: set[str] = set()
    for hit in _WIKI_IN_INDEX.finditer(tail):
        slug = hit.group(1).strip()
        if slug not in seen:
            seen.add(slug)
            slugs.append(slug)
    return slugs


def _fallback_order(topic_dir: Path) -> list[str]:
    skip = {"index"}
    files = sorted(p.stem for p in topic_dir.glob("*.md") if p.stem not in skip)
    return files


def merge_topic_markdown(topic_dir: Path) -> tuple[str, list[str]]:
    """Return combined markdown and list of slugs included."""
    index_path = topic_dir / "index.md"
    if not index_path.is_file():
        raise FileNotFoundError(f"Missing index.md in {topic_dir}")

    index_raw = index_path.read_text(encoding="utf-8")
    slugs = _ordered_slugs(index_raw)
    if not slugs:
        slugs = _fallback_order(topic_dir)

    parts: list[str] = []

    # Title block (Pandoc % syntax: % title / % author / % date)
    title = "Travel guide"
    fm = re.search(r"^title:\s*(.+)$", index_raw, re.MULTILINE)
    if fm:
        title = fm.group(1).strip()

    audience_raw = ""
    am = re.search(r"^audience:\s*(.+)$", index_raw, re.MULTILINE)
    if am:
        audience_raw = am.group(1).strip()
    # Convert "landscape_photographer" → "Landscape Photographer"
    audience_label = audience_raw.replace("_", " ").title() if audience_raw else "Field Guide"

    from datetime import date as _date
    _d = _date.today()
    today = f"{_d.day} {_d.strftime('%B')} {_d.year}"

    parts.append(f"% {title}\n% Audience: {audience_label}\n% {today}\n\n")
    parts.append(obsidian_to_pandoc(index_raw, topic_dir))
    parts.append('<div class="newpage"></div>\n\n')

    for slug in slugs:
        note = topic_dir / f"{slug}.md"
        if not note.is_file():
            continue
        body = obsidian_to_pandoc(note.read_text(encoding="utf-8"), topic_dir)
        # Ensure page-break before each site; anchor for TOC
        heading = slug_to_title(slug)
        if body.startswith("# "):
            body = re.sub(
                r"^# (.+)$",
                rf"# \1 {{#{slug}}}",
                body,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            body = f"# {heading} {{#{slug}}}\n\n{body}"
        parts.append(f'<div class="newpage"></div>\n\n{body}\n\n')

    # Attribution appendix
    att = topic_dir / "attachments" / "images" / "ATTRIBUTION.md"
    if att.is_file():
        parts.append('<div class="newpage"></div>\n\n')
        parts.append(obsidian_to_pandoc(att.read_text(encoding="utf-8"), topic_dir))

    return "".join(parts), slugs
