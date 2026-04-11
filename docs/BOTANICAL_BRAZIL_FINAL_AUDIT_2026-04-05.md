# Botanical Brazil Final Audit

Last updated: 2026-04-05

Scope:
- final audit only
- documentation alignment only
- no schema redesign
- no rebuild
- no dataset expansion

SECTION A — LOCKED

- Shared botanical schema is frozen and remains the active canonical structure in [sql/botanicals/00_core_schema.sql](/C:/Code/CursorBridge/sql/botanicals/00_core_schema.sql).
- Brazil remains a branch inside the shared multi-region system, not a separate schema.
- Core row logic is stable:
  - `1 row = 1 actual botanical entry / species / cultivar / named line`
  - `1 row = 1 botanical entry x branch x zone x production mode`
- Required normalized table stack and generated `"Botanical_Operational_View"` are already defined and live in the repo SQL package.
- Current Brazil branch population is materially present in the live repo export bundle:
  - Brazil identity rows are present in `exports/botanicals_master_union/latest/botanical_entries_master_union_additive.csv`
  - Brazil operational rows are present in `exports/botanicals_master_union/latest/botanical_zone_profiles_brazil_additive.csv`
- Atlantic Forest is confirmed as materially represented inside the current Brazil branch audit state.
- The Atlantic Forest reference wording below is now the locked repo audit wording for the current branch state.

SECTION B — PARTIAL

- Identity-layer biome tagging is not yet complete enough to claim final exact biome totals across the Brazil branch.
- Atlantic Forest identity totals are still under-tagged at the identity layer, so only explicit counts and confirmed minimum counts should be presented as final.
- Current Atlantic Forest layer coverage is not yet a full canonical `species_design_matrix` layer audit.
- The current Atlantic Forest layer summary is still a confirmed growth-habit proxy derived from the operational export.
- Brazil branch documentation is not yet fully aligned across all older botanical docs; some older source-of-truth wording still reflects the pre-lock sequence.
- Final row-by-row biome/count presentation is therefore stable enough for audit reference, but not yet a fully normalized biome-tag completeness state.

SECTION C — DELTA ONLY REMAINING

- Backfill explicit biome tagging for existing Brazil identity rows where the current source stack already supports it.
- Backfill canonical layer values for existing Atlantic-associated rows in the design-matrix layer where source-backed.
- Refresh the Atlantic Forest audit counts after those existing-row tag backfills are applied.
- Align older repo botanical docs that still describe Brazil as the next branch build rather than the current canonical branch baseline.
- Keep all remaining work append-only or correction-only; do not redesign schema, do not rebuild branch structure, and do not expand the dataset during this pass.

## ATLANTIC FOREST COUNT REFERENCE — CURRENT BRAZIL BRANCH AUDIT

* exact explicitly Atlantic-tagged identity rows: 1
* counted confirmed Atlantic-associated identities via operational rows: 20
* exact explicitly Atlantic-tagged operational rows: 34

Important caveat:

* identity-layer biome tagging is not yet complete enough to claim a final exact Atlantic Forest canonical identity total
* current layer summary is a confirmed growth-habit proxy, not yet a full canonical design-matrix layer audit

Working target:

* Atlantic Forest canonical identity target inside Brazil branch: 120
* Atlantic Forest operational row target inside Brazil branch: 250–300

Interpretation:
Atlantic Forest is present and materially represented in the Brazil branch, but exact canonical identity totals remain under-tagged and should not yet be presented as final.
