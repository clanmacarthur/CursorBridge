"""
Create or update the Notion tracker DB for stage->canonical migration tasks.

What it does:
- Ensures a child database exists under the root project page:
  "Stage To Canonical Tracker (DB)"
- Ensures all migration tasks are present (upsert by task title).
- Writes result to docs/_notion_stage_canonical_tracker_result.json.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
PROJECT_RESULT_PATH = ROOT / "docs" / "_notion_project_creation_result.json"
CONFIG_PATH = ROOT / "config" / "notion_db_ids.json"
OUTPUT_PATH = ROOT / "docs" / "_notion_stage_canonical_tracker_result.json"

NOTION_VERSION = "2022-06-28"
TRACKER_TITLE = "Stage To Canonical Tracker (DB)"


TASK_ROWS: List[Dict[str, str]] = [
    {
        "task": "Confirm Supabase freeze and Convex-major-change policy",
        "phase": "Setup",
        "sql_file": "-",
        "stage_table": "-",
        "notes": "Supabase stays stable; major structural changes happen in Convex migration.",
    },
    {
        "task": "Run helper in Supabase SQL editor",
        "phase": "Setup",
        "sql_file": "sql/stage_to_canonical/00_migrate_helper.sql",
        "stage_table": "-",
        "notes": "Create migration helper function before any batch.",
    },
    {
        "task": "Run read-only preflight and capture stop decision",
        "phase": "Setup",
        "sql_file": "sql/stage_to_canonical/01_preflight_readonly.sql",
        "stage_table": "all",
        "notes": "Read-only check. If stop condition appears, do not run P1/P2/P3 yet.",
    },
    {
        "task": "Run P1 migration batch",
        "phase": "P1",
        "sql_file": "sql/stage_to_canonical/P1_safety_and_runtime.sql",
        "stage_table": "P1 batch",
        "notes": "Run full P1 batch.",
    },
    {
        "task": "Verify during_session_stop_triggers stage migration",
        "phase": "P1",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "during_session_stop_triggers_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify contraindications mandatory disclosure stage migration",
        "phase": "P1",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "contraindications_mandatory_disclosure_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify breathwork master taxonomy stage migration",
        "phase": "P1",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "breathwork_master_taxonomy_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify daily regulation sliders stage migration",
        "phase": "P1",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "daily_regulation_sliders_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify controls library design stage migration",
        "phase": "P1",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "controls_library_design_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Run P2 migration batch",
        "phase": "P2",
        "sql_file": "sql/stage_to_canonical/P2_ontology_expansion.sql",
        "stage_table": "P2 batch",
        "notes": "Run full P2 batch.",
    },
    {
        "task": "Verify nadi system stage migration",
        "phase": "P2",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "nadi_system_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify astrology calendrical systems stage migration",
        "phase": "P2",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "astrology_calendrical_systems_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify emotion brain body energy mapping stage migration",
        "phase": "P2",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "emotion_brain_body_energy_mapping_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify full brain neural systems table stage migration",
        "phase": "P2",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "full_brain_neural_systems_table_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Run P3 migration batch",
        "phase": "P3",
        "sql_file": "sql/stage_to_canonical/P3_symbolic_layers.sql",
        "stage_table": "P3 batch",
        "notes": "Run full P3 batch.",
    },
    {
        "task": "Verify mythological beings stage migration",
        "phase": "P3",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "mythological_beings_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify sacred animals stage migration",
        "phase": "P3",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "sacred_animals_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Verify stones minerals stage migration",
        "phase": "P3",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "stones_minerals_stage",
        "notes": "Check stage vs canonical row counts.",
    },
    {
        "task": "Run final verification query",
        "phase": "Verify",
        "sql_file": "sql/stage_to_canonical/99_verify_counts.sql",
        "stage_table": "all",
        "notes": "Capture final migration status for all stage tables.",
    },
]


def load_notion_token() -> str:
    token = os.getenv("NOTION_TOKEN", "").strip()
    if token:
        return token
    if not ENV_PATH.exists():
        return ""
    for raw in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip().lstrip("\ufeff") == "NOTION_TOKEN":
            return value.strip().strip('"').strip("'")
    return ""


class NotionClient:
    def __init__(self, token: str):
        self.base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def request(self, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = requests.request(
            method,
            f"{self.base}{path}",
            headers=self.headers,
            json=body,
            timeout=60,
        )
        if resp.status_code >= 300:
            raise RuntimeError(f"{method} {path} failed ({resp.status_code}): {resp.text}")
        if not resp.text:
            return {}
        return resp.json()

    def verify(self) -> None:
        self.request("GET", "/users/me")

    def list_child_blocks(self, page_id: str) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        while True:
            path = f"/blocks/{page_id}/children?page_size=100"
            if cursor:
                path += f"&start_cursor={cursor}"
            data = self.request("GET", path)
            out.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return out

    def find_child_database(self, page_id: str, title: str) -> Optional[str]:
        title_l = title.strip().lower()
        for block in self.list_child_blocks(page_id):
            if block.get("type") != "child_database":
                continue
            block_title = str(block.get("child_database", {}).get("title", "")).strip().lower()
            if block_title == title_l:
                return str(block.get("id", ""))
        return None

    def create_database(self, page_id: str, title: str, properties: Dict[str, Any]) -> str:
        body = {
            "parent": {"type": "page_id", "page_id": page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        }
        data = self.request("POST", "/databases", body)
        return str(data.get("id", ""))

    def patch_database_properties(self, database_id: str, properties: Dict[str, Any]) -> None:
        self.request("PATCH", f"/databases/{database_id}", {"properties": properties})

    def query_by_title(self, database_id: str, title_property: str, value: str) -> Optional[Dict[str, Any]]:
        body = {
            "filter": {
                "property": title_property,
                "title": {"equals": value},
            },
            "page_size": 1,
        }
        data = self.request("POST", f"/databases/{database_id}/query", body)
        rows = data.get("results", [])
        return rows[0] if rows else None

    def create_page(self, database_id: str, properties: Dict[str, Any]) -> str:
        data = self.request(
            "POST",
            "/pages",
            {"parent": {"database_id": database_id}, "properties": properties},
        )
        return str(data.get("id", ""))

    def patch_page(self, page_id: str, properties: Dict[str, Any]) -> None:
        self.request("PATCH", f"/pages/{page_id}", {"properties": properties})


def title_prop(value: str) -> Dict[str, Any]:
    return {"title": [{"type": "text", "text": {"content": value[:2000]}}]}


def rich_text_prop(value: str) -> Dict[str, Any]:
    if not value:
        return {"rich_text": []}
    return {"rich_text": [{"type": "text", "text": {"content": value[:2000]}}]}


def select_prop(value: str) -> Dict[str, Any]:
    if not value:
        return {"select": None}
    return {"select": {"name": value}}


def checkbox_prop(value: bool) -> Dict[str, Any]:
    return {"checkbox": bool(value)}


def number_prop(value: int) -> Dict[str, Any]:
    return {"number": int(value)}


def tracker_properties() -> Dict[str, Any]:
    return {
        "Task": {"title": {}},
        "Phase": {
            "select": {
                "options": [
                    {"name": "Setup", "color": "gray"},
                    {"name": "P1", "color": "blue"},
                    {"name": "P2", "color": "green"},
                    {"name": "P3", "color": "orange"},
                    {"name": "Verify", "color": "purple"},
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Pending", "color": "gray"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Done", "color": "green"},
                    {"name": "Blocked", "color": "red"},
                ]
            }
        },
        "SQL File": {"rich_text": {}},
        "Stage Table": {"rich_text": {}},
        "Completed": {"checkbox": {}},
        "Blocked": {"checkbox": {}},
        "Ready": {"checkbox": {}},
        "Order": {"number": {"format": "number"}},
        "Notes": {"rich_text": {}},
    }


def build_task_properties(row: Dict[str, str], order: int) -> Dict[str, Any]:
    return {
        "Task": title_prop(row["task"]),
        "Phase": select_prop(row["phase"]),
        "Status": select_prop("Pending"),
        "SQL File": rich_text_prop(row["sql_file"]),
        "Stage Table": rich_text_prop(row["stage_table"]),
        "Completed": checkbox_prop(False),
        "Blocked": checkbox_prop(False),
        "Ready": checkbox_prop(True),
        "Order": number_prop(order),
        "Notes": rich_text_prop(row["notes"]),
    }


def upsert_task_rows(notion: NotionClient, database_id: str) -> Dict[str, int]:
    created = 0
    updated = 0
    for idx, row in enumerate(TASK_ROWS, start=1):
        props = build_task_properties(row, idx)
        existing = notion.query_by_title(database_id, "Task", row["task"])
        if existing is None:
            notion.create_page(database_id, props)
            created += 1
        else:
            notion.patch_page(str(existing.get("id", "")), props)
            updated += 1
    return {"created": created, "updated": updated}


def main() -> None:
    token = load_notion_token()
    if not token:
        raise RuntimeError("NOTION_TOKEN not found")

    project_result = json.loads(PROJECT_RESULT_PATH.read_text(encoding="utf-8"))
    root_page_id = str(project_result.get("root_project_row", {}).get("id", "")).replace("-", "")
    if not root_page_id:
        raise RuntimeError("Root Notion project page id not found in docs/_notion_project_creation_result.json")

    notion = NotionClient(token)
    notion.verify()

    db_id = notion.find_child_database(root_page_id, TRACKER_TITLE)
    created_db = False
    if db_id is None:
        db_id = notion.create_database(root_page_id, TRACKER_TITLE, tracker_properties())
        created_db = True
    else:
        notion.patch_database_properties(db_id, tracker_properties())

    counts = upsert_task_rows(notion, db_id)

    # Save db id into config/notion_db_ids.json for future scripts.
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    config["stage_to_canonical_tracker"] = db_id.replace("-", "")
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = {
        "database_id": db_id,
        "database_url": f"https://www.notion.so/{db_id.replace('-', '')}",
        "database_title": TRACKER_TITLE,
        "created_database": created_db,
        "task_rows_total": len(TASK_ROWS),
        "rows_created": counts["created"],
        "rows_updated": counts["updated"],
        "config_updated": str(CONFIG_PATH),
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
