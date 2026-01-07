# System Manifest

Generated: 2026-01-04T23:38:46Z
Source: Supabase PostgREST OpenAPI (introspected) + docs/SYSTEM_MANIFEST.md where available

| table_name | purpose | level | runtime | dependencies |
|---|---|---|---|---|
| aggregate_patterns | Stores aggregate patterns records. | engine-level | read-only library | - |
| ai_confidence_levels | Stores ai confidence levels records. | engine-level | read-only library | - |
| ai_decision_log | Log records for ai decision log. | engine-level | execution | - |
| ai_depth_levels | Stores ai depth levels records. | engine-level | read-only library | - |
| ai_scope_levels | Stores ai scope levels records. | engine-level | read-only library | - |
| ai_source_levels | Stores ai source levels records. | engine-level | read-only library | - |
| archetypal_personas | AI persona styles (canonical "Style" system). | sector-level | read-only library | - |
| attribute_taxonomy | Universal hierarchy for all capabilities, domains, parameters. | engine-level | read-only library | - |
| blueprint_cues | Stores blueprint cues records. | engine-level | execution | - |
| blueprint_steps | Stores blueprint steps records. | engine-level | execution | - |
| breath_library | Breath protocol library. | sector-level | read-only library | - |
| chakra_systems | Chakra reference. | sector-level | read-only library | - |
| control_definitions | Every knob/tick the UI can render. | engine-level | read-only library | - |
| control_pack_items | Join: packs ↔ controls. | engine-level | read-only library | control_definitions, control_packs |
| control_packs | Curated bundles of controls. | engine-level | read-only library | - |
| coupling_rules | How controls influence each other. | engine-level | read-only library | control_definitions |
| cross_domain_mappings | Stores cross domain mappings records. | engine-level | read-only library | - |
| cue_triggers | Stores cue triggers records. | engine-level | execution | - |
| dashboard_blocks | Reusable UI modules (daily check-ins, packs, sections). | engine-level | read-only library | - |
| deep_work_permissions | Stores deep work permissions records. | engine-level | read-only library | - |
| default_weights | Baseline weights per profile. | engine-level | read-only library | - |
| deities_archetypes | Deity and archetype index. | sector-level | read-only library | - |
| derived_metrics | Computed scores from raw values. | engine-level | read-only library | - |
| elemental_framework | Elemental system (fire, water, earth, air, etc.). | sector-level | read-only library | - |
| evidence_sources | Stores evidence sources records. | engine-level | read-only library | - |
| experimental_flags | Stores experimental flags records. | engine-level | read-only library | - |
| knowledge_bases | Stores knowledge bases records. | engine-level | read-only library | - |
| lens_definitions | Definitions for lens definitions. | engine-level | read-only library | - |
| light_colour | Light and color modalities. | sector-level | read-only library | - |
| mappings | Automation rules (value→relation, defaults). | engine-level | read-only library | - |
| meridian_system | Meridian reference. | sector-level | read-only library | - |
| meta_lens_presets | Stores meta lens presets records. | engine-level | read-only library | - |
| movements_system | Movement practices library. | sector-level | read-only library | - |
| narration_styles | Style definitions for narration styles. | engine-level | execution | - |
| nutrition_and_food | MASTER nutrition table. | sector-level | read-only library | - |
| nutrition_intake | User nutrition logs. | sector-level | user-write | - |
| nutrition_protocols | Diet/protocol definitions. | sector-level | read-only library | - |
| organ_emotion_system | Organ-emotion mappings. | sector-level | read-only library | - |
| persona_kb_compatibility | Stores persona kb compatibility records. | engine-level | read-only library | knowledge_bases |
| persona_lens_compatibility | Stores persona lens compatibility records. | engine-level | read-only library | lens_definitions |
| profile_pack_map | Programme profiles → default packs. | engine-level | read-only library | control_packs |
| programme_knowledge_map | Stores programme knowledge map records. | engine-level | read-only library | knowledge_bases |
| programme_profiles | Preset lenses (Athlete, Trauma-Safe, Breath-Only, etc.). | engine-level | read-only library | - |
| questionnaire_questions | Questions within questionnaires. | engine-level | read-only library | questionnaires |
| questionnaire_responses | User questionnaire answers. | engine-level | user-write | questionnaires |
| questionnaires | Questionnaire definitions. | engine-level | read-only library | - |
| rules_gating | Rule engine layer (trigger/threshold, safety gating). | engine-level | read-only library | - |
| sacred_geometry | Sacred geometry forms. | sector-level | read-only library | - |
| safety_rules | Contraindications, exclusions, gating logic. | engine-level | read-only library | - |
| session_blueprints | Stores session blueprints records. | engine-level | execution | - |
| session_outputs | Session plans/scripts. | engine-level | user-write | session_runs |
| session_phases | Stores session phases records. | engine-level | execution | - |
| session_runs | Generated session instances. | engine-level | user-write | - |
| session_scope_log | Log records for session scope log. | engine-level | execution | - |
| session_templates | Declarative recipes for generating sessions. | engine-level | read-only library | - |
| session_types | High-level session categories (regulation, training, recovery). | engine-level | read-only library | - |
| sound_vibration | Sound and vibration modalities. | sector-level | read-only library | - |
| supplement_interactions | Supplement interaction rules. | sector-level | read-only library | - |
| symbols_index | Symbol reference library. | sector-level | read-only library | - |
| sync_events | Realtime sync events for Main App. | engine-level | execution | - |
| system_manifest | Tracks what exists / what is canonical / archived. | engine-level | read-only library | - |
| technique_lens_explanations | Stores technique lens explanations records. | engine-level | read-only library | lens_definitions, techniques |
| technique_steps | Stores technique steps records. | engine-level | execution | - |
| techniques | Stores techniques records. | engine-level | read-only library | - |
| timing_presets | Stores timing presets records. | engine-level | execution | - |
| transition_rules | Rules for transition rules. | engine-level | execution | - |
| user_checkins | Daily check-in entries. | engine-level | user-write | - |
| user_dashboard_layouts | User dashboard configurations. | engine-level | user-write | - |
| user_knowledge_access | User-owned data for knowledge access. | engine-level | user-write | knowledge_bases |
| user_lens_context | User-owned data for lens context. | engine-level | user-write | - |
| user_lens_preferences | User-owned data for lens preferences. | engine-level | user-write | lens_definitions |
| user_technique_blends | User-owned data for technique blends. | engine-level | user-write | - |
