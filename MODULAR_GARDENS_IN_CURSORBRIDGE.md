# MODULAR_GARDENS_IN_CURSORBRIDGE.md

## PURPOSE
Hold the Modular Gardens workstream inside CursorBridge until a dedicated repo exists.

## WHAT BELONGS HERE NOW
- interactive flow mapping
- click-tree logic
- mock UI control rules
- handover packaging
- architecture notes that affect flow and shell behavior
- freeze-state references for approved mock screens
- Plot Builder / Configure My Plot flow design
- optional sensing, irrigation, and mesh-plan branch design
- tailored public pitchdeck and demo orchestration

## WHAT DOES NOT BELONG HERE
- uncontrolled redesign of approved mock screens
- conversion into generic investor-deck structure when the task is mock-interactive
- replacing the explicit user tree with invented flow logic
- production Meshtastic device integration before runtime and licensing gates are resolved
- rewriting the canonical botanical schema from frontend requirements
- treating Garden-in-a-Box as the name of the entire Modular Gardens app

## SOURCE OF TRUTH FOR FLOW
Use the user-provided explicit click tree as the logic source of truth.
Do not flatten it into generic feature groups.

Current additive handoff for the Plot Builder and optional mesh branch:

- `docs/MODULAR_GARDENS_PLOT_MESH_GENERATOR_HANDOFF.md`

This file extends the flow; it does not replace a later or more specific approved click tree.

## SOURCE OF TRUTH FOR BOTANICAL DATA AND BUILD BOUNDARIES
Use:

- `docs/BOTANICAL_APP_BOUNDARIES_V1.md`
- `docs/BOTANICAL_APP_BUILD_ORDER_V1.md`
- `docs/BOTANICAL_SYSTEM_SOURCE_OF_TRUTH_V2.md`
- `docs/BOTANICAL_DATABASE_BUILDER_HANDOVER_V2.md`
- `sql/botanicals/00_core_schema.sql`

`Modular Gardens` remains standalone-first and HNOS-compatible. The frontend may simplify labels and workflows but may not redefine canonical botanical schema, branch, product-path, layer, or symbiosis logic.

## SOURCE OF TRUTH FOR LOOK / SHELL
Use:
- `CURSORBRIDGE_LAYOUT_FREEZE.md`
- approved screenshots / approved current file state

UI edits remain delta-only:

- header frozen unless explicitly changed
- compact control-surface layout
- horizontal-first packing
- minimal padding
- side panels hidden by default
- no hero/title drift
- no enlarged cards or unnecessary whitespace

## HNOS MESHTASTIC TEST PATH
Use:

- `docs/HNOS_MESHTASTIC_TEST0_DASHBOARD_RUNBOOK.md`

The locked sequence is:

```text
TEST 0A — mock packet to local Dashboard Manager payload
DM setup — exact datapoints, packet group, and scoped API key
TEST 0B — mock packet to Dashboard Manager
TEST 0C — real packet captured over USB
TEST 2 — real packet to Dashboard Manager
TEST 1 — measured walking/range survey
```

Do not start the range survey before the short-range packet path passes.

## PUBLIC PITCHDECK / DEMO HANDOFF
Use:

- `docs/MODULAR_GARDENS_PUBLIC_PITCHDECK_ORCHESTRATOR_BRIEF.md`

The public story is:

```text
Plot Holder
  -> Modular Gardens configuration
  -> botanical / module proposal
  -> optional sensing and mesh plan
  -> generated HNOS dashboard
  -> Seed & Plant Share draft or match
  -> optional VWB verification
  -> reusable HNOS application-building blocks
```

Do not expose private coordinates, channel keys, private messages, node-ownership assumptions, or guaranteed range claims.

## NAMING LOCK

- `HNOS` = wider framework
- `Modular Gardens` = user-facing botanical app/module
- `Garden-in-a-Box` = one configurable route/product format inside Modular Gardens
- `Plot Holder` = broad interface role; legal site relationship stored separately
- `Seed & Plant Share` = reference exchange application
- `VWB` = validation authority, not the dashboard

## FUTURE REPO TRANSFER RULE
When a dedicated Modular Gardens repo exists:
- copy this file into that repo
- copy the Modular Gardens plot/mesh and pitchdeck briefs
- copy or link the current HNOS Meshtastic test runbook
- keep `CANON_AGENT_SYSTEM.md` as the shared backbone
- create Modular-Gardens-specific AGENTS / freeze / change-request files there
- preserve links to the canonical botanical schema and exports
- do not silently reinterpret the workstream during transfer
