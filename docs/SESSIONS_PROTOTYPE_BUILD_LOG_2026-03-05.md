# Sessions Composer Prototype Build Log (2026-03-05)

## Scope Locked For This Pass

- Used existing live inventory files only.
- Built a clean parallel prototype route, without patching old `/sessions` behavior in place.
- Kept excluded systems out of the prototype (`session_blueprints`, `session_templates`, `narration_styles`, `lens_definitions`, `meta_lens_presets`, `control_*`, `coupling_rules`).

## Source Files Used

- `docs/SESSIONS_DOMAIN_INVENTORY_2026-03-05.md`
- `docs/SESSIONS_SUBJECT_TREE_2026-03-05.md`
- `docs/SESSIONS_FIELD_MAP_2026-03-05.md`
- `docs/_sessions_domain_inventory_live_2026-03-05.json`
- `docs/_sessions_support_inventory_live_2026-03-05.json`
- `docs/_sessions_subject_tree_live_2026-03-05.json`
- `docs/_sessions_drilldown_lists_live_2026-03-05.json`

## Build Outputs

- `main-app-starter/pages/sessions-composer-prototype.vue`
- `main-app-starter/server/api/session/composer-payload.get.ts`
- `main-app-starter/server/api/session/composer-save.post.ts`
- `docs/SESSIONS_UI_PAYLOAD_2026-03-05.json`
- `docs/_sessions_prototype_flow_results_2026-03-05.json`
- `docs/screenshots/sessions-composer-2026-03-05/flow-1-breath-only.png`
- `docs/screenshots/sessions-composer-2026-03-05/flow-2-breath-movement.png`
- `docs/screenshots/sessions-composer-2026-03-05/flow-3-breath-colour-sound-movement-nutrition.png`

## Route Check

- Route: `/sessions-composer-prototype`
- Server render status: `200`
- Top subject row loaded from live payload:
  - `Activation`
  - `Breath Awareness`
  - `Hypnosis`
  - `NSDR`
  - `Somatic Regulation`
  - `Trauma Titration`

## Required Flows (Executed)

1. Breath-only flow
- Screenshot: `docs/screenshots/sessions-composer-2026-03-05/flow-1-breath-only.png`
- `session_runs.id`: `f787f598-4bf0-4a77-8d55-270f867d07e7`
- `session_outputs.id`: blocked by policy (none written)

2. Breath + movement flow
- Screenshot: `docs/screenshots/sessions-composer-2026-03-05/flow-2-breath-movement.png`
- `session_runs.id`: `3a0d2257-e6dd-4ec8-99cd-16c75dc2f50d`
- `session_outputs.id`: blocked by policy (none written)

3. Breath + colour/sound + movement + nutrition flow
- Screenshot: `docs/screenshots/sessions-composer-2026-03-05/flow-3-breath-colour-sound-movement-nutrition.png`
- `session_runs.id`: `864a2ff8-1496-4206-a55b-aab2c947fd45`
- `session_outputs.id`: blocked by policy (none written)
- Nutrition row used from live table: `nutrition_and_food` label `Herb / Spice`

## Blocker (Stop Condition Reached)

- Blocking table: `session_outputs`
- Exact issue: `new row violates row-level security policy for table "session_outputs"` (`403`, code `42501`)
- Smallest fix needed:
  - Add an INSERT policy on `session_outputs` that allows authenticated users to insert rows when:
    - `session_outputs.session_run_id` belongs to `session_runs.id`
    - and that `session_runs.user_id = auth.uid()`

## Supporting Evidence

- Full run artifact: `docs/_sessions_prototype_flow_results_2026-03-05.json`
- Includes:
  - route status
  - top-level subjects
  - flow stacks
  - screenshot status and paths
  - save responses and blocker payloads

## Notes Applied During This Pass

- Added route-level auth exclusion for prototype view only:
  - `main-app-starter/nuxt.config.ts` now excludes `/sessions-composer-prototype` from Supabase auth redirect.
- Added test-only flow presets via query string (`?flow=...`) in prototype page to make repeatable screenshots.

## RLS Fix Attempt (2026-03-06)

- Prepared SQL patch file:
  - `sql/rls/session_outputs_owner_policies.sql`
- This patch includes:
  - policy inspection query for `session_runs` and `session_outputs`
  - ownership check for `session_runs.user_id`
  - smallest safe INSERT policy for `session_outputs`
  - matching SELECT policy for `session_outputs`
- SQL execution status from this workspace:
  - Not applied yet (current credentials are anon-level only, no DB-admin execution path available here).

Re-run after patch preparation:

1. Breath-only
- `session_runs.id`: `35287e91-e513-433b-ad28-b4462d3f8701`
- `session_outputs.id`: none (still blocked by RLS)

2. Breath + movement
- `session_runs.id`: `18e2aa7a-8c5b-4958-a3c2-37f80ee83825`
- `session_outputs.id`: none (still blocked by RLS)

3. Breath + colour/sound + movement + nutrition
- `session_runs.id`: `fc09c520-c49e-42e1-b202-f68022beff9f`
- `session_outputs.id`: none (still blocked by RLS)

Still-blocking error after rerun:
- `new row violates row-level security policy for table "session_outputs"` (`403`, code `42501`)
