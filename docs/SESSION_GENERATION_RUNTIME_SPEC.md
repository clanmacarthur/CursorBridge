# Session Generation Runtime Spec
**For: Main App**
**Purpose: Generate sessions from blueprints at runtime**

---

## 🎯 YOUR JOB (Main App Only)

1. **Read** session_blueprints + related tables
2. **Assemble** a timed session plan JSON (phases/steps/cues)
3. **Render** to guided-audio-style script
4. **Write** session_runs + session_outputs

> ⚠️ You do NOT create tables or seed data. Bridge handles that.

---

## 📊 TABLES YOU READ FROM

| Table | What You Get |
|-------|--------------|
| `session_blueprints` | The recipe users pick |
| `blueprint_steps` | Ordered technique steps |
| `blueprint_cues` | Scheduled audio/visual cues |
| `technique_steps` | Duration + intensity for each step |
| `timing_presets` | Total duration + phase percentages |
| `narration_styles` | Voice tone, pace, verbosity |
| `meta_lens_presets` | How to phrase explanations |
| `cue_triggers` | What happens at phase start/end/interval |

---

## 📝 TABLES YOU WRITE TO

| Table | What You Write |
|-------|----------------|
| `session_runs` | User's session record |
| `session_outputs` | Generated timeline, narration, cues |

---

## 🔄 GENERATION FLOW

```
User picks blueprint
       ↓
┌──────────────────────────────────────────┐
│ 1. LOAD BLUEPRINT                        │
│    - Fetch blueprint + related rows      │
│    - Get timing_preset (total duration)  │
│    - Get narration_style (voice/pace)    │
│    - Get lens_preset (explanation style) │
└──────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│ 2. ALLOCATE TIME (Timeline First!)       │
│    - Calculate phase durations from %    │
│    - Place steps within phases           │
│    - Total MUST equal timing_preset mins │
└──────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│ 3. SCHEDULE CUES                         │
│    - phase_start cues at phase begins    │
│    - interval cues repeat every N sec    │
│    - phase_end cues at phase ends        │
└──────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│ 4. RENDER NARRATION                      │
│    - Apply narration_style (WPM, tone)   │
│    - Apply lens_preset (phrasing)        │
│    - Generate spoken text for each cue   │
└──────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│ 5. WRITE OUTPUT                          │
│    - Create session_runs row             │
│    - Write session_outputs (JSON + text) │
└──────────────────────────────────────────┘
```

---

## 📐 OUTPUT FORMAT: Timeline JSON

```json
{
  "session_id": "uuid",
  "blueprint_id": "uuid",
  "total_duration_sec": 1800,
  "phases": [
    {
      "phase_name": "Welcome & Grounding",
      "phase_type": "intro",
      "start_sec": 0,
      "end_sec": 144,
      "duration_sec": 144,
      "steps": [],
      "cues": [
        {
          "time_sec": 0,
          "type": "phase_start",
          "narration": "Welcome. Find a comfortable position..."
        }
      ]
    },
    {
      "phase_name": "Box Breathing",
      "phase_type": "technique",
      "start_sec": 144,
      "end_sec": 594,
      "duration_sec": 450,
      "steps": [
        {
          "step_name": "Box Breathing",
          "technique": "Box Breathing",
          "intensity": "low",
          "instructions": "Breathe in for 4 counts..."
        }
      ],
      "cues": [
        {
          "time_sec": 144,
          "type": "phase_start",
          "narration": "Beginning box breathing now..."
        },
        {
          "time_sec": 234,
          "type": "interval",
          "narration": "Continue this rhythm..."
        }
      ]
    }
  ]
}
```

---

## 📜 OUTPUT FORMAT: Narration Text

```
[00:00] Welcome. Find a comfortable position, either seated or lying down.

[00:15] Allow your eyes to close gently. Take a moment to arrive.

[02:24] Beginning box breathing now. 
        Inhale for four counts... hold for four... 
        exhale for four... hold for four.

[03:54] Continue this rhythm. Notice how each breath brings more calm.

[09:54] Transitioning now to deeper rest...
```

---

## 🎚️ LENS AFFECTS PHRASING ONLY

Same step, different lenses:

| Lens | Narration |
|------|-----------|
| `physiology_plain` | "This activates your parasympathetic nervous system, slowing your heart rate." |
| `tcm_organs_meridians` | "Feel the liver qi soften, green light flowing through your right side." |
| `spiritual` | "With each exhale, release what no longer serves you." |
| `minimalist` | "Breathe. Rest." |

> **Rule:** Lens changes words, NOT the timeline or duration.

---

## ⏱️ TIMING RULES (Non-Negotiable)

1. **Timeline first, narration second**
   - Calculate all durations before generating text
   
2. **Phase durations must sum to total**
   - `intro + technique + integration + outro = timing_preset.total_duration_min`
   
3. **Cues are scheduled events**
   - They have specific timestamps
   - They are not "extra content"
   
4. **Respect min/max durations**
   - Each technique_step has min_duration_sec and max_duration_sec
   - Stay within bounds

---

## 🧪 MINIMUM ACCEPTANCE TEST

### Test Blueprint: "TCM Liver Soothe: Breath + Meridian + Movement"

**Generate 30 minutes** and verify:

- [ ] **A)** Phase list with start/end timestamps summing to 30:00
- [ ] **B)** At least 1 cue at phase_start pulling from 3+ of: sound, colour, organ, symbol
- [ ] **C)** At least 1 interval cue firing during a phase
- [ ] **D)** A readable guided narration render (not just JSON)

### Example API Call

```bash
POST /api/sessions/generate
{
  "blueprint_id": "tcm-liver-soothe-uuid",
  "user_id": "user-uuid",
  "duration_override_min": 30
}
```

### Expected Response

```json
{
  "session_run_id": "uuid",
  "timeline": { /* see format above */ },
  "narration_text": "/* readable script */",
  "total_duration_sec": 1800,
  "phases_count": 4,
  "cues_count": 12
}
```

---

## 🔗 API ENDPOINTS TO CALL (Bridge)

| Endpoint | What You Get |
|----------|--------------|
| `GET /api/query/session_blueprints` | List all blueprints |
| `GET /api/query/timing_presets` | Duration options |
| `GET /api/query/narration_styles` | Voice options |
| `GET /api/query/meta_lens_presets` | Lens presets |
| `GET /api/query/technique_steps` | Step library |
| `POST /sandbox/generate-session` | Full generation (if using sandbox) |

---

## ❌ WHAT YOU MUST NOT DO

1. ❌ Create or modify schema (Bridge does this)
2. ❌ Seed data (Bridge does this)
3. ❌ Change timeline based on lens (lens = phrasing only)
4. ❌ Generate without allocating time first
5. ❌ Skip the acceptance test

---

## ✅ CHECKLIST BEFORE RELEASE

- [ ] Can load any blueprint and generate valid timeline
- [ ] Phase durations sum correctly to total
- [ ] Cues appear at scheduled timestamps
- [ ] Narration changes with lens_preset
- [ ] session_runs written after completion
- [ ] session_outputs contains both JSON and text

---

*Document generated by CursorBridge for Main App integration.*
*Last updated: January 2, 2025*

