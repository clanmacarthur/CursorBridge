# CursorBridge -> Main App Handoff

**Share this document with the Main App AI**

---

## What's Ready

CursorBridge APIs are running and ready for integration:

| Service | Port | Status |
|---------|------|--------|
| Core API | 3000 | Running |
| Sandbox API | 3001 | Running |

---

## NEW: LENS SYSTEM (14 Lenses, Infinite Expansion)

The lens system enables multi-paradigm session explanations. **Users can eventually create their own lenses.**

### Available Lenses

| Slug | Name | Icon | Paradigm |
|------|------|------|----------|
| `western` | Western Scientific | 🔬 | scientific |
| `clinical` | Clinical/Medical | 🏥 | scientific |
| `athletic` | Athletic/Performance | 🏃 | performance |
| `tcm` | Traditional Chinese Medicine | ☯️ | traditional |
| `ayurvedic` | Ayurvedic | 🕉️ | traditional |
| `yogic` | Yogic/Tantric | 🧘 | traditional |
| `somatic` | Somatic/Body-Based | 🫀 | somatic |
| `polyvagal` | Polyvagal-Informed | 🌊 | somatic |
| `spiritual` | Spiritual/Energetic | ✨ | spiritual |
| `contemplative` | Contemplative/Mindfulness | 🪷 | spiritual |
| `plain` | Plain Language | 💬 | practical |
| `motivational` | Motivational/Coaching | 🎯 | practical |
| `hybrid` | Hybrid/Adaptive | 🔄 | adaptive |
| `personalized` | Personalized (user-defined) | 👤 | adaptive |

### Lens Registry Endpoints

```bash
# List all lenses
GET http://localhost:3001/sandbox/lenses

# Get specific lens
GET http://localhost:3001/sandbox/lenses/somatic

# Get all lens explanations for a technique
GET http://localhost:3001/sandbox/techniques/1/lenses

# Update user lens preferences
POST http://localhost:3001/sandbox/user/lens-preferences

# Update context for AI lens selection
POST http://localhost:3001/sandbox/user/lens-context
```

### Quick Test: Flagship Lens Demo

```bash
# Get demo info
curl http://localhost:3001/sandbox/demo/lens-test

# Generate with Western lens
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=western"

# Generate with TCM lens
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=tcm"

# Generate with Hybrid lens (both)
curl -X POST "http://localhost:3001/sandbox/demo/generate-flagship?lens=hybrid"
```

### Session Generation with Lens

```bash
POST http://localhost:3001/sandbox/generate-session
Content-Type: application/json

{
  "user_id": "user-uuid",
  "programme_profile_id": "profile-id",
  "session_template_id": "template-id",
  "duration_min": 30,
  "lens": "hybrid",
  "explanation_level": "plain"
}
```

### New Tables

| Table | Rows | Purpose |
|-------|------|---------|
| `techniques` | 4 | Core techniques with lens templates |
| `evidence_sources` | 4 | Research/traditional references |

Query them:
```bash
GET /api/query/techniques
GET /api/query/evidence_sources
GET /sandbox/techniques
GET /sandbox/techniques?lens=tcm
GET /sandbox/evidence-sources
```

---

## Automation Backbone (Seeded)

The engine tables are populated and ready:

| Table | Rows | Purpose |
|-------|------|---------|
| `control_definitions` | 15 | Every knob/tick the UI can render |
| `control_packs` | 7 | Curated bundles (Daily Essentials, Insomnia, etc.) |
| `derived_metrics` | 6 | Computed scores (Sleep Adequacy, Recovery, etc.) |
| `coupling_rules` | 8 | How controls influence each other |

Query them:
```bash
GET /api/query/control_definitions
GET /api/query/control_packs
GET /api/query/derived_metrics
GET /api/query/coupling_rules
```

---

## Endpoints to Use

### 1. Dashboard Templates

```bash
GET http://localhost:3000/api/templates
GET http://localhost:3000/api/templates?category=wellness
GET http://localhost:3000/api/templates/{template_id}
```

**Available templates:**
- `daily-wellness-check` - Mood, sleep, energy, stress sliders + chart
- `breath-movement` - Session player + feeling rating
- `meditation-journal` - Timer, quality, technique, notes, stats
- `nutrition-tracker` - Hydration, meals, protein
- `sleep-tracker` - Sleep times, quality, energy

### 2. Content Queries

