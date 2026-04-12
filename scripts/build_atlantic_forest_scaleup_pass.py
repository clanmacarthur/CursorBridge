import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"c:\Code\CursorBridge")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_botanical_final_patch_backfill import (
    normalize_text,
    read_xlsx,
    to_bool_token,
    write_csv,
)

BASELINE_DIR = ROOT / "exports" / "botanicals_fnp" / "latest"
ATLANTIC_XLSX = Path(
    r"C:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\ubatuba_green_coast_focus_pack_v1.xlsx"
)
COMPENDIUM_HTML = Path(
    r"C:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\mata_atlantica_compendium.html"
)
OUT_DIR = ROOT / "exports" / "atlantic_forest_scaleup" / "latest"
IDENTITY_TARGET_FLOOR = 3500


ENTRY_FIELDS = [
    "botanical_entry_id",
    "common_name_pt",
    "common_name_en",
    "botanical_name",
    "scientific_name",
    "variety_cultivar",
    "alternative_names",
    "duplicate_name_group",
    "duplicate_name_count",
    "part_used",
    "season",
    "ferment_safety",
    "use_type",
    "functions",
    "form_in_system",
    "micronutrients",
    "notes",
    "ayurvedic_profile",
    "tcm_meridians",
    "tcm_nature_flavour",
    "archetype_animal",
    "scientific_actions",
    "synergy_tags",
    "element_planet",
    "permaculture_guild",
    "biodynamic_timing",
    "soil_type",
    "growing_conditions",
    "foraging_habitat",
    "plant_type",
    "perennial_main_group",
    "sweep_bucket",
    "scarcity_class",
    "conservation_relevance",
    "heritage_flag",
    "medicinal_flag",
    "ecological_value_flag",
    "perennial_rating",
    "inclusion_rationale",
    "mature_height_m_min",
    "mature_height_m_max",
    "mature_height_m",
    "mature_spread_m_min",
    "mature_spread_m_max",
    "mature_spread_m",
    "size_class",
    "root_volume_class",
    "container_suitable",
    "pruning_response",
    "dwarf_flag",
    "grafted_flag",
    "self_fertile_flag",
    "pollination_requirement",
    "pollinator_type",
    "pollination_notes",
    "plant_lifespan_years",
    "productive_lifespan_years",
    "replacement_cycle_years",
    "data_confidence_level",
    "data_source_type",
    "record_completeness_score",
    "fields_completed_count",
    "system_roles",
    "propagation_difficulty",
    "propagation_success_rate",
    "invasiveness_risk_level",
    "spread_control_required",
    "min_temp_c",
    "max_temp_c",
    "drought_tolerance",
    "frost_tolerance",
    "endemic_to_brazil",
    "conservation_flag",
    "invasive_risk_brazil",
    "source_url_primary",
    "source_url_secondary",
    "source_url_tertiary",
    "confidence_score",
    "confidence_notes",
    "kombucha_1f_friendly_flag",
    "tea_friendly_flag",
    "bitters_friendly_flag",
    "cordial_friendly_flag",
    "fresh_produce_friendly_flag",
    "preserve_friendly_flag",
    "cosmetic_friendly_flag",
    "source_table",
    "source_row",
]

ZONE_FIELDS = [
    "zone_profile_id",
    "botanical_entry_id",
    "match_status",
    "match_candidates",
    "botanical_link",
    "common_names",
    "growth_habit",
    "forest_garden_layer",
    "lifespan",
    "native_region",
    "climate_band_prefers",
    "hardiness_class",
    "outdoor_suitability",
    "greenhouse_zone",
    "indoor_container_use",
    "soil_type",
    "soil_moisture",
    "soil_functions",
    "sun_exposure",
    "light_preference",
    "humidity_preference",
    "flood_tolerance",
    "salinity_tolerance",
    "heat_tolerance",
    "fire_tolerance",
    "root_depth_type",
    "spread_pattern",
    "companion_plants",
    "incompatible_with",
    "guild_roles",
    "foraging_habitat",
    "harvest_window",
    "harvest_window_brazil",
    "planting_sowing_window",
    "yield_regrowth",
    "propagation_methods",
    "recommended_establishment_method",
    "recommended_training_method",
    "branch_id",
    "branch_fit",
    "country",
    "region",
    "state_province",
    "zone",
    "microclimate_tags",
    "production_mode",
    "production_mode_basis",
    "spacing_in_row_m",
    "spacing_between_rows_m",
    "spacing_notes",
    "season_start_month",
    "season_end_month",
    "harvest_granularity",
    "harvest_window_1_start",
    "harvest_window_1_end",
    "harvest_window_1_peak_start",
    "harvest_window_1_peak_end",
    "harvest_window_2_start",
    "harvest_window_2_end",
    "harvest_window_2_peak_start",
    "harvest_window_2_peak_end",
    "harvest_passes_per_year",
    "time_to_first_harvest",
    "time_to_full_production",
    "yield_output_type",
    "yield_unit",
    "area_harvested_ha",
    "production_qty",
    "average_yield_per_ha",
    "yield_per_plant",
    "yield_low",
    "yield_typical",
    "yield_high",
    "processing_recovery_pct",
    "production_value_brl",
    "harvest_source",
    "harvest_source_year",
    "harvest_confidence",
    "yield_source",
    "yield_source_year",
    "yield_confidence",
    "notes",
    "source_table",
    "source_row",
]

DESIGN_FIELDS = [
    "design_matrix_id",
    "botanical_entry_id",
    "food_forest_layer",
    "canonical_layer_primary",
    "canonical_layer_secondary",
    "layer_stack_tags",
    "guild_role",
    "shade_tolerance",
    "water_need",
    "companion_tags",
    "notes",
    "source_table",
    "source_row",
]

ROOT_FIELDS = [
    "root_profile_id",
    "botanical_entry_id",
    "root_form",
    "root_depth_class",
    "root_spread_class",
    "root_aggression",
    "root_depth_min_m",
    "root_depth_max_m",
    "root_architecture_type",
    "root_depth_category",
    "excavation_sensitivity",
    "root_competition_intensity",
    "container_root_behavior",
    "waterlogging_tolerance",
    "notes",
    "source_table",
    "source_row",
]

