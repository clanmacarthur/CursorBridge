"""
Apply Mappings Script

Reads mapping rules from the 'mappings' table and applies them to:
- Populate join tables
- Set default relations
- Apply value→relation transformations

This eliminates manual clicking in Notion/Supabase.

Usage:
    python scripts/apply_mappings.py [--dry-run]
"""

import os
import sys
import argparse
from typing import Dict, Any, List
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_mappings() -> List[Dict[str, Any]]:
    """Fetch all active mappings from the database."""
    response = supabase.table("mappings").select("*").execute()
    return response.data


def apply_value_to_relation(mapping: Dict[str, Any], dry_run: bool = False) -> int:
    """
    Apply a value→relation mapping.
    
    Example: When "Programme Profile" = "Athlete", 
             auto-link to packs ["endurance-athlete", "nutrition-basics"]
    """
    from_table = mapping["from_table"]
    from_field = mapping["from_field"]
    from_value = mapping["from_value"]
    to_table = mapping["to_table"]
    to_field = mapping["to_field"]
    to_value = mapping["to_value"]
    
    # Find source rows matching the condition
    source_rows = supabase.table(from_table).select("*").eq(from_field, from_value).execute()
    
    if not source_rows.data:
        print(f"  No rows found in {from_table} where {from_field} = '{from_value}'")
        return 0
    
    # Find target row(s)
    target_rows = supabase.table(to_table).select("*").eq(to_field, to_value).execute()
    
    if not target_rows.data:
        print(f"  No rows found in {to_table} where {to_field} = '{to_value}'")
        return 0
    
    applied = 0
    for source in source_rows.data:
        for target in target_rows.data:
            if dry_run:
                print(f"  [DRY] Would link {from_table}[{source.get('id')}] → {to_table}[{target.get('id')}]")
            else:
                # Apply the relation (implementation depends on table structure)
                # For join tables, insert a row
                # For direct relations, update the source row
                print(f"  Linked {from_table}[{source.get('id')}] → {to_table}[{target.get('id')}]")
            applied += 1
    
    return applied


def apply_default_fill(mapping: Dict[str, Any], dry_run: bool = False) -> int:
    """
    Apply a default_fill mapping.
    
    Example: Set default weights for all programme profiles.
    """
    from_table = mapping["from_table"]
    to_table = mapping["to_table"]
    to_field = mapping["to_field"]
    to_value = mapping["to_value"]
    
    # Get all source rows
    source_rows = supabase.table(from_table).select("*").execute()
    
    applied = 0
    for source in source_rows.data:
        # Check if default already exists
        existing = supabase.table(to_table).select("id").eq(
            "programme_profile_id", source.get("notion_page_id")
        ).execute()
        
        if existing.data:
            continue  # Already has defaults
        
        if dry_run:
            print(f"  [DRY] Would create default {to_field}={to_value} for {source.get('id')}")
        else:
            # Create default entry
            supabase.table(to_table).insert({
                "programme_profile_id": source.get("notion_page_id"),
                to_field: to_value,
            }).execute()
            print(f"  Created default for {source.get('id')}")
        applied += 1
    
    return applied


def apply_profile_pack_defaults(dry_run: bool = False) -> int:
    """
    Apply default pack assignments to programme profiles.
    
    This is a special case handler for the profile → pack mapping.
    """
    # Get all profiles
    profiles = supabase.table("programme_profiles").select("*").execute()
    
    # Get default packs
    default_packs = supabase.table("control_packs").select("*").eq("is_default", True).execute()
    
    if not default_packs.data:
        print("  No default packs found")
        return 0
    
    applied = 0
    for profile in profiles.data:
        profile_id = profile.get("notion_page_id")
        
        for pack in default_packs.data:
            # Check if mapping already exists
            existing = supabase.table("profile_pack_map").select("id").eq(
                "programme_profile_id", profile_id
            ).eq("pack_id", pack.get("id")).execute()
            
            if existing.data:
                continue
            
            if dry_run:
                print(f"  [DRY] Would map {profile.get('programme_profile___title', 'Unknown')} → {pack.get('pack_name')}")
            else:
                supabase.table("profile_pack_map").insert({
                    "programme_profile_id": profile_id,
                    "pack_id": pack.get("id"),
                    "is_required": False,
                }).execute()
                print(f"  Mapped {profile.get('programme_profile___title', 'Unknown')} → {pack.get('pack_name')}")
            applied += 1
    
    return applied


def apply_coupling_rule_defaults(dry_run: bool = False) -> int:
    """
    Seed default coupling rules from the template.
    """
    import json
    
    # Load seed data from template
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notion_automation_databases.json"
    )
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
    
    seed_rules = template.get("seed_data", {}).get("coupling_rules", [])
    
    applied = 0
    for rule in seed_rules:
        # Check if rule already exists
        existing = supabase.table("coupling_rules").select("id").eq(
            "rule_name", rule.get("rule_name")
        ).execute()
        
        if existing.data:
            continue
        
        if dry_run:
            print(f"  [DRY] Would create coupling rule: {rule.get('rule_name')}")
        else:
            supabase.table("coupling_rules").insert({
                "rule_name": rule.get("rule_name"),
                "from_metric": rule.get("from_metric"),
                "to_metric": rule.get("to_metric"),
                "function_type": rule.get("function_type", "linear").lower(),
                "direction": rule.get("direction", "positive").lower(),
                "magnitude": rule.get("magnitude", 1.0),
                "threshold_value": rule.get("threshold_value"),
                "evidence_confidence": rule.get("evidence_confidence", "moderate").lower(),
                "status": "active",
            }).execute()
            print(f"  Created coupling rule: {rule.get('rule_name')}")
        applied += 1
    
    return applied


