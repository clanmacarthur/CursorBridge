# SECTION 1 - CURRENT OBJECTIVE

## 1.1 What this build is

This build is a **Session Composer**.

A user should be able to:
1. choose a subject,
2. browse a large visual wheel of domains,
3. click a domain,
4. drill down into real items from the database,
5. add selected items into an ordered session stack,
6. preview the combined session,
7. save it as a custom session.

The first working build is **not** a blueprint browser and **not** a script architecture document.

## 1.2 What this build is not

This build is not centered on:
- narration styles,
- lens presets,
- personas,
- meta-lens presets,
- old session templates,
- control packs,
- coupling rules,
- prewritten two-audio frameworks.

Those can remain in the database, but they do not drive the first working composer.

## 1.3 What counts as success

A working prototype must allow at least these three user-built flows:

1. Breath only
2. Breath + movement
3. Breath + colour or sound + movement + nutrition

Each of those must:
- show real rows from the database,
- build a visible stack,
- preview a combined session outline,
- save a record into the session output path.

## 1.4 What the wheel represents

The wheel represents **domains**, not every row.

Examples of domains:
- Breath
- Movement
- Colour
- Organ / Emotion
- Meridian
- Sound
- Nutrition
- Symbol
- Geometry
- Chakra

The wheel stays large and readable.
The actual row selection happens in a right-side drawer.

---

# SECTION 2 - USER EXPERIENCE

## 2.1 Screen entry

At the top of the page, the user sees **subject buttons or tabs**.

These are high-level categories such as:
- regulation,
- training,
- recovery,
- and any other real subject categories present in the current session type and taxonomy data.

These are not giant dropdowns.
They are the first narrowing step.

## 2.2 Main wheel

The centre of the screen is one large wheel.

Each ring or segment represents a domain.
The wheel does not attempt to show hundreds of row labels at once.

Clicking a domain does not immediately generate a session.
It opens a drawer for real selection.

## 2.3 Right-side drill-down drawer

When the user clicks a domain, a drawer opens on the right.

That drawer must show:
- a search box,
- a list of real database rows,
- live filter chips generated from real columns,
- a detail view for the selected row,
- an add button.

If a domain has only a small number of rows, the list can appear directly.
If a domain has many rows, the list must be searchable and filterable.

## 2.4 Session stack

Every time the user adds an item, it goes into an ordered stack.

Example stack:
1. breathing method
2. colour or sound cue
3. movement practice
4. nutrition note

The user must be able to:
- reorder stack items,
- remove stack items,
- inspect each stack item,
- repeat the process across multiple domains.

## 2.5 Preview

Preview must show:
- the chosen subject,
- the selected stack in order,
- any safety warnings,
- a simple session outline,
- a combined output preview.

This is where the user sees whether the selected combination makes sense.

## 2.6 Save

The user can save the result as a **custom session**.

Saved sessions can later become examples, templates, or programme components.
But saved sessions are an output of the composer, not the starting point of the product.

---

# SECTION 3 - DOMAIN TO DATABASE MAP

## 3.1 Breath domain

- Table: `breath_library`
- Main label: `protocol_name`
- Suggested filter columns:
  - `typical_use`
  - `activation_level`
  - `safety_tier`
  - `core_breath_quality`

## 3.2 Movement domain

- Table: `movements_system`
- Main label: `movement___practice`
- Suggested filter columns:
  - `movement_family`
  - `intensity`
  - `primary_effect`
  - `intent___condition_fit`
  - `primary_body_region`

## 3.3 Organ / Emotion domain

- Table: `organ_emotion_system`
- Main label: `organ___system`
- Suggested filter columns:
  - `primary_emotion`
  - `stress_expression`
  - `breath_type`
  - `regulation_direction`

## 3.4 Meridian domain

- Table: `meridian_system`
- Main label: `meridian`
- Suggested filter columns:
  - `associated_organ`
  - `primary_emotion`
  - `five_element_phase`
  - `nervous_system_bias`

## 3.5 Colour domain

- Table: `light_colour`
- Main label: `light___colour`
- Suggested filter columns:
  - `colour_family`
  - `psychological_theme`
  - `circadian_influence`

## 3.6 Sound domain

- Table: `sound_vibration`
- Main label: `sound_type`
- Secondary label: `sound___frequency`
- Suggested filter columns:
  - `primary_effect`
  - `nervous_system_bias`
  - `primary_organ`

## 3.7 Nutrition domain

- Primary table: `nutrition_and_food`
- Main label: `food_type`
- Suggested filter columns:
  - `primary_nutrition_domain`
  - `associated_diets___protocols`
  - `evidence_confidence`

- Secondary table: `nutrition_protocols`
- Main label: `nutrition_protocol`
- Suggested filter columns:
  - `primary_nutrition_goal`
  - `primary_attribute_focus`
  - `strictness_level`

## 3.8 Symbol domain

- Table: `symbols_index`
- Main label: `symbol`
- Suggested filter columns:
  - `symbol_class`
  - `meaning_domain`
  - `emotional_tone`
  - `cultural_scope`

## 3.9 Supporting logic tables

These do not appear as the main visual wheel, but they drive filtering, matching, safety, and saving:

- `session_types`
- `attribute_taxonomy`
- `mappings`
- `cross_domain_mappings`
- `safety_rules`
- `session_runs`
- `session_outputs`

## 3.10 Parked tables for this build

These remain in the schema but do not drive the first composer prototype:

- `session_blueprints`
- `session_templates`
- `narration_styles`
- `lens_definitions`
- `meta_lens_presets`
- `control_definitions`
- `control_packs`
- `control_pack_items`
- `coupling_rules`

---

# SECTION 4 - COMPOSITION LOGIC AND TESTING

## 4.1 How combinations are chosen

The user builds the session by combining items from multiple domains.

The system may narrow related options using:
- direct affinity columns already stored in the domain tables,
- `mappings`,
- `cross_domain_mappings`,
- `safety_rules`.

Unsafe combinations must be blocked or clearly warned.

## 4.2 What gets saved

The saved result must create records through the session output path.

Minimum expected save path:
- `session_runs`
- `session_outputs`

## 4.3 Minimum working test suite

The first prototype is not complete until all three of these work visibly:

1. Breath only
2. Breath + movement
3. Breath + colour or sound + movement + nutrition

For each one, the prototype must show:
- subject selected,
- domain chosen,
- rows loaded in drawer,
- item added to stack,
- combined preview visible,
- saved output record created.

## 4.4 What gets archived from the old document

The older Section 6 to Section 9 material should be archived as prior architecture.
It should not continue to define the current Sessions build.

That older material focused on:
- script-generation logic first,
- two-audio interlock,
- narration layers,
- future dropdown engines,
- Notion-first architecture.

The current build is instead:
- subject-first,
- one large wheel,
- drawer-based row selection,
- stack-based composition,
- preview and save.

## 4.5 Completion rule

The current Sessions prototype is complete only when a user can build their own session from real domain tables without needing a pre-made blueprint as the main entry path.
