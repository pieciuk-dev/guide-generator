# PDF compilation

PDF export is **on demand** after Markdown content is stable in a topic folder.

## Planned approach

1. **Source:** all traveler-facing `.md` under `topics/<topic_id>/`, excluding `_ai/`.
2. **Order:** `index.md` first, then files listed in its “Contents” section (or lexical order as fallback).
3. **Tool:** [Pandoc](https://pandoc.org/) with a project CSS template (typography, headings, page breaks).
4. **Images:** resolve `![[attachments/...]]` wikilinks to file paths before Pandoc.
5. **Output:** `topics/<topic_id>/_ai/<topic_id>.pdf` or `topics/<topic_id>/guide.pdf` (TBD when implemented).

## Command (not yet implemented)

```bash
python -m guide_generator.pdf topics/<topic_id>/
```

## Requirements (to install later)

- `pandoc` on PATH
- Optional: `weasyprint` or `wkhtmltopdf` if we need HTML intermediate

## Style goals

- Readable body text, clear heading hierarchy
- Embedded images scaled to page width
- Table of contents from `index.md`
- Print-friendly margins

Implementation will be added when the first topic has real content to validate layout.
