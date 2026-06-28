# Obsidian Markdown conventions

Guide content is written for **Obsidian** (and compatible editors).

## File layout

- `index.md` — entry point / map of content for the topic.
- Additional notes at topic root or in subfolders (e.g. `locations/`, `practical/`).
- Keep filenames **slug-safe**: lowercase, hyphens or underscores, no spaces.

## Frontmatter (each note)

```yaml
---
title: Dune viewpoints
topic: example_trip
tags:
  - guide
  - locations
---
```

## Linking

- **Internal links:** `[[note-name]]` or `[[folder/note-name|Display text]]`
- **Attachments:** store under `attachments/images/` or `attachments/audio/`
- **Embed image:** `![[attachments/images/example.jpg]]`
- **Embed with size (optional):** `![[attachments/images/example.jpg|400]]`

Use relative wikilinks; avoid hard-coded absolute paths.

## Headings

- One H1 (`#`) per note (usually matches `title`).
- Use H2–H4 for structure; keep deep nesting shallow for PDF export.

## Source references in traveler content

Prefer inline attribution where useful:

```markdown
Coordinates: 54.76°N, 17.45°E ([source name](https://…), accessed 2026-06-28).
```

Full research paper trail lives in `_ai/worklog.md`, not duplicated in every note.

## Folders to exclude from traveler bundles

- `_ai/` — agent metadata only
- Do not link traveler notes *into* `_ai/` from main content

## Splitting content

Split when a note exceeds ~500–800 lines or covers distinct subtopics (e.g. one note per major location cluster).
