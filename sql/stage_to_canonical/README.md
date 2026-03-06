# Stage To Canonical Migration Batches

Purpose:
- Move data from `_stage` tables into canonical (non-`_stage`) tables in safe batches.
- Keep reruns safe and idempotent using `notion_page_id` matching.

Current operating mode:
- **Supabase freeze mode** is active.
- Run **read-only checks only** unless an explicit migration window is approved.
- Major structural/model changes are deferred to the Convex migration phase.

Run now (recommended):
1. Open Supabase Dashboard -> SQL Editor.
2. Open file `sql/stage_to_canonical/01_preflight_readonly.sql`.
3. Copy/paste full file into SQL Editor.
4. Click Run.
5. Read `global_decision`:
   - `STOP_WRITE_BATCHES_FOR_NOW` = keep freeze, no P1/P2/P3 writes.
   - `PRECHECK_OK_FOR_WRITE_BATCHES` = write batches may proceed in approved window.

Run order:
1. `sql/stage_to_canonical/00_migrate_helper.sql`
2. `sql/stage_to_canonical/01_preflight_readonly.sql`
3. `sql/stage_to_canonical/P1_safety_and_runtime.sql`
4. `sql/stage_to_canonical/P2_ontology_expansion.sql`
5. `sql/stage_to_canonical/P3_symbolic_layers.sql`
6. `sql/stage_to_canonical/99_verify_counts.sql`

Notes:
- These scripts create canonical tables automatically from stage structure when missing.
- Existing canonical rows are updated by `notion_page_id`.
- New rows are inserted when no match exists.
- Rows with `notion_page_id IS NULL` are skipped on purpose to avoid duplicate drift.
- In freeze mode, do not run `P1/P2/P3` write batches until migration window approval.
