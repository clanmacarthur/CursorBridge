# Notion -> Supabase -> Convex Plan

Last updated: 2026-02-21

## Goal

1. Load in-scope Notion databases into Supabase safely.
2. Keep runtime stable while coverage grows.
3. Move to Convex after Supabase coverage is complete and verified.

## Situation assessment

### Good news

- Notion access is working with the `CursorBridgeSupabase` integration.
- Both target pages are accessible.
- `config/notion_db_ids.json` now includes 27 in-scope database IDs.
- The sessions master now includes the controls-first and profile-first rules.
- Live Supabase sessions-first audit now exists in `docs/SUPABASE_SESSIONS_AUDIT.md` (73 tables, sessions mapping breakdown).

### Risks to manage first

- `api/main.py` still uses hard-coded Notion IDs and does not read `config/notion_db_ids.json`.
- Supabase adapter cannot create tables via API; table SQL must be created first.
- Some Notion databases are design/schema drafts and should not overwrite canonical runtime tables yet.
- Core control tables are present but currently have zero rows, so runtime mapping would be underpowered.

## Phase 1: Lock scope and table targets

Create a table-target map with four buckets:

1. **Direct to existing canonical tables (priority first)**
   - `controls_library_design` -> `controls_library` (or `controls_library_stage` if final schema not locked)
   - `profile_pack_map` + profile-related model -> `user_profiles` support tables
   - Lock slider/checkbox/select metadata in control definitions before broad content expansion
   - `safety_rules` -> `safety_rules`
   - (`control_*`, `coupling_rules`, `derived_metrics`, `questionnaires*`) after row seeding

2. **Direct after Notion seeding (currently empty in Notion)**
   - `control_definitions`
   - `control_packs`
   - `default_weights`
   - `coupling_rules`
   - `derived_metrics`
   - `questionnaires`
   - `questionnaire_questions`

3. **Stage-first (new data, not in current canon table names)**
   - `sacred_animals`
   - `stones_minerals`
   - `astrology_calendrical_systems`
   - `mythological_beings`
   - `nadi_system`
   - `emotion_brain_body_energy_mapping`
   - `full_brain_neural_systems_table`
   - `breathwork_master_taxonomy`
   - `daily_regulation_sliders`
   - `contraindications_mandatory_disclosure`
   - `during_session_stop_triggers`
   - `colour_legacy_archive`

4. **Schema-only / parked**
   - `colours_schema`
   - `symbols_schema`
   - `sacred_geometry_schema`
   - `sounds_tones_schema`
   - `deities_archetypes_schema` (currently only 1 row)

Deliverable:
- `docs/THEME_TABLE_CATALOG.md` updated with `target_table` and `sync_mode` (`direct`, `stage`, `parked`).

## Phase 2: Supabase schema prep

Before ingestion:

1. Add missing stage tables in Supabase.
2. Keep canonical tables untouched unless mapping is confirmed.
3. Ensure each stage table has:
   - `id` primary key
   - `notion_page_id`
   - created/updated timestamps

Deliverable:
- SQL migration file for stage tables (for example `sql/notion_stage_tables.sql`).

## Phase 3: Import Notion data into Supabase

Run dry-runs first, then live import.

For each in-scope DB:

1. Dry run:
   - fetch rows
   - confirm field mapping
2. Live run:
   - write to mapped target table
3. Verify:
   - row count in Supabase
   - sample row integrity

Deliverable:
- import report with `rows_in_notion`, `rows_written`, `errors`.

## Phase 4: Normalize and promote into canonical tables

For stage tables:

1. Normalize field names and relation links.
2. Resolve duplicates/legacy overlap.
3. Promote approved rows into canonical tables.
4. Keep provenance fields (`source_db`, `source_page_id`).

Deliverable:
- promotion SQL/scripts + audit log.

## Phase 5: App integration checks

After Supabase load:

1. Verify current app still works (`/session`, bridge endpoints).
2. Confirm planned `/sessions` work can read new tables later.
3. Update docs and canon manifests for any newly accepted canonical tables.

Deliverable:
- build/test report and updated docs.

## Phase 6: Convex migration (after Supabase stable)

1. Mirror approved Supabase canonical tables into Convex collections.
2. Add adapter layer so app code uses one interface.
3. Run dual-read checks (Supabase vs Convex output).
4. Cut over reads to Convex in steps.

Deliverable:
- Convex cutover checklist + parity report.

## Immediate next actions

1. Update sync endpoint to load IDs from `config/notion_db_ids.json` instead of hard-coded map.
2. Create stage table SQL for non-canonical in-scope databases.
3. Run first ingestion batch for high-value datasets:
   - `sacred_animals`
   - `stones_minerals`
   - `mythological_beings`
   - `astrology_calendrical_systems`
   - `nadi_system`
