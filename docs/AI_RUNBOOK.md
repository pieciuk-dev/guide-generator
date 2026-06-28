# AI runbook

**Start here** in every new agent session. This is the operational manual for the full AI-driven guide workflow.

Related docs: [GUIDE_BUILD_PROCESS.md](GUIDE_BUILD_PROCESS.md) (**three-phase build**), [GUIDE_WORKFLOW.md](GUIDE_WORKFLOW.md), [APPROACH.md](APPROACH.md), [OBSIDIAN.md](OBSIDIAN.md), [PDF.md](PDF.md).

---

## Environment

From repository root (`guide-generator/`):

```bash
pip install -e .
python --version   # requires >= 3.10
```

All `python -m guide_generator.*` commands below assume **repo root** as the current working directory.

**Git:** guide output is local-only — `topics/<id>/`, `data/trips/<your>.yaml`, and `data/cache/` are in `.gitignore`. Project setup (`audiences/`, `docs/`, `src/`, `_ai/buildlog.md`) stays tracked.

---

## Python CLI reference

| Command | When to run |
|---------|-------------|
| `python -m guide_generator.audiences` | After editing any file in `audiences/` |
| `python -m guide_generator.audiences resolve <audience_id>` | Cache profile to `data/cache/audiences/<id>.md` (optional) |
| `python -m guide_generator.audiences resolve <audience_id> <path>` | Write resolved profile to a specific path |
| `python -m guide_generator.topics init data/trips/<trip_id>.yaml` | **New guide** — creates `topics/<trip_id>/` |
| `python -m guide_generator.topics refresh-profile <topic_id>` | After audience edits — updates `topics/<id>/_ai/audience_profile.md` |

### Not implemented yet

| Command | Status |
|---------|--------|
| `python -m guide_generator.pdf <topic_id>` | [PDF.md](PDF.md) — Pandoc + Chrome/Edge headless |
| `python -m guide_generator.maps <topic_id>` | [MAPS.md](MAPS.md) — Google My Maps CSV |

---

## Map user requests → actions

### “Build a guide for &lt;region&gt;” / “Create guide: Madeira, landscape photographer”

1. Check if `topics/<topic_id>/` already exists.
   - **Exists** → continue guide (see below); do **not** run `init` again.
   - **Missing** → continue with step 2.
2. Create or edit `data/trips/<topic_id>.yaml` (see schema below).  
   - `topic_id` = snake_case slug, e.g. `madeira_landscape`, `olands_island_landscape`.
3. Run: `python -m guide_generator.topics init data/trips/<topic_id>.yaml`
4. Run **[Guide build process](GUIDE_BUILD_PROCESS.md)** — Phase 1 → 2 → 3 (see below).

### “Continue the &lt;region&gt; guide” / “Work on &lt;topic_id&gt;”

1. Open `topics/<topic_id>/_ai/` — read `worklog.md`, **`site_list.md`**, `audience_profile.md`, `input.yaml`.
2. Identify **current phase** from worklog and site list status.
3. Continue the appropriate phase; do **not** run `init`.

### “I updated the audience definitions”

1. `python -m guide_generator.audiences` — must exit OK.
2. For each active topic: `python -m guide_generator.topics refresh-profile <topic_id>`
3. Re-read updated `_ai/audience_profile.md` before further content work.

### “Compile PDF” / “Export guide as PDF”

1. Confirm topic Markdown is complete.
2. See [PDF.md](PDF.md): `python -m guide_generator.pdf <topic_id>`

### “Export map” / “Google My Maps CSV”

1. Confirm Phase 3 site notes include coordinates.
2. See [MAPS.md](MAPS.md): `python -m guide_generator.maps <topic_id>`

### “Change the system / project setup”

1. Edit code or docs in `src/`, `docs/`, etc.
2. Append summary to `_ai/buildlog.md` (repo root).
3. Run tests: `python -m pytest -q`

---

## Trip YAML schema

File: `data/trips/<topic_id>.yaml` — **`id` must match filename stem**.

```yaml
id: madeira_landscape
region:
  name: Madeira
  type: island          # island | region | national_park | city | area
  country: Portugal
audience: landscape_photographer   # must exist in audiences/
dates:
  start: null           # optional ISO date
  end: null
notes: []               # optional extra instructions from the user
```

