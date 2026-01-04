# CursorBridge

**The Content Intelligence Layer for Adaptive Wellness Applications**

CursorBridge connects Notion (content authoring) → Supabase (data storage) → Main App (user interface), providing APIs for session generation, lens switching, and personalized content delivery.

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
pip install -r requirements.txt
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

## 📡 API Endpoints

### Core API (Port 3000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/query/{table}` | GET | Query any table |
| `/api/templates` | GET | Dashboard templates |
| `/api/schema/{table}` | GET | Table schema info |
| `/sync/{db}` | POST | Sync Notion → Supabase |

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
| `SESSION_GENERATION_RUNTIME_SPEC.md` | How Main App generates sessions |
| `ADAPTIVE_AI_VISION.md` | Full AI architecture |
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
- [Notion Overview](https://www.notion.so/CursorBridge-Overview-Jan-2-2025-2dcc47c61e21815ebd5ffb19738c6e78)

---

## 📊 Current Status

| Component | Status |
|-----------|--------|
| Core API | ✅ Running |
| Sandbox API | ✅ Running |
| Notion Sync | ✅ Working |
| Supabase | ✅ Connected |
| 25 Content Tables | ✅ Synced |
| 11 Execution Tables | ✅ Created |
| 14 Lenses | ✅ Active |
| 20 Personas | ✅ Active |
| 19 Knowledge Bases | ✅ Active |
| Session Blueprints | ✅ 5 Platform Examples |

---

## 🤝 Contributing

This project is designed to work with the Main App (Nuxt 3). See `MAIN_APP_HANDOFF.md` for integration details.

---

## 📜 License

MIT License - See LICENSE file for details.

---

*Built with ❤️ for adaptive wellness*
*Last updated: January 2, 2025*
