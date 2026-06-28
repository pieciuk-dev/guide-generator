from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from guide_generator.audiences.models import AudienceDefinition
from guide_generator.audiences.sections import parse_sections

ROOT_FORBIDDEN_ON_CHILD = frozenset({"Technical requirements", "Content requirements"})
ROOT_REQUIRED_SECTIONS = frozenset({"Technical requirements", "Content requirements"})


@dataclass
class ValidationError:
    audience_id: str
    message: str

    def __str__(self) -> str:
        return f"{self.audience_id}: {self.message}"


@dataclass
class ValidationResult:
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _parent_chain(audience_id: str, audiences: dict[str, AudienceDefinition]) -> list[str]:
    chain: list[str] = []
    current = audience_id
    seen: set[str] = set()
    while current:
        if current in seen:
            raise ValueError(f"parent cycle at {current}")
        seen.add(current)
        chain.append(current)
        parent = audiences[current].parent
        if parent is None:
            break
        if parent not in audiences:
            raise ValueError(f"unknown parent {parent!r}")
        current = parent
    return list(reversed(chain))


def _copy_from_cycle(audience_id: str, audiences: dict[str, AudienceDefinition]) -> bool:
    visiting: set[str] = set()
    stack: set[str] = set()

    def visit(node: str) -> bool:
        if node in stack:
            return True
        if node in visiting:
            return False
        visiting.add(node)
        stack.add(node)
        for ref in audiences[node].copy_from:
            if ref not in audiences:
                continue
            if visit(ref):
                return True
        stack.remove(node)
        return False

    return visit(audience_id)


def validate_audiences(audiences: dict[str, AudienceDefinition]) -> ValidationResult:
    result = ValidationResult()
    roots = [a for a in audiences.values() if a.parent is None]

    if len(roots) == 0:
        result.errors.append(ValidationError("(graph)", "no root audience (parent: null)"))

    for audience in audiences.values():
        sections = parse_sections(audience.body)
        stem = Path(audience.path).stem

        if audience.id != stem:
            result.errors.append(
                ValidationError(audience.id, f"frontmatter id must match filename stem {stem!r}")
            )

        if audience.parent is not None and audience.parent not in audiences:
            result.errors.append(
                ValidationError(audience.id, f"unknown parent {audience.parent!r}")
            )

        for ref in audience.copy_from:
            if ref not in audiences:
                result.errors.append(ValidationError(audience.id, f"unknown copy_from {ref!r}"))
            elif ref == audience.id:
                result.errors.append(ValidationError(audience.id, "copy_from cannot reference self"))

        if audience.is_root:
            for required in ROOT_REQUIRED_SECTIONS:
                if required not in sections or not sections[required].strip():
                    result.errors.append(
                        ValidationError(audience.id, f"root must define non-empty ## {required}")
                    )
            if "Additions" in sections and sections["Additions"].strip():
                result.warnings.append(
                    ValidationError(audience.id, "## Additions on root is unusual; prefer ## Content requirements")
                )
        else:
            for forbidden in ROOT_FORBIDDEN_ON_CHILD:
                if forbidden in sections and sections[forbidden].strip():
                    result.errors.append(
                        ValidationError(
                            audience.id,
                            f"child must not define ## {forbidden} (use ## Additions)",
                        )
                    )
            if not sections.get("Additions", "").strip():
                result.warnings.append(
                    ValidationError(audience.id, "## Additions is empty")
                )

        if audience.copy_from and "Overrides" not in sections:
            result.warnings.append(
                ValidationError(audience.id, "copy_from set but ## Overrides is missing")
            )
        if not audience.copy_from and "Overrides" in sections and sections["Overrides"].strip():
            result.warnings.append(
                ValidationError(audience.id, "## Overrides has content but copy_from is empty")
            )

        try:
            _parent_chain(audience.id, audiences)
        except ValueError as exc:
            result.errors.append(ValidationError(audience.id, str(exc)))

        if _copy_from_cycle(audience.id, audiences):
            result.errors.append(ValidationError(audience.id, "copy_from cycle detected"))

    return result


def main() -> None:
    from guide_generator.audiences.loader import load_all_audiences

    audiences = load_all_audiences()
    result = validate_audiences(audiences)

    for warning in result.warnings:
        print(f"WARNING {warning}")
    for error in result.errors:
        print(f"ERROR {error}")

    if not result.ok:
        raise SystemExit(1)

    from guide_generator.system import validate_system_config

    for warning in validate_system_config():
        print(f"WARNING (system): {warning}")

    print(f"OK — {len(audiences)} audience(s) validated")


if __name__ == "__main__":
    main()