SYMBIOSIS_FIELDS = [
    "symbiosis_profile_id",
    "botanical_entry_id",
    "symbiosis_type",
    "symbiotic_partner_type",
    "symbiotic_partner_botanical_id",
    "mycorrhizal_association_type",
    "nitrogen_fixing_flag",
    "host_dependency_flag",
    "nurse_plant_flag",
    "rhizosphere_benefit_notes",
    "symbiosis_strength",
    "symbiosis_confidence",
    "symbiotic_role_tags",
    "notes",
    "source_table",
    "source_row",
]

PRODUCT_FIELDS = [
    "product_path_id",
    "botanical_entry_id",
    "product_family_tags",
    "product_angle_notes",
    "kombucha_1f_friendly",
    "bitters_friendly",
    "cordial_friendly",
    "tea_friendly",
    "fresh_produce_friendly",
    "preserve_friendly",
    "cosmetic_friendly",
    "edible_flower_friendly",
    "cut_flower_friendly",
    "medicinal_flower_friendly",
    "petal_flavour_friendly",
    "dried_floral_friendly",
    "source_table",
    "source_row",
]

HONS_FIELDS = [
    "hons_overlay_id",
    "botanical_entry_id",
    "related_entity_id",
    "ownership_model",
    "rights_notes",
    "stage",
    "stage_status",
    "provenance_status",
    "rights_status",
    "branch_eligibility",
    "synergy_status",
    "node_relevance",
    "experimental_policy",
    "release_policy",
    "public_publish_status",
    "attribution",
    "governance_notes",
    "source_table",
    "source_row",
]

ROLE_PRIORITY = [
    "fruit_producer",
    "root_crop",
    "leafy_green",
    "medicinal",
    "nitrogen_fixer",
    "pollinator_support",
    "soil_cover",
    "climber",
    "structural",
    "wetland_filter",
    "xeric_support",
]

LAYER_LABELS = {
    "canopy": "Canopy",
    "subcanopy": "Sub-canopy",
    "shrub": "Shrub",
    "herbaceous": "Herbaceous",
    "groundcover": "Ground Cover",
    "climber": "Climber",
    "root": "Root",
    "epiphyte": "Epiphyte",
    "aquatic_marginal": "Aquatic / Marginal",
}


def parse_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def bool_token(value: str) -> str:
    return to_bool_token(value)


def maybe_bool_flag(value: str) -> str:
    token = bool_token(value)
    return token if token else ""


def canonical_scientific_name(value: str) -> str:
    text = (value or "").replace("×", " x ").strip()
    text = re.sub(r"\s+", " ", text)
    if not text:
        return ""
    parts = text.split(" ")
    if len(parts) < 2:
        return normalize_text(text)
    keep = []
    i = 0
    while i < len(parts):
        part = parts[i]
        if i < 2:
            keep.append(part)
            i += 1
            continue
        if part in {"x", "×"} and i + 1 < len(parts):
            keep.extend([part, parts[i + 1]])
            break
        if part in {"var.", "subsp.", "f."} and i + 1 < len(parts):
            keep.extend([part, parts[i + 1]])
            break
        if re.fullmatch(r"[a-z-]+", part):
            keep.append(part)
            i += 1
            continue
        break
    return normalize_text(" ".join(keep))


def scientific_display_name(value: str) -> str:
    return canonical_scientific_name(value).replace(" x ", " ")


def is_real_taxon(value: str) -> tuple[bool, str]:
    text = (value or "").strip()
    lower = text.lower()
    if not text:
        return False, "blank_scientific_name"
    if "/" in text or "+" in text:
        return False, "grouped_multi_taxon_name"
    if " species" in lower:
        return False, "species_group_name"
    if re.search(r"(^| )spp?\.( |$)", lower):
        return False, "open_species_placeholder"
    if len(canonical_scientific_name(text).split()) < 2:
        return False, "non_canonical_scientific_name"
    return True, ""


def biome_tags_for_text(*values: str) -> list[str]:
    text = normalize_text(" ".join(v for v in values if v))
    tags = {"Atlantic_Forest"}
    if any(
        token in text
        for token in [
            "restinga",
            "litoral",
            "mangrove",
            "manguezal",
            "shore",
            "coastal tableland",
            "coastal shrubland",
            "beach",
        ]
    ):
        tags.add("Coastal_Restinga")
    if any(
        token in text
        for token in ["montane", "montana", "altitude", "altitudinal", "cloud forest", "highland", "alto montana", "upper montane"]
    ):
        tags.add("Highland")
    return [tag for tag in ["Atlantic_Forest", "Coastal_Restinga", "Highland"] if tag in tags]


