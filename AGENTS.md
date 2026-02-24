# CursorBridge Agent Memory

Last updated: 2026-02-24

## Project Snapshot

- This repo has both session routes:
  - `main-app-starter/pages/session.vue` on `/session`
  - `main-app-starter/pages/sessions.vue` on `/sessions`
- `/sessions` is now present in code, but still being matured against data coverage and stable API behavior.
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
- New master Notion project for pre-wheel planning is now live:
  - `Wheels Pre-Build Project - Sessions, DB Map, Convex Prep`
  - `https://www.notion.so/Wheels-Pre-Build-Project-Sessions-DB-Map-Convex-Prep-30fc47c61e2181ef8921c92bb32a3120`
- Reassessment before wheel visual work is tracked in `docs/WHEELS_PREBUILD_REASSESSMENT.md`.
- Canonical updated system map is now tracked in `docs/GRAND_PROJECT_SKELETON.md`.
- ISU tie-in mapping is tracked in `docs/ISU_INTEGRATION_MAP.md` using Notion source page `1b6c47c6-1e21-802e-8e3c-d167e5c1214e`.
- Full Notion->Supabase sync run executed on 2026-02-23 using safe direct + map-only mappings.
- Run report is tracked in `docs/NOTION_SUPABASE_SYNC_RUN_2026-02-23.md`.
- Reusable sync script is `scripts/sync_notion_to_supabase_full.py`.
- Missing target groups now have generated stage SQL in `sql/notion_stage_tables.sql`.
- Stage SQL identifier quoting is required (reserved names like `column` must be quoted).
- Stage tables were created and re-synced; all 27 in-scope runtime groups now sync with 0 blocked groups.
- Fresh live Supabase inventory now shows 85 tables and 1373 total rows in `docs/_supabase_inventory_live.json`.
- Notion relation trackers were re-synced from CSV and checkbox counts now match `docs/RELATIONS_MASTER.csv`.
- `docs/GRAND_PROJECT_SKELETON.md` is canonical for project hierarchy; duplicate download copies are identical.
- Validation routing policy is now explicit: validation gates promotion/commit boundaries; private draft/sandbox work can run pre-validation.
- Notion page `01_SHARED_CORE` now includes “Validation Routing Policy (Clarified 2026-02-23)” for alignment.
- External multi-app scaffold created at `C:\code\Regenerative-Hive-Mind` (outside this repo) with project/app/add-on folder structure.
- External scaffold now has starter `README.md` files across modules plus planning docs:
  - `WORKSPACE_STRUCTURE.md`
  - `MONOREPO_LAYOUT.md`
  - `SUPABASE_STAGE_TO_CANONICAL_PLAN.md`
  - `MODULE_REGISTRY.csv`
- Stage->canonical SQL migration batches now exist in:
  - `sql/stage_to_canonical/00_migrate_helper.sql`
  - `sql/stage_to_canonical/P1_safety_and_runtime.sql`
  - `sql/stage_to_canonical/P2_ontology_expansion.sql`
  - `sql/stage_to_canonical/P3_symbolic_layers.sql`
  - `sql/stage_to_canonical/99_verify_counts.sql`
- Notion tracker database created for migration checkboxes:
  - `Stage To Canonical Tracker (DB)` -> `310c47c61e2181538688e7673a20d973`
  - tracked in `config/notion_db_ids.json` as `stage_to_canonical_tracker`
- Tracker automation scripts:
  - `scripts/create_stage_canonical_tracker.py`
  - `scripts/checkoff_stage_canonical_tracker.py`
- User clarified policy: Supabase should remain stable; major structural changes are deferred to Convex migration.
- Added read-only preflight SQL stop-condition gate:
  - `sql/stage_to_canonical/01_preflight_readonly.sql`
- Policy docs:
  - `docs/SUPABASE_FREEZE_CONVEX_CHANGE_POLICY.md`
  - `docs/STAGE_TO_CANONICAL_TRACKER_WORKFLOW.md`
- Preflight outcome captured: `STOP_WRITE_BATCHES_FOR_NOW`.
- Notion tracker state updated to reflect freeze:
  - preflight task done
  - P1/P2/P3 run tasks blocked
