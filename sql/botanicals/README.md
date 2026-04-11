# Botanical SQL Package

This package adds the first Supabase-first database layer for the botanical,
product, protocol, Recovering Habitats, and HONS-aware build.

## Current Builder Package Status

The March 30 package is no longer the final builder instruction set by itself.
Use these V2 docs alongside this SQL:

- `docs/BOTANICAL_SYSTEM_SOURCE_OF_TRUTH_V2.md`
- `docs/BOTANICAL_DATABASE_BUILDER_HANDOVER_V2.md`
- `docs/BOTANICAL_APP_BUILDER_HANDOVER_V2.md`
- `docs/BOTANICAL_BRAZIL_THREAD_HANDOVER_V2.md`
- `docs/BOTANICAL_HNOS_ARCHITECTURE_ALIGNMENT_V2.md`
- `docs/BOTANICAL_HONS_PITCH_CONTEXT_V2.md`
- `docs/BOTANICAL_SEND_MATRIX_V2.md`

These V2 docs lock in:

- UK sweep completion for this phase
- mandatory sweep/capture fields
- mandatory size/tree fields
- mandatory reproductive/pollination fields
- mandatory lifecycle fields
- mandatory confidence/completeness fields
- mandatory root-detail fields
- mandatory universal layering fields
- mandatory symbiosis separation from companion logic
- mandatory role/propagation/invasiveness/climate fields
- mandatory spacing/establishment/training fields
- mandatory fast season anchor fields
- regional harvest and yield fields
- mandatory two-way product navigation:
  - `product -> matching varieties / entries`
  - `botanical entry / tree / variety -> valid product paths`
- Brazil next-thread execution rules

Current rules captured here:

- Supabase is the canonical build and test layer for now.
- Convex should mirror these IDs and semantics later.
- Notion is the human-facing operations layer, not canonical truth.
- Branch means operational node, not country.
- Brazil is the first ingest source, not the long-term schema template.

## Current Remote Build Status

- Notion V2 botanical databases are created and tracked in:
  - `config/notion_db_ids.json`
- Local Supabase CLI workspace is initialized in:
  - `supabase/`
- Local migration files are staged in:
  - `supabase/migrations/20260331172356_botanicals_v2_core_schema.sql`
  - `supabase/migrations/20260331172357_botanicals_v2_seed_launch_and_kombucha.sql`
- Remote Supabase project is now linked:
  - `dshwdxhycdrtemaxrupu`
- Botanical migrations pushed successfully on `2026-03-31`:
  - `20260331172356_botanicals_v2_core_schema.sql`
  - `20260331172357_botanicals_v2_seed_launch_and_kombucha.sql`
- April patch migration pushed successfully on `2026-04-01`:
  - `20260401110000_botanicals_v2_branch_patch.sql`
- Local `supabase` CLI is installed at:
  - `tools/supabase/supabase.exe`

Current build state:

- Notion V2 botanical databases: live
- Supabase botanical schema: live
- Supabase botanical seed launch migration: live
- April branch patch migration: live

## April 1 Surgical Patch

This patch does not redesign the schema. It extends the live normalized system
with the final source-of-truth deltas only.

Patch migration:

- `supabase/migrations/20260401110000_botanicals_v2_branch_patch.sql`

Backfill pack generated from the larger Brazil identity workbook:

- `exports/botanicals_patch/latest/botanical_entries_master_patch_backfill.csv`
- `exports/botanicals_patch/latest/botanical_zone_profiles_patch_backfill.csv`
- `exports/botanicals_patch/latest/branch_resources_seed.csv`
- `exports/botanicals_patch/latest/canonical_vs_alias_mapping.csv`
- `exports/botanicals_patch/latest/manifest.json`

This patch adds:

- `branch_resources`
- canonical identity enrichments such as:
  - `common_name_en`
  - min/max size ranges
  - Brazil endemic / conservation / invasive flags
  - source URLs
  - numeric confidence fields
- zone/growing-fit enrichments such as:
  - tolerance fields
  - Brazil harvest-window shorthand
  - local/export/nursery/education/current-site flags
- HONS overlay status fields such as:
  - `stage_status`
  - `provenance_status`
  - `rights_status`
  - `branch_eligibility`
  - `synergy_status`
  - `node_relevance`
  - `experimental_policy`
  - `release_policy`
  - `public_publish_status`

The generated backfill pack currently matches `262` Brazil working-master rows
to the larger Brazil identity workbook and prepares `2` branch resource seed
rows without reopening the architecture.

## Live Verification Status

Verified on `2026-03-31`:

- linked remote project ref:
  - `dshwdxhycdrtemaxrupu`
