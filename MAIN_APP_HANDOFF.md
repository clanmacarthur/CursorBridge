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

See `ADAPTIVE_AI_VISION.md` for the full roadmap.

### The Three-Pillar System

| Pillar | What it controls | Count |
|--------|------------------|-------|
| **Lens** | HOW to explain | 14 lenses |
| **Persona** | WHO is speaking | 18 personas |
| **Knowledge Base** | WHAT sources inform | 18 knowledge bases |

### The Four Meta-Dimensions

| Dimension | Range | What AI decides |
|-----------|-------|-----------------|
| **Scope** | Narrow ↔ Wide | How widely to look for solutions |
| **Depth** | Surface ↔ Deep | How deeply to work (behavioral → existential) |
| **Source** | Individual ↔ Collective | Where to draw insights from |
| **Confidence** | Established ↔ Frontier | How proven the approach is |

### Meta-Lens Presets

| Preset | Description | Best For |
|--------|-------------|----------|
| 🛡️ Safe Start | Conservative, evidence-based | New users |
| 🔭 Open Explorer | Curious, adjacent domains | Explorers |
| 🌊 Deep Diver | Narrow but deep | Practitioners |
| 🔀 Synthesizer | Cross-domain, collective wisdom | Tried everything |
| 🚀 Frontier Explorer | Experimental, pioneering | Advanced + support |

### Experimental/Beta Flags

When AI goes beyond established practice:
- `experimental` flag shown to user
- Disclaimer text displayed
- User consent logged
- Feedback collected

### Cross-Domain Transfer

AI can map techniques across fields:
- Athletic recovery → Burnout management
- Addiction tools → Grief processing
- Trauma somatic → Performance anxiety

### User-Created Technique Blends

Users can create their own techniques by blending existing ones with personal modifications.

### Full Transparency

Users can always ask "Why did you suggest this?" and get the full reasoning chain.

---

## 🎛️ SESSIONS PANEL: DROPDOWN & LIBRARY SETUP

This section explains how to populate all dropdowns and library browsers in the Sessions Panel.

### Master Library Endpoints

| Library | Endpoint | Use For |
|---------|----------|---------|
| **Techniques** | `GET /api/query/techniques` | All breathwork, meditation, movement |
| **Session Blueprints** | `GET /api/query/session_blueprints` | Pre-built session recipes |
| **Timing Presets** | `GET /api/query/timing_presets` | Duration options (10/20/30/45/60 min) |
| **Narration Styles** | `GET /api/query/narration_styles` | Voice/pacing options |
| **Lenses** | `GET /sandbox/lenses` | Explanation paradigms (Western, TCM, etc.) |
| **Personas** | `GET /api/query/archetypal_personas` | AI voice/personality |
| **Knowledge Bases** | `GET /api/query/knowledge_bases` | Source traditions |
| **Programme Profiles** | `GET /api/query/programme_profiles` | User wellness profiles |
| **Breath Library** | `GET /api/query/breath_library` | Breathing techniques |
| **Movement Library** | `GET /api/query/movements_system` | Movement practices |

### Dropdown Population Examples

```typescript
// 1. TECHNIQUE SELECTOR
const techniques = await $fetch('/api/query/techniques')
// Returns: { technique, technique_category, objective, intensity_band, lens_explanation_western, lens_explanation_tcm }

// 2. BLUEPRINT SELECTOR (pre-built sessions)
const blueprints = await $fetch('/api/query/session_blueprints?is_platform_example=eq.true')
// Returns: { blueprint_name, description, safety_level, tags }

// 3. TIMING DROPDOWN
const timings = await $fetch('/api/query/timing_presets')
// Returns: { preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct }

// 4. NARRATION STYLE DROPDOWN
const styles = await $fetch('/api/query/narration_styles')
// Returns: { style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level }

// 5. LENS SELECTOR
const lenses = await $fetch('http://localhost:3001/sandbox/lenses')
// Returns: { lenses: [{ lens_slug, lens_name, icon, paradigm_family }] }

// 6. PERSONA SELECTOR
const personas = await $fetch('/api/query/archetypal_personas')
// Returns: { persona, lineage_influence, cognitive_style, language_tone, metaphor_density }
```

