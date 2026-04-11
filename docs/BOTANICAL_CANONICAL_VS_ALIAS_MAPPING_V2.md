# Botanical Canonical Vs Alias Mapping V2

Last updated: 2026-04-01

## Rule

- canonical fields are the source-of-truth fields stored in normalized tables
- legacy or compatibility fields remain for continuity and easier consumers
- operational view aliases are human-facing names in `"Botanical_Operational_View"`

## Mappings

| Layer | Canonical field | Legacy / compatibility field | Operational view alias | Authority rule |
| --- | --- | --- | --- | --- |
| canonical_identity | `common_name_en` | `botanical_name` | `Common Name (EN)` | `common_name_en` is authoritative when populated; fall back to `botanical_name` only for compatibility |
| canonical_identity | `mature_height_m_min`, `mature_height_m_max` | `mature_height_m` | `Mature_Height_m_Min`, `Mature_Height_m_Max`, `Mature_Height_m` | range is canonical; single value remains shorthand |
| canonical_identity | `mature_spread_m_min`, `mature_spread_m_max` | `mature_spread_m` | `Mature_Spread_m_Min`, `Mature_Spread_m_Max`, `Mature_Spread_m` | range is canonical; single value remains shorthand |
| canonical_identity | `confidence_score`, `confidence_notes` | `data_confidence_level`, `record_completeness_score` | `Confidence Score`, `Confidence Notes`, `Data Confidence Level` | numeric score + notes is richer canonical source; coarse fields remain useful compatibility fields |
| zone_overlay | `light_preference`, `flood_tolerance`, `salinity_tolerance`, `heat_tolerance`, `fire_tolerance`, `harvest_window_brazil` | `sun_exposure`, `harvest_window` | `Light Preference`, `Flood Tolerance`, `Salinity Tolerance`, `Heat Tolerance`, `Fire Tolerance`, `Harvest Window Brazil` | new named tolerance/harvest fields are canonical; old broad text fields remain contextual support |
| hons_overlay | `stage_status`, `provenance_status`, `rights_status`, `branch_eligibility`, `synergy_status`, `node_relevance`, `experimental_policy`, `release_policy`, `public_publish_status` | `stage`, `rights_notes`, `governance_notes` | same names in the operational view | explicit status fields are canonical; narrative note fields remain support text |
