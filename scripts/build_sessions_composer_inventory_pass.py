from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, List

import requests


ROOT = Path(__file__).resolve().parents[1]
TASK_MANAGER_ENV = Path(r"C:\code\task-manager\.env")


ACTIVE_TABLES = [
    "breath_library",
    "movements_system",
    "organ_emotion_system",
    "meridian_system",
    "light_colour",
    "sound_vibration",
    "nutrition_and_food",
    "nutrition_protocols",
    "symbols_index",
    "sacred_geometry",
    "chakra_systems",
]

SUPPORT_TABLES = [
    "session_types",
    "attribute_taxonomy",
    "mappings",
    "cross_domain_mappings",
    "safety_rules",
    "session_runs",
    "session_outputs",
]

IGNORED_TABLES = [
    "session_blueprints",
    "session_templates",
    "narration_styles",
    "lens_definitions",
    "meta_lens_presets",
    "control_definitions",
    "control_packs",
    "control_pack_items",
    "coupling_rules",
]

LABEL_COLUMN_MAP: Dict[str, str] = {
    "breath_library": "protocol_name",
    "movements_system": "movement___practice",
    "organ_emotion_system": "organ___system",
    "meridian_system": "meridian",
    "light_colour": "light___colour",
    "sound_vibration": "sound_type",
    "nutrition_and_food": "food_type",
    "nutrition_protocols": "nutrition_protocol",
    "symbols_index": "symbol",
    "sacred_geometry": "geometry",
    "chakra_systems": "chakra",
}

FILTER_PRIORITY_MAP: Dict[str, List[str]] = {
    "breath_library": [
        "typical_use",
        "activation_level",
        "safety_tier",
        "core_breath_quality",
    ],
    "movements_system": [
        "movement_family",
        "intensity",
        "primary_effect",
        "intent___condition_fit",
        "primary_body_region",
    ],
    "organ_emotion_system": [
        "primary_emotion",
        "stress_expression",
        "breath_type",
        "regulation_direction",
    ],
    "meridian_system": [
        "primary_emotion",
        "nervous_system_bias",
        "associated_organ",
        "five_element_phase",
    ],
    "light_colour": [
        "colour_family",
        "circadian_influence",
        "psychological_theme",
    ],
    "sound_vibration": [
        "primary_effect",
        "nervous_system_bias",
        "primary_organ",
    ],
    "nutrition_and_food": [
        "evidence_confidence",
        "primary_nutrition_domain",
        "associated_diets___protocols",
    ],
    "nutrition_protocols": [
        "primary_nutrition_goal",
        "strictness_level",
        "primary_attribute_focus",
        "secondary_attribute_focus",
    ],
    "symbols_index": [
        "symbol_class",
        "meaning_domain",
        "emotional_tone",
        "cultural_scope",
    ],
    "sacred_geometry": [
        "geometry_class",
        "psychophysiological_effect",
        "primary_element",
        "secondary_element",
    ],
    "chakra_systems": [
        "sanskrit_name",
        "primary_element",
        "organ_emotion",
    ],
}

DETAIL_PRIORITY_MAP: Dict[str, List[str]] = {
    "breath_library": [
        "protocol_name",
        "typical_use",
        "activation_level",
        "safety_tier",
        "core_breath_quality",
        "safety_notes",
        "notes",
    ],
    "movements_system": [
        "movement___practice",
        "movement_family",
        "intensity",
        "primary_effect",
        "primary_body_region",
        "notes",
    ],
    "organ_emotion_system": [
        "organ___system",
        "primary_emotion",
        "stress_expression",
        "regulation_direction",
        "contraindications___risk_notes",
        "notes",
    ],
    "meridian_system": [
        "meridian",
        "primary_emotion",
        "nervous_system_bias",
        "physiological_emphasis",
        "notes",
    ],
    "light_colour": [
        "light___colour",
        "colour_family",
        "psychological_theme",
        "circadian_influence",
        "primary_effect",
        "notes",
    ],
    "sound_vibration": [
        "sound_type",
        "sound___frequency",
        "primary_effect",
        "notes",
    ],
    "nutrition_and_food": [
        "food_type",
        "evidence_confidence",
        "contraindications",
        "notes",
    ],
    "nutrition_protocols": [
        "nutrition_protocol",
        "primary_nutrition_goal",
        "strictness_level",
        "contraindications",
        "notes",
    ],
    "symbols_index": [
        "symbol",
        "symbol_class",
        "meaning_domain",
        "emotional_tone",
        "cultural_scope",
        "notes",
    ],
    "sacred_geometry": [
        "geometry",
        "geometry_class",
        "psychophysiological_effect",
        "primary_element",
        "secondary_element",
        "notes",
    ],
    "chakra_systems": [
        "chakra",
        "sanskrit_name",
        "primary_element",
        "notes",
    ],
}

