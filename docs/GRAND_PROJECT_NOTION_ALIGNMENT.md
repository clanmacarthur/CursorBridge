# Grand Project Skeleton vs Notion Plan Alignment

Last updated: 2026-02-23

## What was compared

- `c:\Users\j-lot\Downloads\GRAND_PROJECT_SKELETON.md`
- `c:\Users\j-lot\Downloads\GRAND_PROJECT_SKELETON_v2.md`
- `docs/GRAND_PROJECT_SKELETON.md`
- Live Notion project structure snapshot: `docs/_grand_project_notion_snapshot.json`

## Result

- All three skeleton markdown files are identical (same SHA256 hash).
- Canonical file selected: `docs/GRAND_PROJECT_SKELETON.md`.
- Notion project layout is aligned with this skeleton at the top level:
  - `00_READ_ME`
  - `01_SHARED_CORE`
  - `02_DASHBOARD_BUILDER`
  - `03_WELLNESS_APP`
  - `04_DIGITAL_EXPANSION_DIVISION`
  - `05_SUSTAINABLE_INSTITUTE`
  - `06_MONETIZATION_MENU`
  - `07_PITCH_DECK_LAYER`
  - `08_BACKLOG_AND_FUTURE`
  - `99_ARCHIVE`

## Mismatch found and fixed

Issue found:
- The skeleton wording implied all outputs must always pass Validation Workbench.
- That was too strict for private draft/sandbox work.

Fix applied in `docs/GRAND_PROJECT_SKELETON.md`:
- Added explicit validation routing policy:
  - validation is mandatory for shared/live truth, on-chain writes, and committed onboarding transitions.
  - private sandbox and draft iteration can run pre-validation.
  - promotion from draft to shared/live triggers validation gate.
- Updated cross-project rule #3 to match this policy.

## Legitimacy check (current state)

This now matches the intended model:
- Validation Workbench is a shared trust layer.
- It is a promotion/commit boundary gate, not a blanket blocker for all local experimentation.
- Onboarding is connected to Agreements Engine and only enters committed state after validation gates.

## Next structure decision

A real folder scaffold was created outside this repo at:
- `c:\code\Regenerative-Hive-Mind`

This is now the code-side home for all future app/add-on modules.
