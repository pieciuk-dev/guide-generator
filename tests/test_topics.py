from __future__ import annotations

from pathlib import Path

import pytest

from guide_generator.audiences.resolve import resolve_audience
from guide_generator.topics.scaffold import init_topic, load_trip, refresh_topic_profile


def test_resolve_landscape_photographer():
    resolved = resolve_audience("landscape_photographer")
    assert resolved.audience_id == "landscape_photographer"
    assert resolved.parent_chain == ("photographer", "landscape_photographer")
    assert "Technical requirements" in resolved.sections
    assert "Output format" in resolved.sections["Technical requirements"] or "Obsidian" in resolved.sections["Technical requirements"]


def test_load_trip_example():
    trip = load_trip(Path("data/trips/_example.yaml"))
    assert trip.id == "example_trip"
    assert trip.region["name"] == "Example Region"
    assert trip.audience == "landscape_photographer"


def test_init_topic(tmp_path, monkeypatch):
    sys_yaml = tmp_path / "system.yaml"
    sys_yaml.write_text(
        "supporting_language:\n  name: TestLang\n  code: tl\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "guide_generator.system._DEFAULT_SYSTEM_PATH",
        sys_yaml,
    )
    trip_file = tmp_path / "test_trip.yaml"
    trip_file.write_text(
        "id: test_topic\nregion:\n  name: Test Island\n  type: island\naudience: photographer\n",
        encoding="utf-8",
    )
    topic_dir = init_topic(trip_file, topics_dir=tmp_path / "topics")
    assert (topic_dir / "index.md").is_file()
    assert (topic_dir / "_ai" / "audience_profile.md").is_file()
    assert (topic_dir / "_ai" / "worklog.md").is_file()
    assert (topic_dir / "_ai" / "site_list.md").is_file()
    assert (topic_dir / "_ai" / "research").is_dir()
    assert (topic_dir / "attachments" / "images").is_dir()
    profile = (topic_dir / "_ai" / "audience_profile.md").read_text(encoding="utf-8")
    assert "Technical requirements" in profile
    assert "System context" in profile
    assert "TestLang" in profile


def test_refresh_topic_profile(tmp_path):
    trip_file = tmp_path / "test_trip.yaml"
    trip_file.write_text(
        "id: test_topic\nregion:\n  name: Test Island\n  type: island\naudience: photographer\n",
        encoding="utf-8",
    )
    topics = tmp_path / "topics"
    init_topic(trip_file, topics_dir=topics)
    profile = topics / "test_topic" / "_ai" / "audience_profile.md"
    before = profile.read_text(encoding="utf-8")
    refresh_topic_profile("test_topic", topics_dir=topics)
    after = profile.read_text(encoding="utf-8")
    assert "Technical requirements" in after
    assert before  # profile existed before refresh