SNAP_PRIORITY_MAP: Dict[str, List[str]] = {
    "breath_library": ["activation_level", "typical_use", "safety_tier"],
    "movements_system": ["primary_effect", "intensity", "movement_family"],
    "organ_emotion_system": ["primary_emotion", "regulation_direction", "stress_expression"],
    "meridian_system": ["primary_emotion", "nervous_system_bias"],
    "light_colour": ["psychological_theme", "circadian_influence", "colour_family"],
    "sound_vibration": ["primary_effect"],
    "nutrition_and_food": ["evidence_confidence"],
    "nutrition_protocols": ["primary_nutrition_goal", "strictness_level"],
    "symbols_index": ["meaning_domain", "emotional_tone", "symbol_class"],
    "sacred_geometry": ["psychophysiological_effect", "primary_element", "secondary_element"],
    "chakra_systems": ["primary_element", "sanskrit_name"],
}

TECH_COLUMNS = {"id", "notion_page_id", "created_at", "updated_at"}


def load_env_file(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip().lstrip("\ufeff")] = v.strip().strip('"').strip("'")
    return out


def pick_supabase_credentials() -> tuple[str, str]:
    env = load_env_file(TASK_MANAGER_ENV)
    url = (env.get("SUPABASE_URL") or "").strip().rstrip("/")
    candidates = [
        (env.get("SUPABASE_SERVICE_ROLE_KEY") or "").strip(),
        (env.get("SUPABASE_SERVICE_KEY") or "").strip(),
        (env.get("SUPABASE_ANON_KEY") or "").strip(),
        (env.get("SUPABASE_KEY") or "").strip(),
    ]
    if not url:
        raise RuntimeError("SUPABASE_URL missing in task-manager .env")

    for key in candidates:
        if not key:
            continue
        try:
            resp = requests.get(
                f"{url}/rest/v1/",
                headers={
                    "apikey": key,
                    "Authorization": f"Bearer {key}",
                    "Accept": "application/openapi+json",
                },
                timeout=20,
            )
            if resp.status_code == 200:
                return url, key
        except Exception:
            continue
    raise RuntimeError("No working Supabase key found in task-manager .env")


def supabase_openapi(url: str, key: str) -> Dict[str, Any]:
    resp = requests.get(
        f"{url}/rest/v1/",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Accept": "application/openapi+json",
        },
        timeout=60,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenAPI fetch failed ({resp.status_code})")
    return resp.json()


def fetch_all_rows(url: str, key: str, table: str, limit: int = 1000) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    offset = 0
    while True:
        resp = requests.get(
            f"{url}/rest/v1/{table}",
            headers={"apikey": key, "Authorization": f"Bearer {key}", "Accept": "application/json"},
            params={"select": "*", "limit": str(limit), "offset": str(offset)},
            timeout=60,
        )
        if resp.status_code not in (200, 206):
            raise RuntimeError(f"Fetch failed for {table} ({resp.status_code}): {resp.text[:300]}")
        batch = resp.json()
        if not isinstance(batch, list):
            raise RuntimeError(f"Unexpected response for {table}")
        rows.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
    return rows


