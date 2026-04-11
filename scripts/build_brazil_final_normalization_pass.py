import json
import re
from collections import Counter
from pathlib import Path

from scripts.build_botanical_final_patch_backfill import (
    normalize_text,
    read_xlsx,
    to_bool_token,
    write_csv,
)


ROOT = Path(r"c:\Code\CursorBridge")
BRAZIL_TABLES_XLSX = Path(
    r"C:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\brazil_data_tables_only.xlsx"
)
IDENTITY_XLSX = Path(
    r"C:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\brazil_identity_block1_core_targeted_large_v2.xlsx"
)
OUT_DIR = ROOT / "exports" / "botanicals_fnp" / "latest"

ROLE_PRIORITY = [
    "fruit_producer",
    "root_crop",
    "leafy_green",
    "medicinal",
    "nitrogen_fixer",
    "pollinator_support",
    "soil_cover",
    "climber",
    "wetland_filter",
    "xeric_support",
    "structural",
]

FOOD_FOREST_LABELS = {
    "canopy": "Canopy",
    "subcanopy": "Sub-canopy",
    "shrub": "Shrub",
    "herbaceous": "Herbaceous",
    "groundcover": "Ground Cover",
    "climber": "Climber",
    "root": "Root",
    "aquatic_marginal": "Aquatic / Marginal",
    "epiphyte": "Epiphyte",
    "fungal_layer": "Fungal Layer",
}


def parse_bool(value: str) -> bool | None:
    token = to_bool_token(value)
    if token == "TRUE":
        return True
    if token == "FALSE":
        return False
    return None


def parse_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_temp_band(value: str) -> tuple[float | None, float | None]:
    text = (value or "").strip()
    if not text:
        return None, None
    if "-" not in text:
        single = parse_float(text)
        return single, single
    left, right = text.split("-", 1)
    return parse_float(left), parse_float(right)


def score_to_confidence_level(value: str) -> str:
    score = parse_float(value)
    if score is None:
        return "unresolved"
    if score >= 5:
        return "high"
    if score >= 4:
        return "medium"
    return "low"


def normalize_biomes(*values: str) -> tuple[list[str], list[str]]:
    tags = set()
    bases = set()
    for raw in values:
        text = normalize_text(raw)
        if not text:
            continue
        if "amazon" in text or "amazonia" in text:
            tags.add("Amazon")
            bases.add("amazon")
        if "cerrado" in text:
            tags.add("Cerrado")
            bases.add("cerrado")
        if "atlantic forest" in text or "mata atlantica" in text:
            tags.add("Atlantic_Forest")
            bases.add("atlantic_forest")
        if "caatinga" in text:
            tags.add("Caatinga")
            bases.add("caatinga")
        if "pantanal" in text:
            tags.add("Pantanal")
            bases.add("pantanal")
        if (
            "south subtropical" in text
            or "subtropical humid" in text
            or "south pampa" in text
            or "pampa" in text
        ):
            tags.add("South_Subtropical")
            bases.add("south_subtropical")
        if (
            "coastal systems" in text
            or "coastal cultivated systems" in text
            or "coastal tablelands" in text
            or "northeast coastal humid" in text
            or "atlantic forest coastal" in text
            or "coastal atlantic forest" in text
            or "coastal shrubland" in text
            or "coastal" in text
            or "restinga" in text
        ):
            tags.add("Coastal_Restinga")
            bases.add("coastal_restinga")
        if (
            "highland" in text
            or "highlands" in text
            or "southeast highland mild" in text
            or "cerrado highlands" in text
            or "tropical highland" in text
        ):
            tags.add("Highland")
            bases.add("highland")
    return sorted(tags), sorted(bases)


def slugify(value: str) -> str:
    text = normalize_text(value)
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "unresolved"


