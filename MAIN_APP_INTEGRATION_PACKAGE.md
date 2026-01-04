# CursorBridge Integration Package for Main App

**COMPLETE PACKAGE - All code inline, copy-paste ready**

---

## Quick Start Checklist

1. [ ] Add runtime config to `nuxt.config.ts`
2. [ ] Create `types/bridge.ts`
3. [ ] Create `composables/useBridge.ts`
4. [ ] Create 3 server routes in `server/api/bridge/`
5. [ ] Add SessionPlayer component (optional)
6. [ ] Test with `useBridge().queryTable('techniques')`

---

## STEP 1: Add to nuxt.config.ts

Add these runtime config values:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  // ... your existing config ...
  
  runtimeConfig: {
    // These are server-only (not exposed to client)
    cursorBridgeApi: 'http://localhost:3000',
    cursorBridgeSandbox: 'http://localhost:3001',
    
    public: {
      // Add any client-side config here if needed
    }
  }
})
```

---

## STEP 2: Create types/bridge.ts

Create this file for TypeScript types:

```typescript
// types/bridge.ts

// Control Definitions
export interface ControlDefinition {
  id: string
  control_name: string
  control_type: 'slider' | 'checkbox' | 'knob' | 'hybrid' | 'number' | 'text' | 'time'
  range_min?: number
  range_max?: number
  range_step?: number
  default_value?: number
  unit?: string
  label?: string
  description?: string
  is_required: boolean
  is_default: boolean
  completion_threshold?: number
}

// Control Packs
export interface ControlPack {
  id: string
  pack_name: string
  pack_slug: string
  description?: string
  category: 'wellness' | 'fitness' | 'nutrition' | 'sleep' | 'stress' | 'custom'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  is_default: boolean
}

// Dashboard Templates
export interface DashboardTemplate {
  id: string
  name: string
  description: string
  category: string
  icon: string
  blocks: TemplateBlock[]
}

export interface TemplateBlock {
  block_type: string
  config: Record<string, any>
  position: { x: number; y: number; w: number; h: number }
}

// Coupling Rules
export interface CouplingRule {
  id: string
  rule_name: string
  from_metric?: string
  to_metric?: string
  function_type: 'linear' | 'threshold' | 'conditional' | 'decay' | 'inverse' | 'step'
  direction: 'positive' | 'negative' | 'conditional'
  magnitude: number
  threshold_value?: number
}

// Derived Metrics
export interface DerivedMetric {
  id: string
  metric_name: string
  metric_slug: string
  formula_type: 'weighted_average' | 'sum' | 'min' | 'max' | 'custom'
  domain?: string
  output_min: number
  output_max: number
}

// Techniques
export interface Technique {
  id: string
  technique: string
  technique_category: string
  objective: string
  intensity_band: 'Low' | 'Medium' | 'High'
  lens_availability: string
  lens_explanation_western?: string
  lens_explanation_tcm?: string
  mechanism_notes?: string
  default_duration_min: number
}

// Lenses
export interface Lens {
  lens_slug: string
  lens_name: string
  lens_description?: string
  paradigm_family: string
  language_style: string
  icon: string
}

// Personas
export interface Persona {
  id: string
  persona: string
  lineage_influence?: string
  cognitive_style?: string
  language_tone?: string
  metaphor_density?: string
}

// Knowledge Bases
export interface KnowledgeBase {
  id: string
  kb_slug: string
  kb_name: string
  kb_type: string
  kb_description?: string
  cultural_origin?: string
  requires_permission: boolean
  icon: string
}

// Session Blueprints
export interface SessionBlueprint {
  id: string
  blueprint_name: string
  description?: string
  safety_level: string
  tags: string[]
  is_platform_example: boolean
}

// Timing Presets
export interface TimingPreset {
  id: string
  preset_name: string
  total_duration_min: number
  intro_pct: number
  technique_pct: number
  integration_pct: number
  outro_pct: number
}

// Narration Styles
export interface NarrationStyle {
  id: string
  style_name: string
  voice_tone: string
  reading_pace_wpm: number
}

// Session Generation
export interface SessionRequest {
  user_id: string
  programme_profile_id?: string
  session_template_id?: string
  blueprint_id?: string
  duration_min?: number
  lens?: 'western' | 'tcm' | 'hybrid' | string
  explanation_level?: 'plain' | 'clinical'
  persona_id?: string
  preferences?: Record<string, any>
}

export interface SessionOutput {
  id: string
  name: string
  duration_minutes: number
  lens: string
  persona_style?: string
  sections: SessionSection[]
  safety_warnings: string[]
  created_at?: string
}

