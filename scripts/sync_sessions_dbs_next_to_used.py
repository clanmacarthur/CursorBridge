"""
Sync Notion databases from a source page into a target page as links.

Why this exists:
- The Notion API does not provide a stable "move database to new parent page" path.
- For safe, repeatable operation, this script creates missing `link_to_page` database
  blocks on the target page.

Default pages:
- source: Therapeutic next basic
- target: Therapeutic USED

Usage:
  python scripts/sync_sessions_dbs_next_to_used.py
  python scripts/sync_sessions_dbs_next_to_used.py --dry-run
  python scripts/sync_sessions_dbs_next_to_used.py --source <PAGE_URL_OR_ID> --target <PAGE_URL_OR_ID>
  python scripts/sync_sessions_dbs_next_to_used.py --only-config
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "notion_db_ids.json"
REPORT_PATH = ROOT / "docs" / "_notion_next_to_used_sessions_sync.json"
ENV_PATH = ROOT / ".env"

NOTION_VERSION = "2022-06-28"

DEFAULT_SOURCE = "2d9c47c61e2180a1848bd93728f116cd"  # Therapeutic next basic
DEFAULT_TARGET = "2d9c47c61e218057962ae39660bd641e"  # Therapeutic USED

ADMIN_KEYS = {
    "relations_master",
    "relations_existing",
    "relations_to_be",
    "stage_to_canonical_tracker",
}


def extract_notion_id(url_or_id: str) -> str:
    cleaned = (url_or_id or "").strip().split("?", 1)[0]
    pattern = r"[a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
    match = re.search(pattern, cleaned, re.IGNORECASE)
    if not match:
        raise ValueError(f"Could not extract Notion ID from: {url_or_id}")
    return match.group(0).replace("-", "")


def as_uuid(value: str) -> str:
    v = str(value or "").replace("-", "").strip()
    if len(v) != 32:
        return value
    return f"{v[0:8]}-{v[8:12]}-{v[12:16]}-{v[16:20]}-{v[20:32]}"


def load_notion_token() -> str:
    load_dotenv(dotenv_path=ENV_PATH)
    env_token = os.getenv("NOTION_TOKEN", "").strip()
    if env_token:
        return env_token

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


class NotionClient:
    def __init__(self, token: str) -> None:
        self.base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
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
        resp = requests.request(
            method,
            f"{self.base}{path}",
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

    def verify(self) -> None:
        self._request("GET", "/users/me")

    def list_block_children(self, block_id: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        while True:
            params: Dict[str, Any] = {"page_size": 100}
            if cursor:
                params["start_cursor"] = cursor
            data = self._request("GET", f"/blocks/{block_id}/children", params=params)
            rows.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return rows

    def append_blocks(self, block_id: str, children: List[Dict[str, Any]]) -> None:
        if not children:
            return
        self._request("PATCH", f"/blocks/{block_id}/children", json_body={"children": children})


def load_config_map() -> Dict[str, str]:
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    out: Dict[str, str] = {}
    for key, dbid in data.items():
        if key in ADMIN_KEYS:
            continue
        out[key] = str(dbid).replace("-", "")
    return out


def invert_map(key_to_id: Dict[str, str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key, dbid in key_to_id.items():
        out[dbid] = key
    return out


def collect_page_databases(
    notion: NotionClient, page_id: str, *, max_depth: int = 2, include_link_blocks: bool = True
) -> List[Dict[str, str]]:
    found: List[Dict[str, str]] = []
    seen_pages: Set[str] = set()

    def walk(block_id: str, depth: int, scope: str) -> None:
        if block_id in seen_pages:
            return
        seen_pages.add(block_id)
        for block in notion.list_block_children(block_id):
            btype = block.get("type")
            bid = str(block.get("id", "")).replace("-", "")
            if btype == "child_database":
                found.append(
                    {
                        "database_id": bid,
                        "title": str(block.get("child_database", {}).get("title", "")).strip(),
                        "scope": scope,
                    }
                )
            elif include_link_blocks and btype == "link_to_page":
                link = block.get("link_to_page", {})
                if link.get("type") == "database_id":
                    found.append(
                        {
                            "database_id": str(link.get("database_id", "")).replace("-", ""),
                            "title": "",
                            "scope": scope,
                        }
                    )
            elif include_link_blocks and btype in {
                "paragraph",
                "heading_1",
                "heading_2",
                "heading_3",
                "bulleted_list_item",
                "numbered_list_item",
                "toggle",
            }:
                rich = block.get(btype, {}).get("rich_text", [])
                for token in rich:
                    if token.get("type") != "mention":
                        continue
                    mention = token.get("mention", {})
                    if mention.get("type") != "database":
                        continue
                    dbid = str(mention.get("database", {}).get("id", "")).replace("-", "")
                    if dbid:
                        found.append(
                            {
                                "database_id": dbid,
                                "title": token.get("plain_text", "") or "",
                                "scope": scope,
                            }
                        )
            elif btype == "child_page" and depth < max_depth:
                title = str(block.get("child_page", {}).get("title", "")).strip()
                child_scope = f"{scope}/{title}" if title else scope
                walk(str(block.get("id")), depth + 1, child_scope)

    walk(page_id, 0, "root")
    return found


def make_heading_block(text: str) -> Dict[str, Any]:
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
        },
    }


def make_database_mention_block(database_id: str, key: str) -> Dict[str, Any]:
    prefix = f"{key}: " if key else "DB: "
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"type": "text", "text": {"content": prefix}},
                {
                    "type": "mention",
                    "mention": {"database": {"id": as_uuid(database_id)}},
                },
            ]
        },
    }


def chunks(items: List[Any], size: int) -> List[List[Any]]:
    out: List[List[Any]] = []
    idx = 0
    while idx < len(items):
        out.append(items[idx : idx + size])
        idx += size
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync Notion database links from NEXT page to USED page."
    )
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="Source page URL or ID")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="Target page URL or ID")
    parser.add_argument("--dry-run", action="store_true", help="Report only, no Notion writes")
    parser.add_argument(
        "--only-config",
        action="store_true",
        help="Only include database IDs that exist in config/notion_db_ids.json",
    )
    args = parser.parse_args()

    token = load_notion_token()
    if not token:
        raise RuntimeError("NOTION_TOKEN missing in .env")

    source_id = extract_notion_id(args.source)
    target_id = extract_notion_id(args.target)

    key_to_id = load_config_map()
    id_to_key = invert_map(key_to_id)

    notion = NotionClient(token)
    notion.verify()

    source_blocks = collect_page_databases(
        notion, source_id, max_depth=2, include_link_blocks=False
    )
    target_blocks = collect_page_databases(
        notion, target_id, max_depth=2, include_link_blocks=True
    )

    source_db_ids_all = sorted({row["database_id"] for row in source_blocks if row.get("database_id")})
    target_db_ids_all = {row["database_id"] for row in target_blocks if row.get("database_id")}

    if args.only_config:
        source_db_ids = [dbid for dbid in source_db_ids_all if dbid in id_to_key]
    else:
        source_db_ids = source_db_ids_all

    to_add = [dbid for dbid in source_db_ids if dbid not in target_db_ids_all]

    added: List[str] = []
    if not args.dry_run and to_add:
        stamp = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
        header = make_heading_block(f"Sessions DB links synced from NEXT ({stamp})")
        notion.append_blocks(target_id, [header])
        for part in chunks(
            [make_database_mention_block(dbid, id_to_key.get(dbid, "")) for dbid in to_add], 90
        ):
            notion.append_blocks(target_id, part)
        added = to_add[:]

    report = {
        "generated_at_utc": dt.datetime.now(dt.UTC).isoformat(),
        "source_page_id": source_id,
        "target_page_id": target_id,
        "dry_run": args.dry_run,
        "mode": "only_config" if args.only_config else "all_source_databases",
        "source_database_count": len(source_db_ids),
        "target_database_count_before": len(target_db_ids_all),
        "added_count": len(added if not args.dry_run else to_add),
        "already_present_count": len(source_db_ids) - len(to_add),
        "source_databases": [
            {"database_id": dbid, "key": id_to_key.get(dbid, "")} for dbid in source_db_ids
        ],
        "added_databases": [
            {"database_id": dbid, "key": id_to_key.get(dbid, "")}
            for dbid in (added if not args.dry_run else to_add)
        ],
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Source DBs found: {len(source_db_ids)}")
    print(f"Already present on target: {len(source_db_ids) - len(to_add)}")
    print(f"Added now: {len(added) if not args.dry_run else 0}")
    print(f"Pending to add (dry run aware): {len(to_add)}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
