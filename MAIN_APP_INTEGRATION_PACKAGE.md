# Main App Integration Guide

**Main App connects DIRECTLY to Supabase - Bridge is NOT required to run!**

---

## Architecture (Correct)

```
┌─────────────────────────────────────────────────────────────────┐
│                         SUPABASE                                │
│         (The database - source of truth, always on)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
┌─────────────────────┐           ┌─────────────────────┐
│     MAIN APP        │           │   CURSOR BRIDGE     │
│  (User-facing app)  │           │  (Admin tool ONLY)  │
│                     │           │                     │
│  - Queries Supabase │           │  - Syncs Notion     │
│    DIRECTLY         │           │  - Creates tables   │
│  - Auth, sessions,  │           │  - Excel scripts    │
│    check-ins        │           │  - Content authoring│
│                     │           │                     │
│  ALWAYS RUNNING     │           │  RUNS WHEN NEEDED   │
└─────────────────────┘           └─────────────────────┘
```

**Bridge is a standalone admin utility. Main App does NOT call Bridge APIs.**

---

## What Main App Needs

Main App needs ONE thing: **Supabase connection**

### 1. Install Supabase Client

```bash
npm install @supabase/supabase-js
```

### 2. Create composables/useSupabase.ts

```typescript
// composables/useSupabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.SUPABASE_URL || 'https://dshwdxhycdrtemaxrupu.supabase.co'
const supabaseKey = process.env.SUPABASE_ANON_KEY || 'your-anon-key'

export const supabase = createClient(supabaseUrl, supabaseKey)

export function useSupabase() {
  
  // =========================================================================
  // Techniques Library
  // =========================================================================
  
  async function getTechniques(category?: string) {
    let query = supabase.from('techniques').select('*')
    if (category) query = query.eq('technique_category', category)
    const { data, error } = await query
    if (error) throw error
    return data
  }
  
  async function getTechniqueById(id: string) {
    const { data, error } = await supabase
      .from('techniques')
      .select('*')
      .eq('id', id)
      .single()
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Lenses
  // =========================================================================
  
  async function getLenses() {
    const { data, error } = await supabase
      .from('lens_definitions')
      .select('*')
      .order('sort_order')
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Personas
  // =========================================================================
  
  async function getPersonas() {
    const { data, error } = await supabase
      .from('archetypal_personas')
      .select('*')
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Knowledge Bases
  // =========================================================================
  
  async function getKnowledgeBases() {
    const { data, error } = await supabase
      .from('knowledge_bases')
      .select('*')
      .eq('is_active', true)
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Session Blueprints
  // =========================================================================
  
  async function getSessionBlueprints() {
    const { data, error } = await supabase
      .from('session_blueprints')
      .select('*')
    if (error) throw error
    return data
  }
  
  async function getBlueprintById(id: string) {
    const { data, error } = await supabase
      .from('session_blueprints')
      .select(`
        *,
        blueprint_steps(*, techniques(*)),
        blueprint_cues(*)
      `)
      .eq('id', id)
      .single()
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Timing & Narration
  // =========================================================================
  
  async function getTimingPresets() {
    const { data, error } = await supabase
      .from('timing_presets')
      .select('*')
      .order('total_duration_min')
    if (error) throw error
    return data
  }
  
  async function getNarrationStyles() {
    const { data, error } = await supabase
      .from('narration_styles')
      .select('*')
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Controls & Dashboard
  // =========================================================================
  
  async function getControlDefinitions() {
    const { data, error } = await supabase
      .from('control_definitions')
      .select('*')
    if (error) throw error
    return data
  }
  
  async function getControlPacks() {
    const { data, error } = await supabase
      .from('control_packs')
      .select('*')
    if (error) throw error
    return data
  }
  
  async function getDashboardTemplates() {
    const { data, error } = await supabase
      .from('dashboard_templates')
      .select('*')
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Programme Profiles
  // =========================================================================
  
  async function getProgrammeProfiles() {
    const { data, error } = await supabase
      .from('programme_profiles')
      .select('*')
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // User Check-ins
  // =========================================================================
  
  async function saveCheckin(userId: string, controlValues: Record<string, any>) {
    const { data, error } = await supabase
      .from('user_checkins')
      .insert({
        user_id: userId,
        checkin_date: new Date().toISOString().split('T')[0],
        control_values: controlValues
      })
      .select()
      .single()
    if (error) throw error
    return data
  }
  
  async function getCheckins(userId: string, limit = 30) {
    const { data, error } = await supabase
      .from('user_checkins')
      .select('*')
      .eq('user_id', userId)
      .order('checkin_date', { ascending: false })
      .limit(limit)
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Session Generation (runs in Main App, not Bridge!)
  // =========================================================================
  
  async function saveSessionRun(sessionData: {
    user_id: string
    blueprint_id?: string
    timing_preset_id?: string
    narration_style_id?: string
    selected_lens?: string
    generated_output: any
  }) {
    const { data, error } = await supabase
      .from('session_runs')
      .insert(sessionData)
      .select()
      .single()
    if (error) throw error
    return data
  }
  
  // =========================================================================
  // Generic Query
  // =========================================================================
  
  async function queryTable(table: string, options?: {
    select?: string
    eq?: Record<string, any>
    limit?: number
  }) {
    let query = supabase.from(table).select(options?.select || '*')
    
    if (options?.eq) {
      for (const [key, value] of Object.entries(options.eq)) {
        query = query.eq(key, value)
      }
    }
    
    if (options?.limit) query = query.limit(options.limit)
    
    const { data, error } = await query
    if (error) throw error
    return data
  }
  
  return {
    // Client
    supabase,
    
    // Techniques
    getTechniques,
    getTechniqueById,
    
    // Lenses & Personas
    getLenses,
    getPersonas,
    getKnowledgeBases,
    
    // Sessions
    getSessionBlueprints,
    getBlueprintById,
    getTimingPresets,
    getNarrationStyles,
    saveSessionRun,
    
    // Dashboard
    getControlDefinitions,
    getControlPacks,
    getDashboardTemplates,
    getProgrammeProfiles,
    
    // User Data
    saveCheckin,
    getCheckins,
    
    // Generic
    queryTable
  }
}
```

