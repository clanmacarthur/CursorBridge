# Botanical Brazil Thread Handover V2

Last updated: 2026-04-08

## Purpose

This is the next-thread execution brief for the Brazil branch build.

## Do Not Repeat Previous Failure Pattern

The previous drift happened because structure and data were mixed repeatedly, non-Brazil source lists were reused, and the row logic kept changing mid-stream.

## Locked Execution Order

1. Confirm the schema and columns first.
2. Confirm the row logic first.
3. Confirm size fields are included first.
4. Confirm root, symbiosis, reproductive, and universal layer fields are included first.
5. Then build the Brazil data.
6. Then expand derived views and product logic.

## Locked Row Logic

- identity layer:
  - `1 row = 1 actual species / cultivar / named line`
- operational layer:
  - `1 row = 1 botanical entry x Brazil zone x production mode`

Do not collapse cultivar rows into species-only rows.

## Locked Selection And Layer Rules

- keep `duplicate_name_group` and `duplicate_name_count` populated for
  shared-name clusters
- duplicate caps apply to curated shortlist outputs, not deletion of genuine
  identity rows
- preferred curated cap is `2` rows per shared-name cluster per canonical layer
- allow `3` only when rows are functionally distinct and source-backed
- assign layer from actual occupied mature size and habit, not the largest
  related form elsewhere in the genus
- smallest occupied form wins the layer it actually fits
- compact or dwarf named lines may sit below larger related forms when source
  size data supports that
- do not invent new canonical layers for micro builds; use the same layer
  fields plus size and `layer_stack_tags`

## Brazil Scope Rules

- Brazil is a branch, not a new schema.
- Use the same schema as UK.
- Use the same sweep fields.
- Use the same size fields.
- Use the same reproductive fields.
- Use the same lifecycle and confidence fields.
- Use the same root-detail fields.
- Use the same symbiosis fields.
- Use the same universal layer fields.
- Use the same operational yield/harvest fields.
- Use the same `branch_resources` capability layer.
- Use the same propagation, invasiveness, and climate tolerance fields.
- Preserve the same two-way product logic:
  - `product -> Brazil varieties / trees / entries`
  - `Brazil botanical entry / tree / variety -> valid product paths`

## Brazil Coverage Rules

The branch must be able to cover at minimum:

- Amazon
- Cerrado
- Atlantic Forest
- Caatinga
- Pantanal
- South subtropical systems
- protected-culture crossover where relevant

## Stop Rule

Stop when:

- all major Brazil ecological and cultivation systems are represented
- all major economic, medicinal, heritage, and conservation ranges are represented

Do not treat "everything in existence" as the stop condition.

## Miscommunication Notes To Avoid Repeat

- Do not substitute a general botanical list when a Brazil-only branch is requested.
- Do not restart schema design inside a data-build thread.
- Do not switch between species-only and cultivar-level rows.
- Do not over-explain instead of producing the requested data/docs.
- Do not omit size fields. Tree height and spread are required builder filters.
- Do not collapse min/max size ranges back into one value when the richer Brazil
  identity workbook provides the range.
- Do not omit self-fertility, spacing, or establishment-method fields where source data supports them.
- Do not blur symbiosis into generic companion notes.
- Do not reduce the product layer to a one-way list. Brazil must keep the same
  product-first and botanical-first navigation behavior as UK.
- Do not drop source URLs, confidence fields, endemic flags, or Brazil-specific
  ecological tolerance fields when mapping from the larger identity workbook.
