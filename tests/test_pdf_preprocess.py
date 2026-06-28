from pathlib import Path

from guide_generator.pdf.merge import _ordered_slugs
from guide_generator.pdf.preprocess import obsidian_to_pandoc, strip_frontmatter


def test_strip_frontmatter():
    text = "---\ntitle: Foo\n---\n\n# Body\n"
    assert strip_frontmatter(text).startswith("# Body")


def test_obsidian_embed_and_link(tmp_path: Path):
    img = tmp_path / "attachments" / "images" / "x" / "a.jpg"
    img.parent.mkdir(parents=True)
    img.write_bytes(b"jpeg")
    md = "See [[other-site]] and ![[attachments/images/x/a.jpg|400]]"
    out = obsidian_to_pandoc(md, tmp_path)
    assert "**other-site**" in out
    assert "attachments/images/x/a.jpg" in out


def test_ordered_slugs_from_index():
    index = """# Index\n\n## Contents\n\n| x |\n| [[alpha]] |\n| [[beta]] |\n"""
    assert _ordered_slugs(index) == ["alpha", "beta"]
