# Convex Schema Draft (Stage Import Phase)

Last updated: 2026-02-23

Purpose:
- Define a safe first schema for importing stage-table data into Convex.
- Keep all source fields preserved while we stabilize query paths.

Design approach:
- One collection per stage domain.
- Keep `notion_page_id` as the stable external id.
- Store original payload in `raw` first, then normalize in phase 2.

## Base document shape

```ts
{
  notionPageId: string,          // required, unique per collection
  sourceTable: string,           // e.g. "sacred_animals_stage"
  sourceSystem: "supabase_stage",
  importedAt: number,            // unix ms
  raw: any                       // full row payload from export
}
```

## Collections

- `sessionStopTriggers`
- `contraindications`
- `breathworkTaxonomy`
- `dailyRegulationSliders`
- `controlsLibraryDesign`
- `nadiSystem`
- `astrologyCalendricalSystems`
- `emotionBrainBodyEnergyMapping`
- `fullBrainNeuralSystems`
- `mythologicalBeings`
- `sacredAnimals`
- `stonesMinerals`

## Index recommendation

For each collection:
1. index on `notionPageId` (unique behavior in importer logic).
2. index on `sourceTable`.
3. optional text-search fields added in phase 2 only.

## Import rules

1. Insert when `notionPageId` does not exist.
2. Replace/update when `notionPageId` already exists.
3. Skip rows with missing `notion_page_id` and log them.

## Phase 2 normalization (after parity pass)

1. Add typed fields used by session runtime.
2. Add relation ids for cross-domain links.
3. Keep `raw` during transition, remove only when confident.