### 3. Environment Variables

```env
# .env (Main App)
SUPABASE_URL=https://dshwdxhycdrtemaxrupu.supabase.co
SUPABASE_ANON_KEY=your-public-anon-key
```

---

## Example Usage

```vue
<script setup lang="ts">
const { getTechniques, getLenses, getSessionBlueprints } = useSupabase()

// Get all breathing techniques
const breathwork = await getTechniques('breathwork')

// Get available lenses
const lenses = await getLenses()

// Get session blueprints
const blueprints = await getSessionBlueprints()
</script>
```

---

## Sessions Panel Example

```vue
<template>
  <div class="sessions-panel">
    <h2>Create Session</h2>
    
    <!-- Lens Dropdown -->
    <select v-model="selectedLens">
      <option v-for="lens in lenses" :key="lens.lens_slug" :value="lens.lens_slug">
        {{ lens.icon }} {{ lens.lens_name }}
      </option>
    </select>
    
    <!-- Duration Dropdown -->
    <select v-model="selectedTiming">
      <option v-for="timing in timings" :key="timing.id" :value="timing.id">
        {{ timing.preset_name }} ({{ timing.total_duration_min }} min)
      </option>
    </select>
    
    <!-- Persona Dropdown -->
    <select v-model="selectedPersona">
      <option v-for="persona in personas" :key="persona.id" :value="persona.id">
        {{ persona.persona }}
      </option>
    </select>
    
    <!-- Blueprint Selector -->
    <div class="blueprint-grid">
      <div 
        v-for="bp in blueprints" 
        :key="bp.id"
        :class="{ selected: selectedBlueprint === bp.id }"
        @click="selectedBlueprint = bp.id"
      >
        {{ bp.blueprint_name }}
      </div>
    </div>
    
    <!-- Technique Browser -->
    <div class="technique-browser">
      <div v-for="tech in techniques" :key="tech.id" class="technique-card">
        <strong>{{ tech.technique }}</strong>
        <span>{{ tech.technique_category }}</span>
        <span>{{ tech.intensity_band }}</span>
      </div>
    </div>
    
    <button @click="generateSession">Generate Session</button>
  </div>
</template>

<script setup lang="ts">
const { 
  getLenses, 
  getTimingPresets, 
  getPersonas, 
  getSessionBlueprints,
  getTechniques,
  getBlueprintById
} = useSupabase()

const lenses = ref([])
const timings = ref([])
const personas = ref([])
const blueprints = ref([])
const techniques = ref([])

const selectedLens = ref('hybrid')
const selectedTiming = ref(null)
const selectedPersona = ref(null)
const selectedBlueprint = ref(null)

onMounted(async () => {
  // Load all dropdown data directly from Supabase
  lenses.value = await getLenses()
  timings.value = await getTimingPresets()
  personas.value = await getPersonas()
  blueprints.value = await getSessionBlueprints()
  techniques.value = await getTechniques()
})

async function generateSession() {
  // Get full blueprint with steps
  const blueprint = await getBlueprintById(selectedBlueprint.value)
  
  // Build session locally (Main App generates sessions, not Bridge!)
  const session = {
    blueprint,
    lens: selectedLens.value,
    timing: timings.value.find(t => t.id === selectedTiming.value),
    persona: personas.value.find(p => p.id === selectedPersona.value),
    // ... build your session logic here
  }
  
  // Navigate to player or emit event
}
</script>
```

---

## Available Tables in Supabase

Query these DIRECTLY from Main App:

| Table | Description |
|-------|-------------|
| `techniques` | All breathing/meditation/movement techniques |
| `lens_definitions` | Available explanation lenses (western, tcm, etc) |
| `archetypal_personas` | AI voice/tone styles |
| `knowledge_bases` | Literature sources |
| `session_blueprints` | Pre-built session templates |
| `blueprint_steps` | Steps within blueprints |
| `blueprint_cues` | Timing cues within blueprints |
| `timing_presets` | Duration options |
| `narration_styles` | Voice pacing options |
| `control_definitions` | Dashboard controls |
| `control_packs` | Control groupings |
| `programme_profiles` | Wellness programmes |
| `breath_library` | Breathing techniques |
| `movements_system` | Movement library |
| `evidence_sources` | Scientific references |

---

## What is CursorBridge For Then?

**CursorBridge is an ADMIN TOOL, not a runtime dependency.**

Use it when you need to:
- Sync content from Notion → Supabase
- Create new database tables
- Run Excel automation scripts
- Seed initial data
- Author/edit content

**You run it manually when needed. Main App ignores it.**

---

## Summary

| Task | Who Does It |
|------|-------------|
| Query techniques, lenses, personas | **Main App → Supabase directly** |
| Generate sessions | **Main App (locally)** |
| Save user check-ins | **Main App → Supabase directly** |
| Auth, profiles | **Main App → Supabase directly** |
| Sync Notion databases | CursorBridge (admin, manual) |
| Create/update schemas | CursorBridge (admin, manual) |
| Excel scripts | CursorBridge (admin, manual) |

**Main App is fully independent. Bridge is optional admin tooling.**
