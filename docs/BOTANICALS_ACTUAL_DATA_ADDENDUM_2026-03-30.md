# Botanicals Actual-Data Addendum

Date: 2026-03-30

The core build direction remains correct:

- one branchable multi-country system
- layered source-of-truth tables
- a separate `Protocol_Library`
- a separate product catalogue layer
- one generated flat operational view

This is not a reset or rewrite situation.

## What needs patching

The builder docs now need an actual-data addendum because the exported data has
been reviewed and turned into loadable tables.

The practical corrections are:

- load the real exported tables first
- preserve the product catalogue as a first-class truth layer
- keep product-to-protocol links as a real data layer
- keep product-to-botanical links as a real data layer
- keep unresolved gaps flagged instead of guessed

## Schema implication

This is an alignment patch, not a change in philosophy.

If the builder already has a table that fully behaves like a real catalogue
table, they should document the mapping.

If not, the minimum correction is to keep or elevate:

- `product_catalogue`
- `product_protocol_links`
- `product_botanical_links`

## Ferment modelling patch

The old visible `Kombucha_1F_Friendly` operational flag can still remain in the
flat view, but it is not enough once actual product and protocol data exists.

The addendum should require explicit differentiators such as:

- `ferment_family`
- `ferment_variant`
- `sweetener_base`
- `tea_base`
- `target_temp_c_min`
- `target_temp_c_max`
- `culture_type`
- `live_culture_state`
- `concentration_method`

## Current project status

The current repo package at [sql/botanicals/00_core_schema.sql](c:/Code/CursorBridge/sql/botanicals/00_core_schema.sql)
and [sql/botanicals/01_seed_launch_and_kombucha.sql](c:/Code/CursorBridge/sql/botanicals/01_seed_launch_and_kombucha.sql)
already reflects the narrower patch by using:

- `product_catalogue`
- `protocol_library`
- `product_protocol_links`
- `product_botanical_links`
- `ferment_family`

## Practical payload

The next builder-facing payload should be:

- the actual-data addendum
- the actual tables ZIP
- the workbook-aligned table list

The practical table/file set is:

- `manifest`
- `raw_botanical_list`
- `raw_growing_harvesting`
- `raw_product_catalogue`
- `raw_brew_ferment_protocols`
- `branch_nodes_seed`
- `ferment_family_seed`
- `botanical_entries_master_seed`
- `botanical_zone_profiles_seed`
- `protocol_library_seed`
- `product_catalogue_seed`
- `product_protocol_links_seed`
- `product_botanical_links_seed`
- `current_product_line_summary`
- `current_product_ingredient_roster`
- `protocol_gap_report`
- `botanical_gap_report`
