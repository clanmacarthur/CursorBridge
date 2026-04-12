# Botanical Database Builder Handover V2

Last updated: 2026-04-12

## Active Execution Rule

For active Brazil botanical execution, use
`docs/BOTANICAL_BRAZIL_ATLANTIC_FOREST_STAGE1_DATABASE_BUILDER_HANDOVER_2026-04-08.md`
as the sole live execution contract for this repo's botanical build work.

This file remains a frozen system-support handover for schema, table, field,
and migration compatibility requirements.

## Instruction

Implement the locked botanical system. Do not redesign the schema.

## Current Delivery Status

- Notion V2 botanical databases are already created.
- Local Supabase CLI project scaffold is initialized in `supabase/`.
- Local botanical migrations are staged and ready to push.
- Remote Supabase botanical migrations are now pushed to project
  `dshwdxhycdrtemaxrupu`.

## Required Tables

- `branch_nodes`
- `branch_resources`
- `botanical_entries_master`
- `botanical_zone_profiles`
- `botanical_product_paths`
- `protocol_library`
- `companion_guilds`
- `botanical_companion_rules`
- `species_root_profile`
- `species_symbiosis_profile`
- `species_container_profile`
- `species_social_safety_profile`
- `species_fauna_profile`
- `species_governance_profile`
- `species_substrate_profile`
- `species_design_matrix`
- `module_guild_profiles`
- `addon_library`
- `hons_overlay`

## Required Working View

- `"Botanical_Operational_View"`

## Import Rules

- `1 row = 1 actual botanical entry / cultivar / named line`
- Do not collapse cultivars into species.
- Do not drop rare, ecological, or heritage rows.
- Do not flatten products or protocols into the identity table.
- Preserve `duplicate_name_group` and `duplicate_name_count` for shared-name
  clusters.
- Shared-name caps apply to curated launch selections, not deletion of
  source-backed identity rows.

## Mandatory Capture Fields

Support these fields in the database layer:

- `perennial_main_group`
- `sweep_bucket`
- `scarcity_class`
- `conservation_relevance`
- `heritage_flag`
- `medicinal_flag`
- `ecological_value_flag`
- `perennial_rating`
- `inclusion_rationale`

## Mandatory Size Fields

Support these fields in the database layer:

- `common_name_en`
- `mature_height_m_min`
- `mature_height_m_max`
- `mature_height_m`
- `mature_spread_m_min`
- `mature_spread_m_max`
- `mature_spread_m`
- `size_class`
- `root_volume_class`
- `container_suitable`
- `pruning_response`
- `dwarf_flag`
- `grafted_flag`

Tree size filtering is required. Do not skip these because module layout, crate limits, and branch filtering depend on them.

## Mandatory Reproductive Fields

Support these fields in the identity/reproductive layer:

- `self_fertile_flag`
- `pollination_requirement`
- `pollinator_type`
- `pollination_notes`

## Mandatory Lifecycle Fields

Support these fields in the identity layer:

- `plant_lifespan_years`
- `productive_lifespan_years`
- `replacement_cycle_years`

## Mandatory Operational Fields

Support these fields in the zone/profile layer:

- `branch_fit`
- `state_province`
- `production_mode_basis`
- `local_only_flag`
- `export_mode`
- `nursery_only_flag`
- `education_only_flag`
- `current_site_live_flag`
- `spacing_in_row_m`
- `spacing_between_rows_m`
- `spacing_notes`
- `recommended_establishment_method`
- `recommended_training_method`
- `season_start_month`
- `season_end_month`
- `light_preference`
- `flood_tolerance`
- `salinity_tolerance`
- `heat_tolerance`
- `fire_tolerance`
- `harvest_window_brazil`
- `harvest_granularity`
- `harvest_window_1_start`
- `harvest_window_1_end`
- `harvest_window_1_peak_start`
- `harvest_window_1_peak_end`
- `harvest_window_2_start`
- `harvest_window_2_end`
- `harvest_window_2_peak_start`
- `harvest_window_2_peak_end`
- `harvest_passes_per_year`
- `time_to_first_harvest`
- `time_to_full_production`
- `area_harvested_ha`
- `production_qty`
- `average_yield_per_ha`
- `yield_per_plant`
- `yield_low`
- `yield_typical`
- `yield_high`
- `processing_recovery_pct`
- `production_value_brl`
- `harvest_source`
- `harvest_source_year`
- `harvest_confidence`
- `yield_source`
- `yield_source_year`
- `yield_confidence`

Preserve spacing fields per botanical row where relevant, including accepted
species, cultivars, and named lines carried through later operational mapping.

## Mandatory Confidence And Completeness Fields

Support these fields so records can be validated, ranked for completion, and expanded safely:

