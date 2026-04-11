import csv
import json
import re
import shutil
import tempfile
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(r"c:\Code\CursorBridge")
BRAZIL_XLSX = Path(
    r"c:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\brazil_data_tables_only.xlsx"
)
UK_ZIP = Path(
    r"c:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\Botanical list_Kombucha_Friendly.zip"
)
OUT_DIR = ROOT / "exports" / "botanicals_master_union" / "latest"

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def normalize_text(value: str) -> str:
    value = (value or "").strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.replace("&", " and ")
    value = re.sub(r"[\(\)\[\]\{\}/,.;:+]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def normalize_key(value: str) -> str:
    value = normalize_text(value)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def truthy(value: str) -> bool:
    return normalize_text(value) in {"1", "true", "yes", "y"}


def col_to_index(col: str) -> int:
    value = 0
    for ch in col:
        value = value * 26 + (ord(ch) - 64)
    return value - 1


def index_to_col(index: int) -> str:
    index += 1
    out = ""
    while index:
        index, rem = divmod(index - 1, 26)
        out = chr(65 + rem) + out
    return out


def workbook_target_path(target: str) -> str:
    target = target.lstrip("/")
    if not target.startswith("xl/"):
        target = "xl/" + target.replace("../", "")
    return target


def read_xlsx(path: Path) -> dict[str, list[dict[str, str]]]:
    with zipfile.ZipFile(path) as zf:
        shared_strings = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared_strings.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))

        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}

        def cell_value(cell):
            kind = cell.attrib.get("t")
            if kind == "s":
                v = cell.find("m:v", NS)
                return shared_strings[int(v.text)] if v is not None else ""
            if kind == "inlineStr":
                return "".join(t.text or "" for t in cell.findall(".//m:t", NS))
            v = cell.find("m:v", NS)
            return v.text if v is not None else ""

        sheets = {}
        for sheet in wb.find("m:sheets", NS):
            sheet_name = sheet.attrib["name"]
            rid = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            root = ET.fromstring(zf.read(workbook_target_path(rel_map[rid])))

            rows = []
            for row in root.findall(".//m:sheetData/m:row", NS):
                values = {}
                for cell in row.findall("m:c", NS):
                    col = re.match(r"[A-Z]+", cell.attrib["r"]).group(0)
                    values[col] = cell_value(cell)
                rows.append(values)

            if not rows:
                sheets[sheet_name] = []
                continue

            header_row = rows[0]
            max_col = max(header_row.keys(), key=lambda item: (len(item), item))
            headers = [header_row.get(index_to_col(idx), "").strip() for idx in range(col_to_index(max_col) + 1)]

            records = []
            for source_row_idx, row in enumerate(rows[1:], start=2):
                record = {"__source_row": str(source_row_idx)}
                for idx, header in enumerate(headers):
                    if header:
                        record[header] = row.get(index_to_col(idx), "")
                records.append(record)
            sheets[sheet_name] = records
        return sheets


def read_uk_csv(path: Path) -> list[dict[str, str]]:
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(path) as outer:
            inner_name = [name for name in outer.namelist() if name.lower().endswith(".zip")][0]
            inner_path = Path(td) / "inner.zip"
            inner_path.write_bytes(outer.read(inner_name))
        with zipfile.ZipFile(inner_path) as inner:
            target = [name for name in inner.namelist() if name.lower().endswith("_all.csv")][0]
            data = inner.read(target).decode("utf-8-sig", errors="replace").splitlines()
            reader = csv.DictReader(data)
            rows = []
            for idx, row in enumerate(reader, start=2):
                clean = {"__source_row": str(idx)}
                clean.update({key: value or "" for key, value in row.items()})
                rows.append(clean)
            return rows


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def derive_duplicate_fields(rows: list[dict[str, object]]) -> None:
    groups = Counter(normalize_key(str(row.get("botanical_name", ""))) for row in rows)
    for row in rows:
        group = normalize_key(str(row.get("botanical_name", "")))
        row["duplicate_name_group"] = group
        row["duplicate_name_count"] = groups[group]


