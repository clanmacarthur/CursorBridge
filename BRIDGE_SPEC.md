# CursorBridge ↔ Main App Coordination Spec

**Status:** COORDINATED ✅  
**Last Updated:** 2025-12-30

## Project Overview

| Component | Tech Stack | Port | Responsibilities |
|-----------|------------|------|------------------|
| **Main App** | Vue 3 + Nuxt 3 | 8080 (dev) / 443 (prod) | Dashboard editor, blocks, programmes, marketplace, user UI |
| **CursorBridge API** | Python + FastAPI | 3000 | Content sync, query, logging |
| **CursorBridge Sandbox** | Python + FastAPI | 3001 | Session generation, rule evaluation |
| **Shared Backend** | Supabase | - | PostgreSQL, Auth, Realtime |

---

## 1. Supabase Configuration

**ANSWER: SAME Supabase project**

- Project URL: `https://dshwdxhycdrtemaxrupu.supabase.co`
- Both projects connect to the same Supabase instance
- Auth is shared (Supabase Auth)
- Simplest architecture, no cross-project complexity

**Access pattern:**
- Main app: Full CRUD on user tables (dashboards, blocks, programmes)
- CursorBridge: Full CRUD on content tables (synced from Notion)
- Both can read each other's tables as needed

---

## 2. Table Ownership (Schema Split)

### Main App Owns (User/App Layer):
```sql
-- These tables are for the dashboard builder UI
dashboards, blocks, block_data, programmes, user_profiles, marketplace_listings
```

### CursorBridge Owns (Content Layer):
```sql
-- These tables are synced FROM Notion (25 tables, 599 rows currently)
attribute_taxonomy        -- 76 rows (capabilities, parameters)
programme_profiles        -- 14 rows (wellness programme definitions)
session_templates         -- 19 rows (session recipes)
dashboard_blocks          -- 19 rows (content block definitions)
safety_rules              -- 8 rows (contraindications, gating)
breath_library            -- 26 rows (breath protocols)
movements_system          -- 16 rows (movement practices)
archetypal_personas       -- 10 rows (AI persona styles)
rules_gating              -- 20 rows (rule engine)
-- ... plus 16 more content tables
```

**Key distinction:**
- Main app `blocks` = UI widget definitions (sliders, charts, etc.)
- CursorBridge `dashboard_blocks` = Content block definitions (what to show)

---

## 3. Content Bridge API Contract

### CursorBridge Exposes (Python FastAPI):

**Already implemented:**
```
GET  /                              # Health check
GET  /api/query/{table}             # Query any content table
GET  /api/query/{table}/{id}        # Get by ID
POST /api/sync/notion               # Trigger Notion → Supabase sync
POST /api/logs/checkin              # Log user check-ins
```

**Sandbox endpoints (port 3001):**
```
POST /sandbox/generate-session      # Generate a session from template
POST /sandbox/build-dashboard       # Build dashboard blocks for user
GET  /sandbox/rules/evaluate        # Evaluate safety rules
```

### Main App Should Call:
```
# Get content for building dashboards
GET http://localhost:3000/api/query/programme_profiles
GET http://localhost:3000/api/query/attribute_taxonomy
GET http://localhost:3000/api/query/dashboard_blocks

# Generate sessions for users
POST http://localhost:3001/sandbox/generate-session
{
  "user_id": "uuid",
  "programme_profile_id": "uuid-or-notion-id",
  "session_template_id": "uuid-or-notion-id",
  "duration_min": 20
}

# Build dashboard content for user
POST http://localhost:3001/sandbox/build-dashboard
{
  "user_id": "uuid",
  "programme_profile_id": "uuid-or-notion-id"
}
```

### CursorBridge Needs From Main App:
```
# User authentication (validate JWT)
GET /api/auth/validate  # Returns user_id, roles

# Store generated sessions
POST /api/sessions      # Main app stores session history

# Read user preferences
GET /api/users/{id}/preferences
```

---

## 4. Authentication Handoff

**ANSWER: Shared Supabase Auth (Option B)**

Both projects use the same Supabase project, so:
- Users log in via Main App (Nuxt)
- Main App gets Supabase JWT
- JWT is passed to CursorBridge API in Authorization header
- CursorBridge validates JWT using same Supabase keys

**Token format:** Standard Supabase JWT
**Required claims:** `sub` (user_id), `email`, `role`

**Implementation in CursorBridge:**
```python
from supabase import create_client

def validate_token(token: str) -> dict:
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    user = client.auth.get_user(token)
    return {"user_id": user.id, "email": user.email}
```

---

## 5. Block Type Registry

**CLARIFICATION NEEDED:**

The Main App's "blocks" (UI widgets) are DIFFERENT from CursorBridge's "dashboard_blocks" (content definitions).