- `data_confidence_level`
- `data_source_type`
- `record_completeness_score`
- `fields_completed_count`
- `confidence_score`
- `confidence_notes`

## Mandatory Root Detail Fields

Support these fields in `species_root_profile`:

- `root_depth_min_m`
- `root_depth_max_m`
- `root_architecture_type`
- `root_depth_category`
- `excavation_sensitivity`
- `root_competition_intensity`
- `container_root_behavior`

## Mandatory Role, Propagation, And Risk Fields

Support these fields in the identity/design layer:

- `system_roles`
- `propagation_difficulty`
- `propagation_success_rate`
- `invasiveness_risk_level`
- `spread_control_required`

## Mandatory Climate Tolerance Fields

Support these fields in the identity/zone layer:

- `min_temp_c`
- `max_temp_c`
- `drought_tolerance`
- `frost_tolerance`
- `endemic_to_brazil`
- `conservation_flag`
- `invasive_risk_brazil`
- `source_url_primary`
- `source_url_secondary`
- `source_url_tertiary`

## Mandatory Symbiosis Fields

Create and support `species_symbiosis_profile` with:

- `symbiosis_type`
- `symbiotic_partner_type`
- `symbiotic_partner_botanical_id`
- `mycorrhizal_association_type`
- `nitrogen_fixing_flag`
- `host_dependency_flag`
- `nurse_plant_flag`
- `rhizosphere_benefit_notes`
- `symbiosis_strength`
- `symbiosis_confidence`
- `symbiotic_role_tags`

Do not conflate this table with companion planting.

## Mandatory Layer Fields

Add universal layering fields to `species_design_matrix`:

- `food_forest_layer`
- `canonical_layer_primary`
- `canonical_layer_secondary`
- `layer_stack_tags`

Keep branch/local layer wording if needed, but do not use it as the only layer system.

`food_forest_layer` may be populated as a friendly display label, but canonical
layer fields remain authoritative.

## Selection And Micro-Layer Rules

- preferred curated cap = `2` rows per shared-name cluster per canonical layer
- do not exceed `2` in the active Atlantic Forest cycle
- lower layers may carry more variety than upper layers, but canopy and tree
  selections should stay tight
- assign layer by the actual occupied size and habit of the stored row
- compact or dwarf forms may sit below larger related forms when their mature
  size and footprint justify it
- when same-name rows compete inside a layer, dwarf and smaller occupied forms
  win first
- after size, prefer small/common/practical rows ahead of obscure repeats
  unless conservation, heritage, or ecological value clearly overrides
- for vivariums, terraria, and small domes, do not add new schema layers
- use `mature_height_m_min`, `mature_height_m_max`,
  `mature_spread_m_min`, `mature_spread_m_max`, `dwarf_flag`,
  `container_suitable`, and `layer_stack_tags` to express micro builds
- suggested micro tags are `micro_mat`, `micro_low`, `micro_mid`, and
  `micro_upper`

## Mandatory Flower Product Fields

Add these fields to `botanical_product_paths`:

- `edible_flower_friendly`
- `cut_flower_friendly`
- `medicinal_flower_friendly`
- `petal_flavour_friendly`
- `dried_floral_friendly`

## Mandatory HONS Overlay Fields

Add these fields to `hons_overlay`:

- `stage_status`
- `provenance_status`
- `rights_status`
- `branch_eligibility`
- `synergy_status`
- `node_relevance`
- `experimental_policy`
- `release_policy`
- `public_publish_status`

## Required Relations

- `botanical_entries_master` -> `botanical_zone_profiles` is `1 -> many`
- `botanical_entries_master` -> `botanical_product_paths` is `1 -> many`
- `botanical_entries_master` <-> `companion_guilds` is relation-driven via companion rules
- `botanical_entries_master` -> `species_symbiosis_profile` is `1 -> many`
- `botanical_entries_master` -> species overlay tables is `1 -> many`
- `botanical_entries_master` -> `hons_overlay` is `1 -> many`
- `branch_nodes` -> `botanical_zone_profiles` is `1 -> many`

## Required Product Navigation Behavior

The built database must support both of these query directions cleanly:

- `product -> matching botanical entries / cultivars / trees`
- `botanical entry / cultivar / tree -> valid product paths`

This must be achievable through join-safe keys, not through manual note parsing.
Do not build the product layer in a way that traps it as one-way-only metadata.

## Constraints

- Restoration = native-first only.
- Experimental = contained only.
- Preserve branch parity between UK and Brazil.
- Support future branches without schema forks.

## Return Format

Return:

- `YES / PARTIAL / NO` per required table
- missing tables
- missing columns
- join keys used
- mapping issues