---

## Guide build process (three phases)

Full detail: **[GUIDE_BUILD_PROCESS.md](GUIDE_BUILD_PROCESS.md)**.

| Phase | What | Key files |
|-------|------|-----------|
| **1 — Discovery** | General research; define sites/subjects | `_ai/site_list.md`, worklog Phase 1 |
| **2 — Deep dive** | Research each site in depth | `_ai/research/<slug>.md`, worklog Phase 2 |
| **3 — Compile** | Final Obsidian guide | `index.md`, `*.md` in topic root |

**Websites for search** in the audience profile are **Phase 1 starting points**; Phase 2 may use any additional sources.

### Per-session loop

```
┌─────────────────────────────────────────────────────────┐
│ 1. READ  input.yaml, audience_profile.md, worklog.md,   │
│          site_list.md                                   │
├─────────────────────────────────────────────────────────┤
│ 2. PHASE Identify and execute current build phase       │
├─────────────────────────────────────────────────────────┤
│ 3. WRITE Phase 1 → site_list.md                         │
│          Phase 2 → _ai/research/<slug>.md              │
│          Phase 3 → traveler .md + index.md Contents     │
├─────────────────────────────────────────────────────────┤
│ 4. LOG   sources in worklog (with phase column)         │
├─────────────────────────────────────────────────────────┤
│ 5. MEDIA / SCRIPTS per audience + permission rules      │
└─────────────────────────────────────────────────────────┘
```

### Files the agent reads (in order)

1. `topics/<topic_id>/_ai/input.yaml`
2. `topics/<topic_id>/_ai/audience_profile.md`
3. `topics/<topic_id>/_ai/worklog.md`
4. `topics/<topic_id>/_ai/site_list.md`
5. `topics/<topic_id>/_ai/research/*.md` (Phase 2)
6. `topics/<topic_id>/index.md` and other guide notes (Phase 3)

### Files the agent writes

| Location | Phase | Content |
|----------|-------|---------|
| `_ai/site_list.md` | 1 | Sites/subjects to cover |
| `_ai/worklog.md` | 1–3 | Plans, sources, phase status |
| `_ai/research/<slug>.md` | 2 | Deep-dive working notes |
| `topics/<topic_id>/*.md` | 3 | Traveler-facing guide |
| `attachments/images/<slug>/` | 2 | CC/PD downloads + `ATTRIBUTION.md` |

---

## Research rules (mandatory)

**Allowed:** general knowledge; internet research; URLs from audience profile; downloads when audience requires.

**Forbidden:**

- Inventing coordinates, sunrise times, distances, or opening hours without a source.
- Running or creating download/analysis scripts without **explicit user permission**.
- Scope creep — stay within `region.name` and audience unless high audience benefit (log why in worklog).

---

## Audience work (separate from guide builds)

- Definitions: `audiences/<id>.md` — see [APPROACH.md](APPROACH.md).
- Root: `photographer` — only root may define `## Technical requirements`.
- Children: `## Additions` only (no `## Content requirements`).
- After edits: `python -m guide_generator.audiences`

---

## Topic folder layout

```
topics/<topic_id>/
├── index.md
├── …                     # Phase 3 guide notes
├── _ai/
│   ├── input.yaml
│   ├── audience_profile.md
│   ├── site_list.md      # Phase 1
│   ├── worklog.md
│   └── research/         # Phase 2 per-site notes
└── attachments/
```

---

## Session checklist (copy mentally)

- [ ] Identified task type: new guide / continue guide / audience edit / system / PDF
- [ ] Identified **build phase** (1 / 2 / 3) from worklog + site_list
- [ ] Ran correct Python commands (see table above)
- [ ] Read `audience_profile.md` before content work
- [ ] Phase 1: `site_list.md` updated before deep dives at scale
- [ ] Logged sources in `worklog.md` with phase
- [ ] Guide prose only in topic `.md` (Phase 3); research in `_ai/research/`

---

## Known gaps (do not assume implemented)

- PDF module (`guide_generator.pdf`) — implemented 2026-06-28
- `photographer` content requirements — still placeholder bullets
- Automatic web/cache layer — agent uses tools directly; log in worklog
