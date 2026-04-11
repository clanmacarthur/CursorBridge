# Botanical App Build Order V1

Last updated: 2026-04-08

## Purpose

This document locks the recommended build order for the botanical app using the
current frozen schema and the Atlantic Forest / Green Coast launch slice.

## Build Direction

- one shared branchable botanical system underneath
- Brazil as branch one
- Atlantic Forest / Green Coast as launch focus
- `Modular Gardens` as the user-facing app name
- standalone-first app
- HNOS-compatible integration layer later

## Phase 1

Build the real internal data-driven app shell first.

Must be real in phase 1:

- botanical search
- botanical cards and detail views
- layer filtering
- size filtering
- product filtering
- zone / branch filtering
- product-to-botanical navigation
- botanical-to-product navigation
- Atlantic Forest / Green Coast launch slice

Use:

- `sql/botanicals/00_core_schema.sql`
- `"Botanical_Operational_View"`

## Phase 2

Add focused launch curation and planning features.

Priority:

- Atlantic Forest / Green Coast species focus
- compact/smaller variety prioritisation
- micro-enclosure presets built from existing layer fields plus size tags
- product-focused exploration
- zone and production-mode comparison
- branch capability visibility from `branch_resources`

## Phase 3

Add richer planning logic on top of real data.

Examples:

- shortlist scoring
- symbiosis / companion surfacing
- habitat planning
- modular / living gardens flows
- curated bundles

These must remain consumers of the existing schema, not schema replacements.

## Phase 4

Add HNOS-connected features only after boundaries are explicit.

Examples:

- shared identity
- node permissions
- messaging
- agreement / contract hooks
- cross-node coordination

Until then, use placeholders or thin shells rather than pretending these are
already resolved runtime systems.

## Layer Filter Build Rule

Use canonical layers from `species_design_matrix`:

- `canopy`
- `subcanopy`
- `shrub`
- `herbaceous`
- `groundcover`
- `climber`
- `root`
- `aquatic_marginal`
- `epiphyte`
- `fungal_layer`

`food_forest_layer` may provide the friendly display label, but canonical layer
fields control filtering.

Frontend labels may be food-forest-friendly aliases.

Examples:

- `Large Shrubs` = `shrub` + larger size band
- `Small Shrubs` = `shrub` + smaller size band
- `Ground Cover` = `groundcover`

Micro presets should also be alias filters, not new canonical layers.

Examples:

- `Micro Mat` = `groundcover` and `layer_stack_tags` contains `micro_mat`
- `Micro Low` = `groundcover` or compact `epiphyte` and
  `layer_stack_tags` contains `micro_low`
- `Micro Mid` = `herbaceous` or compact `epiphyte` and
  `layer_stack_tags` contains `micro_mid`
- `Micro Upper` = upper `herbaceous`, `epiphyte`, or `climber` and
  `layer_stack_tags` contains `micro_upper`

Curated choice views should prefer max `2` shared-name options per canonical
layer, allow `3` only when functionally distinct, and rank the smallest
occupied form first.

Do not add `brush` unless a precise alias rule is later written.

## Scope Rule

The launch slice may narrow to Atlantic Forest / Green Coast for clarity and
depth.

This is a content-and-UI narrowing only.
It is not a branch fork and not a schema change.

## Product Naming Rule

Build the frontend and pitchdeck under the name `Modular Gardens`.

Keep:

- `HNOS` as the framework name
- `Modular Gardens` as the app name
- current botanical schema as the backend truth

## Non-Goals For Early Build

Do not block the app on these from day one:

- full HNOS contracts runtime
- full network exchange runtime
- full events manager runtime
- all-Brazil-at-once data exposure
- all-branch-at-once frontend complexity

## Success Condition

The first real app build should already prove:

- the frozen schema works
- the launch slice feels focused
- the product logic is two-way
- the layer filters work from a food-forest perspective
- the app stands on its own without waiting for wider framework completion
