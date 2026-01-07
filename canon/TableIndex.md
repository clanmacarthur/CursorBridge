# Table Index

Generated: 2026-01-04T23:38:46Z
Source: Supabase PostgREST OpenAPI (introspected)

## aggregate_patterns

Columns:
- id (bigint)
- pattern_slug (text)
- pattern_name (text)
- description (text)
- condition_cluster (text)
- effective_interventions (text)
- ineffective_interventions (text)
- sample_size (integer)
- confidence_interval (text)
- last_updated (timestamp with time zone)
- derived_from (text)
- is_verified (boolean)

Primary key: id
Foreign keys: none

## ai_confidence_levels

Columns:
- id (bigint)
- confidence_slug (text)
- confidence_name (text)
- description (text)
- evidence_basis (text)
- disclaimer_required (boolean)
- disclaimer_text (text)
- sort_order (integer)

Primary key: id
Foreign keys: none

## ai_decision_log

Columns:
- id (bigint)
- user_id (text)
- session_id (text)
- timestamp (timestamp with time zone)
- decision_type (text)
- decision_made (text)
- user_context_considered (jsonb)
- options_evaluated (jsonb)
- selection_criteria (text)
- final_reasoning (text)
- alternatives_available (jsonb)
- why_not_alternatives (text)
- user_can_query (boolean)
- explanation_given (boolean)

Primary key: id
Foreign keys: none

## ai_depth_levels

Columns:
- id (bigint)
- depth_slug (text)
- depth_name (text)
- description (text)
- example_work (text)
- requires_professional (boolean)
- requires_consent (boolean)
- safety_notes (text)
- sort_order (integer)

Primary key: id
Foreign keys: none

## ai_scope_levels

Columns:
- id (bigint)
- scope_slug (text)
- scope_name (text)
- description (text)
- example_use (text)
- risk_level (text)
- requires_consent (boolean)
- sort_order (integer)

Primary key: id
Foreign keys: none

## ai_source_levels

Columns:
- id (bigint)
- source_slug (text)
- source_name (text)
- description (text)
- privacy_level (text)
- anonymization_required (boolean)
- requires_consent (boolean)
- sort_order (integer)

Primary key: id
Foreign keys: none

## archetypal_personas

Columns:
- id (bigint)
- notion_page_id (text)
- programme_profiles__db___ (text)
- metaphor_density (text)
- preferred_styles (text)
- symbol_affinity (text)
- sound_affinity (text)
- cognitive_style (text)
- language_tone (text)
- nervous_system_bias (text)
- tradition_affinity (text)
- contraindications___risk_notes (text)
- notes (text)
- lineage___influence (text)
- safety_profile (text)
- light_colour (text)
- primary_use_context (text)
- persona (text)

Primary key: id
Foreign keys: none

## attribute_taxonomy

Columns:
- id (bigint)
- notion_page_id (text)
- untitled_database (text)
- untitled_database_1 (text)
- parent_attribute (text)
- rules___gating__db_ (text)
- dashboard_blocks__db__1 (text)
- dashboard_blocks__db_ (text)
- session_templates__db_ (text)
- attribute_role (text)
- attribute (text)
- role (text)
- parent (text)

Primary key: id
Foreign keys: none

## blueprint_cues

Columns:
- id (uuid)
- blueprint_id (uuid)
- cue_trigger_id (uuid)
- is_required (boolean)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## blueprint_steps

Columns:
- id (uuid)
- blueprint_id (uuid)
- technique_step_id (uuid)
- step_order (integer)
- override_duration_sec (integer)
- override_intensity (text)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## breath_library

Columns:
- id (bigint)
- notion_page_id (text)
- typical_use (text)
- notes (text)
- core_breath_quality (text)
- activation_level (text)
- primary_element (text)
- safety_tier (text)
- untitled_database (text)
- organ___systemprimary_emotionsecondary_emotionstress_expression (text)
- safety_rules (text)
- contraindications (text)
- programme_profiles__db___ (text)
- secondary_element (text)
- chakra_systems__db_ (text)
- protocol_name (text)

Primary key: id
Foreign keys: none

## chakra_systems

