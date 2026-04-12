# Botanical System Source Of Truth V2

Last updated: 2026-04-12

## Status

- This replaces the older March 30 botanical builder package where it conflicts.
- UK perennial sweep is complete for this phase.
- Brazil is the next branch build.
- The schema is branchable and global-ready. Countries are not separate schemas.

## Core Decision

- Build one botanical database system with multiple normalized tables.
- Keep one generated flat working view for builder and ops use.
- Do not use one giant table as source of truth.
- Do not split by country into separate schemas.

## Locked Two-Way Product Experience

The system must support both directions without collapsing cultivar-level truth:

- `product -> matching botanical entries / varieties / trees`
- `botanical entry / tree / variety -> valid product paths`

This behavior must be possible through the normalized product layer plus the
generated operational view. It must not rely on loose notes or one-way-only UI
assumptions.

## Row Logic

- Identity layer:
  - `1 row = 1 actual botanical entry / species / cultivar / named line`
- Operational working view:
  - `1 row = 1 botanical entry x branch x zone x production mode`

Do not collapse cultivar rows into species-only rows.

## Locked Table Stack

- `botanical_entries_master`
- `botanical_zone_profiles`
- `botanical_product_paths`
- `protocol_library`
- `branch_nodes`
- `branch_resources`
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
- generated working view:
  - `"Botanical_Operational_View"`

## Locked Capture Layer

These fields are now part of the system and must be supported in builder work:

- `perennial_main_group`
- `sweep_bucket`
- `scarcity_class`
- `conservation_relevance`
- `heritage_flag`
- `medicinal_flag`
- `ecological_value_flag`
- `perennial_rating`
- `inclusion_rationale`

## Locked Size And Tree Handling Layer

These fields are mandatory because crate logic, filtering, and design modules depend on them:

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

## Locked Reproductive Layer

These fields are required so cultivar-level reproductive behavior is queryable without relying on loose notes:

- `common_name_en`
- `self_fertile_flag`
- `pollination_requirement`
- `pollinator_type`
- `pollination_notes`

## Locked Lifecycle And Maturity Layer

These fields are required for module planning, regeneration logic, and later economic modeling:

- `plant_lifespan_years`
- `productive_lifespan_years`
- `replacement_cycle_years`

## Locked Yield And Harvest Layer

Yield and harvest must be region-aware and source-backed.

Required operational fields include:

- `branch_fit`
- `branch`
- `country`
- `region`
- `state_province`
- `zone`
- `microclimate_tags`
- `production_mode`
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
- `harvest_granularity`
- `harvest_window_brazil`
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
- `yield_output_type`
- `yield_unit`
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

Do not invent precision. If a source only gives month-level harvest timing, store month-level timing.

## Locked Root And Symbiosis Detail

Root and symbiosis handling must support crate logic, ecological logic, restoration logic, and user-end filtering.

Required root-detail fields:

- `root_depth_min_m`
- `root_depth_max_m`
- `root_architecture_type`
- `root_depth_category`
- `excavation_sensitivity`
- `root_competition_intensity`
- `container_root_behavior`

## Locked Confidence And Completeness Layer

These fields are required so the system can support validation, user-generated expansion, and agent-driven completion safely:

- `data_confidence_level`
- `data_source_type`
- `record_completeness_score`
- `fields_completed_count`
- `confidence_score`
- `confidence_notes`

## Locked Role, Propagation, And Risk Layer

These fields are required to keep filtering practical without adding more tables:

- `system_roles`
- `propagation_difficulty`
- `propagation_success_rate`
- `invasiveness_risk_level`
- `spread_control_required`

## Locked Climate Tolerance Layer

These fields are required so the same branchable schema can travel across climates without being UK- or Brazil-bound:

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

Required symbiosis fields:

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

Symbiosis is not the same as companion planting. Keep those as separate layers.

## Locked Universal Layering

The system needs one canonical universal layer model that works across ecological design, module stacking, restoration, user filtering, and branch planning.

Keep branch-specific terms where useful, but add canonical layer fields:

- `food_forest_layer`
- `canonical_layer_primary`
- `canonical_layer_secondary`
- `layer_stack_tags`

Canonical layer vocabulary:

- `canopy`
- `subcanopy`
- `shrub`
- `herbaceous`
- `groundcover`
- `climber`
- `root`
- `aquatic_marginal`
- `epiphyte`
- `fungal_layer`

Populate `food_forest_layer` as a friendly display label if useful, but do not
use it as a replacement for the canonical layer fields.

## Locked Layer Assignment And Selection Rules

- assign layer from the actual occupied mature size and growth habit of the row
  being stored
- do not assign a compact or dwarf form to a larger layer just because related
  forms in the genus can grow bigger
- smallest occupied form wins inside the layer it actually fits
- preserve real source-backed identity rows even when several share the same
  common-name cluster
- use `duplicate_name_group` and `duplicate_name_count` to track shared-name
  clusters
- duplicate caps apply to curated launch selections and shortlist outputs, not
  deletion of real identity rows
- preferred curated cap is `2` rows per shared-name cluster per canonical layer
- do not exceed `2` in the active Atlantic Forest cycle
- when same-name rows compete inside a layer, dwarf and smaller occupied forms
  win first
- after size, prefer small/common/practical rows ahead of obscure repeats
  unless conservation, heritage, or ecological value clearly overrides
- upper layers should stay tighter than lower layers

## Locked Micro-Enclosure Rule

Do not invent new canonical layers for vivariums, terraria, or small domes.

Use the existing canonical layers plus size fields and `layer_stack_tags`.

Suggested micro tags:

- `micro_mat`
- `micro_low`
- `micro_mid`
- `micro_upper`

## Hard Rules

- Restoration mode is native-first only.
- Experimental mode is contained only.
- Product logic does not live in the identity table.
- Protocol content does not live in the identity table.
- New branches must reuse the same schema.
- Product-first and botanical-first journeys must both remain possible.
- `branch_resources` is required as a branch capability layer. `branch_nodes`
  alone is not enough.

## UK Status

- UK perennial sweep is complete enough to freeze for this phase.
- Sweep fields and size fields must be preserved in the schema and app filters.

## Brazil Status

- Brazil remains the next branch build.
- Brazil must use the same schema and execution rules.
- Brazil must not restart schema design from zero.