- Convex preparation started without changing Supabase structure:
  - `docs/CONVEX_STAGE_COLLECTION_MAP.md`
  - `docs/CONVEX_PREMIGRATION_GATES.md`
  - `docs/CONVEX_SCHEMA_DRAFT_STAGE_PHASE.md`
  - `docs/CONVEX_DEPLOYMENT_NEXT_STEPS.md`
  - `docs/CONVEX_READINESS_STATUS.md`
  - `scripts/export_stage_tables_for_convex.py`
  - `scripts/prepare_convex_seed_from_stage_export.py`
  - `scripts/import_convex_seed_with_cli.py`
  - `scripts/convex_connect_and_import.ps1`
  - latest export snapshot: `exports/convex_stage_seed/20260223T184804Z`
  - latest manifest copy: `docs/_convex_stage_export_manifest_latest.json`
  - readiness audit: `docs/_convex_stage_readiness_audit.json` (local idempotency and parity pass)
- External workspace Convex setup completed for Batch 1:
  - `C:\code\Regenerative-Hive-Mind\convex\schema.ts`
  - `C:\code\Regenerative-Hive-Mind\package.json` with convex scripts
  - project created: `regenerative-hive-mind` (team `jyotilotos`)
  - dev deployment linked: `elated-ibis-363`
  - schema applied via `convex dev --once`
  - 12 mapped stage collections imported successfully
  - runtime sanity pass: all 12 collections return non-empty sample reads (`limit 1`)
- Added reusable Convex app-level readiness query:
  - `C:\code\Regenerative-Hive-Mind\convex\readiness.ts`
  - function: `api.readiness.batch1ReadinessSnapshot`
  - npm shortcut: `npm.cmd run convex:readiness:batch1`
  - latest snapshot file: `docs/_convex_batch1_readiness_snapshot_2026-02-24.json`
  - result: `allNonEmpty=true`, `totalDocuments=364`
- Added session-focused Convex lookup layer:
  - `C:\code\Regenerative-Hive-Mind\convex\sessions.ts`
  - functions:
    - `api.sessions.sessionLookupSafety`
    - `api.sessions.sessionLookupBreathwork`
    - `api.sessions.sessionLookupBuilderControls`
    - `api.sessions.sessionLookupThemes`
  - npm shortcut: `npm.cmd run convex:sessions:smoke`
  - snapshot file: `docs/_convex_session_lookup_snapshot_2026-02-24.json`

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
- `docs/RELATIONS_MASTER.csv`
- `docs/NOTION_RELATIONS_TRACKER_SPEC.md`
- `docs/GENERATION_SCOPE_TAXONOMY.md`
- `docs/GENERATION_CAPABILITY_MATRIX.csv`
- `docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md`
- `docs/CONTROLLED_PORT_PLAN_TASK_MANAGER_TO_CURSORBRIDGE.md`
- `docs/WHEELS_PREBUILD_REASSESSMENT.md`
- `docs/GRAND_PROJECT_SKELETON.md`
- `docs/GRAND_PROJECT_NOTION_ALIGNMENT.md`
- `docs/_grand_project_notion_snapshot.json`
- `docs/EXTERNAL_WORKSPACE_BOOTSTRAP.md`
- `docs/STAGE_TO_CANONICAL_TRACKER_WORKFLOW.md`
- `docs/SUPABASE_FREEZE_CONVEX_CHANGE_POLICY.md`
- `docs/CONVEX_STAGE_COLLECTION_MAP.md`
- `docs/CONVEX_PREMIGRATION_GATES.md`
- `docs/CONVEX_SCHEMA_DRAFT_STAGE_PHASE.md`
- `docs/CONVEX_DEPLOYMENT_NEXT_STEPS.md`
- `docs/CONVEX_READINESS_STATUS.md`
- `docs/CONVEX_SESSION_LOOKUPS.md`
- `docs/_convex_stage_export_manifest_latest.json`
- `docs/_convex_stage_readiness_audit.json`
- `docs/_convex_batch1_readiness_snapshot_2026-02-24.json`
- `docs/_convex_session_lookup_snapshot_2026-02-24.json`
- `docs/ISU_INTEGRATION_MAP.md`
- `docs/NOTION_SUPABASE_SYNC_RUN_2026-02-23.md`
- `docs/_notion_project_creation_result.json`
- `docs/_isu_page_snapshot.json`
- `docs/_notion_supabase_sync_full_report.json`
- `docs/_notion_supabase_table_diff.json`
- `sql/notion_stage_tables.sql`
- `README.md`
- `main-app-starter/README.md`

## User Preference Notes

- Use plain language.
- Minimize user setup steps.
- Keep instructions concrete and copy/paste ready.
- Compare new plans against files on disk before implementing.
- Do not ask repeated "if you want" questions for routine next actions.
- Always provide the next recommended steps proactively.
- Explicitly flag tangents: if work starts shifting project direction, call it out immediately with impact.
- Keep Supabase stable; major structural/model changes should be deferred to Convex migration.
