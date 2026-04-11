# Botanicals Master Union And Relation Mapping

Date: 2026-03-30

## Status Note

This document remains useful as a legacy union-import and load-order note.

It is not the live standalone source of truth for the current botanical build.

Current authoritative rule files are:

- `sql/botanicals/00_core_schema.sql`
- `docs/BOTANICAL_SYSTEM_SOURCE_OF_TRUTH_V2.md`
- `docs/BOTANICAL_DATABASE_BUILDER_HANDOVER_V2.md`
- `docs/BOTANICAL_BRAZIL_THREAD_HANDOVER_V2.md`
- `docs/BOTANICAL_BRAZIL_ATLANTIC_FOREST_STAGE1_DATABASE_BUILDER_HANDOVER_2026-04-08.md`
- `docs/BOTANICAL_CANONICAL_VS_ALIAS_MAPPING_V2.md`

Use this document for:

- source priority between the Brazil workbook and UK additive source
- repeatable import-bundle generation
- legacy load-order notes for the union bundle
- explicit relation-registry support files

Do not use this document by itself to redefine:

- the frozen normalized table stack
- the current Atlantic Forest Stage 1 execution rules
- canonical layer policy
- propagation wording
- current curation caps or named-line handling

This is the narrow merge patch required after confirming that the Brazil workbook
is the real primary source and the UK kombucha-friendly export is a secondary
botanical source, not the master replacement.

## Source Priority

- Primary source stack: `brazil_data_tables_only.xlsx`
- Secondary source stack: `Botanical list_Kombucha_Friendly.zip`
- Existing Jun protocol and product line remains valid and should stay loaded as
  the separate protocol/catalogue layer already defined in `sql/botanicals/`.

## Core Rule

The architecture does not change:

- one branchable multi-country system
- normalized botanical tables remain the source of truth
- separate `protocol_library`
- separate `botanical_product_paths`
- separate `product_catalogue`
- separate `product_botanical_links`
- separate branch-aware `botanical_zone_profiles`
- one generated flat operational view

What changes is the load order and the explicit relation registry.

This document describes the union-import slice of that architecture, not the
entire current execution contract.

## Actual Source To Target Mapping

- `Botanicals_Master` -> `botanical_entries_master`
  - Key: `Botanical_ID -> botanical_entry_id`
  - Status: primary load
- `Brazil_Working_Master` -> `botanical_zone_profiles`
  - Key: `Working Master Record ID -> zone_profile_id`
  - Join back to botanical master on `Botanical_ID -> botanical_entry_id`
  - Status: many regional rows per botanical
- `Products` -> `product_catalogue`
  - Key: `Product_ID -> product_id`
  - Join to botanical master on `Primary Botanical ID -> botanical_entry_id`
- `Product_Botanical_Links` -> `product_botanical_links`
  - Key: bridge table
  - Join to products on `Product_ID`
  - Join to botanical master on `Botanical_ID`
- `botanical_product_paths`
  - Status: part of the current frozen schema
  - Note: not fully described by this March 30 union note; follow the current
    schema and builder docs for live product-path handling
- `Botanical list (kombucha friendly)` -> `botanical_entries_master`
  - Key: generated `BOT-UK-*` ids
  - Status: secondary union load
  - Overlap with Brazil is flagged, not collapsed

## Generated Import Bundle

The repeatable merger script is:

- [build_botanicals_master_union.py](/c:/Code/CursorBridge/scripts/build_botanicals_master_union.py)

The generated bundle is written to:

- [latest](/c:/Code/CursorBridge/exports/botanicals_master_union/latest)

Files produced there:

- `raw_botanical_list_uk_additive.csv`
- `botanical_entries_master_union_additive.csv`
- `botanical_zone_profiles_brazil_additive.csv`
- `product_catalogue_brazil_additive.csv`
- `product_botanical_links_brazil_additive.csv`
- `botanical_overlap_mapping.csv`
- `duplicate_name_registry.csv`
- `relation_mapping_registry.csv`
- `manifest.json`

## Relation Status

SQL relations are now explicitly supported by the load bundle:

- `product_catalogue.product_id -> product_botanical_links.product_id`
- `botanical_entries_master.botanical_entry_id -> botanical_zone_profiles.botanical_entry_id`
- `botanical_entries_master.botanical_entry_id -> product_botanical_links.botanical_entry_id`

These relations remain useful, but they are not the full current normalized
relation picture. The frozen schema now also includes:

- `botanical_entries_master -> botanical_product_paths`
- `botanical_entries_master -> species_* overlay tables`
- `botanical_entries_master -> hons_overlay`

Notion native relation properties are still not created yet. The relation map is
now explicit enough to add them cleanly instead of guessing.

## Load Order

Load into the existing schema in this order:

1. `sql/botanicals/00_core_schema.sql`
2. `sql/botanicals/01_seed_launch_and_kombucha.sql`
3. `exports/botanicals_master_union/latest/botanical_entries_master_union_additive.csv`
4. `exports/botanicals_master_union/latest/botanical_zone_profiles_brazil_additive.csv`
5. `exports/botanicals_master_union/latest/product_catalogue_brazil_additive.csv`
6. `exports/botanicals_master_union/latest/product_botanical_links_brazil_additive.csv`

This remains the bundle load order for the union import set.

Current Atlantic Forest Stage 1 build work is broader than this bundle and must
still follow the newer builder and branch handover docs listed above.

Reference-only support files in the same bundle:

- `raw_botanical_list_uk_additive.csv`
- `botanical_overlap_mapping.csv`
- `duplicate_name_registry.csv`
- `relation_mapping_registry.csv`
- `manifest.json`