def uk_to_master_row(row: dict[str, str], uk_index: int) -> dict[str, object]:
    use_type = row.get("Use Type", "")
    return {
        "botanical_entry_id": f"BOT-UK-{uk_index:04d}",
        "botanical_name": row.get("Botanical Name", ""),
        "part_used": row.get("Part Used", ""),
        "season": row.get("Season", ""),
        "ferment_safety": row.get("Ferment Safety", ""),
        "use_type": use_type,
        "functions": row.get("Functions", ""),
        "form_in_system": row.get("Form in System", ""),
        "micronutrients": row.get("Micronutrients", ""),
        "notes": row.get("Notes", ""),
        "ayurvedic_profile": row.get("Ayurvedic Profile", ""),
        "tcm_meridians": row.get("TCM Meridians", ""),
        "tcm_nature_flavour": row.get("TCM Nature & Flavour", ""),
        "archetype_animal": row.get("Archetype / Animal", ""),
        "scientific_actions": row.get("Scientific Actions", ""),
        "synergy_tags": row.get("Synergy Tags", ""),
        "element_planet": row.get("Element / Planet", ""),
        "permaculture_guild": row.get("Permaculture / Guild", ""),
        "biodynamic_timing": row.get("Biodynamic Timing", ""),
        "soil_type": row.get("Soil Type", ""),
        "growing_conditions": row.get("Growing Conditions", ""),
        "foraging_habitat": row.get("Foraging Habitat", ""),
        "kombucha_1f_friendly_flag": normalize_text(row.get("Ferment Safety", "")) == "primary ok",
        "tea_friendly_flag": "tea" in normalize_text(use_type),
        "bitters_friendly_flag": "bitter" in normalize_text(use_type),
        "cordial_friendly_flag": "cordial" in normalize_text(use_type) or "syrup" in normalize_text(use_type),
        "fresh_produce_friendly_flag": "fruit" in normalize_text(use_type) or "culinary" in normalize_text(use_type),
        "preserve_friendly_flag": "preserve" in normalize_text(use_type) or "jam" in normalize_text(use_type),
        "cosmetic_friendly_flag": "cosmetic" in normalize_text(use_type),
        "source_table": "Botanical list (kombucha friendly)",
        "source_row": row.get("__source_row", ""),
    }


def brazil_to_master_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "botanical_entry_id": row.get("Botanical_ID", ""),
        "botanical_name": row.get("Botanical Name", ""),
        "part_used": row.get("Part Used", ""),
        "season": row.get("Season", ""),
        "ferment_safety": row.get("Ferment Safety", ""),
        "use_type": row.get("Use Type", ""),
        "functions": row.get("Functions", ""),
        "form_in_system": row.get("Form in System", ""),
        "micronutrients": row.get("Micronutrients", ""),
        "notes": row.get("Notes", ""),
        "ayurvedic_profile": row.get("Ayurvedic Profile", ""),
        "tcm_meridians": row.get("TCM Meridians", ""),
        "tcm_nature_flavour": row.get("TCM Nature & Flavour", ""),
        "archetype_animal": row.get("Archetype / Animal", ""),
        "scientific_actions": row.get("Scientific Actions", ""),
        "synergy_tags": row.get("Synergy Tags", ""),
        "element_planet": row.get("Element / Planet", ""),
        "permaculture_guild": row.get("Permaculture / Guild", ""),
        "biodynamic_timing": row.get("Biodynamic Timing", ""),
        "soil_type": row.get("Soil Type", ""),
        "growing_conditions": row.get("Growing Conditions", ""),
        "foraging_habitat": row.get("Foraging Habitat", ""),
        "kombucha_1f_friendly_flag": truthy(row.get("Can_Kombucha_1F_Product", "")) or truthy(row.get("Kombucha 1F", "")),
        "tea_friendly_flag": truthy(row.get("Can_Tea_or_Tisane", "")),
        "bitters_friendly_flag": truthy(row.get("Can_Bitters_or_Tincture", "")),
        "cordial_friendly_flag": truthy(row.get("Can_Cordial_or_Syrup", "")),
        "fresh_produce_friendly_flag": truthy(row.get("Can_Fresh_Produce", "")),
        "preserve_friendly_flag": truthy(row.get("Can_Preserve_or_Jam", "")),
        "cosmetic_friendly_flag": truthy(row.get("Can_Oil_or_Cosmetic", "")),
        "source_table": "Botanicals_Master",
        "source_row": row.get("__source_row", ""),
    }


