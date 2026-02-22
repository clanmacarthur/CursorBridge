# Sessions Keep/Merge/Deprecate Matrix

Last updated: 2026-02-22
Scope: sessions-only canonicalization before wider system cleanup.

Decision legend:
- `KEEP_CANON`: keep as canonical table now
- `KEEP_SEED`: keep table, but seed/populate now
- `KEEP_RUNTIME`: keep as runtime write table, even if currently empty
- `MERGE_REVIEW`: overlapping role; keep for now but unify read path

## Supabase Sessions Tables

| table | rows | decision | reason | used_in_session_code | immediate action |
|---|---:|---|---|---|---|
| `ai_depth_levels` | 6 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `archetypal_personas` | 26 | `KEEP_CANON` | active sessions table | `session-dial-library.ts,session-plan.ts` | no rename; keep as source of truth |
| `blueprint_cues` | 0 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `blueprint_steps` | 9 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `chakra_systems` | 7 | `KEEP_CANON` | active sessions table | `session-dial-library.ts` | no rename; keep as source of truth |
| `control_definitions` | 15 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `control_pack_items` | 12 | `KEEP_CANON` | seeded and now active | `` | no rename; keep as source of truth |
| `control_packs` | 7 | `KEEP_CANON` | active sessions table | `session-dial-library.ts` | no rename; keep as source of truth |
| `coupling_rules` | 8 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `cross_domain_mappings` | 6 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `cue_triggers` | 20 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `default_weights` | 7 | `KEEP_CANON` | seeded and now active | `` | no rename; keep as source of truth |
| `deities_archetypes` | 55 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `derived_metrics` | 6 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `elemental_framework` | 19 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `knowledge_bases` | 31 | `KEEP_CANON` | active sessions table | `session-dial-library.ts,session-plan.ts` | no rename; keep as source of truth |
| `lens_definitions` | 22 | `KEEP_CANON` | active sessions table | `session-dial-library.ts,session-plan.ts` | no rename; keep as source of truth |
| `light_colour` | 43 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `mappings` | 10 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `meridian_system` | 12 | `KEEP_CANON` | active sessions table | `session-dial-library.ts` | no rename; keep as source of truth |
| `narration_styles` | 8 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `nutrition_and_food` | 59 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `nutrition_protocols` | 12 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `organ_emotion_system` | 15 | `KEEP_CANON` | active sessions table | `session-dial-library.ts` | no rename; keep as source of truth |
| `persona_lens_compatibility` | 9 | `KEEP_CANON` | seeded and now active | `session-dial-library.ts` | no rename; keep as source of truth |
| `profile_pack_map` | 7 | `KEEP_CANON` | seeded and now active | `session-dial-library.ts` | no rename; keep as source of truth |
| `programme_knowledge_map` | 5 | `KEEP_CANON` | seeded and now active | `session-dial-library.ts` | no rename; keep as source of truth |
| `questionnaire_questions` | 6 | `KEEP_CANON` | seeded and now active | `` | no rename; keep as source of truth |
| `questionnaire_responses` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `` | keep schema; expect rows once sessions run live |
| `questionnaires` | 1 | `KEEP_CANON` | seeded and now active | `` | no rename; keep as source of truth |
| `rules_gating` | 20 | `MERGE_REVIEW` | overlap risk in safety logic; define one runtime read path | `` | define single canonical runtime read path |
| `sacred_geometry` | 21 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `safety_rules` | 8 | `MERGE_REVIEW` | overlap risk in safety logic; define one runtime read path | `` | define single canonical runtime read path |
| `session_blueprints` | 22 | `KEEP_CANON` | active sessions table | `session-plan.ts` | no rename; keep as source of truth |
| `session_outputs` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `generate.post.ts` | keep schema; expect rows once sessions run live |
| `session_phases` | 7 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `session_runs` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `generate.post.ts` | keep schema; expect rows once sessions run live |
| `session_scope_log` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `` | keep schema; expect rows once sessions run live |
| `session_templates` | 22 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `session_types` | 6 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `sound_vibration` | 10 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `symbols_index` | 94 | `KEEP_CANON` | active sessions table | `session-dial-library.ts` | no rename; keep as source of truth |
| `technique_lens_explanations` | 48 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `technique_steps` | 21 | `KEEP_CANON` | active sessions table | `session-dial-library.ts,session-plan.ts` | no rename; keep as source of truth |
| `techniques` | 22 | `KEEP_CANON` | active sessions table | `session-dial-library.ts,session-plan.ts` | no rename; keep as source of truth |
| `timing_presets` | 7 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `transition_rules` | 6 | `KEEP_CANON` | active sessions table | `` | no rename; keep as source of truth |
| `user_checkins` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `` | keep schema; expect rows once sessions run live |
| `user_dashboard_layouts` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `` | keep schema; expect rows once sessions run live |
| `user_knowledge_access` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `` | keep schema; expect rows once sessions run live |
| `user_lens_context` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `` | keep schema; expect rows once sessions run live |
| `user_lens_preferences` | 1 | `KEEP_CANON` | active sessions table | `generate.post.ts` | no rename; keep as source of truth |
| `user_technique_blends` | 0 | `KEEP_RUNTIME` | runtime/user-write table; keep even if currently empty | `` | keep schema; expect rows once sessions run live |

## Notion Placeholder -> Supabase Canonical Mapping

| notion key | notion rows | canonical supabase table | decision | note |
|---|---:|---|---|---|
| `colours_schema` | 0 | `light_colour` | `MAP_ONLY` | schema placeholder in Notion; keep Supabase `light_colour` canonical |
| `sounds_tones_schema` | 0 | `sound_vibration` | `MAP_ONLY` | schema placeholder in Notion; keep Supabase `sound_vibration` canonical |
| `symbols_schema` | 0 | `symbols_index` | `MAP_ONLY` | schema placeholder in Notion; keep Supabase `symbols_index` canonical |
| `sacred_geometry_schema` | 0 | `sacred_geometry` | `MAP_ONLY` | schema placeholder in Notion; keep Supabase `sacred_geometry` canonical |
| `deities_archetypes_schema` | 1 | `deities_archetypes` | `MAP_ONLY` | schema placeholder in Notion; keep Supabase `deities_archetypes` canonical |
| `colour_legacy_archive` | 23 | `light_colour` | `MAP_ONLY` | legacy/archive source; do not replace canonical ontology table |

## Direct answers to your mapping concerns

- Colour canonical now: `light_colour` (not a `colours` runtime table).
- Sound canonical now: `sound_vibration` (not a `sounds_tones` runtime table).
- Relations layer exists now: `mappings`, `cross_domain_mappings`, `coupling_rules`.
- Previously empty coupling/profile tables are now seeded: `persona_lens_compatibility`, `profile_pack_map`, `programme_knowledge_map`.

## Sessions-first execution order

1. Freeze canonical names in this matrix (no new alias tables).
2. Keep seeded relation/control tables under change control (no ad-hoc edits).
3. Unify safety read path (`safety_rules` vs `rules_gating` and Notion stop/contra sources).
4. Run session preview/generate smoke tests against this canonical set only.
