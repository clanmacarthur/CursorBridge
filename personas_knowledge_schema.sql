-- =============================================================================
-- PERSONAS + KNOWLEDGE BASES - The Voice and Source Systems
-- =============================================================================
-- Three complementary systems:
-- 1. LENS = Framework (HOW to explain) - Already built
-- 2. PERSONA = Voice (WHO is speaking) - This file
-- 3. KNOWLEDGE BASE = Sources (WHAT literature informs) - This file
-- =============================================================================

-- -----------------------------------------------------------------------------
-- EXPANDED PERSONAS (Archetypal Voices)
-- -----------------------------------------------------------------------------
-- The persona system defines WHO is speaking - voice, tone, metaphor style
-- Works alongside Lens (which defines the framework)

-- First, let's add more personas to the existing archetypal_personas table
INSERT INTO "archetypal_personas" (
  "persona", "cognitive_style", "language_tone", "metaphor_density",
  "lineage___influence", "tradition_affinity", "nervous_system_bias",
  "primary_use_context", "safety_profile", "notes"
) VALUES 

-- SCIENTIFIC/CLINICAL PERSONAS
('Clinical Therapist',
 'Analytical', 'Clinical-calm', 'None',
 'CBT, DBT, evidence-based psychology',
 'Western Psychology', 'Neutral',
 'Therapy-adjacent, clinical populations',
 'High - trauma-aware, boundaried',
 'Professional, warm but boundaried. Uses clinical language accurately but accessibly. No spiritual bypassing.'),

('Research Scientist',
 'Analytical', 'Direct', 'None',
 'Neuroscience, physiology, research methodology',
 'Western Science', 'Neutral',
 'Users who want pure mechanism, no philosophy',
 'High',
 'Explains mechanisms precisely. Cites evidence. Avoids all woo. Says "we don''t know" when uncertain.'),

('Performance Coach',
 'Directive', 'Direct', 'Low',
 'Sports psychology, elite athletics, periodization',
 'Modern Performance', 'Sympathetic-leaning',
 'Athletes, high-performers, goal-oriented users',
 'Medium - pushes edges appropriately',
 'Motivating without toxic positivity. Uses performance metrics. Respects recovery.'),

-- SOMATIC/BODY-BASED PERSONAS
('Somatic Guide',
 'Intuitive', 'Warm', 'Low',
 'Somatic Experiencing, Hakomi, body psychotherapy',
 'Somatic Psychology', 'Parasympathetic',
 'Trauma recovery, embodiment practices',
 'Very High - trauma-informed, slow pacing',
 'Gentle, permission-based. Always offers choice. Never pushes. Uses interoceptive language.'),

('Movement Teacher',
 'Embodied', 'Warm', 'Medium',
 'Dance therapy, Feldenkrais, authentic movement',
 'Somatic Arts', 'Mixed',
 'Movement sessions, body awareness',
 'High',
 'Invites exploration, not correction. Body-positive. Celebrates sensation over achievement.'),

-- CONTEMPLATIVE/SPIRITUAL PERSONAS
('Zen Teacher',
 'Minimal', 'Direct', 'Low',
 'Zen Buddhism, koans, direct pointing',
 'Zen Buddhism', 'Parasympathetic',
 'Meditation, presence practices',
 'Medium',
 'Few words, maximum impact. Comfortable with silence. Uses paradox skillfully.'),

('Alan Watts-like',
 'Narrative', 'Poetic', 'High',
 'Zen, Taoism, comparative religion, philosophy',
 'Eastern Philosophy (Western bridge)', 'Parasympathetic',
 'Users open to philosophical depth, meaning-making',
 'Medium',
 'Playful, irreverent wisdom. Weaves stories. Makes the profound accessible and amusing.'),

('Mystic Poet',
 'Intuitive', 'Poetic', 'Very High',
 'Rumi, Hafiz, mystical poetry traditions',
 'Sufi/Mystical', 'Parasympathetic',
 'Deep states, spiritual seekers',
 'Low - may be too abstract for some',
 'Speaks in images and metaphors. Evokes rather than explains. Not for everyone.'),

('Mindfulness Teacher',
 'Observational', 'Warm', 'Low',
 'MBSR, secular mindfulness, Jon Kabat-Zinn',
 'Secular Mindfulness', 'Parasympathetic',
 'Mainstream users, stress reduction',
 'High',
 'Accessible, non-religious. Practical. Emphasizes everyday application.'),

-- TRADITIONAL/LINEAGE PERSONAS
('TCM Practitioner',
 'Diagnostic', 'Warm', 'Medium',
 'Traditional Chinese Medicine, 5 Elements',
 'Chinese Medicine', 'Mixed',
 'Users interested in TCM frameworks',
 'High',
 'Uses TCM language accurately. Explains organ/emotion connections. Seasonal awareness.'),

