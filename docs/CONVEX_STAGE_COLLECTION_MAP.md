# Convex Stage Collection Map

Last updated: 2026-02-23

Purpose:
- Define how the 12 Supabase `_stage` tables map into Convex collections.
- Keep Supabase stable while we prepare major model changes in Convex.

Current status:
- Supabase write batches are blocked by preflight (`STOP_WRITE_BATCHES_FOR_NOW`).
- This map is the recommended path forward.

## Proposed collection mapping

| Supabase stage table | Rows | Proposed Convex collection | Notes |
|---|---:|---|---|
| `during_session_stop_triggers_stage` | 7 | `sessionStopTriggers` | Safety control; keep simple shape first. |
| `contraindications_mandatory_disclosure_stage` | 11 | `contraindications` | Safety-first collection. |
| `breathwork_master_taxonomy_stage` | 12 | `breathworkTaxonomy` | Can later merge into wider practice taxonomy. |
| `daily_regulation_sliders_stage` | 11 | `dailyRegulationSliders` | UI/runtime support model. |
| `controls_library_design_stage` | 13 | `controlsLibraryDesign` | Design/config source; may merge with controls later. |
| `nadi_system_stage` | 10 | `nadiSystem` | Ontology domain table. |
| `astrology_calendrical_systems_stage` | 21 | `astrologyCalendricalSystems` | Ontology domain table. |
| `emotion_brain_body_energy_mapping_stage` | 12 | `emotionBrainBodyEnergyMapping` | Cross-domain mapping table. |
| `full_brain_neural_systems_table_stage` | 19 | `fullBrainNeuralSystems` | Reference/ontology table. |
| `mythological_beings_stage` | 23 | `mythologicalBeings` | Symbolic domain; may cross-link with deities/symbols later. |
| `sacred_animals_stage` | 170 | `sacredAnimals` | Large symbolic reference set. |
| `stones_minerals_stage` | 55 | `stonesMinerals` | Symbolic/material reference set. |

## Field strategy

Rules:
1. Keep source field names intact on first import.
2. Keep `notion_page_id` as external stable key.
3. Add normalized aliases in Convex only after baseline parity import is stable.

Example baseline Convex document pattern:

```ts
{
  source: "supabase_stage",
  source_table: "sacred_animals_stage",
  notion_page_id: "...",
  raw: { ...all original fields... },
  imported_at: "...iso timestamp..."
}
```

This avoids losing data while allowing later schema cleanup.

## Relationship strategy (phase 2 in Convex)

After baseline import:
1. Add link fields using normalized ids (not free text).
2. Build join collections for many-to-many links.
3. Add query helpers for session generation paths.

Do not do this before baseline parity import passes.
