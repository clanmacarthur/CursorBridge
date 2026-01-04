-- ============================================================
-- CONTENT ENRICHMENT: More Techniques, Steps, Cues, and Content
-- Run in Supabase SQL Editor
-- ============================================================

-- ============================================================
-- 1. MORE TECHNIQUES
-- ============================================================

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Box Breathing', 'box-breathing', 'breathwork', 'Equal inhale, hold, exhale, hold pattern for nervous system regulation', 5, 'low', 'parasympathetic', 'Safe for most users. Stop if dizzy.', 
'Box breathing activates the parasympathetic nervous system through extended exhales and breath holds, reducing cortisol and heart rate variability.',
'Box breathing harmonizes the flow of Qi through steady rhythm, calming Shen (spirit) and grounding the Heart.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'box-breathing');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Wim Hof Breathing', 'wim-hof', 'breathwork', 'Cyclic hyperventilation followed by breath retention for stress resilience', 10, 'high', 'sympathetic', 'Not for pregnant, cardiovascular issues, or epilepsy. Practice seated/lying.',
'Wim Hof breathing induces controlled hypoxia and respiratory alkalosis, triggering adrenaline release and cold-shock protein production.',
'This vigorous breath stokes the Kidney Yang fire, mobilizing Wei Qi (defensive energy) and clearing stagnation from all channels.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'wim-hof');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Physiological Sigh', 'physiological-sigh', 'breathwork', 'Double inhale through nose, long exhale for rapid calm', 2, 'low', 'parasympathetic', 'Safe for all. Can use anytime.',
'The double inhale reinflates collapsed alveoli, optimizing CO2 offloading. The extended exhale activates vagal tone.',
'Quick settling of agitated Qi. The double breath gathers scattered energy, the long exhale releases excess heat and tension.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'physiological-sigh');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Alternate Nostril Breathing', 'nadi-shodhana', 'breathwork', 'Alternating breath through left and right nostrils for balance', 8, 'low', 'balanced', 'Safe for most. Avoid with severe congestion.',
'Alternating nostril breathing balances left-right brain hemisphere activity and normalizes blood pressure through vagal stimulation.',
'Nadi Shodhana purifies the Ida and Pingala channels, harmonizing lunar (cooling) and solar (warming) energies for Sushumna activation.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'nadi-shodhana');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Inner Smile Meditation', 'inner-smile', 'meditation', 'Taoist practice of directing loving awareness to internal organs', 10, 'low', 'parasympathetic', 'Safe for all. Gentle practice.',
'The inner smile practice activates positive emotional circuits and may reduce inflammatory markers through psychoneuroimmunological pathways.',
'The Inner Smile nourishes each organ with loving Qi: Heart receives joy, Liver receives kindness, Spleen receives trust, Lungs receive courage, Kidneys receive gentleness.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'inner-smile');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Six Healing Sounds', 'six-healing-sounds', 'breathwork', 'Mantak Chia practice pairing sounds with organ healing', 15, 'low', 'balanced', 'Safe for all. Practice gently.',
'Vocalization with specific mouth shapes creates distinct vibrational frequencies that may influence vagal tone and organ blood flow.',
'Each sound releases trapped emotions: SSSSS (Lungs/grief), WHOOOO (Kidneys/fear), SHHHHH (Liver/anger), HAWWWW (Heart/hate), WHOOOOO (Spleen/worry), HEEEEE (Triple Warmer).'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'six-healing-sounds');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Body Scan', 'body-scan', 'meditation', 'Progressive attention through body regions for somatic awareness', 15, 'low', 'parasympathetic', 'Safe for all. Modify for trauma history.',
'Body scanning increases interoceptive awareness, activating the insular cortex and promoting parasympathetic dominance.',
'The body scan circulates Yi (intention) through the flesh, releasing blocked Qi and inviting fresh vitality into neglected areas.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'body-scan');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Microcosmic Orbit', 'microcosmic-orbit', 'meditation', 'Circulating energy through Governing and Conception vessels', 20, 'med', 'balanced', 'Practice gently. Stop if uncomfortable.',
'The Microcosmic Orbit practice may influence autonomic tone through focused attention on midline body regions and rhythmic breathing.',
'Energy ascends the Du Mai (Governing Vessel) up the spine, descends the Ren Mai (Conception Vessel) down the front, completing the Small Heavenly Circuit.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'microcosmic-orbit');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Grounding Visualization', 'grounding', 'meditation', 'Imagining roots growing from body into earth', 5, 'low', 'parasympathetic', 'Safe for all. Good for anxiety.',
'Grounding practices shift attention away from rumination, activating present-moment awareness circuits and reducing amygdala activity.',
'Grounding draws Earth Qi upward through the Yongquan (Kidney 1) points, stabilizing the Shen and anchoring scattered energy.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'grounding');

