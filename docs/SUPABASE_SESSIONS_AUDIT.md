# Supabase Sessions Audit

Last updated: 2026-03-05

## What I checked

- Live Supabase table endpoints and row counts (fresh inventory run).
- Full Notion -> Supabase sync output after stage tables were created.
- Relation tracker checkbox state in `RELATIONS_MASTER.csv` and Notion relation DBs.

## Snapshot

- Supabase tables detected: **85**
- Total rows across all detected tables: **1373**
- Stage tables now active: **12 tables**, **364 rows**
- Priority remains sessions-related tables first; broader infrastructure is still parked.

## Live refresh (2026-03-05)

- Ran dry-run sync checks again and refreshed:
  - `docs/_notion_supabase_sync_full_report.json`
  - `docs/_notion_next_to_used_sessions_sync.json`
- Scanned Notion page `Therapeutic Databases 0a` (`36207156f7034c13a839249dee0afe1a`) and wrote:
  - `docs/_notion_0a_page_scan.json`
- Current result for that page:
  - Total databases found: **14**
  - Already tracked in config: **8**
  - Missing in `config/notion_db_ids.json`: **6**
- The 6 currently untracked IDs:
  - `6ed9bf3a5974460c986c6f82185fa7d1` (`New database`)
  - `addec191b2a9447aa7352af8543b2c96` (`Untitled`)
  - `b7179b0cdda243619e8f20d275ec9b4c` (`Untitled`)
  - `d1503be4cdb0412e8957f074f756de79` (`Finance Tracker (1)`)
  - `dc63ed2c9455406b9c6d41d8e5e8325b` (`Finance Tracker`)
  - `f5a434341cb944d2b5117331ac7cbc49` (`Untitled`)
- Profile details for the 6 were saved in:
  - `docs/_notion_0a_missing_db_profiles.json`
- Initial classification:
  - 2 are clearly finance-only (`Finance Tracker`, `Finance Tracker (1)`), not sessions.
  - 1 is a tiny generic table (`Name`, `Tags`) with 3 rows and no sessions signals.
  - 3 cannot be read by the current Notion integration token (API returns not accessible).

## Sessions composer readiness (2026-03-05)

- Live domain/filter audit created:
  - `docs/SESSIONS_COMPOSER_DOMAIN_AUDIT_2026-03-05.md`
  - `docs/_sessions_composer_domain_audit_2026-03-05.json`
- Locked build spec created:
  - `docs/SESSIONS_COMPOSER_LOCKED_SPEC_2026-03-05.md`
- Legacy architecture archived:
  - `docs/legacy/SESSIONS_COMPOSER_LOCKED_SPEC_PRE_RESET_2026-03-05.md`
  - `docs/legacy/SESSION_GENERATION_RUNTIME_SPEC_LEGACY_2026-03-05.md`
- Strict actual-values-only composer inventory pass created:
  - `docs/SESSIONS_DOMAIN_INVENTORY_2026-03-05.md`
  - `docs/SESSIONS_SUBJECT_TREE_2026-03-05.md`
  - `docs/SESSIONS_FIELD_MAP_2026-03-05.md`
- Hard blocker count: **0**
- Important note for UI/filter build:
  - Some planned filter columns exist but currently have no values in live rows.
  - This means UI filters must hide empty filter groups and only show filters with actual values.

## Sessions Core (execution path)

| table | rows | status |
|---|---:|---|
| `session_blueprints` | 22 | active |
| `blueprint_steps` | 9 | active |
| `blueprint_cues` | 66 | active |
| `cue_triggers` | 20 | active |
| `session_templates` | 22 | active |
| `session_types` | 6 | active |
| `session_phases` | 7 | active |
| `timing_presets` | 7 | active |
| `transition_rules` | 6 | active |
| `techniques` | 22 | active |
| `technique_steps` | 21 | active |
| `narration_styles` | 8 | active |
| `session_runs` | 0 | empty |
| `session_outputs` | 0 | empty |
| `session_scope_log` | 0 | empty |

## Theme/Ontology (wheel domains)

