-- ============================================================
-- EXECUTION LAYER SEED DATA
-- Run AFTER execution_layer_v2.sql
-- ============================================================

-- TIMING PRESETS
INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, notes) 
SELECT '10-min Quick Reset', 10, 10, 60, 20, 10, 'Short reset session'
WHERE NOT EXISTS (SELECT 1 FROM timing_presets WHERE preset_name = '10-min Quick Reset');

INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, notes) 
SELECT '20-min Regulation', 20, 10, 55, 25, 10, 'Standard regulation session'
WHERE NOT EXISTS (SELECT 1 FROM timing_presets WHERE preset_name = '20-min Regulation');

INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, notes) 
SELECT '30-min Rich Mix', 30, 8, 55, 27, 10, 'Full multi-technique session'
WHERE NOT EXISTS (SELECT 1 FROM timing_presets WHERE preset_name = '30-min Rich Mix');

INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, notes) 
SELECT '45-min Deep Practice', 45, 7, 55, 28, 10, 'Extended practice'
WHERE NOT EXISTS (SELECT 1 FROM timing_presets WHERE preset_name = '45-min Deep Practice');

INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, notes) 
SELECT '60-min Immersive', 60, 5, 55, 30, 10, 'Full immersive experience'
WHERE NOT EXISTS (SELECT 1 FROM timing_presets WHERE preset_name = '60-min Immersive');

-- SESSION PHASES
INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes)
SELECT 'Welcome and Grounding', 'intro', 'low', 60, 180, 'Opening orientation'
WHERE NOT EXISTS (SELECT 1 FROM session_phases WHERE phase_name = 'Welcome and Grounding');

INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes)
SELECT 'Breath Technique Phase', 'technique', 'med', 180, 600, 'Core breathwork'
WHERE NOT EXISTS (SELECT 1 FROM session_phases WHERE phase_name = 'Breath Technique Phase');

INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes)
SELECT 'Movement Integration', 'technique', 'med', 120, 480, 'Body movement'
WHERE NOT EXISTS (SELECT 1 FROM session_phases WHERE phase_name = 'Movement Integration');

INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes)
SELECT 'Deep Rest NSDR', 'integration', 'low', 300, 900, 'Non-sleep deep rest'
WHERE NOT EXISTS (SELECT 1 FROM session_phases WHERE phase_name = 'Deep Rest NSDR');

INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes)
SELECT 'Body Scan', 'integration', 'low', 180, 600, 'Somatic awareness'
WHERE NOT EXISTS (SELECT 1 FROM session_phases WHERE phase_name = 'Body Scan');

INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes)
SELECT 'Meridian Energy Work', 'integration', 'low', 180, 480, 'TCM integration'
WHERE NOT EXISTS (SELECT 1 FROM session_phases WHERE phase_name = 'Meridian Energy Work');

INSERT INTO session_phases (phase_name, phase_type, default_intensity, default_min_duration_sec, default_max_duration_sec, notes)
SELECT 'Closing and Transition', 'outro', 'low', 60, 180, 'Return to activity'
WHERE NOT EXISTS (SELECT 1 FROM session_phases WHERE phase_name = 'Closing and Transition');

-- TRANSITION RULES
INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, narration_template, notes)
SELECT 'Soft Fade', 'soft_fade', 5, 'Allow this to settle... gently shifting now...', 'Gentle transition'
WHERE NOT EXISTS (SELECT 1 FROM transition_rules WHERE rule_name = 'Soft Fade');

INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, narration_template, notes)
SELECT 'Counted Pause', 'counted_pause', 10, 'Take three breaths here before we continue...', 'Breath-counted gap'
WHERE NOT EXISTS (SELECT 1 FROM transition_rules WHERE rule_name = 'Counted Pause');

INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, narration_template, notes)
SELECT 'Bell Transition', 'bell', 3, NULL, 'Audio cue marks change'
WHERE NOT EXISTS (SELECT 1 FROM transition_rules WHERE rule_name = 'Bell Transition');

INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, narration_template, notes)
SELECT 'Breath Bridge', 'breath_bridge', 8, 'Three deep breaths to bridge into the next phase...', 'Active breath transition'
WHERE NOT EXISTS (SELECT 1 FROM transition_rules WHERE rule_name = 'Breath Bridge');

INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, narration_template, notes)
SELECT 'Instant', 'instant', 0, NULL, 'No pause'
WHERE NOT EXISTS (SELECT 1 FROM transition_rules WHERE rule_name = 'Instant');