INSERT INTO techniques (technique_name, technique_slug, category, description, default_duration_min, intensity_level, nervous_system_effect, safety_notes, lens_explanation_western, lens_explanation_tcm)
SELECT 'Gentle Spinal Waves', 'spinal-waves', 'movement', 'Undulating movement through the spine for flexibility and release', 8, 'low', 'balanced', 'Move slowly. Stop if pain.',
'Spinal waves mobilize intervertebral joints, stimulate cerebrospinal fluid flow, and release paraspinal muscle tension.',
'Spinal waves open the Du Mai channel, releasing stagnation along the spine and promoting free flow of Yang Qi.'
WHERE NOT EXISTS (SELECT 1 FROM techniques WHERE technique_slug = 'spinal-waves');

-- ============================================================
-- 2. TECHNIQUE STEPS (Link techniques to phases)
-- ============================================================

-- Get phase IDs for linking
INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Box Breathing Introduction', 1, 60, 120, 'low', 'We begin with box breathing. Inhale for 4 counts, hold for 4, exhale for 4, hold for 4. Find your rhythm.', 'Opening step'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Box Breathing Introduction');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Box Breathing Main Practice', 2, 180, 420, 'low', 'Continue the box pattern. Each breath cycle takes about 16 seconds. Stay present with each phase.', 'Core practice'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Box Breathing Main Practice');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Physiological Sigh Reset', 1, 30, 60, 'low', 'Take a double inhale through your nose - one breath, then a second small sip. Now exhale slowly through your mouth.', 'Quick reset'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Physiological Sigh Reset');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'NSDR Induction', 1, 120, 180, 'low', 'Allow your body to become heavy. Release any effort. You have nowhere to go, nothing to do.', 'NSDR opening'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'NSDR Induction');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'NSDR Body Rotation', 2, 300, 600, 'low', 'Bring your awareness to your right hand thumb... index finger... middle finger... Each body part releases as you name it.', 'Yoga Nidra rotation'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'NSDR Body Rotation');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'NSDR Integration', 3, 120, 240, 'low', 'Rest in this spacious awareness. Nothing to change. Simply being.', 'NSDR closing'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'NSDR Integration');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Inner Smile Opening', 1, 60, 120, 'low', 'Bring a gentle smile to your face. Feel how this softens your eyes, your jaw, your whole being.', 'Inner Smile intro'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Inner Smile Opening');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Inner Smile Organ Journey', 2, 300, 600, 'low', 'Direct your inner smile to your heart... feel gratitude and joy spreading... now to your lungs... courage and openness...', 'Organ sequence'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Inner Smile Organ Journey');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Wim Hof Round 1', 1, 180, 240, 'high', '30 deep breaths: fully in, letting go. After 30, exhale and hold. When you need to breathe, inhale fully and hold 15 seconds.', 'First WHM round'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Wim Hof Round 1');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Wim Hof Recovery', 2, 60, 120, 'low', 'Return to normal breathing. Notice the tingling, the aliveness. Allow your system to integrate.', 'WHM recovery'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Wim Hof Recovery');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Grounding Roots', 1, 120, 300, 'low', 'Imagine roots growing from the base of your spine, down through your legs, deep into the earth. Feel the stability.', 'Grounding practice'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Grounding Roots');

INSERT INTO technique_steps (step_name, step_order, min_duration_sec, max_duration_sec, intensity_target, instructions_template, notes)
SELECT 'Closing Stillness', 1, 60, 180, 'low', 'Rest in stillness. Allow all practice to integrate. When ready, begin to deepen your breath.', 'Session closing'
WHERE NOT EXISTS (SELECT 1 FROM technique_steps WHERE step_name = 'Closing Stillness');

