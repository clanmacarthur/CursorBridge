# Convex Migration Plan

Last updated: 2026-02-21
Status: draft plan (not started)

## Goal

Move from Supabase-only reads to Convex-ready reads without breaking session generation.

## Non-Negotiable Rule

Keep one stable app-facing contract for session theme data while backend storage changes.

## Phases

## Phase 0: Supabase Coverage Complete

Before migration:

- Finish `docs/DATA_MODEL_OVERVIEW.md`.
- Finish `docs/THEME_TABLE_CATALOG.md`.
- Confirm every ontology table is mapped or marked "not wired yet".

Exit check:

- We can explain where each theme domain comes from in Supabase.

## Phase 1: Convex Schema Mirror

Build matching Convex collections for:

- theme domains
- mapping edges
- session runtime references

Exit check:

- Convex schema can hold all required fields from mapped Supabase tables.

## Phase 2: Adapter Layer

Create a data adapter that can read from:

- Supabase (current)
- Convex (new)

The app should call one interface only.

Exit check:

- Feature behavior matches for both backends in test runs.

## Phase 3: Dual Read Validation

Run both reads in parallel in non-production checks.
Compare outputs for key scenarios.

Exit check:

- Differences are understood and fixed.

## Phase 4: Controlled Cutover

Switch primary reads to Convex in stages.
Keep Supabase fallback while monitoring.

Exit check:

- Session generation output remains stable.
- No route regressions in main app.

## Phase 5: Supabase Scope Reduction

After stable cutover:

- Keep only required Supabase tables.
- Archive legacy paths.
- Update canon and readme docs.

## Risks and Mitigation

- Risk: field mismatches -> Mitigation: strict mapping table in docs.
- Risk: behavior drift -> Mitigation: dual-read comparisons.
- Risk: partial cutover confusion -> Mitigation: one adapter entry point.

