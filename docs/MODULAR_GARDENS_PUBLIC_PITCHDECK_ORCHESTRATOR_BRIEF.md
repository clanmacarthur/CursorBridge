# Modular Gardens Public Pitchdeck Orchestrator Brief

**Mode:** tailored public pitch + mock-interactive demonstration  
**Repository:** `clanmacarthur/CursorBridge`  
**Do not convert the approved Modular Gardens mock into a generic investor deck or redesign its frozen shell.**

## 1. Assignment

Create the public narrative and demo storyboard:

> **From a Plot to a Living System to a Connected Community Application**

The pitch must show one coherent HNOS route:

```text
Plot Holder describes a site, assets, species, and goals
        ↓
Modular Gardens creates a botanical and modular proposal
        ↓
Optional sensors, irrigation, and mesh infrastructure are added
        ↓
The proposal creates or connects an HNOS dashboard
        ↓
Real or simulated field data updates the dashboard
        ↓
Seed & Plant Share turns selected species and harvest records into draft offers or requests
        ↓
VWB receives evidence when verification is required
        ↓
The same reusable infrastructure can generate another application
```

This is a demonstration of HNOS as a reusable application foundry. The mesh node is a proof of physical/data infrastructure, not the entirety of HNOS or Modular Gardens.

## 2. Canonical naming

Use consistently:

- `HNOS` = wider framework
- `Modular Gardens` = user-facing botanical app/module
- `Garden-in-a-Box` = one configurable product route inside Modular Gardens
- `Plot Holder` = broad user-facing site role
- `Validation Workbench (VWB)` = validation authority
- `Seed & Plant Share` = first exchange/reference application

Do not call the entire product Garden-in-a-Box.

## 3. Claims boundary

Every claim or visual must be tagged as one of:

```text
WORKING NOW
PROTOTYPE INTEGRATION
PLANNED PRODUCT
LONG-TERM VISION
```

### Working now

- CursorBridge botanical schema, source-of-truth docs, exports, and build scripts
- Modular Gardens workstream and controlled mock rules
- botanical search/filter/product-path foundations
- Dashboard Manager generator, AI proposals, typed Entry system, templates, automations, and public API
- two Seeed Meshtastic devices
- TEST 0 Meshtastic mock-packet pack

### Prototype integration

- Meshtastic edge connector into HNOS/Dashboard Manager
- generated HNOS field dashboard
- geographic node/link/range map
- VWB request/status bridge using mock callbacks
- Seed & Plant Share draft listing and matching demonstration

### Planned product

- Modular Gardens Plot Builder
- deterministic Generate Mesh Node Plan
- country-aware component/cost catalogue
- native HNOS Mesh Console
- guided species/guild planning on sufficient site data

### Long-term vision

- multi-plot networks
- verified exchanges and public blueprints
- generated applications for additional sectors
- installer/order handoff and fleet operation

## 4. Public deck sequence

| Slide | Title | Public message | Required visual |
|---:|---|---|---|
| 1 | A plot is more than a location | People have land, containers, species, devices, knowledge, and goals—but these remain disconnected | Before-state collage/diagram |
| 2 | HNOS Layer 1 | Shared infrastructure joins inputs, permissions, dashboards, validation, and action | HNOS building-block stack |
| 3 | Enter through Modular Gardens | The Plot Holder describes the site, permissions, existing assets, and desired outcomes | Existing compact mock with new branch highlighted |
| 4 | Use real botanical structure | Species, layers, products, and companion logic come from the canonical botanical database | Botanical card/filter/product-path view |
| 5 | Generate the living proposal | Modular Gardens combines site context, species, modules, water, power, and maintenance | Proposal fan-out diagram |
| 6 | Reuse what already exists | Existing pumps, nodes, solar panels, plants, and tools reduce cost and waste | Existing-assets audit and delta list |
| 7 | Add optional sensing and mesh | HNOS proposes monitoring or connectivity only where the goal requires it | Optional branch diagram |
| 8 | Simulate before deployment | A mock packet proves the software path before relying on range or hardware installation | TEST 0 packet animation |
| 9 | Measure the real network | Range comes from numbered packets, GPS points, RSSI, SNR, and packet success—not an AI promise | Map with survey points and measured link |
| 10 | Generate the operational dashboard | The same plan produces private, collective, and public views | Dashboard mock with map and field data |
| 11 | Connect Seed & Plant Share | A selected species, seed, plant, cutting, or harvest becomes a draft offer or request | Listing/match flow |
| 12 | Verify without duplicating work | Evidence can be submitted from the dashboard while VWB remains the validation authority | Request → Pending in VWB → Verified by VWB |
| 13 | One foundry, many applications | The reusable inputs, permissions, dashboards, connectors, and validation route can generate other tools | App Blueprint Registry |

