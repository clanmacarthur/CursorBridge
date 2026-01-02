<template>
  <div class="block-checkbox" :class="{ checked: modelValue }" @click="toggle">
    <div class="checkbox-icon">
      <span v-if="modelValue">✓</span>
    </div>
    <div class="checkbox-content">
      <label>{{ control.control_name }}</label>
      <p v-if="control.description">{{ control.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ControlDefinition } from '~/types'

const props = defineProps<{
  control: ControlDefinition
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

function toggle() {
  emit('update:modelValue', !props.modelValue)
}
</script>

<style scoped>
.block-checkbox {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background 0.2s;
}

.block-checkbox:hover {
  background: rgba(255, 255, 255, 0.05);
}

.checkbox-icon {
  width: 28px;
  height: 28px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: #fff;
  font-weight: bold;
}

.block-checkbox.checked .checkbox-icon {
  background: #e94560;
  border-color: #e94560;
}

.checkbox-content label {
  color: #fff;
  font-weight: 500;
  display: block;
}

.checkbox-content p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>

