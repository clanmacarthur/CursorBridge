# BOTANICAL SYSTEM / BRAZIL / ATLANTIC FOREST - ACTIVE EXECUTION CONTRACT

Last updated: 2026-04-11

Use this as the sole active execution contract for botanical build work in this
repo.

This is execution work, not discussion.
Do not summarize this handover back.
Do not reduce it to a starter sample.
Do not ask to confirm what is already stated.
Continue the work directly.

## Primary Objective

Build out the Brazil branch properly inside the one shared botanical system,
with Atlantic Forest as the active branch-zone program.

The immediate goal is not to redesign anything.
The goal is to continue the missing variety cycle at scale, using the frozen
schema, until Atlantic Forest has far broader useful species coverage than it
has now.

## Current Truth

- There is one botanical database system, not separate country schemas.
- Brazil is the active branch.
- Atlantic Forest Stage 1 is the active program.
- Schema is frozen.
- Current work is still identity-led botanical build, with later
  operational/detail layers mapping into the frozen normalized system.
- A provisional clean kept-set exists at about 1600 rows, but the variety
  cycle is not finished and must continue before the final hard lock.

## Authoritative Files

Use these as source of truth in this order:

1. `sql/botanicals/00_core_schema.sql`
2. `docs/BOTANICAL_SYSTEM_SOURCE_OF_TRUTH_V2.md`
3. `docs/BOTANICAL_DATABASE_BUILDER_HANDOVER_V2.md`
4. `docs/BOTANICAL_BRAZIL_THREAD_HANDOVER_V2.md`
5. `docs/BOTANICAL_BRAZIL_ATLANTIC_FOREST_STAGE1_DATABASE_BUILDER_HANDOVER_2026-04-08.md`
6. `docs/BOTANICAL_APP_BOUNDARIES_V1.md`
7. `docs/BOTANICAL_APP_BUILD_ORDER_V1.md`
8. `docs/BOTANICAL_CANONICAL_VS_ALIAS_MAPPING_V2.md`
9. `docs/BOTANICALS_MASTER_RELATION_MAPPING_2026-03-30.md` only as legacy
   union-import/load-order context, not live schema authority

## Locked Schema Rules

- Do not reopen schema.
- Do not create a Brazil-only schema.
- Do not collapse the normalized table stack into one giant table.
- Do not move product logic into the identity table.
- Do not move protocol logic into the identity table.
- Keep canonical layers as:
  - `canonical_layer_primary`
  - `canonical_layer_secondary`
  - `layer_stack_tags`
- `food_forest_layer` remains display-facing only and does not replace
  canonical layers.
- Micro/vivarium logic uses existing canonical layers plus tags like:
  - `micro_mat`
  - `micro_low`
  - `micro_mid`
  - `micro_upper`
- No invented micro schema layers.

## Row Logic

Identity layer:

- `1 row = 1 real botanical entry / species / cultivar / named line only when genuinely distinct and source-backed`

Operational layer:

- `1 row = 1 botanical entry x branch x zone x production mode`

- Do not invent fake cultivars.
- Do not inflate row count using trivial compact/nano/micro variants unless
  the smaller occupied form is genuinely important and functionally distinct.
- Same-name curation cap is:
  - `2` preferred per canonical layer
  - `3` only when functionally distinct and source-backed
- If a compact form is only a size note and not a true distinct line, merge it
  later into the parent species and do not treat it as real breadth.

## Main Failure To Prevent

The previous builder repeatedly minimized output, reused the same parent taxa
with compact or hold variants, and acted as if tiny blocks were acceptable.
Do not do that.

## Strict Execution Rule

- Do not pause to narrate what you are about to do.
- Do not ask for confirmation unless there is a genuine blocking contradiction.
- Do not keep returning undersized blocks.
- Do not pad with repeated species or trivial variants to fake expansion.
- Do not stop the variety cycle unless explicitly told to stop.

## Output Size Rule

For every real expansion pass, output large bulk blocks only.
Target behavior should be very large.

- Do not behave as though 50, 100, or 150 rows is acceptable for a main
  expansion pass.
- Use aggressive bulk execution and keep going.
- The human explicitly wants continuous execution and does not want narration
  between blocks.

## Current Priority

The builder must continue the variety-expansion cycle for Atlantic Forest using
genuinely new accepted species first, not repeated compact variants.

The top priority missing or underfilled areas still include:

- true canopy and upper-subcanopy diversity
- additional underrepresented Atlantic Myrtaceae
- additional underrepresented Lauraceae
- fruit-tree diversity
- medicinal shrub and tree diversity
- fauna-host vines and trees
- additional endemic/threatened overlap where genuinely new
- fungal depth later if needed, but not through generic placeholders
- root / underground-storage depth later if needed, but not through crop-drift
  rows

