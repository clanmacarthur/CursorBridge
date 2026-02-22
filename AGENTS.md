# CursorBridge Agent Memory

Last updated: 2026-02-21

## Project Snapshot

- This repo currently runs a simple session page at `main-app-starter/pages/session.vue` on route `/session`.
- The richer wheel-based session builder (`/sessions`) is a planned target, not implemented yet.
- Canon source files are in `canon/`.
- Main planning docs are in `docs/`.

## What Worked Well

- Keeping "current state" and "target state" in separate sections prevents confusion.
- Using one catalog for table-to-domain mapping helps avoid guessed links.
- Keeping role boundaries in writing reduces accidental broad edits.

## What Failed Or Caused Drift

- Old docs referenced paths that are not in this repo (for example `app/pages/...`).
- Some readme content referenced `/sessions` while code currently exposes `/session`.
- Some setup text in `main-app-starter/README.md` pointed to the wrong repo path.

## Current Decisions

- Supabase coverage comes first.
- Convex migration starts only after Supabase table mapping is complete.
- Lock `controls_library` + `user_profiles` schemas before broad content expansion.
- Persona is profile-owned at generation time (not embedded in content rows).
- Do not treat draft wheel architecture as live until code exists.
- Keep route naming explicit in docs:
  - current: `/session`
  - planned: `/sessions`
- Cross-repo alignment reference is `docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md`.
- `task-manager` is the runtime truth for active `/sessions` behavior; `CursorBridge` is bridge/data-ingestion truth.
- Controlled port tracker is `docs/CONTROLLED_PORT_PLAN_TASK_MANAGER_TO_CURSORBRIDGE.md`.
- Port phase started: `GET /api/session/themes` is now wired in `main-app-starter`; preview/generate remain stubs with aligned contract keys.
- Live Supabase inventory audit is tracked in `docs/SUPABASE_SESSIONS_AUDIT.md` (sessions-first classification + duplicate risk flags).
- Notion database IDs are now tracked in `config/notion_db_ids.json` for the therapeutic pages.
- Use stage tables for new Notion datasets that do not yet map cleanly to canonical Supabase tables.
- Sessions master is now in `docs/SESSIONS_MASTER.md` and mirrored into Notion page `2dcc47c6-1e21-80ed-b68b-d49d46c2f28a`.

## Files To Keep Updated

- `docs/HANDOVER_SESSIONS.md`
- `docs/HANDOVER_CURSORBRIDGE.md`
- `docs/DATA_MODEL_OVERVIEW.md`
- `docs/THEME_TABLE_CATALOG.md`
- `docs/CONVEX_MIGRATION_PLAN.md`
- `docs/NOTION_DB_INVENTORY.md`
- `docs/NOTION_SUPABASE_CONVEX_PLAN.md`
- `docs/SUPABASE_SESSIONS_AUDIT.md`
- `docs/SESSIONS_KEEP_MERGE_DEPRECATE_MATRIX.md`
- `docs/FULL_SYSTEM_KEEP_MERGE_DEPRECATE_MATRIX.md`
- `docs/RELATIONS_REGISTRY.md`
- `docs/RELATIONS_EXISTING.csv`
- `docs/RELATIONS_TO_BE.csv`
- `docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md`
- `docs/CONTROLLED_PORT_PLAN_TASK_MANAGER_TO_CURSORBRIDGE.md`
- `README.md`
- `main-app-starter/README.md`

## User Preference Notes

- Use plain language.
- Minimize user setup steps.
- Keep instructions concrete and copy/paste ready.
- Compare new plans against files on disk before implementing.
