Part B: Create missing tables (execution layer: timing/phases/transitions/cues/narration_styles/session_blueprints)
Seed the example rows (lens presets, narration styles, blueprint examples)
Never generates sessions for users

Main App (runtime: UI → generate → run → output)
Give Main App this doc (put it in the Main App repo):
/docs/MAIN_APP_RUNTIME_SPEC.md

Its job is only:
Read session_blueprints + related tables
Assemble a timed session plan JSON (phases/steps/cues)
Render to a guided-audio-style script
Write session_runs + session_outputs

Sandbox (optional lane)
You do not need to build Sandbox to run this. When you add it later, it becomes a “generate safely → promote to canonical libraries” lane, but your current deterministic pipeline still stays valid.

Seed rows to add now (lenses + presets + platform example blueprints)

A) lens_definitions (DB) — seed rows (copy as rows; map columns to your existing schema)
Lens Name | Lens Type | Output Style | Primary Purpose | Notes
Spiritual Guide | perspective | spiritual | Meaning/ritual framing without physiology | Use archetypal language, avoid clinical claims
Science Explainer | perspective | scientific | Physiology explanations and mechanisms | Use cautious language, disclaimers if needed
TCM Interpreter | medical_tradition | spiritual/technical | Meridians, organ-emotion framing | Avoid diagnosis; use “traditional framing”
Trauma-Safe Lens | safety | gentle | Soften intensity, add grounding and opt-outs | Default for sensitive profiles
Performance Coach | coaching | direct | Training/recovery optimization framing | Avoid medical claims, emphasize self-monitoring

B) meta_lens_presets (DB) — seed rows (these are what users pick in dropdowns)
Preset Name | Primary Lens | Secondary Lenses | Verbosity | Evidence Tone | Notes
Ritual Calm | Spiritual Guide | Trauma-Safe Lens | normal | low | Default “spiritual session” preset
Clinical Clarity | Science Explainer | Performance Coach | detailed | high | For users wanting mechanism explanations
TCM Body Map | TCM Interpreter | Spiritual Guide | normal | mixed | For meridian/organ-emotion narrative
Ultra-Gentle Regulation | Trauma-Safe Lens | Spiritual Guide | minimal | low | For fragile days
Athlete Recovery Brief | Performance Coach | Science Explainer | minimal | high | Short, practical cues

C) narration_styles (DB) — seed rows (immediately changes “voice” of scripts)
Style Name | Voice Tone | Reading Pace WPM | Breath Verbosity | Physiology Level | TCM Level | Notes
Temple Guide | spiritual | 125 | detailed | none | light | Slow cadence, imagery, soft pacing
Lab Coach | scientific | 150 | normal | full | none | Explanations between cues, still readable
TCM Storyteller | spiritual | 130 | normal | none | full | Meridian/organ-emotion framing, avoid certainty
Minimal Timer | neutral | 160 | minimal | none | none | Mostly timings and short prompts

D) techniques (DB) — ensure these entries exist (if already present, don’t duplicate; just confirm titles match)
Technique Name (Title)
Box Breathing
Fire Breath
NSDR
Wim Hof Breathing (if you separate from generic fire breath)
Water Breath (your term; define clearly)
Mantak Chia: Inner Smile (or whichever you want first)
Mantak Chia: Six Healing Sounds (if included)
Gentle Closing Stretch (movement placeholder)

E) session_blueprints (DB) — “platform examples” that create rich sessions now
Blueprint Name | Timing Preset | Narration Style | Lens Preset | Steps | Cue Pack | Notes
Breath Ladder (Calm→Charge→Deep Rest) | 30-min Rich Mix | Temple Guide | Ritual Calm | Box → Fire → NSDR | Phase Start Calm + Breath Interval Cue | General flagship
Science Breath Ladder (Mechanisms) | 30-min Rich Mix | Lab Coach | Clinical Clarity | Box → WHM → NSDR | Breath Interval Cue | Adds physiology explanations
TCM Regulation + Healing Sounds Close | 20-min Regulation | TCM Storyteller | TCM Body Map | Box → NSDR → Six Healing Sounds | Phase Start Calm | Organ/meridian narrative
Ultra-Gentle Downshift | 20-min Regulation | Temple Guide | Ultra-Gentle Regulation | Box (short) → NSDR (long) | Phase Start Calm | No intense breathwork
Athlete Recovery Reset | 20-min Regulation | Lab Coach | Athlete Recovery Brief | Box → NSDR → Closing Stretch | Interval Cue | Practical recovery framing

