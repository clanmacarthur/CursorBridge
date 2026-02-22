"""
Build docs/RELATIONS_MASTER.csv from the existing and to-be relation tables.

This keeps one merged tracking table with check fields for:
- Supabase status
- Convex status
- launch readiness
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
EXISTING_PATH = ROOT / "docs" / "RELATIONS_EXISTING.csv"
TO_BE_PATH = ROOT / "docs" / "RELATIONS_TO_BE.csv"
INVENTORY_PATH = ROOT / "docs" / "_supabase_inventory_live.json"
OUTPUT_PATH = ROOT / "docs" / "RELATIONS_MASTER.csv"


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def relation_key(row: Dict[str, str]) -> str:
    return (
        f"{row.get('from_table', '').strip()}."
        f"{row.get('from_column', '').strip()}->"
        f"{row.get('to_table', '').strip()}."
        f"{row.get('to_column', '').strip()}"
    )


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def load_supabase_table_set(path: Path) -> set[str]:
    if not path.exists():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    tables = payload.get("tables", [])
    return {str(item.get("table", "")).strip() for item in tables if item.get("table")}


def main() -> None:
    existing_rows = load_csv(EXISTING_PATH)
    to_be_rows = load_csv(TO_BE_PATH)
    supabase_tables = load_supabase_table_set(INVENTORY_PATH)

    existing_by_key = {relation_key(r): r for r in existing_rows}
    to_be_by_key = {relation_key(r): r for r in to_be_rows}

    all_keys = sorted(set(existing_by_key.keys()) | set(to_be_by_key.keys()))
    out_rows: List[Dict[str, str]] = []

    for key in all_keys:
        existing = existing_by_key.get(key)
        target = to_be_by_key.get(key)

        base = target if target is not None else existing
        assert base is not None

        from_table = base.get("from_table", "").strip()
        to_table = base.get("to_table", "").strip()

        current_state = (
            target.get("current_state", "").strip()
            if target is not None
            else existing.get("state", "").strip()
        )
        next_action = (
            target.get("next_action", "").strip() if target is not None else "keep"
        )
        phase = target.get("phase", "").strip() if target is not None else "P0"

        supabase_configured = current_state in {
            "live",
            "live_fk",
            "derived_live",
            "live_edge_table",
        }
        needs_more_data = (
            current_state in {"text_link_only", "json_link_only"}
            or "stabilize_lookup_key" in next_action
            or "define_json_schema" in next_action
        )

        source_status = "both" if existing and target else "existing" if existing else "to_be"

        out_rows.append(
            {
                "relation_key": key,
                "from_table": from_table,
                "from_column": base.get("from_column", "").strip(),
                "to_table": to_table,
                "to_column": base.get("to_column", "").strip(),
                "relation_type": (
                    target.get("target_type", "").strip()
                    if target is not None
                    else existing.get("relation_type", "").strip()
                ),
                "source_status": source_status,
                "in_existing": bool_str(existing is not None),
                "in_to_be": bool_str(target is not None),
                "current_state": current_state,
                "next_action": next_action,
                "phase": phase,
                "on_supabase": bool_str(
                    from_table in supabase_tables and to_table in supabase_tables
                ),
                "supabase_configured": bool_str(supabase_configured),
                "needs_more_data": bool_str(needs_more_data),
                "on_convex": "false",
                "convex_configured": "false",
                "convex_synced": "false",
                "ready_for_launch": bool_str(supabase_configured and not needs_more_data),
                "mach_layer": "Core",
                "notes": (
                    target.get("notes", "").strip()
                    if target is not None
                    else existing.get("source", "").strip()
                ),
            }
        )

    fieldnames = [
        "relation_key",
        "from_table",
        "from_column",
        "to_table",
        "to_column",
        "relation_type",
        "source_status",
        "in_existing",
        "in_to_be",
        "current_state",
        "next_action",
        "phase",
        "on_supabase",
        "supabase_configured",
        "needs_more_data",
        "on_convex",
        "convex_configured",
        "convex_synced",
        "ready_for_launch",
        "mach_layer",
        "notes",
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

