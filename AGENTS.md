# Agent instructions — guide-generator

**→ Start here: [`docs/AI_RUNBOOK.md`](docs/AI_RUNBOOK.md)**  
**→ New users: [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)**  
**→ Guide phases: [`docs/GUIDE_BUILD_PROCESS.md`](docs/GUIDE_BUILD_PROCESS.md)** (Discovery → Deep dive → Compile)

## Quick reference

```bash
pip install -e .
python -m guide_generator.audiences
python -m guide_generator.system          # supporting language (data/system.yaml)
python -m guide_generator.topics init data/trips/<id>.yaml
python -m guide_generator.topics refresh-profile <topic_id>
python -m pytest -q
```

## Task routing

| User asks | You do |
|-----------|--------|
| Build guide for &lt;region&gt; | Trip YAML → `topics init` → **Phase 1** ([process](docs/GUIDE_BUILD_PROCESS.md)) |
| Continue / work on &lt;topic&gt; | Read `_ai/worklog.md` + `site_list.md` → resume phase |
| Audience changes | `audiences` validate → `refresh-profile` per topic |
| PDF | After Phase 3 — [PDF.md](docs/PDF.md) |
| My Maps CSV | After Phase 3 — [MAPS.md](docs/MAPS.md) |

## Non-negotiables

- Three-phase build; `site_list.md` before bulk deep dives
- **Websites for search** in audience profile = Phase 1 starters (more sources OK later)
- Sourced facts only; scripts need user permission

## More detail

- [GUIDE_WORKFLOW.md](docs/GUIDE_WORKFLOW.md) · [APPROACH.md](docs/APPROACH.md) · [OBSIDIAN.md](docs/OBSIDIAN.md)
