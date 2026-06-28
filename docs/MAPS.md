# Google My Maps CSV export

Export guide sites as a **single CSV** for [Google My Maps](https://www.google.com/maps/d/) import.

## Command

```bash
python -m guide_generator.maps <topic_id>
```

Example:

```bash
python -m guide_generator.maps olands_island_history
```

Output: `topics/<topic_id>/guide_map.csv`

Optional path:

```bash
python -m guide_generator.maps olands_island_landscape -o path/to/sites.csv
```

## CSV columns

| Column | My Maps use |
|--------|-------------|
| **Name** | Marker title (select during import) |
| **Description** | Info-window text (short overview from guide) |
| **Latitude** | Position (decimal degrees, WGS84) |
| **Longitude** | Position |
| **Layer** | **Style by data column** → one icon/colour per group |
| **Priority** | must / should / optional (extra metadata) |
| **Type** | Site type from guide (ringfort, cluster, iconic, …) |
| **Slug** | Topic note filename stem (for cross-reference) |

## Import into Google My Maps

1. Open [Google My Maps](https://www.google.com/maps/d/) → **Create new map**.
2. **Import** → upload `guide_map.csv`.
3. Choose **Latitude** and **Longitude** for positioning.
4. Choose **Name** for marker titles.
5. After import: open the layer **⋮** menu → **Uniform style** → **Style by data column** → select **Layer**.
6. Assign a distinct icon (or colour) to each **Layer** value (e.g. “Iron Age ringforts”, “Inscribed stones & clusters”).

Sites without a parseable coordinate in the guide note are **omitted** unless listed in `_ai/map_coords.yaml` (WGS84 fallbacks with optional `note` for provenance). The CLI reports skipped slugs on stderr.

## Coordinate overrides (`_ai/map_coords.yaml`)

When a site is a cluster, linear feature, or only has a representative access point:

```yaml
sites:
  linear-villages-walls:
    latitude: 56.739278
    longitude: 16.710389
    note: "Representative — Himmelsberga row village"
```

Name and description still come from the compiled site note unless you set `name` / `description` in the override.

## Coordinates

Parsed from `## Location` or `## Location & access` in each site note:

- Decimal degrees in parentheses: `(56.552667, 16.639778)`
- Bare decimal pairs: `56.52804, 16.51992`
- DMS: `56°23′9″N, 16°25′59″E`

Representative points are used when the guide says “no single point” but gives a parking or access coordinate.

## When to run

After **Phase 3** compile, whenever site notes or coordinates change. Re-run before sharing the map alongside PDF export.
