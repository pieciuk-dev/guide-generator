---
id: photographer
parent: null
copy_from: []
---

# Photographer

## About

Photography enthusiasts who travel mainly with photography in mind. They need location-specific tips aligned with their favorite genre and solid technical guidance.

Root audience for the first use case. Defines baseline content rules and **locked technical requirements** for all descendant audiences.

## Technical requirements

- **Build process:** follow `docs/GUIDE_BUILD_PROCESS.md` — Phase 1 (discovery + site list) → Phase 2 (deep dive per site) → Phase 3 (compile guide). Track progress in `_ai/site_list.md` and `_ai/worklog.md`.
- **Output format:** Obsidian-compatible Markdown (see `docs/OBSIDIAN.md`). Multiple `.md` files per topic; split by logical section.
- **Topic layout:** each guide lives in `topics/<topic_id>/` with `_ai/` (agent files) and `attachments/` (images, audio). See `docs/GUIDE_WORKFLOW.md`.
- **Audience snapshot:** before research, use flat `topics/<topic_id>/_ai/audience_profile.md` (resolved from audience graph).
- **PDF:** compile on request only (`docs/PDF.md`); not part of initial generation.
- **Research:** general knowledge, internet research, and URLs listed under audience **Websites for search**. Log sources in `topics/<topic_id>/_ai/worklog.md` by phase.
- **Media downloads:** when a descendant audience **requires reference images** (e.g. `landscape_photographer`), Phase 2 must **search, license-check, and download** CC/public-domain files to `attachments/images/<slug>/`; link-only for restricted licenses. See `docs/GUIDE_BUILD_PROCESS.md` image minimums.
- **Scripts:** create or run download/analysis scripts only with explicit human permission.
- **Facts:** coordinates, times, distances, and similar data must come from cited sources — never from assumption or calculation without a source.
- **Scope:** stay within geographic constraint and audience; add off-topic material only when the audience would highly benefit (note rationale in worklog).
- **Supporting language:** installation-wide setting in `data/system.yaml` (see **System context** in the resolved audience profile). Child audiences may require specific labels in that language — e.g. local bird names for a wildlife photographer — without translating the whole guide.

## Content requirements

- **Process:** all guides use the three-phase build in `docs/GUIDE_BUILD_PROCESS.md`; do not skip site-list discovery.
- **Sources:** cite or link sources for factual claims; maintain a source table in the topic worklog.
- **Permissions:** respect local laws, park rules, privacy, and photography restrictions at each site.
- **Attribution:** credit photographers, authors, and image rights holders; maintain `attachments/images/ATTRIBUTION.md` per topic.
- **Practical usability:** guides are field references — prefer clear structure, scannable headings, and actionable access information over long prose.
- **Supporting language:** when a child audience asks for names or terms in the reader's **supporting language**, use the language configured in `data/system.yaml` and surfaced in **System context** of `audience_profile.md`. Keep authoritative regional or scientific names from sources; add supporting-language forms only where the audience specifies (species names, local aliases, etc.).

### Websites for search

<!-- Add root-level URLs useful for any photography guide (maps, commons, global portfolios). Child audiences add region-specific URLs in ## Additions. -->

- _None defined at root yet — add trusted global resources here, or list per-audience URLs in child definitions._