-- NARRATION STYLES
INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes)
SELECT 'Temple Guide', 'spiritual', 125, 'detailed', 'none', 'light', 'Slow cadence, imagery, soft pacing'
WHERE NOT EXISTS (SELECT 1 FROM narration_styles WHERE style_name = 'Temple Guide');

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes)
SELECT 'Lab Coach', 'scientific', 150, 'normal', 'full', 'none', 'Explanations between cues'
WHERE NOT EXISTS (SELECT 1 FROM narration_styles WHERE style_name = 'Lab Coach');

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes)
SELECT 'Science Coach', 'neutral', 145, 'normal', 'light', 'none', 'Clear, practical, some mechanism'
WHERE NOT EXISTS (SELECT 1 FROM narration_styles WHERE style_name = 'Science Coach');

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes)
SELECT 'TCM Storyteller', 'spiritual', 130, 'normal', 'none', 'full', 'Meridian/organ framing'
WHERE NOT EXISTS (SELECT 1 FROM narration_styles WHERE style_name = 'TCM Storyteller');

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes)
SELECT 'Minimal Timer', 'neutral', 160, 'minimal', 'none', 'none', 'Few words, long silences'
WHERE NOT EXISTS (SELECT 1 FROM narration_styles WHERE style_name = 'Minimal Timer');

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes)
SELECT 'Warm Guide', 'warm', 135, 'normal', 'light', 'light', 'Friendly, supportive tone'
WHERE NOT EXISTS (SELECT 1 FROM narration_styles WHERE style_name = 'Warm Guide');

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, notes)
SELECT 'Spiritual Guide', 'spiritual', 120, 'detailed', 'none', 'none', 'Symbolic, meaning-based'
WHERE NOT EXISTS (SELECT 1 FROM narration_styles WHERE style_name = 'Spiritual Guide');

-- CUE TRIGGERS
INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Phase Start Ritual', 'phase_start', NULL, 'Beginning this phase with presence and intention...', 'Proves full array works'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Phase Start Ritual');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Liver Emphasis Interval', 'interval', 60, 'Feel the flow through your liver space, soft green light...', 'Use with TCM blueprint'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Liver Emphasis Interval');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'NSDR Soft Reminder', 'interval', 90, 'Return to the breath... body heavy, mind quiet...', 'Gentle NSDR prompt'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'NSDR Soft Reminder');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Transition Bell', 'phase_end', NULL, NULL, 'Audio cue marks change'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Transition Bell');

-- SESSION BLUEPRINTS
INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Breath Ladder Box to Fire to NSDR', 'Progressive breath journey from calm to activation to deep rest', 'baseline', true, true, 10, ARRAY['breathwork', 'regulation', 'nsdr'], 'Good demo - shows full system'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Breath Ladder Box to Fire to NSDR');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Trauma-Safe Settle Long Exhale NSDR', 'Gentle downregulation for sensitive systems', 'trauma_safe', true, true, 20, ARRAY['trauma-safe', 'regulation', 'gentle'], 'No intensity spikes'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Trauma-Safe Settle Long Exhale NSDR');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'NSDR Only Strict Protocol', 'Pure NSDR session with Huberman-style cueing', 'baseline', true, true, 30, ARRAY['nsdr', 'rest', 'protocol'], 'Deterministic script'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'NSDR Only Strict Protocol');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Athlete Downshift CO2 Tolerance', 'Recovery-focused session for athletes', 'baseline', true, true, 40, ARRAY['athlete', 'recovery', 'performance'], 'Recovery-centric framing'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Athlete Downshift CO2 Tolerance');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'TCM Liver Soothe Breath Meridian Movement', 'Organ/color/sound integration with TCM framing', 'baseline', true, true, 50, ARRAY['tcm', 'meridian', 'liver', 'movement'], 'Organs/colour/sound test'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'TCM Liver Soothe Breath Meridian Movement');

