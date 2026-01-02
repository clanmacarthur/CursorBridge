"""
Create Notion databases from automation backbone template.

This script creates the missing automation databases in Notion
to mirror the Supabase automation tables.

Usage:
    python scripts/create_notion_databases.py --parent-page-id YOUR_PAGE_ID
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import requests

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"

if not NOTION_TOKEN:
    print("ERROR: NOTION_TOKEN not set in environment")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}


def load_template() -> Dict[str, Any]:
    """Load the database template JSON."""
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notion_automation_databases.json"
    )
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def notion_property_to_schema(prop_name: str, prop_def: Dict[str, Any]) -> Dict[str, Any]:
    """Convert our template property definition to Notion API schema."""
    prop_type = prop_def["type"]
    
    if prop_type == "title":
        return {"title": {}}
    
    elif prop_type == "text":
        return {"rich_text": {}}
    
    elif prop_type == "number":
        return {"number": {"format": "number"}}
    
    elif prop_type == "checkbox":
        return {"checkbox": {}}
    
    elif prop_type == "select":
        options = prop_def.get("options", [])
        return {
            "select": {
                "options": [{"name": opt, "color": "default"} for opt in options]
            }
        }
    
    elif prop_type == "multi_select":
        options = prop_def.get("options", [])
        return {
            "multi_select": {
                "options": [{"name": opt, "color": "default"} for opt in options]
            }
        }
    
    elif prop_type == "relation":
        # For relations, we need the target database ID
        # This will be filled in later after databases are created
        return {
            "relation": {
                "database_id": "placeholder",
                "type": "single_property" if prop_def.get("limit") == "L1" else "dual_property",
            }
        }
    
    else:
        # Default to rich_text
        return {"rich_text": {}}


def create_database(
    parent_page_id: str,
    db_template: Dict[str, Any],
    skip_relations: bool = True
) -> Dict[str, Any]:
    """Create a Notion database from template."""
    
    # Build properties schema
    properties = {}
    relation_props = []
    
    for prop_name, prop_def in db_template["properties"].items():
        if prop_def["type"] == "relation":
            if not skip_relations:
                relation_props.append((prop_name, prop_def))
            continue
        
        properties[prop_name] = notion_property_to_schema(prop_name, prop_def)
    
    # Create database
    payload = {
        "parent": {"page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": db_template["title"]}}],
        "icon": {"type": "emoji", "emoji": db_template.get("icon", "📄")},
        "properties": properties,
    }
    
    response = requests.post(
        "https://api.notion.com/v1/databases",
        headers=HEADERS,
        json=payload,
    )
    
    if response.status_code != 200:
        print(f"ERROR creating {db_template['title']}: {response.text}")
        return None
    
    result = response.json()
    print(f"[OK] Created: {db_template['title']} (ID: {result['id']})")
    
    return {
        "id": result["id"],
        "template_id": db_template["id"],
        "title": db_template["title"],
        "relation_props": relation_props,
    }


def add_relations(
    database_id: str,
    relation_props: List[tuple],
    db_id_map: Dict[str, str],
) -> None:
    """Add relation properties to an existing database."""
    
    for prop_name, prop_def in relation_props:
        target_db_title = prop_def["database"]
        
        # Find target database ID
        target_id = None
        for template_id, info in db_id_map.items():
            if info.get("title") == target_db_title:
                target_id = info["id"]
                break
        
        if not target_id:
            print(f"  [WARN] Cannot find target database for relation: {prop_name} -> {target_db_title}")
            continue
        
        # Add relation property
        payload = {
            "properties": {
                prop_name: {
                    "relation": {
                        "database_id": target_id,
                    }
                }
            }
        }
        
        response = requests.patch(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=HEADERS,
            json=payload,
        )
        
        if response.status_code == 200:
            print(f"  [OK] Added relation: {prop_name} -> {target_db_title}")
        else:
            print(f"  [ERR] Failed to add relation {prop_name}: {response.text}")


def main():
    parser = argparse.ArgumentParser(description="Create Notion automation databases")
    parser.add_argument(
        "--parent-page-id",
        required=True,
        help="Notion page ID to create databases under",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating",
    )
    args = parser.parse_args()
    
    # Load template
    template = load_template()
    print(f"\nLoaded template with {len(template['databases'])} databases")
    
    if args.dry_run:
        print("\n[DRY RUN] Would create:")
        for db in template["databases"]:
            print(f"  - {db['title']} ({db['id']})")
            for prop_name, prop_def in db["properties"].items():
                print(f"      * {prop_name}: {prop_def['type']}")
        return
    
    # Phase 1: Create all databases without relations
    print("\n[Phase 1] Creating databases...")
    db_id_map = {}
    
    for db_template in template["databases"]:
        result = create_database(args.parent_page_id, db_template, skip_relations=True)
        if result:
            db_id_map[db_template["id"]] = result
    
    # Phase 2: Add relations (now that all databases exist)
    print("\n[Phase 2] Adding relations...")
    for template_id, info in db_id_map.items():
        if info.get("relation_props"):
            print(f"\nAdding relations to: {info['title']}")
            add_relations(info["id"], info["relation_props"], db_id_map)
    
    # Output summary
    print("\n" + "=" * 60)
    print("COMPLETE! Created databases:")
    print("=" * 60)
    
    output_map = {}
    for template_id, info in db_id_map.items():
        print(f"  {info['title']}")
        print(f"    ID: {info['id']}")
        output_map[template_id] = info["id"]
    
    # Save ID map for future use
    map_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config",
        "notion_db_ids.json"
    )
    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(output_map, f, indent=2)
    
    print(f"\nDatabase ID map saved to: {map_path}")


if __name__ == "__main__":
    main()

