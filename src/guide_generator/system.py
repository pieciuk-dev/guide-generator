"""Installation-wide settings (supporting language, etc.)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_SYSTEM_PATH = _REPO_ROOT / "data" / "system.yaml"
_EXAMPLE_SYSTEM_PATH = _REPO_ROOT / "data" / "system.example.yaml"


@dataclass(frozen=True)
class SupportingLanguage:
    name: str
    code: str | None = None


@dataclass(frozen=True)
class SystemConfig:
    supporting_language: SupportingLanguage | None = None
    path: Path | None = None

    @property
    def is_configured(self) -> bool:
        return self.supporting_language is not None


def _parse_supporting_language(raw: object) -> SupportingLanguage | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        name = raw.strip()
        return SupportingLanguage(name=name) if name else None
    if isinstance(raw, dict):
        name = str(raw.get("name", "")).strip()
        if not name:
            return None
        code = raw.get("code")
        code_str = str(code).strip() if code else None
        return SupportingLanguage(name=name, code=code_str or None)
    return None


def load_system_config(path: Path | None = None) -> SystemConfig:
    """Load data/system.yaml. Returns empty config if the file is missing."""
    cfg_path = path or _DEFAULT_SYSTEM_PATH
    if not cfg_path.is_file():
        return SystemConfig(path=None)

    data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    lang = _parse_supporting_language(data.get("supporting_language"))
    return SystemConfig(supporting_language=lang, path=cfg_path.resolve())


def system_context_markdown(config: SystemConfig | None = None) -> str:
    """Markdown section injected into topic audience profiles."""
    config = config if config is not None else load_system_config()
    lines = ["## System context", ""]

    if config.supporting_language:
        lang = config.supporting_language
        code_part = f" (`{lang.code}`)" if lang.code else ""
        lines.extend(
            [
                f"- **Supporting language:** {lang.name}{code_part} — from `data/system.yaml`.",
                "- **When to use:** only where the audience profile explicitly requires "
                "**supporting language** labels (e.g. bird names in the reader's language). "
                "Keep primary regional or scientific names from sources; add the supporting "
                "language in parentheses or a second column when the audience asks for it.",
                "- **When not to use:** do not translate the whole guide unless the audience "
                "requires it; most prose stays in the language of the sources and region.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "- **Supporting language:** not configured.",
                "- Copy `data/system.example.yaml` to `data/system.yaml` and set "
                "`supporting_language` if any audience references it.",
                "",
            ]
        )
    return "\n".join(lines)


def validate_system_config(config: SystemConfig | None = None) -> list[str]:
    """Return warning messages (empty if OK)."""
    config = config if config is not None else load_system_config()
    warnings: list[str] = []
    if config.path is None:
        warnings.append(
            "data/system.yaml missing — copy data/system.example.yaml to data/system.yaml "
            "to set supporting language for this installation"
        )
    elif config.supporting_language is None:
        warnings.append(
            "data/system.yaml has no supporting_language — audiences that reference it "
            "cannot apply local labels until you set one"
        )
    return warnings


def main() -> None:
    import sys

    config = load_system_config()
    warnings = validate_system_config(config)

    if config.supporting_language:
        lang = config.supporting_language
        code = f" ({lang.code})" if lang.code else ""
        print(f"Supporting language: {lang.name}{code}")
    else:
        print("Supporting language: (not set)")

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    if warnings and "--strict" in sys.argv:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
