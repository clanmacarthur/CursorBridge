# External Workspace Bootstrap

Last updated: 2026-02-23

External root:
- `C:\code\Regenerative-Hive-Mind`

What was created:
- Full top-level project tree (`00_READ_ME` to `11_SHARED_MODULE_ECONOMY`, plus `_governance`, `docs`, `99_ARCHIVE`).
- Starter `README.md` in each folder to reduce setup friction.
- Planning docs in external `docs`:
  - `GRAND_PROJECT_SKELETON.md`
  - `GRAND_PROJECT_NOTION_ALIGNMENT.md`
  - `WORKSPACE_STRUCTURE.md`
  - `MONOREPO_LAYOUT.md`
  - `SUPABASE_STAGE_TO_CANONICAL_PLAN.md`
  - `MODULE_REGISTRY.csv`
  - `STAGE_TO_CANONICAL_TRACKER_WORKFLOW.md`
  - `SUPABASE_FREEZE_CONVEX_CHANGE_POLICY.md`
  - `CONVEX_STAGE_COLLECTION_MAP.md`
  - `CONVEX_PREMIGRATION_GATES.md`
  - `CONVEX_SCHEMA_DRAFT_STAGE_PHASE.md`
  - `CONVEX_DEPLOYMENT_NEXT_STEPS.md`
  - `CONVEX_READINESS_STATUS.md`
  - `_convex_stage_export_manifest_latest.json`
  - `_convex_stage_readiness_audit.json`

Notion alignment:
- Canonical structure check is in `docs/GRAND_PROJECT_NOTION_ALIGNMENT.md`.
- Validation routing clarification was also added to Notion `01_SHARED_CORE` page.

How to use this next:
1. Put each new app/add-on inside the matching external module folder.
2. Keep cross-project policy edits in `_governance`.
3. Use `SUPABASE_STAGE_TO_CANONICAL_PLAN.md` to move stage tables safely, one table at a time.
4. Use `STAGE_TO_CANONICAL_TRACKER_WORKFLOW.md` and the Notion tracker DB to check off migration progress.
