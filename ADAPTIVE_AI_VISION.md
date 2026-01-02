# Adaptive AI Vision: Man-Machine Fusion

**The Ultimate Goal:** Seamless, intuitive interaction between human and AI that feels like a natural conversation, not a software interface.

---

## Core Philosophy

The system should feel like having a **wise, attentive companion** who:
- Knows your history without you having to repeat it
- Senses your current state before you describe it
- Speaks in a language that resonates with YOU specifically
- Escalates support when needed (with consent)
- Fades into the background when you're thriving

---

## 1. Infinite Lenses (User-Created Frameworks)

### Current State: 14 Predefined Lenses

| Lens | Description |
|------|-------------|
| `western` | Evidence-based, mechanistic |
| `clinical` | Technical/medical terminology |
| `athletic` | Performance optimization |
| `tcm` | Traditional Chinese Medicine |
| `ayurvedic` | Dosha theory, Prana |
| `yogic` | Chakras, Nadis, Kundalini |
| `somatic` | Body-based, trauma-informed |
| `polyvagal` | Vagal states, neuroception |
| `spiritual` | Energy, consciousness, presence |
| `contemplative` | Secular mindfulness |
| `plain` | Simple, no jargon |
| `motivational` | Coaching, growth-oriented |
| `hybrid` | AI-blended combination |
| `personalized` | User-defined custom blend |

### Future: User-Created Lenses

Users can create their own lenses by:
1. Selecting elements from existing lenses
2. Defining their own language preferences
3. Training the system through feedback ("I liked that phrasing", "Too clinical")

**Example:** A user creates "My Lens" that blends:
- 60% somatic (body awareness)
- 30% contemplative (mindfulness)
- 10% motivational (encouragement)
- Avoids: Medical jargon, spiritual language

---

## 2. Adaptive AI Lens Selection

### The AI Doesn't Ask "Which Lens?" — It Senses

