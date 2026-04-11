import csv
import json
import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(r"c:\Code\CursorBridge")
IDENTITY_XLSX = Path(
    r"C:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\brazil_identity_block1_core_targeted_large_v2.xlsx"
)
BRAZIL_TABLES_XLSX = Path(
    r"C:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\brazil_data_tables_only.xlsx"
)
OUT_DIR = ROOT / "exports" / "botanicals_patch" / "latest"

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def normalize_text(value: str) -> str:
    value = (value or "").strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def to_bool_token(value: str) -> str:
    value = normalize_text(value)
    if value in {"yes", "true", "1", "sim"}:
        return "TRUE"
    if value in {"no", "false", "0", "nao", "não"}:
        return "FALSE"
    return ""


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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def main() -> None:
    identity = read_xlsx(IDENTITY_XLSX)["IDENTITY_BRAZIL_BLOCK1"]
    brazil = read_xlsx(BRAZIL_TABLES_XLSX)["Brazil_Working_Master"]

    identity_by_sciname = {}
    for row in identity:
        accepted = normalize_text(row.get("accepted_name", ""))
        if accepted:
            identity_by_sciname[accepted] = row

    entries_rows = []
    zone_rows = []
    for row in brazil:
        entry_id = row.get("Botanical_ID", "") or row.get("Botanical Entry ID", "")
        sci_name = row.get("Scientific Name", "")
        match = identity_by_sciname.get(normalize_text(sci_name))
        if not entry_id or not match:
            continue

        entries_rows.append(
            {
                "botanical_entry_id": entry_id,
                "common_name_en": match.get("common_name_en", ""),
                "mature_height_m_min": match.get("mature_height_m_min", ""),
                "mature_height_m_max": match.get("mature_height_m_max", ""),
                "mature_spread_m_min": match.get("mature_spread_m_min", ""),
                "mature_spread_m_max": match.get("mature_spread_m_max", ""),
                "endemic_to_brazil": to_bool_token(match.get("endemic_to_brazil", "")),
                "conservation_flag": match.get("conservation_flag", ""),
                "invasive_risk_brazil": match.get("invasive_risk_brazil", ""),
                "source_url_primary": match.get("source_url_primary", ""),
                "source_url_secondary": match.get("source_url_secondary", ""),
                "source_url_tertiary": match.get("source_url_tertiary", ""),
                "confidence_score": match.get("confidence_score", ""),
                "confidence_notes": match.get("confidence_notes", ""),
                "match_basis": "scientific_name_to_accepted_name",
            }
        )

        zone_rows.append(
            {
                "botanical_entry_id": entry_id,
                "light_preference": match.get("light_preference", ""),
                "flood_tolerance": match.get("flood_tolerance", ""),
                "salinity_tolerance": match.get("salinity_tolerance", ""),
                "heat_tolerance": match.get("heat_tolerance", ""),
                "fire_tolerance": match.get("fire_tolerance", ""),
                "harvest_window_brazil": match.get("harvest_window_brazil", ""),
                "local_only_flag": "",
                "export_mode": "",
                "nursery_only_flag": "",
                "education_only_flag": "",
                "current_site_live_flag": "",
                "match_basis": "scientific_name_to_accepted_name",
            }
        )

    branch_resources_rows = [
        {
            "branch_resource_id": "brres_branch_brazil_001",
            "branch_id": "branch_brazil",
            "capability_type": "country_capability_profile",
            "capability_name": "Brazil baseline branch capability profile",
            "status": "reference_pending_detail",
            "machinery": "",
            "fabrication": "",
            "orchard": "",
            "greenhouse": "",
            "substrate_materials": "",
            "pond_life_materials": "",
            "soil_amendments": "",
            "staffing_or_skill": "",
            "notes": "Created by patch pass to satisfy final source-of-truth schema. Detailed branch capability rows still need explicit operational source data.",
            "source": "builder_patch_note_after_audit.md",
            "confidence": "medium",
        },
        {
            "branch_resource_id": "brres_branch_brazil_ubatuba_001",
            "branch_id": "branch_brazil_ubatuba_green_coast",
            "capability_type": "regional_focus_capability_profile",
            "capability_name": "Ubatuba / Green Coast focus capability profile",
            "status": "active_build_source_pack",
            "machinery": "",
            "fabrication": "",
            "orchard": "",
            "greenhouse": "protected_culture_crossover_possible",
            "substrate_materials": "atlantic_forest_and_coastal_focus",
            "pond_life_materials": "",
            "soil_amendments": "",
            "staffing_or_skill": "",
            "notes": "Derived from Ubatuba focus pack scope note: Atlantic Forest / Green Coast / protected-culture crossover.",
            "source": "ubatuba_green_coast_focus_pack_v1.xlsx",
            "confidence": "medium",
        },
    ]

    mapping_rows = [
        {
            "layer": "canonical_identity",
            "canonical_field": "common_name_en",
            "legacy_or_compatibility_field": "botanical_name",
            "operational_view_alias": "Common Name (EN)",
            "authority_rule": "common_name_en is authoritative when populated; fallback to botanical_name only for compatibility",
        },
        {
            "layer": "canonical_identity",
            "canonical_field": "mature_height_m_min / mature_height_m_max",
            "legacy_or_compatibility_field": "mature_height_m",
            "operational_view_alias": "Mature_Height_m_Min / Mature_Height_m_Max / Mature_Height_m",
            "authority_rule": "min/max range is canonical; single value remains compatibility shorthand",
        },
        {
            "layer": "canonical_identity",
            "canonical_field": "mature_spread_m_min / mature_spread_m_max",
            "legacy_or_compatibility_field": "mature_spread_m",
            "operational_view_alias": "Mature_Spread_m_Min / Mature_Spread_m_Max / Mature_Spread_m",
            "authority_rule": "min/max range is canonical; single value remains compatibility shorthand",
        },
        {
            "layer": "canonical_identity",
            "canonical_field": "confidence_score / confidence_notes",
            "legacy_or_compatibility_field": "data_confidence_level / record_completeness_score",
            "operational_view_alias": "Confidence Score / Confidence Notes / Data Confidence Level",
            "authority_rule": "numeric confidence_score + confidence_notes is richer canonical source; data_confidence_level stays as coarse compatibility field",
        },
        {
            "layer": "zone_overlay",
            "canonical_field": "light_preference / flood_tolerance / salinity_tolerance / heat_tolerance / fire_tolerance / harvest_window_brazil",
            "legacy_or_compatibility_field": "sun_exposure / harvest_window",
            "operational_view_alias": "Light Preference / Flood Tolerance / Salinity Tolerance / Heat Tolerance / Fire Tolerance / Harvest Window Brazil",
            "authority_rule": "new named tolerance fields are canonical; old broad text fields remain compatibility/context fields",
        },
        {
            "layer": "hons_overlay",
            "canonical_field": "stage_status / provenance_status / rights_status / branch_eligibility / synergy_status / node_relevance / experimental_policy / release_policy / public_publish_status",
            "legacy_or_compatibility_field": "stage / rights_notes / governance_notes",
            "operational_view_alias": "Stage Status / Provenance Status / Rights Status / Branch Eligibility / Synergy Status / Node Relevance / Experimental Policy / Release Policy / Public Publish Status",
            "authority_rule": "new explicit HONS status fields are canonical; old note fields remain narrative support",
        },
    ]

    manifest = {
        "identity_source": str(IDENTITY_XLSX),
        "brazil_working_source": str(BRAZIL_TABLES_XLSX),
        "counts": {
            "identity_rows_matched_to_brazil_working_master": len(entries_rows),
            "zone_rows_backfilled_by_entry": len(zone_rows),
            "branch_resources_seed_rows": len(branch_resources_rows),
            "canonical_alias_mapping_rows": len(mapping_rows),
        },
        "notes": [
            "Identity and zone patch backfill rows are keyed by current Brazil_Working_Master botanical entry IDs.",
            "Matching uses scientific_name from Brazil_Working_Master to accepted_name from the larger Brazil identity workbook.",
            "Operational flags local_only_flag/export_mode/nursery_only_flag/education_only_flag/current_site_live_flag did not have explicit source columns in the inspected workbooks and remain intentionally blank pending source-backed values.",
        ],
    }

    write_csv(
        OUT_DIR / "botanical_entries_master_patch_backfill.csv",
        entries_rows,
        [
            "botanical_entry_id",
            "common_name_en",
            "mature_height_m_min",
            "mature_height_m_max",
            "mature_spread_m_min",
            "mature_spread_m_max",
            "endemic_to_brazil",
            "conservation_flag",
            "invasive_risk_brazil",
            "source_url_primary",
            "source_url_secondary",
            "source_url_tertiary",
            "confidence_score",
            "confidence_notes",
            "match_basis",
        ],
    )
    write_csv(
        OUT_DIR / "botanical_zone_profiles_patch_backfill.csv",
        zone_rows,
        [
            "botanical_entry_id",
            "light_preference",
            "flood_tolerance",
            "salinity_tolerance",
            "heat_tolerance",
            "fire_tolerance",
            "harvest_window_brazil",
            "local_only_flag",
            "export_mode",
            "nursery_only_flag",
            "education_only_flag",
            "current_site_live_flag",
            "match_basis",
        ],
    )
    write_csv(
        OUT_DIR / "branch_resources_seed.csv",
        branch_resources_rows,
        [
            "branch_resource_id",
            "branch_id",
            "capability_type",
            "capability_name",
            "status",
            "machinery",
            "fabrication",
            "orchard",
            "greenhouse",
            "substrate_materials",
            "pond_life_materials",
            "soil_amendments",
            "staffing_or_skill",
            "notes",
            "source",
            "confidence",
        ],
    )
    write_csv(
        OUT_DIR / "canonical_vs_alias_mapping.csv",
        mapping_rows,
        [
            "layer",
            "canonical_field",
            "legacy_or_compatibility_field",
            "operational_view_alias",
            "authority_rule",
        ],
    )
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