def is_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def norm_value(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def md_list(items: List[str]) -> str:
    if not items:
        return "- (none)"
    return "\n".join(f"- `{i}`" for i in items)


def md_value_list(items: List[str]) -> str:
    if not items:
        return "- (none)"
    return "\n".join(f"- {i}" for i in items)


def build_domain_inventory(url: str, key: str, defs: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for table in ACTIVE_TABLES:
        rows = fetch_all_rows(url, key, table)
        columns = list((defs.get(table, {}).get("properties", {}) or {}).keys())
        if not columns and rows:
            # fallback if schema is missing
            cols = set()
            for row in rows:
                cols.update(row.keys())
            columns = sorted(cols)

        non_empty_cols: List[str] = []
        empty_cols: List[str] = []
        for col in columns:
            has_any = any(is_non_empty(row.get(col)) for row in rows)
            if has_any:
                non_empty_cols.append(col)
            else:
                empty_cols.append(col)

        label_col = LABEL_COLUMN_MAP[table]
        if label_col not in columns:
            raise RuntimeError(f"Label column {label_col} missing in {table}")

        candidate_filters = FILTER_PRIORITY_MAP.get(table, [])
        usable_filters = [c for c in candidate_filters if c in non_empty_cols]
        filter_distinct: Dict[str, List[str]] = {}
        for col in usable_filters:
            vals = sorted({norm_value(row.get(col)) for row in rows if is_non_empty(row.get(col))})
            filter_distinct[col] = vals

        subject_group_col = usable_filters[0] if usable_filters else label_col
        first_drill_col = usable_filters[1] if len(usable_filters) > 1 else ""
        second_drill_col = usable_filters[2] if len(usable_filters) > 2 else ""

        detail_cols = [c for c in DETAIL_PRIORITY_MAP.get(table, []) if c in non_empty_cols]
        if not detail_cols:
            detail_cols = [c for c in non_empty_cols if c not in TECH_COLUMNS][:8]

        snap_cols = [c for c in SNAP_PRIORITY_MAP.get(table, []) if c in non_empty_cols]
        search_cols = []
        for c in [label_col, subject_group_col, first_drill_col, second_drill_col, *usable_filters, *snap_cols]:
            if c and c not in search_cols and c in non_empty_cols:
                search_cols.append(c)

        hidden_cols = sorted({*empty_cols, *(c for c in columns if c in TECH_COLUMNS)})

        result[table] = {
            "table": table,
            "row_count": len(rows),
            "columns": columns,
            "label_column": label_col,
            "non_empty_columns": non_empty_cols,
            "empty_columns": empty_cols,
            "usable_filter_columns": usable_filters,
            "filter_distinct_values": filter_distinct,
            "subject_grouping_column": subject_group_col,
            "first_drill_down_column": first_drill_col,
            "second_drill_down_column": second_drill_col,
            "search_columns": search_cols,
            "drawer_detail_columns": detail_cols,
            "snapping_columns": snap_cols,
            "hidden_columns": hidden_cols,
            "rows": rows,
        }
    return result


def split_csv_ids(value: Any) -> List[str]:
    if not isinstance(value, str):
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def build_support_inventory(url: str, key: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for table in SUPPORT_TABLES:
        rows = fetch_all_rows(url, key, table)
        out[table] = {"row_count": len(rows), "rows": rows}
    return out


def write_domain_inventory_doc(domain: Dict[str, Any], support: Dict[str, Any], path: Path) -> None:
    lines: List[str] = []
    lines.append("# Sessions Domain Inventory (Strict Live Values)")
    lines.append("")
    lines.append(f"Generated: {dt.datetime.now(dt.UTC).isoformat()}")
    lines.append("")
    lines.append("Scope: Active Sessions Composer domain tables only. Live data only.")
    lines.append("")
    lines.append("## Active Table Row Counts")
    lines.append("")
    for table in ACTIVE_TABLES:
        lines.append(f"- `{table}`: {domain[table]['row_count']}")
    lines.append("")
    lines.append("## Support Table Row Counts")
    lines.append("")
    for table in SUPPORT_TABLES:
        lines.append(f"- `{table}`: {support[table]['row_count']}")
    lines.append("")

    for table in ACTIVE_TABLES:
        d = domain[table]
        lines.append(f"## `{table}`")
        lines.append("")
        lines.append(f"- Table name: `{table}`")
        lines.append(f"- Total row count: `{d['row_count']}`")
        lines.append(f"- Main label column: `{d['label_column']}`")
        lines.append("- Exact non-empty columns:")
        lines.append(md_list(d["non_empty_columns"]))
        lines.append("- Exact empty columns:")
        lines.append(md_list(d["empty_columns"]))
        lines.append("- Usable filter columns (non-empty only):")
        lines.append(md_list(d["usable_filter_columns"]))
        lines.append("- Exact distinct values for each usable filter column:")
        if d["usable_filter_columns"]:
            for col in d["usable_filter_columns"]:
                lines.append(f"  - `{col}` ({len(d['filter_distinct_values'][col])} distinct)")
                vals = d["filter_distinct_values"][col]
                if vals:
                    for v in vals:
                        lines.append(f"    - {v}")
                else:
                    lines.append("    - (none)")
        else:
            lines.append("  - (none)")

        lines.append("- Column use for UI:")
        lines.append(f"  - Subject grouping: `{d['subject_grouping_column']}`")
        lines.append(f"  - First drill-down: `{d['first_drill_down_column'] or '(none)'}`")
        lines.append(f"  - Second drill-down: `{d['second_drill_down_column'] or '(none)'}`")
        lines.append(f"  - Search: `{', '.join(d['search_columns']) if d['search_columns'] else '(none)'}`")
        lines.append(
            f"  - Drawer detail display: `{', '.join(d['drawer_detail_columns']) if d['drawer_detail_columns'] else '(none)'}`"
        )
        lines.append(
            f"  - Snapping / cross-domain matching: `{', '.join(d['snapping_columns']) if d['snapping_columns'] else '(none)'}`"
        )
        lines.append(
            f"  - Hidden columns (empty + technical): `{', '.join(d['hidden_columns']) if d['hidden_columns'] else '(none)'}`"
        )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_subject_tree_doc(domain: Dict[str, Any], support: Dict[str, Any], path: Path) -> Dict[str, Any]:
    session_type_rows = support["session_types"]["rows"]
    mappings_rows = support["mappings"]["rows"]
    taxonomy_rows = support["attribute_taxonomy"]["rows"]
    cross_rows = support["cross_domain_mappings"]["rows"]

    map_by_session: Dict[str, List[str]] = {}
    for row in mappings_rows:
        from_value = (row.get("from_value") or "").strip()
        to_value = (row.get("to_value") or "").strip()
        mapping_type = (row.get("mapping_type") or "").strip()
        if from_value and to_value and "Session Type" in mapping_type:
            map_by_session.setdefault(from_value, []).append(to_value)

    lines: List[str] = []
    lines.append("# Sessions Subject Tree (Strict Live Values)")
    lines.append("")
    lines.append(f"Generated: {dt.datetime.now(dt.UTC).isoformat()}")
    lines.append("")
    lines.append("Top-level subjects are taken from `session_types.session_type`.")
    lines.append("")
    lines.append("## Top-Level Subjects")
    lines.append("")

    subject_tree: Dict[str, Any] = {"session_types": {}, "attribute_taxonomy": {}, "cross_domain_mappings": {}}

    for row in sorted(session_type_rows, key=lambda r: (r.get("session_type") or "").strip()):
        subject = (row.get("session_type") or "").strip()
        if not subject:
            continue
        max_intensity = (row.get("max_intensity") or "").strip()
        allows_activation = (row.get("allows_activation") or "").strip()
        relevant_emotions_ids = split_csv_ids(row.get("relevant_emotions"))
        allowed_styles_ids = split_csv_ids(row.get("allowed_styles"))
        mapped_attrs = sorted(set(map_by_session.get(subject, [])))

        subject_tree["session_types"][subject] = {
            "max_intensity": max_intensity,
            "allows_activation": allows_activation,
            "relevant_emotions_ids": relevant_emotions_ids,
            "allowed_styles_ids": allowed_styles_ids,
            "mapped_attributes_via_mappings": mapped_attrs,
        }

        lines.append(f"- `{subject}`")
        lines.append(f"  - max_intensity: `{max_intensity}`")
        lines.append(f"  - allows_activation: `{allows_activation}`")
        lines.append(
            f"  - relevant_emotions_ids: `{', '.join(relevant_emotions_ids) if relevant_emotions_ids else '(none)'}`"
        )
        lines.append(
            f"  - allowed_styles_ids: `{', '.join(allowed_styles_ids) if allowed_styles_ids else '(none)'}`"
        )
        lines.append(
            f"  - mapped_attributes_via_mappings: `{', '.join(mapped_attrs) if mapped_attrs else '(none)'}`"
        )
    lines.append("")

    lines.append("## Attribute Taxonomy Parent Tree")
    lines.append("")
    parent_to_children: Dict[str, List[str]] = {}
    roots: List[str] = []
    for row in taxonomy_rows:
        attr = (row.get("attribute") or "").strip()
        parent = (row.get("parent") or "").strip()
        if not attr:
            continue
        if parent:
            parent_to_children.setdefault(parent, []).append(attr)
        else:
            roots.append(attr)

    for parent, children in parent_to_children.items():
        parent_to_children[parent] = sorted(set(children))
    roots = sorted(set(roots))

    for root in roots:
        children = parent_to_children.get(root, [])
        subject_tree["attribute_taxonomy"][root] = children
        lines.append(f"- `{root}`")
        if children:
            for child in children:
                lines.append(f"  - `{child}`")
        else:
            lines.append("  - (no child branches)")
    lines.append("")

    lines.append("## Cross-Domain Mapping Tree")
    lines.append("")
    source_to_targets: Dict[str, List[str]] = {}
    for row in cross_rows:
        source = (row.get("source_domain") or "").strip()
        target = (row.get("target_domain") or "").strip()
        if source and target:
            source_to_targets.setdefault(source, []).append(target)
    for source in list(source_to_targets.keys()):
        source_to_targets[source] = sorted(set(source_to_targets[source]))

    for source in sorted(source_to_targets.keys()):
        targets = source_to_targets[source]
        subject_tree["cross_domain_mappings"][source] = targets
        lines.append(f"- `{source}`")
        for target in targets:
            lines.append(f"  - `{target}`")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return subject_tree


def write_field_map_doc(domain: Dict[str, Any], path: Path) -> None:
    lines: List[str] = []
    lines.append("# Sessions Field Map (Strict Live Values)")
    lines.append("")
    lines.append(f"Generated: {dt.datetime.now(dt.UTC).isoformat()}")
    lines.append("")

    for table in ACTIVE_TABLES:
        d = domain[table]
        lines.append(f"## `{table}`")
        lines.append("")
        lines.append(f"- Label column: `{d['label_column']}`")
        lines.append(
            f"- Search columns: `{', '.join(d['search_columns']) if d['search_columns'] else '(none)'}`"
        )
        lines.append(
            f"- Filter columns: `{', '.join(d['usable_filter_columns']) if d['usable_filter_columns'] else '(none)'}`"
        )
        lines.append(
            f"- Detail columns: `{', '.join(d['drawer_detail_columns']) if d['drawer_detail_columns'] else '(none)'}`"
        )
        lines.append(
            f"- Hidden columns: `{', '.join(d['hidden_columns']) if d['hidden_columns'] else '(none)'}`"
        )
        lines.append(
            f"- Snapping columns: `{', '.join(d['snapping_columns']) if d['snapping_columns'] else '(none)'}`"
        )
        lines.append("- Reason for choices:")
        lines.append(
            f"  - Label uses `{d['label_column']}` because it is non-empty across live rows and is the domain's primary readable name field."
        )
        if d["usable_filter_columns"]:
            lines.append(
                "  - Filters include only non-empty live columns; empty columns are hidden by rule."
            )
        else:
            lines.append("  - No filter columns are shown because candidate filter columns are empty in live data.")
        lines.append(
            "  - Search includes label + active drill-down + snapping columns to keep queries aligned with visible UI controls."
        )
        lines.append(
            "  - Drawer detail columns prioritize readable non-empty fields and exclude technical identifiers."
        )
        lines.append(
            "  - Snapping columns are non-empty relation-like fields used for cross-domain matching with mappings and cross_domain_mappings."
        )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    url, key = pick_supabase_credentials()
    openapi = supabase_openapi(url, key)
    defs = openapi.get("definitions", {})

    domain_inventory = build_domain_inventory(url, key, defs)
    support_inventory = build_support_inventory(url, key)

    inventory_path = ROOT / "docs" / "SESSIONS_DOMAIN_INVENTORY_2026-03-05.md"
    subject_tree_path = ROOT / "docs" / "SESSIONS_SUBJECT_TREE_2026-03-05.md"
    field_map_path = ROOT / "docs" / "SESSIONS_FIELD_MAP_2026-03-05.md"

    write_domain_inventory_doc(domain_inventory, support_inventory, inventory_path)
    subject_tree = write_subject_tree_doc(domain_inventory, support_inventory, subject_tree_path)
    write_field_map_doc(domain_inventory, field_map_path)

    # Machine-readable outputs for proof and UI wiring.
    write_json(ROOT / "docs" / "_sessions_domain_inventory_live_2026-03-05.json", domain_inventory)
    write_json(ROOT / "docs" / "_sessions_support_inventory_live_2026-03-05.json", support_inventory)
    write_json(ROOT / "docs" / "_sessions_subject_tree_live_2026-03-05.json", subject_tree)

    drilldown = {}
    for table, d in domain_inventory.items():
        drilldown[table] = {
            "row_count": d["row_count"],
            "label_column": d["label_column"],
            "subject_grouping_column": d["subject_grouping_column"],
            "first_drill_down_column": d["first_drill_down_column"],
            "second_drill_down_column": d["second_drill_down_column"],
            "subject_grouping_values": d["filter_distinct_values"].get(d["subject_grouping_column"], []),
            "first_drill_down_values": d["filter_distinct_values"].get(d["first_drill_down_column"], []),
            "second_drill_down_values": d["filter_distinct_values"].get(d["second_drill_down_column"], []),
        }
    write_json(ROOT / "docs" / "_sessions_drilldown_lists_live_2026-03-05.json", drilldown)

    print(str(inventory_path))
    print(str(subject_tree_path))
    print(str(field_map_path))
    print("OK")


if __name__ == "__main__":
    main()
