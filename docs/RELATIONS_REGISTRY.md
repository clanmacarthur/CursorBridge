# Relations Registry (As-Is and To-Be)

Last updated: 2026-02-22

Goal: keep three clear relation tables:
- `RELATIONS_MASTER.csv`: one checklist view across both states
- `RELATIONS_EXISTING.csv`: what is live now
- `RELATIONS_TO_BE.csv`: what should exist (including gaps and next action)

## Files

- `docs/RELATIONS_EXISTING.csv`
- `docs/RELATIONS_TO_BE.csv`
- `docs/RELATIONS_MASTER.csv`

## How to read the two tables

- `RELATIONS_MASTER.csv`
  - This is the operational checklist table.
  - Use it to track:
    - what is already configured in Supabase
    - what still needs data/configuration
    - Convex migration status
    - launch readiness

- `RELATIONS_EXISTING.csv`
  - This is the live schema relation list from `canon/RelationsManifest.md`.
  - If it is here, it already exists now.

- `RELATIONS_TO_BE.csv`
  - This is the target relation map.
  - It includes both:
    - live relations we keep
    - missing relations we still need to add
  - Use `current_state` and `next_action` columns to decide work order.

## Current state summary

- Existing live relations: 16 rows
- Target relation map: 44 rows
- Master merged checklist: 45 rows
- Missing or non-FK links to resolve: 28 rows

## Simple phase order

1. `P0`: keep and validate what is already live.
2. `P1`: add safe missing FKs where IDs already line up.
3. `P2`: fix type mismatches and text-based links.
4. `P3`: normalize JSON-based links into stable relation fields.

## Notion Tracker Plan

Three Notion databases should mirror these CSVs:

1. `Relations Master (DB)`:
   - one row per relation key
   - includes status checkboxes:
     - `On Supabase`
     - `Supabase Configured`
     - `Needs More Data`
     - `On Convex`
     - `Convex Configured`
     - `Convex Synced`
     - `Ready For Launch`
   - includes phase and layer fields:
     - `Phase`
     - `Mach Layer` (`Core`, `Mach1.1`, `Advanced`)

2. `Relations Existing (DB)`:
   - live-only relation rows
   - links each row to master via `Master Link`

3. `Relations To-Be (DB)`:
   - target/gap relation rows
   - links each row to master via `Master Link`

Script:

- `scripts/create_notion_relations_registry.py`

Build master CSV script:

- `scripts/build_relations_master_csv.py`

## Parked Advanced Layer

- User-defined databases and custom wheels are parked under `Mach1.1` for now.
- Keep core sessions schema and relation cleanup first.
- Add `Mach1.1` rows in `RELATIONS_MASTER.csv` when that feature work starts.

## Source references used

- `canon/RelationsManifest.md`
- `canon/TableIndex.md`
- `canon/SystemManifest.md`
- `docs/SYSTEM_MANIFEST.md`
- `docs/THEME_TABLE_CATALOG.md`