def build_harvest_window(row: dict[str, str]) -> str:
    chunks = []
    for slot in ("1", "2"):
        start = row.get(f"Harvest_Window_{slot}_Start", "")
        end = row.get(f"Harvest_Window_{slot}_End", "")
        peak_start = row.get(f"Harvest_Window_{slot}_Peak_Start", "")
        peak_end = row.get(f"Harvest_Window_{slot}_Peak_End", "")
        if start or end:
            part = f"{start}-{end}".strip("-")
            if peak_start or peak_end:
                part = f"{part} peak {peak_start}-{peak_end}".strip()
            chunks.append(part)
    return "; ".join(item for item in chunks if item)


def brazil_to_zone_row(row: dict[str, str]) -> dict[str, object]:
    common_names = "; ".join(
        item for item in [row.get("Common Name (PT)", ""), row.get("Common Name (EN)", ""), row.get("Alternative Names", "")] if item
    )
    botanical_id = row.get("Botanical_ID", "") or row.get("Botanical Entry ID", "")
    return {
        "zone_profile_id": row.get("Working Master Record ID", ""),
        "botanical_entry_id": botanical_id,
        "match_status": "matched_source_id",
        "match_candidates": f"{botanical_id}:{row.get('Botanical Name', '')}",
        "botanical_link": row.get("Botanical Name", ""),
        "common_names": common_names,
        "growth_habit": row.get("Plant Type", ""),
        "forest_garden_layer": "",
        "lifespan": "",
        "native_region": "Brazil",
        "climate_band_prefers": row.get("Brazil Climate Group", ""),
        "hardiness_class": "",
        "outdoor_suitability": row.get("Brazil Status", ""),
        "greenhouse_zone": "",
        "indoor_container_use": "",
        "soil_type": row.get("Soil Type", ""),
        "soil_moisture": "",
        "soil_functions": "",
        "sun_exposure": row.get("Growing Conditions", ""),
        "humidity_preference": "",
        "root_depth_type": "",
        "spread_pattern": "",
        "companion_plants": "",
        "incompatible_with": "",
        "guild_roles": row.get("Permaculture / Guild", ""),
        "foraging_habitat": row.get("Foraging Habitat", ""),
        "harvest_window": build_harvest_window(row),
        "planting_sowing_window": "",
        "yield_regrowth": "",
        "propagation_methods": "",
        "conservation_status": row.get("Conservation Status", ""),
        "foraging_cautions": "",
        "wildlife_supported": "",
        "notes": row.get("Regional_Data_Notes", "") or row.get("Notes", ""),
        "branch_id": "branch_brazil",
        "country": "Brazil",
        "region": row.get("BR_Macroregion_Single", ""),
        "zone": row.get("BR_Zone_Single", ""),
        "microclimate_tags": row.get("Microclimate Tags", ""),
        "production_mode": row.get("Production_Mode", ""),
        "source_table": "Brazil_Working_Master",
        "source_row": row.get("__source_row", ""),
    }


def brazil_to_product_row(row: dict[str, str]) -> dict[str, object]:
    notes = []
    for label in ["Evidence Basis", "Processing Type", "Suggested Packaging / Form", "Primary Source URL", "Notes"]:
        value = row.get(label, "")
        if value:
            notes.append(f"{label}: {value}")
    return {
        "product_id": row.get("Product_ID", ""),
        "product_name": row.get("Product Record", ""),
        "catalogue_line_guess": row.get("Product Family", ""),
        "fermentation_family_guess": "",
        "format_label": row.get("Product Type", ""),
        "function_label": row.get("Suggested Positioning", ""),
        "core_base": row.get("Primary Botanical Name", ""),
        "protocols_used": "",
        "botanicals_used": row.get("Primary Botanical Name", ""),
        "live_status": "",
        "intended_use": row.get("Suggested Positioning", ""),
        "strength_level": row.get("Evidence Level", ""),
        "shelf_stability": "",
        "development_status": row.get("Product Status", ""),
        "notes": " | ".join(notes),
        "source_table": "Products",
        "source_row": row.get("__source_row", ""),
    }


