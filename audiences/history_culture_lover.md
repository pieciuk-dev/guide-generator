---
id: history_culture_lover
parent: null
copy_from: []
---

# History & culture lover

## About

Travelers who explore places primarily for **deep time** — ancient history, early settlement, land use over millennia, archaeological landmarks, and the **stories** that attach to them. They care about prehistory, the Iron Age and Viking periods, medieval traces, and visible signs of conflict or upheaval (fortresses, battlefields, massacre sites, ruined strongholds).

They are **not** looking for conventional “history museum” tourism (royal dynasties, 19th–20th century trivia) unless it directly illuminates how the **landscape was shaped** or how people lived in earlier eras.

Root audience for heritage-focused guides. Defines baseline content rules and **locked technical requirements** for all descendant audiences.

## Technical requirements

- **Build process:** follow `docs/GUIDE_BUILD_PROCESS.md` — Phase 1 (discovery + site list) → Phase 2 (deep dive per site) → Phase 3 (compile guide). Track progress in `_ai/site_list.md` and `_ai/worklog.md`.
- **Output format:** Obsidian-compatible Markdown (see `docs/OBSIDIAN.md`). Multiple `.md` files per topic; split by logical section.
- **Topic layout:** each guide lives in `topics/<topic_id>/` with `_ai/` (agent files) and `attachments/` (images, audio). See `docs/GUIDE_WORKFLOW.md`.
- **Audience snapshot:** before research, use flat `topics/<topic_id>/_ai/audience_profile.md` (resolved from audience graph).
- **PDF:** compile on request only (`docs/PDF.md`); not part of initial generation.
- **Research:** general knowledge, internet research, and URLs listed under audience **Websites for search**. Log sources in `topics/<topic_id>/_ai/worklog.md` by phase.
- **Scripts:** create or run download/analysis scripts only with explicit human permission.
- **Facts:** dates, coordinates, distances, and similar data must come from cited sources — never from assumption or calculation without a source.
- **Scope:** stay within geographic constraint and audience; add off-topic material only when the audience would highly benefit (note rationale in worklog).

## Content requirements

- **Process:** all guides use the three-phase build in `docs/GUIDE_BUILD_PROCESS.md`; do not skip site-list discovery.
- **Sources:** cite or link sources for every factual claim and every story; maintain a source table in the topic worklog.
- **Chronology:** when a site spans multiple periods, give a brief **timeline** (earliest evidence → key phases → present) from sources.
- **Stories:** for each site where narrative material exists (legends, archaeological interpretations, documented events), include a **Stories** section with short retellings and **links to the full original** (museum page, academic article, saga translation, county museum blog, etc.). Distinguish **documented fact** from **tradition or interpretation** when sources do.
- **Heritage focus:** prioritize prehistoric and ancient sites, early settlement patterns, Iron Age and Viking remains, medieval ruins, UNESCO/cultural-landscape context, and **signs of conflict** (ringforts, battlefields, massacre archaeology, defensive works).
- **Exclude or de-emphasize:** modern tourism fluff, generic restaurant tips, and recent history unless it explains visible heritage.
- **Practical usability:** guides are field references — clear structure, scannable headings, access information, and cross-links between related sites (`[[wikilinks]]`).

### Phase 1 discovery (required)

Phase 1 must produce a site list that reflects **what actually exists in the region**, not only what tourism pages headline. Before approving `site_list.md`:

1. **Monument inventory pass** — Survey the country's **official heritage / archaeological register** (maps, databases, parish listings) for all registered monuments within the geographic constraint. Log which register was used and that the pass was completed in `worklog.md` Phase 1.
2. **Beyond landmarks** — Do not stop at famous complexes (castles, major grave fields, UNESCO zones). Actively look for **dispersed, small-scale, and single-object** sites: lone burial mounds and barrows, standing or carved stones, assembly markers, village ruins, churchyard antiquities, industrial remnants, and similar parish-level monuments that registers or scholarship record in the area.
3. **Judge by significance, not size** — Include a scattered site when sources show period importance, a documented event or tradition, unusual typology, or a cluster pattern across the landscape — even if the visit is “one stone in a field” or a relocated monument.
4. **Cluster when sensible** — Many minor monuments of the same type in one parish or valley may be **one site-list row** (e.g. a village's standing stones) with Phase 2 listing each object; do not omit a cluster because entries are small.
5. **Gap check** — In worklog Phase 1, briefly note any **register categories** present in the region but missing from the site list (e.g. “mounds present in Fornsök, none yet in list”) and justify omissions (destroyed, inaccessible, duplicate of included site).

### Per-site information (required for every location)

Each site entry in the guide must include, **from cited sources**:

- **Name and significance** — what it is, which period(s) it represents, and why it matters for understanding the region's deep past.
- **Historical context** — who lived here, how the place was used, and how it fits the wider island/regional story.
- **Stories** — legends, documented events, or archaeological narratives (with source links); omit section only if no sourced story exists.
- **Coordinates** — from a reliable map or official source.
- **Accessibility** — how to reach the site (roadside, trail, museum hours, seasonal access).
- **Access rules** — heritage protection, permits, fees, closures, respectful conduct at graves and ruins.
- **On site** — what to look for (visible remains, information boards, museum exhibits), and related sites nearby.
- **Sources** — key references the reader can follow for deeper reading.

### Guide structure hints

- Group sites by **era** or **region** (e.g. Iron Age ringforts, Viking graves, WH agricultural landscape, medieval strongholds).
- Tag priority (must / should / optional) and site type (fortress, grave field, landscape, museum, cluster, etc.).
- Cross-link related sites (e.g. ringforts to each other, WH villages to alvar context, monuments near a larger complex).

### Websites for search

<!-- Global starting points for heritage guides; add region-specific registers in topic worklog Phase 1. -->

- https://whc.unesco.org/ — UNESCO World Heritage documentation
- https://www.kulturarv.se/ — Swedish National Heritage Board (Riksantikvarieämbetet)
- https://app.raa.se/id/search — Fornsök / Swedish ancient-monument register (map + parish search)
- https://commons.wikimedia.org/ — images of sites and artifacts (check license)
