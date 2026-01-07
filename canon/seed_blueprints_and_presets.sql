-- Seed: timing presets, narration styles, transition rules, cue triggers, session blueprints
-- Generated: 2026-01-04T23:38:46Z

INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, default_pause_sec, notes)
SELECT
  '10-min Reset', 10, 10, 60, 20, 10, 3, 'Short reset session.'
WHERE NOT EXISTS (
  SELECT 1 FROM timing_presets WHERE preset_name = '10-min Reset'
);

INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, default_pause_sec, notes)
SELECT
  '20-min Regulation', 20, 10, 55, 25, 10, 3, 'Standard regulation session.'
WHERE NOT EXISTS (
  SELECT 1 FROM timing_presets WHERE preset_name = '20-min Regulation'
);

INSERT INTO timing_presets (preset_name, total_duration_min, intro_pct, technique_pct, integration_pct, outro_pct, default_pause_sec, notes)
SELECT
  '30-min Deep Restore', 30, 8, 55, 27, 10, 4, 'Extended restore session.'
WHERE NOT EXISTS (
  SELECT 1 FROM timing_presets WHERE preset_name = '30-min Deep Restore'
);

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, pause_between_sentences_sec, notes)
SELECT
  'Spiritual Guide', 'spiritual', 125, 'detailed', 'none', 'light', 1.8, 'Symbolic language, gentle pacing.'
WHERE NOT EXISTS (
  SELECT 1 FROM narration_styles WHERE style_name = 'Spiritual Guide'
);

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, pause_between_sentences_sec, notes)
SELECT
  'Western Coach', 'scientific', 150, 'normal', 'full', 'none', 1.2, 'Mechanism-forward, direct cues.'
WHERE NOT EXISTS (
  SELECT 1 FROM narration_styles WHERE style_name = 'Western Coach'
);

INSERT INTO narration_styles (style_name, voice_tone, reading_pace_wpm, breath_verbosity, physiology_level, tcm_level, pause_between_sentences_sec, notes)
SELECT
  'TCM Storyteller', 'spiritual', 130, 'normal', 'none', 'full', 1.6, 'Organ/meridian framing with imagery.'
WHERE NOT EXISTS (
  SELECT 1 FROM narration_styles WHERE style_name = 'TCM Storyteller'
);

INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, audio_cue, narration_template, notes)
SELECT
  'Soft Fade', 'soft_fade', 5, NULL, 'Allow this to settle... gently shifting now...', 'Gentle transition.'
WHERE NOT EXISTS (
  SELECT 1 FROM transition_rules WHERE rule_name = 'Soft Fade'
);

INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, audio_cue, narration_template, notes)
SELECT
  'Counted Pause', 'counted_pause', 10, NULL, 'Take three breaths here before we continue...', 'Breath-counted gap.'
WHERE NOT EXISTS (
  SELECT 1 FROM transition_rules WHERE rule_name = 'Counted Pause'
);

INSERT INTO transition_rules (rule_name, transition_type, pause_duration_sec, audio_cue, narration_template, notes)
SELECT
  'Bell Marker', 'bell', 3, 'bell', NULL, 'Audio cue marks change.'
WHERE NOT EXISTS (
  SELECT 1 FROM transition_rules WHERE rule_name = 'Bell Marker'
);

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT
  'Heart Coherence Pulse', 'interval', 60, 'Bring attention to the Heart, steady and warm.', 'Organ cue: Heart.'
WHERE NOT EXISTS (
  SELECT 1 FROM cue_triggers WHERE trigger_name = 'Heart Coherence Pulse'
);

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT
  'Lung Expansion Cue', 'interval', 75, 'Let the Lungs widen and lift with each inhale.', 'Organ cue: Lungs.'
WHERE NOT EXISTS (
  SELECT 1 FROM cue_triggers WHERE trigger_name = 'Lung Expansion Cue'
);

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT
  'Liver Flow Cue', 'interval', 90, 'Soften around the Liver, invite smooth flow.', 'Organ cue: Liver.'
WHERE NOT EXISTS (
  SELECT 1 FROM cue_triggers WHERE trigger_name = 'Liver Flow Cue'
);

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT
  'Kidney Calm Cue', 'interval', 90, 'Let the Kidneys feel supported and calm.', 'Organ cue: Kidneys.'
WHERE NOT EXISTS (
  SELECT 1 FROM cue_triggers WHERE trigger_name = 'Kidney Calm Cue'
);

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT
  'Spleen-Stomach Grounding', 'interval', 75, 'Ground the Spleen and Stomach, steady and nourished.', 'Organ cue: Spleen/Stomach.'
