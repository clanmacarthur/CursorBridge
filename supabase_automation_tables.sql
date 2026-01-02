-- ============================================================================
-- CursorBridge: Automation Backbone Tables
-- Missing databases from README_MASTER_CANONICAL.md Section 2.2
-- ============================================================================
-- Run this in Supabase SQL Editor after the core library tables exist
-- ============================================================================

-- ============================================================================
-- 1. CONTROL DEFINITIONS (DB)
-- Canonical list of every knob/tick the UI can render
-- ============================================================================
CREATE TABLE IF NOT EXISTS control_definitions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Core fields
    control_name TEXT NOT NULL,
    control_type TEXT NOT NULL DEFAULT 'slider', -- slider | checkbox | knob | hybrid | number | text | time
    
    -- Domain mapping
    primary_domain TEXT, -- FK to attribute_taxonomy via notion_page_id
    secondary_domains TEXT[], -- Array of attribute taxonomy notion_page_ids
    
    -- Range/config
    range_min NUMERIC DEFAULT 0,
    range_max NUMERIC DEFAULT 10,
    range_step NUMERIC DEFAULT 1,
    default_value NUMERIC DEFAULT 5,
    unit TEXT, -- minutes, hours, ml, %, score, etc.
    
    -- UI hints
    label TEXT,
    description TEXT,
    icon TEXT,
    color TEXT,
    
    -- Behavior
    is_required BOOLEAN DEFAULT false,
    is_default BOOLEAN DEFAULT false, -- Include in default dashboard
    completion_threshold NUMERIC, -- Value above which counts as "completed"
    
    -- Metadata
    status TEXT DEFAULT 'active', -- active | deprecated | archived
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_control_definitions_type ON control_definitions(control_type);
CREATE INDEX idx_control_definitions_domain ON control_definitions(primary_domain);

COMMENT ON TABLE control_definitions IS 'Canonical list of every knob/tick the UI can render. One control = one meaning.';

-- ============================================================================
-- 2. CONTROL PACKS (DB)
-- Curated bundles of controls (Insomnia Essentials, Endurance Daily, etc.)
-- ============================================================================
CREATE TABLE IF NOT EXISTS control_packs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Core fields
    pack_name TEXT NOT NULL,
    pack_slug TEXT UNIQUE NOT NULL, -- URL-safe identifier
    description TEXT,
    
    -- Categorization
    category TEXT, -- wellness | fitness | nutrition | sleep | stress | custom
    difficulty TEXT DEFAULT 'beginner', -- beginner | intermediate | advanced
    
    -- UI
    icon TEXT,
    color TEXT,
    display_order INTEGER DEFAULT 0,
    
    -- Behavior
    is_public BOOLEAN DEFAULT true,
    is_default BOOLEAN DEFAULT false,
    
    -- Metadata
    status TEXT DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_control_packs_category ON control_packs(category);
CREATE INDEX idx_control_packs_slug ON control_packs(pack_slug);

COMMENT ON TABLE control_packs IS 'Curated bundles of controls for drag/drop dashboard building.';

-- ============================================================================
-- 2a. CONTROL PACK ITEMS (Join table: control_packs ↔ control_definitions)
-- ============================================================================
CREATE TABLE IF NOT EXISTS control_pack_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    pack_id UUID NOT NULL REFERENCES control_packs(id) ON DELETE CASCADE,
    control_id UUID NOT NULL REFERENCES control_definitions(id) ON DELETE CASCADE,
    
    -- Order within pack
    display_order INTEGER DEFAULT 0,
    
    -- Override defaults for this pack context
    override_default_value NUMERIC,
    override_range_min NUMERIC,
    override_range_max NUMERIC,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(pack_id, control_id)
);

CREATE INDEX idx_control_pack_items_pack ON control_pack_items(pack_id);
CREATE INDEX idx_control_pack_items_control ON control_pack_items(control_id);

COMMENT ON TABLE control_pack_items IS 'Join table linking control packs to their controls.';

