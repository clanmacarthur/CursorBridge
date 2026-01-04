<template>
  <div class="session-player">
    <div class="player-header">
      <h1>{{ session.name }}</h1>
      <p class="persona">{{ session.persona_style }}</p>
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
        {{ isPlaying ? '⏸' : '▶' }}
      </button>
      <button @click="skipSection" class="skip-button">
        Skip →
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
    <button @click="$emit('complete')" class="btn-secondary close-button">
      End Session
    </button>
  </div>
</template>

<script setup lang="ts">
import type { SessionOutput, SessionSection } from '~/types'

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
      
      // Check if we should advance to next section
      const sectionEnd = getSectionEndTime(currentSectionIndex.value)
      if (elapsedSeconds.value >= sectionEnd && currentSectionIndex.value < props.session.sections.length - 1) {
        currentSectionIndex.value++
      }
      
      // Check if session is complete
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
  
  const cueMinutes = parseInt(match[1])
  const cueSeconds = parseInt(match[2])
  const cueTime = cueMinutes * 60 + cueSeconds
  
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
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2.5rem;
}

.player-header {
  text-align: center;
  margin-bottom: 2rem;
}

.player-header h1 {
  color: #fff;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.persona {
  color: #e94560;
  font-style: italic;
}

.progress-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #e94560, #ff6b6b);
  transition: width 0.5s;
}

.time-display {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
}

.current-section {
  text-align: center;
  padding: 2rem 0;
}

.section-type {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 1rem;
}

.section-type.breathwork {
  background: rgba(100, 200, 255, 0.2);
  color: #64c8ff;
}

.section-type.movement {
  background: rgba(100, 255, 150, 0.2);
  color: #64ff96;
}

.section-type.meditation {
  background: rgba(200, 150, 255, 0.2);
  color: #c896ff;
}

.current-section h2 {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.instructions {
  color: rgba(255, 255, 255, 0.7);
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.6;
}

.cues {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: center;
}

.cue {
  color: rgba(255, 255, 255, 0.3);
  font-size: 0.875rem;
  transition: all 0.3s;
}

.cue.active {
  color: #fff;
  font-weight: 500;
}

.player-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
}

.play-button {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #e94560;
  border: none;
  color: #fff;
  font-size: 2rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.play-button:hover {
  transform: scale(1.05);
}

.skip-button {
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #fff;
  cursor: pointer;
}

.safety-warnings {
  background: rgba(255, 200, 100, 0.1);
  border: 1px solid rgba(255, 200, 100, 0.2);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-top: 2rem;
}

.safety-warnings h3 {
  color: #ffc864;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.safety-warnings ul {
  margin: 0;
  padding-left: 1.25rem;
}

.safety-warnings li {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.875rem;
  margin: 0.25rem 0;
}

.close-button {
  width: 100%;
  margin-top: 1.5rem;
}
</style>






