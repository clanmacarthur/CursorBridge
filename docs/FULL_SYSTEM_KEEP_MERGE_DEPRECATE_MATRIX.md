# Full-System Keep/Merge/Deprecate Matrix

Last updated: 2026-02-22
Scope: all live Supabase tables, with sessions-first priority applied.

| table | rows | category | decision | reason |
|---|---:|---|---|---|
| `aggregate_patterns` | 3 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `ai_confidence_levels` | 6 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `ai_decision_log` | 0 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `ai_depth_levels` | 6 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `ai_scope_levels` | 6 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `ai_source_levels` | 5 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `archetypal_personas` | 26 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `attribute_taxonomy` | 76 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `blueprint_cues` | 0 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `blueprint_steps` | 9 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `breath_library` | 26 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `chakra_systems` | 7 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `control_definitions` | 15 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `control_pack_items` | 12 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `control_packs` | 7 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `coupling_rules` | 8 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `cross_domain_mappings` | 6 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `cue_triggers` | 20 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `dashboard_blocks` | 19 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `deep_work_permissions` | 0 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `default_weights` | 7 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `deities_archetypes` | 55 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `derived_metrics` | 6 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `elemental_framework` | 19 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `evidence_sources` | 12 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `experimental_flags` | 0 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `knowledge_bases` | 31 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `lens_definitions` | 22 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `light_colour` | 43 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `mappings` | 10 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `meridian_system` | 12 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `meta_lens_presets` | 5 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `movements_system` | 16 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `narration_styles` | 8 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `nutrition_and_food` | 59 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `nutrition_intake` | 5 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `nutrition_protocols` | 12 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `organ_emotion_system` | 15 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `persona_kb_compatibility` | 0 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `persona_lens_compatibility` | 9 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `profile_pack_map` | 7 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `programme_knowledge_map` | 5 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `programme_profiles` | 14 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `questionnaire_questions` | 6 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `questionnaire_responses` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `questionnaires` | 1 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `rules_gating` | 20 | `SESSIONS_SCOPE` | `MERGE_REVIEW` | overlap to merge |
| `sacred_geometry` | 21 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `safety_rules` | 8 | `SESSIONS_SCOPE` | `MERGE_REVIEW` | overlap to merge |
| `session_blueprints` | 22 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `session_outputs` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `session_phases` | 7 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `session_runs` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `session_scope_log` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `session_templates` | 22 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `session_types` | 6 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `sound_vibration` | 10 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `supplement_interactions` | 14 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `symbols_index` | 94 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `sync_events` | 0 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `system_manifest` | 9 | `BROADER_DOMAIN` | `PARK_REVIEW` | outside immediate sessions core; map in full-system pass |
| `technique_lens_explanations` | 48 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `technique_steps` | 21 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `techniques` | 22 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `timing_presets` | 7 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `transcriptions_staging` | 3 | `INFRA_META` | `PARK` | infrastructure/meta/ops; park for sessions phase |
| `transition_rules` | 6 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `user_checkins` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `user_dashboard_layouts` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `user_knowledge_access` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `user_lens_context` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |
| `user_lens_preferences` | 1 | `SESSIONS_SCOPE` | `KEEP_CANON` | sessions-related table |
| `user_technique_blends` | 0 | `SESSIONS_SCOPE` | `KEEP_RUNTIME` | sessions-related table |

## Parked Buckets (requested)

- Infrastructure/meta/ops tables are marked `PARK` during sessions cleanup.
- Broader-domain tables (events-like, taxonomy-wide, auxiliary libraries) are marked `PARK_REVIEW` for the whole-system pass.
- No legislation/policy table was detected in the current Supabase table snapshot.

## Next whole-system pass

1. For each `PARK_REVIEW` table, assign one of: `KEEP_CANON`, `STAGE_ONLY`, `MERGE_INTO`, `DEPRECATE`.
2. Add owner module and API read/write path for each kept table.
3. Freeze a pre-Convex canonical table list and ban new legacy aliases.