def derive_layers(master_row: dict[str, str], identity_row: dict[str, str] | None, roles: list[str]) -> tuple[str, str, str, str]:
    growth_form = (identity_row or {}).get("growth_form", "")
    plant_type = (master_row.get("Plant Type", "") or "").strip().lower()
    growth = normalize_text(growth_form)
    height_max = parse_float((identity_row or {}).get("mature_height_m_max", ""))
    size_class = ((identity_row or {}).get("builder_size_class", "") or "").strip()

    primary = ""
    secondary = ""

    if "climbing orchid vine" in growth:
        primary = "climber"
        secondary = "epiphyte"
    elif "woody climber" in growth or "woody vine" in growth or "vine" in growth or "climbing cactus" in plant_type:
        primary = "climber"
    elif growth == "orchid":
        primary = "epiphyte"
    elif "groundcover" in growth:
        primary = "groundcover"
    elif "bromeliad" in growth:
        primary = "herbaceous"
    elif "herbaceous perennial" in growth or "large herbaceous monocot" in growth or "tall perennial grass" in growth:
        primary = "herbaceous"
    elif "cactus or succulent" in growth:
        primary = "shrub"
    elif (
        "palm" in growth
        or "tree" in growth
        or plant_type in {"tree", "tree / shrub", "palm"}
        or "bamboo" in growth
    ):
        if height_max is not None:
            if height_max > 10:
                primary = "canopy"
            elif height_max > 5:
                primary = "subcanopy"
            else:
                primary = "subcanopy" if plant_type == "palm" else "shrub"
        else:
            if "small tree" in growth or plant_type in {"shrub / small tree", "tree / shrub", "shrub / vine"}:
                primary = "subcanopy"
            elif plant_type == "palm":
                primary = "subcanopy"
            else:
                primary = "canopy"
    elif "shrub" in growth or "subshrub" in plant_type or "shrub" in plant_type:
        primary = "shrub"
    elif plant_type in {"herb", "herb / shrub"}:
        primary = "herbaceous"
    elif plant_type == "vine":
        primary = "climber"
    else:
        primary = "herbaceous"

    if primary in {"herbaceous", "groundcover"} and "root_crop" in roles:
        secondary = "root"
    elif primary == "herbaceous" and "groundcover" in growth:
        secondary = "groundcover"
    elif primary == "shrub" and ("small tree" in growth or "tree" in plant_type) and (height_max or 0) > 5:
        secondary = "subcanopy"

    label = FOOD_FOREST_LABELS[primary]
    if secondary:
        label = f"{label} / {FOOD_FOREST_LABELS[secondary]}"

    stack_parts = [f"primary:{primary}"]
    if secondary:
        stack_parts.append(f"secondary:{secondary}")
    if size_class:
        stack_parts.append(f"size:{size_class}")
    if growth_form:
        stack_parts.append(f"growth:{slugify(growth_form)}")
    return label, primary, secondary, ";".join(stack_parts)


def derive_roles(
    master_row: dict[str, str],
    identity_row: dict[str, str] | None,
    primary_layer: str,
    biome_tags: list[str],
) -> list[str]:
    roles = set()
    source_bits = " ".join(
        [
            master_row.get("Use Type", ""),
            master_row.get("Functions", ""),
            master_row.get("Part Used", ""),
            master_row.get("Plant Type", ""),
            (identity_row or {}).get("primary_use_class", ""),
            (identity_row or {}).get("secondary_use_class", ""),
            (identity_row or {}).get("growth_form", ""),
        ]
    )
    source = normalize_text(source_bits)

    if any(token in source for token in ["fruit", "pulp", "citrus", "nut", "seed", "berry", "coffee", "beverage_seed"]):
        roles.add("fruit_producer")
    if any(token in source for token in ["root_crop", "rhizome", "corm", "tuber", "starch", "spice_rhizome", "medicinal_rhizome"]):
        roles.add("root_crop")
    if "leaf_crop" in source or "leaf vegetable" in source or "panc" in source:
        roles.add("leafy_green")
    if parse_bool((identity_row or {}).get("medicinal_flag", "")) or any(
        token in source for token in ["medicinal", "tea", "tincture", "extract", "tonic", "aromatic", "functional beverage"]
    ):
        roles.add("medicinal")
    if normalize_text((identity_row or {}).get("nitrogen_fixer_flag", "")) == "yes" or "agroforestry_nurse_tree" in source:
        roles.add("nitrogen_fixer")
    if any(token in source for token in ["pollinator_garden", "hummingbird_garden"]) or "hummingbird" in normalize_text((identity_row or {}).get("pollination_mode", "")):
        roles.add("pollinator_support")
    if primary_layer == "groundcover":
        roles.add("soil_cover")
    if primary_layer == "climber":
        roles.add("climber")
    if any(token in source for token in ["tree", "palm", "bamboo", "timber", "shade_tree", "screening", "structural", "ornamental_tree"]):
        roles.add("structural")
    if any(token in source for token in ["wetland", "floodplain"]) or "Pantanal" in biome_tags:
        roles.add("wetland_filter")
    if (
        "Caatinga" in biome_tags
        or "Coastal_Restinga" in biome_tags
        or "cactus" in source
        or "succulent" in source
    ) and normalize_text((identity_row or {}).get("drought_tolerance", "")) == "high":
        roles.add("xeric_support")

    if not roles:
        roles.add("structural" if primary_layer in {"canopy", "subcanopy", "shrub"} else "soil_cover")

    return [role for role in ROLE_PRIORITY if role in roles]


