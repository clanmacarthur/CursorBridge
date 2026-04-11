# BRAZIL / ATLANTIC FOREST STAGE 1 - DATABASE BUILDER EXECUTION HANDOVER

READ THIS AS A STRICT EXECUTION CONTRACT.
DO NOT SUMMARIZE IT.
DO NOT REINTERPRET IT INTO A SMALLER TASK.

PRIMARY OBJECTIVE
Complete Stage 1 botanical data build inside the frozen shared schema and current system logic.

CURRENT CONTEXT
- Brazil branch is the active working branch.
- We are NOT starting Africa.
- We are NOT reopening schema.
- We are continuing the same system objective:
  1. complete Brazil properly
  2. complete Atlantic Forest and surrounding linked regions properly
  3. then use that to readjust UK and connected climates later

SCHEMA RULE
- Schema is frozen.
- Do not redesign tables.
- Do not invent Brazil-only schema.
- Do not reopen architecture.
- Work only against the current canonical schema and current generated operational view.

AUTHORITATIVE FILES
- sql/botanicals/00_core_schema.sql
- docs/BOTANICAL_SYSTEM_SOURCE_OF_TRUTH_V2.md
- docs/BOTANICAL_DATABASE_BUILDER_HANDOVER_V2.md
- docs/BOTANICAL_BRAZIL_THREAD_HANDOVER_V2.md
- docs/BOTANICAL_CANONICAL_VS_ALIAS_MAPPING_V2.md

MANDATORY EXECUTION RULE
DO NOT DEFAULT TO MINIMAL OUTPUT.
DO NOT CAP BELOW 200 ROWS PER BULK BLOCK.
DO NOT RETURN 10, 20, 40, OR "SAMPLE" SETS.
MINIMUM BULK OUTPUT BLOCK = 200 ROWS.
Preferred block size = 200-400 rows.

THIS IS CRITICAL:
The previous repeated failure pattern was minimisation.
That must not happen again.

PHASE RULE
Do not mix phases.
Use strict execution order:
1. identity bulk build
2. enrichment layering
3. propagation/rootstock layering
4. climate/confidence layering
5. final cleanup/integrity

Do not jump backwards.
Do not redesign earlier work.

ATLANTIC FOREST STAGE 1 OBJECTIVE
Build Atlantic Forest and surrounding linked regions to Stage 1 density.

STAGE 1 TARGET COUNTS
- Minimum viable: 2000
- Correct target: 2800
- Stretch: 3500+

Build against the 2800 target.

ZONE TARGETS
- Atlantic Forest Core: 1000
- Restinga / Coastal: 350
- Serra / Montane: 350
- South Subtropical: 300
- Riparian / Wet-edge: 300
- Cerrado Transition: 500

TOTAL = 2800

LAYER TARGETS
- Groundcover / creeping: ~500
- Herbaceous: ~560
- Root crops: ~280
- Shrubs: ~560
- Climbers / vines: ~280
- Small trees (<10m): ~475
- Aquatic / wet margin: ~140

PRIORITY ORDER
1. Endemic / native Atlantic species
2. Edible
3. Medicinal
4. Strong guild / companion value
5. Ecological restoration value
6. Product relevance
7. Small / compact species first
8. Larger canopy later

ROW LOGIC
Identity layer:
- 1 row = 1 real species / cultivar / named variety / named line

Operational layer:
- 1 row = 1 botanical entry x zone x production mode

Do not invent fake cultivars.
Do not inflate row count artificially.
Do not collapse genuinely distinct rows.

DUPLICATION RULE
- Shared-name caps apply to promoted Stage 1 selection per canonical layer, not
  deletion of genuine identity rows.
- Groundcover / herbaceous / epiphyte / compact bromeliad-orchid clusters:
  preferred max `2`
- Allow `3` only where rows are functionally distinct and source-backed.
- Shrubs / small trees: max `2`
- Trees / canopy-scale entries: `1`
- Lower layers may carry more variety than upper layers.
- Smallest-first prioritisation remains mandatory.
- The smallest occupied form wins the layer.
- A compact or dwarf named line may sit below a larger related form if mature
  size and footprint justify it.

MICRO-LAYER RULE
- Do not invent new schema layers for vivariums, terraria, or small domes.
- Use existing layer fields:
  - `food_forest_layer`
  - `canonical_layer_primary`
  - `canonical_layer_secondary`
  - `layer_stack_tags`
- Use size bands and micro tags such as:
  - `micro_mat`
  - `micro_low`
  - `micro_mid`
  - `micro_upper`
- In micro builds, the normal upward transition is:
  - mat / moss-like groundcover
  - low groundcover
  - low herbaceous / fern / rosette
  - upper herbaceous / mounted epiphyte / compact climber
- Do not force `subcanopy` or `canopy` into enclosures that do not physically
  support them.

PROPAGATION RULE
Add / preserve within the frozen schema:
- `grafted_flag`
- `propagation_difficulty`
- `propagation_success_rate`
- `propagation_methods`
- `recommended_establishment_method`
- source-backed compatibility notes only where no frozen structured field exists

Do not assume cross-family grafting.

CRITICAL ANTI-FAILURE RULES
- Do not minimize.
- Do not return sample blocks.
- Do not say "start with a few examples".
- Do not stop after a small set.
- Do not switch to schema discussion.
- Do not ask to confirm every small step.
- Do not reduce output because of caution.

WORKING MODE
- Bulk-first
- Real species only
- Delta-only where appropriate
- Continue in large blocks until zone targets are materially advanced

EXPECTED OUTPUT FORMAT
For each block, return:
1. rows added
2. zone covered
3. layer mix
4. unresolved items
5. next 200+ row block

CURRENT NEXT TASK
Begin Atlantic Forest Core Stage 1 bulk build.
Start with:
- small to medium species first
- edible + medicinal + ecological mix
- minimum 200 rows in first block

FINAL NOTE
The biggest historical failure was repeated minimisation and tiny outputs.
You must actively prevent that.
