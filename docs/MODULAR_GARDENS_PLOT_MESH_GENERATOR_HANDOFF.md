# Modular Gardens — Plot Builder, Mesh Option, and HNOS Handoff

**Status:** implementation handoff for the Modular Gardens workstream inside CursorBridge  
**Repository role:** flow mapping, mock-interactive controls, data contracts, and handover packaging  
**Do not treat this file as permission for a broad UI redesign or a botanical-schema rewrite.**

## 1. Product placement

`Modular Gardens` remains the user-facing botanical app/module name.

`Garden-in-a-Box` is one configurable product path inside Modular Gardens. It is not the name of the whole app, schema, or HNOS layer.

The proposed user journey is:

```text
Modular Gardens
  -> Configure My Plot / Garden
      -> describe site and permissions
      -> record existing assets
      -> select existing / planned / wanted species
      -> choose goals and garden/module type
      -> optional water, sensor, automation, and mesh branch
      -> generate a versioned proposal
      -> review assumptions, price range, tests, and next actions
      -> create or connect an HNOS dashboard
      -> optional Seed & Plant Share draft
```

The first implementation in CursorBridge is a controlled interactive mock and handoff, not a production hardware configurator.

## 2. Repository constraints

Apply the current CursorBridge control files in this order:

1. `CURSORBRIDGE_LAYOUT_FREEZE.md`
2. `CURSORBRIDGE_CHANGE_REQUEST_TEMPLATE.md`
3. `CURSORBRIDGE_CHAT_AGENT.md`
4. `AGENTS.md`
5. `CANON_AGENT_SYSTEM.md`

Mandatory UI rules:

- delta edit only
- preserve the approved compact shell
- keep the header unchanged
- retain horizontal-first packing
- keep side panels hidden by default
- do not add hero/title drift
- do not enlarge cards or increase empty space
- map the user's explicit click tree before broad implementation

## 3. Canonical data boundaries

The botanical database remains the source of truth for species, layers, products, branch logic, zones, and companion/symbiosis data.

Use:

- `sql/botanicals/00_core_schema.sql`
- `docs/BOTANICAL_SYSTEM_SOURCE_OF_TRUTH_V2.md`
- `docs/BOTANICAL_DATABASE_BUILDER_HANDOVER_V2.md`
- `docs/BOTANICAL_APP_BOUNDARIES_V1.md`
- `docs/BOTANICAL_APP_BUILD_ORDER_V1.md`

The frontend may simplify labels and provide aliases. It may not invent new canonical botanical layers, rewrite product-to-botanical relationships, or fork the shared branchable schema.

HNOS integration is additive. Modular Gardens must remain standalone-capable for browsing, filtering, botanical planning, and product-path exploration when wider HNOS services are unavailable.

## 4. User-facing role language

Use **Plot Holder** as the broad interface role.

Store the actual relationship separately:

```text
owner
joint_owner
tenant
licensee
allotment_holder
community_manager
site_host
caretaker
authorised_operator
other
```

Do not use `landowner` as the universal interface label. Retain it only where legal ownership is specifically relevant.

## 5. Click-tree draft

This is a draft branch to merge into the user's explicit Modular Gardens tree. It must not replace a more recent approved tree.

```text
MODULAR GARDENS
|
+-- Explore Species
|   +-- Search / filter canonical botanical data
|   +-- View botanical card
|   +-- View valid product paths
|   +-- Add to shortlist / existing / planned / wanted
|
+-- Configure My Plot / Garden
|   +-- 1. Location and country
|   +-- 2. Plot relationship and permissions
|   +-- 3. Plot map, dimensions, sun, slope, drainage
|   +-- 4. Existing assets and existing species
|   +-- 5. Desired outcomes
|   +-- 6. Species, crops, products, modules, and guild goals
|   +-- 7. Water, power, and connectivity
|   +-- 8. Optional sensors, irrigation, and mesh
|   +-- 9. Budget, maintenance, and build preference
|   +-- 10. Review and generate proposal
|
+-- Generated Proposal
|   +-- Plot profile
|   +-- Modular Garden / Garden-in-a-Box configuration
|   +-- Species and guild candidates
|   +-- Existing assets reused
|   +-- Water and power plan
|   +-- Optional sensor and mesh plan
|   +-- Country-aware bill of materials and price range
|   +-- Build and test sequence
|   +-- HNOS dashboard handoff
|   +-- Seed & Plant Share draft handoff
|
+-- My Plot & Records
    +-- Species inventory
    +-- Planting and crop cycles
    +-- Observations and harvests
    +-- Sensor / mesh state when connected
    +-- Private / group / collective / public visibility
```

## 6. Guided inputs

### Site and permission

- country and region
- approximate or exact location
- plot relationship
- permission to install structures, pumps, poles, aerials, sensors, or solar equipment
- coordinate visibility: private, group, collective, or public

### Plot and environment

- area and dimensions
- boundary drawn or imported on a map
- urban / suburban / rural / remote
- slope and drainage
- sun and shade zones
- buildings, walls, mature trees, and radio obstructions
- water source and water storage
- power and connectivity already available

### Existing assets