def role_to_guild_role(roles: list[str]) -> str:
    return roles[0] if roles else "unresolved"


def build_inclusion_rationale(biome_tags: list[str], biome_bases: list[str], identity_match: bool) -> str:
    if not biome_tags:
        return "biome_tags=unresolved; biome_basis=unresolved; normalization_pass=Brazil_FNP_2026-04-05"
    basis = "|".join(biome_bases) if biome_bases else "source_present"
    match_note = "identity_match" if identity_match else "master_zone_only"
    return (
        f"biome_tags={'|'.join(biome_tags)}; "
        f"biome_basis={basis}; "
        f"normalization_pass=Brazil_FNP_2026-04-05; "
        f"identity_source={match_note}"
    )


def build_zone_notes(existing_notes: str, biome_tags: list[str], biome_bases: list[str]) -> str:
    bits = []
    if (existing_notes or "").strip():
        bits.append((existing_notes or "").strip())
    bits.append(
        f"biome_tags={'|'.join(biome_tags) if biome_tags else 'unresolved'}; biome_basis={'|'.join(biome_bases) if biome_bases else 'unresolved'}; normalization_pass=Brazil_FNP_2026-04-05"
    )
    return " | ".join(bits)


def build_product_family_tags(master_row: dict[str, str]) -> str:
    tags = (master_row.get("Suggested_Product_Families", "") or "").strip()
    if tags:
        return tags
    return (master_row.get("Use Type", "") or "").strip()


def bool_from_master(value: str) -> str:
    text = normalize_text(value)
    if text in {"true", "yes", "1"}:
        return "TRUE"
    if text in {"false", "no", "0"}:
        return "FALSE"
    return ""


def derive_water_need(identity_row: dict[str, str] | None) -> str:
    if not identity_row:
        return "unresolved"
    drought = normalize_text(identity_row.get("drought_tolerance", ""))
    flood = normalize_text(identity_row.get("flood_tolerance", ""))
    waterlogging = normalize_text(identity_row.get("waterlogging_tolerance", ""))
    if flood in {"high", "medium"} or waterlogging in {"medium"}:
        return "high"
    if drought == "high":
        return "low"
    if drought in {"medium", "low to medium"}:
        return "medium"
    return "unresolved"


def derive_propagation_methods(identity_row: dict[str, str] | None) -> str:
    if not identity_row:
        return ""
    labels = {
        "propagation_seed": "seed",
        "propagation_cutting": "cutting",
        "propagation_graft": "graft",
        "propagation_division": "division",
        "propagation_tissue_culture": "tissue_culture",
    }
    methods = []
    for field, label in labels.items():
        value = normalize_text(identity_row.get(field, ""))
        if value == "yes":
            methods.append(label)
        elif value == "limited":
            methods.append(f"{label}_limited")
    return ";".join(methods)