Columns:
- id (bigint)
- notion_page_id (text)
- dysregulation_signs (text)
- primary_element (text)
- movements_system__db_ (text)
- symbol (text)
- sound___vibration_system__db_ (text)
- organ_emotion (text)
- sanskrit_name (text)
- secondary_element (text)
- location__somatic_ (text)
- regulation_direction (text)
- nadi_system__db_ (text)
- contraindications___safety_notes (text)
- notes (text)
- nervous_system_bias (text)
- untitled_database_1 (text)
- physiological_correlates (text)
- untitled_database (text)
- breath_type (text)
- psychological_function (text)
- chakra (text)

Primary key: id
Foreign keys: none

## control_definitions

Columns:
- id (uuid)
- notion_page_id (text)
- control_name (text)
- control_type (text)
- primary_domain (text)
- secondary_domains (text[])
- range_min (numeric)
- range_max (numeric)
- range_step (numeric)
- default_value (numeric)
- unit (text)
- label (text)
- description (text)
- icon (text)
- color (text)
- is_required (boolean)
- is_default (boolean)
- completion_threshold (numeric)
- status (text)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## control_pack_items

Columns:
- id (uuid)
- pack_id (uuid)
- control_id (uuid)
- display_order (integer)
- override_default_value (numeric)
- override_range_min (numeric)
- override_range_max (numeric)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys:
- control_id -> control_definitions.id
- pack_id -> control_packs.id

## control_packs

Columns:
- id (uuid)
- notion_page_id (text)
- pack_name (text)
- pack_slug (text)
- description (text)
- category (text)
- difficulty (text)
- icon (text)
- color (text)
- display_order (integer)
- is_public (boolean)
- is_default (boolean)
- status (text)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## coupling_rules

