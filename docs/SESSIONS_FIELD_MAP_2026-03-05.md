# Sessions Field Map (Strict Live Values)

Generated: 2026-03-05T04:54:35.605540+00:00

## `breath_library`

- Label column: `protocol_name`
- Search columns: `protocol_name, typical_use, activation_level, safety_tier, core_breath_quality`
- Filter columns: `typical_use, activation_level, safety_tier, core_breath_quality`
- Detail columns: `protocol_name, typical_use, activation_level, safety_tier, core_breath_quality, notes`
- Hidden columns: `chakra_systems__db_, id, notion_page_id, organ___systemprimary_emotionsecondary_emotionstress_expression, primary_element, programme_profiles__db___, safety_rules, secondary_element, untitled_database`
- Snapping columns: `activation_level, typical_use, safety_tier`
- Reason for choices:
  - Label uses `protocol_name` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `movements_system`

- Label column: `movement___practice`
- Search columns: `movement___practice, movement_family, intensity, primary_effect, primary_body_region`
- Filter columns: `movement_family, intensity, primary_effect, primary_body_region`
- Detail columns: `movement___practice, movement_family, intensity, primary_effect, primary_body_region, notes`
- Hidden columns: `chakra_affinity, id, intent___condition_fit, light___colour_pairing, meridian_affinity, nadi_affinity, notion_page_id, organ_affinity, primary_element, programme_profiles__db___, recommended_persona_bias, secondary_element, sound_pairing, untitled_database`
- Snapping columns: `primary_effect, intensity, movement_family`
- Reason for choices:
  - Label uses `movement___practice` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `organ_emotion_system`

- Label column: `organ___system`
- Search columns: `organ___system, primary_emotion, stress_expression, regulation_direction`
- Filter columns: `primary_emotion, stress_expression, regulation_direction`
- Detail columns: `organ___system, primary_emotion, stress_expression, regulation_direction, contraindications___risk_notes, notes`
- Hidden columns: `breath_type, chakra_systems__db_, chakra_systems__db__1, id, intent___condition_framework__db_, intent___condition_framework__db__1, meridian_system__db_, movements_system__db_, notion_page_id, sound___vibration_system__db_, symbol, untitled_database`
- Snapping columns: `primary_emotion, regulation_direction, stress_expression`
- Reason for choices:
  - Label uses `organ___system` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `meridian_system`

- Label column: `meridian`
- Search columns: `meridian, primary_emotion, nervous_system_bias`
- Filter columns: `primary_emotion, nervous_system_bias`
- Detail columns: `meridian, primary_emotion, nervous_system_bias, physiological_emphasis, notes`
- Hidden columns: `associated_organ, five_element_phase, id, movements_system__db_, notion_page_id, sound___vibration_system__db_, untitled_database`
- Snapping columns: `primary_emotion, nervous_system_bias`
- Reason for choices:
  - Label uses `meridian` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `light_colour`

- Label column: `light___colour`
- Search columns: `light___colour, colour_family, circadian_influence, psychological_theme`
- Filter columns: `colour_family, circadian_influence, psychological_theme`
- Detail columns: `light___colour, colour_family, psychological_theme, circadian_influence, primary_effect, notes`
- Hidden columns: `archetypal_personas__db_, chakra_affinity, contraindications___safety_notes, elemental_bias, id, movements_system__db_, notion_page_id, programme_profiles__db___`
- Snapping columns: `psychological_theme, circadian_influence, colour_family`
- Reason for choices:
  - Label uses `light___colour` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `sound_vibration`

- Label column: `sound_type`
- Search columns: `sound_type, primary_effect`
- Filter columns: `primary_effect`
- Detail columns: `sound_type, sound___frequency, primary_effect, notes`
- Hidden columns: `archetypal_personas__db_, chakra_affinity, contraindications___safety_notes, elemental_bias, id, meridian_affinity, movements_system__db_, nervous_system_bias, notion_page_id, primary_organ, programme_profiles__db___, untitled_database`
- Snapping columns: `primary_effect`
- Reason for choices:
  - Label uses `sound_type` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `nutrition_and_food`

- Label column: `food_type`
- Search columns: `food_type, evidence_confidence`
- Filter columns: `evidence_confidence`
- Detail columns: `food_type, evidence_confidence, notes`
- Hidden columns: `associated_diets___protocols, id, notion_page_id, primary_nutrition_domain, relevant_supplement_interactions, secondary_nutrition_domains`
- Snapping columns: `evidence_confidence`
- Reason for choices:
  - Label uses `food_type` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `nutrition_protocols`

- Label column: `nutrition_protocol`
- Search columns: `nutrition_protocol, primary_nutrition_goal, strictness_level`
- Filter columns: `primary_nutrition_goal, strictness_level`
- Detail columns: `nutrition_protocol, primary_nutrition_goal, strictness_level, notes`
- Hidden columns: `id, included_food, notion_page_id, primary_attribute_focus, secondary_attribute_focus`
- Snapping columns: `primary_nutrition_goal, strictness_level`
- Reason for choices:
  - Label uses `nutrition_protocol` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `symbols_index`

- Label column: `symbol`
- Search columns: `symbol, symbol_class, meaning_domain, emotional_tone, cultural_scope`
- Filter columns: `symbol_class, meaning_domain, emotional_tone, cultural_scope`
- Detail columns: `symbol, symbol_class, meaning_domain, emotional_tone, cultural_scope, notes`
- Hidden columns: `archetypal_personas__db_, astrological_archetype, chakra_systems__db_, id, mythology, nadi_system__db_, notion_page_id, organ___systemprimary_emotionsecondary_emotionstress_expression, primary_element, programme_profiles__db___, sacred_animal, sacred_geometry, secondary_element, stones, untitled_database`
- Snapping columns: `meaning_domain, emotional_tone, symbol_class`
- Reason for choices:
  - Label uses `symbol` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `sacred_geometry`

- Label column: `geometry`
- Search columns: `geometry, geometry_class, psychophysiological_effect, primary_element, secondary_element`
- Filter columns: `geometry_class, psychophysiological_effect, primary_element, secondary_element`
- Detail columns: `geometry, geometry_class, psychophysiological_effect, primary_element, secondary_element, notes`
- Hidden columns: `id, notion_page_id, symbols_index__db_, untitled_database`
- Snapping columns: `psychophysiological_effect, primary_element, secondary_element`
- Reason for choices:
  - Label uses `geometry` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.

## `chakra_systems`

- Label column: `chakra`
- Search columns: `chakra, sanskrit_name, primary_element`
- Filter columns: `sanskrit_name, primary_element`
- Detail columns: `chakra, sanskrit_name, primary_element, notes`
- Hidden columns: `breath_type, id, movements_system__db_, nadi_system__db_, notion_page_id, organ_emotion, sound___vibration_system__db_, symbol, untitled_database, untitled_database_1`
- Snapping columns: `primary_element, sanskrit_name`
- Reason for choices:
  - Label uses `chakra` because it is non-empty across live rows and is the domain's primary readable name field.
  - Filters include only non-empty live columns; empty columns are hidden by rule.
  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls.
  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers.
  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings.
