# Sessions Master

Last updated: 2026-03-05
Status: master sessions reference
Source pages:
- `2dcc47c6-1e21-80ed-b68b-d49d46c2f28a` (Sessions)
- `2d5c47c6-1e21-809b-95aa-d3c17be66d50` (Entire User Plan Notes)
- Active build spec:
  - `docs/SESSIONS_COMPOSER_LOCKED_SPEC_2026-03-05.md`
- Legacy archived architecture:
  - `docs/legacy/SESSION_GENERATION_RUNTIME_SPEC_LEGACY_2026-03-05.md`

## Purpose

This is the master sessions document.
It merges:

- The Notion Sessions notes.
- Local handover notes in this repo.
- The current app reality (`/session` today, `/sessions` placeholder UI, theme endpoint now wired).

## Scope

This file covers the current Session Composer direction:

- subject-first entry
- one large domain wheel
- drawer-based row selection
- stack-based composition
- preview
- save as custom session

Programmes (scheduled tasks over days to months) remain the next layer.
Programmes are not the first prototype entry path.

## Plain Definitions

- Session: one guided run a user does now.
- Session template: an older recipe layer; parked for first composer prototype.
- Programme profile: preset that steers defaults and safety level.
- Persona: voice/tone of narration.
- Lens: explanation style or framework.
- Mode: conversation posture (coach, analyst, gentle support, etc.).

## Core Model To Keep Stable

- Keep one universal control/knob library for all adjustable inputs.
- Use deterministic control mapping (slider vs checkbox) so UI decisions are repeatable.
- Keep dialogue intake flexible, but always write answers into stable structured fields.

## Immediate Priority (From User Plan Notes)

- Create the `controls_library` schema first as the single source of truth for trackable controls.
- Create the `user_profiles` schema first so persona choice is profile-owned and not embedded in content rows.
- Do schema first, then seed/populate in later passes.

## Deterministic Control UI Rule

- bounded numeric control -> slider
- binary yes/no control -> checkbox
- small fixed options -> select/radio
- control type is decided by control metadata, never ad-hoc per screen

## Nutrition Layering Rule

- Keep nutrition effects in taxonomy/ontology tables.
- Keep food/protocol libraries as additive content that points into taxonomy.
- This allows large nutrition expansion without changing runtime mechanics.

## What Can Be Parked Safely

- Long diet and protocol lists.
- User-created custom libraries.
- Advanced colour/sacred geometry/symbol expansion.
- Park these until controls + profiles schemas are locked.

## Current Code Reality

- Live route: `/session`
- File: `main-app-starter/pages/session.vue`
- Current generation path:
  - `main-app-starter/server/api/bridge/session.post.ts`
  - proxy to `POST /sandbox/generate-session`

Planned route and contract path now exists:

- `/sessions` placeholder page:
  - `main-app-starter/pages/sessions.vue`
- Session endpoints:
  - `GET /api/session/themes` is now wired to Supabase theme graph loading.
  - `POST /api/session/preview` remains stubbed but now returns contract-shaped payload keys.
  - `POST /api/session/generate` remains stubbed but now returns contract-shaped payload keys.

## Canonical Session Composer Flow

Subject selected
-> Domain wheel shown
-> Domain clicked
-> Drawer opens with real rows + live filters
-> User adds items to session stack
-> Preview combined session + warnings
-> Save to session output path

## Runtime Contract

## Input (minimum)

- `user_id` or `programme_profile_id`
- `duration_minutes`
- `strictness`
- optional `persona_id`
- optional `lens`
- optional future `themeSelection`

## Output (minimum JSON)

- `phases[]` (arrival, main, downshift, close)
- `steps[]` per phase (breath, movement, sound, stillness)
- `cues[]` with timestamps
- `safety_notes[]`
- `contraindications_triggered[]`
- adjustable controls (pace, pause, intensity)
- metadata (lens, persona, profile, template, timing preset)

## Rules We Keep Stable