Concrete tips so Main App “gets it” and stops drifting

Part B:
A) Add these Lens Presets and Lenses now (seed rows)


lens_definitions (DB) — seed rows
Paste as rows (adapt column names to your table if they differ):


Lens Name | Lens Type | Purpose | Output Tone Defaults | Notes
Physiology (Plain) | Western | Explain what’s happening in the body in simple terms | neutral | No citations required in output
Physiology (Scientific) | Western | Clinical/scientific explanation | scientific | For pro users
TCM (Organs & Meridians) | TCM | Explain via organ systems/meridians | spiritual | Use organ_emotion + meridian systems
Somatic Trauma-Safe | Clinical | Safety-first language, gentle pacing | soft | Avoid intensity spikes
Spiritual Guide | Spiritual | Symbolic, meaning-based narration | spiritual | Uses archetypal + symbols
Performance Coach | Performance | Training/recovery framing | direct | Emphasise protocols + timing
Huberman-style NSDR | Science-Comm | Clear structure + practical cues | neutral | Keep jargon light
Mantak Chia (Microcosmic Orbit) | TCM/Daoist | Daoist framing and intent | spiritual | References movements_system rows you’ve built
Breathwork Teacher | Practice | Breath instruction clarity + pacing | neutral | Works across techniques
Minimalist | Minimal | Few words, longer silences | neutral | For users who dislike talk


meta_lens_presets (DB) — seed rows
Preset Name | Primary Lens | Secondary Lenses | Default Narration Style | Notes
Balanced Wellness | Physiology (Plain) | Breathwork Teacher | Science Coach | Good default
Spiritual Ritual | Spiritual Guide | TCM (Organs & Meridians) | Spiritual Guide | Symbol-heavy
Trauma-Safe Regulation | Somatic Trauma-Safe | Minimalist | Spiritual Guide | Low intensity, long pauses
Athlete Recovery | Performance Coach | Physiology (Plain) | Science Coach | Recovery framing
TCM Energy Flow | TCM (Organs & Meridians) | Mantak Chia (Microcosmic Orbit) | Spiritual Guide | Organ/meridian cues
NSDR Protocol | Huberman-style NSDR | Physiology (Plain) | Science Coach | Strict structure
Scientific Deep Dive | Physiology (Scientific) | Breathwork Teacher | Science Coach | For clinician/researcher view
Minimal Words | Minimalist | Physiology (Plain) | Spiritual Guide | Sparse narration


B) Add “platform example” Session Blueprints (seed rows)
These are your “fun, rich, dropdown-driven” examples that prove the system works without AI.


session_blueprints (DB) — seed rows
Blueprint Name | Programme Profile | Archetypal Persona | Lens Preset | Timing Preset | Narration Style | Steps | Cue Pack | Safety Rules | Notes
Breath Ladder: Box → Fire → NSDR → TCM Close | General Wellness | (choose) | Balanced Wellness | 30-min Rich Mix | Spiritual Guide | link to technique_steps (4) | link Phase Start Calm + Breath Interval Cue | baseline safety | Good demo
Trauma-Safe Settle + Long Exhale + NSDR | Trauma-Safe Regulation | (choose) | Trauma-Safe Regulation | 20-min Regulation | Minimal Words | link 2–3 steps | Phase Start Calm only | trauma-safe safety | No intensity
NSDR Only (Strict) | Breath-Only | (choose) | NSDR Protocol | 20-min Regulation | Science Coach | NSDR step only | interval cue optional | baseline safety | Deterministic script
Athlete Downshift: CO2 Tolerance → Soft Stretch | Athlete | (choose) | Athlete Recovery | 30-min Rich Mix | Science Coach | link 2–3 steps | interval cue | baseline safety | Recovery-centric
TCM Liver Soothe: Breath + Meridian + Movement | General Wellness | (choose) | TCM Energy Flow | 30-min Rich Mix | Spiritual Guide | link 3–4 steps | cues include organ/meridian | baseline safety | Your “organs/colour/sound” test


