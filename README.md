# CursorBridge

**The Content Intelligence Layer for Adaptive Wellness Applications**

CursorBridge syncs Notion-authored content into Supabase and provides optional Core/Sandbox APIs for queries, lens testing, and session generation. The Main App can call these APIs or connect directly to Supabase; see `MAIN_APP_INTEGRATION_PACKAGE.md`.

---

## 🎯 What CursorBridge Does

| Function | Description |
|----------|-------------|
| **Content Sync** | Syncs Notion databases to Supabase tables |
| **Query API** | REST endpoints for content retrieval |
| **Session Generation** | Creates timed sessions from blueprints |
| **Lens System** | 14+ lenses for different explanation styles |
| **Persona System** | 20+ AI voices/personas |
| **Knowledge Bases** | 19+ curated knowledge sources |
| **Meta-Intelligence** | 4 adaptive dimensions (Scope, Depth, Source, Confidence) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Supabase account
- Notion integration token

### Installation

```bash
git clone https://github.com/clanmacarthur/CursorBridge.git
cd CursorBridge
python -m pip install -r api/requirements.txt
python -m pip install -r sandbox/requirements.txt
# Optional: install the CLI package
python -m pip install -e .
```

### Environment Variables

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-service-role-key"
export NOTION_TOKEN="your-notion-integration-token"
```

### Run Servers

```bash
# Terminal 1: Core API (port 3000)
python run_api.py