Columns:
- id (uuid)
- notion_page_id (text)
- rule_name (text)
- from_control_id (uuid)
- from_attribute_id (text)
- from_metric (text)
- to_control_id (uuid)
- to_attribute_id (text)
- to_metric (text)
- function_type (text)
- direction (text)
- magnitude (numeric)
- threshold_value (numeric)
- threshold_comparator (text)
- threshold_high (numeric)
- condition_expression (text)
- applies_to_profiles (text[])
- priority (integer)
- evidence_confidence (text)
- notes (text)
- status (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys:
- from_control_id -> control_definitions.id
- to_control_id -> control_definitions.id

## cross_domain_mappings

Columns:
- id (bigint)
- source_domain (text)
- target_domain (text)
- technique_pattern (text)
- translation_notes (text)
- confidence (text)
- evidence_sources (text)
- contraindications (text)
- is_verified (boolean)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## cue_triggers

Columns:
- id (uuid)
- trigger_name (text)
- trigger_scope (text)
- interval_sec (integer)
- sound_id (uuid)
- light_colour_id (uuid)
- symbol_id (uuid)
- sacred_geometry_id (uuid)
- organ_emotion_id (uuid)
- meridian_id (uuid)
- chakra_id (uuid)
- narration_text (text)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## dashboard_blocks

Columns:
- id (bigint)
- notion_page_id (text)
- covers_attributes (text)
- linked_system (text)
- default_depth (text)
- rules_applied (text)
- linked_programme_profile_2 (text)
- required_attributes (text)
- max_depth (text)
- settings (text)
- type (text)
- secondary_attribute_focus (text)
- display_depth (text)
- linked_programme_profile (text)
- primary_attribute_focus (text)
- default_strictness (text)
- column (text)
- default_frequency (text)
- block_type (text)

Primary key: id
Foreign keys: none

## deep_work_permissions

Columns:
- id (bigint)
- user_id (text)
- pattern_work_enabled (boolean)
- structural_work_enabled (boolean)
- identity_work_enabled (boolean)
- foundational_work_enabled (boolean)
- wide_scope_enabled (boolean)
- universal_scope_enabled (boolean)
- experimental_enabled (boolean)
- aggregate_insights_enabled (boolean)
- collective_wisdom_enabled (boolean)
- contribute_to_research (boolean)
- professional_support_confirmed (boolean)
- buddy_system_enabled (boolean)
- emergency_contact_set (boolean)
- consent_given_at (timestamp with time zone)
- consent_reviewed_at (timestamp with time zone)
- consent_version (text)

Primary key: id
Foreign keys: none

## default_weights

Columns:
- id (uuid)
- notion_page_id (text)
- programme_profile_id (text)
- attribute_id (text)
- weight (numeric)
- weight_label (text)
- domain (text)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## deities_archetypes

Columns:
- id (bigint)
- notion_page_id (text)
- primary_domain (text)
- type (text)
- associated_colours (text)
- sacred_geometry (text)
- sound_mantra_seed (text)
- culture_lineage (text)
- notes (text)
- key_symbols (text)
- secondary_domains (text)
- risk_tag (text)
- untitled_database (text)
- name (text)

Primary key: id
Foreign keys: none

## derived_metrics

Columns:
- id (uuid)
- notion_page_id (text)
- metric_name (text)
- metric_slug (text)
- description (text)
- formula_type (text)
- formula_expression (text)
- input_control_ids (uuid[])
- input_weights (jsonb)
- output_min (numeric)
- output_max (numeric)
- unit (text)
- threshold_low (numeric)
- threshold_medium (numeric)
- threshold_high (numeric)
- domain (text)
- notes (text)
- status (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## elemental_framework

Columns:
- id (bigint)
- notion_page_id (text)
- notes (text)
- risk_profile (text)
- core_qualities (text)
- emotional_tone (text)
- alternate_names___systems (text)
- physiological_correlates (text)
- nervous_system_bias (text)
- typical_functions (text)
- element (text)

Primary key: id
Foreign keys: none

## evidence_sources

Columns:
- id (bigint)
- notion_page_id (text)
- evidence_source (text)
- evidence_type (text)
- primary_domain (text)
- secondary_domains (text)
- applies_to_techniques (text)
- applies_to_protocols (text)
- applies_to_supplement_interactions (text)
- lens_tags (text)
- citation_apa_short (text)
- doi_url (text)
- year (integer)
- author_organisation (text)
- key_claims_summary (text)
- evidence_confidence (text)
- review_state (text)
- verified_by (text)
- verification_notes (text)
- last_reviewed_date (date)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## experimental_flags

Columns:
- id (bigint)
- content_type (text)
- content_id (text)
- flag_type (text)
- testing_phase (text)
- user_count (integer)
- positive_reports (integer)
- negative_reports (integer)
- neutral_reports (integer)
- disclaimer_text (text)
- contraindication_warning (text)
- professional_consult_recommended (boolean)
- created_at (timestamp with time zone)
- promoted_to_established_at (timestamp with time zone)
- deprecated_at (timestamp with time zone)
- deprecation_reason (text)

Primary key: id
Foreign keys: none

## knowledge_bases

Columns:
- id (bigint)
- kb_slug (text)
- kb_name (text)
- kb_description (text)
- kb_type (text)
- paradigm_family (text)
- cultural_origin (text)
- era (text)
- is_system (boolean)
- is_public (boolean)
- requires_training (boolean)
- maturity_gate (text)
- primary_topics (text)
- language_register (text)
- evidence_level (text)
- contraindication_tags (text)
- requires_disclaimer (boolean)
- disclaimer_text (text)
- icon (text)
- sort_order (integer)
- is_active (boolean)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## lens_definitions

Columns:
- id (bigint)
- lens_slug (text)
- lens_name (text)
- lens_description (text)
- paradigm_family (text)
- language_style (text)
- cultural_origin (text)
- is_system (boolean)
- is_active (boolean)
- created_by (text)
- icon (text)
- color (text)
- sort_order (integer)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## light_colour

Columns:
- id (bigint)
- notion_page_id (text)
- contraindications___safety_notes (text)
- primary_effect (text)
- programme_profiles__db___ (text)
- notes (text)
- colour_family (text)
- archetypal_personas__db_ (text)
- elemental_bias (text)
- chakra_affinity (text)
- movements_system__db_ (text)
- light___colour (text)
- psychological_theme (text)
- wavelength__nm_ (text)
- circadian_influence (text)

Primary key: id
Foreign keys: none

## mappings

Columns:
- id (bigint)
- notion_page_id (text)
- direction (text)
- mapping_type (text)
- from_value (text)
- to_db (text)
- from_db (text)
- notes (text)
- to_value (text)
- mapping (text)
- to_field (text)
- from_field (text)

Primary key: id
Foreign keys: none

## meridian_system

Columns:
- id (bigint)
- notion_page_id (text)
- regulation_direction (text)
- movements_system__db_ (text)
- secondary_emotional_themes (text)
- associated_organ (text)
- somatic_pathway (text)
- notes (text)
- primary_emotion (text)
- yin___yang (text)
- sound___vibration_system__db_ (text)
- five_element_phase (text)
- nervous_system_bias (text)
- untitled_database (text)
- contraindications___safety_notes (text)
- physiological_emphasis (text)
- meridian (text)

Primary key: id
Foreign keys: none

## meta_lens_presets

Columns:
- id (bigint)
- preset_slug (text)
- preset_name (text)
- description (text)
- default_scope (text)
- default_depth (text)
- default_source (text)
- default_confidence (text)
- preferred_lenses (text)
- preferred_personas (text)
- preferred_knowledge_bases (text)
- best_for (text)
- not_for (text)
- icon (text)
- sort_order (integer)

Primary key: id
Foreign keys: none

## movements_system

Columns:
- id (bigint)
- notion_page_id (text)
- sound_pairing (text)
- contraindications___safety_notes (text)
- nadi_affinity (text)
- primary_body_region (text)
- tradition___lineage (text)
- programme_profiles__db___ (text)
- primary_effect (text)
- secondary_element (text)
- organ_affinity (text)
- nervous_system_bias (text)
- untitled_database (text)
- movement_family (text)
- notes (text)
- recommended_persona_bias (text)
- meridian_affinity (text)
- light___colour_pairing (text)
- intensity (text)
- primary_element (text)
- intent___condition_fit (text)
- chakra_affinity (text)
- movement___practice (text)

Primary key: id
Foreign keys: none

## narration_styles

Columns:
- id (uuid)
- style_name (text)
- voice_tone (text)
- reading_pace_wpm (integer)
- breath_verbosity (text)
- physiology_level (text)
- tcm_level (text)
- pause_between_sentences_sec (numeric)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## nutrition_and_food

Columns:
- id (bigint)
- notion_page_id (text)
- type (text)
- settings___relation (text)
- column_name (text)
- food_type (text)
- primary_nutrition_domain (text)
- associated_diets___protocols (text)
- evidence_confidence (text)
- secondary_nutrition_domains (text)
- notes (text)
- feeds_intake_items (text)
- relevant_supplement_interactions (text)

Primary key: id
Foreign keys: none

## nutrition_intake

Columns:
- id (bigint)
- notion_page_id (text)
- notes (text)
- type (text)
- completion_type (text)
- linked_supplement (text)
- dashboard_blocks__db_ (text)
- linked_nutrition_metric (text)
- intake_item (text)

Primary key: id
Foreign keys: none

## nutrition_protocols

Columns:
- id (bigint)
- notion_page_id (text)
- strictness_level (text)
- secondary_attribute_focus (text)
- notes (text)
- included_food (text)
- primary_nutrition_goal (text)
- primary_attribute_focus (text)
- nutrition_protocol (text)

Primary key: id
Foreign keys: none

## organ_emotion_system

Columns:
- id (bigint)
- notion_page_id (text)
- secondary_element (text)
- regulation_direction (text)
- intent___condition_framework__db_ (text)
- chakra_systems__db__1 (text)
- nervous_system_bias (text)
- notes (text)
- meridian_system__db_ (text)
- breath_type (text)
- intent___condition_framework__db__1 (text)
- primary_emotion (text)
- movements_system__db_ (text)
- contraindications___risk_notes (text)
- secondary_emotion (text)
- somatic_manifestation (text)
- stress_expression (text)
- primary_element (text)
- chakra_systems__db_ (text)
- sound___vibration_system__db_ (text)
- untitled_database (text)
- symbol (text)
- organ___system (text)

Primary key: id
Foreign keys: none

## persona_kb_compatibility

Columns:
- id (bigint)
- persona_id (bigint)
- kb_id (bigint)
- compatibility_score (integer)
- notes (text)

Primary key: id
Foreign keys:
- kb_id -> knowledge_bases.id

## persona_lens_compatibility

Columns:
- id (bigint)
- persona_id (bigint)
- lens_id (bigint)
- compatibility_score (integer)
- notes (text)

Primary key: id
Foreign keys:
- lens_id -> lens_definitions.id

## profile_pack_map

Columns:
- id (uuid)
- notion_page_id (text)
- programme_profile_id (text)
- pack_id (uuid)
- display_order (integer)
- is_required (boolean)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys:
- pack_id -> control_packs.id

## programme_knowledge_map

Columns:
- id (bigint)
- programme_profile_id (text)
- kb_id (bigint)
- is_required (boolean)
- is_default (boolean)
- weight (integer)

Primary key: id
Foreign keys:
- kb_id -> knowledge_bases.id

## programme_profiles

Columns:
- id (bigint)
- notion_page_id (text)
- session_templates__db____relation___session_templates__db___if_ (text)
- default_strictness___select (text)
- primary_doctrine___select (text)
- enabled_blocks___relation___dashboard_blocks__db_ (text)
- secondary_attribute_focus___relation___attribute_taxonomy__db_ (text)
- dashboard_blocks__db____relation___dashboard_blocks__db___if_pr (text)
- default_depth___select (text)
- notes___text (text)
- primary_attribute_focus___relation___attribute_taxonomy__db_ (text)
- programme_profile___title (text)

Primary key: id
Foreign keys: none

## questionnaire_questions

Columns:
- id (uuid)
- notion_page_id (text)
- questionnaire_id (uuid)
- question_text (text)
- question_type (text)
- options (jsonb)
- scale_min (integer)
- scale_max (integer)
- scale_labels (jsonb)
- weight (numeric)
- scoring_map (jsonb)
- display_order (integer)
- is_required (boolean)
- conditional_on (jsonb)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys:
- questionnaire_id -> questionnaires.id

## questionnaire_responses

Columns:
- id (uuid)
- user_id (uuid)
- questionnaire_id (uuid)
- answers (jsonb)
- assigned_profile_id (text)
- computed_weights (jsonb)
- safety_flags (text[])
- completed_at (timestamp with time zone)
- version (integer)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys:
- questionnaire_id -> questionnaires.id

## questionnaires

Columns:
- id (uuid)
- notion_page_id (text)
- questionnaire_name (text)
- questionnaire_slug (text)
- description (text)
- version (integer)
- is_active (boolean)
- is_onboarding (boolean)
- scoring_method (text)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## rules_gating

Columns:
- id (bigint)
- notion_page_id (text)
- dashboard_blocks__db_ (text)
- breath_library__db_ (text)
- blocked_elements (text)
- programme_profiles__db___ (text)
- settings (text)
- threshold_parametre (text)
- required_persona_bias (text)
- allowed_breath_protocols (text)
- type (text)
- column_name (text)
- rule_type (text)
- applies_to (text)
- relates_to (text)
- max_level (text)
- operator (text)
- threshold_parameter (text)
- threshold_value (text)
- limit (text)
- two_way (text)
- min_level (text)
- action (text)
- trigger_attribute (text)
- priority (text)

Primary key: id
Foreign keys: none

## sacred_geometry

Columns:
- id (bigint)
- notion_page_id (text)
- secondary_element (text)
- notes (text)
- symbols_index__db_ (text)
- psychophysiological_effect (text)
- untitled_database (text)
- primary_element (text)
- cultural_lineage (text)
- risk___contraindications (text)
- dimensional_emphasis (text)
- primary_function (text)
- geometry_class (text)
- geometry (text)

Primary key: id
Foreign keys: none

## safety_rules

Columns:
- id (bigint)
- notion_page_id (text)
- description (text)
- applies_to (text)
- severity (text)
- untitled_database (text)
- rule_name (text)

Primary key: id
Foreign keys: none

## session_blueprints

Columns:
- id (uuid)
- blueprint_name (text)
- description (text)
- programme_profile_id (uuid)
- persona_id (uuid)
- lens_preset_id (uuid)
- timing_preset_id (uuid)
- narration_style_id (uuid)
- safety_level (text)
- is_platform_example (boolean)
- is_published (boolean)
- sort_order (integer)
- tags (text[])
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## session_outputs

Columns:
- id (uuid)
- session_run_id (uuid)
- output_type (text)
- output_data (jsonb)
- version (integer)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys:
- session_run_id -> session_runs.id

## session_phases

Columns:
- id (uuid)
- phase_name (text)
- phase_type (text)
- default_intensity (text)
- default_min_duration_sec (integer)
- default_max_duration_sec (integer)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## session_runs

Columns:
- id (uuid)
- user_id (uuid)
- session_template_id (text)
- duration_minutes (integer)
- strictness (text)
- persona_id (text)
- safety_rules_applied (text[])
- safety_warnings (text[])
- status (text)
- started_at (timestamp with time zone)
- completed_at (timestamp with time zone)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## session_scope_log

Columns:
- id (bigint)
- session_id (text)
- user_id (text)
- timestamp (timestamp with time zone)
- scope_used (text)
- depth_used (text)
- source_used (text)
- confidence_used (text)
- scope_reasoning (text)
- depth_reasoning (text)
- why_this_combination (text)
- user_state_snapshot (jsonb)
- resistance_detected (text)
- alternative_paths_considered (text)
- experimental_flag (boolean)
- disclaimer_shown (boolean)
- user_consent_obtained (boolean)

Primary key: id
Foreign keys: none

## session_templates

Columns:
- id (bigint)
- notion_page_id (text)
- settings (text)
- type (text)
- column_name (text)
- secondary_intents____nl_ (text)
- primary_intent____l1_ (text)
- pause_style (text)
- session_type____l1_ (text)
- style____nl_ (text)
- movements____nl_ (text)
- default_duration__min_ (text)
- notes (text)
- safety_rules____nl_ (text)
- breath_protocols____nl_ (text)
- script_strictness (text)

Primary key: id
Foreign keys: none

## session_types

Columns:
- id (bigint)
- notion_page_id (text)
- untitled_database (text)
- allows_activation (text)
- max_intensity (text)
- relevant_emotions (text)
- allowed_styles (text)
- notes (text)
- session_type (text)

Primary key: id
Foreign keys: none

## sound_vibration

Columns:
- id (bigint)
- notion_page_id (text)
- frequency__hz_ (text)
- programme_profiles__db___ (text)
- elemental_bias (text)
- meridian_affinity (text)
- archetypal_personas__db_ (text)
- movements_system__db_ (text)
- sound_type (text)
- untitled_database (text)
- nervous_system_bias (text)
- primary_organ (text)
- notes (text)
- chakra_affinity (text)
- contraindications___safety_notes (text)
- primary_effect (text)
- sound___frequency (text)

Primary key: id
Foreign keys: none

## supplement_interactions

Columns:
- id (bigint)
- notion_page_id (text)
- type (text)
- settings (text)
- nutrition_intake__db_ (text)
- evidence_note (text)
- column (text)
- b_supplement (text)
- do_not (text)
- a_supplement (text)
- do (text)
- interaction_type (text)
- strength (text)
- safety_flag (text)
- mechanism__short_ (text)

Primary key: id
Foreign keys: none

## symbols_index

Columns:
- id (bigint)
- notion_page_id (text)
- cultural_scope (text)
- organ___systemprimary_emotionsecondary_emotionstress_expression (text)
- sacred_geometry (text)
- secondary_element (text)
- untitled_database (text)
- programme_profiles__db___ (text)
- primary_element (text)
- archetypal_personas__db_ (text)
- meaning_domain (text)
- stones (text)
- emotional_tone (text)
- mythology (text)
- symbol_class (text)
- nadi_system__db_ (text)
- chakra_systems__db_ (text)
- astrological_archetype (text)
- sacred_animal (text)
- symbol (text)
- notes (text)

Primary key: id
Foreign keys: none

## sync_events

Columns:
- id (uuid)
- event_type (text)
- table_name (text)
- record_id (text)
- payload (jsonb)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## system_manifest

Columns:
- id (bigint)
- notion_page_id (text)
- export_order (text)
- status (text)
- primary_key (text)
- canonical_name_confirmed (text)
- purpose (text)
- notes (text)
- depends_on (text)
- database (text)

Primary key: id
Foreign keys: none

## technique_lens_explanations

Columns:
- id (bigint)
- technique_id (bigint)
- lens_id (bigint)
- explanation_template (text)
- mechanism_notes (text)
- cue_language (text)
- safety_framing (text)
- is_verified (boolean)
- verified_by (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys:
- lens_id -> lens_definitions.id
- technique_id -> techniques.id

## technique_steps

Columns:
- id (uuid)
- step_name (text)
- technique_id (uuid)
- phase_id (uuid)
- step_order (integer)
- min_duration_sec (integer)
- max_duration_sec (integer)
- intensity_target (text)
- transition_rule_id (uuid)
- instructions_template (text)
- safety_notes (text)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## techniques

Columns:
- id (bigint)
- notion_page_id (text)
- technique (text)
- technique_category (text)
- objective (text)
- primary_intent (text)
- secondary_intents (text)
- lens_availability (text)
- lens_explanation_western (text)
- lens_explanation_tcm (text)
- mechanism_notes_simple (text)
- contraindications_summary (text)
- required_inputs (text)
- default_duration_min (integer)
- intensity_band (text)
- session_compatibility (text)
- evidence_sources (text)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## timing_presets

Columns:
- id (uuid)
- preset_name (text)
- total_duration_min (integer)
- intro_pct (integer)
- technique_pct (integer)
- integration_pct (integer)
- outro_pct (integer)
- default_pause_sec (integer)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## transition_rules

Columns:
- id (uuid)
- rule_name (text)
- transition_type (text)
- pause_duration_sec (integer)
- audio_cue (text)
- narration_template (text)
- notes (text)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## user_checkins

Columns:
- id (uuid)
- user_id (uuid)
- checkin_date (date)
- control_values (jsonb)
- derived_scores (jsonb)
- total_controls (integer)
- completed_controls (integer)
- completion_percentage (numeric)
- notes (text)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## user_dashboard_layouts

Columns:
- id (uuid)
- user_id (uuid)
- layout_name (text)
- layout_slug (text)
- is_default (boolean)
- layout_config (jsonb)
- weight_overrides (jsonb)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none

## user_knowledge_access

Columns:
- id (bigint)
- user_id (text)
- kb_id (bigint)
- access_level (text)
- granted_at (timestamp with time zone)
- granted_by (text)
- notes (text)

Primary key: id
Foreign keys:
- kb_id -> knowledge_bases.id

## user_lens_context

Columns:
- id (bigint)
- user_id (text)
- context_date (date)
- mood_state (text)
- energy_level (integer)
- receptivity (text)
- recent_lenses_used (text)
- ai_suggested_lens (text)
- ai_reasoning (text)
- override_lens (text)
- created_at (timestamp with time zone)
- suggested_persona (text)
- suggested_kb (text)
- persona_reasoning (text)
- kb_reasoning (text)

Primary key: id
Foreign keys: none

## user_lens_preferences

Columns:
- id (bigint)
- user_id (text)
- lens_id (bigint)
- preference_level (integer)
- is_enabled (boolean)
- last_used_at (timestamp with time zone)
- use_count (integer)
- created_at (timestamp with time zone)

Primary key: id
Foreign keys:
- lens_id -> lens_definitions.id

## user_technique_blends

Columns:
- id (bigint)
- user_id (text)
- blend_name (text)
- description (text)
- base_technique_ids (text)
- modifications (jsonb)
- user_objectives (text)
- personal_cues (text)
- times_used (integer)
- effectiveness_rating (integer)
- notes (text)
- is_private (boolean)
- share_anonymously (boolean)
- created_at (timestamp with time zone)
- updated_at (timestamp with time zone)

Primary key: id
Foreign keys: none
