from __future__ import annotations

from dataclasses import dataclass, field

from guide_generator.audiences.sections import parse_sections


@dataclass(frozen=True)
class AudienceDefinition:
    """Parsed audience definition from audiences/<id>.md."""

    id: str
    parent: str | None
    copy_from: tuple[str, ...] = field(default_factory=tuple)
    body: str = ""
    path: str = ""

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def sections(self) -> dict[str, str]:
        return parse_sections(self.body)
