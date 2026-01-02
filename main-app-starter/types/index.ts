// ============================================================================
// CursorBridge Types
// ============================================================================

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

// Session Generation
export interface SessionRequest {
  user_id: string
  programme_profile_id: string
  session_template_id: string
  duration_min: number
  preferences?: Record<string, any>
}

export interface SessionOutput {
  id: string
  name: string
  duration_minutes: number
  persona_style?: string
  sections: SessionSection[]
  safety_warnings: string[]
  created_at: string
}

export interface SessionSection {
  type: 'breathwork' | 'movement' | 'meditation' | 'transition'
  name: string
  duration_minutes: number
  instructions: string
  audio_url?: string
  cues?: string[]
}

// User Check-in
export interface CheckinData {
  user_id: string
  checkin_date: string
  control_values: Record<string, number | boolean>
  derived_scores?: Record<string, number>
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

