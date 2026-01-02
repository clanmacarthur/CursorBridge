<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div>
        <h1>Good {{ greeting }}, {{ userName }}</h1>
        <p class="date">{{ formattedDate }}</p>
      </div>
      <button @click="showTemplates = true" class="btn-primary">
        + Add Block
      </button>
    </header>
    
    <!-- Check-in Section -->
    <section class="checkin-section">
      <h2>Daily Check-in</h2>
      <div class="controls-grid">
        <div v-for="control in defaultControls" :key="control.id" class="control-card">
          <BlockSlider 
            v-if="control.control_type === 'slider'"
            :control="control"
            v-model="checkinValues[control.id]"
          />
          <BlockCheckbox 
            v-else-if="control.control_type === 'checkbox'"
            :control="control"
            v-model="checkinValues[control.id]"
          />
        </div>
      </div>
      <button @click="saveCheckin" class="btn-primary" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save Check-in' }}
      </button>
    </section>
    
    <!-- Templates Modal -->
    <div v-if="showTemplates" class="modal-overlay" @click.self="showTemplates = false">
      <div class="modal">
        <h2>Add Dashboard Block</h2>
        <div class="templates-grid">
          <div 
            v-for="template in templates" 
            :key="template.id"
            class="template-card"
            @click="selectTemplate(template)"
          >
            <span class="template-icon">{{ template.icon }}</span>
            <h3>{{ template.name }}</h3>
            <p>{{ template.description }}</p>
          </div>
        </div>
        <button @click="showTemplates = false" class="btn-secondary">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ControlDefinition, DashboardTemplate } from '~/types'

const user = useSupabaseUser()
const { getControlDefinitions, getTemplates } = useBridge()

// State
const showTemplates = ref(false)
const saving = ref(false)
const checkinValues = ref<Record<string, number | boolean>>({})
const defaultControls = ref<ControlDefinition[]>([])
const templates = ref<DashboardTemplate[]>([])

// Computed
const userName = computed(() => user.value?.email?.split('@')[0] || 'Friend')

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 17) return 'afternoon'
  return 'evening'
})

const formattedDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric'
  })
})

// Load data
onMounted(async () => {
  const [controlsRes, templatesRes] = await Promise.all([
    getControlDefinitions(),
    getTemplates()
  ])
  
  defaultControls.value = controlsRes.data.filter(c => c.is_default)
  templates.value = templatesRes.templates
  
  // Initialize values
  defaultControls.value.forEach(control => {
    checkinValues.value[control.id] = control.default_value || 0
  })
})

// Actions
async function saveCheckin() {
  saving.value = true
  
  const client = useSupabaseClient()
  await client.from('user_checkins').insert({
    user_id: user.value?.id,
    checkin_date: new Date().toISOString().split('T')[0],
    control_values: checkinValues.value
  })
  
  saving.value = false
}

function selectTemplate(template: DashboardTemplate) {
  console.log('Selected template:', template)
  showTemplates.value = false
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  color: #fff;
  font-size: 2rem;
}

.date {
  color: rgba(255, 255, 255, 0.5);
}

.checkin-section {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
}

.checkin-section h2 {
  color: #fff;
  margin-bottom: 1.5rem;
}

.controls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.control-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1.25rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: #1a1a2e;
  border-radius: 20px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
}

.modal h2 {
  color: #fff;
  margin-bottom: 1.5rem;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.template-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.template-card:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #e94560;
}

.template-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

.template-card h3 {
  color: #fff;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.template-card p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
}
</style>