# Terminal 2: Sandbox API (port 3001)
python run_sandbox.py
```

---

## End-to-End Flow (Beginning -> End)

1. Author content in Notion (programmes, techniques, templates, lenses).
2. Sync Notion to Supabase via `POST /api/sync/notion` or the `cb` CLI (uses `config/bridge.yaml` + `config/notion_db_ids.json`).
3. Supabase becomes the source of truth for content tables and execution-layer tables.
4. Main App reads from Supabase directly (preferred) or via Core API `/api/query/*` and `/api/templates`.
5. Sessions are generated in one of two ways:
   - Main App assembles timeline + narration from `session_blueprints` (see `docs/SESSION_GENERATION_RUNTIME_SPEC.md`) and writes `session_runs` + `session_outputs`.
   - Sandbox API `/sandbox/generate-session` generates demo sessions for validation/testing.
6. Main App plays back the session (example player in `main-app-starter/components/SessionPlayer.vue`).

---

## Action Triggers (Who Calls What)

| Trigger | Action | Endpoint / Tool |
|---------|--------|-----------------|
| Content update | Sync Notion -> Supabase | `POST /api/sync/notion` or `cb export notion-to-db` |
| Content read | Query tables | `GET /api/query/{table}` or direct Supabase |
| Template read | Dashboard templates | `GET /api/templates` |
| Session generation | Build session output | Main App runtime (blueprints) or `POST /sandbox/generate-session` |
| Lens lookup | List lens registry | `GET /sandbox/lenses` |
| Check-in logging | Save user check-in | `POST /api/logs/checkin` or direct Supabase insert |
| Realtime update | Notify content sync | `sync_events` insert (published by `shared/realtime.py`) |

---

## Main App Starter (Nuxt 3 Example)

`main-app-starter/` is a reference Nuxt 3 app that:
- Uses Supabase Auth via `@nuxtjs/supabase`
- Proxies CursorBridge APIs via `server/api/bridge/*`
- Demonstrates session playback + check-ins with example components

For production, follow `MAIN_APP_INTEGRATION_PACKAGE.md` and connect directly to Supabase.

---

## 📡 API Endpoints

### Core API (Port 3000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/query/{table}` | GET | Query any table |
| `/api/templates` | GET | Dashboard templates |
| `/api/schema/{table}` | GET | Table schema info |
| `/api/sync/notion` | POST | Sync Notion to Supabase |

### Sandbox API (Port 3001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sandbox/lenses` | GET | List all 14+ lenses |
| `/sandbox/generate-session` | POST | Generate session from blueprint |
| `/sandbox/demo/generate-flagship` | POST | Demo session with lens |

---

## 📊 Database Tables

### Core Content (25 tables from Notion)
- `attribute_taxonomy`, `programme_profiles`, `session_templates`
- `breath_library`, `movements_system`, `sound_vibration`
- `archetypal_personas`, `chakra_system`, `meridian_system`
- ... and 16 more

### Execution Layer (11 tables)
- `timing_presets` - Duration configurations
- `session_phases` - Phase templates
- `transition_rules` - Phase connections
- `narration_styles` - Voice/pace settings
- `cue_triggers` - Scheduled events
- `session_blueprints` - Complete session recipes
- `technique_steps` - Step sequences
- `blueprint_steps` - Blueprint-step links
- `blueprint_cues` - Blueprint-cue links
- `session_runs` - User session records
- `session_outputs` - Generated content

### Intelligence Layer
- `lens_definitions` - 14+ explanation paradigms
- `meta_lens_presets` - 5+ user-selectable presets
- `knowledge_bases` - 19+ curated sources
- `ai_scope_levels`, `ai_depth_levels`, `ai_source_levels`, `ai_confidence_levels`

---

## 🔮 The Lens System

Same technique, different explanations:

| Lens | Example |
|------|---------|
| **Western** | "Activates parasympathetic nervous system..." |
| **TCM** | "Smooths Liver Qi, releasing stagnation..." |
| **Somatic** | "Notice the settling in your body..." |
| **Spiritual** | "Each breath connects you to source..." |

```bash
# Test it:
curl http://localhost:3001/sandbox/lenses
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=tcm"
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `MAIN_APP_HANDOFF.md` | Share with Main App AI |
| `docs/SESSION_GENERATION_RUNTIME_SPEC.md` | How Main App generates sessions |
| `ADAPTIVE_AI_VISION.md` | Full AI architecture |
| `MAIN_APP_INTEGRATION_PACKAGE.md` | Direct-to-Supabase integration guide |
| `scripts/sync_sessions_dbs_next_to_used.py` | Syncs Notion DB mentions from `Therapuetic next basic` to `Therapeutic USED` |
| `main-app-starter/` | Nuxt 3 starter project |

---

## 🛣️ Future Vision

### Phase 1: Standalone Bridge App
- Downloadable desktop application
- Power Automate Desktop (PAD) integration
- Scheduled content syncs
- Trigger-based automations

### Phase 2: User Knowledge Base Uploads
- Upload personal documents (PDFs, notes, journals)
- AI learns from user-provided texts
- Private knowledge bases with permission controls
- Custom lenses from user content

### Phase 3: Expanded Content Domains

| Domain | Description |
|--------|-------------|
| **Storytelling** | Myths, legends, folklore integration |
| **Religious Texts** | Comparative wisdom traditions (with legal review) |
| **Instruction Manuals** | Step-by-step practice guides |
| **Astrology** | Birth chart integration for personalized sessions |
| **Tarot** | Card readings as session prompts/reflections |

### Phase 4: Advanced AI Features
- Cross-domain technique transfer
- Collective wisdom from anonymized patterns
- Experimental frontier mode with disclaimers
- Buddy/family notification system
- Conversational questionnaires

---

## 🔒 Legal Considerations for Future Features

- **User Uploads**: Terms of service for uploaded content
- **Religious Texts**: Fair use, proper attribution, sensitivity
- **Astrology/Tarot**: Entertainment disclaimer, not predictive claims
- **AI Permissions**: Clear user consent for data usage levels

---

## 🧪 Testing

```bash
# Verify all tables
curl http://localhost:3000/api/query/session_blueprints
curl http://localhost:3000/api/query/timing_presets
curl http://localhost:3000/api/query/narration_styles

# Test lens system
curl http://localhost:3001/sandbox/lenses

# Generate demo session
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=hybrid"
```

---

## 📖 Documentation

- [Main App Handoff](MAIN_APP_HANDOFF.md)
- [Session Generation Spec](docs/SESSION_GENERATION_RUNTIME_SPEC.md)
- [Adaptive AI Vision](ADAPTIVE_AI_VISION.md)
- [Main App Integration Package](MAIN_APP_INTEGRATION_PACKAGE.md)
- [Sessions Handover](docs/HANDOVER_SESSIONS.md)
- [Sessions Master](docs/SESSIONS_MASTER.md)
- [Wheels Pre-Build Reassessment](docs/WHEELS_PREBUILD_REASSESSMENT.md)
- [Grand Project Skeleton](docs/GRAND_PROJECT_SKELETON.md)
- [ISU Integration Map](docs/ISU_INTEGRATION_MAP.md)
- [CursorBridge Role Reset](docs/HANDOVER_CURSORBRIDGE.md)
- [CursorBridge Status Report](docs/CURSORBRIDGE_STATUS.md)
- [Data Model Overview](docs/DATA_MODEL_OVERVIEW.md)
- [Theme Table Catalog](docs/THEME_TABLE_CATALOG.md)
- [Convex Migration Plan](docs/CONVEX_MIGRATION_PLAN.md)
- [Convex Session Lookups](docs/CONVEX_SESSION_LOOKUPS.md)
- [Notion DB Inventory](docs/NOTION_DB_INVENTORY.md)
- [Notion Supabase Convex Plan](docs/NOTION_SUPABASE_CONVEX_PLAN.md)
- [Notion Supabase Sync Run (2026-02-23)](docs/NOTION_SUPABASE_SYNC_RUN_2026-02-23.md)
- [Supabase Sessions Audit](docs/SUPABASE_SESSIONS_AUDIT.md)
- [Sessions Keep Merge Deprecate Matrix](docs/SESSIONS_KEEP_MERGE_DEPRECATE_MATRIX.md)
- [Full System Keep Merge Deprecate Matrix](docs/FULL_SYSTEM_KEEP_MERGE_DEPRECATE_MATRIX.md)
- [Relations Registry Guide](docs/RELATIONS_REGISTRY.md)
- [Relations Existing Table](docs/RELATIONS_EXISTING.csv)
- [Relations To-Be Table](docs/RELATIONS_TO_BE.csv)
- [Relations Master Table](docs/RELATIONS_MASTER.csv)
- [Notion Relations Tracker Spec](docs/NOTION_RELATIONS_TRACKER_SPEC.md)
- [Generation Scope Taxonomy](docs/GENERATION_SCOPE_TAXONOMY.md)
- [Generation Capability Matrix](docs/GENERATION_CAPABILITY_MATRIX.csv)
- [Task-Manager Alignment](docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md)
- [Controlled Port Plan](docs/CONTROLLED_PORT_PLAN_TASK_MANAGER_TO_CURSORBRIDGE.md)
- [Notion Overview](https://www.notion.so/CursorBridge-Overview-Jan-2-2025-2dcc47c61e21815ebd5ffb19738c6e78)

---

## 📊 Current Status

| Component | Status |
|-----------|--------|
| Core API | Implemented (run via `run_api.py`) |
| Sandbox API | Implemented (run via `run_sandbox.py`) |
| Notion Sync | Implemented (Core API + `cb` CLI) |
| Supabase | Required backend |
| Content Tables | Defined + seeded (see SQL files) |
| Execution Tables | Defined + seeded (see SQL files) |
| Lenses | Defined (table + sandbox endpoints) |
| Personas | Defined (table + seed data) |
| Knowledge Bases | Defined (table + seed data) |
| Session Blueprints | Defined (execution layer schema + seeds) |

---

## 🤝 Contributing

This project is designed to work with the Main App (Nuxt 3). See `MAIN_APP_HANDOFF.md` for integration details.

---

## 📜 License

MIT License - See LICENSE file for details.

---

*Built with ❤️ for adaptive wellness*
*Last updated: February 22, 2026*