def map_layers(master_row: dict[str, str], design_row: dict[str, str], zone_rows: list[dict[str, str]]) -> tuple[str, str, str, str]:
    raw = normalize_text(design_row.get("canonical_layer_primary", "") or design_row.get("food_forest_layer", ""))
    plant_type = normalize_text(master_row.get("plant_type", ""))
    form = normalize_text(master_row.get("form_in_system", ""))
    secondary_source = normalize_text(design_row.get("canonical_layer_secondary", ""))
    zone_text = normalize_text(
        " ".join(
            [
                " ".join(row.get("microclimate_tags", "") for row in zone_rows),
                " ".join(row.get("soil_moisture", "") for row in zone_rows),
                " ".join(row.get("native_region", "") for row in zone_rows),
                " ".join(row.get("zone", "") for row in zone_rows),
            ]
        )
    )
    height = parse_float(master_row.get("mature_height_m", ""))
    epiphyte = any(
        token in " ".join([form, secondary_source, master_row.get("notes", "")]).lower()
        for token in ["epiphy", "epifit"]
    )
    fern = any(
        token in " ".join([master_row.get("common_name_pt", ""), secondary_source, form]).lower()
        for token in ["fern", "samambaia", "xaxim", "avenca"]
    )
    palm = raw == "palm_layer" or plant_type == "palm"
    wet = any(
        token in zone_text for token in ["wet", "riparian", "mangrove", "restinga", "brejo", "alag", "marsh", "palud", "humid"]
    )

    if epiphyte:
        primary = "epiphyte"
    elif raw == "vine_layer" or "vine" in plant_type or "liana" in plant_type or "trepadeira" in form:
        primary = "climber"
    elif raw == "canopy_tree":
        primary = "canopy"
    elif palm:
        primary = "canopy" if height and height > 10 else "subcanopy"
    elif raw == "subcanopy_tree_shrub":
        primary = "subcanopy" if plant_type in {"tree", "tree_shrub"} and (height is None or height >= 5) else "shrub"
    elif raw in {"shrub_layer", "subshrub_layer"}:
        primary = "herbaceous" if raw == "subshrub_layer" and height is not None and height <= 1.0 else "shrub"
    elif raw == "succulent_layer":
        primary = "groundcover" if height is not None and height <= 0.5 else "shrub"
    elif raw == "mixed_layer":
        if "tree" in plant_type:
            primary = "subcanopy" if height is None or height <= 10 else "canopy"
        elif "vine" in plant_type or "liana" in plant_type:
            primary = "climber"
        else:
            primary = "shrub" if height and height > 1.0 else "herbaceous"
    else:
        primary = "groundcover" if raw == "herb_layer" and height is not None and height <= 0.35 else "herbaceous"

    secondary = ""
    secondary_tags = []
    if palm:
        secondary_tags.append("palm")
    if fern:
        secondary_tags.append("fern")
    if wet and primary in {"groundcover", "herbaceous", "shrub"}:
        secondary = "aquatic_marginal"
    elif epiphyte and primary != "epiphyte":
        secondary = "epiphyte"

    stack_tags = [f"primary:{primary}", f"raw:{raw or 'unmapped'}", f"plant_type:{plant_type or 'unresolved'}"]
    if secondary:
        stack_tags.append(f"secondary:{secondary}")
    stack_tags.extend(secondary_tags)
    stack_tags.append(f"size:{(master_row.get('size_class', '') or 'unresolved')}")
    food_forest_layer = LAYER_LABELS[primary]
    if secondary:
        food_forest_layer = f"{food_forest_layer} / {LAYER_LABELS[secondary]}"
    secondary_value = secondary or ";".join(secondary_tags)
    return food_forest_layer, primary, secondary_value, ";".join(stack_tags)


def derive_roles(master_row: dict[str, str], primary: str, zone_rows: list[dict[str, str]]) -> list[str]:
    roles = set()
    raw_roles = normalize_text(master_row.get("system_roles", ""))
    plant_type = normalize_text(master_row.get("plant_type", ""))
    form = normalize_text(master_row.get("form_in_system", ""))
    zone_text = normalize_text(
        " ".join(row.get("soil_moisture", "") + " " + row.get("microclimate_tags", "") + " " + row.get("zone", "") for row in zone_rows)
    )
    scientific = normalize_text(master_row.get("scientific_name", ""))

    if bool_token(master_row.get("medicinal_flag", "")) == "TRUE":
        roles.add("medicinal")
    if primary == "climber":
        roles.add("climber")
    if primary == "groundcover":
        roles.add("soil_cover")
    if primary in {"canopy", "subcanopy"} or plant_type in {"tree", "tree_shrub", "palm"}:
        roles.add("structural")
    if any(token in zone_text for token in ["wet", "riparian", "mangrove", "marsh", "brejo", "alag", "restinga"]) and primary in {"groundcover", "herbaceous", "shrub"}:
        roles.add("wetland_filter")
    if master_row.get("drought_tolerance", "") == "high" or "succulent" in plant_type or "cactus" in plant_type:
        roles.add("xeric_support")
    if any(token in scientific for token in ["inga ", "mimosa ", "erythrina ", "canavalia ", "phaseolus ", "aeschynomene ", "desmodium "]):
        roles.add("nitrogen_fixer")
    if master_row.get("pollinator_type", "") or master_row.get("pollination_notes", ""):
        roles.add("pollinator_support")
    if "horticulture_or_crop" in raw_roles:
        if primary in {"canopy", "subcanopy", "shrub", "climber"}:
            roles.add("fruit_producer")
        elif any(token in form for token in ["rhizome", "rizoma", "tuber", "bulb", "corm"]):
            roles.add("root_crop")
        else:
            roles.add("leafy_green")
    if not roles:
        if primary == "climber":
            roles.add("climber")
        elif primary in {"canopy", "subcanopy", "shrub"}:
            roles.add("structural")
        elif primary == "groundcover":
            roles.add("soil_cover")
        elif bool_token(master_row.get("ecological_value_flag", "")) == "TRUE":
            roles.add("pollinator_support")
        else:
            roles.add("leafy_green")
    return [role for role in ROLE_PRIORITY if role in roles]


def next_botanical_id(start_value: int) -> str:
    return f"BOT-BR-{start_value:04d}"


