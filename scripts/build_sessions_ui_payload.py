from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]


DOMAIN_ORDER = [
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

DOMAIN_LABELS = {
    "breath_library": "Breath",
    "movements_system": "Movement",
    "organ_emotion_system": "Organ / Emotion",
    "meridian_system": "Meridian",
    "light_colour": "Colour",
    "sound_vibration": "Sound",
    "nutrition_and_food": "Nutrition Food",
    "nutrition_protocols": "Nutrition Protocol",
    "symbols_index": "Symbol",
    "sacred_geometry": "Geometry",
    "chakra_systems": "Chakra",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    domain_inventory = load_json(ROOT / "docs" / "_sessions_domain_inventory_live_2026-03-05.json")
    support_inventory = load_json(ROOT / "docs" / "_sessions_support_inventory_live_2026-03-05.json")
    subject_tree = load_json(ROOT / "docs" / "_sessions_subject_tree_live_2026-03-05.json")
    drilldown = load_json(ROOT / "docs" / "_sessions_drilldown_lists_live_2026-03-05.json")

    subjects = sorted(subject_tree.get("session_types", {}).keys())

    domains: List[Dict[str, Any]] = []
    for table in DOMAIN_ORDER:
        d = domain_inventory[table]
        dd = drilldown.get(table, {})
        domains.append(
            {
                "table": table,
                "domain_label": DOMAIN_LABELS.get(table, table),
                "row_count": d["row_count"],
                "label_column": d["label_column"],
                "search_columns": d["search_columns"],
                "visible_filter_columns": d["usable_filter_columns"],
                "visible_filter_values": d["filter_distinct_values"],
                "hidden_dead_columns": d["hidden_columns"],
                "detail_fields": d["drawer_detail_columns"],
                "snapping_fields": d["snapping_columns"],
                "subject_grouping_column": dd.get("subject_grouping_column", ""),
                "first_drill_down_column": dd.get("first_drill_down_column", ""),
                "second_drill_down_column": dd.get("second_drill_down_column", ""),
                "subject_grouping_values": dd.get("subject_grouping_values", []),
                "first_drill_down_values": dd.get("first_drill_down_values", []),
                "second_drill_down_values": dd.get("second_drill_down_values", []),
                "rows": d["rows"],
            }
        )

    payload = {
        "generated_from": [
            "docs/SESSIONS_DOMAIN_INVENTORY_2026-03-05.md",
            "docs/SESSIONS_SUBJECT_TREE_2026-03-05.md",
            "docs/SESSIONS_FIELD_MAP_2026-03-05.md",
            "docs/_sessions_domain_inventory_live_2026-03-05.json",
            "docs/_sessions_support_inventory_live_2026-03-05.json",
            "docs/_sessions_subject_tree_live_2026-03-05.json",
            "docs/_sessions_drilldown_lists_live_2026-03-05.json",
        ],
        "top_level_subjects": subjects,
        "domains": domains,
        "support_tables": {
            "session_types": support_inventory["session_types"]["rows"],
            "attribute_taxonomy": support_inventory["attribute_taxonomy"]["rows"],
            "mappings": support_inventory["mappings"]["rows"],
            "cross_domain_mappings": support_inventory["cross_domain_mappings"]["rows"],
            "safety_rules": support_inventory["safety_rules"]["rows"],
            "session_runs_row_count": support_inventory["session_runs"]["row_count"],
            "session_outputs_row_count": support_inventory["session_outputs"]["row_count"],
        },
        "ui_rules": {
            "hide_dead_filters": True,
            "hide_empty_columns": True,
            "no_placeholder_filters": True,
            "no_invented_categories": True,
        },
    }

    out_path = ROOT / "docs" / "SESSIONS_UI_PAYLOAD_2026-03-05.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
