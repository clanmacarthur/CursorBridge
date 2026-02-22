"""
Check off relation progress in Notion as work is completed.

This updates:
- Relations Master (DB)
- Relations To-Be (DB)
- Relations Existing (DB)

You can target rows by:
- relation id (for To-Be/Existing), for example: TG018 or EX006
- relation key (for Master), for example:
  session_runs.session_template_id->session_templates.id

Examples:
  python scripts/checkoff_notion_relation_progress.py --relation-id TG018 --mark-supabase-done
  python scripts/checkoff_notion_relation_progress.py --relation-id TG018 --note "FK added in migration 2026-02-22"
  python scripts/checkoff_notion_relation_progress.py --relation-key "mappings.from_db+from_field->mappings.to_db+to_field" --mark-convex-done
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "notion_db_ids.json"
ENV_PATH = ROOT / ".env"
NOTION_VERSION = "2022-06-28"


def load_notion_token() -> str:
    token = os.getenv("NOTION_TOKEN", "").strip()
    if token:
        return token
    if not ENV_PATH.exists():
        return ""
    for raw in ENV_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip().lstrip("\ufeff") == "NOTION_TOKEN":
            return value.strip()
    return ""


def load_db_ids() -> Dict[str, str]:
    if not CONFIG_PATH.exists():
        raise RuntimeError(f"Missing {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def rich_text(value: str) -> Dict[str, Any]:
    value = str(value or "").strip()
    if not value:
        return {"rich_text": []}
    return {
        "rich_text": [
            {
                "type": "text",
                "text": {"content": value[:2000]},
            }
        ]
    }


def select_value(value: str) -> Dict[str, Any]:
    value = str(value or "").strip()
    if not value:
        return {"select": None}
    return {"select": {"name": value}}


def checkbox(value: bool) -> Dict[str, Any]:
    return {"checkbox": bool(value)}


def date_value(value: str) -> Dict[str, Any]:
    if not value:
        return {"date": None}
    return {"date": {"start": value}}


def plain_from_prop(prop: Dict[str, Any]) -> str:
    ptype = prop.get("type")
    if ptype == "title":
        return "".join([item.get("plain_text", "") for item in prop.get("title", [])]).strip()
    if ptype == "rich_text":
        return "".join([item.get("plain_text", "") for item in prop.get("rich_text", [])]).strip()
    if ptype == "select":
        sel = prop.get("select")
        return sel.get("name", "").strip() if sel else ""
    return ""


class Notion:
    def __init__(self, token: str, *, dry_run: bool = False):
        self.token = token
        self.dry_run = dry_run
        self.base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base}{path}"
        resp = requests.request(method, url, headers=self.headers, json=payload, timeout=60)
        if resp.status_code >= 300:
            raise RuntimeError(f"{method} {path} failed ({resp.status_code}): {resp.text}")
        if not resp.text:
            return {}
        return resp.json()

    def query_by_title(self, database_id: str, title_property: str, title_value: str) -> Optional[Dict[str, Any]]:
        data = self.request(
            "POST",
            f"/databases/{database_id}/query",
            {
                "filter": {
                    "property": title_property,
                    "title": {"equals": title_value},
                },
                "page_size": 1,
            },
        )
        rows = data.get("results", [])
        return rows[0] if rows else None

    def patch_page(self, page_id: str, properties: Dict[str, Any]) -> None:
        if self.dry_run:
            print(f"[DRY-RUN] PATCH page {page_id}: {list(properties.keys())}")
            return
        self.request("PATCH", f"/pages/{page_id}", {"properties": properties})

    def verify(self) -> None:
        self.request("GET", "/users/me")


def relation_key_from_row(row: Dict[str, Any]) -> Optional[str]:
    props = row.get("properties", {})
    from_table = plain_from_prop(props.get("From Table", {}))
    from_col = plain_from_prop(props.get("From Column", {}))
    to_table = plain_from_prop(props.get("To Table", {}))
    to_col = plain_from_prop(props.get("To Column", {}))
    if not (from_table and from_col and to_table and to_col):
        return None
    return f"{from_table}.{from_col}->{to_table}.{to_col}"


def build_generic_updates(args: argparse.Namespace) -> Dict[str, Any]:
    updates: Dict[str, Any] = {}
    today = dt.date.today().isoformat()

    if args.mark_supabase_done:
        updates["Current State"] = select_value("live")
        updates["On Supabase"] = checkbox(True)
        updates["Supabase Configured"] = checkbox(True)
        updates["Needs More Data"] = checkbox(False)
        updates["Ready For Launch"] = checkbox(True)

    if args.mark_convex_done:
        updates["On Convex"] = checkbox(True)
        updates["Convex Configured"] = checkbox(True)
        updates["Convex Synced"] = checkbox(True)

    if args.on_supabase is not None:
        updates["On Supabase"] = checkbox(as_bool(args.on_supabase))
    if args.supabase_configured is not None:
        updates["Supabase Configured"] = checkbox(as_bool(args.supabase_configured))
    if args.needs_more_data is not None:
        updates["Needs More Data"] = checkbox(as_bool(args.needs_more_data))
    if args.on_convex is not None:
        updates["On Convex"] = checkbox(as_bool(args.on_convex))
    if args.convex_configured is not None:
        updates["Convex Configured"] = checkbox(as_bool(args.convex_configured))
    if args.convex_synced is not None:
        updates["Convex Synced"] = checkbox(as_bool(args.convex_synced))
    if args.ready_for_launch is not None:
        updates["Ready For Launch"] = checkbox(as_bool(args.ready_for_launch))

    if args.phase:
        updates["Phase"] = select_value(args.phase)
    if args.current_state:
        updates["Current State"] = select_value(args.current_state)
    if args.mach_layer:
        updates["Mach Layer"] = select_value(args.mach_layer)
    if args.next_action:
        updates["Next Action"] = rich_text(args.next_action)
    if args.note:
        updates["Notes"] = rich_text(args.note)

    updates["Last Checked"] = date_value(today)
    return updates


def filter_updates_for_row(row: Dict[str, Any], generic_updates: Dict[str, Any]) -> Dict[str, Any]:
    allowed = set(row.get("properties", {}).keys())
    return {k: v for k, v in generic_updates.items() if k in allowed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check off relation progress in Notion")
    parser.add_argument("--relation-id", action="append", default=[], help="Relation ID (TGxxx or EXxxx)")
    parser.add_argument("--relation-key", action="append", default=[], help="Master relation key")
    parser.add_argument("--mark-supabase-done", action="store_true", help="Mark Supabase done fields")
    parser.add_argument("--mark-convex-done", action="store_true", help="Mark Convex done fields")
    parser.add_argument("--on-supabase")
    parser.add_argument("--supabase-configured")
    parser.add_argument("--needs-more-data")
    parser.add_argument("--on-convex")
    parser.add_argument("--convex-configured")
    parser.add_argument("--convex-synced")
    parser.add_argument("--ready-for-launch")
    parser.add_argument("--phase", help="P0|P1|P2|P3|Parked")
    parser.add_argument("--current-state", help="live|missing_fk|text_link_only|json_link_only|live_edge_table")
    parser.add_argument("--mach-layer", help="Core|Mach1.1|Advanced")
    parser.add_argument("--next-action")
    parser.add_argument("--note")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.relation_id and not args.relation_key:
        raise RuntimeError("Provide at least one --relation-id or --relation-key")

    token = load_notion_token()
    if not token:
        raise RuntimeError("NOTION_TOKEN not found in environment or .env")

    ids = load_db_ids()
    master_db = ids.get("relations_master")
    existing_db = ids.get("relations_existing")
    to_be_db = ids.get("relations_to_be")
    if not (master_db and existing_db and to_be_db):
        raise RuntimeError("Missing relations_* IDs in config/notion_db_ids.json")

    notion = Notion(token, dry_run=args.dry_run)
    notion.verify()

    generic_updates = build_generic_updates(args)
    touched_master: set[str] = set()

    def update_master_by_key(key: str) -> None:
        row = notion.query_by_title(master_db, "Relation Key", key)
        if not row:
            print(f"[WARN] Master row not found for key: {key}")
            return
        props = filter_updates_for_row(row, generic_updates)
        notion.patch_page(row["id"], props)
        touched_master.add(key)
        print(f"[OK] Master updated: {key}")

    # 1) Update explicit master keys first.
    for key in args.relation_key:
        update_master_by_key(key)

    # 2) Update by relation IDs (to-be or existing), then linked master.
    for rel_id in args.relation_id:
        rel_id = rel_id.strip()
        target_db = to_be_db if rel_id.upper().startswith("TG") else existing_db
        row = notion.query_by_title(target_db, "Relation ID", rel_id)
        if not row:
            # fallback: search the other db
            other_db = existing_db if target_db == to_be_db else to_be_db
            row = notion.query_by_title(other_db, "Relation ID", rel_id)
            target_db = other_db if row else target_db
        if not row:
            print(f"[WARN] Relation ID not found: {rel_id}")
            continue

        props = filter_updates_for_row(row, generic_updates)
        notion.patch_page(row["id"], props)
        print(f"[OK] Relation updated: {rel_id}")

        key = relation_key_from_row(row)
        if key and key not in touched_master:
            update_master_by_key(key)

    print("Done.")


if __name__ == "__main__":
    main()