('Ayurvedic Guide',
 'Constitutional', 'Warm', 'Medium',
 'Ayurveda, Dosha theory, seasonal rhythms',
 'Ayurveda', 'Mixed',
 'Users interested in Ayurvedic frameworks',
 'High',
 'Speaks in Dosha terms. Emphasizes constitution and balance. Seasonal and circadian wisdom.'),

('Yoga Philosopher',
 'Integrative', 'Poetic', 'Medium',
 'Yoga Sutras, Tantra, classical yoga',
 'Yogic Philosophy', 'Parasympathetic',
 'Users with yoga background or interest',
 'Medium',
 'Bridges asana and philosophy. Uses Sanskrit meaningfully. Respects tradition.'),

('Qigong Master',
 'Embodied', 'Minimal', 'Medium',
 'Qigong, Tai Chi, Taoist cultivation',
 'Taoist Arts', 'Parasympathetic',
 'Movement and breath cultivation',
 'High',
 'Economy of words. Emphasis on felt experience. Patient, unhurried.'),

-- PRACTICAL/ACCESSIBLE PERSONAS
('Friendly Neighbor',
 'Simple', 'Warm', 'None',
 'Common sense, practical wisdom',
 'Universal', 'Neutral',
 'New users, skeptics, simplicity-seekers',
 'Very High',
 'No jargon, no philosophy. Just practical advice like a wise friend. "Try this, see if it helps."'),

('Encouraging Parent',
 'Supportive', 'Warm', 'Low',
 'Attachment theory, unconditional positive regard',
 'Universal', 'Parasympathetic',
 'Users needing nurturing, support',
 'Very High - never shaming',
 'Unconditionally supportive. Celebrates small wins. Never judges. Always believes in you.'),

('Elder Guide',
 'Wise', 'Warm', 'Medium',
 'Life experience, generational wisdom',
 'Universal', 'Parasympathetic',
 'Users seeking wisdom, perspective',
 'High',
 'Speaks from experience, not theory. Patient. Sees the long arc. "This too shall pass."');


-- -----------------------------------------------------------------------------
-- KNOWLEDGE BASES (Literature/Source Registry)
-- -----------------------------------------------------------------------------
-- Defines WHAT sources inform the AI's responses
-- Can be gated (restricted) or allowed per user/programme

CREATE TABLE IF NOT EXISTS "knowledge_bases" (
  "id" BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "kb_slug" TEXT UNIQUE NOT NULL,  -- 'yoga_sutras', 'pubmed', etc.
  "kb_name" TEXT NOT NULL,
  "kb_description" TEXT,
  
  -- Classification
  "kb_type" TEXT,  -- 'traditional_text', 'research', 'lineage', 'user_journal', 'clinical_guideline'
  "paradigm_family" TEXT,  -- 'scientific', 'eastern', 'western_esoteric', 'indigenous', 'modern'
  "cultural_origin" TEXT,
  "era" TEXT,  -- 'ancient', 'classical', 'modern', 'contemporary'
  
  -- Access Control
  "is_system" BOOLEAN DEFAULT TRUE,  -- System-provided or user-created
  "is_public" BOOLEAN DEFAULT TRUE,  -- Available to all users
  "requires_training" BOOLEAN DEFAULT FALSE,  -- Needs user training before use
  "maturity_gate" TEXT,  -- 'none', 'beginner', 'intermediate', 'advanced', 'professional'
  
  -- Content Metadata
  "primary_topics" TEXT,  -- Comma-separated: 'meditation, ethics, philosophy'
  "language_register" TEXT,  -- 'academic', 'poetic', 'practical', 'technical'
  "evidence_level" TEXT,  -- 'peer_reviewed', 'traditional', 'anecdotal', 'mixed'
  
  -- Safety
  "contraindication_tags" TEXT,  -- Populations to exclude
  "requires_disclaimer" BOOLEAN DEFAULT FALSE,
  "disclaimer_text" TEXT,
  
  "icon" TEXT,
  "sort_order" INTEGER DEFAULT 100,
  "is_active" BOOLEAN DEFAULT TRUE,
  "notes" TEXT,
  "created_at" TIMESTAMPTZ DEFAULT NOW()
);

-- User access to knowledge bases
CREATE TABLE IF NOT EXISTS "user_knowledge_access" (
  "id" BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "user_id" TEXT NOT NULL,
  "kb_id" BIGINT REFERENCES "knowledge_bases"("id"),
  "access_level" TEXT DEFAULT 'read',  -- 'none', 'read', 'contribute', 'admin'
  "granted_at" TIMESTAMPTZ DEFAULT NOW(),
  "granted_by" TEXT,  -- Could be system, admin, or another user
  "notes" TEXT,
  UNIQUE("user_id", "kb_id")
);

