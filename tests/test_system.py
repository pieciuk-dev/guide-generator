from __future__ import annotations

from pathlib import Path

from guide_generator.system import (
    SupportingLanguage,
    load_system_config,
    system_context_markdown,
    validate_system_config,
)


def test_load_supporting_language(tmp_path):
    cfg = tmp_path / "system.yaml"
    cfg.write_text(
        "supporting_language:\n  name: Polish\n  code: pl\n",
        encoding="utf-8",
    )
    config = load_system_config(cfg)
    assert config.supporting_language == SupportingLanguage(name="Polish", code="pl")


def test_system_context_includes_language(tmp_path):
    cfg = tmp_path / "system.yaml"
    cfg.write_text("supporting_language:\n  name: Swedish\n  code: sv\n", encoding="utf-8")
    md = system_context_markdown(load_system_config(cfg))
    assert "Supporting language:** Swedish (`sv`)" in md
    assert "bird names" in md or "supporting language" in md.lower()


def test_system_context_when_missing():
    md = system_context_markdown(load_system_config(Path("/nonexistent/system.yaml")))
    assert "not configured" in md


def test_validate_warns_when_missing():
    warnings = validate_system_config(load_system_config(Path("/nonexistent/system.yaml")))
    assert any("missing" in w for w in warnings)
