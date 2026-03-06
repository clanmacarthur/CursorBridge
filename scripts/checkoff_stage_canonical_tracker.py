"""
Check off rows in the Notion "Stage To Canonical Tracker (DB)" database.

Examples:
  python scripts/checkoff_stage_canonical_tracker.py --task "Run P1 migration batch"
  python scripts/checkoff_stage_canonical_tracker.py --phase P1 --only-status "In Progress"
  python scripts/checkoff_stage_canonical_tracker.py --phase P2
  python scripts/checkoff_stage_canonical_tracker.py --task "Run P1 migration batch" --status Blocked --blocked true --completed false
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
CONFIG_PATH = ROOT / "config" / "notion_db_ids.json"
NOTION_VERSION = "2022-06-28"


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

    def query_rows(self, db_id: str, filter_body: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        while True:
            body: Dict[str, Any] = {"page_size": 100}
            if filter_body:
                body["filter"] = filter_body
            if cursor:
                body["start_cursor"] = cursor
            data = self.request("POST", f"/databases/{db_id}/query", body)
            out.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return out

    def patch_page(self, page_id: str, properties: Dict[str, Any]) -> None:
        self.request("PATCH", f"/pages/{page_id}", {"properties": properties})


def plain_title(row: Dict[str, Any]) -> str:
    props = row.get("properties", {})
    task_prop = props.get("Task", {})
    return "".join([t.get("plain_text", "") for t in task_prop.get("title", [])]).strip()


def rich_text(value: str) -> Dict[str, Any]:
    if not value:
        return {"rich_text": []}
    return {"rich_text": [{"type": "text", "text": {"content": value[:2000]}}]}


def select_value(value: str) -> Dict[str, Any]:
    if not value:
        return {"select": None}
    return {"select": {"name": value}}


def checkbox(value: bool) -> Dict[str, Any]:
    return {"checkbox": bool(value)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check off Stage To Canonical Tracker tasks in Notion")
    parser.add_argument("--task", action="append", default=[], help="Exact task title (can be repeated)")
    parser.add_argument("--phase", help="Setup|P1|P2|P3|Verify")
    parser.add_argument(
        "--only-status",
        help="Optional status filter when using --phase (for example: Pending, In Progress)",
    )
    parser.add_argument("--note", default="", help="Optional note appended to Notes")
    parser.add_argument("--in-progress", action="store_true", help="Mark status as In Progress instead of Done")
    parser.add_argument("--status", help="Explicit status (Pending|In Progress|Done|Blocked)")
    parser.add_argument("--completed", help="Explicit completed value (true/false)")
    parser.add_argument("--blocked", help="Explicit blocked value (true/false)")
    args = parser.parse_args()

    if not args.task and not args.phase:
        raise RuntimeError("Provide at least one --task or --phase")

    token = load_notion_token()
    if not token:
        raise RuntimeError("NOTION_TOKEN not found")

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    db_id = str(config.get("stage_to_canonical_tracker", "")).replace("-", "")
    if not db_id:
        raise RuntimeError("Missing stage_to_canonical_tracker in config/notion_db_ids.json")

    notion = NotionClient(token)
    notion.verify()

    targets: List[Dict[str, Any]] = []
    if args.task:
        for task_title in args.task:
            rows = notion.query_rows(
                db_id,
                {"property": "Task", "title": {"equals": task_title}},
            )
            targets.extend(rows)

    if args.phase:
        phase_filter: Dict[str, Any] = {"property": "Phase", "select": {"equals": args.phase}}
        if args.only_status:
            phase_filter = {
                "and": [
                    {"property": "Phase", "select": {"equals": args.phase}},
                    {"property": "Status", "select": {"equals": args.only_status}},
                ]
            }
        rows = notion.query_rows(db_id, phase_filter)
        targets.extend(rows)

    # Deduplicate by row id.
    unique: Dict[str, Dict[str, Any]] = {}
    for row in targets:
        unique[str(row.get("id", ""))] = row

    if not unique:
        print("No matching rows found.")
        return

    def as_bool(value: str) -> bool:
        return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}

    if args.status or args.completed is not None or args.blocked is not None:
        status_name = (args.status or "Pending").strip()
        completed_value = as_bool(args.completed) if args.completed is not None else (status_name == "Done")
        blocked_value = as_bool(args.blocked) if args.blocked is not None else (status_name == "Blocked")
    else:
        status_name = "In Progress" if args.in_progress else "Done"
        completed_value = False if args.in_progress else True
        blocked_value = False

    updated = 0
    for page_id, row in unique.items():
        note_text = args.note.strip()
        if note_text:
            task_name = plain_title(row)
            note_text = f"{task_name}: {note_text}"
        props = {
            "Status": select_value(status_name),
            "Completed": checkbox(completed_value),
            "Blocked": checkbox(blocked_value),
        }
        if note_text:
            props["Notes"] = rich_text(note_text)
        notion.patch_page(page_id, props)
        updated += 1

    print(f"Updated rows: {updated}")


if __name__ == "__main__":
    main()
