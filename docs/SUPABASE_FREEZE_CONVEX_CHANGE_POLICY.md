# Supabase Freeze And Convex Change Policy

Last updated: 2026-02-23

Decision:
- Keep Supabase stable.
- Allow major model/schema changes in the Convex migration phase.

What this means now:
- Supabase:
  - read-only checks are allowed
  - bug fixes and small safe corrections are allowed
  - major structural changes are deferred
- Convex:
  - can carry major redesigns
  - becomes the main place for broader schema evolution

Stop condition:
- If a step would create/reshape many canonical tables in Supabase, stop and defer to Convex plan.
- Use `sql/stage_to_canonical/01_preflight_readonly.sql` before any write batch.

Current recommended action:
1. Run read-only preflight.
2. Record result in Notion tracker.
3. Wait for migration-window approval before running `P1/P2/P3`.

Readiness snapshot (2026-02-23):
- Stage tables present: 12
- Canonical counterparts present: 0/12
- Decision: `STOP_WRITE_BATCHES_FOR_NOW`

Meaning:
- We are not ready for Supabase structural migration batches.
- We are ready to continue Convex migration planning/design.
