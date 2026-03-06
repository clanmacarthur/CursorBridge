# Notion to Supabase Sync Run

Run date: 2026-02-23
Mode: live apply

## Final summary (after stage table creation)

- Notion databases configured: 30
- Synced groups: 27
- Blocked groups: 0
- Skipped groups (admin trackers): 3
- Sync errors: 0

## Rows processed

- Rows found in Notion: 396
- Rows inserted: 364
- Rows updated: 32
- Rows failed: 0

This confirms idempotent upsert by `notion_page_id` and full coverage for all in-scope runtime groups.

## Stage table result

The missing-table groups were resolved by creating stage tables and re-running sync.

Stage tables now loaded:

- `astrology_calendrical_systems_stage` (21)
- `breathwork_master_taxonomy_stage` (12)
- `contraindications_mandatory_disclosure_stage` (11)
- `controls_library_design_stage` (13)
- `daily_regulation_sliders_stage` (11)
- `during_session_stop_triggers_stage` (7)
- `emotion_brain_body_energy_mapping_stage` (12)
- `full_brain_neural_systems_table_stage` (19)
- `mythological_beings_stage` (23)
- `nadi_system_stage` (10)
- `sacred_animals_stage` (170)
- `stones_minerals_stage` (55)

## SQL syntax fix applied

The stage SQL generator now quotes all SQL identifiers.

This fixed reserved-word column names such as:

- `column`
- `type`
- `action`

File: `sql/notion_stage_tables.sql`

## Files generated/updated

- `docs/_notion_supabase_sync_full_report.json`
- `docs/_notion_supabase_table_diff.json`
- `docs/_supabase_inventory_live.json`
- `sql/notion_stage_tables.sql`
- `scripts/sync_notion_to_supabase_full.py`

## Notes

- Admin relation tracker Notion databases are intentionally skipped in data sync:
  - `relations_master`
  - `relations_existing`
  - `relations_to_be`
- Relation checkboxes were synced separately using:
  - `scripts/create_notion_relations_registry.py`
