"""
Add relations between Notion automation databases.

This script adds the relation properties that link the new automation
databases to each other and to existing databases.

Usage:
    python scripts/add_notion_relations.py
"""

import os
import sys
import json

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

# Load the database IDs we created
def load_db_ids():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config",
        "notion_db_ids.json"
    )
    with open(config_path, "r") as f:
        return json.load(f)


def add_relation(database_id: str, property_name: str, target_database_id: str) -> bool:
    """Add a relation property to a database."""
    payload = {
        "properties": {
            property_name: {
                "relation": {
                    "database_id": target_database_id,
                    "single_property": {}
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
        print(f"  [OK] Added: {property_name}")
        return True
    else:
        error = response.json().get("message", response.text)
        if "already exists" in error.lower() or "duplicate" in error.lower():
            print(f"  [SKIP] {property_name} already exists")
            return True
        print(f"  [ERR] {property_name}: {error}")
        return False


def main():
    print("\n" + "=" * 60)
    print("Adding Relations to Notion Databases")
    print("=" * 60)
    
    db_ids = load_db_ids()
    
    # Existing databases (you'll need to update these with your actual IDs)
    # These are from your earlier Notion sync
    EXISTING_DBS = {
        "attribute_taxonomy": "2d5c47c61e2180ae9a53d844719cbcd7",
        "programme_profiles": "2d5c47c61e21802caf3be7cd77aef164",
    }
    
    success_count = 0
    total_count = 0
    
    # 1. Control Definitions -> Attribute Taxonomy
    print(f"\n[1] Control Definitions (DB)")
    print(f"    ID: {db_ids['control_definitions']}")
    
    total_count += 1
    if add_relation(db_ids['control_definitions'], "Primary Domain", EXISTING_DBS['attribute_taxonomy']):
        success_count += 1
    
    total_count += 1
    if add_relation(db_ids['control_definitions'], "Secondary Domains", EXISTING_DBS['attribute_taxonomy']):
        success_count += 1
    
    # 2. Control Packs -> Control Definitions
    print(f"\n[2] Control Packs (DB)")
    print(f"    ID: {db_ids['control_packs']}")
    
    total_count += 1
    if add_relation(db_ids['control_packs'], "Controls", db_ids['control_definitions']):
        success_count += 1
    
    # 3. Profile Pack Map -> Programme Profiles + Control Packs
    print(f"\n[3] Profile Pack Map (DB)")
    print(f"    ID: {db_ids['profile_pack_map']}")
    
    total_count += 1
    if add_relation(db_ids['profile_pack_map'], "Programme Profile", EXISTING_DBS['programme_profiles']):
        success_count += 1
    
    total_count += 1
    if add_relation(db_ids['profile_pack_map'], "Control Pack", db_ids['control_packs']):
        success_count += 1
    
    # 4. Default Weights -> Programme Profiles + Attribute Taxonomy
    print(f"\n[4] Default Weights (DB)")
    print(f"    ID: {db_ids['default_weights']}")
    
    total_count += 1
    if add_relation(db_ids['default_weights'], "Programme Profile", EXISTING_DBS['programme_profiles']):
        success_count += 1
    
    total_count += 1
    if add_relation(db_ids['default_weights'], "Attribute", EXISTING_DBS['attribute_taxonomy']):
        success_count += 1
    
    # 5. Coupling Rules -> Control Definitions + Attribute Taxonomy + Programme Profiles
    print(f"\n[5] Coupling Rules (DB)")
    print(f"    ID: {db_ids['coupling_rules']}")
    
    total_count += 1
    if add_relation(db_ids['coupling_rules'], "From Control", db_ids['control_definitions']):
        success_count += 1
    
    total_count += 1
    if add_relation(db_ids['coupling_rules'], "To Control", db_ids['control_definitions']):
        success_count += 1
    
    total_count += 1
    if add_relation(db_ids['coupling_rules'], "From Attribute", EXISTING_DBS['attribute_taxonomy']):
        success_count += 1
    
    total_count += 1
    if add_relation(db_ids['coupling_rules'], "To Attribute", EXISTING_DBS['attribute_taxonomy']):
        success_count += 1
    
    total_count += 1
    if add_relation(db_ids['coupling_rules'], "Applies To Profiles", EXISTING_DBS['programme_profiles']):
        success_count += 1
    
    # 6. Derived Metrics -> Control Definitions
    print(f"\n[6] Derived Metrics (DB)")
    print(f"    ID: {db_ids['derived_metrics']}")
    
    total_count += 1
    if add_relation(db_ids['derived_metrics'], "Input Controls", db_ids['control_definitions']):
        success_count += 1
    
    # 7. Questionnaire Questions -> Questionnaires
    print(f"\n[7] Questionnaire Questions (DB)")
    print(f"    ID: {db_ids['questionnaire_questions']}")
    
    total_count += 1
    if add_relation(db_ids['questionnaire_questions'], "Questionnaire", db_ids['questionnaires']):
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"COMPLETE! Added {success_count}/{total_count} relations")
    print("=" * 60)


if __name__ == "__main__":
    main()