WHERE NOT EXISTS (
  SELECT 1 FROM cue_triggers WHERE trigger_name = 'Spleen-Stomach Grounding'
);

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT
  'Brain-Nervous Reset', 'interval', 120, 'Settle the Brain and nervous system into quiet focus.', 'Organ cue: Brain/Nervous System.'
WHERE NOT EXISTS (
  SELECT 1 FROM cue_triggers WHERE trigger_name = 'Brain-Nervous Reset'
);

INSERT INTO session_blueprints (blueprint_name, description, timing_preset_id, narration_style_id, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT
  'Western Reset: Box Breath + Heart Coherence', 'Western lens regulation with Heart/Lung coherence cues.', (SELECT id FROM timing_presets WHERE preset_name = '20-min Regulation' LIMIT 1), (SELECT id FROM narration_styles WHERE style_name = 'Western Coach' LIMIT 1), 'baseline', true, true, 10, ARRAY['western','regulation','heart','lungs'], 'Heart/Lungs emphasis.'
WHERE NOT EXISTS (
  SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Western Reset: Box Breath + Heart Coherence'
);

INSERT INTO session_blueprints (blueprint_name, description, timing_preset_id, narration_style_id, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT
  'TCM Liver Soothe: Meridian Flow', 'TCM lens for Liver flow and emotional easing.', (SELECT id FROM timing_presets WHERE preset_name = '30-min Deep Restore' LIMIT 1), (SELECT id FROM narration_styles WHERE style_name = 'TCM Storyteller' LIMIT 1), 'baseline', true, true, 20, ARRAY['tcm','liver','meridian','restoration'], 'Liver emphasis.'
WHERE NOT EXISTS (
  SELECT 1 FROM session_blueprints WHERE blueprint_name = 'TCM Liver Soothe: Meridian Flow'
);

INSERT INTO session_blueprints (blueprint_name, description, timing_preset_id, narration_style_id, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT
  'Spiritual Grounding: Symbolic Breath', 'Spiritual lens grounding with symbolic cues.', (SELECT id FROM timing_presets WHERE preset_name = '20-min Regulation' LIMIT 1), (SELECT id FROM narration_styles WHERE style_name = 'Spiritual Guide' LIMIT 1), 'baseline', true, true, 30, ARRAY['spiritual','grounding','symbolic'], 'Symbolic framing.'
WHERE NOT EXISTS (
  SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Spiritual Grounding: Symbolic Breath'
);

INSERT INTO session_blueprints (blueprint_name, description, timing_preset_id, narration_style_id, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT
  'Athlete Recovery: CO2 Tolerance + Downshift', 'Performance lens recovery with gentle downshift.', (SELECT id FROM timing_presets WHERE preset_name = '20-min Regulation' LIMIT 1), (SELECT id FROM narration_styles WHERE style_name = 'Western Coach' LIMIT 1), 'baseline', true, true, 40, ARRAY['performance','recovery','athlete'], 'Recovery framing.'
WHERE NOT EXISTS (
  SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Athlete Recovery: CO2 Tolerance + Downshift'
);

INSERT INTO session_blueprints (blueprint_name, description, timing_preset_id, narration_style_id, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT
  'Somatic Safety: Long Exhale + NSDR', 'Somatic lens with long-exhale regulation.', (SELECT id FROM timing_presets WHERE preset_name = '30-min Deep Restore' LIMIT 1), (SELECT id FROM narration_styles WHERE style_name = 'Spiritual Guide' LIMIT 1), 'trauma_safe', true, true, 50, ARRAY['somatic','trauma-safe','nervous-system'], 'Nervous system safety cues.'
WHERE NOT EXISTS (
  SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Somatic Safety: Long Exhale + NSDR'
);

INSERT INTO session_blueprints (blueprint_name, description, timing_preset_id, narration_style_id, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT
  'Neuro Focus: Brain Reset + Calm', 'Scientific lens focus with Brain/Nervous System cues.', (SELECT id FROM timing_presets WHERE preset_name = '10-min Reset' LIMIT 1), (SELECT id FROM narration_styles WHERE style_name = 'Western Coach' LIMIT 1), 'baseline', true, true, 60, ARRAY['scientific','focus','brain','nervous-system'], 'Brain/Nervous System emphasis.'
WHERE NOT EXISTS (
  SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Neuro Focus: Brain Reset + Calm'
);
