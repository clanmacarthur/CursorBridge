# Data Model Overview

Last updated: 2026-02-22
Status: first-pass map

## Goal

List all important tables in plain language, grouped by purpose, so we can finish Supabase coverage in a clear order.

Primary source files:

- `canon/TableIndex.md`
- `canon/SystemManifest.md`
- `canon/RelationsManifest.md`

## Category 1: Theme and Session Ontology (Priority)

These tables shape session meaning and planned wheel domains.

- `lens_definitions`
- `light_colour`
- `chakra_systems`
- `meridian_system`
- `organ_emotion_system`
- `elemental_framework`
- `deities_archetypes`
- `symbols_index`
- `sacred_geometry`
- `sound_vibration`
- `movements_system`
- `nutrition_protocols`
- `nutrition_and_food`
- `knowledge_bases`
- `mappings`
- `cross_domain_mappings`

## Category 2: Session Runtime and Execution

These tables run session generation and storage.

- `session_blueprints`
- `blueprint_steps`
- `blueprint_cues`
- `technique_steps`
- `techniques`
- `timing_presets`
- `transition_rules`
- `narration_styles`
- `cue_triggers`
- `session_phases`
- `session_runs`
- `session_outputs`
- `session_templates`
- `session_types`

## Category 3: Engine and Control System

These tables power controls, packs, rules, and scoring.

- `control_definitions`
- `control_packs`
- `control_pack_items`
- `coupling_rules`
- `derived_metrics`
- `default_weights`
- `profile_pack_map`
- `programme_profiles`
- `programme_knowledge_map`
- `rules_gating`
- `safety_rules`
- `attribute_taxonomy`
- `dashboard_blocks`
- `questionnaires`
- `questionnaire_questions`

## Category 4: User and Runtime Data

These tables store user activity and preferences.

- `questionnaire_responses`
- `user_checkins`
- `user_dashboard_layouts`
- `user_lens_preferences`
- `user_lens_context`
- `user_knowledge_access`
- `user_technique_blends`
- `deep_work_permissions`
- `ai_decision_log`
- `session_scope_log`

## Category 5: Support, Evidence, and Infrastructure

These tables support references, monitoring, and sync.

- `evidence_sources`
- `experimental_flags`
- `supplement_interactions`
- `breath_library`
- `archetypal_personas`
- `persona_lens_compatibility`
- `persona_kb_compatibility`
- `aggregate_patterns`
- `sync_events`
- `system_manifest`
- `meta_lens_presets`
- `ai_scope_levels`
- `ai_depth_levels`
- `ai_source_levels`
- `ai_confidence_levels`
- `technique_lens_explanations`

## Category 6: ISU and Shared Token Infrastructure (Planned)

These are planned tables for the Sustainable Utilities Institute (ISU) model.
They are architecture planning only right now, not active session runtime tables.

- `isu_projects`
- `isu_token_classes`
- `isu_funding_allocations`
- `isu_recoup_rules`
- `isu_governance_votes`
- `isu_agreements`

Planned links to existing core tables:

- `isu_projects.sector_attribute_id -> attribute_taxonomy.id`
- `isu_projects.owner_profile_id -> programme_profiles.id`
- `isu_agreements.rule_id -> rules_gating.id`

## Coverage Status (Today)

- ThemeGraph and sessions route work is now present in `main-app-starter` on `/sessions`, alongside `/session`.
- Canon manifests: present and usable as source of truth.
- ISU architecture is now mapped as planned-only (P4), so it does not block sessions-first delivery.

## Next Pass Checklist

1. Add one row per table with:
   - category
   - main label field
   - key relation fields
   - used now (yes/no)
2. Link every ontology table to:
   - a domain ring, or
   - inner attributes, or
   - edge-only mapping
3. Mark any table as "not wired yet" if not used.
4. Keep ISU tables in planning status until sessions Supabase parity is complete.