### Sessions Panel UI Components

```vue
<template>
  <!-- BLUEPRINT QUICK SELECT -->
  <select v-model="selectedBlueprint">
    <option v-for="bp in blueprints" :key="bp.id" :value="bp.id">
      {{ bp.blueprint_name }} ({{ bp.description }})
    </option>
  </select>

  <!-- TIMING DROPDOWN -->
  <select v-model="selectedTiming">
    <option v-for="t in timings" :key="t.id" :value="t.id">
      {{ t.preset_name }} ({{ t.total_duration_min }} min)
    </option>
  </select>

  <!-- LENS DROPDOWN -->
  <select v-model="selectedLens">
    <option v-for="lens in lenses" :key="lens.lens_slug" :value="lens.lens_slug">
      {{ lens.icon }} {{ lens.lens_name }}
    </option>
  </select>

  <!-- PERSONA DROPDOWN -->
  <select v-model="selectedPersona">
    <option v-for="p in personas" :key="p.id" :value="p.id">
      {{ p.persona }} ({{ p.cognitive_style }})
    </option>
  </select>

  <!-- NARRATION STYLE DROPDOWN -->
  <select v-model="selectedNarrationStyle">
    <option v-for="ns in narrationStyles" :key="ns.id" :value="ns.id">
      {{ ns.style_name }} - {{ ns.voice_tone }} ({{ ns.reading_pace_wpm }} WPM)
    </option>
  </select>

  <!-- TECHNIQUE BROWSER (expandable library) -->
  <div class="technique-library">
    <div v-for="category in techniqueCategories" :key="category">
      <h4>{{ category }}</h4>
      <div v-for="tech in techniquesBy(category)" :key="tech.id" @click="addTechnique(tech)">
        {{ tech.technique }} - {{ tech.intensity_band }}
      </div>
    </div>
  </div>

  <!-- GENERATE BUTTON -->
  <button @click="generateSession">Generate Session</button>
</template>
```

### Generate Session Call

```typescript
async function generateSession() {
  const session = await $fetch('http://localhost:3001/sandbox/generate-session', {
    method: 'POST',
    body: {
      blueprint_id: selectedBlueprint,
      timing_preset_id: selectedTiming,
      lens: selectedLens,
      persona_id: selectedPersona,
      narration_style_id: selectedNarrationStyle,
      user_id: currentUser.id
    }
  })
  
  // session contains: { id, name, duration_minutes, sections[], lens, persona_style }
  displaySession(session)
}
```

### Library Browser Component

```vue
<template>
  <div class="library-browser">
    <tabs>
      <tab name="Techniques">
        <search v-model="searchTerm" />
        <filter :options="['breathwork', 'meditation', 'movement']" v-model="categoryFilter" />
        <grid :items="filteredTechniques">
          <template #item="{ item }">
            <card>
              <h3>{{ item.technique }}</h3>
              <badge>{{ item.technique_category }}</badge>
              <badge :color="intensityColor(item.intensity_band)">{{ item.intensity_band }}</badge>
              <p>{{ item.objective }}</p>
              <expand-panel title="Western Explanation">
                {{ item.lens_explanation_western }}
              </expand-panel>
              <expand-panel title="TCM Explanation">
                {{ item.lens_explanation_tcm }}
              </expand-panel>
            </card>
          </template>
        </grid>
      </tab>
      
      <tab name="Blueprints">
        <grid :items="blueprints">
          <template #item="{ item }">
            <card @click="selectBlueprint(item)">
              <h3>{{ item.blueprint_name }}</h3>
              <p>{{ item.description }}</p>
              <tags :items="item.tags" />
            </card>
          </template>
        </grid>
      </tab>
      
      <tab name="Lenses">
        <grid :items="lenses">
          <template #item="{ item }">
            <card @click="selectLens(item.lens_slug)">
              <span class="icon">{{ item.icon }}</span>
              <h3>{{ item.lens_name }}</h3>
              <p>{{ item.lens_description }}</p>
            </card>
          </template>
        </grid>
      </tab>
      
      <tab name="Knowledge Bases">
        <grid :items="knowledgeBases">
          <template #item="{ item }">
            <card>
              <span class="icon">{{ item.icon }}</span>
              <h3>{{ item.kb_name }}</h3>
              <p>{{ item.kb_description }}</p>
              <badge>{{ item.cultural_origin }}</badge>
            </card>
          </template>
        </grid>
      </tab>
    </tabs>
  </div>
</template>
```