export interface SessionSection {
  type: 'breathwork' | 'movement' | 'meditation' | 'transition'
  name: string
  duration_minutes: number
  instructions: string
  lens_explanation?: string
  lens_explanation_western?: string
  lens_explanation_tcm?: string
  mechanism_notes?: string
  audio_url?: string
  cues?: string[]
}

// Programme Profiles
export interface ProgrammeProfile {
  id: string
  notion_page_id: string
  programme_profile___title: string
  primary_doctrine___select?: string
  default_depth___select?: string
  default_strictness___select?: string
}

// User Check-in
export interface CheckinData {
  user_id: string
  checkin_date: string
  control_values: Record<string, number | boolean>
  derived_scores?: Record<string, number>
}
```

---

## STEP 3: Create composables/useBridge.ts

This is the main API helper:

```typescript
// composables/useBridge.ts

import type { 
  DashboardTemplate, 
  ControlDefinition, 
  ControlPack,
  CouplingRule,
  DerivedMetric,
  ProgrammeProfile,
  SessionRequest,
  SessionOutput,
  Technique,
  Lens,
  Persona,
  KnowledgeBase,
  SessionBlueprint,
  TimingPreset,
  NarrationStyle
} from '~/types/bridge'

export function useBridge() {
  
  // =========================================================================
  // Templates
  // =========================================================================
  
  async function getTemplates(category?: string) {
    const query = category ? `?category=${category}` : ''
    return await $fetch<{ count: number; templates: DashboardTemplate[] }>(
      `/api/bridge/templates${query}`
    )
  }
  
  async function getTemplate(id: string) {
    return await $fetch<DashboardTemplate>(`/api/bridge/templates/${id}`)
  }
  
  // =========================================================================
  // Controls & Packs
  // =========================================================================
  
  async function getControlDefinitions(limit = 100) {
    return await $fetch<{ table: string; count: number; data: ControlDefinition[] }>(
      `/api/bridge/query/control_definitions?limit=${limit}`
    )
  }
  
  async function getControlPacks() {
    return await $fetch<{ table: string; count: number; data: ControlPack[] }>(
      `/api/bridge/query/control_packs`
    )
  }
  
  // =========================================================================
  // Engine Data
  // =========================================================================
  
  async function getCouplingRules() {
    return await $fetch<{ table: string; count: number; data: CouplingRule[] }>(
      `/api/bridge/query/coupling_rules`
    )
  }
  
  async function getDerivedMetrics() {
    return await $fetch<{ table: string; count: number; data: DerivedMetric[] }>(
      `/api/bridge/query/derived_metrics`
    )
  }
  
  // =========================================================================
  // Profiles
  // =========================================================================
  
  async function getProgrammeProfiles() {
    return await $fetch<{ table: string; count: number; data: ProgrammeProfile[] }>(
      `/api/bridge/query/programme_profiles`
    )
  }
  
  // =========================================================================
  // TECHNIQUES & LENSES (New!)
  // =========================================================================
  
  async function getTechniques() {
    return await $fetch<{ table: string; count: number; data: Technique[] }>(
      `/api/bridge/query/techniques`
    )
  }
  
  async function getLenses() {
    return await $fetch<{ lenses: Lens[] }>('/api/bridge/lenses')
  }
  
  async function getPersonas() {
    return await $fetch<{ table: string; count: number; data: Persona[] }>(
      `/api/bridge/query/archetypal_personas`
    )
  }
  
  async function getKnowledgeBases() {
    return await $fetch<{ table: string; count: number; data: KnowledgeBase[] }>(
      `/api/bridge/query/knowledge_bases`
    )
  }
  
  async function getSessionBlueprints() {
    return await $fetch<{ table: string; count: number; data: SessionBlueprint[] }>(
      `/api/bridge/query/session_blueprints`
    )
  }
  
  async function getTimingPresets() {
    return await $fetch<{ table: string; count: number; data: TimingPreset[] }>(
      `/api/bridge/query/timing_presets`
    )
  }
  
  async function getNarrationStyles() {
    return await $fetch<{ table: string; count: number; data: NarrationStyle[] }>(
      `/api/bridge/query/narration_styles`
    )
  }
  
  // =========================================================================
  // Session Generation
  // =========================================================================
  
  async function generateSession(request: SessionRequest): Promise<SessionOutput> {
    return await $fetch<SessionOutput>('/api/bridge/session', {
      method: 'POST',
      body: request
    })
  }
  
  // =========================================================================
  // Content Queries (generic)
  // =========================================================================
  
  async function queryTable<T = any>(table: string, limit = 100) {
    return await $fetch<{ table: string; count: number; data: T[] }>(
      `/api/bridge/query/${table}?limit=${limit}`
    )
  }
  
  return {
    // Templates
    getTemplates,
    getTemplate,
    
    // Controls
    getControlDefinitions,
    getControlPacks,
    
    // Engine
    getCouplingRules,
    getDerivedMetrics,
    
    // Profiles
    getProgrammeProfiles,
    
    // NEW: Techniques & Lenses
    getTechniques,
    getLenses,
    getPersonas,
    getKnowledgeBases,
    getSessionBlueprints,
    getTimingPresets,
    getNarrationStyles,
    
    // Sessions
    generateSession,
    
    // Generic
    queryTable,
  }
}
```

---

## STEP 4: Create Server Routes

Create these 4 files in your `server/api/bridge/` folder:

### 4a. server/api/bridge/templates.get.ts

```typescript
// server/api/bridge/templates.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  
  const url = new URL('/api/templates', config.cursorBridgeApi)
  if (query.category) {
    url.searchParams.set('category', String(query.category))
  }
  
  return await $fetch(url.toString())
})
```

### 4b. server/api/bridge/session.post.ts

```typescript
// server/api/bridge/session.post.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)
  
  return await $fetch(`${config.cursorBridgeSandbox}/sandbox/generate-session`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body
  })
})
```

### 4c. server/api/bridge/lenses.get.ts

```typescript
// server/api/bridge/lenses.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  
  return await $fetch(`${config.cursorBridgeSandbox}/sandbox/lenses`)
})
```

### 4d. server/api/bridge/query/[table].get.ts

```typescript
// server/api/bridge/query/[table].get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const table = getRouterParam(event, 'table')
  const query = getQuery(event)
  
  const url = new URL(`/api/query/${table}`, config.cursorBridgeApi)
  if (query.limit) {
    url.searchParams.set('limit', String(query.limit))
  }
  
  return await $fetch(url.toString())
})
```

---

## STEP 5: SessionPlayer Component (Optional)

If you want a ready-made session player, create this component:

```vue
<!-- components/SessionPlayer.vue -->
<template>
  <div class="session-player">
    <div class="player-header">
      <h1>{{ session.name }}</h1>
      <p class="persona">{{ session.persona_style }}</p>
      <p class="lens-badge">{{ session.lens }} lens</p>
    </div>
    
    <!-- Progress -->
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
    </div>
    <div class="time-display">
      <span>{{ formatTime(elapsedSeconds) }}</span>
      <span>{{ formatTime(totalSeconds) }}</span>
    </div>
    
    <!-- Current Section -->
    <div class="current-section">
      <div class="section-type" :class="currentSection?.type">
        {{ currentSection?.type }}
      </div>
      <h2>{{ currentSection?.name }}</h2>
      <p class="instructions">{{ currentSection?.instructions }}</p>
      
      <!-- Lens Explanations -->
      <div v-if="currentSection?.lens_explanation_western" class="lens-explanation">
        <strong>Western:</strong> {{ currentSection.lens_explanation_western }}
      </div>
      <div v-if="currentSection?.lens_explanation_tcm" class="lens-explanation">
        <strong>TCM:</strong> {{ currentSection.lens_explanation_tcm }}
      </div>
      
      <!-- Cues -->
      <div v-if="currentSection?.cues" class="cues">
        <div 
          v-for="(cue, i) in currentSection.cues" 
          :key="i"
          class="cue"
          :class="{ active: isCueActive(cue) }"
        >
          {{ cue }}
        </div>
      </div>
    </div>
    
    <!-- Controls -->
    <div class="player-controls">
      <button @click="togglePlay" class="play-button">
        {{ isPlaying ? 'Pause' : 'Play' }}
      </button>
      <button @click="skipSection" class="skip-button">
        Skip
      </button>
    </div>
    
    <!-- Safety Warnings -->
    <div v-if="session.safety_warnings?.length" class="safety-warnings">
      <h3>Safety Notes</h3>
      <ul>
        <li v-for="(warning, i) in session.safety_warnings" :key="i">
          {{ warning }}
        </li>
      </ul>
    </div>
    
    <!-- Close -->
    <button @click="$emit('complete')" class="close-button">
      End Session
    </button>
  </div>
