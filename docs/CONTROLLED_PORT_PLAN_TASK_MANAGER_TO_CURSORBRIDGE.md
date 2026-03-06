# Controlled Port Plan: task-manager -> CursorBridge

Last updated: 2026-02-21
Status: in progress

## Goal

Bring proven `/sessions` behavior from `task-manager` into `CursorBridge` safely, without breaking the current `/session` flow.

## Guardrails

- Keep `/session` working during all phases.
- Keep behavior deterministic (no runtime AI requirement).
- Move in small steps: backend contract first, then UI.
- Do not switch production route defaults until parity checks pass.

## Phase order

### Phase 1: Theme graph endpoint first (started)

Objective:
- Make `GET /api/session/themes` return real graph data in `CursorBridge main-app-starter`.

Done now:
- Ported theme graph engine file:
  - `main-app-starter/domain/engine/themes.ts`
- Wired endpoint:
  - `main-app-starter/server/api/session/themes.get.ts`
  - uses `serverSupabaseClient` + `buildThemeGraphFromSupabase`
- Added resilient fallback response if data loading fails in environment.

Verification:
- `main-app-starter` build passes.

### Phase 2: Contract alignment for preview/generate (started)

Objective:
- Keep stubs for now, but make response keys match live contract shape from `task-manager`.

Done now:
- Updated:
  - `main-app-starter/server/api/session/preview.post.ts`
  - `main-app-starter/server/api/session/generate.post.ts`
- Both now return contract-style keys such as:
  - `output_data`
  - `narration_text`
  - `session_run_id` / `session_output_id` (generate)
  - `dial_selection` / `theme_selection` inside `output_data`

Still pending:
- Replace stub logic with real planner + persistence behavior.

### Phase 3: Wheel UI port (next)

Objective:
- Move stable wheel UI components from `task-manager` after endpoint parity is confirmed.

Planned components to port:
- `AllThemesWheel.vue` (baseline first)
- optional style panel/workbench variants later

Rule:
- Baseline wheel first, styling extras second.

### Phase 4: Preview/generate logic port

Objective:
- Move real planning logic behind:
  - `POST /api/session/preview`
  - `POST /api/session/generate`

Need before this step:
- Confirm required tables and mappings are present in current Supabase project.
- Confirm planner utility dependencies are either ported or replaced.

### Phase 5: Route promotion decision

Objective:
- Decide when `/sessions` becomes active runtime in this repo.

Promotion checks:
- Theme graph endpoint stable.
- Preview/generate real logic stable.
- UI parity tested.
- `/session` fallback remains available until sign-off.

## Current state snapshot

- `/session`: live and working.
- `/sessions`: placeholder page.
- `GET /api/session/themes`: now wired.
- `POST /api/session/preview`: stub, contract aligned.
- `POST /api/session/generate`: stub, contract aligned.
