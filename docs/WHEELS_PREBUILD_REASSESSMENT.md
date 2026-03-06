# Wheels Pre-Build Reassessment
Last updated: 2026-02-22

## What Changed

These two new docs shift the order of work:

- `GRAND_PROJECT_SKELETON.md` says we should keep one shared model for all projects.
- `AI_BUILDER_INSTRUCTIONS_NOTION.md` says we should lock a clear Notion structure first.
- New ISU reference page adds sustainability token architecture detail:
  - `Sustainable Utilities (Institute)(Token)- ISU`
  - https://www.notion.so/Sustainable-Utilities-Institute-Token-ISU-1b6c47c61e21802e8e3cd167e5c1214e

This means we should not jump into wheel visuals first.  
We should lock structure and data mapping first, then build wheel behavior/UI.
ISU integration is now tracked as a project-architecture stream in parallel with sessions-first delivery.

## Current Reality Check

- We now have both routes in code:
  - current simple route: `/session`
  - richer builder route: `/sessions`
- Sessions data and mapping work is still in progress.
- Supabase remains first source of truth for this phase.
- Convex is still the next phase after Supabase parity.

## Notion Project Created

A new master Notion project was created under `Evans Projects`:

- Root page:
  - `Wheels Pre-Build Project - Sessions, DB Map, Convex Prep`
  - https://www.notion.so/Wheels-Pre-Build-Project-Sessions-DB-Map-Convex-Prep-30fc47c61e2181ef8921c92bb32a3120

It includes:

- `00_READ_ME`
- `01_SHARED_CORE`
- `02_DASHBOARD_BUILDER`
- `03_WELLNESS_APP`
- `04_DIGITAL_EXPANSION_DIVISION`
- `05_SUSTAINABLE_INSTITUTE`
- `06_MONETIZATION_MENU`
- `07_PITCH_DECK_LAYER`
- `08_BACKLOG_AND_FUTURE`
- `99_ARCHIVE`
- `EXECUTION_TRACKER` database

Creation output is tracked in:

- `docs/_notion_project_creation_result.json`

## Reassessed Build Order (Before Wheel Visual Work)

1. Lock structure and naming
   - Keep shared model definitions in one place.
   - Keep sessions decisions tied to the new Notion project tracker.

2. Finish Supabase sessions table inventory
   - Confirm keep/merge/deprecate for all session-related tables.
   - Mark duplicates and legacy tables clearly.

3. Lock table-to-domain mapping
   - For each table, decide: ring domain, inner attributes, relation-only, or not wired yet.
   - Keep this synced in `docs/THEME_TABLE_CATALOG.md` and `docs/DATA_MODEL_OVERVIEW.md`.

4. Fill critical data gaps in Supabase
   - Prioritize domains that drive sessions output quality:
     - lens, colour/light, chakra, meridian, organ-emotion, symbol, deity/archetype, sound, practice.

5. Stabilize `/api/session/*` behavior
   - Keep contract keys stable while logic improves.
   - Avoid regressions in existing routes.

6. Start Convex prep only after parity check passes
   - Move with adapter/dual-read planning, not a blind switch.

## Ready Gate For Wheel UI Work

Wheel UI work should start only when these are true:

- session-related Supabase inventory is complete and labeled.
- table-to-domain mapping is complete for active session domains.
- top missing data rows are loaded for active domains.
- `/api/session/themes`, `/api/session/preview`, `/api/session/generate` have stable payload contracts.
