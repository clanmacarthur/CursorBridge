# Relations Registry (As-Is and To-Be)

Last updated: 2026-02-22

Goal: keep two clear relation tables:
- `RELATIONS_EXISTING.csv`: what is live now
- `RELATIONS_TO_BE.csv`: what should exist (including gaps and next action)

## Files

- `docs/RELATIONS_EXISTING.csv`
- `docs/RELATIONS_TO_BE.csv`

## How to read the two tables

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
- Missing or non-FK links to resolve: 28 rows

## Simple phase order

1. `P0`: keep and validate what is already live.
2. `P1`: add safe missing FKs where IDs already line up.
3. `P2`: fix type mismatches and text-based links.
4. `P3`: normalize JSON-based links into stable relation fields.

## Source references used

- `canon/RelationsManifest.md`
- `canon/TableIndex.md`
- `canon/SystemManifest.md`
- `docs/SYSTEM_MANIFEST.md`
- `docs/THEME_TABLE_CATALOG.md`