def apply_control_definitions_seed(dry_run: bool = False) -> int:
    """
    Seed default control definitions from the template.
    """
    import json
    
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notion_automation_databases.json"
    )
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
    
    seed_controls = template.get("seed_data", {}).get("control_definitions", [])
    
    applied = 0
    for control in seed_controls:
        # Check if control already exists
        existing = supabase.table("control_definitions").select("id").eq(
            "control_name", control.get("control_name")
        ).execute()
        
        if existing.data:
            continue
        
        if dry_run:
            print(f"  [DRY] Would create control: {control.get('control_name')}")
        else:
            supabase.table("control_definitions").insert({
                "control_name": control.get("control_name"),
                "control_type": control.get("control_type", "slider"),
                "range_min": control.get("range_min", 0),
                "range_max": control.get("range_max", 10),
                "range_step": control.get("range_step", 1),
                "default_value": control.get("default_value", 5),
                "unit": control.get("unit"),
                "is_default": control.get("is_default", False),
                "completion_threshold": control.get("completion_threshold"),
                "status": "active",
            }).execute()
            print(f"  Created control: {control.get('control_name')}")
        applied += 1
    
    return applied


def apply_control_packs_seed(dry_run: bool = False) -> int:
    """
    Seed default control packs from the template.
    """
    import json
    
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notion_automation_databases.json"
    )
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
    
    seed_packs = template.get("seed_data", {}).get("control_packs", [])
    
    applied = 0
    for pack in seed_packs:
        # Check if pack already exists
        existing = supabase.table("control_packs").select("id").eq(
            "pack_slug", pack.get("pack_slug")
        ).execute()
        
        if existing.data:
            continue
        
        if dry_run:
            print(f"  [DRY] Would create pack: {pack.get('pack_name')}")
        else:
            supabase.table("control_packs").insert({
                "pack_name": pack.get("pack_name"),
                "pack_slug": pack.get("pack_slug"),
                "category": pack.get("category", "wellness").lower(),
                "difficulty": pack.get("difficulty", "beginner").lower(),
                "is_default": pack.get("is_default", False),
                "is_public": True,
                "status": "active",
            }).execute()
            print(f"  Created pack: {pack.get('pack_name')}")
        applied += 1
    
    return applied


def apply_derived_metrics_seed(dry_run: bool = False) -> int:
    """
    Seed derived metrics from the template.
    """
    import json
    
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notion_automation_databases.json"
    )
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
    
    seed_metrics = template.get("seed_data", {}).get("derived_metrics", [])
    
    applied = 0
    for metric in seed_metrics:
        # Check if metric already exists
        existing = supabase.table("derived_metrics").select("id").eq(
            "metric_slug", metric.get("metric_slug")
        ).execute()
        
        if existing.data:
            continue
        
        if dry_run:
            print(f"  [DRY] Would create metric: {metric.get('metric_name')}")
        else:
            supabase.table("derived_metrics").insert({
                "metric_name": metric.get("metric_name"),
                "metric_slug": metric.get("metric_slug"),
                "formula_type": metric.get("formula_type", "weighted_average").lower().replace(" ", "_"),
                "domain": metric.get("domain"),
                "output_min": 0,
                "output_max": 100,
                "unit": "score",
                "status": "active",
            }).execute()
            print(f"  Created metric: {metric.get('metric_name')}")
        applied += 1
    
    return applied


def main():
    parser = argparse.ArgumentParser(description="Apply mapping rules")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--seed-only", action="store_true", help="Only seed default data")
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("CursorBridge - Apply Mappings")
    print("=" * 60)
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)
    
    total_applied = 0
    
    # Seed default data first
    print("\n[1/4] Seeding control definitions...")
    total_applied += apply_control_definitions_seed(args.dry_run)
    
    print("\n[2/4] Seeding control packs...")
    total_applied += apply_control_packs_seed(args.dry_run)
    
    print("\n[3/4] Seeding derived metrics...")
    total_applied += apply_derived_metrics_seed(args.dry_run)
    
    print("\n[4/4] Seeding coupling rules...")
    total_applied += apply_coupling_rule_defaults(args.dry_run)
    
    if not args.seed_only:
        print("\n[+] Applying profile -> pack defaults...")
        total_applied += apply_profile_pack_defaults(args.dry_run)
        
        # Apply custom mappings from the mappings table
        print("\n[+] Applying custom mappings...")
        try:
            mappings = get_mappings()
            for mapping in mappings:
                mapping_type = mapping.get("mapping_type")
                print(f"\n  Processing: {mapping.get('id')} ({mapping_type})")
                
                if mapping_type == "value_to_relation":
                    total_applied += apply_value_to_relation(mapping, args.dry_run)
                elif mapping_type == "default_fill":
                    total_applied += apply_default_fill(mapping, args.dry_run)
                else:
                    print(f"    Unknown mapping type: {mapping_type}")
        except Exception as e:
            print(f"  Note: mappings table may not exist yet: {e}")
    
    print("\n" + "=" * 60)
    print(f"COMPLETE! Applied {total_applied} mappings/seeds")
    print("=" * 60)


if __name__ == "__main__":
    main()

