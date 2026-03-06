# Task Manager vs CursorBridge Alignment

Last updated: 2026-02-21
Scope: compare `C:\code\task-manager` and `C:\code\CursorBridge` so we can merge safely.

## Why this file exists

Both repos describe sessions, wheels, validation, and Supabase-to-Convex migration.
Some statements agree, some conflict, and some are simply different phases.
This file is the practical merge guide.

## High-level result

- They are **not** contradictory at the architecture level.
- They are in **different implementation phases**.
- Main conflict is runtime status wording:
  - `task-manager`: `/sessions` is active and wheel/theme graph APIs are live.
  - `CursorBridge`: `/session` is live and `/sessions` is still planned/stubbed.

## Side-by-side status

| Topic | CursorBridge (current) | task-manager (current) | Conflict type |
|---|---|---|---|
| Main session route | `/session` is live (`main-app-starter/pages/session.vue`) | `/sessions` is live builder (`app/pages/sessions.vue`) | Phase mismatch |
| `/sessions` page | Placeholder (planned builder text) | Full wheel builder with template + preview + generate | Real implementation gap |
| Session APIs | `/api/session/*` return `501 NOT_IMPLEMENTED` | `/api/session/themes`, `/preview`, `/generate` implemented | Real implementation gap |
| Theme graph engine | Not present in `main-app-starter` | Present at `app/domain/engine/themes.ts` | Real implementation gap |
| Wheel components | Not present in `main-app-starter` | `AllThemesWheel`, grid, playground exist | Real implementation gap |
| Validation routes | Not part of `main-app-starter` runtime docs | `/classic` + `/workbench` and validation APIs are canonical | Different app surface |
| Deterministic rule | Present in sessions master wording | Present and enforced in canonical docs | Aligned |
| AI dependency stance | AI optional wording present | AI optional and non-required baseline explicit | Aligned |
| Data source now | Supabase + bridge/sandbox | Supabase + file-backed validation runs | Mostly aligned |
| Convex status | Planned after Supabase parity | Planned phased migration, not complete | Aligned |
| Programmes scope | Parked for later in current phase | Included in sessions canonical behavior spec | Phase mismatch |
| Notion sync coverage | Strong focus and active in this repo | Not main focus | Different responsibility |

## Evidence files used

- `docs/SESSIONS_MASTER.md`
- `docs/HANDOVER_SESSIONS.md`
- `main-app-starter/pages/session.vue`
- `main-app-starter/pages/sessions.vue`
- `main-app-starter/server/api/session/themes.get.ts`
- `main-app-starter/server/api/session/preview.post.ts`
- `main-app-starter/server/api/session/generate.post.ts`
- `C:\code\task-manager\README.md`
- `C:\code\task-manager\SESSIONS_MASTER_SPEC.md`
- `C:\code\task-manager\ARCHITECTURE.md`
- `C:\code\task-manager\CONVEX_MIGRATION_PLAN.md`
- `C:\code\task-manager\app\pages\sessions.vue`
- `C:\code\task-manager\app\server\api\session\themes.get.ts`
- `C:\code\task-manager\app\server\api\session\preview.post.ts`
- `C:\code\task-manager\app\server\api\session\generate.post.ts`
- `C:\code\task-manager\app\domain\engine\themes.ts`

## Source-of-truth decisions (recommended)

1. Runtime truth for **active sessions UI/API behavior**:
   - Use `task-manager` as source-of-truth.
2. Truth for **Notion -> Supabase ingestion and workspace DB inventory**:
   - Use `CursorBridge` as source-of-truth.
3. Truth for **session principles and boundaries**:
   - Keep deterministic/no-runtime-AI rule from `task-manager`.
   - Keep controls-library-first and user-profile-first priorities from `CursorBridge` sessions master.
4. Truth for **migration sequencing**:
   - Supabase-first coverage, then phased Convex cutover (both repos already align here).

## Practical merge plan

### Phase A: Doc unification (safe, immediate)

1. Keep `CursorBridge` docs explicit that it is currently bridge-first and `main-app-starter` is a simplified app surface.
2. Add a boundary note: `task-manager` has newer `/sessions` runtime behavior.
3. Keep one alignment file (this one) and update it whenever either repo changes route/API status.

### Phase B: Contract unification (no UI copy yet)

1. Lock one shared request/response contract for:
   - `GET /api/session/themes`
   - `POST /api/session/preview`
   - `POST /api/session/generate`
2. In `CursorBridge`, keep stubs but match response keys to final contract where possible.
3. Preserve backward compatibility keys:
   - `dialSelection` + `themeSelection`
   - `planner_config` aliases where needed.

### Phase C: Implementation transfer (optional, explicit)

1. Port theme graph server logic from `task-manager` to `CursorBridge` only when ready.
2. Port wheel components only after theme graph endpoint is live in `CursorBridge`.
3. Keep `/session` route working until `/sessions` reaches parity in `CursorBridge`.

### Phase D: Data migration readiness

1. Finish Supabase coverage and control/profile schema lock in `CursorBridge`.
2. Keep `task-manager` Convex plan as migration reference model.
3. Do not cut over to Convex until Supabase parity checks pass.

## Non-negotiable shared guardrails

- Deterministic runtime first, AI optional assist only.
- No invented ontology mappings.
- One production path per feature during migration.
- Keep validation surface and session surface contracts stable while internals evolve.

## Immediate next actions

1. Mark this file as canonical cross-repo alignment reference.
2. Add the same summary to Notion Sessions page under a short "Cross-repo status" section.
   - Done on 2026-02-21.
3. Decide whether to keep `CursorBridge` as bridge-only repo or start porting `task-manager` sessions runtime into it.