**Main App Block Types (UI Layer):**
```typescript
// These render the UI
type InputBlockType = 'slider' | 'number' | 'text' | 'toggle' | 'select' | 'date'
type OutputBlockType = 'timeline' | 'chart' | 'gauge' | 'stat' | 'list'
```

**CursorBridge Block Types (Content Layer):**
```python
# These define WHAT to show (from Notion)
block_types = ['Metrics', 'Checkboxes', 'Mixed', 'Info', 'Tracker']

# Our blocks have:
# - Required attributes (from attribute_taxonomy)
# - Linked programme profiles
# - Display depth, strictness settings
```

**Recommendation:**
- Main App owns UI block types (how to render)
- CursorBridge provides content blocks (what to render)
- Main App maps content blocks → UI blocks based on `block_type`

---

## 6. Sandbox Execution Environment

**CursorBridge runs Python/FastAPI (NOT Deno/Edge Functions)**

Current capabilities:
- Session generation from templates
- Rule evaluation and safety gating
- Taxonomy expansion (attribute parent/child)
- Persona-style script generation

**Not currently supported:**
- User-defined functions (could add via restricted eval)
- Real-time processing (batch only)

**If user functions needed:**
- Could add Supabase Edge Functions (Deno) as a separate layer
- CursorBridge would call Edge Functions for user scripts

---

## 7. Event/Message Contract

**Recommendation: Supabase Realtime**

CursorBridge can publish to Supabase Realtime after sync:

```python
# After Notion sync completes
channel = client.channel('content_sync')
channel.send({
    'type': 'broadcast',
    'event': 'sync_complete',
    'payload': {
        'tables': ['attribute_taxonomy', 'programme_profiles', ...],
        'rows_updated': 599,
        'timestamp': '2025-12-30T...'
    }
})
```

**Main App subscribes:**
```typescript
const channel = supabase.channel('content_sync')
channel.on('broadcast', { event: 'sync_complete' }, (payload) => {
  // Refresh content caches
})
```

---

## Summary Answers

| Question | Answer |
|----------|--------|
| Same Supabase project? | **Yes** - same project, shared auth |
| Sandbox tech stack? | **Python + FastAPI** (ports 3000, 3001) |
| Who owns schema migrations? | **Split:** Main App owns user tables, CursorBridge owns content tables |
| Webhook vs Realtime? | **Supabase Realtime** for sync events |
| Can sandbox define custom block types? | **No** - block types come from Notion, Main App maps them to UI |

---

## Integration Flow (Confirmed)

```
User opens Main App (port 8080)
  → Authenticates via Supabase Auth
  → Main App stores JWT in cookie
  → User creates dashboard
  → User clicks "Add Programme Block"
  → Nuxt server route calls CursorBridge API (port 3000):
      GET localhost:3000/api/query/programme_profiles
      Header: Authorization: Bearer <supabase_jwt>
  → CursorBridge validates JWT, returns programmes
  → Main App displays in block selector
  → User picks programme → calls Sandbox (port 3001):
      POST localhost:3001/sandbox/generate-session
      Body: { programme_id, user_preferences }
  → Session injected into user's dashboard
```

---

## Realtime Events (content_updates channel)

CursorBridge publishes to `sync_events` table after Notion sync:

```json
{
  "type": "programme_updated" | "template_added" | "content_synced",
  "table": "programme_profiles",
  "record_id": "uuid-or-null",
  "timestamp": "2025-12-30T..."
}
```

Main App subscribes via Supabase Realtime to update UI reactively.

---

## CORS Configuration

CursorBridge allows requests from:
- `http://localhost:8080` (Main App dev)
- `https://yourdomain.com` (Main App prod - TBD)

---

## User Profile Schema (Main App Owns)

```sql
CREATE TABLE public.user_profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username text UNIQUE NOT NULL,
  display_name text,
  email text,
  avatar_url text,
  bio text,
  stripe_customer_id text,
  stripe_connect_account_id text,
  subscription_tier text DEFAULT 'free',
  preferences jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
```

---

## Status

| Task | Status |
|------|--------|
| Notion → Supabase sync | ✅ Done (25 tables, 599 rows) |
| Content Query API | ✅ Done (port 3000) |
| Session Generation | ✅ Done (port 3001) |
| Dashboard Builder | ✅ Done (port 3001) |
| JWT Validation | ✅ Done |
| CORS for Main App | ✅ Done |
| Realtime Publishing | ✅ Done |
| Main App Integration | ⏳ Waiting for Main App |

---

## API Endpoints Summary

### CursorBridge (http://localhost:3000)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/query/{table}` | Query content tables |
| POST | `/api/sync/notion` | Trigger Notion sync |
| POST | `/api/logs/checkin` | Log user check-ins |

### Sandbox (http://localhost:3001)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/sandbox/generate-session` | Generate wellness session |
| POST | `/sandbox/build-dashboard` | Build dashboard content |
| GET | `/sandbox/rules/evaluate` | Evaluate safety rules |