- beds, modules, crates, greenhouse, pond, tank, irrigation, pumps, tools
- controllers, Meshtastic nodes, antennas, solar panels, batteries, sensors
- existing species, seeds, trees, propagation stock, and products

Every compatible owned asset must reduce the generated purchase quantity.

### Goals

- food growing
- propagation / nursery
- habitat / biodiversity
- Garden-in-a-Box or another module format
- irrigation
- environmental monitoring
- crop / harvest logging
- Seed & Plant Share
- education / community use
- research
- optional camera / AI logging
- optional mesh communications

### Species

Use canonical botanical references where available and capture:

- existing / planned / wanted / available to share
- quantity
- plot zone
- planting or transplant date
- intended product path
- harvest or propagation intention
- visibility

## 7. Botanical recommendation gate

The catalogue remains browsable without onboarding.

Tailored companion, guild, and site-placement suggestions require at minimum:

```text
location or climate profile
sun / shade context
water availability
soil / drainage or an explicit unknown
at least one species or outcome
```

Every recommendation must display one of these evidence labels:

```text
canonical botanical fact
sourced local restriction
traditional association
experimental Modular Gardens recommendation
user observation
AI hypothesis requiring review
```

## 8. Optional mesh branch

The mesh branch is optional and appears only when the user selects communication, remote sensing, irrigation, alerting, or multi-site coordination.

User-facing action:

```text
Generate a Mesh Node Plan
```

It produces a design proposal, not an automatic purchase or range guarantee.

Questions:

- required distance and direction
- fixed and mobile endpoints
- buildings, trees, terrain, and possible mounting height
- available power at each position
- existing Meshtastic hardware
- sensor and actuator requirements
- operating time through darkness or bad weather
- internet availability
- data frequency and visibility
- minimum viable / balanced / resilient preference

Outputs:

- node count and roles
- proposed positions and coverage assumptions
- power architecture
- antenna and mounting plan
- sensors / actuators
- existing assets reused
- bill of materials and country-aware cost range
- TEST 0 simulation
- local two-node test
- measured range-survey gate
- generated HNOS dashboard requirements

Never guarantee radio range before measured testing.

## 9. Meshtastic presentation inside HNOS

Meshtastic is not a second user-facing dashboard in the target architecture.

Use:

- an edge connector for continuous collection
- an HNOS Mesh Console widget for authorised node, message, telemetry, and survey views
- a geographic map widget for nodes, links, survey points, and measured heatmaps
- an optional link to the official Meshtastic console for advanced device configuration

CursorBridge's current responsibility is to define the flow, mock controls, and handoff contract. Production integration belongs to the appropriate runtime repository after licensing and architecture gates are resolved.

## 10. Generated proposal contract

The mock should emit a versioned object shaped broadly like:

```json
{
  "status": "draft",
  "plotProfile": {},
  "existingAssets": [],
  "speciesSelections": [],
  "modulePlan": [],
  "meshNodePlan": [],
  "sensorPlan": [],
  "costLines": [],
  "costRange": {
    "low": null,
    "expected": null,
    "high": null,
    "currency": "GBP",
    "checkedAt": null
  },
  "assumptions": [],
  "warnings": [],
  "requiredTests": [],
  "dashboardHandoff": {},
  "seedPlantShareDrafts": []
}
```

AI may explain and help complete the proposal. Cost arithmetic, owned-asset subtraction, country rules, safety gates, and pass/fail tests must be deterministic or explicitly unresolved.

## 11. Mock screen delta

Do not redesign the shell. Add only the requested region to the existing Modular Gardens mock flow.

Suggested compact controls:

```text
[Explore] [My Plot] [Build] [Species] [Records]

My Plot
Country | Area | Relationship | Water | Power | Existing assets

Build
Module | Species goal | Irrigation | Sensors | Mesh | Budget

Result
Plan status | Reused assets | Estimated cost | Required tests | Create dashboard
```

Use compact tabs, minimal padding, horizontal-first fields, and collapsible detail rather than tall stacked cards.

## 12. Build order in CursorBridge

1. Create/update the explicit flow map.
2. Confirm the allowed UI region and frozen regions through the change-request template.
3. Add the minimal clickable mock branch.
4. Add fixture data using canonical botanical fields.
5. Add the generated-proposal mock object.
6. Add the optional mesh-plan placeholder and TEST 0 state.
7. Package the handoff for Dashboard Manager / HNOS runtime integration.
8. Do not implement production purchasing, live radio control, or schema migrations in this phase.

## 13. Acceptance criteria

- Modular Gardens remains the app name.
- Garden-in-a-Box appears only as a configurable route/product format.
- The approved CursorBridge shell and header are unchanged.
- The explicit click tree is preserved and extended, not flattened.
- Canonical botanical data fields are consumed without schema invention.
- The user can record existing assets before recommendations are generated.
- Plot relationship is separate from legal ownership.
- The mock can show species, module, optional mesh, cost, test, dashboard, and sharing outputs.
- Cost and range are presented with assumptions and gates.
- No production Meshtastic SDK or direct device control is added in this workstream.
- A clean handoff package exists for the runtime repositories.
