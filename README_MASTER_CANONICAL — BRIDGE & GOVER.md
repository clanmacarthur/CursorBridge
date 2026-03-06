README_MASTER_CANONICAL - BRIDGE & GOVERNANCE
Alignment note (2026-02-21):

- Current live UI route in this repo is `/session` (`main-app-starter/pages/session.vue`).
- `/sessions` is the planned wheel-based builder route and is not the current production flow.
- Planned wheel and theme-graph work must be treated as target architecture until code is present.
- Canon source docs for table truth remain:
  - `canon/TableIndex.md`
  - `canon/SystemManifest.md`
  - `canon/RelationsManifest.md`
- Handover docs for this transition:
  - `docs/HANDOVER_SESSIONS.md`
  - `docs/HANDOVER_CURSORBRIDGE.md`
  - `docs/DATA_MODEL_OVERVIEW.md`
  - `docs/THEME_TABLE_CATALOG.md`

0) Non-negotiables

Supabase is canonical runtime. Notion is optional authoring and must not be required at runtime.

The Bridge/Operator is the only layer allowed to create/alter schemas and seed canonical libraries.

The Main App never writes to canonical libraries. It writes only user state (check-ins, session runs, session outputs).

No direct writes from any generation process into canonical libraries. All generation produces artefacts that can be promoted only through Bridge rules.

1) The three apps and their boundaries

A) Wellness App (End-User App)

Purpose: UI/UX, auth, dashboard rendering, session playback, user logs.

Data: reads canonical libraries; writes user state.

Must not: run migrations; mutate canonical libraries; invent schema.

B) Connector / Operator App (Bridge)

Purpose: ingestion (Notion/CSV/Excel/external), normalization, schema enforcement, migrations, seeding, promotion workflow.

Data: maintains canonical library tables and engine tables.

Must not: implement UI logic for end users.

C) Sandbox + Validation Environment

Purpose: safe experimentation, simulations, review workflows, professional validation.

Data: produces validated artefacts; never touches production user data.

MVP note: sandbox can be "logical boundary" behind the Bridge; full professional UX can come later.

2) Canonical lens set (few masters, deep sub-layers)

The system uses a small set of master lenses with deep sub-lenses. These affect explanation style, language, symbolism, and optional mappings. They must not change the underlying technique objects.

Master lenses (canonical):

Western (biomedical/physiology)

TCM (Five Elements, Qi, meridians)

Ayurveda (doshas, prana)

Yogic/Energetic (chakras, nadis, bandhas)

Somatic/Trauma-Informed (titration, safety cues, nervous system language)

Spiritual/Esoteric (symbolic/ritual language; non-medical)

Athletic/Performance (training/recovery framing)

Hybrid (explicitly composes 2+ master lenses)

Sub-lenses (examples; extend later):

Western: neuroscience, autonomic physiology, sleep science

TCM: Five Elements emphasis, organ clock, eight principles

Yogic: chakra emphasis, pranayama emphasis

Somatic: polyvagal framing, interoception emphasis

Rule: master lens is mandatory per session; sub-lens optional.

3) Organ/system coverage (no single-organ examples)

When an organ/system mapping exists, it must support at minimum these systems, each with lens-specific fields:

Cardiovascular

Respiratory

Nervous (CNS/PNS/ANS)

Endocrine

Digestive

Hepatobiliary (liver/gallbladder)

Renal/urinary (kidneys/bladder)

Immune/lymph

Musculoskeletal

Integumentary (skin)

Reproductive

TCM organ network must support:

Zang: Heart, Liver, Spleen, Lung, Kidney

Fu: Small Intestine, Gallbladder, Stomach, Large Intestine, Bladder, San Jiao

Pericardium as functional system

Rule: do not ship partial organ mappings as "complete". Partial is allowed only when explicitly flagged as partial with missing list.

4) What already exists (do not recreate)

Canonical libraries (expected to already exist in Supabase; verify, do not rebuild):

Attribute Taxonomy (DB)

Programme Profiles (DB)

Dashboard Blocks (DB)

Session Types (DB)

Session Templates (DB) (one canonical set)

Safety Rules (DB)

Breath Library (DB)

Movement Systems (DB)

Sound & Vibration (DB)

Light & Colour (DB)

Symbols Index (DB)

Sacred Geometry (DB)

Archetypal Personas (DB)

Chakra Systems (DB)

Meridian System (DB)

Organ-Emotion System (DB)

Nutrition core (expected to exist):

Nutrition and Food (DB) - MASTER TABLE

Nutrition Intake (DB)

Nutrition Protocols (DB)

Supplement Interactions (DB)

5) Missing "session richness" layer (must exist for timed guided sessions)

These are engine/execution tables that turn selections into a timed, cue-driven script.

Required tables:

timing_presets

session_phases

transition_rules

technique_steps

cue_triggers

narration_styles

session_blueprints

session_runs

session_plan_blocks

session_plan_cues

session_output_text

Rule: Programme Profiles store defaults (lens, timing preset, blueprint availability). They do not store timelines.

6) Evidence + Techniques (validation-ready)

Required tables:

evidence_sources

validation_reviews

professional_profiles

credentials_licensure

approval_states

audit_logs

techniques

Minimal requirement for this phase:

evidence_sources includes citation fields and review state

techniques includes lens explanation templates and safety links

7) Bridge deliverables (exact outputs)

Bridge must produce these artefacts as files (Markdown + JSON):

SystemManifest.md (what tables exist; purpose; pk; level)

RelationsManifest.md (edges and join tables)

TableIndex.md (table list + key columns)

SeedPack.md (exact seeded rows for presets)

Bridge must implement one script:

apply_mappings (reads mappings table and populates join tables / defaults deterministically)

8) Acceptance criteria for "sessions fully as intended"

"Sessions fully as intended" is achieved when the following end-to-end path works without manual linking:

One blueprint selected in UI generates a session run.

The run expands to a phase timeline with blocks and transitions.

Cues fire sounds/colours/symbols/organs at timestamps.

Output text is long enough to cover the chosen duration.

Lens switch changes explanation language without changing the underlying technique sequence.

Safety rules are attached and displayed.
