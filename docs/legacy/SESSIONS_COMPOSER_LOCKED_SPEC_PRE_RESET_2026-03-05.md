# Sessions Composer Locked Spec (Supabase-First)

Last updated: 2026-03-05

## Purpose

This is the locked build direction for Sessions Composer in the current Supabase phase.
It keeps Supabase stable and focuses on usable behavior in the UI.

## Core Rule

- The wheel represents **domains**.
- The drawer/list represents **real table rows**.

Do not place hundreds of item rows directly on the wheel.

## User Flow (Simple)

1. User picks a subject family at the top.
2. Big wheel shows available domains.
3. User clicks a ring.
4. Right drawer opens with real rows from that domain table.
5. User filters and selects rows.
6. Selected rows are added to a build stack (ordered session steps).
7. User previews generated session.
8. User saves as custom session.

## Domain Tables (Current)

- `breath_library`
- `movements_system`
- `organ_emotion_system`
- `meridian_system`
- `light_colour`
- `sound_vibration`
- `nutrition_and_food`
- `nutrition_protocols`
- `symbols_index`
- `sacred_geometry`
- `chakra_systems`

Live audit confirms all exist and are non-empty.
Reference: `docs/SESSIONS_COMPOSER_DOMAIN_AUDIT_2026-03-05.md`

## Filter Rule (Important)

Only show filter groups that have real values.

Reason: several columns exist but currently have no populated values.
Showing empty filters confuses users and makes the app look broken.

## Mapping Rule

Use only real existing relation sources:

- `mappings`
- `cross_domain_mappings`
- direct relation columns already in domain tables

No guessed links.
No invented compatibility rules.

## Out Of Scope (First Prototype)

Keep these parked for now:

- lens/meta-lens UI logic
- narration style selector logic
- control packs/coupling UI
- old template-first flow as the main path

These can be layered later after the domain composer is stable.

## Data Governance Notes

- Supabase structure stays stable in this phase.
- Major model changes are deferred to Convex migration phase.
- New Notion tables stay in stage flow until mapped cleanly.

## 0a Notion Page Reality Check

Page: `36207156f7034c13a839249dee0afe1a`

- DBs found: 14
- Tracked in config: 8
- Untracked: 6

Initial profile result:

- 2 are finance-only (`Finance Tracker`, `Finance Tracker (1)`) and not sessions scope.
- 1 is generic (`Name`, `Tags`) with 3 rows and no session signals.
- 3 are inaccessible by current Notion token (cannot classify yet).

References:

- `docs/_notion_0a_page_scan.json`
- `docs/_notion_0a_missing_db_profiles.json`

## Stop Condition For This Prototype

Stop and report if any core domain table is empty or any required relation table cannot be queried.

Otherwise continue building and testing until these 3 flows are visibly working:

1. Breath-only composition.
2. Breath + movement composition.
3. Breath + colour/sound + movement + nutrition composition.
