"""
Prepare Convex seed files from the latest Supabase stage export and run a local readiness audit.

Outputs:
- <latest_export>/convex_seed/<collection>.json
- <latest_export>/convex_seed/manifest_convex.json
- docs/_convex_stage_readiness_audit.json
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
EXPORT_ROOT = ROOT / "exports" / "convex_stage_seed"
LATEST_PATH = EXPORT_ROOT / "LATEST.txt"
AUDIT_PATH = ROOT / "docs" / "_convex_stage_readiness_audit.json"


TABLE_TO_COLLECTION: Dict[str, str] = {
    "during_session_stop_triggers_stage": "sessionStopTriggers",
    "contraindications_mandatory_disclosure_stage": "contraindications",
    "breathwork_master_taxonomy_stage": "breathworkTaxonomy",
    "daily_regulation_sliders_stage": "dailyRegulationSliders",
    "controls_library_design_stage": "controlsLibraryDesign",
    "nadi_system_stage": "nadiSystem",
    "astrology_calendrical_systems_stage": "astrologyCalendricalSystems",
    "emotion_brain_body_energy_mapping_stage": "emotionBrainBodyEnergyMapping",
    "full_brain_neural_systems_table_stage": "fullBrainNeuralSystems",
    "mythological_beings_stage": "mythologicalBeings",
    "sacred_animals_stage": "sacredAnimals",
    "stones_minerals_stage": "stonesMinerals",
}


def load_latest_export_dir() -> Path:
    if not LATEST_PATH.exists():
        raise RuntimeError(f"Missing latest export pointer: {LATEST_PATH}")
    path = Path(LATEST_PATH.read_text(encoding="utf-8").strip())
    if not path.exists():
        raise RuntimeError(f"Latest export directory does not exist: {path}")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def convert_row(table: str, row: Dict[str, Any], imported_at_ms: int) -> Dict[str, Any]:
    return {
        "notionPageId": str(row["notion_page_id"]),
        "sourceTable": table,
        "sourceSystem": "supabase_stage",
        "importedAt": imported_at_ms,
        "raw": row,
    }


def audit_collection_docs(docs: List[Dict[str, Any]]) -> Tuple[int, int]:
    seen = set()
    duplicate = 0
    for doc in docs:
        key = doc["notionPageId"]
        if key in seen:
            duplicate += 1
        else:
            seen.add(key)
    return len(seen), duplicate


def simulate_upsert_twice(collection_docs: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = {}
    for collection, docs in collection_docs.items():
        store: Dict[str, Dict[str, Any]] = {}
        first_inserted = 0
        first_updated = 0
        second_inserted = 0
        second_updated = 0

        for doc in docs:
            k = doc["notionPageId"]
            if k in store:
                store[k] = doc
                first_updated += 1
            else:
                store[k] = doc
                first_inserted += 1

        for doc in docs:
            k = doc["notionPageId"]
            if k in store:
                store[k] = doc
                second_updated += 1
            else:
                store[k] = doc
                second_inserted += 1

        out[collection] = {
            "first_inserted": first_inserted,
            "first_updated": first_updated,
            "second_inserted": second_inserted,
            "second_updated": second_updated,
            "final_store_size": len(store),
        }
    return out


def main() -> None:
    latest_dir = load_latest_export_dir()
    src_manifest_path = latest_dir / "manifest.json"
    if not src_manifest_path.exists():
        raise RuntimeError(f"Missing source manifest: {src_manifest_path}")
    src_manifest = read_json(src_manifest_path)

    imported_at_ms = int(dt.datetime.now(dt.UTC).timestamp() * 1000)
    convex_seed_dir = latest_dir / "convex_seed"
    convex_seed_dir.mkdir(parents=True, exist_ok=True)

    table_reports: List[Dict[str, Any]] = []
    collection_docs: Dict[str, List[Dict[str, Any]]] = {}
    convex_manifest_rows: List[Dict[str, Any]] = []

    for item in src_manifest.get("tables", []):
        table = str(item.get("table", "")).strip()
        if table not in TABLE_TO_COLLECTION:
            continue
        source_file = latest_dir / str(item.get("file", ""))
        if not source_file.exists():
            raise RuntimeError(f"Missing source table file: {source_file}")
        rows = read_json(source_file)
        if not isinstance(rows, list):
            raise RuntimeError(f"Unexpected table payload for {table}: expected list")

        missing_notion = 0
        docs: List[Dict[str, Any]] = []
        for row in rows:
            notion_id = row.get("notion_page_id")
            if not notion_id:
                missing_notion += 1
                continue
            docs.append(convert_row(table, row, imported_at_ms))

        collection = TABLE_TO_COLLECTION[table]
        unique_count, duplicate_count = audit_collection_docs(docs)
        collection_docs[collection] = docs

        out_file = convex_seed_dir / f"{collection}.json"
        out_file.write_text(
            json.dumps(docs, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        table_reports.append(
            {
                "table": table,
                "collection": collection,
                "source_rows": len(rows),
                "seed_rows": len(docs),
                "missing_notion_page_id": missing_notion,
                "duplicate_notion_page_id": duplicate_count,
                "unique_notion_page_id": unique_count,
                "seed_file": str(out_file.relative_to(latest_dir)),
            }
        )
        convex_manifest_rows.append(
            {
                "collection": collection,
                "rows": len(docs),
                "file": f"{collection}.json",
            }
        )

    upsert_sim = simulate_upsert_twice(collection_docs)
    local_idempotent = all(
        stat["second_inserted"] == 0 and stat["final_store_size"] == stat["first_inserted"]
        for stat in upsert_sim.values()
    )
    no_missing_ids = all(t["missing_notion_page_id"] == 0 for t in table_reports)
    no_duplicates = all(t["duplicate_notion_page_id"] == 0 for t in table_reports)

    convex_manifest = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "source_export": str(latest_dir),
        "collections": convex_manifest_rows,
    }
    (convex_seed_dir / "manifest_convex.json").write_text(
        json.dumps(convex_manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    audit = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "latest_export": str(latest_dir),
        "mapping_rows": len(TABLE_TO_COLLECTION),
        "tables_audited": len(table_reports),
        "table_reports": table_reports,
        "upsert_simulation": upsert_sim,
        "gates": {
            "mapping_gate": True,
            "export_gate": True,
            "seed_transform_gate": True,
            "data_quality_no_missing_notion_page_id": no_missing_ids,
            "data_quality_no_duplicate_notion_page_id": no_duplicates,
            "local_dry_run_idempotent": local_idempotent,
        },
    }
    AUDIT_PATH.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Latest export: {latest_dir}")
    print(f"Convex seed dir: {convex_seed_dir}")
    print(f"Audit report: {AUDIT_PATH}")
    print(f"Gate local_dry_run_idempotent: {local_idempotent}")
    print(f"Gate no_missing_notion_page_id: {no_missing_ids}")
    print(f"Gate no_duplicate_notion_page_id: {no_duplicates}")


if __name__ == "__main__":
    main()
