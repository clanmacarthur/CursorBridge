"""
Export Supabase stage tables into JSON files for Convex seeding.

Output:
- exports/convex_stage_seed/<timestamp>/manifest.json
- exports/convex_stage_seed/<timestamp>/<table>.json
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, List

import requests

from sync_notion_to_supabase_full import load_supabase_config


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "exports" / "convex_stage_seed"

STAGE_TABLES = [
    "during_session_stop_triggers_stage",
    "contraindications_mandatory_disclosure_stage",
    "breathwork_master_taxonomy_stage",
    "daily_regulation_sliders_stage",
    "controls_library_design_stage",
    "nadi_system_stage",
    "astrology_calendrical_systems_stage",
    "emotion_brain_body_energy_mapping_stage",
    "full_brain_neural_systems_table_stage",
    "mythological_beings_stage",
    "sacred_animals_stage",
    "stones_minerals_stage",
]


def rest_get(url: str, key: str, table: str, params: Dict[str, str]) -> requests.Response:
    return requests.get(
        f"{url}/rest/v1/{table}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
        },
        params=params,
        timeout=90,
    )


def fetch_all_rows(url: str, key: str, table: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    limit = 1000
    offset = 0
    while True:
        resp = rest_get(
            url,
            key,
            table,
            {
                "select": "*",
                "limit": str(limit),
                "offset": str(offset),
                "order": "id.asc",
            },
        )
        if resp.status_code not in (200, 206):
            raise RuntimeError(f"Failed reading {table} ({resp.status_code}): {resp.text[:500]}")
        payload = resp.json()
        if not isinstance(payload, list):
            raise RuntimeError(f"Unexpected payload for {table}: not a list")
        rows.extend(payload)
        if len(payload) < limit:
            break
        offset += limit
    return rows


def main() -> None:
    supabase_url, supabase_key = load_supabase_config()

    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUTPUT_ROOT / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest: Dict[str, Any] = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "supabase_url": supabase_url,
        "tables": [],
    }

    for table in STAGE_TABLES:
        rows = fetch_all_rows(supabase_url, supabase_key, table)
        (out_dir / f"{table}.json").write_text(
            json.dumps(rows, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        manifest["tables"].append(
            {
                "table": table,
                "rows": len(rows),
                "file": f"{table}.json",
            }
        )
        print(f"{table}: {len(rows)} rows")

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    latest_pointer = OUTPUT_ROOT / "LATEST.txt"
    latest_pointer.write_text(str(out_dir), encoding="utf-8")

    print(f"\nExport complete: {out_dir}")
    print(f"Manifest: {out_dir / 'manifest.json'}")
    print(f"Pointer: {latest_pointer}")


if __name__ == "__main__":
    main()
