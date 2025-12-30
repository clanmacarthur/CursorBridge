# CursorBridge

**Content sync and session generation for wellness applications.**

CursorBridge syncs content from Notion databases to Supabase and provides APIs for dashboard templates, session generation, and content queries.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Main App (Port 8080)                    │
│                    Vue 3 + Nuxt 3 Dashboard Builder             │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP + JWT Auth
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CursorBridge APIs                          │
│  ┌──────────────────────┐    ┌──────────────────────────────┐   │
│  │   Core API (:3000)   │    │   Sandbox API (:3001)        │   │
│  │  • /api/templates    │    │  • /sandbox/generate-session │   │
│  │  • /api/query/{t}    │    │  • /sandbox/build-dashboard  │   │
│  │  • /api/schema/{t}   │    │                              │   │
│  │  • /api/sync/notion  │    │                              │   │
│  └──────────────────────┘    └──────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supabase (Shared Backend)                    │
│  ┌──────────────┐  ┌────────────┐  ┌─────────────────────────┐  │
│  │ PostgreSQL   │  │  Auth      │  │  Realtime               │  │
│  │ 25+ content  │  │  JWT       │  │  sync_events channel    │  │
│  │ tables       │  │  validation│  │                         │  │
│  └──────────────┘  └────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Supabase account
- Notion integration (optional, for content sync)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/CursorBridge.git
cd CursorBridge

# Install dependencies
pip install -r requirements.txt

# For Supabase support
pip install supabase psycopg2-binary
```

### Configuration

Create a `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
NOTION_TOKEN=your-notion-integration-token
```

### Running the APIs

```bash
# Core API (port 3000)
python run_api.py

# Sandbox API (port 3001)
python run_sandbox.py
```

---

## 📚 API Reference

### Core API (Port 3000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/templates` | GET | List dashboard templates |
| `/api/templates/{id}` | GET | Get specific template |
| `/api/schema/{table}` | GET | Get field documentation |
| `/api/query/{table}` | GET | Query content tables |
| `/api/sync/notion` | POST | Sync from Notion |
| `/api/logs/checkin` | POST | Log user check-in |

### Sandbox API (Port 3001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/sandbox/generate-session` | POST | Generate guided session |
| `/sandbox/build-dashboard` | POST | Build dashboard from template |

---

## 📦 Dashboard Templates

5 pre-built templates available via `GET /api/templates`:

| ID | Name | Category | Blocks |
|----|------|----------|--------|
| `daily-wellness-check` | Daily Wellness Check | wellness | 5 |
| `breath-movement` | Breath & Movement | fitness | 3 |
| `meditation-journal` | Meditation Journal | meditation | 7 |
| `nutrition-tracker` | Nutrition Tracker | nutrition | 4 |
| `sleep-tracker` | Sleep Tracker | wellness | 6 |

### Template Format

```json
{
  "id": "daily-wellness-check",
  "name": "Daily Wellness Check",
  "description": "Track your daily mood, sleep quality, energy, and stress levels",
  "category": "wellness",
  "icon": "heart",
  "blocks": [
    {
      "block_type": "slider",
      "config": {
        "label": "Mood",
        "min": 1,
        "max": 10,
        "step": 1,
        "default": 5
      },
      "position": {"x": 0, "y": 0, "w": 6, "h": 2}
    }
  ]
}
```

---

## 🧘 Session Generation

`POST /sandbox/generate-session`

### Request

```json
{
  "user_id": "user-uuid",
  "template_id": "session-template-id",
  "duration_min": 15,
  "preferences": {
    "intensity": "gentle",
    "focus": "relaxation"
  }
}
```

### Response

```json
{
  "id": "session-uuid",
  "name": "Morning Energy Flow",
  "duration_minutes": 15,
  "persona_style": "Alan Watts-like",
  "sections": [
    {
      "type": "breathwork",
      "name": "Physiological Sigh",
      "duration_minutes": 2.5,
      "instructions": "Begin with deep breathing...",
      "cues": [
        "0:00 - Begin breathing",
        "0:30 - Deepen your breath",
        "2:00 - Prepare to transition"
      ]
    },
    {
      "type": "movement",
      "name": "Qigong Silk Reeling",
      "duration_minutes": 7.5,
      "instructions": "Practice gentle movement..."
    },
    {
      "type": "breathwork",
      "name": "Integration Breath",
      "duration_minutes": 5,
      "instructions": "Return to natural breathing..."
    }
  ],
  "safety_warnings": ["Avoid if experiencing acute anxiety"]
}
```

---

## 🗄️ Content Tables

CursorBridge owns these Supabase tables (synced from Notion):

| Table | Description |
|-------|-------------|
| `programme_profiles` | Wellness programme definitions |
| `breath_library` | Breath protocol library |
| `movements_system` | Movement practices |
| `session_templates` | Session recipes |
| `archetypal_personas` | AI persona styles |
| `attribute_taxonomy` | Attribute hierarchy |
| `safety_rules` | Safety gating rules |
| `nutrition_and_food` | Nutrition database |
| `chakra_systems` | Chakra reference |
| `meridian_system` | Meridian reference |
| ... and 15+ more |

Use `GET /api/schema/{table}` for field documentation.

---

## 🔐 Authentication

CursorBridge validates Supabase JWTs. Include in requests:

```
Authorization: Bearer <supabase_jwt>
```

JWT claims expected:
- `sub` - User ID
- `email` - User email
- `role` - User role (optional)

---

## 🔄 Realtime Sync

Content updates are published to Supabase Realtime via the `sync_events` table:

```json
{
  "type": "content_synced",
  "table": "programme_profiles",
  "record_id": "uuid",
  "timestamp": "2025-12-30T12:00:00Z"
}
```

Subscribe in Main App to receive live updates.

---

## 📁 Project Structure

```
CursorBridge/
├── api/
│   └── main.py           # Core API (FastAPI)
├── sandbox/
│   └── main.py           # Sandbox API (FastAPI)
├── shared/
│   ├── auth.py           # JWT validation
│   ├── database.py       # Supabase client
│   ├── realtime.py       # Realtime publishing
│   └── templates.py      # Dashboard templates
├── cb/
│   ├── bridge.py         # Notion→DB sync logic
│   ├── notion.py         # Notion API client
│   ├── db.py             # Database adapters
│   └── cli.py            # CLI commands
├── config/
│   └── bridge.yaml       # Sync profiles
├── run_api.py            # Start Core API
├── run_sandbox.py        # Start Sandbox API
├── requirements.txt      # Dependencies
├── BRIDGE_SPEC.md        # Integration spec
└── COORDINATION_RESPONSE.md  # Main App coordination
```

---

## 🔗 Integration with Main App

See `BRIDGE_SPEC.md` for full integration details.

### Quick Integration

```javascript
// Nuxt server route example
export default defineEventHandler(async (event) => {
  const jwt = getCookie(event, 'sb-access-token')
  
  const templates = await $fetch('http://localhost:3000/api/templates', {
    headers: { Authorization: `Bearer ${jwt}` }
  })
  
  return templates
})
```

---

## 🛠️ CLI Usage

```bash
# Export Notion database to Supabase
python -m cb.cli export notion-to-db \
  --database-id YOUR_NOTION_DB_ID \
  --target supabase \
  --connection "https://xxx.supabase.co|your-key" \
  --table my_table

# Dry run (preview only)
python -m cb.cli export notion-to-db \
  --database-id YOUR_NOTION_DB_ID \
  --dry-run
```

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