1. Timeline first, narration second.
2. Lens/persona/mode can change language, not timing math.
3. Safety gating is mandatory.
4. Session output shape must stay stable even when content sources grow.

## Separation Rules (Very Important)

## Programme Profile

Decides what is relevant by default:

- safety strictness
- suitable session types
- default packs/controls

## Persona

Decides how it sounds:

- tone
- narrative style
- voice flavor

## Mode

Decides what conversation we are having now:

- coaching vs analysis vs reflection
- which outputs to emphasize
- depth of questioning

## Lens

Decides the explanation framework:

- clinical
- somatic
- traditional systems
- hybrid

None of these should directly mutate schema design.

## Delivery Architecture (Who Does What)

## Main App

- Renders session JSON for the user.
- Stores user runtime data (check-ins, session history, outcomes).
- Does not own library curation or safety logic.

## Bridge / Operator

- Syncs Notion and other sources into Supabase.
- Runs mapping, schema checks, and manifests.
- Does not own end-user runtime behavior.

## Sandbox / Runner

- Builds sessions from templates and rules.
- Applies safety gating.
- Adds optional explanation blocks (for example clinical or TCM wording).
- Returns deterministic session JSON for the main app to render.

## One-Line Build Instructions

- Main app: render and log, do not generate core session logic.
- Bridge: sync and govern canonical data, do not own runtime generation.
- Sandbox: generate sessions, enforce safety, and return structured output.

## Data Ownership Map

## Canonical Libraries (Supabase)

- templates
- techniques
- safety rules
- voice/lens/persona knowledge
- supporting ontology and mappings

## User Runtime (Supabase)

- user profile and preferences
- check-ins and control values
- session instances and outcomes

## Sandbox Staging (optional)

- draft session outputs
- validation artifacts
- approval states before promotion

## Composition Requirement For Multi-Technique Sessions

For complex sessions, step ordering must be explicit.
If current templates do not store ordered steps, add a stable step table.

Suggested fields:

- `template_id`
- `step_order`
- `step_type` (breath, movement, sound, education, rest)
- `referenced_item_id`
- `duration_seconds` or reps
- `intensity_level`
- `notes`

## Explanation Source Requirement

If explanations can switch between frameworks, source control is required.

Minimum source layer:

- evidence/source registry
- approved knowledge snippets
- technique annotations linking techniques to source snippets

Rule:

- Do not copy protected text without rights.
- Store references and approved summaries where needed.

## Data Sources For First Composer Prototype

Domain libraries used directly:

- `breath_library`
- `movements_system`
- `organ_emotion_system`
- `meridian_system`
- `light_colour`
- `sound_vibration`
- `nutrition_and_food`
- `nutrition_protocols`
- `symbols_index`

Support/logic tables used directly:

- `attribute_taxonomy`
- `mappings`
- `cross_domain_mappings`
- `safety_rules`
- `session_types`
- `session_runs`
- `session_outputs`

Parked for first prototype (do not drive first composer build):

- `session_blueprints`
- `session_templates`
- `narration_styles`
- `lens_definitions`
- `meta_lens_presets`
- `control_packs`
- `coupling_rules`

## Build Order

1. Keep `/session` stable.
2. Implement first composer behavior on `/sessions` using subject -> wheel -> drawer -> stack -> preview -> save.
3. Keep `/api/session/*` contract stable while logic is added.
4. Complete field-map/data-gap cleanup for empty filter columns.
5. Move broader architecture changes to Convex phase only after Supabase parity checks pass.

## Parked For Later

- Inner multi-ring wheel visuals per domain.
- Smarter text layout in arcs.
- Advanced sizing and ring ordering logic.
- Programmes:
  - scheduled tasks across days to months
  - adherence tracking
  - progression rules and plan-level safety checks

## Programmes Later (Boundary)

Programmes are multi-session plans built on top of saved session outputs.

When programmes start, add:

- programme timeline model
- schedule and recurrence rules
- task completion logs
- plan-level adaptation rules

But keep first-session composer entry and single-session output contract unchanged.
