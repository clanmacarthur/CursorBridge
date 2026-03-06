# Theme Table Catalog

Last updated: 2026-02-21
Status: planning map (Supabase-first)

## Purpose

This file maps Supabase tables to planned session theme domains.
It prevents guessed mappings and keeps wheel plans tied to real data.

## Current Reality

- There is no checked-in ThemeGraph code in this repo yet.
- This catalog is the contract for future implementation.

## Domain Mapping Table

| Table | Planned Domain | Primary Label Field | Secondary/Inner Fields | Edge Fields | Status |
|---|---|---|---|---|---|
| `lens_definitions` | `lens` | `lens_name` | `lens_description`, `paradigm_family`, `language_style` | `id` | planned |
| `light_colour` | `colour` | `light___colour` | `wavelength__nm_`, `circadian_influence`, `psychological_theme`, `primary_effect`, `elemental_bias` | relation text fields | planned |
| `chakra_systems` | `chakra` | `chakra` | `psychological_function`, `location__somatic_`, `primary_element`, `secondary_element` | relation text fields | planned |
| `meridian_system` | `meridian` | `meridian` | `primary_emotion`, `secondary_emotional_themes`, `five_element_phase`, `yin___yang` | relation text fields | planned |
| `organ_emotion_system` | `organ` + `emotion` | `organ___system` | `primary_emotion`, `secondary_emotion`, `stress_expression`, `nervous_system_bias` | `chakra_systems__db_`, `meridian_system__db_` | planned |
| `elemental_framework` | `element` | `element` | `core_qualities`, `emotional_tone`, `nervous_system_bias`, `physiological_correlates` | relation text fields | planned |
| `deities_archetypes` | `deity` | `name` | `primary_domain`, `secondary_domains`, `associated_colours`, `key_symbols` | relation text fields | planned |
| `symbols_index` | `symbol` | `symbol` | `symbol_class`, `meaning_domain`, `emotional_tone`, `mythology` | `sacred_geometry`, `chakra_systems__db_` | planned |
| `sacred_geometry` | `sacred_geometry` | `geometry` | `geometry_class`, `primary_function`, `psychophysiological_effect` | `symbols_index__db_` | planned |
| `sound_vibration` | `sound` | `sound___frequency` | `sound_type`, `primary_effect`, `frequency__hz_`, `nervous_system_bias` | `chakra_affinity`, `meridian_affinity` | planned |
| `movements_system` | `practice_modality` | `movement___practice` | `movement_family`, `primary_effect`, `intensity`, `nervous_system_bias` | `chakra_affinity`, `meridian_affinity`, `organ_affinity` | planned |
| `nutrition_protocols` | `nutrition` | `nutrition_protocol` | `primary_nutrition_goal`, `strictness_level`, `secondary_attribute_focus` | relation text fields | planned |
| `nutrition_and_food` | `nutrition` support | `food_type` | `primary_nutrition_domain`, `secondary_nutrition_domains`, `evidence_confidence` | `associated_diets___protocols` | planned |
| `knowledge_bases` | `knowledge_pack` | `kb_name` | `kb_description`, `cultural_origin`, `evidence_level`, `maturity_gate` | `id` | planned |
| `mappings` | edge-only | `mapping` | `mapping_type`, `from_value`, `to_value` | `from_db`, `from_field`, `to_db`, `to_field` | planned |
| `cross_domain_mappings` | edge-only | `technique_pattern` | `translation_notes`, `confidence` | `source_domain`, `target_domain` | planned |

## Build Rules For Implementation

1. Use only real tables and real fields from canon manifests.
2. No guessed edges: every edge must come from explicit relation data.
3. If a table is not wired yet, keep it marked as `planned`.
4. Keep naming stable between docs and code.

## Immediate Follow-up

1. Add a `used_in_code` column once ThemeGraph files are added.
2. Add file and line references after implementation.
3. Expand inner fields for domains with dense metadata.