</template>

<script setup lang="ts">
import type { SessionOutput } from '~/types/bridge'

const props = defineProps<{
  session: SessionOutput
}>()

defineEmits<{
  complete: []
}>()

const isPlaying = ref(false)
const elapsedSeconds = ref(0)
const currentSectionIndex = ref(0)

const totalSeconds = computed(() => props.session.duration_minutes * 60)

const progressPercent = computed(() => 
  (elapsedSeconds.value / totalSeconds.value) * 100
)

const currentSection = computed(() => 
  props.session.sections[currentSectionIndex.value]
)

let timer: ReturnType<typeof setInterval> | null = null

function togglePlay() {
  isPlaying.value = !isPlaying.value
  
  if (isPlaying.value) {
    timer = setInterval(() => {
      elapsedSeconds.value++
      
      const sectionEnd = getSectionEndTime(currentSectionIndex.value)
      if (elapsedSeconds.value >= sectionEnd && currentSectionIndex.value < props.session.sections.length - 1) {
        currentSectionIndex.value++
      }
      
      if (elapsedSeconds.value >= totalSeconds.value) {
        isPlaying.value = false
        if (timer) clearInterval(timer)
      }
    }, 1000)
  } else if (timer) {
    clearInterval(timer)
  }
}

function skipSection() {
  if (currentSectionIndex.value < props.session.sections.length - 1) {
    elapsedSeconds.value = getSectionEndTime(currentSectionIndex.value)
    currentSectionIndex.value++
  }
}