## 5. Live mock-interactive demonstration

The demo should remain inside the approved compact CursorBridge/Modular Gardens shell wherever possible.

### Demo A — Configure a plot

1. Open `Modular Gardens`.
2. Select `My Plot` or `Configure My Plot / Garden`.
3. Enter country, approximate location, Plot Holder relationship, and permission scope.
4. Enter area, water, power, sun/shade, and obstructions.
5. Record existing assets—including two Seeed nodes, antennas, pump, and solar panel.
6. Select outcomes: irrigation, environmental monitoring, crop/harvest logging, and Seed & Plant Share.
7. Add an existing or planned species from the canonical botanical search.

### Demo B — Generate the proposal

Show:

- selected module or Garden-in-a-Box route
- species and candidate guilds
- reused assets
- optional sensor/mesh branch
- country-aware low/expected/high cost
- assumptions and missing information
- TEST 0 and measured range-test gates
- action to create/connect an HNOS dashboard

### Demo C — Simulated mesh packet

1. Run the prepared TEST 0 packet.
2. Show packet ID, node, timestamp, RSSI, SNR, and telemetry.
3. Show the packet normalising into HNOS/dashboard records.
4. Mark this clearly as simulated.

### Demo D — Measured map

Show separate layers:

- fixed node markers
- measured radio links
- walking-survey points
- measured heatmap
- predicted planner layer clearly labelled as prediction

Do not infer location from RSSI.

### Demo E — Seed & Plant Share

1. Mark a species/crop record `available_to_share` or `wanted`.
2. Create a draft offer or request.
3. Show approximate-location matching, date, quantity, and visibility.
4. Do not publish automatically.

### Demo F — VWB bridge

1. Select a claim or field observation.
2. Attach evidence.
3. Click `Send to VWB for verification`.
4. Show `Pending in VWB`.
5. Apply a seeded mock return and show `Verified by VWB`.

## 6. Public language

Use:

```text
Plot Holder
Configure my plot
Generate a proposal
Generate a Mesh Node Plan
Proposed node placement
Estimated cost range
Measured range survey
HNOS connection
Generated dashboard
Draft Seed & Plant Share listing
Send to VWB for verification
Permissioned collective data
```

Avoid:

```text
Landowner as the universal user role
Guaranteed 4 km range
AI buys or installs the system
Dashboard validates evidence
HNOS owns Meshtastic
Every user requires a node
Exact private coordinates on public maps
Autonomous pump control in the public demo
Garden-in-a-Box as the name of the entire app
```

## 7. Visual rules

- preserve the approved compact control-surface shell
- no new hero or oversized title block in the interactive mock
- use horizontal-first packing
- keep side panels collapsed by default
- avoid tall stacks of cards and excessive whitespace
- use progressive disclosure for technical detail
- do not redesign approved screens to fit conventional pitchdeck expectations
- create diagrams separately where the deck needs a simplified public explanation

## 8. Required diagrams and screenshots

1. HNOS Layer 1 building-block stack
2. Modular Gardens click tree with optional mesh branch
3. Plot inputs → generated proposal outputs
4. Botanical database → species/product/guild suggestions
5. Node → Meshtastic → edge connector → HNOS dashboard
6. Node/link/survey/heatmap map mock
7. Species record → Seed & Plant Share draft → match
8. Dashboard → VWB → returned status
9. App Blueprint Registry showing reuse

## 9. Evidence and privacy register

The orchestrator must maintain a companion table:

```text
Claim
Status class
Source/evidence
Screenshot or diagram
Mock/live label
Privacy treatment
Speaker-note caveat
```

Exact site coordinates, private messages, channel keys, legal agreements, and private-incubator concepts are excluded from the public deck.

## 10. Required orchestrator outputs

```text
5-minute deck outline
12-minute deck outline
speaker notes
live-demo runbook
screenshot/diagram shot list
claims and evidence register
mock-versus-live labels
technical appendix
follow-up implementation roadmap
```

## 11. Closing proposition

> **HNOS provides reusable building blocks that turn a place, its living systems, its people, and its data into a permissioned application—demonstrated first through Modular Gardens, connected field nodes, and Seed & Plant Share.**
