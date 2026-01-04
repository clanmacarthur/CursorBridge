-- ============================================================
-- EXECUTION LAYER SEED (CLEAN - New Tables Only)
-- Run AFTER execution_layer_v2.sql creates the tables
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