def build_hons_row(botanical_id: str, master_row: dict[str, str]) -> dict[str, object]:
    return {
        "hons_overlay_id": f"HONS-{botanical_id}",
        "botanical_entry_id": botanical_id,
        "related_entity_id": "",
        "ownership_model": "unresolved",
        "rights_notes": "unresolved",
        "stage": "unresolved",
        "stage_status": "unresolved",
        "provenance_status": "source_workbook_backfilled",
        "rights_status": "unresolved",
        "branch_eligibility": "branch_brazil",
        "synergy_status": "unresolved",
        "node_relevance": "current_branch_botanical",
        "experimental_policy": "unresolved",
        "release_policy": "delta_only",
        "public_publish_status": "internal_audit",
        "attribution": "Brazil source workbooks",
        "governance_notes": "FNP populated explicit unresolved governance statuses because no row-level HONS source fields exist in the current Brazil workbooks.",
        "source_table": "Botanicals_Master",
        "source_row": master_row.get("__source_row", ""),
    }


def main() -> None:
    brazil_sheets = read_xlsx(BRAZIL_TABLES_XLSX)
    identity_rows = read_xlsx(IDENTITY_XLSX)["IDENTITY_BRAZIL_BLOCK1"]
    master_rows = brazil_sheets["Botanicals_Master"]
    working_rows = brazil_sheets["Brazil_Working_Master"]

    identity_by_sci = {
        normalize_text(row.get("accepted_name", "")): row
        for row in identity_rows
        if normalize_text(row.get("accepted_name", ""))
    }

    working_by_botanical_id: dict[str, list[dict[str, str]]] = {}
    for row in working_rows:
        botanical_id = (row.get("Botanical_ID", "") or "").strip()
        if botanical_id:
            working_by_botanical_id.setdefault(botanical_id, []).append(row)

    identity_backfill = []
    zone_backfill = []
    design_rows = []
    root_rows = []
    symbiosis_rows = []
    product_path_rows = []
    hons_rows = []

    unresolved = {
        "identity_workbook_unmatched": [],
        "biome_unresolved": [],
        "root_partial": [],
        "symbiosis_partial": [],
        "hons_unresolved": [],
    }

    species_with_biome_tags = 0
    species_with_design_matrix = 0
    species_with_roles = 0
    atlantic_identity_ids = set()
    atlantic_operational_ids = set()
    identity_biome_counts = Counter()
    operational_biome_counts = Counter()
    layer_counts = Counter()

    for master in master_rows:
        botanical_id = (master.get("Botanical_ID", "") or "").strip()
        sci_name = (master.get("Scientific Name", "") or "").strip()
        identity = identity_by_sci.get(normalize_text(sci_name))
        zone_group = working_by_botanical_id.get(botanical_id, [])

        if not identity:
            unresolved["identity_workbook_unmatched"].append(
                {
                    "botanical_entry_id": botanical_id,
                    "botanical_name": master.get("Botanical Name", ""),
                    "scientific_name": sci_name,
                }
            )

        biome_tags, biome_bases = normalize_biomes(
            master.get("Brazil Biomes", ""),
            master.get("Brazil Climate Group", ""),
            master.get("Brazil Zone Group", ""),
            master.get("Brazil Macroregions", ""),
            *(zone.get("Brazil Biomes", "") for zone in zone_group),
            *(zone.get("BR_Zone_Single", "") for zone in zone_group),
            *(zone.get("Microclimate Tags", "") for zone in zone_group),
            *(identity.get(field, "") for field in ["primary_biome", "secondary_biome", "phytogeographic_domains"])
            if identity
            else (),
        )
        if biome_tags:
            species_with_biome_tags += 1
        else:
            unresolved["biome_unresolved"].append(botanical_id)

        common_name_en = zone_group[0].get("Common Name (EN)", "") if zone_group else ""
        common_name_pt = zone_group[0].get("Common Name (PT)", "") if zone_group else ""
        alternative_names = zone_group[0].get("Alternative Names", "") if zone_group else ""

        temp_min, temp_max = parse_temp_band((identity or {}).get("temperature_band_c", ""))
        food_forest_layer, primary_layer, secondary_layer, layer_stack_tags = derive_layers(master, identity, [])
        roles = derive_roles(master, identity, primary_layer, biome_tags)
        food_forest_layer, primary_layer, secondary_layer, layer_stack_tags = derive_layers(master, identity, roles)
        guild_role = role_to_guild_role(roles)

        if roles:
            species_with_roles += 1
        if food_forest_layer and primary_layer and layer_stack_tags and guild_role:
            species_with_design_matrix += 1
        if "Atlantic_Forest" in biome_tags:
            atlantic_identity_ids.add(botanical_id)
        for tag in biome_tags:
            identity_biome_counts[tag] += 1
        layer_counts[primary_layer] += 1

        completion_fields = [
            common_name_pt,
            common_name_en or (identity or {}).get("common_name_en", ""),
            sci_name,
            master.get("Variety / Cultivar", ""),
            "|".join(biome_tags),
            primary_layer,
            "|".join(roles),
            (identity or {}).get("mature_height_m_min", ""),
            (identity or {}).get("mature_height_m_max", ""),
            (identity or {}).get("source_url_primary", "") or master.get("Primary Source URL", ""),
            (identity or {}).get("confidence_score", ""),
        ]
        fields_completed_count = len([item for item in completion_fields if str(item).strip()])
        record_completeness_score = round(fields_completed_count / len(completion_fields), 3)

        identity_backfill.append(
            {
                "botanical_entry_id": botanical_id,
                "common_name_pt": common_name_pt or master.get("Botanical Name", ""),
                "common_name_en": common_name_en or (identity or {}).get("common_name_en", ""),
                "scientific_name": sci_name,
                "variety_cultivar": master.get("Variety / Cultivar", ""),
                "alternative_names": alternative_names,
                "plant_type": master.get("Plant Type", ""),
                "heritage_flag": to_bool_token((identity or {}).get("heritage_flag", "")),
                "medicinal_flag": to_bool_token((identity or {}).get("medicinal_flag", "")),
                "inclusion_rationale": build_inclusion_rationale(biome_tags, biome_bases, bool(identity)),
                "mature_height_m_min": (identity or {}).get("mature_height_m_min", ""),
                "mature_height_m_max": (identity or {}).get("mature_height_m_max", ""),
                "mature_spread_m_min": (identity or {}).get("mature_spread_m_min", ""),
                "mature_spread_m_max": (identity or {}).get("mature_spread_m_max", ""),
                "data_confidence_level": score_to_confidence_level((identity or {}).get("confidence_score", "")),
                "data_source_type": "Brazil_Workbooks_FNP",
                "record_completeness_score": record_completeness_score,
                "fields_completed_count": fields_completed_count,
                "system_roles": ";".join(roles),
                "invasiveness_risk_level": (identity or {}).get("invasive_risk_brazil", ""),
                "spread_control_required": "TRUE"
                if normalize_text((identity or {}).get("invasive_risk_brazil", "")) in {"medium", "high"}
                else "FALSE"
                if (identity or {}).get("invasive_risk_brazil", "")
                else "",
                "min_temp_c": "" if temp_min is None else temp_min,
                "max_temp_c": "" if temp_max is None else temp_max,
                "drought_tolerance": (identity or {}).get("drought_tolerance", ""),
                "frost_tolerance": (identity or {}).get("frost_tolerance", ""),
                "endemic_to_brazil": to_bool_token((identity or {}).get("endemic_to_brazil", "")),
                "conservation_flag": (identity or {}).get("conservation_flag", "") or master.get("Conservation Status", ""),
                "invasive_risk_brazil": (identity or {}).get("invasive_risk_brazil", ""),
                "source_url_primary": (identity or {}).get("source_url_primary", "") or master.get("Primary Source URL", ""),
                "source_url_secondary": (identity or {}).get("source_url_secondary", "") or master.get("Taxonomy Source URL", ""),
                "source_url_tertiary": (identity or {}).get("source_url_tertiary", "") or master.get("Conservation Source URL", ""),
                "confidence_score": (identity or {}).get("confidence_score", ""),
                "confidence_notes": (identity or {}).get("confidence_notes", ""),
                "source_table": "Botanicals_Master",
                "source_row": master.get("__source_row", ""),
            }
        )

        design_rows.append(
            {
                "design_matrix_id": f"SDM-{botanical_id}",
                "botanical_entry_id": botanical_id,
                "food_forest_layer": food_forest_layer,
                "canonical_layer_primary": primary_layer,
                "canonical_layer_secondary": secondary_layer,
                "layer_stack_tags": layer_stack_tags,
                "guild_role": guild_role,
                "shade_tolerance": (identity or {}).get("shade_tolerance", ""),
                "water_need": derive_water_need(identity),
                "companion_tags": ";".join(role for role in roles if role in {"pollinator_support", "nitrogen_fixer", "soil_cover", "wetland_filter", "xeric_support"}),
                "notes": build_inclusion_rationale(biome_tags, biome_bases, bool(identity)),
                "source_table": "Botanicals_Master",
                "source_row": master.get("__source_row", ""),
            }
        )

        root_rows.append(
            {
                "root_profile_id": f"ROOT-{botanical_id}",
                "botanical_entry_id": botanical_id,
                "root_form": (identity or {}).get("root_architecture", ""),
                "root_depth_class": (identity or {}).get("root_depth_class", ""),
                "root_spread_class": (identity or {}).get("root_spread_class", ""),
                "root_aggression": (identity or {}).get("root_aggression_risk", ""),
                "root_depth_min_m": "",
                "root_depth_max_m": "",
                "root_architecture_type": (identity or {}).get("root_architecture", ""),
                "root_depth_category": (identity or {}).get("root_depth_class", ""),
                "excavation_sensitivity": "",
                "root_competition_intensity": "",
                "container_root_behavior": "",
                "waterlogging_tolerance": (identity or {}).get("waterlogging_tolerance", ""),
                "notes": "root_depth_min_m_unresolved;root_depth_max_m_unresolved;excavation_sensitivity_unresolved;root_competition_intensity_unresolved;container_root_behavior_unresolved"
                + (";identity_workbook_unmatched" if not identity else ""),
                "source_table": "IDENTITY_BRAZIL_BLOCK1" if identity else "Botanicals_Master",
                "source_row": (identity or {}).get("__source_row", "") or master.get("__source_row", ""),
            }
        )
        unresolved["root_partial"].append(botanical_id)

        nitrogen_fix = normalize_text((identity or {}).get("nitrogen_fixer_flag", ""))
        myco = (identity or {}).get("mycorrhizae_flag", "")
        sym_types = []
        sym_tags = []
        if nitrogen_fix == "yes":
            sym_types.append("nitrogen_fixation")
            sym_tags.append("nitrogen_fixer")
        if normalize_text(myco) not in {"", "no"}:
            sym_types.append("mycorrhizal_association")
            sym_tags.append("mycorrhizae")
        if normalize_text((identity or {}).get("primary_use_class", "")) == "agroforestry_nurse_tree":
            sym_tags.append("nurse_plant")
        if not sym_types:
            sym_types.append("unresolved")
        symbiosis_rows.append(
            {
                "symbiosis_profile_id": f"SYM-{botanical_id}",
                "botanical_entry_id": botanical_id,
                "symbiosis_type": ";".join(sym_types),
                "symbiotic_partner_type": "soil_microbe" if sym_types != ["unresolved"] else "",
                "symbiotic_partner_botanical_id": "",
                "mycorrhizal_association_type": myco,
                "nitrogen_fixing_flag": "TRUE" if nitrogen_fix == "yes" else "FALSE" if nitrogen_fix == "no" else "",
                "host_dependency_flag": "",
                "nurse_plant_flag": "TRUE"
                if normalize_text((identity or {}).get("primary_use_class", "")) == "agroforestry_nurse_tree"
                else "FALSE"
                if identity
                else "",
                "rhizosphere_benefit_notes": (identity or {}).get("symbiosis_detail", ""),
                "symbiosis_strength": myco or "unresolved",
                "symbiosis_confidence": score_to_confidence_level((identity or {}).get("confidence_score", "")) if identity else "unresolved",
                "symbiotic_role_tags": ";".join(sym_tags) if sym_tags else "unresolved",
                "notes": "identity_workbook_unmatched" if not identity else "",
                "source_table": "IDENTITY_BRAZIL_BLOCK1" if identity else "Botanicals_Master",
                "source_row": (identity or {}).get("__source_row", "") or master.get("__source_row", ""),
            }
        )
        if not identity:
            unresolved["symbiosis_partial"].append(botanical_id)

        product_path_rows.append(
            {
                "product_path_id": f"BPP-{botanical_id}",
                "botanical_entry_id": botanical_id,
                "product_family_tags": build_product_family_tags(master),
                "product_angle_notes": master.get("Top Product Opportunity (Rollup Suggested)", "") or master.get("Use Type", ""),
                "kombucha_1f_friendly": bool_from_master(master.get("Can_Kombucha_1F_Product", "")),
                "bitters_friendly": bool_from_master(master.get("Can_Bitters_or_Tincture", "")),
                "cordial_friendly": bool_from_master(master.get("Can_Cordial_or_Syrup", "")),
                "tea_friendly": bool_from_master(master.get("Can_Tea_or_Tisane", "")),
                "fresh_produce_friendly": bool_from_master(master.get("Can_Fresh_Produce", "")),
                "preserve_friendly": bool_from_master(master.get("Can_Preserve_or_Jam", "")),
                "cosmetic_friendly": bool_from_master(master.get("Can_Oil_or_Cosmetic", "")),
                "edible_flower_friendly": "TRUE"
                if "flower_use" in normalize_text((identity or {}).get("secondary_use_class", "")) and "fresh market" in normalize_text(master.get("Use Type", ""))
                else "",
                "cut_flower_friendly": "TRUE"
                if "cut_flower" in normalize_text((identity or {}).get("secondary_use_class", ""))
                else "",
                "medicinal_flower_friendly": "TRUE"
                if "flower_use" in normalize_text((identity or {}).get("secondary_use_class", "")) and "medicinal" in normalize_text(master.get("Use Type", ""))
                else "",
                "petal_flavour_friendly": "",
                "dried_floral_friendly": "TRUE"
                if "fragrant_flower" in normalize_text((identity or {}).get("secondary_use_class", ""))
                else "",
                "source_table": "Botanicals_Master",
                "source_row": master.get("__source_row", ""),
            }
        )

        hons_rows.append(build_hons_row(botanical_id, master))
        unresolved["hons_unresolved"].append(botanical_id)

        for zone in zone_group:
            zone_biomes, zone_bases = normalize_biomes(
                zone.get("Brazil Biomes", ""),
                zone.get("BR_Zone_Single", ""),
                zone.get("Microclimate Tags", ""),
                zone.get("Brazil Climate Group", ""),
            )
            if not zone_biomes:
                zone_biomes = biome_tags
                zone_bases = biome_bases
            if "Atlantic_Forest" in zone_biomes:
                atlantic_operational_ids.add(zone.get("Working Master Record ID", ""))
            for tag in zone_biomes:
                operational_biome_counts[tag] += 1
            zone_backfill.append(
                {
                    "zone_profile_id": zone.get("Working Master Record ID", ""),
                    "botanical_entry_id": botanical_id,
                    "branch_id": "branch_brazil",
                    "country": "Brazil",
                    "region": zone.get("BR_Macroregion_Single", ""),
                    "zone": zone.get("BR_Zone_Single", ""),
                    "microclimate_tags": zone.get("Microclimate Tags", ""),
                    "production_mode": zone.get("Production_Mode", ""),
                    "growth_habit": master.get("Plant Type", ""),
                    "forest_garden_layer": food_forest_layer,
                    "guild_roles": ";".join(roles),
                    "light_preference": (identity or {}).get("light_preference", ""),
                    "flood_tolerance": (identity or {}).get("flood_tolerance", ""),
                    "salinity_tolerance": (identity or {}).get("salinity_tolerance", ""),
                    "heat_tolerance": (identity or {}).get("heat_tolerance", ""),
                    "fire_tolerance": (identity or {}).get("fire_tolerance", ""),
                    "harvest_window_brazil": (identity or {}).get("harvest_window_brazil", ""),
                    "propagation_methods": derive_propagation_methods(identity),
                    "conservation_status": (identity or {}).get("conservation_flag", "") or zone.get("Conservation Status", ""),
                    "notes": build_zone_notes(zone.get("Regional_Data_Notes", "") or zone.get("Notes", ""), zone_biomes, zone_bases),
                    "source_table": "Brazil_Working_Master",
                    "source_row": zone.get("__source_row", ""),
                }
            )

    manifest = {
        "generated_at": "2026-04-05",
        "source_files": {
            "brazil_tables": str(BRAZIL_TABLES_XLSX),
            "identity_workbook": str(IDENTITY_XLSX),
        },
        "counts": {
            "botanical_entries_master_backfill": len(identity_backfill),
            "botanical_zone_profiles_backfill": len(zone_backfill),
            "species_design_matrix_backfill": len(design_rows),
            "species_root_profile_backfill": len(root_rows),
            "species_symbiosis_profile_backfill": len(symbiosis_rows),
            "botanical_product_paths_backfill": len(product_path_rows),
            "hons_overlay_backfill": len(hons_rows),
            "rows_updated_total": len(identity_backfill)
            + len(zone_backfill)
            + len(design_rows)
            + len(root_rows)
            + len(symbiosis_rows)
            + len(product_path_rows)
            + len(hons_rows),
            "species_with_biome_tags_added": species_with_biome_tags,
            "species_with_design_matrix_completed": species_with_design_matrix,
            "species_with_roles_normalized": species_with_roles,
            "atlantic_forest_identity_count": len(atlantic_identity_ids),
            "atlantic_forest_operational_count": len(atlantic_operational_ids),
        },
        "exact_identity_biome_counts": dict(identity_biome_counts),
        "exact_operational_biome_counts": dict(operational_biome_counts),
        "exact_primary_layer_counts": dict(layer_counts),
        "unresolved": unresolved,
        "notes": [
            "Biome tags were normalized into botanical_entries_master.inclusion_rationale because the frozen schema has no dedicated identity-biome tag column.",
            "Operational biome tags were normalized into botanical_zone_profiles.notes for exact reproducible operational biome counts without adding columns.",
            "HONS rows were populated with explicit unresolved statuses where no row-level governance source exists in the current Brazil workbooks.",
        ],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUT_DIR / "botanical_entries_master_fnp_backfill.csv",
        identity_backfill,
        [
            "botanical_entry_id",
            "common_name_pt",
            "common_name_en",
            "scientific_name",
            "variety_cultivar",
            "alternative_names",
            "plant_type",
            "heritage_flag",
            "medicinal_flag",
            "inclusion_rationale",
            "mature_height_m_min",
            "mature_height_m_max",
            "mature_spread_m_min",
            "mature_spread_m_max",
            "data_confidence_level",
            "data_source_type",
            "record_completeness_score",
            "fields_completed_count",
            "system_roles",
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
            "source_table",
            "source_row",
        ],
    )
    write_csv(
        OUT_DIR / "botanical_zone_profiles_fnp_backfill.csv",
        zone_backfill,
        [
            "zone_profile_id",
            "botanical_entry_id",
            "branch_id",
            "country",
            "region",
            "zone",
            "microclimate_tags",
            "production_mode",
            "growth_habit",
            "forest_garden_layer",
            "guild_roles",
            "light_preference",
            "flood_tolerance",
            "salinity_tolerance",
            "heat_tolerance",
            "fire_tolerance",
            "harvest_window_brazil",
            "propagation_methods",
            "conservation_status",
            "notes",
            "source_table",
            "source_row",
        ],
    )
    write_csv(
        OUT_DIR / "species_design_matrix_fnp_seed.csv",
        design_rows,
        [
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
        ],
    )
    write_csv(
        OUT_DIR / "species_root_profile_fnp_seed.csv",
        root_rows,
        [
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
        ],
    )
    write_csv(
        OUT_DIR / "species_symbiosis_profile_fnp_seed.csv",
        symbiosis_rows,
        [
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
        ],
    )
    write_csv(
        OUT_DIR / "botanical_product_paths_fnp_seed.csv",
        product_path_rows,
        [
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
        ],
    )
    write_csv(
        OUT_DIR / "hons_overlay_fnp_seed.csv",
        hons_rows,
        [
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
        ],
    )
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