-- ============================================================================
-- 3. PROGRAMME PROFILE ↔ PACK MAP (DB)
-- Default packs per programme profile
-- ============================================================================
CREATE TABLE IF NOT EXISTS profile_pack_map (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Relations (store notion_page_id for Notion compatibility)
    programme_profile_id TEXT NOT NULL, -- FK to programme_profiles.notion_page_id
    pack_id UUID REFERENCES control_packs(id) ON DELETE CASCADE,
    
    -- Priority/ordering
    display_order INTEGER DEFAULT 0,
    is_required BOOLEAN DEFAULT false, -- Pack is mandatory for this profile
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_profile_pack_map_profile ON profile_pack_map(programme_profile_id);
CREATE INDEX idx_profile_pack_map_pack ON profile_pack_map(pack_id);

COMMENT ON TABLE profile_pack_map IS 'Maps programme profiles to their default control packs.';

-- ============================================================================
-- 4. DEFAULT WEIGHTS (DB)
-- Out-of-box weighting distributions per profile
-- ============================================================================
CREATE TABLE IF NOT EXISTS default_weights (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Relations
    programme_profile_id TEXT NOT NULL, -- FK to programme_profiles.notion_page_id
    attribute_id TEXT NOT NULL, -- FK to attribute_taxonomy.notion_page_id
    
    -- Weight value
    weight NUMERIC NOT NULL DEFAULT 1.0, -- 0.0 to 1.0 typically
    weight_label TEXT, -- "high", "medium", "low" for UI
    
    -- Context
    domain TEXT, -- recovery | nutrition | movement | sleep | stress | cognitive
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(programme_profile_id, attribute_id)
);

CREATE INDEX idx_default_weights_profile ON default_weights(programme_profile_id);
CREATE INDEX idx_default_weights_attribute ON default_weights(attribute_id);
CREATE INDEX idx_default_weights_domain ON default_weights(domain);

COMMENT ON TABLE default_weights IS 'Baseline weighting distributions per programme profile.';

-- ============================================================================
-- 5. COUPLING RULES / INFLUENCE GRAPH (DB)
-- The "sliders affect other sliders" engine
-- ============================================================================
CREATE TABLE IF NOT EXISTS coupling_rules (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Rule name
    rule_name TEXT NOT NULL,
    
    -- Source (what triggers the effect)
    from_control_id UUID REFERENCES control_definitions(id),
    from_attribute_id TEXT, -- Alternative: attribute_taxonomy.notion_page_id
    from_metric TEXT, -- Or a derived metric name
    
    -- Target (what is affected)
    to_control_id UUID REFERENCES control_definitions(id),
    to_attribute_id TEXT,
    to_metric TEXT,
    
    -- Effect definition
    function_type TEXT NOT NULL DEFAULT 'linear', -- linear | threshold | conditional | decay | inverse | step
    direction TEXT DEFAULT 'positive', -- positive | negative | conditional
    magnitude NUMERIC DEFAULT 1.0, -- Strength of effect (0.0 to 2.0 typically)
    
    -- Threshold rules (for threshold/conditional types)
    threshold_value NUMERIC,
    threshold_comparator TEXT, -- >= | <= | = | between | above | below
    threshold_high NUMERIC, -- For "between" type
    
    -- Conditional rules
    condition_expression TEXT, -- JSON or simple expression for complex rules
    
    -- Context
    applies_to_profiles TEXT[], -- Array of programme_profile notion_page_ids (empty = all)
    
    -- Priority (for conflict resolution)
    priority INTEGER DEFAULT 0,
    
    -- Metadata
    evidence_confidence TEXT DEFAULT 'moderate', -- strong | moderate | emerging | traditional
    notes TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_coupling_rules_from_control ON coupling_rules(from_control_id);
CREATE INDEX idx_coupling_rules_to_control ON coupling_rules(to_control_id);
CREATE INDEX idx_coupling_rules_function ON coupling_rules(function_type);

COMMENT ON TABLE coupling_rules IS 'Defines how controls/metrics influence each other. Core of the adaptive engine.';

-- ============================================================================
-- 6. DERIVED METRICS (DB)
-- Computed metrics from raw check-ins + coupling rules
-- ============================================================================
CREATE TABLE IF NOT EXISTS derived_metrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Core fields
    metric_name TEXT NOT NULL UNIQUE,
    metric_slug TEXT NOT NULL UNIQUE, -- URL-safe identifier
    description TEXT,
    
    -- Computation
    formula_type TEXT NOT NULL DEFAULT 'weighted_average', -- weighted_average | sum | min | max | custom
    formula_expression TEXT, -- JSON formula definition or custom expression
    
    -- Input controls (what feeds this metric)
    input_control_ids UUID[], -- Array of control_definitions.id
    input_weights JSONB, -- {"control_id": weight, ...}
    
    -- Output range
    output_min NUMERIC DEFAULT 0,
    output_max NUMERIC DEFAULT 100,
    unit TEXT DEFAULT 'score',
    
    -- Thresholds for interpretation
    threshold_low NUMERIC DEFAULT 30,
    threshold_medium NUMERIC DEFAULT 60,
    threshold_high NUMERIC DEFAULT 80,
    
    -- Domain
    domain TEXT, -- recovery | sleep_quality | nutrition_quality | stress_load | etc.
    
    -- Metadata
    notes TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_derived_metrics_domain ON derived_metrics(domain);
CREATE INDEX idx_derived_metrics_slug ON derived_metrics(metric_slug);

COMMENT ON TABLE derived_metrics IS 'Computed metrics like Sleep Adequacy, Recovery Strain, Nutrition Quality.';

-- ============================================================================
-- 7. QUESTIONNAIRE (DB)
-- Questions + scoring to assign programme profile
-- ============================================================================
CREATE TABLE IF NOT EXISTS questionnaires (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Core fields
    questionnaire_name TEXT NOT NULL,
    questionnaire_slug TEXT UNIQUE NOT NULL,
    description TEXT,
    
    -- Configuration
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    is_onboarding BOOLEAN DEFAULT false, -- Used during signup
    
    -- Scoring
    scoring_method TEXT DEFAULT 'weighted', -- weighted | simple | branching
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE questionnaires IS 'Questionnaire definitions for profile assignment.';

-- ============================================================================
-- 7a. QUESTIONNAIRE QUESTIONS (DB)
-- Individual questions within a questionnaire
-- ============================================================================
CREATE TABLE IF NOT EXISTS questionnaire_questions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    notion_page_id TEXT UNIQUE,
    
    -- Parent questionnaire
    questionnaire_id UUID NOT NULL REFERENCES questionnaires(id) ON DELETE CASCADE,
    
    -- Question content
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL DEFAULT 'single_choice', -- single_choice | multi_choice | scale | text | yes_no
    
    -- Options (for choice types)
    options JSONB, -- [{"value": "a", "label": "Option A", "score": 1}, ...]
    
    -- Scale config (for scale type)
    scale_min INTEGER DEFAULT 1,
    scale_max INTEGER DEFAULT 5,
    scale_labels JSONB, -- {"1": "Never", "5": "Always"}
    
    -- Scoring
    weight NUMERIC DEFAULT 1.0,
    scoring_map JSONB, -- Maps answers to attribute/profile scores
    
    -- Flow control
    display_order INTEGER DEFAULT 0,
    is_required BOOLEAN DEFAULT true,
    conditional_on JSONB, -- Show only if previous answer matches
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_questionnaire_questions_q ON questionnaire_questions(questionnaire_id);

COMMENT ON TABLE questionnaire_questions IS 'Individual questions within questionnaires.';

-- ============================================================================
-- 8. QUESTIONNAIRE RESPONSES (DB)
-- Stores user answers + resulting profile/weights
-- ============================================================================
CREATE TABLE IF NOT EXISTS questionnaire_responses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- User and questionnaire
    user_id UUID NOT NULL, -- FK to auth.users
    questionnaire_id UUID NOT NULL REFERENCES questionnaires(id),
    
    -- Answers (JSONB for flexibility)
    answers JSONB NOT NULL, -- {"question_id": "answer_value", ...}
    
    -- Computed results
    assigned_profile_id TEXT, -- programme_profiles.notion_page_id
    computed_weights JSONB, -- {"attribute_id": weight, ...}
    safety_flags TEXT[], -- Array of safety rule IDs triggered
    
    -- Metadata
    completed_at TIMESTAMPTZ DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_questionnaire_responses_user ON questionnaire_responses(user_id);
CREATE INDEX idx_questionnaire_responses_q ON questionnaire_responses(questionnaire_id);

COMMENT ON TABLE questionnaire_responses IS 'User questionnaire answers and computed profile assignments.';

-- ============================================================================
-- 9. USER DASHBOARD LAYOUTS (DB)
-- Stores which blocks/packs/controls a user placed
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_dashboard_layouts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- User
    user_id UUID NOT NULL, -- FK to auth.users
    
    -- Layout name (users can have multiple dashboards)
    layout_name TEXT NOT NULL DEFAULT 'Main Dashboard',
    layout_slug TEXT,
    is_default BOOLEAN DEFAULT false,
    
    -- Layout data
    layout_config JSONB NOT NULL DEFAULT '{"blocks": [], "packs": []}',
    -- Structure: {
    --   "blocks": [{"block_id": "uuid", "position": {"x": 0, "y": 0, "w": 6, "h": 2}}],
    --   "packs": ["pack_id_1", "pack_id_2"],
    --   "controls": [{"control_id": "uuid", "position": {...}, "overrides": {...}}]
    -- }
    
    -- User weight overrides
    weight_overrides JSONB, -- {"attribute_id": weight, ...}
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id, layout_slug)
);

CREATE INDEX idx_user_dashboard_layouts_user ON user_dashboard_layouts(user_id);

COMMENT ON TABLE user_dashboard_layouts IS 'User dashboard configurations and customizations.';

-- ============================================================================
-- 10. USER CHECK-INS (DB)
-- Daily entries (the runtime log)
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_checkins (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- User and timing
    user_id UUID NOT NULL, -- FK to auth.users
    checkin_date DATE NOT NULL,
    
    -- Check-in data
    control_values JSONB NOT NULL, -- {"control_id": value, ...}
    
    -- Derived scores (computed from control_values + coupling rules)
    derived_scores JSONB, -- {"metric_slug": score, ...}
    
    -- Completion tracking
    total_controls INTEGER,
    completed_controls INTEGER,
    completion_percentage NUMERIC,
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id, checkin_date)
);