technique_steps (DB) — add a few more ready-made sequences


Step Name | Technique | Phase Template | Min Duration Sec | Max Duration Sec | Intensity Target | Transition Rule | Notes
Long Exhale Breathing | (link technique) | Breath Technique Phase | 240 | 600 | low | Soft Fade | Great for trauma-safe
CO2 Tolerance (Gentle) | (link technique) | Breath Technique Phase | 180 | 360 | med | Counted Pause | Keep safety rules strict
Body Scan (NSDR Adjacent) | (link technique) | Integration | 420 | 900 | low | Soft Fade | Works even without “Huberman” branding
Meridian Tap Sequence | (link technique or movements_system) | Integration | 180 | 360 | low | Soft Fade | TCM add-on
Microcosmic Orbit Primer | (link technique) | Integration | 180 | 480 | low | Soft Fade | Mantak Chia lens shines here
Closing Stillness | (link technique) | Outro | 90 | 240 | low | Soft Fade | Always ends cleanly


cue_triggers (DB) — make cues actually pull multiple DBs


Trigger Name | Trigger Scope | Interval Sec | Sound | Light/Colour | Symbol | Sacred Geometry | Organ-Emotion | Meridian | Chakra | Notes
Phase Start Ritual | phase_start | (null) | (pick 1) | (pick 1) | (pick 1) | (pick 1) | (pick 1) | (pick 1) | (pick 1) | Proves “full array” works
Liver Emphasis Interval | interval | 60 | (pick) | Green | (pick) | (pick) | Liver | Liver meridian | (pick) | Use with TCM blueprint
NSDR Soft Reminder | interval | 90 | (optional) | (optional) | (optional) | (optional) | (optional) | (optional) | (optional) | “Return to breath…”
Transition Bell | phase_end | (null) | (pick) | (optional) | (optional) | (optional) | (optional) | (optional) | (optional) | End-of-phase marker
C) Exactly which document goes to Bridge vs Main App


Give this to the Bridge / Operator App (ETL + schema + seeding)
Document name: SECTION_3_EXECUTION_FOR_BRIDGE.md
Contents (only):
The list of new tables to create (timing_presets, session_phases, technique_steps, transition_rules, cue_triggers, narration_styles, session_blueprints) plus the seed rows above for:
lens_definitions, meta_lens_presets, technique_steps, cue_triggers, session_blueprints.


Bridge’s job ends at: “tables exist + rows inserted + relationships valid”.


Give this to the Main App (runtime generation)
Document name: SESSION_GENERATION_RUNTIME_SPEC.md
Contents (only):
How to expand blueprint → timed phases → cues → narration → write session_runs + session_outputs, plus the “minimum acceptance test” below.


Do not give the Main App the schema-creation instructions. That’s why it keeps thrashing.
D) Concrete tips so Main App “gets it” and you can test for real
Minimum acceptance test (do this exactly)


Pick blueprint “TCM Liver Soothe: Breath + Meridian + Movement”


Generate 30 minutes


Output must contain:
A) A phase list with start/end timestamps summing to 30:00
B) At least 1 cue at phase_start pulling from at least 3 of: sound, colour, organ, symbol
C) At least 1 interval cue firing during a phase
D) A readable guided narration render (not just JSON)


Runtime rules Main App must follow (non-negotiable)


Blueprint is the “session configuration object”. Session templates are recipes; blueprints are what users pick.


The generator must allocate time first (timeline), then render text second (narration).


Cues are not “extra content”. They are scheduled events on the timeline.


Lens preset affects phrasing only; it must not change the underlying schedule.


If you want, I can now produce the two documents (Bridge execution doc + Main App runtime spec) as clean copy-paste text blocks in your preferred handover format.
