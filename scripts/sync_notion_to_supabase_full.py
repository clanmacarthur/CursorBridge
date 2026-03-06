"""
Sync Notion databases into Supabase using configured IDs and safe table mapping.

What this script does:
- Reads Notion database IDs from `config/notion_db_ids.json`.
- Reads Notion token from `c:/code/CursorBridge/.env`.
- Reads Supabase URL/key from `c:/code/task-manager/.env` (tries multiple keys and picks a working one).
- Syncs direct table matches plus approved map-only aliases.
- Skips admin tracker databases.
- Produces:
  - `docs/_notion_supabase_sync_full_report.json`
  - `sql/notion_stage_tables.sql` for currently missing target tables.

This script is designed to be idempotent based on `notion_page_id`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cb.db import notion_type_to_sql, sanitize_column_name
from cb.notion import query_database


ROOT_ENV = ROOT / ".env"
TASK_MANAGER_ENV = Path(r"C:\code\task-manager\.env")
NOTION_DB_IDS_PATH = ROOT / "config" / "notion_db_ids.json"

REPORT_PATH = ROOT / "docs" / "_notion_supabase_sync_full_report.json"
STAGE_SQL_PATH = ROOT / "sql" / "notion_stage_tables.sql"
TABLE_DIFF_PATH = ROOT / "docs" / "_notion_supabase_table_diff.json"


# Approved map-only aliases from docs/SESSIONS_KEEP_MERGE_DEPRECATE_MATRIX.md
TARGET_MAP: Dict[str, str] = {
    "colours_schema": "light_colour",
    "sounds_tones_schema": "sound_vibration",
    "symbols_schema": "symbols_index",
    "sacred_geometry_schema": "sacred_geometry",
    "deities_archetypes_schema": "deities_archetypes",
    "colour_legacy_archive": "light_colour",
}

# Not runtime data targets
SKIP_KEYS = {"relations_master", "relations_existing", "relations_to_be"}


def load_env_file(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    out: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip().lstrip("\ufeff")] = v.strip().strip('"').strip("'")
    return out


def load_notion_token() -> str:
    vals = load_env_file(ROOT_ENV)
    return (vals.get("NOTION_TOKEN") or "").strip()


def pick_working_supabase_key(url: str, candidates: List[str]) -> Optional[str]:
    url = (url or "").strip().rstrip("/")
    if not url:
        return None
    for key in candidates:
        key = (key or "").strip()
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
                return key
        except Exception:
            pass
    return None


def load_supabase_config() -> Tuple[str, str]:
    vals = load_env_file(TASK_MANAGER_ENV)
    url = (vals.get("SUPABASE_URL") or "").strip().rstrip("/")
    candidates = [
        (vals.get("SUPABASE_SERVICE_ROLE_KEY") or "").strip(),
        (vals.get("SUPABASE_SERVICE_KEY") or "").strip(),
        (vals.get("SUPABASE_ANON_KEY") or "").strip(),
        (vals.get("SUPABASE_KEY") or "").strip(),
    ]
    key = pick_working_supabase_key(url, candidates)
    if not url or not key:
        raise RuntimeError(
            "Could not find working Supabase URL/key from task-manager .env"
        )
    return url, key


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
        raise RuntimeError(f"OpenAPI request failed ({resp.status_code}): {resp.text[:300]}")
    return resp.json()


def load_notion_db_ids() -> Dict[str, str]:
    return json.loads(NOTION_DB_IDS_PATH.read_text(encoding="utf-8"))


def rest_get(url: str, key: str, table: str, params: Dict[str, str]) -> requests.Response:
    return requests.get(
        f"{url}/rest/v1/{table}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
        },
        params=params,
        timeout=60,
    )


def rest_insert(url: str, key: str, table: str, rows: List[Dict[str, Any]]) -> requests.Response:
    return requests.post(
        f"{url}/rest/v1/{table}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        json=rows,
        timeout=120,
    )


def rest_update_by_notion_page_id(
    url: str, key: str, table: str, notion_page_id: str, payload: Dict[str, Any]
) -> requests.Response:
    return requests.patch(
        f"{url}/rest/v1/{table}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        params={"notion_page_id": f"eq.{notion_page_id}"},
        json=payload,
        timeout=60,
    )


def fetch_existing_notion_ids(url: str, key: str, table: str) -> Set[str]:
    out: Set[str] = set()
    limit = 1000
    offset = 0
    while True:
        resp = rest_get(
            url,
            key,
            table,
            {"select": "notion_page_id", "limit": str(limit), "offset": str(offset)},
        )
        if resp.status_code not in (200, 206):
            return out
        rows = resp.json()
        if not isinstance(rows, list) or not rows:
            break
        for row in rows:
            value = row.get("notion_page_id")
            if value:
                out.add(str(value))
        if len(rows) < limit:
            break
        offset += limit
    return out


def generate_stage_sql(blocked_defs: List[Dict[str, Any]]) -> None:
    def sql_ident(name: str) -> str:
        escaped = str(name).replace('"', '""')
        # Always quote identifiers to avoid reserved-word and keyword conflicts.
        return f'"{escaped}"'

    lines = [
        "-- Auto-generated from Notion schemas for currently missing Supabase target tables",
        f"-- Generated: {dt.datetime.now(dt.UTC).isoformat()}",
        "",
    ]
    for item in blocked_defs:
        key = item["notion_key"]
        schema = item.get("schema", {}) or {}
        cols = [
            f'{sql_ident("id")} BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY',
            f'{sql_ident("notion_page_id")} TEXT UNIQUE',
        ]
        for prop, notion_type in schema.items():
            col = sanitize_column_name(prop)
            if col in {"id", "notion_page_id"}:
                continue
            # Quote all identifiers (especially reserved names like "column", "type", "action").
            cols.append(f"{sql_ident(col)} {notion_type_to_sql(notion_type)}")
        table_name = f"{key}_stage"
        lines.append(f"CREATE TABLE IF NOT EXISTS {sql_ident(table_name)} (")
        lines.append("  " + ",\n  ".join(cols))
        lines.append(");")
        lines.append("")

    STAGE_SQL_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAGE_SQL_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Notion databases to Supabase")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Read and report only. Do not write to Supabase.",
    )
    args = parser.parse_args()

    notion_token = load_notion_token()
    if not notion_token:
        raise RuntimeError("NOTION_TOKEN missing in root .env")
    os.environ["NOTION_TOKEN"] = notion_token

    supabase_url, supabase_key = load_supabase_config()

    openapi = supabase_openapi(supabase_url, supabase_key)
    defs = openapi.get("definitions", {})
    supabase_tables = set(defs.keys())
    columns_by_table = {
        table: set((defs[table].get("properties") or {}).keys())
        for table in supabase_tables
    }

    notion_map = load_notion_db_ids()

    common = sorted([k for k in notion_map if k in supabase_tables])
    missing = sorted(
        [k for k in notion_map if k not in supabase_tables and k not in TARGET_MAP]
    )
    TABLE_DIFF_PATH.write_text(
        json.dumps(
            {
                "notion_table_count": len(notion_map),
                "supabase_table_count": len(supabase_tables),
                "common_count": len(common),
                "notion_missing_in_supabase": missing,
                "common_tables": common,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report: Dict[str, Any] = {
        "timestamp": f"{dt.datetime.now(dt.UTC).isoformat()}",
        "dry_run": args.dry_run,
        "supabase_url": supabase_url,
        "notion_db_count": len(notion_map),
        "synced": [],
        "blocked_missing_target_table": [],
        "skipped": [],
        "errors": [],
    }

    blocked_defs: List[Dict[str, Any]] = []

    for notion_key, notion_db_id in notion_map.items():
        if notion_key in SKIP_KEYS:
            report["skipped"].append(
                {"notion_key": notion_key, "reason": "admin_tracker_not_runtime"}
            )
            continue

        target = notion_key if notion_key in supabase_tables else TARGET_MAP.get(notion_key)
        if not target:
            stage_target = f"{notion_key}_stage"
            if stage_target in supabase_tables:
                target = stage_target
        if not target or target not in supabase_tables:
            try:
                data = query_database(notion_db_id)
                rows_in_notion = len(data.get("rows", []))
                schema = data.get("schema", {})
            except Exception as e:
                rows_in_notion = 0
                schema = {}
                report["errors"].append(
                    {
                        "notion_key": notion_key,
                        "target_table": None,
                        "error": f"notion_query_failed_for_stage: {e}",
                    }
                )
            report["blocked_missing_target_table"].append(
                {
                    "notion_key": notion_key,
                    "target_table": None,
                    "rows_in_notion": rows_in_notion,
                    "reason": "no_supabase_table_or_mapping",
                }
            )
            blocked_defs.append(
                {"notion_key": notion_key, "schema": schema, "rows": rows_in_notion}
            )
            continue

        try:
            data = query_database(notion_db_id)
        except Exception as e:
            report["errors"].append(
                {
                    "notion_key": notion_key,
                    "target_table": target,
                    "error": f"notion_query_failed: {e}",
                }
            )
            continue

        rows = data.get("rows", [])
        schema = data.get("schema", {})
        target_cols = columns_by_table.get(target, set())

        if "notion_page_id" not in target_cols:
            report["errors"].append(
                {
                    "notion_key": notion_key,
                    "target_table": target,
                    "error": "target table missing notion_page_id column",
                }
            )
            continue

        transformed: List[Dict[str, Any]] = []
        for row in rows:
            payload: Dict[str, Any] = {"notion_page_id": row.get("_page_id")}
            for prop_name, value in row.items():
                if prop_name == "_page_id":
                    continue
                col = sanitize_column_name(prop_name)
                if col in target_cols and col != "id":
                    payload[col] = value
            transformed.append(payload)

        inserted = 0
        updated = 0
        failed = 0

        if not args.dry_run:
            existing_ids = fetch_existing_notion_ids(supabase_url, supabase_key, target)
            to_insert: List[Dict[str, Any]] = []

            for payload in transformed:
                notion_page_id = payload.get("notion_page_id")
                if not notion_page_id:
                    failed += 1
                    continue
                if notion_page_id in existing_ids:
                    resp = rest_update_by_notion_page_id(
                        supabase_url, supabase_key, target, str(notion_page_id), payload
                    )
                    if resp.status_code in (200, 204):
                        updated += 1
                    else:
                        failed += 1
                        report["errors"].append(
                            {
                                "notion_key": notion_key,
                                "target_table": target,
                                "notion_page_id": notion_page_id,
                                "error": f"update_failed_{resp.status_code}: {resp.text[:300]}",
                            }
                        )
                else:
                    to_insert.append(payload)

            for i in range(0, len(to_insert), 100):
                batch = to_insert[i : i + 100]
                resp = rest_insert(supabase_url, supabase_key, target, batch)
                if resp.status_code in (200, 201, 204):
                    inserted += len(batch)
                    continue

                # Fallback row-by-row to isolate failures
                for payload in batch:
                    one = rest_insert(supabase_url, supabase_key, target, [payload])
                    if one.status_code in (200, 201, 204):
                        inserted += 1
                    else:
                        failed += 1
                        report["errors"].append(
                            {
                                "notion_key": notion_key,
                                "target_table": target,
                                "notion_page_id": payload.get("notion_page_id"),
                                "error": f"insert_failed_{one.status_code}: {one.text[:300]}",
                            }
                        )

        report["synced"].append(
            {
                "notion_key": notion_key,
                "target_table": target,
                "rows_in_notion": len(rows),
                "rows_inserted": inserted,
                "rows_updated": updated,
                "rows_failed": failed,
                "source_schema_fields": len(schema),
            }
        )

    generate_stage_sql(blocked_defs)
    REPORT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    synced_count = len(report["synced"])
    blocked_count = len(report["blocked_missing_target_table"])
    error_count = len(report["errors"])

    print(f"Synced groups: {synced_count}")
    print(f"Blocked groups: {blocked_count}")
    print(f"Errors: {error_count}")
    print(f"Report: {REPORT_PATH}")
    print(f"Stage SQL: {STAGE_SQL_PATH}")


if __name__ == "__main__":
    main()