CREATE INDEX idx_user_checkins_user ON user_checkins(user_id);
CREATE INDEX idx_user_checkins_date ON user_checkins(checkin_date);
CREATE INDEX idx_user_checkins_user_date ON user_checkins(user_id, checkin_date);

COMMENT ON TABLE user_checkins IS 'Daily user check-in entries with control values and derived scores.';

-- ============================================================================
-- 11. SESSION RUNS (DB)
-- Instances of generated sessions
-- ============================================================================
CREATE TABLE IF NOT EXISTS session_runs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- User
    user_id UUID NOT NULL, -- FK to auth.users
    
    -- Template reference
    session_template_id TEXT NOT NULL, -- session_templates.notion_page_id
    
    -- Run configuration
    duration_minutes INTEGER NOT NULL,
    strictness TEXT DEFAULT 'normal', -- loose | normal | strict
    persona_id TEXT, -- archetypal_personas.notion_page_id
    
    -- Safety rules applied
    safety_rules_applied TEXT[], -- Array of safety_rules.notion_page_id
    safety_warnings TEXT[],
    
    -- Status
    status TEXT DEFAULT 'generated', -- generated | started | completed | cancelled
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_session_runs_user ON session_runs(user_id);
CREATE INDEX idx_session_runs_template ON session_runs(session_template_id);
CREATE INDEX idx_session_runs_status ON session_runs(status);

