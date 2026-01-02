# System Manifest

**CursorBridge Database Registry**

Generated: 2025-01-02

---

## Overview

This document lists all databases in the CursorBridge system, their purpose, ownership, and relationships.

---

## 1. Library Backbone (Content Layer)

These databases are **read-only at runtime** for end users. They define what exists in the system.

| Database | Purpose | Primary Key | Level |
|----------|---------|-------------|-------|
| `system_manifest` | Tracks what exists / what is canonical / archived | id | Engine |
| `attribute_taxonomy` | Universal hierarchy for all capabilities, domains, parameters | id, notion_page_id | Engine |
| `programme_profiles` | Preset lenses (Athlete, Trauma-Safe, Breath-Only, etc.) | id, notion_page_id | Engine |
| `dashboard_blocks` | Reusable UI modules (daily check-ins, packs, sections) | id, notion_page_id | Engine |
| `session_templates` | Declarative recipes for generating sessions | id, notion_page_id | Engine |
| `session_types` | High-level session categories (regulation, training, recovery) | id, notion_page_id | Engine |
| `safety_rules` | Contraindications, exclusions, gating logic | id, notion_page_id | Engine |
| `rules_gating` | Rule engine layer (trigger/threshold, safety gating) | id, notion_page_id | Engine |

---

## 2. Modal/Symbolic Systems

| Database | Purpose | Primary Key | Level |
|----------|---------|-------------|-------|
| `breath_library` | Breath protocol library | id, notion_page_id | Content |
| `movements_system` | Movement practices library | id, notion_page_id | Content |
| `sound_vibration` | Sound and vibration modalities | id, notion_page_id | Content |
| `light_colour` | Light and color modalities | id, notion_page_id | Content |
| `symbols_index` | Symbol reference library | id, notion_page_id | Content |
| `sacred_geometry` | Sacred geometry forms | id, notion_page_id | Content |
| `archetypal_personas` | AI persona styles (canonical "Style" system) | id, notion_page_id | Content |
| `deities_archetypes` | Deity and archetype index | id, notion_page_id | Content |
| `chakra_systems` | Chakra reference | id, notion_page_id | Content |
| `meridian_system` | Meridian reference | id, notion_page_id | Content |
| `organ_emotion_system` | Organ-emotion mappings | id, notion_page_id | Content |
| `elemental_framework` | Elemental system (fire, water, earth, air, etc.) | id, notion_page_id | Content |

---

## 3. Nutrition Core

| Database | Purpose | Primary Key | Level |
|----------|---------|-------------|-------|
| `nutrition_and_food` | MASTER nutrition table | id, notion_page_id | Content |
| `nutrition_intake` | User nutrition logs | id | User |
| `nutrition_protocols` | Diet/protocol definitions | id, notion_page_id | Content |
| `supplement_interactions` | Supplement interaction rules | id, notion_page_id | Content |

---

## 4. Automation Backbone (Engine Layer)

These databases power the adaptive engine - weights, coupling, and automation.

| Database | Purpose | Primary Key | Level |
|----------|---------|-------------|-------|
| `control_definitions` | Every knob/tick the UI can render | id | Engine |
| `control_packs` | Curated bundles of controls | id | Engine |
| `control_pack_items` | Join: packs ↔ controls | id | Engine |
| `profile_pack_map` | Programme profiles → default packs | id | Engine |
| `default_weights` | Baseline weights per profile | id | Engine |
| `coupling_rules` | How controls influence each other | id | Engine |
| `derived_metrics` | Computed scores from raw values | id | Engine |
| `questionnaires` | Questionnaire definitions | id | Engine |
| `questionnaire_questions` | Questions within questionnaires | id | Engine |
| `mappings` | Automation rules (value→relation, defaults) | id | Engine |

---

## 5. User Data Layer

These databases store user-specific data. **RLS enabled**.

| Database | Purpose | Primary Key | Level |
|----------|---------|-------------|-------|
| `user_dashboard_layouts` | User dashboard configurations | id | User |
| `user_checkins` | Daily check-in entries | id | User |
| `questionnaire_responses` | User questionnaire answers | id | User |
| `session_runs` | Generated session instances | id | User |
| `session_outputs` | Session plans/scripts | id | User |

---

## 6. Sync/Integration

| Database | Purpose | Primary Key | Level |
|----------|---------|-------------|-------|
| `sync_events` | Realtime sync events for Main App | id | System |

---

## Table Ownership

### CursorBridge Owns (Content + Engine)

All tables in sections 1-4 above.

- Synced from Notion (content)
- Managed by CursorBridge APIs
- Read-only for Main App

### Main App Owns (User Data)

All tables in section 5 above, plus:

- `user_profiles` (if separate from auth.users)
- `dashboards` (Main App's dashboard instances)
- `dashboard_blocks` (Main App's block instances)
- `block_data` (Main App's block values)
- `contracts` (marketplace)
- `marketplace_listings` (marketplace)
- `purchases` (marketplace)
- `automations` (user automation rules)

---

## Key Relations

### Engine Relations

```
programme_profiles → control_packs (via profile_pack_map)
programme_profiles → default_weights → attribute_taxonomy
control_packs → control_definitions (via control_pack_items)
coupling_rules → control_definitions (from/to)
derived_metrics → control_definitions (inputs)
questionnaires → questionnaire_questions
```

### Session Relations

```
session_templates → session_types
session_templates → archetypal_personas (style)
session_templates → breath_library
session_templates → movements_system
session_templates → safety_rules
session_runs → session_templates
session_runs → session_outputs
```

### User Relations

```
user_dashboard_layouts → control_packs
user_dashboard_layouts → dashboard_blocks
user_checkins → control_definitions
questionnaire_responses → questionnaires
questionnaire_responses → programme_profiles
```

---

## Database Levels

| Level | Description | Who Manages |
|-------|-------------|-------------|
| **Engine** | Core system logic, shared across all sectors | CursorBridge |
| **Content** | Library data (protocols, movements, etc.) | CursorBridge (from Notion) |
| **User** | User-specific data | Main App |
| **System** | Infrastructure (sync, events) | CursorBridge |

---

## Migration Notes

1. **Existing tables** (from Notion sync): Do NOT recreate
2. **New automation tables**: Created via `supabase_automation_tables.sql`
3. **Seed data**: Applied via `scripts/apply_mappings.py`
4. **Notion mirrors**: Created via `scripts/create_notion_databases.py`

---

## Verification Queries

```sql
-- Count all tables
SELECT COUNT(*) FROM information_schema.tables 
WHERE table_schema = 'public';

-- List tables with row counts
SELECT schemaname, relname, n_live_tup 
FROM pg_stat_user_tables 
ORDER BY n_live_tup DESC;

-- Check automation tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'control_definitions', 'control_packs', 'coupling_rules',
    'derived_metrics', 'questionnaires', 'user_checkins'
);
```

