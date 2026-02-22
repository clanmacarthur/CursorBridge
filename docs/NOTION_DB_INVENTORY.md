# Notion Database Inventory

Last updated: 2026-02-22
Source pages:
- `2d9c47c6-1e21-80a1-848b-d93728f116cd` (Therapuetic next basic)
- `2d6c47c6-1e21-805c-9796-ff9f33200552` (Therapeutic Databases 0C)
- `36207156f7034c13a839249dee0afe1a` (Therapeutic Databases 0a)

## What we found

- Total discovered databases: 30
- In-scope therapeutic/workflow databases: 27
- Excluded as out-of-scope personal data: finance tracker databases
- Fresh rescan status: 27/27 IDs reachable (all HTTP 200)
- Total rows across in-scope databases: 396
- New 0a page check: 8 child databases found, all already present in `config/notion_db_ids.json`

## In-scope databases with rows

| Key in `config/notion_db_ids.json` | Notion title | Rows |
|---|---|---:|
| `daily_regulation_sliders` | DAILY REGULATION SLIDERS (DB) | 11 |
| `controls_library_design` | Controls Library design | 13 |
| `breathwork_master_taxonomy` | BREATHWORK MASTER TAXONOMY | 12 |
| `colour_legacy_archive` | Colour (Legacy / Archive) | 23 |
| `stones_minerals` | Stones & Minerals (DB) | 55 |
| `astrology_calendrical_systems` | Astrology & Calendrical Systems (DB) | 21 |
| `mythological_beings` | Mythological Beings (DB) | 23 |
| `sacred_animals` | Sacred Animals (DB) | 170 |
| `emotion_brain_body_energy_mapping` | Emotion x Brain x Body x Energy Mapping | 12 |
| `full_brain_neural_systems_table` | FULL BRAIN & NEURAL SYSTEMS TABLE | 19 |
| `nadi_system` | Nadi System (DB) | 10 |
| `deities_archetypes_schema` | Deities & Archetypes (DB) - schema | 1 |
| `contraindications_mandatory_disclosure` | Contraindications (Non-Exhaustive, Mandatory Disclosure) | 11 |
| `during_session_stop_triggers` | During-Session Stop Triggers | 7 |
| `safety_rules` | Safety Rules | 8 |

## In-scope databases with zero rows

| Key in `config/notion_db_ids.json` | Notion title | Rows |
|---|---|---:|
| `control_definitions` | Control Definitions (DB) | 0 |
| `control_packs` | Control Packs (DB) | 0 |
| `profile_pack_map` | Profile Pack Map (DB) | 0 |
| `default_weights` | Default Weights (DB) | 0 |
| `coupling_rules` | Coupling Rules (DB) | 0 |
| `derived_metrics` | Derived Metrics (DB) | 0 |
| `questionnaires` | Questionnaires (DB) | 0 |
| `questionnaire_questions` | Questionnaire Questions (DB) | 0 |
| `symbols_schema` | Symbols (DB) - schema | 0 |
| `colours_schema` | Colours (DB) - schema | 0 |
| `sacred_geometry_schema` | Sacred Geometry (DB) - schema | 0 |
| `sounds_tones_schema` | Sounds & Tones (DB) - schema | 0 |

## Current code reality

- `config/notion_db_ids.json` is now updated with all 27 in-scope database IDs.
- `api/main.py` sync endpoint still has a hard-coded Notion ID map.
- Supabase write code cannot auto-create tables through Supabase API; new table SQL must be created first.

## New Administrative Tracker Databases (2026-02-22)

Created under page `2d9c47c6-1e21-80a1-848b-d93728f116cd`:

| Key in `config/notion_db_ids.json` | Notion title | Rows |
|---|---|---:|
| `relations_master` | Relations Master (DB) | 45 |
| `relations_existing` | Relations Existing (DB) | 16 |
| `relations_to_be` | Relations To-Be (DB) | 44 |

Notes:
- These are administrative tracking databases.
- They are designed to show Supabase status, Convex status, data gaps, and launch readiness.