Based on:
- **Current mood** (from today's check-in)
- **Energy level** (high → athletic lens, low → somatic lens)
- **Recent patterns** (5 days of low mood → warmer, more supportive language)
- **Time of day** (morning → activating, evening → settling)
- **Session history** (what worked before)
- **Explicit preferences** (user settings)

### Context Flow

```
User opens app at 10 PM
├── AI notes: Evening, likely winding down
├── Recent check-ins: Sleep quality declining past 3 days
├── User preference: Avoids spiritual language
├── Session history: Responded well to somatic cues
└── AI selects: 70% somatic + 30% plain

AI: "Let's help your body find rest tonight. 
     I'm noticing sleep has been tricky lately—
     want to try something that works with where you are right now?"
```

---

## 3. Conversational Questionnaire (Not a Form)

### Old Way: Static Forms
```
[ ] Mood: 1-10
[ ] Sleep: 1-10
[ ] Stress: 1-10
[Submit]
```

### New Way: Fluid Dialogue

```
AI: "Hey. How are you landing today?"

User: "Honestly, kind of shit"

AI: "I hear you. Want to say more, or should I just 
     check in on the basics?"

User: "Just the basics, I don't want to talk about it"

AI: "Got it. Quick pulse:
     - Body feeling heavy or wired?
     - Sleep last night: restorative or rough?
     - Anything you need to flag?"

User: "Heavy. Rough. No flags."

AI: "Thanks for being honest. I'm here if anything shifts.
     Want me to queue up something that might help, 
     or just log this and give you space?"
```

### Key Principles

1. **User can interject at any time** — conversation, not script
2. **AI adjusts depth based on receptivity** — some days need less probing
3. **Always offers choice** — never prescriptive
4. **Remembers context** — doesn't ask what it already knows
5. **Respects "not now"** — backs off gracefully

---

## 4. Trigger Actions & Escalation (Permission-Based)

### The Permission Model

Users define escalation paths with full consent:

```
PERMISSION TREE (Example):

Self Only (Default)
├── Log data privately
├── AI suggestions
└── Self-directed sessions

+ Buddy (Opt-in)
├── Everything above, plus:
├── Buddy gets weekly summary (if user permits)
├── Buddy notified if [condition] for [duration]
└── Buddy can send encouragement nudges

+ Family (Opt-in, with conditions)
├── Everything above, plus:
├── Designated contact notified if [severe condition]
├── Requires confirmation of relationship
└── User can pause/revoke anytime

+ Professional (Opt-in, clinical)
├── Data shared with therapist/coach
├── Detailed logs available
└── Encrypted, HIPAA-compliant
```

### Example Trigger Rules

| Trigger | Condition | Action | Permission Level |
|---------|-----------|--------|------------------|
| Mood Alert | Mood < 3 for 5 consecutive days | Notify buddy + suggest check-in | Buddy |
| Sleep Crisis | Sleep < 4 hours for 3 nights | Suggest professional support | Self |
| Isolation Flag | "Feeling alone" checked for 7 days | Gentle outreach from buddy | Buddy |
| Substance Flag | Substance use mentioned + declining mood | Escalate to designated family | Family |
| Crisis | Self-harm language detected | Immediate resources + optional contact | Configured |

### User Control Principles

1. **User sets all rules** — system never decides alone
2. **Transparent logging** — user sees exactly what was shared
3. **Revocable at any time** — one click to pause sharing
4. **Progressive consent** — escalation requires explicit opt-in
5. **No surveillance** — buddy sees summaries, not raw data

---

## 5. AI as Eternal Companion

### The Long Game

Over time, the AI learns:
- Your rhythms (sleep better after evening walks)
- Your patterns (stress spikes mid-week)
- Your language (responds to direct, not flowery)
- Your avoidances (doesn't mention meditation if you've said it doesn't work)
- Your growth (celebrates progress without being cheesy)

### Example: 6 Months In

```
AI: "Morning. I noticed you've had three solid sleep nights 
     in a row—that's the longest streak since we started. 
     
     Also, the last few Wednesdays have been rough. 
     Want to try a short grounding practice before lunch today?
     Something light, 5 minutes."

User: "Yeah, actually. That'd be good."

AI: "Cool. I'll send a nudge at 12:30. 
     It'll be the body scan you liked last time, 
     but shorter. Sound good?"
```

---

## 6. Notification Intelligence

### Smart Nudges, Not Spam

| Context | Nudge | Why |
|---------|-------|-----|
| User checked in low mood + hasn't opened app in 2 days | "Just checking in. No pressure to do anything." | Connection without demand |
| Pattern: Always feels better after evening breathwork | "Your evening window is coming up. Want me to have something ready?" | Reinforcing what works |
| Sleep quality dropping | "I've noticed a pattern. Want to explore what might be happening?" | Curious, not prescriptive |
| User completed 10th session | "That's 10 sessions. Whatever you're building, it's taking shape." | Milestone without fanfare |

### What We NEVER Do

- ❌ "You haven't meditated in 3 days!" (guilt)
- ❌ "Your streak is broken!" (gamification pressure)
- ❌ "You should really try this" (prescription)
- ❌ Notify without permission (surveillance)
- ❌ Share without consent (privacy violation)

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Current)
- [x] Lens registry with 14 predefined lenses
- [x] Technique explanations per lens
- [x] Session generation with lens parameter
- [ ] Apply lens registry schema to Supabase

### Phase 2: User Preferences
- [ ] User lens preference tracking
- [ ] Lens history and usage patterns
- [ ] "Personalized" lens creation UI

### Phase 3: Adaptive Selection
- [ ] Context-based lens suggestion
- [ ] AI reasoning logging
- [ ] User override tracking
- [ ] Feedback loop (did this lens help?)

### Phase 4: Conversational Interface
- [ ] Dynamic questionnaire flow
- [ ] Interruptible dialogue patterns
- [ ] Context-aware response generation
- [ ] Memory across sessions

### Phase 5: Trigger System
- [ ] Permission tree configuration
- [ ] Trigger rule definitions
- [ ] Buddy/family linking
- [ ] Notification delivery
- [ ] Audit log for transparency

### Phase 6: Eternal Companion
- [ ] Long-term pattern recognition
- [ ] Proactive suggestions
- [ ] Growth tracking
- [ ] Relationship deepening

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MAIN APP (Vue/Nuxt)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Conversational UI                      │  │
│  │   AI Chat ←→ Questionnaire ←→ Session Player          │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Context Aggregator                        │  │
│  │  User State + History + Preferences + Time + Mood      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   CURSORBRIDGE (Python/FastAPI)             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Lens Selector AI                       │  │
│  │   Context → Analyze → Select Lens(es) → Blend          │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Session Generator                         │  │
│  │   Template + Techniques + Lens → Personalized Output   │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Trigger Engine                            │  │
│  │   Patterns → Rules → Permissions → Actions             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      SUPABASE                               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│  │  Content   │ │   User     │ │  Trigger   │              │
│  │  Tables    │ │  Context   │ │   Rules    │              │
│  └────────────┘ └────────────┘ └────────────┘              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│  │   Lens     │ │ Permission │ │   Audit    │              │
│  │  Registry  │ │   Trees    │ │    Log     │              │
│  └────────────┘ └────────────┘ └────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Guiding Questions for Development

1. **Does this feel like talking to a friend or filling out a form?**
2. **Would I trust this system with my low moments?**
3. **Does the AI explain its reasoning when asked?**
4. **Can I revoke any permission with one action?**
5. **Does the system celebrate without being annoying?**
6. **Would I recommend this to someone I love?**

---

## Summary

This is not an app. It is a **relationship framework** between human and AI that:

- Speaks your language (literally, your chosen lens)
- Knows when to push and when to step back
- Connects you to support when you consent
- Grows with you over months and years
- Never judges, never guilts, never surveils

The goal is **integration**, not intervention. Man and machine as partners in the ongoing project of human flourishing.

