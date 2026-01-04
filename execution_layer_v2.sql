-- ============================================================
-- EXECUTION LAYER SCHEMA V2 (SIMPLE)
-- Run in Supabase SQL Editor
-- ============================================================

-- 1. TIMING PRESETS
CREATE TABLE IF NOT EXISTS timing_presets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    preset_name TEXT NOT NULL,
    total_duration_min INTEGER NOT NULL,
    intro_pct INTEGER DEFAULT 10,
    technique_pct INTEGER DEFAULT 60,
    integration_pct INTEGER DEFAULT 20,
    outro_pct INTEGER DEFAULT 10,
    default_pause_sec INTEGER DEFAULT 3,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. SESSION PHASES
CREATE TABLE IF NOT EXISTS session_phases (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    phase_name TEXT NOT NULL,
    phase_type TEXT NOT NULL,
    default_intensity TEXT,
    default_min_duration_sec INTEGER,
    default_max_duration_sec INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. TRANSITION RULES
CREATE TABLE IF NOT EXISTS transition_rules (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name TEXT NOT NULL,
    transition_type TEXT NOT NULL,
    pause_duration_sec INTEGER DEFAULT 3,
    audio_cue TEXT,
    narration_template TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 4. NARRATION STYLES
CREATE TABLE IF NOT EXISTS narration_styles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    style_name TEXT NOT NULL,
    voice_tone TEXT NOT NULL,
    reading_pace_wpm INTEGER DEFAULT 140,
    breath_verbosity TEXT,
    physiology_level TEXT,
    tcm_level TEXT,
    pause_between_sentences_sec NUMERIC(3,1) DEFAULT 1.5,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. CUE TRIGGERS
CREATE TABLE IF NOT EXISTS cue_triggers (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    trigger_name TEXT NOT NULL,
    trigger_scope TEXT NOT NULL,
    interval_sec INTEGER,
    sound_id uuid,
    light_colour_id uuid,
    symbol_id uuid,
    sacred_geometry_id uuid,
    organ_emotion_id uuid,
    meridian_id uuid,
    chakra_id uuid,
    narration_text TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 6. SESSION BLUEPRINTS
CREATE TABLE IF NOT EXISTS session_blueprints (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_name TEXT NOT NULL,
    description TEXT,
    programme_profile_id uuid,
    persona_id uuid,
    lens_preset_id uuid,
    timing_preset_id uuid,
    narration_style_id uuid,
    safety_level TEXT DEFAULT 'baseline',
    is_platform_example BOOLEAN DEFAULT false,
    is_published BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 100,
    tags TEXT[],
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 7. TECHNIQUE STEPS
CREATE TABLE IF NOT EXISTS technique_steps (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    step_name TEXT NOT NULL,
    technique_id uuid,
    phase_id uuid,
    step_order INTEGER DEFAULT 1,
    min_duration_sec INTEGER DEFAULT 60,
    max_duration_sec INTEGER DEFAULT 600,
    intensity_target TEXT,
    transition_rule_id uuid,
    instructions_template TEXT,
    safety_notes TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 8. BLUEPRINT STEPS
CREATE TABLE IF NOT EXISTS blueprint_steps (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_id uuid,
    technique_step_id uuid,
    step_order INTEGER NOT NULL DEFAULT 1,
    override_duration_sec INTEGER,
    override_intensity TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 9. BLUEPRINT CUES
CREATE TABLE IF NOT EXISTS blueprint_cues (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_id uuid,
    cue_trigger_id uuid,
    is_required BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 10. SESSION RUNS
CREATE TABLE IF NOT EXISTS session_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid,
    blueprint_id uuid,
    started_at TIMESTAMPTZ DEFAULT now(),
    completed_at TIMESTAMPTZ,
    actual_duration_sec INTEGER,
    completion_status TEXT,
    user_rating INTEGER,
    user_notes TEXT,
    session_data JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 11. SESSION OUTPUTS
CREATE TABLE IF NOT EXISTS session_outputs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_run_id uuid,
    output_type TEXT NOT NULL,
    content JSONB,
    content_text TEXT,
    generated_at TIMESTAMPTZ DEFAULT now()
);



