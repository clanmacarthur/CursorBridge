<template>
  <div class="session-page">
    <!-- Session Setup -->
    <div v-if="!session" class="session-setup">
      <h1>Generate a Session</h1>
      <p class="subtitle">Choose your preferences and we'll create a personalized guided session.</p>
      
      <div class="setup-form">
        <div class="form-group">
          <label>Duration</label>
          <div class="duration-options">
            <button 
              v-for="d in [10, 15, 20, 30]" 
              :key="d"
              :class="{ active: duration === d }"
              @click="duration = d"
            >
              {{ d }} min
            </button>
          </div>
        </div>
        
        <div class="form-group">
          <label>Profile</label>
          <select v-model="selectedProfile">
            <option v-for="p in profiles" :key="p.id" :value="p.id">
              {{ p.programme_profile___title }}
            </option>
          </select>
        </div>
        
        <button @click="generateSession" class="btn-primary btn-large" :disabled="generating">
          {{ generating ? 'Generating...' : 'Generate Session' }}
        </button>
      </div>
    </div>
    
    <!-- Session Player -->
    <div v-else class="session-player">
      <SessionPlayer :session="session" @complete="session = null" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SessionOutput, ProgrammeProfile } from '~/types'

const user = useSupabaseUser()
const { generateSession: genSession, getProgrammeProfiles } = useBridge()

const session = ref<SessionOutput | null>(null)
const generating = ref(false)
const duration = ref(15)
const selectedProfile = ref('')
const profiles = ref<ProgrammeProfile[]>([])

onMounted(async () => {
  const res = await getProgrammeProfiles()
  profiles.value = res.data
  if (profiles.value.length > 0) {
    selectedProfile.value = profiles.value[0].id
  }
})

async function generateSession() {
  generating.value = true
  
  try {
    session.value = await genSession({
      user_id: user.value?.id || 'anonymous',
      programme_profile_id: selectedProfile.value,
      session_template_id: '1', // Default template
      duration_min: duration.value
    })
  } catch (error) {
    console.error('Failed to generate session:', error)
  }
  
  generating.value = false
}
</script>

<style scoped>
.session-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.session-setup {
  text-align: center;
  max-width: 500px;
}

.session-setup h1 {
  color: #fff;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 2rem;
}

.setup-form {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

.form-group label {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
}

.duration-options {
  display: flex;
  gap: 0.5rem;
}

.duration-options button {
  flex: 1;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s;
}

.duration-options button.active {
  background: #e94560;
  border-color: #e94560;
}

.form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
}

.session-player {
  width: 100%;
  max-width: 800px;
}
</style>

