# 📦 CursorBridge → Main App Handoff

**Share this document with the Main App AI**

---

## ✅ What's Ready

CursorBridge APIs are running and ready for integration:

| Service | Port | Status |
|---------|------|--------|
| Core API | 3000 | ✅ Running |
| Sandbox API | 3001 | ✅ Running |

---

## 🔌 Endpoints to Use

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

**Response format:**
```json
{
  "id": "session-uuid",
  "name": "Session Name",
  "duration_minutes": 15,
  "sections": [
    {
      "type": "breathwork",
      "name": "Protocol Name",
      "duration_minutes": 2.5,
      "instructions": "Guidance text...",
      "cues": ["0:00 - Begin", "1:00 - Deepen"]
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

Ready to build! 🎯