### Current Content Counts

| Table | Count | Description |
|-------|-------|-------------|
| `techniques` | 22+ | Breathwork, meditation, movement |
| `session_blueprints` | 13+ | Pre-built session recipes |
| `timing_presets` | 5 | 10/20/30/45/60 min options |
| `narration_styles` | 7 | Temple Guide, Lab Coach, etc. |
| `lens_definitions` | 22+ | Western, TCM, Trauma-Informed, etc. |
| `archetypal_personas` | 20+ | Alan Watts, Clinical Guide, etc. |
| `knowledge_bases` | 31+ | Yoga Sutras, PubMed, Tarot, etc. |

---

## 📝 PERSONAL NOTE TO MAIN APP DEVELOPER

**Important context for integration:**

1. **Examples are just examples** - Any specific scenarios I describe (like "breathing techniques for anxiety") are illustrative, not requirements. The system is flexible.

2. **User browsing is key** - Users should be able to browse ALL libraries (techniques, lenses, personas, knowledge bases) not just pick from dropdowns.

3. **Lens switching is powerful** - Same session, different explanations. Let users toggle between Western/TCM/Hybrid on the fly.

4. **Everything is extensible** - Users will eventually create their own lenses, personas, and technique blends.

---

## 🚀 NEXT STEPS (Roadmap)

### Immediate (This Sprint)
- [ ] Main App implements Sessions Panel with dropdowns
- [ ] Technique library browser
- [ ] Lens selector in session player
- [ ] Blueprint quick-select

### Short Term
- [ ] User can toggle lens explanation during playback
- [ ] Save user lens/persona preferences
- [ ] Session history with lens used

### Medium Term: Famous Psychologist Personas
Add historical figures as AI personas:
- **Carl Jung** - Archetypal, shadow work, collective unconscious
- **Sigmund Freud** - Psychoanalytic, unconscious drives
- **William James** - Pragmatic, stream of consciousness
- **Carl Rogers** - Humanistic, unconditional positive regard
- **Fritz Perls** - Gestalt, present-moment awareness
- **Abraham Maslow** - Self-actualization, peak experiences
- **Viktor Frankl** - Logotherapy, meaning-focused

### Medium Term: User Knowledge Base Uploads
- [ ] User uploads PDFs, journals, notes
- [ ] AI learns from user-provided texts
- [ ] Private knowledge bases with permissions
- [ ] Custom lenses derived from user content

### Long Term: Expanded Domains
- [ ] Astrology integration (birth chart personalization)
- [ ] Tarot readings as session prompts
- [ ] I Ching hexagram guidance
- [ ] Mythology/archetype storytelling sessions

---

## CONTACT

CursorBridge APIs:
- Core API: http://localhost:3000
- Sandbox API: http://localhost:3001
- GitHub: https://github.com/clanmacarthur/CursorBridge

Key docs:
- `LENS_SYSTEM_SETUP.md` - How to test lenses
- `ADAPTIVE_AI_VISION.md` - Full adaptive AI roadmap
- `SESSION_GENERATION_RUNTIME_SPEC.md` - How to generate sessions

Ready to build!



