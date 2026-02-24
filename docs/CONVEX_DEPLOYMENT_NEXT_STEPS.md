# Convex Deployment Next Steps

Last updated: 2026-02-24

Current state:
- Convex project created: `regenerative-hive-mind`
- Team: `jyotilotos`
- Dev deployment: `elated-ibis-363`
- Schema applied from `C:\code\Regenerative-Hive-Mind\convex\schema.ts`
- Batch 1 seed import completed for all 12 collections.

## What was run

```powershell
cd C:\code\Regenerative-Hive-Mind
npx convex dev --once --configure new --team jyotilotos --project regenerative-hive-mind --dev-deployment cloud

cd C:\code\CursorBridge
python scripts/import_convex_seed_with_cli.py --workspace C:\code\Regenerative-Hive-Mind --execute
```

## Imported collections

- `sessionStopTriggers`
- `contraindications`
- `breathworkTaxonomy`
- `dailyRegulationSliders`
- `controlsLibraryDesign`
- `nadiSystem`
- `astrologyCalendricalSystems`
- `emotionBrainBodyEnergyMapping`
- `fullBrainNeuralSystems`
- `mythologicalBeings`
- `sacredAnimals`
- `stonesMinerals`

## Immediate next checks

1. Table visibility + sample-read check (completed):

```powershell
cd C:\code\Regenerative-Hive-Mind
npx convex data
```

2. App-level readiness query check (completed):

```powershell
cd C:\code\Regenerative-Hive-Mind
npx convex run api.readiness.batch1ReadinessSnapshot
# or:
npm.cmd run convex:readiness:batch1
```

3. Add session-specific read checks (template + theme lookup paths).
4. Record any mapping gaps before Batch 2.

Session lookup layer (completed):

```powershell
cd C:\code\Regenerative-Hive-Mind
npx convex run api.sessions.sessionLookupSafety
npx convex run api.sessions.sessionLookupBreathwork "{useCase:'NSDR',limit:5}"
npx convex run api.sessions.sessionLookupBuilderControls
npx convex run api.sessions.sessionLookupThemes "{domain:'mythologicalBeings',limit:5}"
```

Snapshot:
- `docs/_convex_session_lookup_snapshot_2026-02-24.json`

## Guardrails

- Keep Supabase in freeze mode for major structural changes.
- Continue major model changes in Convex.
- Avoid rerunning import blindly with `--append` unless duplicate handling is planned.
