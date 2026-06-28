"""Transform Obsidian Markdown into Pandoc-friendly Markdown."""
from __future__ import annotations

import re
from pathlib import Path

_FRONTMATTER = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
_WIKI_EMBED = re.compile(
    r"!\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]",
)
_WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]")
# Broken compile artifact: **[Name** (license)](url)**
_BROKEN_PHOTO_LINK = re.compile(
    r"\*\*\[([^\]]*?)\*\*([^]]*?)\]\(([^)]+)\)\*\*"
)


def strip_frontmatter(text: str) -> str:
    return _FRONTMATTER.sub("", text, count=1)


def obsidian_to_pandoc(text: str, topic_dir: Path) -> str:
    """Convert wikilinks and embeds; verify image paths exist."""
    text = strip_frontmatter(text)

    def embed_repl(m: re.Match[str]) -> str:
        path = m.group(1).strip()
        alt = Path(path).stem.replace("-", " ")
        full = topic_dir / path
        if full.is_file():
            # Relative path for Pandoc resource path
            return f"![{alt}]({path.replace(chr(92), '/')})"
        return f"*[Image missing: {path}]*"

    def link_repl(m: re.Match[str]) -> str:
        slug = m.group(1).strip()
        label = (m.group(2) or slug.replace("-", " ")).strip()
        return f"**{label}**"

    text = _WIKI_EMBED.sub(embed_repl, text)
    text = _WIKI_LINK.sub(link_repl, text)

    def fix_photo(m: re.Match[str]) -> str:
        name = m.group(1).strip()
        suffix = m.group(2).strip()
        url = m.group(3)
        return f"[{name}{suffix}]({url})"

    text = _BROKEN_PHOTO_LINK.sub(fix_photo, text)
    return text.strip() + "\n"


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").title()
