"""
Create/update Notion relation tracker databases and load rows from CSV files.

This creates three databases under a Notion page:
1) Relations Master (DB)
2) Relations Existing (DB)
3) Relations To-Be (DB)

Data source files:
- docs/RELATIONS_MASTER.csv
- docs/RELATIONS_EXISTING.csv
- docs/RELATIONS_TO_BE.csv

Usage:
    python scripts/create_notion_relations_registry.py --page <NOTION_PAGE_URL_OR_ID>
    python scripts/create_notion_relations_registry.py --page <PAGE> --dry-run
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
MASTER_CSV = ROOT / "docs" / "RELATIONS_MASTER.csv"
EXISTING_CSV = ROOT / "docs" / "RELATIONS_EXISTING.csv"
TO_BE_CSV = ROOT / "docs" / "RELATIONS_TO_BE.csv"

NOTION_VERSION = "2022-06-28"

load_dotenv(dotenv_path=ROOT / ".env")


def load_notion_token() -> str:
    token = os.getenv("NOTION_TOKEN", "").strip()
    if token:
        return token

    env_path = ROOT / ".env"
    if not env_path.exists():
        return ""

    for raw in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip().lstrip("\ufeff") == "NOTION_TOKEN":
            return value.strip()

    return ""


def extract_page_id(url_or_id: str) -> str:
    cleaned = url_or_id.split("?")[0]
    pattern = r"[a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
    match = re.search(pattern, cleaned, re.IGNORECASE)
    if not match:
        raise ValueError(f"Could not extract Notion page ID from: {url_or_id}")
    return match.group(0).replace("-", "")


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def rich_text_payload(value: str) -> Dict[str, Any]:
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


def title_payload(value: str) -> Dict[str, Any]:
    value = str(value or "").strip()
    return {
        "title": [
            {
                "type": "text",
                "text": {"content": value[:2000]},
            }
        ]
    }


def checkbox_payload(value: Any) -> Dict[str, Any]:
    return {"checkbox": as_bool(value)}


def select_payload(value: str) -> Dict[str, Any]:
    value = str(value or "").strip()
    if not value:
        return {"select": None}
    return {"select": {"name": value}}


def date_payload(value: str) -> Dict[str, Any]:
    value = str(value or "").strip()
    if not value:
        return {"date": None}
    return {"date": {"start": value}}


def options(values: Iterable[str]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for value in values:
        label = str(value).strip()
        if label:
            out.append({"name": label, "color": "default"})
    return out


class NotionClient:
    def __init__(self, token: str, *, dry_run: bool = False):
        self.token = token
        self.dry_run = dry_run
        self.base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base}{path}"
        resp = requests.request(
            method,
            url,
            headers=self.headers,
            params=params,
            json=json_body,
            timeout=60,
        )
        if resp.status_code >= 300:
            raise RuntimeError(f"{method} {path} failed ({resp.status_code}): {resp.text}")
        if not resp.text:
            return {}
        return resp.json()

    def verify_access(self) -> None:
        self._request("GET", "/users/me")

    def list_page_children(self, page_id: str) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        while True:
            params: Dict[str, Any] = {"page_size": 100}
            if cursor:
                params["start_cursor"] = cursor
            payload = self._request("GET", f"/blocks/{page_id}/children", params=params)
            items.extend(payload.get("results", []))
            if not payload.get("has_more"):
                break
            cursor = payload.get("next_cursor")
        return items

    def find_child_database(self, page_id: str, title: str) -> Optional[str]:
        target = title.strip().lower()
        for block in self.list_page_children(page_id):
            if block.get("type") != "child_database":
                continue
            block_title = str(block.get("child_database", {}).get("title", "")).strip().lower()
            if block_title == target:
                return block.get("id")
        return None

    def create_database(
        self,
        page_id: str,
        *,
        title: str,
        icon: str,
        properties: Dict[str, Any],
    ) -> str:
        if self.dry_run:
            print(f"[DRY-RUN] Would create database: {title}")
            return f"dry-run-{title.lower().replace(' ', '-')}"
        payload = {
            "parent": {"page_id": page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "icon": {"type": "emoji", "emoji": icon},
            "properties": properties,
        }
        data = self._request("POST", "/databases", json_body=payload)
        return str(data["id"])

    def patch_database_properties(self, database_id: str, properties: Dict[str, Any]) -> None:
        if self.dry_run:
            print(f"[DRY-RUN] Would patch database properties: {database_id}")
            return
        self._request(
            "PATCH",
            f"/databases/{database_id}",
            json_body={"properties": properties},
        )

    def ensure_database(
        self,
        page_id: str,
        *,
        title: str,
        icon: str,
        properties: Dict[str, Any],
    ) -> str:
        existing_id = self.find_child_database(page_id, title)
        if existing_id:
            print(f"[OK] Found database: {title} ({existing_id})")
            self.patch_database_properties(existing_id, properties)
            return existing_id
        db_id = self.create_database(page_id, title=title, icon=icon, properties=properties)
        print(f"[OK] Created database: {title} ({db_id})")
        return db_id

    def query_page_by_title(
        self, database_id: str, title_property: str, value: str
    ) -> Optional[Dict[str, Any]]:
        if self.dry_run:
            return None
        payload = {
            "filter": {
                "property": title_property,
                "title": {"equals": value},
            },
            "page_size": 1,
        }
        data = self._request("POST", f"/databases/{database_id}/query", json_body=payload)
        rows = data.get("results", [])
        return rows[0] if rows else None

    def create_page(self, database_id: str, properties: Dict[str, Any]) -> str:
        if self.dry_run:
            print(f"[DRY-RUN] Would create page in {database_id}")
            return "dry-run-page"
        payload = {"parent": {"database_id": database_id}, "properties": properties}
        data = self._request("POST", "/pages", json_body=payload)
        return str(data["id"])

    def patch_page(self, page_id: str, properties: Dict[str, Any]) -> None:
        if self.dry_run:
            print(f"[DRY-RUN] Would patch page: {page_id}")
            return
        self._request("PATCH", f"/pages/{page_id}", json_body={"properties": properties})

    def upsert_page(
        self,
        database_id: str,
        *,
        title_property: str,
        title_value: str,
        properties: Dict[str, Any],
    ) -> str:
        existing = self.query_page_by_title(database_id, title_property, title_value)
        if existing:
            page_id = str(existing["id"])
            self.patch_page(page_id, properties)
            return page_id
        return self.create_page(database_id, properties)


def master_db_schema() -> Dict[str, Any]:
    return {
        "Relation Key": {"title": {}},
        "From Table": {"rich_text": {}},
        "From Column": {"rich_text": {}},
        "To Table": {"rich_text": {}},
        "To Column": {"rich_text": {}},
        "Relation Type": {
            "select": {
                "options": options(
                    [
                        "schema_fk",
                        "many-to-many",
                        "mapping_rule",
                        "edge_registry",
                        "live_fk",
                        "derived_live",
                    ]
                )
            }
        },
        "Source Status": {"select": {"options": options(["existing", "to_be", "both"])}},
        "In Existing": {"checkbox": {}},
        "In To Be": {"checkbox": {}},
        "Current State": {
            "select": {
                "options": options(
                    [
                        "live",
                        "live_fk",
                        "derived_live",
                        "live_edge_table",
                        "not_created",
                        "missing_fk",
                        "text_link_only",
                        "json_link_only",
                    ]
                )
            }
        },
        "Next Action": {"rich_text": {}},
        "Phase": {"select": {"options": options(["P0", "P1", "P2", "P3", "P4", "Parked"])}},
        "On Supabase": {"checkbox": {}},
        "Supabase Configured": {"checkbox": {}},
        "Needs More Data": {"checkbox": {}},
        "On Convex": {"checkbox": {}},
        "Convex Configured": {"checkbox": {}},
        "Convex Synced": {"checkbox": {}},
        "Ready For Launch": {"checkbox": {}},
        "Mach Layer": {"select": {"options": options(["Core", "Mach1.1", "Advanced"])}},
        "Last Checked": {"date": {}},
        "Notes": {"rich_text": {}},
    }


def existing_db_schema() -> Dict[str, Any]:
    return {
        "Relation ID": {"title": {}},
        "From Table": {"rich_text": {}},
        "From Column": {"rich_text": {}},
        "To Table": {"rich_text": {}},
        "To Column": {"rich_text": {}},
        "Relation Type": {
            "select": {"options": options(["many-to-one", "many-to-many", "schema_fk", "edge_registry"])}
        },
        "Join Table": {"rich_text": {}},
        "State": {"select": {"options": options(["live_fk", "derived_live"])}},
        "Source": {"rich_text": {}},
        "On Supabase": {"checkbox": {}},
        "Ready For Launch": {"checkbox": {}},
        "Notes": {"rich_text": {}},
    }


def to_be_db_schema() -> Dict[str, Any]:
    return {
        "Relation ID": {"title": {}},
        "From Table": {"rich_text": {}},
        "From Column": {"rich_text": {}},
        "To Table": {"rich_text": {}},
        "To Column": {"rich_text": {}},
        "Target Type": {
            "select": {"options": options(["schema_fk", "mapping_rule", "edge_registry"])}
        },
        "Current State": {
            "select": {
                "options": options(
                    [
                        "live",
                        "not_created",
                        "missing_fk",
                        "text_link_only",
                        "json_link_only",
                        "live_edge_table",
                    ]
                )
            }
        },
        "Next Action": {"rich_text": {}},
        "Phase": {"select": {"options": options(["P0", "P1", "P2", "P3", "P4", "Parked"])}},
        "On Supabase": {"checkbox": {}},
        "Supabase Configured": {"checkbox": {}},
        "Needs More Data": {"checkbox": {}},
        "On Convex": {"checkbox": {}},
        "Convex Configured": {"checkbox": {}},
        "Ready For Launch": {"checkbox": {}},
        "Mach Layer": {"select": {"options": options(["Core", "Mach1.1", "Advanced"])}},
        "Notes": {"rich_text": {}},
    }


def relation_link_property(target_database_id: str) -> Dict[str, Any]:
    return {
        "Master Link": {
            "relation": {
                "database_id": target_database_id,
                "single_property": {},
            }
        }
    }


def load_rows() -> Tuple[List[Dict[str, str]], List[Dict[str, str]], List[Dict[str, str]]]:
    if not MASTER_CSV.exists():
        raise RuntimeError("docs/RELATIONS_MASTER.csv not found. Run build_relations_master_csv.py first.")
    return read_csv(MASTER_CSV), read_csv(EXISTING_CSV), read_csv(TO_BE_CSV)


def build_master_properties(row: Dict[str, str], today: str) -> Dict[str, Any]:
    return {
        "Relation Key": title_payload(row.get("relation_key", "")),
        "From Table": rich_text_payload(row.get("from_table", "")),
        "From Column": rich_text_payload(row.get("from_column", "")),
        "To Table": rich_text_payload(row.get("to_table", "")),
        "To Column": rich_text_payload(row.get("to_column", "")),
        "Relation Type": select_payload(row.get("relation_type", "")),
        "Source Status": select_payload(row.get("source_status", "")),
        "In Existing": checkbox_payload(row.get("in_existing", False)),
        "In To Be": checkbox_payload(row.get("in_to_be", False)),
        "Current State": select_payload(row.get("current_state", "")),
        "Next Action": rich_text_payload(row.get("next_action", "")),
        "Phase": select_payload(row.get("phase", "")),
        "On Supabase": checkbox_payload(row.get("on_supabase", False)),
        "Supabase Configured": checkbox_payload(row.get("supabase_configured", False)),
        "Needs More Data": checkbox_payload(row.get("needs_more_data", False)),
        "On Convex": checkbox_payload(row.get("on_convex", False)),
        "Convex Configured": checkbox_payload(row.get("convex_configured", False)),
        "Convex Synced": checkbox_payload(row.get("convex_synced", False)),
        "Ready For Launch": checkbox_payload(row.get("ready_for_launch", False)),
        "Mach Layer": select_payload(row.get("mach_layer", "Core")),
        "Last Checked": date_payload(today),
        "Notes": rich_text_payload(row.get("notes", "")),
    }


def build_existing_properties(
    row: Dict[str, str], master_page_id: Optional[str]
) -> Dict[str, Any]:
    props: Dict[str, Any] = {
        "Relation ID": title_payload(row.get("relation_id", "")),
        "From Table": rich_text_payload(row.get("from_table", "")),
        "From Column": rich_text_payload(row.get("from_column", "")),
        "To Table": rich_text_payload(row.get("to_table", "")),
        "To Column": rich_text_payload(row.get("to_column", "")),
        "Relation Type": select_payload(row.get("relation_type", "")),
        "Join Table": rich_text_payload(row.get("join_table", "")),
        "State": select_payload(row.get("state", "")),
        "Source": rich_text_payload(row.get("source", "")),
        "On Supabase": checkbox_payload(True),
        "Ready For Launch": checkbox_payload(
            row.get("state", "").strip() in {"live_fk", "derived_live"}
        ),
        "Notes": rich_text_payload(""),
    }
    if master_page_id:
        props["Master Link"] = {"relation": [{"id": master_page_id}]}
    return props


def build_to_be_properties(
    row: Dict[str, str], master_page_id: Optional[str]
) -> Dict[str, Any]:
    state = row.get("current_state", "").strip()
    next_action = row.get("next_action", "").strip()
    on_supabase = state != "not_created"
    supabase_configured = state in {"live", "live_fk", "derived_live", "live_edge_table"}
    needs_more_data = state in {"text_link_only", "json_link_only"} or "stabilize_lookup_key" in next_action

    props: Dict[str, Any] = {
        "Relation ID": title_payload(row.get("relation_id", "")),
        "From Table": rich_text_payload(row.get("from_table", "")),
        "From Column": rich_text_payload(row.get("from_column", "")),
        "To Table": rich_text_payload(row.get("to_table", "")),
        "To Column": rich_text_payload(row.get("to_column", "")),
        "Target Type": select_payload(row.get("target_type", "")),
        "Current State": select_payload(state),
        "Next Action": rich_text_payload(next_action),
        "Phase": select_payload(row.get("phase", "")),
        "On Supabase": checkbox_payload(on_supabase),
        "Supabase Configured": checkbox_payload(supabase_configured),
        "Needs More Data": checkbox_payload(needs_more_data),
        "On Convex": checkbox_payload(False),
        "Convex Configured": checkbox_payload(False),
        "Ready For Launch": checkbox_payload(supabase_configured and not needs_more_data),
        "Mach Layer": select_payload("Core"),
        "Notes": rich_text_payload(row.get("notes", "")),
    }
    if master_page_id:
        props["Master Link"] = {"relation": [{"id": master_page_id}]}
    return props


def build_master_index(master_rows: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    out: Dict[str, Dict[str, str]] = {}
    for row in master_rows:
        key = row.get("relation_key", "").strip()
        if key:
            out[key] = row
    return out


def relation_key(row: Dict[str, str]) -> str:
    return (
        f"{row.get('from_table', '').strip()}."
        f"{row.get('from_column', '').strip()}->"
        f"{row.get('to_table', '').strip()}."
        f"{row.get('to_column', '').strip()}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Notion relation registry databases")
    parser.add_argument("--page", required=True, help="Notion page URL or ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    page_id = extract_page_id(args.page)
    master_rows, existing_rows, to_be_rows = load_rows()
    print(f"Loaded rows: master={len(master_rows)}, existing={len(existing_rows)}, to_be={len(to_be_rows)}")

    token = load_notion_token()
    if not token:
        if args.dry_run:
            print("NOTION_TOKEN is not set. Dry run only.")
            return
        raise RuntimeError("NOTION_TOKEN is not set. Set it in environment and run again.")

    notion = NotionClient(token=token, dry_run=args.dry_run)
    if not args.dry_run:
        notion.verify_access()
        print("Verified Notion access.")

    # 1) Ensure all three databases exist.
    master_db_id = notion.ensure_database(
        page_id,
        title="Relations Master (DB)",
        icon="🧭",
        properties=master_db_schema(),
    )
    existing_db_id = notion.ensure_database(
        page_id,
        title="Relations Existing (DB)",
        icon="✅",
        properties=existing_db_schema(),
    )
    to_be_db_id = notion.ensure_database(
        page_id,
        title="Relations To-Be (DB)",
        icon="🛠️",
        properties=to_be_db_schema(),
    )

    # 2) Add relation link from existing/to-be to master.
    notion.patch_database_properties(existing_db_id, relation_link_property(master_db_id))
    notion.patch_database_properties(to_be_db_id, relation_link_property(master_db_id))

    # 3) Upsert master rows and keep page id map by relation_key.
    master_page_ids: Dict[str, str] = {}
    today = dt.date.today().isoformat()
    for row in master_rows:
        key = row.get("relation_key", "").strip()
        props = build_master_properties(row, today)
        page_id_out = notion.upsert_page(
            master_db_id,
            title_property="Relation Key",
            title_value=key,
            properties=props,
        )
        master_page_ids[key] = page_id_out

    # 4) Upsert existing rows with master link.
    master_index = build_master_index(master_rows)
    for row in existing_rows:
        key = relation_key(row)
        master_page_id = master_page_ids.get(key)
        if not master_page_id and key in master_index:
            # Dry-run fallback; no page id available.
            master_page_id = None
        props = build_existing_properties(row, master_page_id)
        notion.upsert_page(
            existing_db_id,
            title_property="Relation ID",
            title_value=row.get("relation_id", "").strip(),
            properties=props,
        )

    # 5) Upsert to-be rows with master link.
    for row in to_be_rows:
        key = relation_key(row)
        master_page_id = master_page_ids.get(key)
        if not master_page_id and key in master_index:
            master_page_id = None
        props = build_to_be_properties(row, master_page_id)
        notion.upsert_page(
            to_be_db_id,
            title_property="Relation ID",
            title_value=row.get("relation_id", "").strip(),
            properties=props,
        )

    print("Done. Notion relation registry is ready.")


if __name__ == "__main__":
    main()