| table | rows | status |
|---|---:|---|
| `lens_definitions` | 22 | active |
| `light_colour` | 66 | active |
| `chakra_systems` | 7 | active |
| `meridian_system` | 12 | active |
| `organ_emotion_system` | 15 | active |
| `elemental_framework` | 19 | active |
| `deities_archetypes` | 56 | active |
| `symbols_index` | 94 | active |
| `sacred_geometry` | 21 | active |
| `sound_vibration` | 10 | active |
| `nutrition_protocols` | 12 | active |
| `nutrition_and_food` | 59 | active |
| `knowledge_bases` | 31 | active |

## Mappings and Relations

| table | rows | status |
|---|---:|---|
| `mappings` | 10 | active |
| `cross_domain_mappings` | 6 | active |
| `coupling_rules` | 8 | active |
| `persona_lens_compatibility` | 9 | active |
| `profile_pack_map` | 7 | active |
| `programme_knowledge_map` | 5 | active |
| `control_pack_items` | 12 | active |

## User State and Controls

| table | rows | status |
|---|---:|---|
| `control_definitions` | 15 | active |
| `control_packs` | 7 | active |
| `default_weights` | 7 | active |
| `derived_metrics` | 6 | active |
| `questionnaires` | 1 | active |
| `questionnaire_questions` | 6 | active |
| `questionnaire_responses` | 0 | empty |
| `user_checkins` | 0 | empty |
| `user_lens_preferences` | 1 | active |
| `user_dashboard_layouts` | 0 | empty |
| `user_lens_context` | 0 | empty |
| `user_technique_blends` | 0 | empty |
| `user_knowledge_access` | 0 | empty |

## Stage Tables (newly loaded from Notion)

| table | rows | status |
|---|---:|---|
| `astrology_calendrical_systems_stage` | 21 | active |
| `breathwork_master_taxonomy_stage` | 12 | active |
| `contraindications_mandatory_disclosure_stage` | 11 | active |
| `controls_library_design_stage` | 13 | active |
| `daily_regulation_sliders_stage` | 11 | active |
| `during_session_stop_triggers_stage` | 7 | active |
| `emotion_brain_body_energy_mapping_stage` | 12 | active |
| `full_brain_neural_systems_table_stage` | 19 | active |
| `mythological_beings_stage` | 23 | active |
| `nadi_system_stage` | 10 | active |
| `sacred_animals_stage` | 170 | active |
| `stones_minerals_stage` | 55 | active |

## Relation Tracker Checkbox Snapshot

- Master relation rows: **55**
- `on_supabase = true`: **45**
- `supabase_configured = true`: **18**
- `needs_more_data = true`: **8**
- `ready_for_launch = true`: **18**
- Notion relation databases were synced from CSV on 2026-02-23.

## Infrastructure / Broader System (parked for now)

| table | rows | status |
|---|---:|---|
| `system_manifest` | 9 | active |
| `dashboard_blocks` | 19 | active |
| `rules_gating` | 20 | active |
| `aggregate_patterns` | 3 | active |
| `ai_scope_levels` | 6 | active |
| `ai_depth_levels` | 6 | active |
| `ai_source_levels` | 5 | active |
| `ai_confidence_levels` | 6 | active |
| `ai_decision_log` | 0 | empty |
| `experimental_flags` | 0 | empty |
| `deep_work_permissions` | 0 | empty |
| `sync_events` | 0 | empty |
| `transcriptions_staging` | 3 | active |
| `meta_lens_presets` | 5 | active |
| `nutrition_intake` | 5 | active |
| `supplement_interactions` | 14 | active |
| `breath_library` | 26 | active |
| `movements_system` | 16 | active |
| `archetypal_personas` | 26 | active |
| `attribute_taxonomy` | 76 | active |
| `programme_profiles` | 14 | active |
| `evidence_sources` | 12 | active |
| `persona_kb_compatibility` | 0 | empty |

## Sessions-first cleanup actions (recommended now)

1. Keep canonical sessions table names fixed: `light_colour`, `sound_vibration`, `mappings`, `cross_domain_mappings`, and session blueprint/runtime tables.
2. Keep schema-only Notion sources in stage tables until canonical mapping is approved table-by-table.
3. Move stage tables into canonical tables only when relation keys and field names are fully locked.
4. Keep relation tracker checkboxes updated at the end of each migration step.
5. Prepare Convex migration mapping only after the above reaches stable parity.


Update note (2026-02-26): lueprint_cues was seeded with baseline phase_start/interval/phase_end links for all existing session blueprints.