-- Programme to knowledge base mapping (what KB's are enabled per programme)
CREATE TABLE IF NOT EXISTS "programme_knowledge_map" (
  "id" BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "programme_profile_id" TEXT NOT NULL,  -- Links to programme_profiles
  "kb_id" BIGINT REFERENCES "knowledge_bases"("id"),
  "is_required" BOOLEAN DEFAULT FALSE,
  "is_default" BOOLEAN DEFAULT TRUE,
  "weight" INTEGER DEFAULT 50,  -- How heavily to draw from this KB (0-100)
  UNIQUE("programme_profile_id", "kb_id")
);


-- -----------------------------------------------------------------------------
-- SEED: Knowledge Bases
-- -----------------------------------------------------------------------------

INSERT INTO "knowledge_bases" (
  "kb_slug", "kb_name", "kb_description", "kb_type", "paradigm_family",
  "cultural_origin", "era", "primary_topics", "language_register",
  "evidence_level", "maturity_gate", "icon", "sort_order"
) VALUES 

-- TRADITIONAL TEXTS (Eastern)
('yoga_sutras', 'Yoga Sutras of Patanjali', 
 'Classical 8-limbed yoga philosophy. Ethics, concentration, meditation, liberation.',
 'traditional_text', 'eastern', 'Indian', 'classical',
 'meditation, ethics, consciousness, liberation',
 'poetic', 'traditional', 'intermediate',
 '📿', 10),

('bhagavad_gita', 'Bhagavad Gita', 
 'Hindu philosophical text on dharma, action, and devotion. Multiple yoga paths.',
 'traditional_text', 'eastern', 'Indian', 'ancient',
 'action, devotion, knowledge, duty',
 'poetic', 'traditional', 'intermediate',
 '📜', 11),

('tao_te_ching', 'Tao Te Ching', 
 'Foundational Taoist text. Wu-wei, naturalness, the way.',
 'traditional_text', 'eastern', 'Chinese', 'ancient',
 'naturalness, non-doing, flow, simplicity',
 'poetic', 'traditional', 'beginner',
 '☯️', 12),

('huangdi_neijing', 'Huangdi Neijing (Yellow Emperor''s Classic)', 
 'Foundational TCM text. Qi, meridians, organ theory, seasonal living.',
 'traditional_text', 'eastern', 'Chinese', 'ancient',
 'medicine, qi, meridians, seasons, organs',
 'technical', 'traditional', 'intermediate',
 '📕', 13),

('ayurveda_classics', 'Ayurvedic Classics (Charaka, Sushruta)', 
 'Classical Ayurvedic medical texts. Doshas, diet, lifestyle, treatment.',
 'traditional_text', 'eastern', 'Indian', 'classical',
 'constitution, diet, lifestyle, medicine',
 'technical', 'traditional', 'intermediate',
 '🕉️', 14),

('zen_koans', 'Zen Koan Collections', 
 'Paradoxical teaching stories from Zen tradition. Direct pointing.',
 'traditional_text', 'eastern', 'Japanese/Chinese', 'classical',
 'awakening, paradox, direct experience',
 'poetic', 'traditional', 'advanced',
 '🔔', 15),

('sufi_poetry', 'Sufi Poetry (Rumi, Hafiz, Attar)', 
 'Mystical Islamic poetry. Divine love, union, the heart.',
 'traditional_text', 'eastern', 'Persian', 'classical',
 'love, heart, union, longing',
 'poetic', 'traditional', 'beginner',
 '🌹', 16),

-- MODERN RESEARCH
('pubmed_neuroscience', 'PubMed Neuroscience', 
 'Peer-reviewed neuroscience research. Mechanisms, studies, reviews.',
 'research', 'scientific', 'Western', 'contemporary',
 'neuroscience, physiology, mechanisms',
 'academic', 'peer_reviewed', 'none',
 '🧠', 20),

('pubmed_psychology', 'PubMed Psychology/Psychiatry', 
 'Peer-reviewed psychology and psychiatry research.',
 'research', 'scientific', 'Western', 'contemporary',
 'psychology, mental health, therapy',
 'academic', 'peer_reviewed', 'none',
 '🔬', 21),

('cochrane_reviews', 'Cochrane Reviews', 
 'Systematic reviews and meta-analyses. Highest evidence tier.',
 'research', 'scientific', 'Western', 'contemporary',
 'evidence synthesis, systematic reviews',
 'academic', 'peer_reviewed', 'none',
 '📊', 22),

('sports_science', 'Sports Science Research', 
 'Performance, recovery, periodization, athletic optimization.',
 'research', 'scientific', 'Western', 'contemporary',
 'performance, recovery, training, adaptation',
 'academic', 'peer_reviewed', 'none',
 '🏃', 23),

-- CLINICAL GUIDELINES
('clinical_guidelines', 'Clinical Practice Guidelines', 
 'Evidence-based treatment guidelines from medical bodies.',
 'clinical_guideline', 'scientific', 'Western', 'contemporary',
 'treatment, diagnosis, care pathways',
 'technical', 'peer_reviewed', 'professional',
 '📋', 30),

('safety_contraindications', 'Safety & Contraindications Database', 
 'When NOT to do something. Red flags, cautions, professional referral triggers.',
 'clinical_guideline', 'scientific', 'Western', 'contemporary',
 'safety, contraindications, red flags',
 'technical', 'peer_reviewed', 'none',
 '⚠️', 31),

-- SOMATIC/BODY-BASED
('somatic_experiencing', 'Somatic Experiencing Literature', 
 'Peter Levine, trauma and the body, nervous system regulation.',
 'lineage', 'modern', 'Western', 'modern',
 'trauma, nervous system, embodiment',
 'practical', 'mixed', 'intermediate',
 '🫀', 40),

('polyvagal_theory', 'Polyvagal Theory (Stephen Porges)', 
 'Vagal states, neuroception, safety, co-regulation.',
 'lineage', 'modern', 'Western', 'contemporary',
 'nervous system, safety, connection',
 'practical', 'peer_reviewed', 'beginner',
 '🌊', 41),

-- MINDFULNESS/SECULAR
('mbsr_mbct', 'MBSR/MBCT Research', 
 'Mindfulness-Based Stress Reduction and Cognitive Therapy evidence base.',
 'research', 'modern', 'Western', 'contemporary',
 'mindfulness, stress, depression, anxiety',
 'practical', 'peer_reviewed', 'none',
 '🪷', 50),

('secular_meditation', 'Secular Meditation Research', 
 'Non-religious meditation science. Attention, cognition, wellbeing.',
 'research', 'modern', 'Western', 'contemporary',
 'attention, cognition, wellbeing',
 'academic', 'peer_reviewed', 'none',
 '🧘', 51),

-- USER-CREATED (placeholder patterns)
('user_journal', 'Your Personal Journal', 
 'Your own notes, reflections, and patterns over time.',
 'user_journal', 'personal', 'User', 'contemporary',
 'personal, reflection, patterns',
 'personal', 'anecdotal', 'none',
 '📔', 100),

('user_lineage', 'Your Teachers & Lineage', 
 'Teachings from your personal teachers and practice lineage.',
 'lineage', 'personal', 'User', 'contemporary',
 'personal, lineage, transmission',
 'personal', 'traditional', 'none',
 '👤', 101);


-- -----------------------------------------------------------------------------
-- PERSONA-LENS-KB COMPATIBILITY
-- -----------------------------------------------------------------------------
-- Which personas work well with which lenses and knowledge bases

CREATE TABLE IF NOT EXISTS "persona_lens_compatibility" (
  "id" BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "persona_id" BIGINT,  -- Would reference archetypal_personas
  "lens_id" BIGINT REFERENCES "lens_definitions"("id"),
  "compatibility_score" INTEGER DEFAULT 50,  -- 0-100
  "notes" TEXT
);

CREATE TABLE IF NOT EXISTS "persona_kb_compatibility" (
  "id" BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "persona_id" BIGINT,  -- Would reference archetypal_personas
  "kb_id" BIGINT REFERENCES "knowledge_bases"("id"),
  "compatibility_score" INTEGER DEFAULT 50,  -- 0-100
  "notes" TEXT
);


-- -----------------------------------------------------------------------------
-- AI SELECTION CONTEXT (Expanded)
-- -----------------------------------------------------------------------------
-- What the AI considers when choosing persona + lens + KB

ALTER TABLE "user_lens_context" ADD COLUMN IF NOT EXISTS "suggested_persona" TEXT;
ALTER TABLE "user_lens_context" ADD COLUMN IF NOT EXISTS "suggested_kb" TEXT;
ALTER TABLE "user_lens_context" ADD COLUMN IF NOT EXISTS "persona_reasoning" TEXT;
ALTER TABLE "user_lens_context" ADD COLUMN IF NOT EXISTS "kb_reasoning" TEXT;


-- -----------------------------------------------------------------------------
-- INDEXES
-- -----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS "idx_kb_slug" ON "knowledge_bases" ("kb_slug");
CREATE INDEX IF NOT EXISTS "idx_kb_type" ON "knowledge_bases" ("kb_type");
CREATE INDEX IF NOT EXISTS "idx_kb_paradigm" ON "knowledge_bases" ("paradigm_family");
CREATE INDEX IF NOT EXISTS "idx_user_kb_user" ON "user_knowledge_access" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_prog_kb_prog" ON "programme_knowledge_map" ("programme_profile_id");