-- ADDITIONAL LENSES
INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'physiology_plain', 'Physiology Plain', 'perspective', 'scientific', 'neutral', 'Explain what is happening in the body in simple terms', '🫁', 20
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'physiology_plain');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'physiology_scientific', 'Physiology Scientific', 'perspective', 'scientific', 'scientific', 'Clinical/scientific explanation with citations', '🔬', 21
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'physiology_scientific');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'somatic_trauma_safe', 'Somatic Trauma-Safe', 'safety', 'somatic', 'soft', 'Safety-first language, gentle pacing, opt-outs', '🛡️', 23
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'somatic_trauma_safe');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'performance_coach', 'Performance Coach', 'coaching', 'performance', 'direct', 'Training/recovery framing, protocols and timing', '🏋️', 24
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'performance_coach');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'huberman_nsdr', 'Huberman-style NSDR', 'science_comm', 'scientific', 'neutral', 'Clear structure, practical cues, light jargon', '🧠', 25
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'huberman_nsdr');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'mantak_chia', 'Mantak Chia Microcosmic Orbit', 'tcm_daoist', 'traditional', 'spiritual', 'Daoist framing, energy circulation, inner smile', '☀️', 26
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'mantak_chia');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'breathwork_teacher', 'Breathwork Teacher', 'practice', 'practical', 'neutral', 'Breath instruction clarity and pacing', '🌬️', 27
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'breathwork_teacher');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_type, paradigm, output_style, description, icon, sort_order)
SELECT 'minimalist', 'Minimalist', 'minimal', 'practical', 'neutral', 'Few words, longer silences', '⚪', 28
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'minimalist');

-- ADDITIONAL META-LENS PRESETS
INSERT INTO meta_lens_presets (preset_slug, preset_name, icon, description, primary_lens, secondary_lenses, default_scope, default_depth, default_source, default_confidence, is_platform_default, sort_order)
SELECT 'balanced_wellness', 'Balanced Wellness', '⚖️', 'Good default - plain physiology plus breath teaching', 'physiology_plain', ARRAY['breathwork_teacher'], 'medium', 'pattern', 'individual', 'established', true, 10
WHERE NOT EXISTS (SELECT 1 FROM meta_lens_presets WHERE preset_slug = 'balanced_wellness');

INSERT INTO meta_lens_presets (preset_slug, preset_name, icon, description, primary_lens, secondary_lenses, default_scope, default_depth, default_source, default_confidence, is_platform_default, sort_order)
SELECT 'spiritual_ritual', 'Spiritual Ritual', '🕯️', 'Symbol-heavy, TCM plus spiritual framing', 'spiritual', ARRAY['tcm'], 'wide', 'structural', 'collective', 'traditional', false, 20
WHERE NOT EXISTS (SELECT 1 FROM meta_lens_presets WHERE preset_slug = 'spiritual_ritual');

INSERT INTO meta_lens_presets (preset_slug, preset_name, icon, description, primary_lens, secondary_lenses, default_scope, default_depth, default_source, default_confidence, is_platform_default, sort_order)
SELECT 'trauma_safe_regulation', 'Trauma-Safe Regulation', '🛡️', 'Low intensity, long pauses, opt-outs available', 'somatic_trauma_safe', ARRAY['minimalist'], 'narrow', 'behavioral', 'individual', 'established', false, 30
WHERE NOT EXISTS (SELECT 1 FROM meta_lens_presets WHERE preset_slug = 'trauma_safe_regulation');

INSERT INTO meta_lens_presets (preset_slug, preset_name, icon, description, primary_lens, secondary_lenses, default_scope, default_depth, default_source, default_confidence, is_platform_default, sort_order)
SELECT 'athlete_recovery', 'Athlete Recovery', '🏃', 'Recovery framing, practical protocols', 'performance_coach', ARRAY['physiology_plain'], 'focused', 'pattern', 'collective', 'established', false, 40
WHERE NOT EXISTS (SELECT 1 FROM meta_lens_presets WHERE preset_slug = 'athlete_recovery');

INSERT INTO meta_lens_presets (preset_slug, preset_name, icon, description, primary_lens, secondary_lenses, default_scope, default_depth, default_source, default_confidence, is_platform_default, sort_order)
SELECT 'nsdr_protocol', 'NSDR Protocol', '🧠', 'Strict structure, Huberman-style', 'huberman_nsdr', ARRAY['physiology_plain'], 'focused', 'behavioral', 'individual', 'established', false, 60
WHERE NOT EXISTS (SELECT 1 FROM meta_lens_presets WHERE preset_slug = 'nsdr_protocol');

INSERT INTO meta_lens_presets (preset_slug, preset_name, icon, description, primary_lens, secondary_lenses, default_scope, default_depth, default_source, default_confidence, is_platform_default, sort_order)
SELECT 'minimal_words', 'Minimal Words', '⚪', 'Sparse narration, mostly silence', 'minimalist', ARRAY['physiology_plain'], 'narrow', 'behavioral', 'individual', 'established', false, 80
WHERE NOT EXISTS (SELECT 1 FROM meta_lens_presets WHERE preset_slug = 'minimal_words');