## Current Dataset State

- There was a historical draft build that reached roughly 2030 rows.
- A re-pruned working kept-set estimate exists at about 1600 rows.
- That 1600 is a cleaned base, not the end of the variety cycle.
- The next work should expand beyond that base with real species diversity,
  then later re-prune again.

## Keep / Merge / Remove Logic

Keep:

- threatened-priority species
- endemic-priority species
- strong Atlantic Forest bromeliads
- strong Atlantic Forest orchids
- strong lowest ground-floor and wet-edge species
- strong medicinal understory rows
- strong edible / fruit tree rows
- strong fauna-host rows
- strong canopy and upper-subcanopy structural rows
- strong visible fungal decomposer rows where clearly useful

Merge:

- juvenile rows into real species rows where the real species row exists
- compact / nano / micro forms into real species rows where they are not true
  distinct lines
- priority duplicates into one upgraded parent species row
- same-name rows above curation cap into the strongest one or two rows

Remove:

- weak-core ornamentals
- broad ruderal herbs
- placeholder hold rows with no strategic reason to remain
- generic fungal placeholders
- generic mycorrhiza placeholders in identity layer
- duplicate compact variants that add no real structural or taxonomic value
- non-core horticultural drift

## Distance / Spacing Requirement

The human explicitly wants distance data added where relevant.
Preserve and populate spacing-related fields whenever operational/detail
mapping is being carried forward or prepared:

- `spacing_in_row_m`
- `spacing_between_rows_m`
- `spacing_notes`

Apply this per accepted species / cultivar / named-line row where relevant.

Do not invent false precision.
Use real source-backed ranges or clear placeholders for later fill if exact
spacing is not yet known.

Where a species has meaningful spacing implications because of root spread,
mature spread, or canopy behavior, make sure this is not lost.

## Other Important Detail Fields To Preserve

At minimum, builder work must stay compatible with the frozen field set already
locked in the system, especially:

- `perennial_main_group`
- `sweep_bucket`
- `scarcity_class`
- `conservation_relevance`
- `heritage_flag`
- `medicinal_flag`
- `ecological_value_flag`
- `perennial_rating`
- `inclusion_rationale`
- `mature_height_m_min`
- `mature_height_m_max`
- `mature_height_m`
- `mature_spread_m_min`
- `mature_spread_m_max`
- `mature_spread_m`
- `size_class`
- `root_volume_class`
- `container_suitable`
- `pruning_response`
- `dwarf_flag`
- `grafted_flag`
- `common_name_en`
- `self_fertile_flag`
- `pollination_requirement`
- `pollinator_type`
- `pollination_notes`
- `plant_lifespan_years`
- `productive_lifespan_years`
- `replacement_cycle_years`
- `system_roles`
- `propagation_difficulty`
- `propagation_success_rate`
- `invasiveness_risk_level`
- `spread_control_required`
- `min_temp_c`
- `max_temp_c`
- `drought_tolerance`
- `frost_tolerance`
- `endemic_to_brazil`
- `conservation_flag`
- `invasive_risk_brazil`
- `source_url_primary`
- `source_url_secondary`
- `source_url_tertiary`
- `canonical_layer_primary`
- `canonical_layer_secondary`
- `layer_stack_tags`

## Quality Filter

Every new expansion row should be judged by:

- Is this a genuinely new accepted species or real named line?
- Does it improve Atlantic Forest coverage?
- Does it fit the frozen schema?
- Does it avoid redundant same-name inflation?
- Does it add real ecological, medicinal, edible, structural, conservation, or
  fauna-host value?

If not, do not add it.

## Current Instruction To Execute

Continue the Atlantic Forest variety cycle immediately with broad, genuinely
new species expansion.

- Bias next on real species, not repeated compact variants.
- Bias strongly toward underfilled canopy and upper-subcanopy,
  underfilled genera, real fruit-tree diversity, medicinal diversity, and
  underrepresented Atlantic species.
- Carry spacing/distance needs forward per accepted row where relevant.
- Do not stop to explain.
- Do not ask for confirmation.
- Do not shrink the output.
- Keep going until the variety cycle is materially advanced, then re-prune
  against the expanded base.

## Final Reminder

The previous assistant wasted time by repeating the same taxa, narrating
instead of executing, and shrinking output blocks.

The correct workflow is:

1. receive command
2. execute immediately
3. continue execution
4. answer interruptions inline without abandoning the build
5. stop only when explicitly told to stop
