CREATE TABLE IF NOT EXISTS branch_resources (
  branch_resource_id TEXT PRIMARY KEY,
  branch_id TEXT NOT NULL REFERENCES branch_nodes(branch_id) ON DELETE CASCADE,
  capability_type TEXT NOT NULL,
  capability_name TEXT NOT NULL,
  status TEXT,
  machinery TEXT,
  fabrication TEXT,
  orchard TEXT,
  greenhouse TEXT,
  substrate_materials TEXT,
  pond_life_materials TEXT,
  soil_amendments TEXT,
  staffing_or_skill TEXT,
  notes TEXT,
  source TEXT,
  confidence TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS common_name_en TEXT;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS mature_height_m_min NUMERIC;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS mature_height_m_max NUMERIC;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS mature_spread_m_min NUMERIC;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS mature_spread_m_max NUMERIC;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS endemic_to_brazil BOOLEAN;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS conservation_flag TEXT;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS invasive_risk_brazil TEXT;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS source_url_primary TEXT;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS source_url_secondary TEXT;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS source_url_tertiary TEXT;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS confidence_score NUMERIC;
ALTER TABLE botanical_entries_master ADD COLUMN IF NOT EXISTS confidence_notes TEXT;

ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS light_preference TEXT;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS flood_tolerance TEXT;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS salinity_tolerance TEXT;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS heat_tolerance TEXT;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS fire_tolerance TEXT;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS harvest_window_brazil TEXT;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS local_only_flag BOOLEAN;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS export_mode TEXT;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS nursery_only_flag BOOLEAN;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS education_only_flag BOOLEAN;
ALTER TABLE botanical_zone_profiles ADD COLUMN IF NOT EXISTS current_site_live_flag BOOLEAN;

ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS stage_status TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS provenance_status TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS rights_status TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS branch_eligibility TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS synergy_status TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS node_relevance TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS experimental_policy TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS release_policy TEXT;
ALTER TABLE hons_overlay ADD COLUMN IF NOT EXISTS public_publish_status TEXT;

DROP VIEW IF EXISTS "Botanical_Operational_View";

CREATE OR REPLACE VIEW "Botanical_Operational_View" AS
SELECT
  bem.botanical_entry_id AS "Botanical Entry ID",
  bem.common_name_pt AS "Common Name (PT)",
  COALESCE(bem.common_name_en, bem.botanical_name) AS "Common Name (EN)",
  bem.alternative_names AS "Alternative Names",
  bem.scientific_name AS "Scientific Name",
  bem.variety_cultivar AS "Variety / Cultivar",
  COALESCE(bem.plant_type, bem.form_in_system) AS "Plant Type",
  bem.perennial_main_group AS "Perennial_Main_Group",
  bem.sweep_bucket AS "Sweep_Bucket",
  bem.scarcity_class AS "Scarcity_Class",
  bem.conservation_relevance AS "Conservation_Relevance",
  bem.heritage_flag AS "Heritage_Flag",
  bem.medicinal_flag AS "Medicinal_Flag",
  bem.ecological_value_flag AS "Ecological_Value_Flag",
  bem.perennial_rating AS "Perennial_Rating",
  bem.inclusion_rationale AS "Inclusion_Rationale",
  bem.mature_height_m_min AS "Mature_Height_m_Min",
  bem.mature_height_m_max AS "Mature_Height_m_Max",
  bem.mature_height_m AS "Mature_Height_m",
  bem.mature_spread_m_min AS "Mature_Spread_m_Min",
  bem.mature_spread_m_max AS "Mature_Spread_m_Max",
  bem.mature_spread_m AS "Mature_Spread_m",
  bem.size_class AS "Size_Class",
  bem.root_volume_class AS "Root_Volume_Class",
  bem.container_suitable AS "Container_Suitable",
  bem.pruning_response AS "Pruning_Response",
  bem.dwarf_flag AS "Dwarf_Flag",
  bem.grafted_flag AS "Grafted_Flag",
  bem.self_fertile_flag AS "Self_Fertile_Flag",
  bem.pollination_requirement AS "Pollination Requirement",
  bem.pollinator_type AS "Pollinator Type",
  bem.pollination_notes AS "Pollination Notes",
  bem.plant_lifespan_years AS "Plant Lifespan Years",
  bem.productive_lifespan_years AS "Productive Lifespan Years",
  bem.replacement_cycle_years AS "Replacement Cycle Years",
  bem.data_confidence_level AS "Data Confidence Level",
  bem.data_source_type AS "Data Source Type",
  bem.record_completeness_score AS "Record Completeness Score",
  bem.fields_completed_count AS "Fields Completed Count",
  bem.system_roles AS "System Roles",
  bem.propagation_difficulty AS "Propagation Difficulty",
  bem.propagation_success_rate AS "Propagation Success Rate",
  bem.invasiveness_risk_level AS "Invasiveness Risk Level",
  bem.spread_control_required AS "Spread Control Required",
  bem.min_temp_c AS "Min Temp C",
  bem.max_temp_c AS "Max Temp C",
  bem.drought_tolerance AS "Drought Tolerance",
  bem.frost_tolerance AS "Frost Tolerance",
  bem.endemic_to_brazil AS "Endemic To Brazil",
  bem.conservation_flag AS "Conservation Flag",
  bem.invasive_risk_brazil AS "Invasive Risk Brazil",
  bem.source_url_primary AS "Source URL Primary",
  bem.source_url_secondary AS "Source URL Secondary",
  bem.source_url_tertiary AS "Source URL Tertiary",
  bem.confidence_score AS "Confidence Score",
  bem.confidence_notes AS "Confidence Notes",
  bn.branch_name AS "Branch",
  bn.branch_scope_type AS "Branch Scope Type",
  bzp.branch_fit AS "Branch_Fit",
  bzp.country AS "Country",
  bzp.region AS "Region",
  bzp.state_province AS "State / Province",
  bzp.zone AS "Zone",
  bzp.microclimate_tags AS "Microclimate Tags",
  bzp.production_mode AS "Production Mode",
  bzp.production_mode_basis AS "Production Mode Basis",
  bzp.local_only_flag AS "Local Only Flag",
  bzp.export_mode AS "Export Mode",
  bzp.nursery_only_flag AS "Nursery Only Flag",
  bzp.education_only_flag AS "Education Only Flag",
  bzp.current_site_live_flag AS "Current Site Live Flag",
  bzp.spacing_in_row_m AS "Spacing In Row M",
  bzp.spacing_between_rows_m AS "Spacing Between Rows M",
  bzp.spacing_notes AS "Spacing Notes",
  bzp.recommended_establishment_method AS "Recommended Establishment Method",
  bzp.recommended_training_method AS "Recommended Training Method",
  bzp.season_start_month AS "Season Start Month",
  bzp.season_end_month AS "Season End Month",
  bzp.light_preference AS "Light Preference",
  bzp.flood_tolerance AS "Flood Tolerance",
  bzp.salinity_tolerance AS "Salinity Tolerance",
  bzp.heat_tolerance AS "Heat Tolerance",
  bzp.fire_tolerance AS "Fire Tolerance",
  bzp.harvest_window_brazil AS "Harvest Window Brazil",
  bem.kombucha_1f_friendly_flag AS "Kombucha_1F_Friendly",
  bem.tea_friendly_flag AS "Tea Friendly",
  bem.bitters_friendly_flag AS "Bitters Friendly",
  bem.cordial_friendly_flag AS "Cordial Friendly",
  bem.fresh_produce_friendly_flag AS "Fresh Produce Friendly",
  bem.preserve_friendly_flag AS "Preserve Friendly",
  bem.cosmetic_friendly_flag AS "Cosmetic Friendly",
  bzp.harvest_granularity AS "Harvest Granularity",
  bzp.harvest_window_1_start AS "Harvest Window 1 Start",
  bzp.harvest_window_1_end AS "Harvest Window 1 End",
  bzp.harvest_window_1_peak_start AS "Harvest Window 1 Peak Start",
  bzp.harvest_window_1_peak_end AS "Harvest Window 1 Peak End",
  bzp.harvest_window_2_start AS "Harvest Window 2 Start",
  bzp.harvest_window_2_end AS "Harvest Window 2 End",
  bzp.harvest_window_2_peak_start AS "Harvest Window 2 Peak Start",
  bzp.harvest_window_2_peak_end AS "Harvest Window 2 Peak End",
  bzp.harvest_passes_per_year AS "Harvest Passes Per Year",
  bzp.time_to_first_harvest AS "Time To First Harvest",
  bzp.time_to_full_production AS "Time To Full Production",
  bzp.harvest_window AS "Harvest Window",
  bzp.planting_sowing_window AS "Planting / Sowing Window",
  bzp.yield_regrowth AS "Yield & Regrowth",
  bzp.yield_output_type AS "Yield Output Type",
  bzp.yield_unit AS "Yield Unit",
  bzp.area_harvested_ha AS "Area Harvested Ha",
  bzp.production_qty AS "Production Qty",
  bzp.average_yield_per_ha AS "Average Yield Per Ha",
  bzp.yield_per_plant AS "Yield Per Plant",
  bzp.yield_low AS "Yield Low",
  bzp.yield_typical AS "Yield Typical",
  bzp.yield_high AS "Yield High",
  bzp.processing_recovery_pct AS "Processing Recovery Pct",
  bzp.production_value_brl AS "Production Value BRL",
  bzp.harvest_source AS "Harvest Source",
  bzp.harvest_source_year AS "Harvest Source Year",
  bzp.harvest_confidence AS "Harvest Confidence",
  bzp.yield_source AS "Yield Source",
  bzp.yield_source_year AS "Yield Source Year",
  bzp.yield_confidence AS "Yield Confidence",
  bzp.propagation_methods AS "Propagation Methods",
  bzp.conservation_status AS "Conservation Status",
  bzp.wildlife_supported AS "Wildlife Supported",
  ho.stage_status AS "Stage Status",
  ho.provenance_status AS "Provenance Status",
  ho.rights_status AS "Rights Status",
  ho.branch_eligibility AS "Branch Eligibility",
  ho.synergy_status AS "Synergy Status",
  ho.node_relevance AS "Node Relevance",
  ho.experimental_policy AS "Experimental Policy",
  ho.release_policy AS "Release Policy",
  ho.public_publish_status AS "Public Publish Status",
  bzp.notes AS "Notes"
FROM botanical_entries_master bem
LEFT JOIN botanical_zone_profiles bzp
  ON bzp.botanical_entry_id = bem.botanical_entry_id
LEFT JOIN branch_nodes bn
  ON bn.branch_id = bzp.branch_id
LEFT JOIN LATERAL (
  SELECT
    ho.stage_status,
    ho.provenance_status,
    ho.rights_status,
    ho.branch_eligibility,
    ho.synergy_status,
    ho.node_relevance,
    ho.experimental_policy,
    ho.release_policy,
    ho.public_publish_status
  FROM hons_overlay ho
  WHERE ho.botanical_entry_id = bem.botanical_entry_id
  ORDER BY ho.updated_at DESC, ho.created_at DESC
  LIMIT 1
) ho ON TRUE;