-- ============================================================
-- 3. MORE CUE TRIGGERS (Sound, Color, Organ references)
-- ============================================================

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Heart Opening Cue', 'interval', 120, 'Feel your heart space expanding with each breath. Soft rose light.', 'Heart chakra cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Heart Opening Cue');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Grounding Earth Cue', 'interval', 90, 'Feel your connection to the earth. Stable. Supported. Present.', 'Root chakra cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Grounding Earth Cue');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Kidney Water Cue', 'interval', 60, 'Deep blue light pooling in your lower back. The Kidneys hold your vital essence.', 'Kidney/water element cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Kidney Water Cue');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Lung Metal Cue', 'interval', 60, 'White light filling your chest with each inhale. The Lungs receive pure Qi.', 'Lung/metal element cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Lung Metal Cue');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Spleen Earth Cue', 'interval', 60, 'Golden yellow warmth in your center. The Spleen transforms and nourishes.', 'Spleen/earth element cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Spleen Earth Cue');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Third Eye Activation', 'phase_start', NULL, 'Bring your awareness to the point between your eyebrows. Indigo light.', 'Ajna chakra cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Third Eye Activation');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Sacral Flow Cue', 'interval', 90, 'Orange warmth below your navel. Creativity and flow.', 'Sacral chakra cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Sacral Flow Cue');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Crown Opening', 'phase_end', NULL, 'Violet light at the crown of your head, opening to receive.', 'Crown chakra cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Crown Opening');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'Singing Bowl Tone', 'phase_start', NULL, 'A resonant tone marks this transition. Let it wash through you.', 'Sound cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'Singing Bowl Tone');

INSERT INTO cue_triggers (trigger_name, trigger_scope, interval_sec, narration_text, notes)
SELECT 'OM Vibration', 'interval', 180, 'The sound of OM vibrating through your entire being.', 'Sacred sound cue'
WHERE NOT EXISTS (SELECT 1 FROM cue_triggers WHERE trigger_name = 'OM Vibration');

-- ============================================================
-- 4. MORE SESSION BLUEPRINTS
-- ============================================================

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Inner Smile + NSDR Journey', 'Taoist organ loving-kindness flowing into deep rest', 'baseline', true, true, 60, ARRAY['taoist', 'meditation', 'nsdr', 'organs'], 'Mantak Chia meets Huberman'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Inner Smile + NSDR Journey');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Wim Hof Activation + Recovery', 'Intense breathwork followed by grounding and rest', 'baseline', true, true, 70, ARRAY['wim-hof', 'activation', 'recovery'], 'For experienced practitioners'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Wim Hof Activation + Recovery');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Chakra Journey Full Spectrum', 'Progressive movement through all seven energy centers', 'baseline', true, true, 80, ARRAY['chakra', 'energy', 'meditation'], 'Full chakra activation'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Chakra Journey Full Spectrum');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Five Element Balance', 'TCM organ journey through Wood, Fire, Earth, Metal, Water', 'baseline', true, true, 90, ARRAY['tcm', 'elements', 'organs'], 'Complete element cycle'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Five Element Balance');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Morning Energizer', 'Quick activation breath followed by grounding', 'baseline', true, true, 100, ARRAY['morning', 'energy', 'quick'], '10-minute morning routine'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Morning Energizer');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Evening Wind-Down', 'Gentle breathing and body scan for sleep preparation', 'baseline', true, true, 110, ARRAY['evening', 'sleep', 'relaxation'], 'Pre-sleep protocol'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Evening Wind-Down');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Anxiety SOS Protocol', 'Rapid calming with physiological sighs and grounding', 'trauma_safe', true, true, 120, ARRAY['anxiety', 'sos', 'quick', 'trauma-safe'], 'Emergency calm-down'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Anxiety SOS Protocol');

INSERT INTO session_blueprints (blueprint_name, description, safety_level, is_platform_example, is_published, sort_order, tags, notes)
SELECT 'Microcosmic Orbit Meditation', 'Traditional Taoist energy circulation practice', 'baseline', true, true, 130, ARRAY['taoist', 'energy', 'advanced'], 'Advanced Taoist practice'
WHERE NOT EXISTS (SELECT 1 FROM session_blueprints WHERE blueprint_name = 'Microcosmic Orbit Meditation');