```bash
GET http://localhost:3000/api/query/programme_profiles?limit=10
GET http://localhost:3000/api/query/breath_library?limit=10
GET http://localhost:3000/api/query/movements_system?limit=10
GET http://localhost:3000/api/query/session_templates?limit=10
GET http://localhost:3000/api/query/archetypal_personas?limit=10
```

### 3. Field Documentation

```bash
GET http://localhost:3000/api/schema/programme_profiles
GET http://localhost:3000/api/schema/breath_library
GET http://localhost:3000/api/schema/movements_system
```

### 4. Session Generation

```bash
POST http://localhost:3001/sandbox/generate-session
Content-Type: application/json

{
  "user_id": "user-uuid",
  "template_id": "session-template-id-from-supabase",
  "duration_min": 15,
  "preferences": {}
}
```

**Response format (with lens system):**
```json
{
  "id": "session-uuid",
  "name": "Session Name",
  "duration_minutes": 15,
  "lens": "hybrid",
  "explanation_level": "plain",
  "sections": [
    {
      "type": "movement",
      "name": "TCM Liver Flow Qigong (Beginner)",
      "duration_minutes": 15,
      "instructions": "[Western] Gentle movement + breathing... [TCM] Supports Liver Qi flow...",
      "lens_explanation": "Combined lens explanation",
      "lens_explanation_western": "Gentle movement + breathing can reduce muscle guarding...",
      "lens_explanation_tcm": "Supports Liver Qi flow: smooth movement, soft eyes...",
      "mechanism_notes": "Gentle mobility + breath synchrony; good for tension patterns.",
      "technique_id": "technique-uuid",
      "cues": ["0:00 - Begin", "7:00 - Find rhythm", "14:00 - Transition"]
    },
    {
      "type": "meditation",
      "name": "NSDR (Non-Sleep Deep Rest)",
      "duration_minutes": 15,
      "instructions": "[Western] Shifts attention inward... [TCM] Supports Shen settling...",
      "lens_explanation_western": "This practice shifts attention inward...",
      "lens_explanation_tcm": "In TCM language, this supports Shen settling...",
      "cues": ["0:00 - Begin", "14:00 - Transition"]
    }
  ],
  "safety_warnings": []
}
```

---

## 🔐 Authentication

Include Supabase JWT in all requests:

```
Authorization: Bearer <supabase_access_token>
```

CORS is configured for:
- `http://localhost:8080` (Main App dev)
- `https://yourdomain.com` (update when known)

---

## 📊 Block Types Registry

Both projects should support these block types:

### Input Blocks
| Type | Config |
|------|--------|
| `slider` | min, max, step, default, labels |
| `number` | min, max, unit |
| `text` | maxLength, placeholder, multiline |
| `toggle` | items: [{id, label}] |
| `select` | options: [{value, label}] |
| `date` | format |
| `time` | default |
| `timer` | default_minutes, presets |
| `button` | label, action |

### Output Blocks
| Type | Config |
|------|--------|
| `chart` | chartType, dataSource, groupBy |
| `timeline` | dataSource, groupBy, showLast |
| `stat` | aggregation, dataSource, unit |
| `gauge` | min, max, thresholds |
| `list` | dataSource, template |
| `session_player` | showTimer, showInstructions |

---

## 🔄 Realtime Events

Subscribe to Supabase table `sync_events` for content updates:

```javascript
supabase
  .channel('content-updates')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'sync_events'
  }, (payload) => {
    // payload.new = { type, table, record_id, timestamp }
  })
  .subscribe()
```

---

## 📁 Table Ownership

### CursorBridge owns (content):
- programme_profiles
- breath_library
- movements_system
- session_templates
- archetypal_personas
- attribute_taxonomy
- safety_rules
- nutrition_and_food
- + 17 more content tables

### Main App owns (user data):
- user_profiles
- dashboards
- dashboard_blocks
- block_data
- contracts
- marketplace_listings
- purchases
- automations

---

## 🚀 Quick Test

```bash
# Health check
curl http://localhost:3000/

# Get templates
curl http://localhost:3000/api/templates

# Get programme profiles
curl http://localhost:3000/api/query/programme_profiles?limit=3

# Get breath library
curl http://localhost:3000/api/query/breath_library?limit=3
```

---

## 📝 Nuxt Server Route Example

```typescript
// server/api/bridge/templates.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token = getCookie(event, 'sb-access-token')
  
  const response = await $fetch('http://localhost:3000/api/templates', {
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  })
  
  return response
})
```

