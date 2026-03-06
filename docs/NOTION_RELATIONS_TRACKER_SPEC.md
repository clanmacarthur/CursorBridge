# Notion Relations Tracker Spec

Last updated: 2026-02-22

Purpose: define the exact columns for the three Notion relation tracker databases.

## Database 1: Relations Master (DB)

One row per relation key, used as the single checklist.

| Column | Type | Why it exists |
|---|---|---|
| `Relation Key` | Title | Unique key: `from_table.from_column->to_table.to_column` |
| `From Table` | Text | Source table |
| `From Column` | Text | Source column |
| `To Table` | Text | Target table |
| `To Column` | Text | Target column |
| `Relation Type` | Select | FK, mapping rule, edge registry, etc. |
| `Source Status` | Select | `existing`, `to_be`, `both` |
| `In Existing` | Checkbox | Present in live relation list |
| `In To Be` | Checkbox | Present in target relation list |
| `Current State` | Select | `live`, `missing_fk`, `text_link_only`, etc. |
| `Next Action` | Text | Plain action step |
| `Phase` | Select | `P0`, `P1`, `P2`, `P3`, `P4`, `Parked` |
| `On Supabase` | Checkbox | Relation source/target lives in Supabase |
| `Supabase Configured` | Checkbox | Relation already configured in schema/runtime |
| `Needs More Data` | Checkbox | Missing content or mapping quality |
| `On Convex` | Checkbox | Relation already represented in Convex |
| `Convex Configured` | Checkbox | Convex structure/config exists |
| `Convex Synced` | Checkbox | Data synced to Convex |
| `Ready For Launch` | Checkbox | Good enough for launch |
| `Mach Layer` | Select | `Core`, `Mach1.1`, `Advanced` |
| `Last Checked` | Date | Last review date |
| `Notes` | Text | Extra context |

## Database 2: Relations Existing (DB)

Live relation rows only.

| Column | Type | Why it exists |
|---|---|---|
| `Relation ID` | Title | Stable row ID like `EX001` |
| `From Table` | Text | Source table |
| `From Column` | Text | Source column |
| `To Table` | Text | Target table |
| `To Column` | Text | Target column |
| `Relation Type` | Select | Relation kind |
| `Join Table` | Text | Join table when relevant |
| `State` | Select | `live_fk`, `derived_live` |
| `Source` | Text | Source manifest/doc |
| `On Supabase` | Checkbox | Always true for this table |
| `Ready For Launch` | Checkbox | Quick launch flag |
| `Master Link` | Relation -> `Relations Master (DB)` | Connects to master row |
| `Notes` | Text | Extra context |

## Database 3: Relations To-Be (DB)

Target relation rows and gap tracking.

| Column | Type | Why it exists |
|---|---|---|
| `Relation ID` | Title | Stable row ID like `TG001` |
| `From Table` | Text | Source table |
| `From Column` | Text | Source column |
| `To Table` | Text | Target table |
| `To Column` | Text | Target column |
| `Target Type` | Select | Target relation type |
| `Current State` | Select | Live/missing/text-link/json-link/not-created |
| `Next Action` | Text | Immediate action |
| `Phase` | Select | `P0` to `P4` |
| `On Supabase` | Checkbox | Exists in Supabase context |
| `Supabase Configured` | Checkbox | Configured now |
| `Needs More Data` | Checkbox | Still needs more data/mapping |
| `On Convex` | Checkbox | Exists in Convex context |
| `Convex Configured` | Checkbox | Convex config done |
| `Ready For Launch` | Checkbox | Launch readiness |
| `Mach Layer` | Select | `Core`, `Mach1.1`, `Advanced` |
| `Master Link` | Relation -> `Relations Master (DB)` | Connects to master row |
| `Notes` | Text | Extra context |

## Scripts

- Build master CSV:
  - `python scripts/build_relations_master_csv.py`
- Create/update Notion DBs and load rows:
  - `python scripts/create_notion_relations_registry.py --page <NOTION_PAGE_URL_OR_ID>`
- Preview only:
  - `python scripts/create_notion_relations_registry.py --page <PAGE> --dry-run`
- Check boxes as work is completed:
  - `python scripts/checkoff_notion_relation_progress.py --relation-id TG018 --mark-supabase-done --note "FK added"`
  - `python scripts/checkoff_notion_relation_progress.py --relation-key "mappings.from_db+from_field->mappings.to_db+to_field" --mark-convex-done`
