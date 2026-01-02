<template>
  <div class="block-slider">
    <div class="slider-header">
      <label>{{ control.control_name }}</label>
      <span class="value">{{ modelValue }} {{ control.unit }}</span>
    </div>
    <input 
      type="range"
      :min="control.range_min || 0"
      :max="control.range_max || 10"
      :step="control.range_step || 1"
      :value="modelValue"
      @input="$emit('update:modelValue', Number(($event.target as HTMLInputElement).value))"
    />
    <div class="range-labels">
      <span>{{ control.range_min || 0 }}</span>
      <span>{{ control.range_max || 10 }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ControlDefinition } from '~/types'

defineProps<{
  control: ControlDefinition
  modelValue: number
}>()

defineEmits<{
  'update:modelValue': [value: number]
}>()
</script>

<style scoped>
.block-slider {
  width: 100%;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.slider-header label {
  color: #fff;
  font-weight: 500;
}

.value {
  color: #e94560;
  font-weight: 600;
}

input[type="range"] {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  outline: none;
  -webkit-appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #e94560;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.range-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.75rem;
}
</style>



