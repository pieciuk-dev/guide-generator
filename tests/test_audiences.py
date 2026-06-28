from __future__ import annotations

from guide_generator.audiences.loader import load_all_audiences
from guide_generator.audiences.sections import parse_sections
from guide_generator.audiences.validate import validate_audiences


def test_load_all_audiences():
    audiences = load_all_audiences()
    assert set(audiences) == {
        "photographer",
        "landscape_photographer",
        "history_culture_lover",
    }
    assert audiences["landscape_photographer"].parent == "photographer"
    assert audiences["history_culture_lover"].parent == "photographer"


def test_validate_current_audiences():
    result = validate_audiences(load_all_audiences())
    assert result.ok, [str(e) for e in result.errors]


def test_parse_sections():
    body = "## About\n\nhello\n\n## Additions\n\n- one\n"
    sections = parse_sections(body)
    assert sections["About"] == "hello"
    assert sections["Additions"] == "- one"


def test_child_with_content_section_fails_validation():
    from guide_generator.audiences.models import AudienceDefinition

    audiences = load_all_audiences()
    bad = AudienceDefinition(
        id="bad_child",
        parent="photographer",
        copy_from=(),
        body="## Content requirements\n\n- nope\n",
        path="bad_child.md",
    )
    audiences["bad_child"] = bad
    result = validate_audiences(audiences)
    assert not result.ok
    assert any("Content requirements" in str(e) for e in result.errors)
