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


def _extract_property_value(prop: Dict[str, Any]) -> Any:
    """Extract a plain Python value from a Notion property object."""
    prop_type = prop.get("type", "")
    
    if prop_type == "title":
        parts = prop.get("title", [])
        return "".join(p.get("plain_text", "") for p in parts)
    
    if prop_type == "rich_text":
        parts = prop.get("rich_text", [])
        return "".join(p.get("plain_text", "") for p in parts)
    
    if prop_type == "number":
        return prop.get("number")
    
    if prop_type == "checkbox":
        return prop.get("checkbox", False)
    
    if prop_type == "date":
        date_obj = prop.get("date")
        if date_obj:
            return date_obj.get("start")
        return None
    
    if prop_type == "select":
        sel = prop.get("select")
        return sel.get("name") if sel else None
    
    if prop_type == "multi_select":
        items = prop.get("multi_select", [])
        return ", ".join(item.get("name", "") for item in items)
    
    if prop_type == "url":
        return prop.get("url")
    
    if prop_type == "email":
        return prop.get("email")
    
    if prop_type == "phone_number":
        return prop.get("phone_number")
    
    if prop_type == "status":
        status = prop.get("status")
        return status.get("name") if status else None
    
    if prop_type == "created_time":
        return prop.get("created_time")
    
    if prop_type == "last_edited_time":
        return prop.get("last_edited_time")
    
    if prop_type == "formula":
        formula = prop.get("formula", {})
        f_type = formula.get("type")
        return formula.get(f_type) if f_type else None
    
    if prop_type == "rollup":
        rollup = prop.get("rollup", {})
        r_type = rollup.get("type")
        return rollup.get(r_type) if r_type else None
    
    if prop_type == "relation":
        # Extract linked page IDs as comma-separated string
        relations = prop.get("relation", [])
        if relations:
            return ", ".join(rel.get("id", "") for rel in relations)
        return None
    
    if prop_type == "people":
        people = prop.get("people", [])
        if people:
            return ", ".join(p.get("name", p.get("id", "")) for p in people)
        return None
    
    if prop_type == "files":
        files = prop.get("files", [])
        if files:
            urls = []
            for f in files:
                if f.get("type") == "external":
                    urls.append(f.get("external", {}).get("url", ""))
                elif f.get("type") == "file":
                    urls.append(f.get("file", {}).get("url", ""))
            return ", ".join(urls) if urls else None
        return None
    
    # Fallback for unsupported types
    return None


def query_database(database_id: str, page_size: int = 100) -> Dict[str, Any]:
    """Query all rows from a Notion database with pagination.
    
    Returns:
        Dict with 'schema' (property name -> type mapping) and 'rows' (list of dicts).
    """
    all_results = []
    has_more = True
    next_cursor: Optional[str] = None
    schema: Dict[str, str] = {}
    
    while has_more:
        payload: Dict[str, Any] = {"page_size": page_size}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        
        resp = requests.post(
            f"{NOTION_API_BASE}/databases/{database_id}/query",
            headers=_headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        
        results = data.get("results", [])
        all_results.extend(results)
        
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")
    
    # Build schema from first result and extract rows
    rows = []
    for page in all_results:
        props = page.get("properties", {})
        row: Dict[str, Any] = {"_page_id": page.get("id")}
        
        for prop_name, prop_value in props.items():
            # Record schema on first pass
            if prop_name not in schema:
                schema[prop_name] = prop_value.get("type", "unknown")
            
            row[prop_name] = _extract_property_value(prop_value)
        
        rows.append(row)
    
    return {"schema": schema, "rows": rows}