COMMENT ON TABLE session_runs IS 'Instances of generated sessions with their configuration.';

-- ============================================================================
-- 12. SESSION OUTPUTS (DB)
-- Stores the produced session plan/script
-- ============================================================================
CREATE TABLE IF NOT EXISTS session_outputs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- Parent run
    session_run_id UUID NOT NULL REFERENCES session_runs(id) ON DELETE CASCADE,
    
    -- Output type
    output_type TEXT NOT NULL DEFAULT 'plan', -- plan | script | audio_plan | full
    
    -- The generated content
    output_data JSONB NOT NULL,
    -- Structure for 'plan' type:
    -- {
    --   "sections": [
    --     {"type": "breathwork", "name": "...", "duration_minutes": 5, "instructions": "...", "cues": [...]},
    --     {"type": "movement", "name": "...", ...}
    --   ],
    --   "total_duration": 15,
    --   "persona_style": "Alan Watts-like"
    -- }
    
    -- Versioning
    version INTEGER DEFAULT 1,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_session_outputs_run ON session_outputs(session_run_id);

COMMENT ON TABLE session_outputs IS 'Generated session plans and scripts.';

-- ============================================================================
-- 13. SYNC EVENTS (for Realtime)
-- Used by CursorBridge to publish content updates
-- ============================================================================
CREATE TABLE IF NOT EXISTS sync_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    event_type TEXT NOT NULL, -- content_synced | content_updated | session_generated
    table_name TEXT NOT NULL,
    record_id TEXT,
    payload JSONB,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE sync_events REPLICA IDENTITY FULL;

