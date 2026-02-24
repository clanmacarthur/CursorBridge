# Convex Readiness Status

Last updated: 2026-02-24

Current state: **Batch 1 Convex migration is complete on dev deployment.**

Completed:
- Stage data exported from Supabase (`20260223T184804Z`).
- Stage -> Convex collection mapping defined.
- Convex schema file created (`C:\code\Regenerative-Hive-Mind\convex\schema.ts`).
- Local seed transform completed.
- Local idempotency dry-run passed.
- Local parity counts passed.
- Convex project created: `regenerative-hive-mind` (team: `jyotilotos`).
- Dev deployment provisioned: `elated-ibis-363`.
- Schema pushed successfully (`npx convex dev --once`).
- Import executed successfully for all 12 mapped collections.
- Basic runtime sanity check passed (`npx convex data` shows all 12 collections).
- Per-table read sanity check passed (`--limit 1 --format jsonArray` returned non-empty for all 12 collections).
- App-level Convex query check passed:
  - function: `api.readiness.batch1ReadinessSnapshot`
  - result: `allNonEmpty = true`, `totalDocuments = 364`
  - snapshot file: `docs/_convex_batch1_readiness_snapshot_2026-02-24.json`
- Session lookup query layer added and validated:
  - source: `C:\code\Regenerative-Hive-Mind\convex\sessions.ts`
  - functions: safety, breathwork, builder controls, themes
  - snapshot file: `docs/_convex_session_lookup_snapshot_2026-02-24.json`

Current blockers:
- None for Batch 1 data migration.

Important guardrail:
- Supabase stays in freeze mode for major structural changes.
- Continue major model evolution in Convex first, then plan controlled cutover.

Next focus:
1. Keep using `api.readiness.batch1ReadinessSnapshot` as the baseline health check.
2. Wire app routes to these Convex lookups and confirm end-to-end reads.
3. Prepare Batch 2 mappings (if more stage tables are added).
