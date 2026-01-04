-- ============================================================
-- EXECUTION LAYER SCHEMA
-- CursorBridge: Tables for session generation & runtime
-- ============================================================

-- 1. TIMING PRESETS
-- Duration/pace configurations users pick from dropdowns
CREATE TABLE IF NOT EXISTS timing_presets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    preset_name TEXT NOT NULL UNIQUE,
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
-- Phase templates that structure sessions
CREATE TABLE IF NOT EXISTS session_phases (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    phase_name TEXT NOT NULL UNIQUE,
    phase_type TEXT NOT NULL CHECK (phase_type IN ('intro', 'technique', 'integration', 'outro', 'transition')),
    default_intensity TEXT CHECK (default_intensity IN ('low', 'med', 'high')),
    default_min_duration_sec INTEGER,
    default_max_duration_sec INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. TRANSITION RULES
-- How phases connect to each other
CREATE TABLE IF NOT EXISTS transition_rules (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name TEXT NOT NULL UNIQUE,
    transition_type TEXT NOT NULL CHECK (transition_type IN ('soft_fade', 'counted_pause', 'bell', 'breath_bridge', 'instant')),
    pause_duration_sec INTEGER DEFAULT 3,
    audio_cue TEXT,
    narration_template TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 4. NARRATION STYLES
-- Voice/pace/tone configurations
CREATE TABLE IF NOT EXISTS narration_styles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    style_name TEXT NOT NULL UNIQUE,
    voice_tone TEXT NOT NULL CHECK (voice_tone IN ('spiritual', 'scientific', 'neutral', 'direct', 'soft', 'warm')),
    reading_pace_wpm INTEGER DEFAULT 140,
    breath_verbosity TEXT CHECK (breath_verbosity IN ('minimal', 'normal', 'detailed')),
    physiology_level TEXT CHECK (physiology_level IN ('none', 'light', 'full')),
    tcm_level TEXT CHECK (tcm_level IN ('none', 'light', 'full')),
    pause_between_sentences_sec NUMERIC(3,1) DEFAULT 1.5,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. TECHNIQUE STEPS
-- Ready-made step sequences for techniques
CREATE TABLE IF NOT EXISTS technique_steps (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    step_name TEXT NOT NULL,
    technique_id uuid REFERENCES techniques(id),
    phase_id uuid REFERENCES session_phases(id),
    step_order INTEGER DEFAULT 1,
    min_duration_sec INTEGER NOT NULL,
    max_duration_sec INTEGER NOT NULL,
    intensity_target TEXT CHECK (intensity_target IN ('low', 'med', 'high')),
    transition_rule_id uuid REFERENCES transition_rules(id),
    instructions_template TEXT,
    safety_notes TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 6. CUE TRIGGERS
-- Multi-DB scheduled events (sound, color, symbol, chakra, etc.)
CREATE TABLE IF NOT EXISTS cue_triggers (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    trigger_name TEXT NOT NULL UNIQUE,
    trigger_scope TEXT NOT NULL CHECK (trigger_scope IN ('phase_start', 'phase_end', 'interval', 'on_demand')),
    interval_sec INTEGER,
    -- References to content DBs (all optional)
    sound_id uuid,  -- References sound_vibration
    light_colour_id uuid,  -- References light_colour
    symbol_id uuid,  -- References symbols_index
    sacred_geometry_id uuid,  -- References sacred_geometry
    organ_emotion_id uuid,  -- References organ_emotion_system
    meridian_id uuid,  -- References meridian_system
    chakra_id uuid,  -- References chakra_system
    narration_text TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 7. SESSION BLUEPRINTS
-- Complete session recipes users pick from
CREATE TABLE IF NOT EXISTS session_blueprints (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_name TEXT NOT NULL UNIQUE,
    description TEXT,
    -- Core configuration
    programme_profile_id uuid,  -- References programme_profiles
    persona_id uuid,  -- References archetypal_personas
    lens_preset_id uuid REFERENCES meta_lens_presets(id),
    timing_preset_id uuid REFERENCES timing_presets(id),
    narration_style_id uuid REFERENCES narration_styles(id),
    -- Safety
    safety_level TEXT DEFAULT 'baseline' CHECK (safety_level IN ('baseline', 'trauma_safe', 'clinical', 'advanced')),
    -- Metadata
    is_platform_example BOOLEAN DEFAULT false,
    is_published BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 100,
    tags TEXT[],
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 8. BLUEPRINT STEPS (junction table)
-- Links blueprints to technique_steps in order
CREATE TABLE IF NOT EXISTS blueprint_steps (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_id uuid REFERENCES session_blueprints(id) ON DELETE CASCADE,
    technique_step_id uuid REFERENCES technique_steps(id),
    step_order INTEGER NOT NULL,
    override_duration_sec INTEGER,
    override_intensity TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 9. BLUEPRINT CUES (junction table)
-- Links blueprints to cue_triggers
CREATE TABLE IF NOT EXISTS blueprint_cues (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    blueprint_id uuid REFERENCES session_blueprints(id) ON DELETE CASCADE,
    cue_trigger_id uuid REFERENCES cue_triggers(id),
    is_required BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 10. SESSION RUNS (runtime output - Main App writes here)
CREATE TABLE IF NOT EXISTS session_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid,
    blueprint_id uuid REFERENCES session_blueprints(id),
    started_at TIMESTAMPTZ DEFAULT now(),
    completed_at TIMESTAMPTZ,
    actual_duration_sec INTEGER,
    completion_status TEXT CHECK (completion_status IN ('completed', 'partial', 'abandoned')),
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_notes TEXT,
    session_data JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 11. SESSION OUTPUTS (generated content - Main App writes here)
CREATE TABLE IF NOT EXISTS session_outputs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_run_id uuid REFERENCES session_runs(id) ON DELETE CASCADE,
    output_type TEXT NOT NULL CHECK (output_type IN ('timeline_json', 'narration_text', 'cue_schedule', 'audio_script')),
    content JSONB,
    content_text TEXT,
    generated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_blueprint_steps_blueprint ON blueprint_steps(blueprint_id);
CREATE INDEX IF NOT EXISTS idx_blueprint_cues_blueprint ON blueprint_cues(blueprint_id);
CREATE INDEX IF NOT EXISTS idx_session_runs_user ON session_runs(user_id);
CREATE INDEX IF NOT EXISTS idx_session_runs_blueprint ON session_runs(blueprint_id);
CREATE INDEX IF NOT EXISTS idx_technique_steps_technique ON technique_steps(technique_id);

-- ============================================================
-- SEED DATA
-- ============================================================

-- TIMING PRESETS
INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, notes) VALUES
('10-min Quick Reset', 10, 10, 60, 20, 10, 'Short reset session'),
('20-min Regulation', 20, 10, 55, 25, 10, 'Standard regulation session'),
('30-min Rich Mix', 30, 8, 55, 27, 10, 'Full multi-technique session'),
('45-min Deep Practice', 45, 7, 55, 28, 10, 'Extended practice'),
('60-min Immersive', 60, 5, 55, 30, 10, 'Full immersive experience')
ON CONFLICT (preset_name) DO NOTHING;

-- SESSION PHASES
INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes) VALUES
('Welcome & Grounding', 'intro', 'low', 60, 180, 'Opening orientation'),
('Breath Technique Phase', 'technique', 'med', 180, 600, 'Core breathwork'),
('Movement Integration', 'technique', 'med', 120, 480, 'Body movement'),
('Deep Rest (NSDR)', 'integration', 'low', 300, 900, 'Non-sleep deep rest'),
('Body Scan', 'integration', 'low', 180, 600, 'Somatic awareness'),
('Meridian/Energy Work', 'integration', 'low', 180, 480, 'TCM integration'),
('Closing & Transition', 'outro', 'low', 60, 180, 'Return to activity')
ON CONFLICT (phase_name) DO NOTHING;

-- TRANSITION RULES
INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, narration_template, notes) VALUES
('Soft Fade', 'soft_fade', 5, 'Allow this to settle... gently shifting now...', 'Gentle transition'),
('Counted Pause', 'counted_pause', 10, 'Take three breaths here before we continue...', 'Breath-counted gap'),
('Bell Transition', 'bell', 3, NULL, 'Audio cue marks change'),
('Breath Bridge', 'breath_bridge', 8, 'Three deep breaths to bridge into the next phase...', 'Active breath transition'),
('Instant', 'instant', 0, NULL, 'No pause')
ON CONFLICT (rule_name) DO NOTHING;

-- NARRATION STYLES
INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes) VALUES
('Temple Guide', 'spiritual', 125, 'detailed', 'none', 'light', 'Slow cadence, imagery, soft pacing'),
('Lab Coach', 'scientific', 150, 'normal', 'full', 'none', 'Explanations between cues'),
('Science Coach', 'neutral', 145, 'normal', 'light', 'none', 'Clear, practical, some mechanism'),
('TCM Storyteller', 'spiritual', 130, 'normal', 'none', 'full', 'Meridian/organ framing'),
('Minimal Timer', 'neutral', 160, 'minimal', 'none', 'none', 'Few words, long silences'),
('Warm Guide', 'warm', 135, 'normal', 'light', 'light', 'Friendly, supportive tone'),
('Spiritual Guide', 'spiritual', 120, 'detailed', 'none', 'none', 'Symbolic, meaning-based')
ON CONFLICT (style_name) DO NOTHING;

-- ADDITIONAL LENS DEFINITIONS (supplements existing 14)
INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order) VALUES
('physiology_plain', 'Physiology (Plain)', 'perspective', 'scientific', 'neutral', 'Explain what''s happening in the body in simple terms', '🫁', 20),
('physiology_scientific', 'Physiology (Scientific)', 'perspective', 'scientific', 'scientific', 'Clinical/scientific explanation with citations', '🔬', 21),
('tcm_organs_meridians', 'TCM (Organs & Meridians)', 'medical_tradition', 'traditional', 'spiritual', 'Explain via organ systems and meridians', '☯️', 22),
('somatic_trauma_safe', 'Somatic Trauma-Safe', 'safety', 'somatic', 'soft', 'Safety-first language, gentle pacing, opt-outs', '🛡️', 23),
('performance_coach', 'Performance Coach', 'coaching', 'performance', 'direct', 'Training/recovery framing, protocols + timing', '🏋️', 24),
('huberman_nsdr', 'Huberman-style NSDR', 'science_comm', 'scientific', 'neutral', 'Clear structure, practical cues, light jargon', '🧠', 25),
('mantak_chia', 'Mantak Chia (Microcosmic Orbit)', 'tcm_daoist', 'traditional', 'spiritual', 'Daoist framing, energy circulation, inner smile', '☀️', 26),
('breathwork_teacher', 'Breathwork Teacher', 'practice', 'practical', 'neutral', 'Breath instruction clarity + pacing', '🌬️', 27),
('minimalist', 'Minimalist', 'minimal', 'practical', 'neutral', 'Few words, longer silences', '⚪', 28)
ON CONFLICT (lens_slug) DO NOTHING;

-- ADDITIONAL META-LENS PRESETS
INSERT INTO meta_lens_presets (preset_slug, preset_name, icon, description, primary_lens, secondary_lenses, default_scope, default_depth, default_source, default_confidence, is_platform_default, sort_order) VALUES
('balanced_wellness', 'Balanced Wellness', '⚖️', 'Good default - plain physiology + breath teaching', 'physiology_plain', ARRAY['breathwork_teacher'], 'medium', 'pattern', 'individual', 'established', true, 10),
('spiritual_ritual', 'Spiritual Ritual', '🕯️', 'Symbol-heavy, TCM + spiritual framing', 'spiritual', ARRAY['tcm_organs_meridians'], 'wide', 'structural', 'collective', 'traditional', false, 20),
('trauma_safe_regulation', 'Trauma-Safe Regulation', '🛡️', 'Low intensity, long pauses, opt-outs available', 'somatic_trauma_safe', ARRAY['minimalist'], 'narrow', 'behavioral', 'individual', 'established', false, 30),
('athlete_recovery', 'Athlete Recovery', '🏃', 'Recovery framing, practical protocols', 'performance_coach', ARRAY['physiology_plain'], 'focused', 'pattern', 'collective', 'established', false, 40),
('tcm_energy_flow', 'TCM Energy Flow', '☯️', 'Organ/meridian cues, energy circulation', 'tcm_organs_meridians', ARRAY['mantak_chia'], 'medium', 'pattern', 'traditional', 'traditional', false, 50),
('nsdr_protocol', 'NSDR Protocol', '🧠', 'Strict structure, Huberman-style', 'huberman_nsdr', ARRAY['physiology_plain'], 'focused', 'behavioral', 'individual', 'established', false, 60),
('scientific_deep_dive', 'Scientific Deep Dive', '🔬', 'For clinician/researcher view', 'physiology_scientific', ARRAY['breathwork_teacher'], 'focused', 'structural', 'collective', 'frontier', false, 70),
('minimal_words', 'Minimal Words', '⚪', 'Sparse narration, mostly silence', 'minimalist', ARRAY['physiology_plain'], 'narrow', 'behavioral', 'individual', 'established', false, 80)
ON CONFLICT (preset_slug) DO NOTHING;

-- CUE TRIGGERS
INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes) VALUES
('Phase Start Ritual', 'phase_start', NULL, 'Beginning this phase with presence and intention...', 'Proves full array works - add DB refs later'),
('Liver Emphasis Interval', 'interval', 60, 'Feel the flow through your liver space, soft green light...', 'Use with TCM blueprint'),
('NSDR Soft Reminder', 'interval', 90, 'Return to the breath... body heavy, mind quiet...', 'Gentle NSDR prompt'),
('Transition Bell', 'phase_end', NULL, NULL, 'Audio cue marks change')
ON CONFLICT (trigger_name) DO NOTHING;

-- SESSION BLUEPRINTS (Platform Examples)
INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes) VALUES
('Breath Ladder: Box → Fire → NSDR', 'Progressive breath journey from calm to activation to deep rest', 'baseline', true, true, 10, ARRAY['breathwork', 'regulation', 'nsdr'], 'Good demo - shows full system'),
('Trauma-Safe Settle + Long Exhale + NSDR', 'Gentle downregulation for sensitive systems', 'trauma_safe', true, true, 20, ARRAY['trauma-safe', 'regulation', 'gentle'], 'No intensity spikes'),
('NSDR Only (Strict Protocol)', 'Pure NSDR session with Huberman-style cueing', 'baseline', true, true, 30, ARRAY['nsdr', 'rest', 'protocol'], 'Deterministic script'),
('Athlete Downshift: CO2 Tolerance → Soft Stretch', 'Recovery-focused session for athletes', 'baseline', true, true, 40, ARRAY['athlete', 'recovery', 'performance'], 'Recovery-centric framing'),
('TCM Liver Soothe: Breath + Meridian + Movement', 'Organ/color/sound integration with TCM framing', 'baseline', true, true, 50, ARRAY['tcm', 'meridian', 'liver', 'movement'], 'Organs/colour/sound test')
ON CONFLICT (blueprint_name) DO NOTHING;

-- ============================================================
-- SUCCESS MESSAGE
-- ============================================================
DO $$
BEGIN
    RAISE NOTICE '✅ Execution layer schema created successfully!';
    RAISE NOTICE '   - timing_presets: 5 rows';
    RAISE NOTICE '   - session_phases: 7 rows';
    RAISE NOTICE '   - transition_rules: 5 rows';
    RAISE NOTICE '   - narration_styles: 7 rows';
    RAISE NOTICE '   - lens_definitions: +9 rows (supplements existing 14)';
    RAISE NOTICE '   - meta_lens_presets: +8 rows (supplements existing 5)';
    RAISE NOTICE '   - cue_triggers: 4 rows';
    RAISE NOTICE '   - session_blueprints: 5 platform examples';
END $$;

