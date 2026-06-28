# guide-generator

Build **custom travel guides** for a specific **place** and **audience** — for example, a landscape photography guide for an island, or a heritage guide for history-minded travelers.

Guides are produced as **Obsidian-compatible Markdown** in local topic folders. You can optionally export **PDF** and a **Google My Maps CSV**. Research and writing are designed to run with an **AI assistant** (e.g. Cursor) following a structured three-phase workflow: discovery → deep dive per site → compile for travelers.

## Quick start

```bash
pip install -e .
python -m guide_generator.audiences
python -m guide_generator.topics init data/trips/<your_trip>.yaml
```

Full setup, tools, risks, and disclaimer: **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)**

| Topic | Document |
|-------|----------|
| AI / agent workflow | [docs/AI_RUNBOOK.md](docs/AI_RUNBOOK.md) |
| Build phases | [docs/GUIDE_BUILD_PROCESS.md](docs/GUIDE_BUILD_PROCESS.md) |
| Audiences | [docs/APPROACH.md](docs/APPROACH.md) |
| PDF export | [docs/PDF.md](docs/PDF.md) |
| Map export | [docs/MAPS.md](docs/MAPS.md) |

Guide output (`topics/`, trip YAMLs, `data/system.yaml`) stays **local** by default — see `.gitignore`.

## Author

**Piotr Pieciukiewicz**

- **Tutorials:** [framesyntax.com](https://framesyntax.com) — guides and articles on photography and related topics  
- **Instagram:** [@pieciukiewicz.photography](https://www.instagram.com/pieciukiewicz.photography/)

## License

See repository license file if present. Generated guide content you create locally is yours; verify licenses for any third-party images or sources you include.
