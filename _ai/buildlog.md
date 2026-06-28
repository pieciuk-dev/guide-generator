# Build log

Short summaries of system-building work (not traveler-facing content).

---

## 2026-06-28 — Initial project setup

- Added project layout: `docs/`, `audiences/`, `data/`, `src/`, `output/`, `_ai/`.
- Documented audience model in `docs/APPROACH.md` (single root parent, no child override of parent; copy-from with explicit overrides).
- Created audience skeletons: `photographer`, `landscape_photographer`, `history_culture_lover` (placeholders for you to fill in).
- Added `audiences/_template.md`, `AGENTS.md`, and Cursor rule `.cursor/rules/guide-generator.mdc`.
- Bootstrapped Python package `guide_generator` with audience MD loader (`src/guide_generator/audiences/`).
- **Next:** you refine audience definitions; we extend setup (resolver, cache, guide pipeline) when requirements are clear.

---

## 2026-06-28 — Setup review fixes

- Clarified audience sections: root uses `## Content requirements`; children use `## Additions` only.
- Documented copy-from semantics, override syntax, trip schema, and output paths in `docs/APPROACH.md`.
- Split templates into `_template.root.md` and `_template.child.md`; updated child audience files.
- Added section parser, graph validator (`python -m guide_generator.audiences`), and tests.
- Added `docs/tasks/`, fixed `pyproject.toml` package layout and pytest `pythonpath`.
- **Next:** you refine `photographer.md`; then implement audience resolver + profile cache.

---

## 2026-06-28 — Guide workflow and topic scaffolding

- Documented guide pipeline in `docs/GUIDE_WORKFLOW.md`, Obsidian rules in `docs/OBSIDIAN.md`, PDF plan in `docs/PDF.md`.
- Trip schema: `region` (name, type, country) + `audience`; example `slowinski_landscape`.
- Topic folders under `topics/<id>/` with `_ai/`, `attachments/`, `index.md`.
- Implemented audience resolver (`guide_generator.audiences.resolve`) and topic init (`python -m guide_generator.topics init …`).
- Seeded `photographer` technical requirements (Obsidian output, research rules, no guessed facts, scripts need permission).
- **Next:** you refine audience content requirements; first real guide build on a chosen region.

---

## 2026-06-28 — AI runbook and CLI clarity

- Added `docs/AI_RUNBOOK.md` as single entry point for agent sessions (user intents → commands → build loop).
- Slimmed `AGENTS.md` to point at runbook; updated Cursor rule.
- Extended CLI: `audiences resolve`, `topics refresh-profile`.
- Fixed `photographer.md` missing YAML frontmatter (validation blocker).
- Documented existing-topic vs new-topic paths in `GUIDE_WORKFLOW.md`.

---

## 2026-06-28 — General guide build process + photographer content

- Added `docs/GUIDE_BUILD_PROCESS.md`: Phase 1 Discovery (`site_list.md`) → Phase 2 Deep dive (`_ai/research/`) → Phase 3 Compile.
- **Websites for search** in audience profile = Phase 1 starting URLs; later phases may add sources.
- Updated `photographer` content requirements and technical build-process link; landscape template for Websites.
- Topic scaffold now creates `site_list.md`, phased worklog, `research/` dir.

---

## 2026-06-28 — Remove example topic artifacts

- Deleted `topics/slowinski_landscape/` (guide instance, not project setup).
- Reverted `data/trips/_example.yaml` to generic placeholder; docs/tests use non-instantiated examples.

---

## 2026-06-28 — Gitignore guide output

- `.gitignore` now excludes all `topics/**` except `topics/_template/`; `data/trips/*` except `_example.yaml`; `data/cache/**`.
- Documented in `docs/AI_RUNBOOK.md`.
- **Next:** add landscape Websites for search URLs or start a guide when a region is chosen.

---

## 2026-06-28 — Phase 2 image requirements (audience + build process)

- **`landscape_photographer`:** explicit Phase 2 image search, URL minimums, CC/PD downloads, `ATTRIBUTION.md`.
- **`photographer`:** clarified that descendants requiring images trigger downloads in Phase 2 (not “downloads only when required” ambiguity).
- **`docs/GUIDE_BUILD_PROCESS.md`:** image minimums table, expanded research template (`Reference photographers` + `Reference images` tables); Phase 3 must use Phase 2 images.
- **`docs/AI_RUNBOOK.md`:** attachments path + image minimums in phase table.
- Applied catch-up on `olands_island_landscape` research files and partial Commons downloads.

---

## 2026-06-28 — PDF export module

- Implemented `python -m guide_generator.pdf <topic_id>` (Pandoc → HTML + xhtml2pdf).
- Optional deps: `pip install -e ".[pdf]"`; requires `pandoc` on PATH.
- Outputs `guide.pdf` and `guide.html` per topic; Öland reference build ~19 MB with embedded images.

---

## 2026-06-28 — `history_culture_lover` audience + Öland heritage guide

- **`audiences/history_culture_lover.md`:** filled as second **root** audience — deep-time heritage, stories with source links, chronology, conflict archaeology; no photography requirements.
- **`validate.py`:** allow multiple root audiences (independent guide families).
- **Trip + topic:** `data/trips/olands_island_history.yaml` → `topics/olands_island_history/` (18 sites, Phases 1–3 complete).
- Research template extended with Timeline + Stories tables; `compile_phase3.py` for heritage note structure.

---

## 2026-06-28 — History audience: dispersed-monument discovery

- **`history_culture_lover`:** added **Phase 1 discovery (required)** — monument inventory pass via official registers (Fornsök), beyond-landmarks rule, significance-over-size, clustering, gap check in worklog. No topic-specific monument types hardcoded.
- **Websites for search:** `app.raa.se/id/search` (Fornsök). Refreshed `olands_island_history` audience profile.

## 2026-06-28 — Supporting language (installation-wide)

- **`data/system.example.yaml`** + local **`data/system.yaml`** (gitignored): `supporting_language.name` / optional `code`.
- **`guide_generator.system`:** load config, `python -m guide_generator.system`, warnings on `audiences` validate.
- **`audience_profile.md`:** appends **System context** on init/refresh/resolve.
- **`photographer`:** technical + content bullets; child template shows wildlife/bird-name example pattern.
- Docs: APPROACH, GUIDE_BUILD_PROCESS Phase 0, AI_RUNBOOK, GETTING_STARTED.
