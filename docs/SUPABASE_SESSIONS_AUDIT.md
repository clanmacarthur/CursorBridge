# Supabase Sessions Audit

Last updated: 2026-02-22

## What I checked

- Live Supabase table endpoints and row counts (from the current connected project).
- Sessions runtime table usage from `task-manager` session code paths.
- New Notion page `Therapeutic Databases 0a` child databases.

## Snapshot

- Supabase tables detected: **73**
- Total rows across all detected tables: **977**
- Seed pass completed for required empty sessions tables (see `docs/_sessions_seed_report.json`).
- Priority requested: sessions-related tables first; infrastructure parked but listed.

## Sessions Core (execution path)

| table | rows | status |
|---|---:|---|
| `session_blueprints` | 22 | active |
| `blueprint_steps` | 9 | active |
| `blueprint_cues` | 0 | empty |
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
| `light_colour` | 43 | active |
| `chakra_systems` | 7 | active |
| `meridian_system` | 12 | active |
| `organ_emotion_system` | 15 | active |
| `elemental_framework` | 19 | active |
| `deities_archetypes` | 55 | active |
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

## Mapping tables you asked about

- `mappings`: 10 rows
- `cross_domain_mappings`: 6 rows
- `coupling_rules`: 8 rows
- `persona_lens_compatibility`: 9 rows
- `profile_pack_map`: 7 rows
- `programme_knowledge_map`: 5 rows
- Interpretation: relation scaffolding is now active, including previously empty coupling/profile relation tables.

## Duplicate / legacy risk flags (sessions context)

- `light_colour` is the active colour ontology table in Supabase.
- `sound_vibration` is the active sound ontology table in Supabase.
- No active Supabase runtime tables named `colours` or `sounds_tones` were found.
- Safety overlap to rationalize later: `safety_rules` and `rules_gating`, plus Notion stop/contra sources.
- Event-like table present: `sync_events` (currently 0 rows).

## New Notion Page 0a (child databases found)

| Notion DB title | rows | note |
|---|---:|---|
| `Deities & Archetypes (DB) — schema` | 1 | schema placeholder |
| `Symbols (DB) — schema` | 0 | schema placeholder |
| `Colours (DB) — schema` | 0 | schema placeholder |
| `Sacred Geometry (DB) — schema` | 0 | schema placeholder |
| `Sounds & Tones (DB) — schema` | 0 | schema placeholder |
| `Contraindications (Non-Exhaustive, Mandatory Disclosure)` | 11 | content/safety source |
| `During-Session Stop Triggers` | 7 | content/safety source |
| `Safety Rules` | 8 | content/safety source |

Observation: page 0a mostly adds schema/safety references. Colour/sound schema DBs there are placeholders, not canonical runtime sources yet.

## Sessions-first cleanup actions (recommended now)

1. Freeze canonical sessions table names: `light_colour`, `sound_vibration`, `mappings`, `cross_domain_mappings`, and session blueprint/runtime tables.
2. Keep Notion schema placeholders as `schema-only`; do not sync them into canonical runtime tables.
3. Keep and maintain the newly seeded relation/control tables (`persona_lens_compatibility`, `profile_pack_map`, `programme_knowledge_map`, `control_pack_items`, `default_weights`).
4. Reconcile safety stack: define one canonical runtime read path between `safety_rules`, `rules_gating`, and Notion stop/contra sources.
5. Create a deprecation list for non-sessions tables before Convex migration so legacy names do not reappear.

## Whole-system plan (parked but mapped)

- Keep infrastructure/AI/meta tables parked during sessions cleanup, but preserve inventory and row counts.
- After sessions tables are canonicalized, run a second pass for events/infrastructure/legislation and assign keep/merge/deprecate decisions.
