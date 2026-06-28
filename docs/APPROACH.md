# Audience-based approach

## Core idea

Every guide targets **one audience**. The audience defines what the guide must cover, how detailed it is, and technical constraints for generation.

Audiences form a **graph**:

1. **Parent chain** (tree) — exactly one root; each audience has at most one parent. Requirements flow down the chain. **Children cannot override the parent.**
2. **Copy-from** (optional edges) — references to other audiences whose resolved sections form a **base** for this audience. **Copy-from content may be overridden** in `## Overrides`. Parent chain always wins on conflict.

A guide uses **one audience id**. The system resolves that id into a single **audience profile** (snapshot) before generating content.

## Inheritance rules

| Source | Role | Override allowed? |
|--------|------|-------------------|
| Root (`photographer`) | `## Technical requirements` + `## Content requirements` | No (locked for all descendants) |
| Ancestors (parent, grandparent, …) | `## Content requirements` and `## Additions` from each ancestor | No |
| Copy-from audiences | Resolved sections (see below) | Yes — via `## Overrides` |
| This audience | `## Additions` (+ `## Overrides` when `copy_from` set) | — |

### Section rules by role

| Section | Root | Child (has parent) |
|---------|------|---------------------|
| `## About` | Yes | Yes |
| `## Technical requirements` | Yes — **required** | **Forbidden** (inherited from root only) |
| `## Content requirements` | Yes — **required** | **Forbidden** (use `## Additions` instead) |
| `## Additions` | No | Yes — **only place for child-specific requirements** |
| `## Overrides` | No | Only when `copy_from` is non-empty |

**Merge unit:** each section is a list of Markdown bullets. Merging **concatenates** bullets in order (no deduplication yet).

### Copy-from semantics

- **Resolved profile:** each `copy_from` id is fully resolved (its parent chain + its own `copy_from` + its `## Additions`) before merging.
- **Any audience** may be referenced, including siblings (not limited to the parent chain).
- **Technical requirements** come **only** from the target’s own parent chain to root — never from copy-from.
- **Merge order:** for each id in `copy_from` (in list order), append that audience’s resolved `## Content requirements` and `## Additions` into a copy-from base.
- **Conflict:** if copy-from content conflicts with the parent chain, **parent chain wins** (copy-from bullets are dropped or ignored for that topic — resolver logs a warning).
- **Copy-from vs copy-from:** later ids in `copy_from` append after earlier ones; `## Overrides` applies last.

### Overrides syntax

When `copy_from` is set, `## Overrides` may contain subsections named after merged section types:

```markdown
## Overrides

### Content requirements
- Replace or narrow a copy-from rule stated here as a full bullet.

### Additions
- Replace or narrow copy-from additions here.
```

Overrides affect **copy-from base only**, not the parent chain.

**Resolution order:**

```
1. Walk parent chain root → target; concatenate Technical (root only) + Content + Additions per ancestor
2. For each copy_from id (in order): merge its resolved Content + Additions into copy-from base
3. Append this audience's ## Additions
4. Apply ## Overrides subsections to copy-from base
5. Emit resolved profile snapshot
```

Resolved profiles are cached under `data/cache/audiences/<audience_id>.md` via `python -m guide_generator.audiences resolve <audience_id>`.

## Audience files

- Location: `audiences/<id>.md` — **`id` in frontmatter must match the filename stem**
- Format: YAML frontmatter + Markdown sections
- Templates: `audiences/_template.root.md`, `audiences/_template.child.md`

### Frontmatter

```yaml
---
id: landscape_photographer
parent: photographer
copy_from: []
---
```

Run validation after edits: `python -m guide_generator.audiences`

## Topics (guide output)

Each guide is a **topic folder**: `topics/<topic_id>/` where `topic_id` matches trip `id`.

Initialize:

```bash
python -m guide_generator.topics init data/trips/<trip_id>.yaml
```

See [GUIDE_WORKFLOW.md](GUIDE_WORKFLOW.md), [OBSIDIAN.md](OBSIDIAN.md), [PDF.md](PDF.md).

## Trip input (geographic + audience)

Trip files: `data/trips/<trip_id>.yaml`

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Topic id (filename stem) |
| `region.name` | Yes | Geographic scope (island, region, park, …) |
| `region.type` | No | e.g. `island`, `region`, `national_park`, `city` |
| `region.country` | No | Country or region context |
| `audience` | Yes | Audience id |
| `dates.start` / `dates.end` | No | ISO dates |
| `notes` | No | Extra instructions for the agent |

Example regions: Öland island, Madeira, Pomerania, Słowiński National Park.

## Worklogs

| Activity | File |
|----------|------|
| System work | `_ai/buildlog.md` |
| Guide / topic work | `topics/<topic_id>/_ai/worklog.md` |