- remote migration history confirms both botanical migrations are applied:
  - `20260331172356_botanicals_v2_core_schema.sql`
  - `20260331172357_botanicals_v2_seed_launch_and_kombucha.sql`

Important note:

- direct remote schema dump/table-name introspection through the CLI still needs
  `SUPABASE_DB_PASSWORD`
- without that password, the strongest live verification available from this
  environment is:
  - successful `supabase db push`
  - matching remote migration history

This package remains aligned to
`database_builder_actual_tables_only.xlsx`, but it now carries the additional
V2 builder fields required after the later locked decisions.

## Brazil + UK Master Union

The next additive load bundle is generated from the real source stacks:

- Brazil primary workbook:
  `c:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\brazil_data_tables_only.xlsx`
- UK secondary export:
  `c:\Users\Lenovo\Desktop\OneDrive\Work folder\Modular gardens\Botanical list_Kombucha_Friendly.zip`

The repeatable builder script is:

- `scripts/build_botanicals_master_union.py`

It writes import-ready additive CSVs to:

- `exports/botanicals_master_union/latest`

This is an additive union patch, not an architecture rewrite:

- Brazil remains the primary master source
- UK botanicals are unioned into `botanical_entries_master`
- overlap is flagged in `botanical_overlap_mapping.csv`
- existing Jun protocol and catalogue rows remain valid and separate

## Actual-Data Addendum

The core architecture still stands:

- one branchable multi-country system
- layered source-of-truth tables
- separate protocol library
- separate product catalogue layer
- one generated flat operational view

What changed after reviewing the actual export is narrower:

- `product_catalogue` must remain a first-class truth layer
- `product_protocol_links` and `product_botanical_links` are persistent data layers, not temporary helpers
- Jun-led ferment data is now proven in the export
- Kombucha should stay differentiable from Jun, not be duplicated by assumption

This package already reflects that narrower patch by using:

- `product_catalogue`
- `protocol_library`
- `product_protocol_links`
- `product_botanical_links`
- `ferment_family`

The current schema still keeps the same architecture. The V2 update extends the
existing tables rather than replacing them.

Follow-up ferment detail can still be added later if needed through fields such
as:

- `ferment_variant`
- `sweetener_base`
- `tea_base`
- `culture_type`
- `concentration_method`

The current workbook-aligned import package to load first is:

- `manifest.csv`
- `raw_botanical_list.csv`
- `raw_growing_harvesting.csv`
- `raw_product_catalogue.csv`
- `raw_brew_ferment_protocols.csv`
- `branch_nodes_seed.csv`
- `ferment_family_seed.csv`
- `botanical_entries_master_seed.csv`
- `botanical_zone_profiles_seed.csv`
- `protocol_library_seed.csv`
- `product_catalogue_seed.csv`
- `product_protocol_links_seed.csv`
- `product_botanical_links_seed.csv`
- `current_product_line_summary.csv`
- `current_product_ingredient_roster.csv`
- `protocol_gap_report.csv`
- `botanical_gap_report.csv`

## Files

- `00_core_schema.sql`
  - Creates the workbook-aligned raw tables
  - Creates the actual modeled tables including:
    - `branch_nodes`
    - `branch_resources`
    - `ferment_family`
    - `botanical_entries_master`
    - `botanical_zone_profiles`
    - `botanical_product_paths`
    - `protocol_library`
    - `product_catalogue`
    - `product_protocol_links`
    - `product_botanical_links`
    - species overlay tables
    - HONS-aware overlay tables
  - Carries the V2 sweep fields, size/tree fields, and regional yield/harvest fields
  - Creates workbook-aligned views including `"Botanical_Operational_View"`
- `01_seed_launch_and_kombucha.sql`
  - Seeds the three launch branches
  - Seeds ferment-family differentiators
  - Seeds the current catalogue structure as `product_catalogue`
  - Seeds protocol rows recoverable from the export
  - Seeds only the few botanical rows already explicitly resolved in the workbook
  - Preserves unresolved ingredient/protocol joins as unresolved rows instead of inventing data

## Recommended application order

```sql
\i sql/botanicals/00_core_schema.sql
\i sql/botanicals/01_seed_launch_and_kombucha.sql
```

## Why the catalogue is included now

The existing product catalogue is already part of the project reality. It
should not sit outside the shared schema, and it should not be flattened into
generic product rows too early.

This package keeps the catalogue explicit through:

- `product_catalogue`
- `protocol_library`
- `product_protocol_links`
- `product_botanical_links`
- `current_product_line_summary`
- `protocol_gap_report`
- `botanical_gap_report`

That preserves the current Jun/SCOBY catalogue truth while keeping Kombucha as
a differentiated ferment family rather than collapsing everything together.