```typescript
// server/api/bridge/session.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const token = getCookie(event, 'sb-access-token')
  
  const session = await $fetch('http://localhost:3001/sandbox/generate-session', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body
  })
  
  return session
})
```

---

## ❓ Questions?

Reference docs:
- `BRIDGE_SPEC.md` - Full integration specification
- `COORDINATION_RESPONSE.md` - Detailed API documentation
- `README.md` - Project overview

---

## VERIFIED WORKING (Test Results)

All endpoints tested and working:

| Endpoint | Status | Sample Data |
|----------|--------|-------------|
| `GET /api/query/control_definitions` | OK | 15 controls |
| `GET /api/query/control_packs` | OK | 7 packs |
| `GET /api/query/coupling_rules` | OK | 8 rules |
| `GET /api/query/derived_metrics` | OK | 6 metrics |
| `GET /api/templates` | OK | 5 templates |
| `POST /sandbox/generate-session` | OK | Full session with sections |

### Sample Session Output

```json
{
  "id": "uuid",
  "name": "Movements",
  "duration_minutes": 15,
  "persona_style": "Alan Watts-like",
  "sections": [
    {
      "type": "breathwork",
      "name": "Counting Breath",
      "duration_minutes": 2,
      "instructions": "Begin with Counting Breath...",
      "cues": ["0:00 - Begin", "0:30 - Deepen", "1:00 - Transition"]
    },
    {
      "type": "movement",
      "name": "Qigong Silk Reeling",
      "duration_minutes": 7,
      "instructions": "Practice Qigong Silk Reeling...",
      "cues": ["0:00 - Begin", "3:00 - Find rhythm", "5:00 - Slow down"]
    },
    {
      "type": "breathwork",
      "name": "Physiological Sigh",
      "duration_minutes": 6,
      "instructions": "Return to natural breath...",
      "cues": ["0:00 - Natural breathing", "5:00 - Return", "6:00 - Complete"]
    }
  ],
  "safety_warnings": [
    "Ground Before Visualization",
    "Post-Session No Driving",
    "Avoid Major Decisions Post-Session"
  ]
}
```

---

## MAIN APP BUILD CHECKLIST

### Phase 1: Setup
- [ ] Create Nuxt 3 project with Supabase module
- [ ] Configure Supabase Auth (email + social)
- [ ] Set up server routes to proxy CursorBridge APIs

### Phase 2: Core Features
- [ ] User registration/login (Supabase Auth)
- [ ] Profile selection page (fetch from `/api/query/programme_profiles`)
- [ ] Dashboard builder (fetch from `/api/templates`, `/api/query/control_packs`)
- [ ] Check-in form (save to `user_checkins` table)
- [ ] Session player (call `/sandbox/generate-session`)

### Phase 3: Adaptive Engine
- [ ] Apply coupling rules to check-in data
- [ ] Calculate derived metrics
- [ ] Display progress/insights

### Phase 4: Polish
- [ ] Subscribe to Realtime for content updates
- [ ] Add user weight overrides
- [ ] Questionnaire flow for profile assignment

---

## FUTURE VISION: Adaptive AI Companion

See `ADAPTIVE_AI_VISION.md` for the full roadmap. Key concepts:

### 1. Infinite User-Created Lenses
Users will create their own explanatory frameworks by blending existing lenses.

### 2. AI-Driven Lens Selection
The AI selects lenses based on:
- Current mood/energy (from check-ins)
- Time of day
- User history and patterns
- Explicit preferences

### 3. Conversational Questionnaire
Not static forms—dynamic dialogue that adapts to user receptivity.

### 4. Permission-Based Escalation
Trigger system with buddy/family notifications (user-controlled):
- Low mood for 5 days → notify buddy
- Crisis language → immediate resources + designated contact

### 5. Eternal Companion
AI learns patterns over months/years and proactively suggests interventions.

---

## CONTACT

CursorBridge APIs:
- Core API: http://localhost:3000
- Sandbox API: http://localhost:3001
- GitHub: https://github.com/clanmacarthur/CursorBridge

Key docs:
- `LENS_SYSTEM_SETUP.md` - How to test lenses
- `ADAPTIVE_AI_VISION.md` - Full adaptive AI roadmap
- `lens_registry_schema.sql` - Lens registry SQL

Ready to build!



