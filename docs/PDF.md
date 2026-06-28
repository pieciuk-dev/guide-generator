# PDF compilation

PDF export is **on demand** after Phase 3 Markdown content is stable in a topic folder.

## Command

```bash
pip install -e ".[pdf]"
python -m guide_generator.pdf <topic_id>
```

Example:

```bash
python -m guide_generator.pdf olands_island_landscape
```

Outputs:

- `topics/<topic_id>/guide.pdf` — print-ready reference
- `topics/<topic_id>/guide.html` — same content with inlined CSS (browser preview)

Optional output path:

```bash
python -m guide_generator.pdf topics/olands_island_landscape/ -o path/to/guide.pdf
```

## Pipeline

1. **Source:** traveler-facing `.md` under `topics/<topic_id>/`, excluding `_ai/`.
2. **Order:** `index.md` first, then sites in index **Contents** wikilink order.
3. **Preprocess:** Obsidian `[[wikilinks]]` → bold labels; `![[attachments/…]]` → standard images.
4. **HTML:** [Pandoc](https://pandoc.org/) with project CSS (`guide_generator/pdf/assets/guide.css`) and table of contents.
5. **PDF:** [xhtml2pdf](https://pypi.org/project/xhtml2pdf/) (pure Python; no LaTeX required).

## Requirements

- **pandoc** on PATH
- Python extras: `pip install -e ".[pdf]"` (`xhtml2pdf`, `markdown`)

## Style

- A4, readable sans-serif body
- Teal heading hierarchy, styled tables (site index)
- Page break before each site note
- Images scaled to page width with attribution captions
- Image attribution appendix from `attachments/images/ATTRIBUTION.md`