def brazil_to_product_botanical_row(row: dict[str, str], products_by_id: dict[str, dict[str, str]]) -> dict[str, object]:
    product = products_by_id.get(row.get("Product_ID", ""), {})
    botanical_name = row.get("Primary Botanical Name", "")
    botanical_id = row.get("Botanical_ID", "")
    return {
        "product_id": row.get("Product_ID", ""),
        "product_name": product.get("Product Record", "") or row.get("Product Record", ""),
        "ingredient_label": botanical_name,
        "ingredient_kind": row.get("Role in Product", "") or "primary_botanical",
        "botanical_entry_id": botanical_id,
        "matched_botanical_name": botanical_name,
        "match_status": "matched_source_id" if botanical_id else "missing_botanical_id",
        "candidate_matches": f"{botanical_id}:{botanical_name}" if botanical_id else "",
        "resolution_needed": not bool(botanical_id),
    }


def relation_mapping_rows(
    brazil_counts: dict[str, int], uk_count: int, overlap_count: int, output_counts: dict[str, int]
) -> list[dict[str, object]]:
    return [
        {
            "source_stack": "Brazil workbook",
            "source_table": "Botanicals_Master",
            "source_key": "Botanical_ID",
            "relation_type": "primary_load",
            "target_table": "botanical_entries_master",
            "target_key": "botanical_entry_id",
            "row_count": brazil_counts["Botanicals_Master"],
            "notes": "Primary botanical truth layer from Brazil source.",
        },
        {
            "source_stack": "Brazil workbook",
            "source_table": "Brazil_Working_Master",
            "source_key": "Working Master Record ID",
            "relation_type": "many_to_one",
            "target_table": "botanical_zone_profiles",
            "target_key": "zone_profile_id",
            "row_count": brazil_counts["Brazil_Working_Master"],
            "notes": "Join to botanical_entries_master on Botanical_ID. Multiple regional rows per botanical.",
        },
        {
            "source_stack": "Brazil workbook",
            "source_table": "Products",
            "source_key": "Product_ID",
            "relation_type": "primary_load",
            "target_table": "product_catalogue",
            "target_key": "product_id",
            "row_count": brazil_counts["Products"],
            "notes": "Primary Brazil product catalogue load.",
        },
        {
            "source_stack": "Brazil workbook",
            "source_table": "Products",
            "source_key": "Primary Botanical ID",
            "relation_type": "many_to_one",
            "target_table": "botanical_entries_master",
            "target_key": "botanical_entry_id",
            "row_count": brazil_counts["Products"],
            "notes": "Product primary botanical relation.",
        },
        {
            "source_stack": "Brazil workbook",
            "source_table": "Product_Botanical_Links",
            "source_key": "Link_ID",
            "relation_type": "bridge_table",
            "target_table": "product_botanical_links",
            "target_key": "product_id + ingredient_label",
            "row_count": brazil_counts["Product_Botanical_Links"],
            "notes": "Explicit product to botanical link layer.",
        },
        {
            "source_stack": "UK export",
            "source_table": "Botanical list (kombucha friendly)",
            "source_key": "generated BOT-UK ids",
            "relation_type": "secondary_union_load",
            "target_table": "botanical_entries_master",
            "target_key": "botanical_entry_id",
            "row_count": uk_count,
            "notes": "Secondary botanical source unioned into master without replacing Brazil rows.",
        },
        {
            "source_stack": "Cross-source",
            "source_table": "Brazil + UK overlap scan",
            "source_key": "normalized botanical_name",
            "relation_type": "soft_match_registry",
            "target_table": "botanical_overlap_mapping",
            "target_key": "uk_botanical_entry_id + brazil_botanical_entry_id",
            "row_count": overlap_count,
            "notes": "Overlap is flagged, not collapsed.",
        },
        {
            "source_stack": "Output bundle",
            "source_table": "master union outputs",
            "source_key": "generated CSVs",
            "relation_type": "ready_for_load",
            "target_table": "exports/botanicals_master_union/latest",
            "target_key": "file set",
            "row_count": sum(output_counts.values()),
            "notes": json.dumps(output_counts, ensure_ascii=True),
        },
    ]


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    brazil = read_xlsx(BRAZIL_XLSX)
    uk_rows = read_uk_csv(UK_ZIP)

    brazil_master_rows = [brazil_to_master_row(row) for row in brazil["Botanicals_Master"]]
    uk_master_rows = [uk_to_master_row(row, idx) for idx, row in enumerate(uk_rows, start=1)]
    botanical_master_rows = brazil_master_rows + uk_master_rows
    derive_duplicate_fields(botanical_master_rows)

    brazil_zone_rows = [brazil_to_zone_row(row) for row in brazil["Brazil_Working_Master"]]
    products_by_id = {row.get("Product_ID", ""): row for row in brazil["Products"]}
    product_rows = [brazil_to_product_row(row) for row in brazil["Products"]]
    product_botanical_rows = [
        brazil_to_product_botanical_row(row, products_by_id) for row in brazil["Product_Botanical_Links"]
    ]

    raw_uk_rows = []
    for row in uk_rows:
        raw_uk_rows.append(
            {
                "source_row": row.get("__source_row", ""),
                "botanical_name": row.get("Botanical Name", ""),
                "part_used": row.get("Part Used", ""),
                "season": row.get("Season", ""),
                "ferment_safety": row.get("Ferment Safety", ""),
                "use_type": row.get("Use Type", ""),
                "functions": row.get("Functions", ""),
                "form_in_system": row.get("Form in System", ""),
                "micronutrients": row.get("Micronutrients", ""),
                "notes": row.get("Notes", ""),
                "ayurvedic_profile": row.get("Ayurvedic Profile", ""),
                "tcm_meridians": row.get("TCM Meridians", ""),
                "tcm_nature_flavour": row.get("TCM Nature & Flavour", ""),
                "archetype_animal": row.get("Archetype / Animal", ""),
                "scientific_actions": row.get("Scientific Actions", ""),
                "synergy_tags": row.get("Synergy Tags", ""),
                "element_planet": row.get("Element / Planet", ""),
                "permaculture_guild": row.get("Permaculture / Guild", ""),
                "biodynamic_timing": row.get("Biodynamic Timing", ""),
                "soil_type": row.get("Soil Type", ""),
                "growing_conditions": row.get("Growing Conditions", ""),
                "foraging_habitat": row.get("Foraging Habitat", ""),
            }
        )

    overlaps = []
    brazil_by_name = defaultdict(list)
    for row in brazil_master_rows:
        brazil_by_name[normalize_key(str(row["botanical_name"]))].append(row)
    for row in uk_master_rows:
        matches = brazil_by_name.get(normalize_key(str(row["botanical_name"])), [])
        for match in matches:
            overlaps.append(
                {
                    "uk_botanical_entry_id": row["botanical_entry_id"],
                    "uk_botanical_name": row["botanical_name"],
                    "brazil_botanical_entry_id": match["botanical_entry_id"],
                    "brazil_botanical_name": match["botanical_name"],
                    "match_type": "exact_normalized_name",
                    "match_confidence": "high",
                    "action": "flag_overlap_keep_both",
                }
            )

    duplicate_registry = []
    for row in botanical_master_rows:
        if int(row["duplicate_name_count"]) > 1:
            duplicate_registry.append(
                {
                    "botanical_entry_id": row["botanical_entry_id"],
                    "botanical_name": row["botanical_name"],
                    "duplicate_name_group": row["duplicate_name_group"],
                    "duplicate_name_count": row["duplicate_name_count"],
                    "source_table": row["source_table"],
                    "source_row": row["source_row"],
                }
            )

    output_counts = {
        "raw_botanical_list_uk_additive": len(raw_uk_rows),
        "botanical_entries_master_union_additive": len(botanical_master_rows),
        "botanical_zone_profiles_brazil_additive": len(brazil_zone_rows),
        "product_catalogue_brazil_additive": len(product_rows),
        "product_botanical_links_brazil_additive": len(product_botanical_rows),
        "botanical_overlap_mapping": len(overlaps),
        "duplicate_name_registry": len(duplicate_registry),
    }

    write_csv(
        OUT_DIR / "raw_botanical_list_uk_additive.csv",
        raw_uk_rows,
        [
            "source_row",
            "botanical_name",
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
        ],
    )
    write_csv(
        OUT_DIR / "botanical_entries_master_union_additive.csv",
        botanical_master_rows,
        [
            "botanical_entry_id",
            "botanical_name",
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
            "kombucha_1f_friendly_flag",
            "tea_friendly_flag",
            "bitters_friendly_flag",
            "cordial_friendly_flag",
            "fresh_produce_friendly_flag",
            "preserve_friendly_flag",
            "cosmetic_friendly_flag",
            "source_table",
            "source_row",
        ],
    )
    write_csv(
        OUT_DIR / "botanical_zone_profiles_brazil_additive.csv",
        brazil_zone_rows,
        [
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
            "humidity_preference",
            "root_depth_type",
            "spread_pattern",
            "companion_plants",
            "incompatible_with",
            "guild_roles",
            "foraging_habitat",
            "harvest_window",
            "planting_sowing_window",
            "yield_regrowth",
            "propagation_methods",
            "conservation_status",
            "foraging_cautions",
            "wildlife_supported",
            "notes",
            "branch_id",
            "country",
            "region",
            "zone",
            "microclimate_tags",
            "production_mode",
            "source_table",
            "source_row",
        ],
    )
    write_csv(
        OUT_DIR / "product_catalogue_brazil_additive.csv",
        product_rows,
        [
            "product_id",
            "product_name",
            "catalogue_line_guess",
            "fermentation_family_guess",
            "format_label",
            "function_label",
            "core_base",
            "protocols_used",
            "botanicals_used",
            "live_status",
            "intended_use",
            "strength_level",
            "shelf_stability",
            "development_status",
            "notes",
            "source_table",
            "source_row",
        ],
    )
    write_csv(
        OUT_DIR / "product_botanical_links_brazil_additive.csv",
        product_botanical_rows,
        [
            "product_id",
            "product_name",
            "ingredient_label",
            "ingredient_kind",
            "botanical_entry_id",
            "matched_botanical_name",
            "match_status",
            "candidate_matches",
            "resolution_needed",
        ],
    )
    write_csv(
        OUT_DIR / "botanical_overlap_mapping.csv",
        overlaps,
        [
            "uk_botanical_entry_id",
            "uk_botanical_name",
            "brazil_botanical_entry_id",
            "brazil_botanical_name",
            "match_type",
            "match_confidence",
            "action",
        ],
    )
    write_csv(
        OUT_DIR / "duplicate_name_registry.csv",
        duplicate_registry,
        [
            "botanical_entry_id",
            "botanical_name",
            "duplicate_name_group",
            "duplicate_name_count",
            "source_table",
            "source_row",
        ],
    )
    write_csv(
        OUT_DIR / "relation_mapping_registry.csv",
        relation_mapping_rows(
            {
                "Botanicals_Master": len(brazil["Botanicals_Master"]),
                "Brazil_Working_Master": len(brazil["Brazil_Working_Master"]),
                "Products": len(brazil["Products"]),
                "Product_Botanical_Links": len(brazil["Product_Botanical_Links"]),
            },
            len(uk_rows),
            len(overlaps),
            output_counts,
        ),
        ["source_stack", "source_table", "source_key", "relation_type", "target_table", "target_key", "row_count", "notes"],
    )

    manifest = {
        "brazil_source": str(BRAZIL_XLSX),
        "uk_source": str(UK_ZIP),
        "output_dir": str(OUT_DIR),
        "row_counts": output_counts,
        "notes": [
            "Brazil workbook treated as primary source of truth.",
            "UK kombucha-friendly export unioned into botanical master without replacing Brazil rows.",
            "Overlap rows are flagged in botanical_overlap_mapping.csv rather than collapsed.",
            "Existing Jun protocol and product seed bundle remains separate and should still be loaded.",
        ],
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
