# Guide Generator — Vision

A system for building **custom travel guides** tailored to specific **audiences** and **geographic regions**.

Each guide is a **topic folder**: research and Markdown content for a place (island, region, national park, …) written for one resolved audience profile. Output is **Obsidian-compatible Markdown**; **PDF** is compiled on request.

## Goals

- Audience-first guides (not one-size-fits-all itineraries)
- Region + audience → clear research and content scope
- Reusable audience definitions in a graph (parent chain + copy-from)
- Reliable research discipline (sourced facts, no guessed coordinates)
- Cached profiles and incremental work to save time and cost
- Separation: specs (`audiences/`, `docs/`), topics (`topics/`), system log (`_ai/`)

## First use case

Audience tree rooted at **photographer**, with children:

- `landscape_photographer`
- `history_culture_lover`

See [APPROACH.md](APPROACH.md), [GUIDE_WORKFLOW.md](GUIDE_WORKFLOW.md), and [../audiences/](../audiences/).