def compendium_candidate_count(seen_scientific_names: set[str]) -> int:
    text = COMPENDIUM_HTML.read_text(encoding="utf-8", errors="ignore")
    objects = re.findall(r"\{name:'([^']*)',sci:'([^']*)',fam:'([^']*)',cat:'([^']*)',g:'([^']*)',sz:([^,}]+)", text)
    exclude_terms = [
        "fungus",
        "lichen",
        "moss",
        "bee",
        "bird",
        "mammal",
        "fish",
        "crab",
        "crustacean",
        "bivalve",
        "reptile",
        "cyanobacteria",
        "algae",
        "product",
        "insect",
    ]
    count = 0
    for name, sci, fam, cat, g, sz in objects:
        combined = f"{name} {sci} {fam} {cat}".lower()
        if any(term in combined for term in exclude_terms):
            continue
        if "/" in sci or "+" in sci or " species" in sci.lower() or re.search(r"(^| )spp?\.( |$)", sci.lower()):
            continue
        canonical = canonical_scientific_name(sci)
        if canonical and canonical not in seen_scientific_names:
            count += 1
    return count


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    baseline_manifest = json.loads((BASELINE_DIR / "manifest.json").read_text(encoding="utf-8"))
    baseline_identity_count = baseline_manifest["counts"]["atlantic_forest_identity_count"]
    baseline_operational_count = baseline_manifest["counts"]["atlantic_forest_operational_count"]

    with (BASELINE_DIR / "botanical_entries_master_fnp_backfill.csv").open(encoding="utf-8-sig", newline="") as handle:
        baseline_entries = list(csv.DictReader(handle))

    baseline_scientific = {
        canonical_scientific_name(row.get("scientific_name", ""))
        for row in baseline_entries
        if row.get("scientific_name")
    }
    baseline_scientific.discard("")

    max_id = 0
    for row in baseline_entries:
        match = re.match(r"BOT-BR-(\d+)$", row.get("botanical_entry_id", ""))
        if match:
            max_id = max(max_id, int(match.group(1)))

    workbook = read_xlsx(ATLANTIC_XLSX)
    master_rows = workbook["botanical_entries_master"]
    design_by_old_id = {row["botanical_entry_id"]: row for row in workbook["species_design_matrix"]}
    root_by_old_id = {row["botanical_entry_id"]: row for row in workbook["species_root_profile"]}
    symbiosis_by_old_id = {row["botanical_entry_id"]: row for row in workbook["species_symbiosis_profile"]}
    product_by_old_id = {row["botanical_entry_id"]: row for row in workbook["botanical_product_paths"]}
    zones_by_old_id: dict[str, list[dict[str, str]]] = {}
    for row in workbook["botanical_zone_profiles"]:
        zones_by_old_id.setdefault(row["botanical_entry_id"], []).append(row)

    entries_out: list[dict[str, str]] = []
    design_out: list[dict[str, str]] = []
    zones_out: list[dict[str, str]] = []
    root_out: list[dict[str, str]] = []
    symbiosis_out: list[dict[str, str]] = []
    product_out: list[dict[str, str]] = []
    hons_out: list[dict[str, str]] = []

    overlap_existing: list[dict[str, str]] = []
    skipped_non_real: list[dict[str, str]] = []
    unresolved_product: list[str] = []
    derived_symbiosis: list[str] = []
    mixed_layer_review: list[str] = []
    layer_counts: Counter[str] = Counter()
    biome_tag_counter: Counter[str] = Counter()

    seen_new_scientific: set[str] = set()
    id_counter = max_id

    for row in master_rows:
        scientific_raw = row.get("scientific_name", "")
        valid, reason = is_real_taxon(scientific_raw)
        if not valid:
            skipped_non_real.append(
                {
                    "source_id": row.get("botanical_entry_id", ""),
                    "scientific_name": scientific_raw,
                    "reason": reason,
                }
            )
            continue

        canonical = canonical_scientific_name(scientific_raw)
        if canonical in baseline_scientific or canonical in seen_new_scientific:
            overlap_existing.append(
                {
                    "source_id": row.get("botanical_entry_id", ""),
                    "scientific_name": canonical,
                }
            )
            continue

        old_id = row["botanical_entry_id"]
        design_row = design_by_old_id.get(old_id, {})
        root_row = root_by_old_id.get(old_id, {})
        sym_row = symbiosis_by_old_id.get(old_id, {})
        product_row = product_by_old_id.get(old_id, {})
        related_zones = zones_by_old_id.get(old_id, [])

        biome_tags = biome_tags_for_text(
            row.get("growing_conditions", ""),
            row.get("foraging_habitat", ""),
            row.get("notes", ""),
            row.get("inclusion_rationale", ""),
            " ".join(zone.get("zone", "") for zone in related_zones),
            " ".join(zone.get("microclimate_tags", "") for zone in related_zones),
            " ".join(zone.get("native_region", "") for zone in related_zones),
        )
        for tag in biome_tags:
            biome_tag_counter[tag] += 1

        food_layer, primary_layer, secondary_layer, stack_tags = map_layers(row, design_row, related_zones)
        layer_counts[primary_layer] += 1
        if normalize_text(design_row.get("canonical_layer_primary", "")) == "mixed_layer":
            mixed_layer_review.append(old_id)

        roles = derive_roles(row, primary_layer, related_zones)
        guild_role = ";".join(roles) or "structural"

        id_counter += 1
        new_id = next_botanical_id(id_counter)
        seen_new_scientific.add(canonical)

        inclusion_parts = [
            f"biome_tags={'|'.join(biome_tags)}",
            "scaleup_pass=Atlantic_Forest_Scaleup_2026-04-06",
            "scaleup_source=ubatuba_green_coast_focus_pack_v1",
        ]
        source_rationale = row.get("inclusion_rationale", "").strip()
        if source_rationale:
            inclusion_parts.append(f"source_rationale={source_rationale}")

        notes = row.get("notes", "").strip()
        if old_id.startswith("BR-BEM-"):
            notes = f"{notes} | source_botanical_entry_id={old_id}" if notes else f"source_botanical_entry_id={old_id}"

        common_name_pt = row.get("common_name_pt", "") or row.get("botanical_name", "")
        scientific_name = scientific_display_name(scientific_raw)
        source_url_primary = f"https://floradobrasil.jbrj.gov.br/consulta/?q={scientific_name.replace(' ', '%20')}" if scientific_name else ""
        source_url_secondary = f"https://powo.science.kew.org/results?q={scientific_name.replace(' ', '%20')}" if scientific_name else ""

        entries_out.append(
            {
                "botanical_entry_id": new_id,
                "common_name_pt": common_name_pt,
                "common_name_en": "",
                "botanical_name": row.get("botanical_name", scientific_name or common_name_pt),
                "scientific_name": scientific_name,
                "variety_cultivar": row.get("variety_cultivar", ""),
                "alternative_names": row.get("alternative_names", ""),
                "duplicate_name_group": row.get("duplicate_name_group", ""),
                "duplicate_name_count": row.get("duplicate_name_count", ""),
                "part_used": row.get("part_used", ""),
                "season": row.get("season", ""),
                "ferment_safety": row.get("ferment_safety", ""),
                "use_type": row.get("use_type", ""),
                "functions": row.get("functions", ""),
                "form_in_system": row.get("form_in_system", ""),
                "micronutrients": row.get("micronutrients", ""),
                "notes": notes,
                "ayurvedic_profile": row.get("ayurvedic_profile", ""),
                "tcm_meridians": row.get("tcm_meridians", ""),
                "tcm_nature_flavour": row.get("tcm_nature_flavour", ""),
                "archetype_animal": row.get("archetype_animal", ""),
                "scientific_actions": row.get("scientific_actions", ""),
                "synergy_tags": row.get("synergy_tags", ""),
                "element_planet": row.get("element_planet", ""),
                "permaculture_guild": row.get("permaculture_guild", ""),
                "biodynamic_timing": row.get("biodynamic_timing", ""),
                "soil_type": row.get("soil_type", ""),
                "growing_conditions": row.get("growing_conditions", ""),
                "foraging_habitat": row.get("foraging_habitat", ""),
                "plant_type": row.get("plant_type", ""),
                "perennial_main_group": row.get("perennial_main_group", ""),
                "sweep_bucket": row.get("sweep_bucket", ""),
                "scarcity_class": row.get("scarcity_class", ""),
                "conservation_relevance": row.get("conservation_relevance", ""),
                "heritage_flag": maybe_bool_flag(row.get("heritage_flag", "")),
                "medicinal_flag": maybe_bool_flag(row.get("medicinal_flag", "")),
                "ecological_value_flag": maybe_bool_flag(row.get("ecological_value_flag", "")),
                "perennial_rating": row.get("perennial_rating", ""),
                "inclusion_rationale": "; ".join(inclusion_parts),
                "mature_height_m_min": "",
                "mature_height_m_max": row.get("mature_height_m", ""),
                "mature_height_m": row.get("mature_height_m", ""),
                "mature_spread_m_min": "",
                "mature_spread_m_max": row.get("mature_spread_m", ""),
                "mature_spread_m": row.get("mature_spread_m", ""),
                "size_class": row.get("size_class", ""),
                "root_volume_class": row.get("root_volume_class", ""),
                "container_suitable": row.get("container_suitable", ""),
                "pruning_response": row.get("pruning_response", ""),
                "dwarf_flag": "FALSE",
                "grafted_flag": maybe_bool_flag(row.get("grafted_flag", "")),
                "self_fertile_flag": maybe_bool_flag(row.get("self_fertile_flag", "")),
                "pollination_requirement": row.get("pollination_requirement", ""),
                "pollinator_type": row.get("pollinator_type", ""),
                "pollination_notes": row.get("pollination_notes", ""),
                "plant_lifespan_years": row.get("plant_lifespan_years", ""),
                "productive_lifespan_years": row.get("productive_lifespan_years", ""),
                "replacement_cycle_years": row.get("replacement_cycle_years", ""),
                "data_confidence_level": row.get("data_confidence_level", "medium"),
                "data_source_type": row.get("data_source_type", "ubatuba_green_coast_focus_pack_v1"),
                "record_completeness_score": row.get("record_completeness_score", ""),
                "fields_completed_count": row.get("fields_completed_count", ""),
                "system_roles": ";".join(roles),
                "propagation_difficulty": row.get("propagation_difficulty", ""),
                "propagation_success_rate": row.get("propagation_success_rate", ""),
                "invasiveness_risk_level": row.get("invasiveness_risk_level", ""),
                "spread_control_required": maybe_bool_flag(row.get("spread_control_required", "")),
                "min_temp_c": row.get("min_temp_c", ""),
                "max_temp_c": row.get("max_temp_c", ""),
                "drought_tolerance": row.get("drought_tolerance", ""),
                "frost_tolerance": row.get("frost_tolerance", ""),
                "endemic_to_brazil": "TRUE" if "endemic" in normalize_text(row.get("scarcity_class", "")) else "FALSE",
                "conservation_flag": row.get("conservation_relevance", ""),
                "invasive_risk_brazil": row.get("invasiveness_risk_level", ""),
                "source_url_primary": source_url_primary,
                "source_url_secondary": source_url_secondary,
                "source_url_tertiary": "",
                "confidence_score": row.get("record_completeness_score", ""),
                "confidence_notes": "Atlantic Forest scale-up row carried from Ubatuba / Green Coast focus pack; layer and role normalization applied without schema changes.",
                "kombucha_1f_friendly_flag": maybe_bool_flag(row.get("kombucha_1f_friendly_flag", "")),
                "tea_friendly_flag": maybe_bool_flag(row.get("tea_friendly_flag", "")),
                "bitters_friendly_flag": maybe_bool_flag(row.get("bitters_friendly_flag", "")),
                "cordial_friendly_flag": maybe_bool_flag(row.get("cordial_friendly_flag", "")),
                "fresh_produce_friendly_flag": maybe_bool_flag(row.get("fresh_produce_friendly_flag", "")),
                "preserve_friendly_flag": maybe_bool_flag(row.get("preserve_friendly_flag", "")),
                "cosmetic_friendly_flag": maybe_bool_flag(row.get("cosmetic_friendly_flag", "")),
                "source_table": row.get("source_table", "ubatuba_green_coast_focus_pack_v1"),
                "source_row": row.get("source_row", row.get("__source_row", "")),
            }
        )

        design_notes = design_row.get("notes", "").strip()
        design_notes = f"{design_notes} | normalized_layer_primary={primary_layer}" if design_notes else f"normalized_layer_primary={primary_layer}"
        design_out.append(
            {
                "design_matrix_id": f"SDM-{new_id}",
                "botanical_entry_id": new_id,
                "food_forest_layer": food_layer,
                "canonical_layer_primary": primary_layer,
                "canonical_layer_secondary": secondary_layer,
                "layer_stack_tags": stack_tags,
                "guild_role": guild_role,
                "shade_tolerance": design_row.get("shade_tolerance", ""),
                "water_need": design_row.get("water_need", ""),
                "companion_tags": design_row.get("companion_tags", ""),
                "notes": f"biome_tags={'|'.join(biome_tags)}; {design_notes}",
                "source_table": design_row.get("source_table", "ubatuba_green_coast_focus_pack_v1"),
                "source_row": design_row.get("source_row", design_row.get("__source_row", "")),
            }
        )

        root_out.append(
            {
                "root_profile_id": f"ROOT-{new_id}",
                "botanical_entry_id": new_id,
                "root_form": root_row.get("root_form", ""),
                "root_depth_class": root_row.get("root_depth_class", ""),
                "root_spread_class": root_row.get("root_spread_class", ""),
                "root_aggression": root_row.get("root_aggression", ""),
                "root_depth_min_m": root_row.get("root_depth_min_m", ""),
                "root_depth_max_m": root_row.get("root_depth_max_m", ""),
                "root_architecture_type": root_row.get("root_architecture_type", ""),
                "root_depth_category": root_row.get("root_depth_category", ""),
                "excavation_sensitivity": root_row.get("excavation_sensitivity", ""),
                "root_competition_intensity": root_row.get("root_competition_intensity", ""),
                "container_root_behavior": root_row.get("container_root_behavior", ""),
                "waterlogging_tolerance": root_row.get("waterlogging_tolerance", ""),
                "notes": root_row.get("notes", ""),
                "source_table": root_row.get("source_table", "ubatuba_green_coast_focus_pack_v1"),
                "source_row": root_row.get("source_row", root_row.get("__source_row", "")),
            }
        )

        if "builder_inference" in normalize_text(sym_row.get("symbiosis_confidence", "")) or "derived" in normalize_text(sym_row.get("symbiosis_strength", "")):
            derived_symbiosis.append(new_id)
        symbiosis_out.append(
            {
                "symbiosis_profile_id": f"SYM-{new_id}",
                "botanical_entry_id": new_id,
                "symbiosis_type": sym_row.get("symbiosis_type", ""),
                "symbiotic_partner_type": sym_row.get("symbiotic_partner_type", ""),
                "symbiotic_partner_botanical_id": "",
                "mycorrhizal_association_type": sym_row.get("mycorrhizal_association_type", ""),
                "nitrogen_fixing_flag": maybe_bool_flag(sym_row.get("nitrogen_fixing_flag", "")),
                "host_dependency_flag": maybe_bool_flag(sym_row.get("host_dependency_flag", "")),
                "nurse_plant_flag": maybe_bool_flag(sym_row.get("nurse_plant_flag", "")),
                "rhizosphere_benefit_notes": sym_row.get("rhizosphere_benefit_notes", ""),
                "symbiosis_strength": sym_row.get("symbiosis_strength", ""),
                "symbiosis_confidence": sym_row.get("symbiosis_confidence", ""),
                "symbiotic_role_tags": sym_row.get("symbiotic_role_tags", ""),
                "notes": sym_row.get("notes", ""),
                "source_table": sym_row.get("source_table", "ubatuba_green_coast_focus_pack_v1"),
                "source_row": sym_row.get("source_row", sym_row.get("__source_row", "")),
            }
        )

        product_tags = []
        if "fruit_producer" in roles or "leafy_green" in roles or "root_crop" in roles:
            product_tags.append("Fresh Produce")
        if "medicinal" in roles:
            product_tags.append("Medicinal")
        if maybe_bool_flag(row.get("cordial_friendly_flag", "")) == "TRUE":
            product_tags.append("Cordial / Syrup")
        if maybe_bool_flag(row.get("tea_friendly_flag", "")) == "TRUE":
            product_tags.append("Tea / Tisane")
        if maybe_bool_flag(row.get("preserve_friendly_flag", "")) == "TRUE":
            product_tags.append("Jam / Preserve")
        if maybe_bool_flag(row.get("cosmetic_friendly_flag", "")) == "TRUE":
            product_tags.append("Cosmetic / Topical")
        product_family_tags = "; ".join(dict.fromkeys(product_tags))
        if product_family_tags:
            product_angle_notes = f"Derived from normalized roles for Atlantic Forest scale-up: {';'.join(roles)}"
        else:
            product_family_tags = "review_needed_for_atlantic_product_mapping"
            product_angle_notes = "Atlantic focus pack provided no explicit product-use fields for this row; retain for later product mapping."
            unresolved_product.append(new_id)

        product_out.append(
            {
                "product_path_id": f"BPP-{new_id}",
                "botanical_entry_id": new_id,
                "product_family_tags": product_family_tags,
                "product_angle_notes": product_angle_notes,
                "kombucha_1f_friendly": maybe_bool_flag(product_row.get("kombucha_1f_friendly", row.get("kombucha_1f_friendly_flag", ""))),
                "bitters_friendly": maybe_bool_flag(product_row.get("bitters_friendly", row.get("bitters_friendly_flag", ""))),
                "cordial_friendly": maybe_bool_flag(product_row.get("cordial_friendly", row.get("cordial_friendly_flag", ""))),
                "tea_friendly": maybe_bool_flag(product_row.get("tea_friendly", row.get("tea_friendly_flag", ""))),
                "fresh_produce_friendly": maybe_bool_flag(product_row.get("fresh_produce_friendly", row.get("fresh_produce_friendly_flag", ""))),
                "preserve_friendly": maybe_bool_flag(product_row.get("preserve_friendly", row.get("preserve_friendly_flag", ""))),
                "cosmetic_friendly": maybe_bool_flag(product_row.get("cosmetic_friendly", row.get("cosmetic_friendly_flag", ""))),
                "edible_flower_friendly": maybe_bool_flag(product_row.get("edible_flower_friendly", "")),
                "cut_flower_friendly": maybe_bool_flag(product_row.get("cut_flower_friendly", "")),
                "medicinal_flower_friendly": maybe_bool_flag(product_row.get("medicinal_flower_friendly", "")),
                "petal_flavour_friendly": maybe_bool_flag(product_row.get("petal_flavour_friendly", "")),
                "dried_floral_friendly": maybe_bool_flag(product_row.get("dried_floral_friendly", "")),
                "source_table": product_row.get("source_table", "ubatuba_green_coast_focus_pack_v1"),
                "source_row": product_row.get("source_row", product_row.get("__source_row", "")),
            }
        )

        hons_out.append(
            {
                "hons_overlay_id": f"HONS-{new_id}",
                "botanical_entry_id": new_id,
                "related_entity_id": "",
                "ownership_model": "unresolved",
                "rights_notes": "unresolved",
                "stage": "unresolved",
                "stage_status": "unresolved",
                "provenance_status": "atlantic_scaleup_source_pack",
                "rights_status": "unresolved",
                "branch_eligibility": "branch_brazil;branch_brazil_ubatuba_green_coast",
                "synergy_status": "unresolved",
                "node_relevance": "atlantic_forest_current_branch",
                "experimental_policy": "unresolved",
                "release_policy": "delta_only",
                "public_publish_status": "internal_audit",
                "attribution": "Ubatuba / Green Coast source workbooks",
                "governance_notes": "Atlantic Forest scale-up populated explicit unresolved governance statuses because no row-level HONS source fields exist in the current Atlantic source pack.",
                "source_table": "ubatuba_green_coast_focus_pack_v1",
                "source_row": row.get("source_row", row.get("__source_row", "")),
            }
        )

        for zone_row in related_zones:
            zone_notes = zone_row.get("notes", "").strip()
            biome_note = f"biome_tags={'|'.join(biome_tags)}; scaleup_pass=Atlantic_Forest_Scaleup_2026-04-06"
            zone_notes = f"{zone_notes} | {biome_note}" if zone_notes else biome_note
            zones_out.append(
                {
                    "zone_profile_id": f"AF-ZONE-{new_id}-{zone_row.get('zone_profile_id', zone_row.get('__source_row', '0'))}",
                    "botanical_entry_id": new_id,
                    "match_status": zone_row.get("match_status", "source_matched"),
                    "match_candidates": zone_row.get("match_candidates", ""),
                    "botanical_link": scientific_name or row.get("botanical_name", ""),
                    "common_names": zone_row.get("common_names", common_name_pt),
                    "growth_habit": zone_row.get("growth_habit", ""),
                    "forest_garden_layer": food_layer,
                    "lifespan": zone_row.get("lifespan", ""),
                    "native_region": zone_row.get("native_region", ""),
                    "climate_band_prefers": zone_row.get("climate_band_prefers", ""),
                    "hardiness_class": zone_row.get("hardiness_class", ""),
                    "outdoor_suitability": zone_row.get("outdoor_suitability", ""),
                    "greenhouse_zone": zone_row.get("greenhouse_zone", ""),
                    "indoor_container_use": zone_row.get("indoor_container_use", ""),
                    "soil_type": zone_row.get("soil_type", ""),
                    "soil_moisture": zone_row.get("soil_moisture", ""),
                    "soil_functions": zone_row.get("soil_functions", ""),
                    "sun_exposure": zone_row.get("sun_exposure", ""),
                    "light_preference": zone_row.get("light_preference", ""),
                    "humidity_preference": zone_row.get("humidity_preference", ""),
                    "flood_tolerance": zone_row.get("flood_tolerance", ""),
                    "salinity_tolerance": zone_row.get("salinity_tolerance", ""),
                    "heat_tolerance": zone_row.get("heat_tolerance", ""),
                    "fire_tolerance": zone_row.get("fire_tolerance", ""),
                    "root_depth_type": zone_row.get("root_depth_type", ""),
                    "spread_pattern": zone_row.get("spread_pattern", ""),
                    "companion_plants": zone_row.get("companion_plants", ""),
                    "incompatible_with": zone_row.get("incompatible_with", ""),
                    "guild_roles": guild_role,
                    "foraging_habitat": zone_row.get("foraging_habitat", ""),
                    "harvest_window": zone_row.get("harvest_window", ""),
                    "harvest_window_brazil": zone_row.get("harvest_window", ""),
                    "planting_sowing_window": zone_row.get("planting_sowing_window", ""),
                    "yield_regrowth": zone_row.get("yield_regrowth", ""),
                    "propagation_methods": zone_row.get("propagation_methods", ""),
                    "recommended_establishment_method": zone_row.get("recommended_establishment_method", ""),
                    "recommended_training_method": zone_row.get("recommended_training_method", ""),
                    "branch_id": zone_row.get("branch_id", "branch_brazil_ubatuba_green_coast"),
                    "branch_fit": zone_row.get("branch_fit", ""),
                    "country": zone_row.get("country", "Brazil"),
                    "region": zone_row.get("region", ""),
                    "state_province": zone_row.get("state_province", ""),
                    "zone": zone_row.get("zone", "atlantic_forest_reference_general"),
                    "microclimate_tags": zone_row.get("microclimate_tags", ""),
                    "production_mode": zone_row.get("production_mode", ""),
                    "production_mode_basis": zone_row.get("production_mode_basis", ""),
                    "spacing_in_row_m": zone_row.get("spacing_in_row_m", ""),
                    "spacing_between_rows_m": zone_row.get("spacing_between_rows_m", ""),
                    "spacing_notes": zone_row.get("spacing_notes", ""),
                    "season_start_month": zone_row.get("season_start_month", ""),
                    "season_end_month": zone_row.get("season_end_month", ""),
                    "harvest_granularity": zone_row.get("harvest_granularity", ""),
                    "harvest_window_1_start": zone_row.get("harvest_window_1_start", ""),
                    "harvest_window_1_end": zone_row.get("harvest_window_1_end", ""),
                    "harvest_window_1_peak_start": zone_row.get("harvest_window_1_peak_start", ""),
                    "harvest_window_1_peak_end": zone_row.get("harvest_window_1_peak_end", ""),
                    "harvest_window_2_start": zone_row.get("harvest_window_2_start", ""),
                    "harvest_window_2_end": zone_row.get("harvest_window_2_end", ""),
                    "harvest_window_2_peak_start": zone_row.get("harvest_window_2_peak_start", ""),
                    "harvest_window_2_peak_end": zone_row.get("harvest_window_2_peak_end", ""),
                    "harvest_passes_per_year": zone_row.get("harvest_passes_per_year", ""),
                    "time_to_first_harvest": zone_row.get("time_to_first_harvest", ""),
                    "time_to_full_production": zone_row.get("time_to_full_production", ""),
                    "yield_output_type": zone_row.get("yield_output_type", ""),
                    "yield_unit": zone_row.get("yield_unit", ""),
                    "area_harvested_ha": zone_row.get("area_harvested_ha", ""),
                    "production_qty": zone_row.get("production_qty", ""),
                    "average_yield_per_ha": zone_row.get("average_yield_per_ha", ""),
                    "yield_per_plant": zone_row.get("yield_per_plant", ""),
                    "yield_low": zone_row.get("yield_low", ""),
                    "yield_typical": zone_row.get("yield_typical", ""),
                    "yield_high": zone_row.get("yield_high", ""),
                    "processing_recovery_pct": zone_row.get("processing_recovery_pct", ""),
                    "production_value_brl": zone_row.get("production_value_brl", ""),
                    "harvest_source": zone_row.get("harvest_source", ""),
                    "harvest_source_year": zone_row.get("harvest_source_year", ""),
                    "harvest_confidence": zone_row.get("harvest_confidence", ""),
                    "yield_source": zone_row.get("yield_source", ""),
                    "yield_source_year": zone_row.get("yield_source_year", ""),
                    "yield_confidence": zone_row.get("yield_confidence", ""),
                    "notes": zone_notes,
                    "source_table": zone_row.get("source_table", "ubatuba_green_coast_focus_pack_v1"),
                    "source_row": zone_row.get("source_row", zone_row.get("__source_row", "")),
                }
            )

    updated_identity_count = baseline_identity_count + len(entries_out)
    updated_operational_count = baseline_operational_count + len(zones_out)
    rows_added_total = (
        len(entries_out)
        + len(design_out)
        + len(zones_out)
        + len(root_out)
        + len(symbiosis_out)
        + len(product_out)
        + len(hons_out)
    )
    seen_for_next_block = baseline_scientific | seen_new_scientific
    next_block_compendium_candidates = compendium_candidate_count(seen_for_next_block)

    write_csv(OUT_DIR / "botanical_entries_master_atlantic_scaleup.csv", entries_out, ENTRY_FIELDS)
    write_csv(OUT_DIR / "species_design_matrix_atlantic_scaleup.csv", design_out, DESIGN_FIELDS)
    write_csv(OUT_DIR / "botanical_zone_profiles_atlantic_scaleup.csv", zones_out, ZONE_FIELDS)
    write_csv(OUT_DIR / "species_root_profile_atlantic_scaleup.csv", root_out, ROOT_FIELDS)
    write_csv(OUT_DIR / "species_symbiosis_profile_atlantic_scaleup.csv", symbiosis_out, SYMBIOSIS_FIELDS)
    write_csv(OUT_DIR / "botanical_product_paths_atlantic_scaleup.csv", product_out, PRODUCT_FIELDS)
    write_csv(OUT_DIR / "hons_overlay_atlantic_scaleup.csv", hons_out, HONS_FIELDS)

    manifest = {
        "generated_at": "2026-04-06",
        "source_files": {
            "baseline_manifest": str(BASELINE_DIR / "manifest.json"),
            "atlantic_source_workbook": str(ATLANTIC_XLSX),
            "next_block_reference_compendium": str(COMPENDIUM_HTML),
        },
        "baseline_counts": {
            "atlantic_forest_identity_count": baseline_identity_count,
            "atlantic_forest_operational_count": baseline_operational_count,
        },
        "added_counts": {
            "botanical_entries_master": len(entries_out),
            "species_design_matrix": len(design_out),
            "botanical_zone_profiles": len(zones_out),
            "species_root_profile": len(root_out),
            "species_symbiosis_profile": len(symbiosis_out),
            "botanical_product_paths": len(product_out),
            "hons_overlay": len(hons_out),
            "rows_added_total": rows_added_total,
        },
        "updated_counts": {
            "atlantic_forest_identity_count": updated_identity_count,
            "atlantic_forest_operational_count": updated_operational_count,
        },
        "layer_coverage_added": dict(sorted(layer_counts.items())),
        "biome_tags_added": dict(sorted(biome_tag_counter.items())),
        "unresolved": {
            "skipped_existing_baseline_overlap": overlap_existing,
            "skipped_non_real_taxon": skipped_non_real,
            "product_mapping_review_needed_count": len(unresolved_product),
            "product_mapping_review_needed_rows": unresolved_product[:100],
            "derived_symbiosis_count": len(derived_symbiosis),
            "derived_symbiosis_rows": derived_symbiosis[:100],
            "mixed_layer_review_count": len(mixed_layer_review),
            "mixed_layer_review_rows": mixed_layer_review,
        },
        "next_block_target": {
            "identity_target_floor": IDENTITY_TARGET_FLOOR,
            "identity_gap_after_this_pass": max(0, IDENTITY_TARGET_FLOOR - updated_identity_count),
            "safe_compendium_candidate_pool": next_block_compendium_candidates,
            "recommended_next_bulk_block": "close the remaining identity gap with additional Atlantic-only source extraction, starting from the compendium-only real-plant candidates that are not yet in the normalized Brazil baseline or this scale-up pack",
        },
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
