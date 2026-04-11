# Botanical App Boundaries V1

Last updated: 2026-04-08

## Purpose

This document locks the build boundaries for the botanical app before frontend
and runtime work expands.

## Canonical Naming

- `HNOS` is the canonical framework name:
  - `Human Network Optimisation System`
- `Modular Gardens` is the botanical app / module name for user-facing build
  and pitchdeck work.
- Older `HONS` wording in legacy or pitch-facing material should be treated as
  naming drift, not as a separate framework.

## Launch Scope

- The botanical system remains one shared branchable schema.
- `Brazil` remains branch one.
- `Atlantic Forest / Green Coast` is the current launch focus inside Brazil.
- This focus is:
  - a scoped curation pack
  - a filtered operational view
  - a frontend / pitchdeck narrowing
- This focus is not:
  - a new schema
  - a new branch model
  - a competing architecture

## Ownership Boundaries

### 1. Canonical Data Layer

Owned by the botanical schema and locked builder docs.

Authoritative files:

- `sql/botanicals/00_core_schema.sql`
- `docs/BOTANICAL_SYSTEM_SOURCE_OF_TRUTH_V2.md`
- `docs/BOTANICAL_DATABASE_BUILDER_HANDOVER_V2.md`
- `docs/BOTANICAL_CANONICAL_VS_ALIAS_MAPPING_V2.md`

This layer defines:

- tables
- fields
- row logic
- product logic
- branch logic
- layer logic
- symbiosis / companion separation

The frontend may not redefine this layer.

### 2. App Logic Layer

Owned by the botanical app build.

This layer may define:

- search
- filtering
- scoring
- recommendations
- user workflow
- shortlist logic
- launch-slice defaults

This layer must consume canonical schema fields and may not invent schema
structure.

### 3. Presentation Layer

Owned by the frontend / pitchdeck / UI mock.

This layer may define:

- visual style
- wording
- navigation
- simplification of labels
- progressive disclosure
- cards, maps, and views

This layer may simplify.
This layer may not redefine source-of-truth row logic or canonical fields.

### 4. HNOS Integration Layer

Owned by the wider framework integration.

This layer may provide:

- auth
- shared identity
- node relationships
- permissions
- messaging
- agreements / contract execution
- cross-module orchestration

The botanical app must remain standalone-capable even when these integrations
are absent.

## Living Gardens Rule

`Living Gardens` is a feature / module expression inside the botanical app
direction.

It is not a separate database architecture.
It is not permission to fork the schema.

It may shape:

- launch framing
- UI language
- modular garden workflows
- curated product / habitat bundles

It may not replace the canonical botanical data model.

## Naming Structure

Use this structure consistently:

- `HNOS` = framework / umbrella system
- `Modular Gardens` = botanical app / product name
- `Atlantic Forest / Green Coast` = launch focus inside Brazil branch one
- frozen botanical schema = shared backend truth underneath

This naming structure does not change schema, branch logic, or row rules.

## Layer Filter Rule

Canonical layer values remain fixed:

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

`food_forest_layer` may be used as a friendly display label, but canonical
layer fields remain authoritative.

The frontend may expose friendlier food-forest labels built from canonical
layer plus size.

Examples:

- `Canopy` -> `canonical_layer_primary = canopy`
- `Sub-canopy` -> `canonical_layer_primary = subcanopy`
- `Large Shrubs` -> `canonical_layer_primary = shrub` + larger size filter
- `Small Shrubs` -> `canonical_layer_primary = shrub` + smaller size filter
- `Ground Cover` -> `canonical_layer_primary = groundcover`

The frontend may also expose micro-enclosure aliases built from canonical
layer, size bands, and `layer_stack_tags`.

Examples:

- `Micro Mat` -> `canonical_layer_primary = groundcover` and
  `layer_stack_tags` contains `micro_mat`
- `Micro Low` -> `groundcover` or compact `epiphyte` and
  `layer_stack_tags` contains `micro_low`
- `Micro Mid` -> `herbaceous` or compact `epiphyte` and
  `layer_stack_tags` contains `micro_mid`
- `Micro Upper` -> upper `herbaceous`, `epiphyte`, or `climber` and
  `layer_stack_tags` contains `micro_upper`

These are alias filters only. They are not new canonical layers.

Curated choice views should:

- prefer max `2` shared-name options per canonical layer
- allow `3` only when rows are functionally distinct and source-backed
- rank the smallest occupied form first inside the layer it actually fits

Do not add vague UI labels such as `brush` unless a precise alias rule is
written first.

## Product Logic Rule

The app must preserve both directions:

- `product -> matching botanical entries / varieties / trees`
- `botanical entry / tree / variety -> valid product paths`

Do not collapse product logic into loose notes, tags, or presentation-only
filters.

## Standalone Rule

The botanical app should be built as:

- standalone-first
- HNOS-compatible

This means the app must still function for:

- browsing
- filtering
- botanical planning
- product-path exploration
- branch / zone exploration

without requiring full HNOS runtime integration on day one.

## What The Frontend May Never Redefine

- schema shape
- table philosophy
- row rules
- branch model
- product path model
- symbiosis model
- canonical layer model

## Build Rule

Frontend and pitchdeck work must align to the frozen schema and current branch
rules.

If the UI needs a simpler label or grouped filter, implement that as an alias
or presentation rule, not as a schema change.
