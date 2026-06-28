from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from guide_generator.audiences.loader import load_all_audiences
from guide_generator.audiences.models import AudienceDefinition
from guide_generator.audiences.sections import parse_override_subsections, parse_sections


@dataclass
class ResolvedAudience:
    audience_id: str
    parent_chain: tuple[str, ...]
    copy_from: tuple[str, ...]
    sections: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        resolved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        lines = [
            "---",
            f"audience_id: {self.audience_id}",
            f"parent_chain: [{', '.join(self.parent_chain)}]",
            f"copy_from: [{', '.join(self.copy_from)}]",
            f"resolved_at: {resolved_at}",
            "---",
            "",
            f"# Resolved audience: {self.audience_id}",
            "",
            "Flat profile for guide generation. Do not edit by hand — regenerate with "
            "`python -m guide_generator.audiences.resolve <audience_id>`.",
            "",
        ]
        if self.warnings:
            lines.extend(["## Resolution warnings", ""])
            lines.extend(f"- {w}" for w in self.warnings)
            lines.append("")

        order = [
            "Technical requirements",
            "Content requirements",
            "Additions",
            "Copy-from base",
        ]
        emitted: set[str] = set()
        for key in order:
            if key in self.sections and self.sections[key].strip():
                lines.extend([f"## {key}", "", self.sections[key].strip(), ""])
                emitted.add(key)
        for key, body in self.sections.items():
            if key not in emitted and body.strip():
                lines.extend([f"## {key}", "", body.strip(), ""])
        return "\n".join(lines).rstrip() + "\n"


def _concat_section(parts: list[str]) -> str:
    bullets = [p.strip() for p in parts if p.strip()]
    return "\n\n".join(bullets)


def _resolve_one(
    audience_id: str,
    audiences: dict[str, AudienceDefinition],
    stack: set[str] | None = None,
) -> ResolvedAudience:
    if audience_id not in audiences:
        raise KeyError(f"unknown audience: {audience_id}")

    if stack is None:
        stack = set()
    if audience_id in stack:
        raise ValueError(f"copy_from cycle at {audience_id}")
    stack = set(stack)
    stack.add(audience_id)

    audience = audiences[audience_id]
    warnings: list[str] = []

    chain_ids: list[str] = []
    current: str | None = audience_id
    seen: set[str] = set()
    while current:
        if current in seen:
            raise ValueError(f"parent cycle at {current}")
        seen.add(current)
        chain_ids.append(current)
        current = audiences[current].parent
    chain_ids.reverse()
    root_to_target = chain_ids

    technical_parts: list[str] = []
    content_parts: list[str] = []
    additions_parts: list[str] = []

    for aid in root_to_target:
        sections = parse_sections(audiences[aid].body)
        if audiences[aid].is_root:
            if "Technical requirements" in sections:
                technical_parts.append(sections["Technical requirements"])
            if "Content requirements" in sections:
                content_parts.append(sections["Content requirements"])
        else:
            if "Additions" in sections:
                additions_parts.append(sections["Additions"])

    copy_from_base_parts: list[str] = []
    for ref in audience.copy_from:
        ref_resolved = _resolve_one(ref, audiences, stack)
        for key in ("Content requirements", "Additions", "Copy-from base"):
            if key in ref_resolved.sections and ref_resolved.sections[key].strip():
                copy_from_base_parts.append(
                    f"### From `{ref}` — {key}\n\n{ref_resolved.sections[key].strip()}"
                )
        warnings.extend(ref_resolved.warnings)

    overrides = parse_sections(audiences[audience_id].body).get("Overrides", "")
    override_subs = parse_override_subsections(overrides) if overrides else {}

    copy_from_merged = _concat_section(copy_from_base_parts)
    if override_subs:
        for sub_name, sub_body in override_subs.items():
            if sub_body.strip():
                copy_from_merged += f"\n\n### Override — {sub_name}\n\n{sub_body.strip()}"
                warnings.append(f"Applied override for copy-from subsection: {sub_name}")

    sections_out: dict[str, str] = {}
    if technical_parts:
        sections_out["Technical requirements"] = _concat_section(technical_parts)
    if content_parts:
        sections_out["Content requirements"] = _concat_section(content_parts)
    if additions_parts:
        sections_out["Additions"] = _concat_section(additions_parts)
    if copy_from_merged.strip():
        sections_out["Copy-from base"] = copy_from_merged.strip()

    return ResolvedAudience(
        audience_id=audience_id,
        parent_chain=tuple(root_to_target),
        copy_from=audience.copy_from,
        sections=sections_out,
        warnings=warnings,
    )


def resolve_audience(
    audience_id: str,
    audiences_dir=None,
) -> ResolvedAudience:
    audiences = load_all_audiences(audiences_dir)
    return _resolve_one(audience_id, audiences)


def write_resolved_profile(
    audience_id: str,
    output_path,
    audiences_dir=None,
) -> ResolvedAudience:
    from pathlib import Path

    resolved = resolve_audience(audience_id, audiences_dir)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(resolved.to_markdown(), encoding="utf-8")
    return resolved


def main() -> None:
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("Usage: python -m guide_generator.audiences.resolve <audience_id> [output.md]")
        raise SystemExit(2)

    audience_id = sys.argv[1]
    if len(sys.argv) >= 3:
        out = Path(sys.argv[2])
    else:
        out = Path("data/cache/audiences") / f"{audience_id}.md"

    resolved = write_resolved_profile(audience_id, out)
    print(f"Wrote {out} (chain: {' → '.join(resolved.parent_chain)})")


if __name__ == "__main__":
    main()
