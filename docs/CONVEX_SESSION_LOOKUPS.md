# Convex Session Lookups

Last updated: 2026-02-24

Purpose:
- Provide clean, app-ready read functions for session-related data in Convex.
- Keep lookups simple while source data is still stage-shaped.

Source file:
- `C:\code\Regenerative-Hive-Mind\convex\sessions.ts`

## Public functions

1. `api.sessions.sessionLookupSafety`
- Returns:
  - `stopTriggers` (symptom + action)
  - `contraindications` (condition + restriction)

2. `api.sessions.sessionLookupBreathwork`
- Args:
  - `useCase` (optional string filter)
  - `limit` (optional number, capped)
- Returns:
  - breathwork lookup rows with `breathType`, `pattern`, `nervousSystem`, `physiologyEffect`, `safetyNotes`

3. `api.sessions.sessionLookupBuilderControls`
- Returns:
  - `controls` from `controlsLibraryDesign`
  - `sliders` from `dailyRegulationSliders`

4. `api.sessions.sessionLookupThemes`
- Args:
  - `domain` (required):
    - `mythologicalBeings`
    - `sacredAnimals`
    - `stonesMinerals`
    - `astrologyCalendricalSystems`
  - `search` (optional)
  - `limit` (optional number, capped)
- Returns:
  - normalized theme options: `label`, `category`, `primaryElement`, `psychologicalTheme`, `intensity`, `notes`

## Run commands

From `C:\code\Regenerative-Hive-Mind`:

```powershell
npx convex run api.sessions.sessionLookupSafety
npx convex run api.sessions.sessionLookupBreathwork "{useCase:'NSDR',limit:5}"
npx convex run api.sessions.sessionLookupBuilderControls
npx convex run api.sessions.sessionLookupThemes "{domain:'mythologicalBeings',limit:5}"
```

Smoke command:

```powershell
npm.cmd run convex:sessions:smoke
```

## Validation snapshot

- Latest snapshot:
  - `docs/_convex_session_lookup_snapshot_2026-02-24.json`
- Coverage:
  - safety lookup
  - breathwork lookup
  - builder controls lookup
  - theme lookups across all 4 domains
