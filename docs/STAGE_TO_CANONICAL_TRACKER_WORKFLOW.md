# Stage To Canonical Tracker Workflow

Last updated: 2026-02-23

Tracker database:
- `Stage To Canonical Tracker (DB)`
- https://www.notion.so/310c47c61e2181538688e7673a20d973

Policy:
- Supabase is in freeze mode for major changes.
- Major structural changes are deferred to Convex migration.
- Until migration window is approved, run read-only checks only.

Scripts:
- `scripts/create_stage_canonical_tracker.py`
- `scripts/checkoff_stage_canonical_tracker.py`

## Setup

Create or refresh tracker rows:

```powershell
python scripts/create_stage_canonical_tracker.py
```

## Check off tasks

Mark one task done:

```powershell
python scripts/checkoff_stage_canonical_tracker.py --task "Run P1 migration batch"
```

Mark an entire phase done:

```powershell
python scripts/checkoff_stage_canonical_tracker.py --phase P1
```

Mark a phase as in progress:

```powershell
python scripts/checkoff_stage_canonical_tracker.py --phase P2 --only-status Pending --in-progress
```

Add a note while checking off:

```powershell
python scripts/checkoff_stage_canonical_tracker.py --task "Run final verification query" --note "Counts confirmed in Supabase SQL editor"
```

## SQL run order

1. `sql/stage_to_canonical/00_migrate_helper.sql`
2. `sql/stage_to_canonical/01_preflight_readonly.sql`
3. `sql/stage_to_canonical/P1_safety_and_runtime.sql`
4. `sql/stage_to_canonical/P2_ontology_expansion.sql`
5. `sql/stage_to_canonical/P3_symbolic_layers.sql`
6. `sql/stage_to_canonical/99_verify_counts.sql`

Freeze-mode recommended now:
1. Run only `01_preflight_readonly.sql`.
2. Do not run `P1/P2/P3` write batches yet.
3. Update tracker notes with preflight outcome.

Current recorded outcome (2026-02-23):
- Preflight result: `STOP_WRITE_BATCHES_FOR_NOW`
- Tracker state:
  - `Run read-only preflight and capture stop decision` -> Done
  - `Run P1 migration batch` -> Blocked
  - `Run P2 migration batch` -> Blocked
  - `Run P3 migration batch` -> Blocked
