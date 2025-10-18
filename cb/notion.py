import os
from typing import Any, Dict, Optional

import requests


NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def _headers() -> Dict[str, str]:
    token = os.getenv("NOTION_TOKEN", "").strip()
    if not token:
        raise RuntimeError("NOTION_TOKEN not set in environment")
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def edit_page(page_id: str, append_text: Optional[str], properties: Dict[str, str]) -> None:
    if properties:
        props_payload: Dict[str, Any] = {}
        for name, value in properties.items():
            props_payload[name] = {"rich_text": [{"text": {"content": value}}]}
        resp = requests.patch(
            f"{NOTION_API_BASE}/pages/{page_id}",
            headers=_headers(),
            json={"properties": props_payload},
            timeout=30,
        )
        resp.raise_for_status()

    if append_text:
        resp = requests.patch(
            f"{NOTION_API_BASE}/blocks/{page_id}/children",
            headers=_headers(),
            json={
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": append_text}}]
                        },
                    }
                ]
            },
            timeout=30,
        )
        resp.raise_for_status()


def create_database_row(database_id: str, properties: Dict[str, str]) -> Dict[str, Any]:
    # Convert simple name=value map into Notion property objects (basic text/title)
    notion_props: Dict[str, Any] = {}
    for name, value in properties.items():
        # Heuristic: if field is 'Name' use title; otherwise rich_text
        if name.lower() == "name":
            notion_props[name] = {"title": [{"type": "text", "text": {"content": value}}]}
        else:
            notion_props[name] = {"rich_text": [{"type": "text", "text": {"content": value}}]}

    resp = requests.post(
        f"{NOTION_API_BASE}/pages",
        headers=_headers(),
        json={
            "parent": {"database_id": database_id},
            "properties": notion_props,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