function getSectionEndTime(index: number): number {
  let time = 0
  for (let i = 0; i <= index; i++) {
    time += props.session.sections[i].duration_minutes * 60
  }
  return time
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${m}:${s.toString().padStart(2, '0')}`
}

function isCueActive(cue: string): boolean {
  const match = cue.match(/^(\d+):(\d+)/)
  if (!match) return false
  
  const cueTime = parseInt(match[1]) * 60 + parseInt(match[2])
  const sectionStart = currentSectionIndex.value > 0 
    ? getSectionEndTime(currentSectionIndex.value - 1) 
    : 0
  const sectionElapsed = elapsedSeconds.value - sectionStart
  
  return sectionElapsed >= cueTime
}

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.session-player {
  background: #1a1a2e;
  border-radius: 16px;
  padding: 2rem;
  color: white;
}

.player-header { text-align: center; margin-bottom: 2rem; }
.player-header h1 { font-size: 1.75rem; margin-bottom: 0.5rem; }
.persona { color: #e94560; font-style: italic; }
.lens-badge { background: #333; padding: 0.25rem 0.75rem; border-radius: 20px; display: inline-block; margin-top: 0.5rem; }

.progress-bar { height: 6px; background: #333; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #e94560, #ff6b6b); transition: width 0.5s; }
.time-display { display: flex; justify-content: space-between; margin-top: 0.5rem; color: #666; font-size: 0.875rem; }

.current-section { text-align: center; padding: 2rem 0; }
.section-type { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; text-transform: uppercase; font-weight: 600; margin-bottom: 1rem; background: #333; }
.section-type.breathwork { background: rgba(100, 200, 255, 0.2); color: #64c8ff; }
.section-type.movement { background: rgba(100, 255, 150, 0.2); color: #64ff96; }
.section-type.meditation { background: rgba(200, 150, 255, 0.2); color: #c896ff; }

.current-section h2 { font-size: 1.5rem; margin-bottom: 1rem; }
.instructions { color: #aaa; max-width: 500px; margin: 0 auto; line-height: 1.6; }

.lens-explanation { background: #222; padding: 1rem; border-radius: 8px; margin-top: 1rem; text-align: left; font-size: 0.9rem; }

.cues { margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.cue { color: #555; font-size: 0.875rem; transition: all 0.3s; }
.cue.active { color: #fff; font-weight: 500; }

.player-controls { display: flex; justify-content: center; gap: 1rem; margin: 2rem 0; }
.play-button { padding: 1rem 2rem; background: #e94560; border: none; border-radius: 8px; color: white; font-size: 1rem; cursor: pointer; }
.skip-button { padding: 1rem 1.5rem; background: #333; border: none; border-radius: 8px; color: white; cursor: pointer; }

.safety-warnings { background: rgba(255, 200, 100, 0.1); border: 1px solid rgba(255, 200, 100, 0.2); border-radius: 12px; padding: 1rem 1.5rem; margin-top: 2rem; }
.safety-warnings h3 { color: #ffc864; font-size: 0.875rem; margin-bottom: 0.5rem; }
.safety-warnings ul { margin: 0; padding-left: 1.25rem; }
.safety-warnings li { color: #888; font-size: 0.875rem; margin: 0.25rem 0; }

.close-button { width: 100%; padding: 1rem; background: transparent; border: 1px solid #444; border-radius: 8px; color: #888; margin-top: 1.5rem; cursor: pointer; }
</style>
```

---

## STEP 6: Example Usage in a Page

```vue
<!-- pages/session.vue -->
<template>
  <div class="session-page">
    <!-- Session Setup -->
    <div v-if="!activeSession" class="session-setup">
      <h1>Create Session</h1>
      
      <!-- Lens Selector -->
      <div class="form-group">
        <label>Lens</label>
        <select v-model="selectedLens">
          <option v-for="lens in lenses" :key="lens.lens_slug" :value="lens.lens_slug">
            {{ lens.icon }} {{ lens.lens_name }}
          </option>
        </select>
      </div>
      
      <!-- Technique Browser -->
      <div class="form-group">
        <label>Techniques</label>
        <div class="technique-grid">
          <div 
            v-for="tech in techniques" 
            :key="tech.id" 
            class="technique-card"
            :class="{ selected: selectedTechniques.includes(tech.id) }"
            @click="toggleTechnique(tech.id)"
          >
            <strong>{{ tech.technique }}</strong>
            <span class="badge">{{ tech.technique_category }}</span>
            <span class="intensity">{{ tech.intensity_band }}</span>
          </div>
        </div>
      </div>
      
      <!-- Duration -->
      <div class="form-group">
        <label>Duration</label>
        <select v-model="selectedDuration">
          <option v-for="timing in timings" :key="timing.id" :value="timing.total_duration_min">
            {{ timing.preset_name }} ({{ timing.total_duration_min }} min)
          </option>
        </select>
      </div>
      
      <button @click="generateSession" :disabled="loading">
        {{ loading ? 'Generating...' : 'Generate Session' }}
      </button>
    </div>
    
    <!-- Session Player -->
    <SessionPlayer 
      v-else 
      :session="activeSession" 
      @complete="activeSession = null" 
    />
  </div>
</template>

<script setup lang="ts">
import type { SessionOutput, Technique, Lens, TimingPreset } from '~/types/bridge'

const bridge = useBridge()

const lenses = ref<Lens[]>([])
const techniques = ref<Technique[]>([])
const timings = ref<TimingPreset[]>([])

const selectedLens = ref('hybrid')
const selectedTechniques = ref<string[]>([])
const selectedDuration = ref(20)
const loading = ref(false)
const activeSession = ref<SessionOutput | null>(null)

// Load data on mount
onMounted(async () => {
  const [lensData, techData, timingData] = await Promise.all([
    bridge.getLenses(),
    bridge.getTechniques(),
    bridge.getTimingPresets()
  ])
  
  lenses.value = lensData.lenses
  techniques.value = techData.data
  timings.value = timingData.data
})

function toggleTechnique(id: string) {
  if (selectedTechniques.value.includes(id)) {
    selectedTechniques.value = selectedTechniques.value.filter(t => t !== id)
  } else {
    selectedTechniques.value.push(id)
  }
}

async function generateSession() {
  loading.value = true
  try {
    activeSession.value = await bridge.generateSession({
      user_id: 'current-user-id', // Replace with actual user
      duration_min: selectedDuration.value,
      lens: selectedLens.value,
      explanation_level: 'plain'
    })
  } finally {
    loading.value = false
  }
}
</script>
```

---

## Available Tables (queryTable)

Use `useBridge().queryTable('table_name')` to query any of these:

| Table | Content |
|-------|---------|
| `techniques` | Breathing, meditation, movement techniques |
| `session_blueprints` | Pre-built session recipes |
| `timing_presets` | Duration options (10/20/30/45/60 min) |
| `narration_styles` | Voice/pacing options |
| `lens_definitions` | All available lenses |
| `archetypal_personas` | AI personality styles |
| `knowledge_bases` | Source traditions/literature |
| `programme_profiles` | User wellness profiles |
| `breath_library` | Breathing technique library |
| `movements_system` | Movement library |
| `session_templates` | Session templates |
| `control_definitions` | All UI controls |
| `control_packs` | Control bundles |
| `coupling_rules` | How controls affect each other |
| `derived_metrics` | Calculated scores |
| `evidence_sources` | Research references |

---

## API Endpoints Summary

| What | Endpoint | Method |
|------|----------|--------|
| All templates | `/api/bridge/templates` | GET |
| Single template | `/api/bridge/templates/{id}` | GET |
| Any table | `/api/bridge/query/{table}` | GET |
| All lenses | `/api/bridge/lenses` | GET |
| Generate session | `/api/bridge/session` | POST |

---

## That's It!

You now have everything needed to integrate with CursorBridge. Just copy-paste the code blocks above into your existing Main App.

**Test it:**
```typescript
// In any component
const bridge = useBridge()
const { data: techniques } = await bridge.getTechniques()
console.log('Techniques:', techniques)
```

