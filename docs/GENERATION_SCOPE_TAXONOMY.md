# Generation Scope Taxonomy

Last updated: 2026-02-22

Purpose: keep session generation clear across all use-cases, not just therapeutic sessions.

## The 6-Layer Model

Use these layers in this order every time.

1. `Intent` (why): what outcome we want.
2. `Practice Family` (what): the method used.
3. `Delivery Format` (how): what gets generated.
4. `Lens` (explanation style): how it is explained.
5. `Meta Lens` (depth/scope/safety posture): how broad/deep/cautious the explanation is.
6. `Persona + Narration` (voice): how it sounds.

If these are mixed together, the generator becomes confusing.

## Layer 1: Intent (Why)

Primary intent categories:

- Regulation / downshift
- Recovery / restoration
- Sleep support (including insomnia support)
- Focus / clarity
- Activation / energizing
- Emotional processing
- Pain/tension modulation
- Learning / educational
- Reflection / meaning / story

## Layer 2: Practice Family (What)

Practice families:

- Breathwork
- NSDR / deep rest / guided stillness
- Meditation / attention training
- Tapping / EFT
- Movement / somatic practice
- Sound / vibration
- Visualisation / symbolic practice
- Education block (teaching segment)
- Storytelling block (myth, narrative reflection)

Important: one practice can support many intents.

## Layer 3: Delivery Format (How)

Generation output formats:

- Guided session timeline JSON
- Guided narration text script
- Audio-ready cue sheet
- Instructional video script (scene-by-scene)
- On-screen lesson cards
- Short educational explainer blocks
- Reflection prompts / journaling prompts

## Layer 4: Lens (Explanation Style)

Lens decides phrasing and meaning frame, not timeline math.

Examples:

- Clinical
- Western scientific
- Somatic
- TCM
- Spiritual/symbolic
- Hybrid

## Layer 5: Meta Lens (Safety/Depth Posture)

Meta lens decides:

- scope
- depth
- source strictness
- confidence posture

This controls how cautious and how deep the generated explanation is.

## Layer 6: Persona + Narration (Voice)

Persona and narration style decide:

- tone
- pacing
- wording feel
- delivery mood

## Where NSDR Sits (Direct Answer)

NSDR should not be trapped in one category.

- `Practice Family`: `NSDR / deep rest / guided stillness` (primary)
- `Intent` tags: usually `recovery`, `regulation`, `sleep support`
- `Condition` tags: may include `insomnia`, anxiety, stress, overstimulation
- `Delivery Format`: guided audio script, integration block, sleep wind-down script, recovery module

So yes, insomnia can connect to NSDR, but NSDR should live as a reusable practice family.

## Data-Where-It-Counts Checklist

For strong output quality, these are the high-value data anchors:

1. Session structure quality:
   - `session_blueprints`
   - `blueprint_steps`
   - `blueprint_cues`
   - `timing_presets`
   - `session_phases`
   - `transition_rules`

2. Practice quality:
   - `techniques`
   - `technique_steps`
   - `safety_rules`

3. Language quality:
   - `lens_definitions`
   - `meta_lens_presets`
   - `technique_lens_explanations`
   - `narration_styles`
   - `archetypal_personas`

4. Learning/story quality:
   - `knowledge_bases`
   - (future) educational/story content packs linked to technique and lens

5. Output quality:
   - `session_outputs` must carry both structured JSON and readable script text

## Category Placement Rules

Use these rules to avoid category drift:

1. Intent answers: "what result?"
2. Practice family answers: "what method?"
3. Delivery format answers: "what artifact is generated?"
4. Lens/meta-lens/persona answer: "how is it explained and delivered?"
5. Condition tags (like insomnia) are tags, not practice families.

## Advanced Layer (Parked: Mach1.1)

Parked for now:

- user-defined database packs
- user-defined custom wheels
- user-defined category trees

When started, these should be marked as `Mach1.1` and added after core taxonomy stability.

