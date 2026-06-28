from __future__ import annotations

import re

_SECTION_RE = re.compile(r"^## (.+)$", re.MULTILINE)
_SUBSECTION_RE = re.compile(r"^### (.+)$", re.MULTILINE)


def parse_sections(body: str) -> dict[str, str]:
    """Parse top-level ## sections from audience markdown body."""
    sections: dict[str, str] = {}
    matches = list(_SECTION_RE.finditer(body))
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[title] = body[start:end].strip()
    return sections


def parse_override_subsections(overrides_body: str) -> dict[str, str]:
    """Parse ### subsections inside ## Overrides."""
    subsections: dict[str, str] = {}
    matches = list(_SUBSECTION_RE.finditer(overrides_body))
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(overrides_body)
        subsections[title] = overrides_body[start:end].strip()
    return subsections