-- ============================================================
-- 5. ADDITIONAL LENSES (Using correct column names)
-- ============================================================

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'trauma_informed', 'Trauma-Informed', 'Safety-first language with opt-outs and gentle pacing', 'somatic', 'soft', 'western', true, true, '🛡️', 30
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'trauma_informed');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'taoist', 'Taoist/Daoist', 'Wu wei, natural flow, effortless action framing', 'traditional', 'poetic', 'chinese', true, true, '☯️', 31
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'taoist');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'buddhist', 'Buddhist/Mindfulness', 'Present-moment awareness, impermanence, non-attachment', 'contemplative', 'clear', 'indian', true, true, '🪷', 32
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'buddhist');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'shamanic', 'Shamanic/Indigenous', 'Nature spirits, ancestors, elemental forces', 'spiritual', 'evocative', 'indigenous', true, true, '🦅', 33
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'shamanic');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'stoic', 'Stoic/Philosophical', 'Virtue, discipline, acceptance of what cannot be changed', 'philosophical', 'direct', 'greek', true, true, '🏛️', 34
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'stoic');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'sufi', 'Sufi/Mystical', 'Divine love, heart opening, ecstatic union', 'mystical', 'poetic', 'persian', true, true, '💫', 35
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'sufi');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'neuroscience', 'Neuroscience', 'Brain regions, neurotransmitters, neural pathways', 'scientific', 'technical', 'western', true, true, '🧠', 36
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'neuroscience');

INSERT INTO lens_definitions (lens_slug, lens_name, lens_description, paradigm_family, language_style, cultural_origin, is_system, is_active, icon, sort_order)
SELECT 'poetic', 'Poetic/Metaphorical', 'Rich imagery, metaphor, emotional resonance', 'artistic', 'poetic', 'universal', true, true, '✒️', 37
WHERE NOT EXISTS (SELECT 1 FROM lens_definitions WHERE lens_slug = 'poetic');

-- ============================================================
-- 6. MORE KNOWLEDGE BASES
-- ============================================================

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'greek_philosophy', 'Greek Philosophy', 'literature', 'Stoics, Epicureans, Plato, Aristotle on wellbeing', 'Greek', false, true, '🏛️', 30
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'greek_philosophy');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'celtic_wisdom', 'Celtic/Druidic Wisdom', 'literature', 'Nature cycles, tree lore, seasonal practices', 'Celtic', false, true, '🌳', 31
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'celtic_wisdom');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'egyptian_mysteries', 'Egyptian Mysteries', 'literature', 'Book of the Dead, Emerald Tablets, hermetic wisdom', 'Egyptian', false, true, '𓂀', 32
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'egyptian_mysteries');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'norse_mythology', 'Norse Mythology', 'literature', 'Eddas, runes, Norse cosmology', 'Norse', false, true, '⚡', 33
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'norse_mythology');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'kabbalah', 'Kabbalah/Jewish Mysticism', 'literature', 'Tree of Life, Sefirot, mystical Judaism', 'Jewish', false, true, '✡️', 34
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'kabbalah');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'christian_mystics', 'Christian Mysticism', 'literature', 'Desert Fathers, Meister Eckhart, contemplative Christianity', 'Christian', false, true, '✝️', 35
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'christian_mystics');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'shamanic_traditions', 'Shamanic Traditions', 'literature', 'Indigenous healing practices from various cultures', 'Indigenous', false, true, '🦅', 36
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'shamanic_traditions');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'astrology_systems', 'Astrological Systems', 'reference', 'Western, Vedic, Chinese astrology frameworks', 'Various', false, true, '⭐', 40
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'astrology_systems');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'tarot_arcana', 'Tarot Arcana', 'reference', 'Major and Minor Arcana meanings and interpretations', 'Western Esoteric', false, true, '🃏', 41
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'tarot_arcana');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'i_ching', 'I Ching', 'literature', 'Book of Changes, hexagrams, Chinese divination wisdom', 'Chinese', false, true, '☰', 42
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'i_ching');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'mythology_world', 'World Mythology', 'literature', 'Comparative mythology across cultures', 'Universal', false, true, '🌍', 43
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'mythology_world');

INSERT INTO knowledge_bases (kb_slug, kb_name, kb_type, description, source_tradition, requires_permission, is_active, icon, sort_order)
SELECT 'fairy_tales', 'Fairy Tales & Folklore', 'literature', 'Archetypal stories, Jungian interpretations', 'Universal', false, true, '📖', 44
WHERE NOT EXISTS (SELECT 1 FROM knowledge_bases WHERE kb_slug = 'fairy_tales');

-- ============================================================
-- SUCCESS MESSAGE
-- ============================================================

SELECT 'Content enrichment complete!' as status,
       (SELECT COUNT(*) FROM techniques) as techniques,
       (SELECT COUNT(*) FROM technique_steps) as technique_steps,
       (SELECT COUNT(*) FROM cue_triggers) as cue_triggers,
       (SELECT COUNT(*) FROM session_blueprints) as blueprints,
       (SELECT COUNT(*) FROM lens_definitions) as lenses,
       (SELECT COUNT(*) FROM knowledge_bases) as knowledge_bases;