CREATE INDEX idx_sync_events_type ON sync_events(event_type);
CREATE INDEX idx_sync_events_created ON sync_events(created_at);

COMMENT ON TABLE sync_events IS 'Realtime sync events for Main App subscription.';

-- ============================================================================
-- Enable Row Level Security (RLS) for user tables
-- ============================================================================
ALTER TABLE user_dashboard_layouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_checkins ENABLE ROW LEVEL SECURITY;
ALTER TABLE questionnaire_responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE session_outputs ENABLE ROW LEVEL SECURITY;

-- RLS Policies (users can only see their own data)
CREATE POLICY "Users can view own dashboard layouts"
    ON user_dashboard_layouts FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own dashboard layouts"
    ON user_dashboard_layouts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own dashboard layouts"
    ON user_dashboard_layouts FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can view own checkins"
    ON user_checkins FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own checkins"
    ON user_checkins FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own checkins"
    ON user_checkins FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can view own questionnaire responses"
    ON questionnaire_responses FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own questionnaire responses"
    ON questionnaire_responses FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own session runs"
    ON session_runs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own session runs"
    ON session_runs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view outputs for own sessions"
    ON session_outputs FOR SELECT
    USING (
        session_run_id IN (
            SELECT id FROM session_runs WHERE user_id = auth.uid()
        )
    );

-- ============================================================================
-- SUMMARY
-- ============================================================================
-- Tables created:
-- 1. control_definitions - Every knob/tick the UI can render
-- 2. control_packs - Curated bundles of controls
-- 3. control_pack_items - Join table for packs ↔ controls
-- 4. profile_pack_map - Programme profiles → default packs
-- 5. default_weights - Baseline weights per profile
-- 6. coupling_rules - How controls influence each other
-- 7. derived_metrics - Computed scores from raw values
-- 8. questionnaires - Questionnaire definitions
-- 9. questionnaire_questions - Questions within questionnaires
-- 10. questionnaire_responses - User answers + computed profiles
-- 11. user_dashboard_layouts - User dashboard configurations
-- 12. user_checkins - Daily check-in entries
-- 13. session_runs - Generated session instances
-- 14. session_outputs - Session plans/scripts
-- 15. sync_events - Realtime sync for Main App
-- ============================================================================

